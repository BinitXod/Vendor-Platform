from typing import Any
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.vendor import vendor_repo
from app.schemas.report import VendorReport
from app.services.ai import generate_recommendation_report, generate_work_query_embedding
from app.services.work_requirement import work_requirement_service
from app.utils.logger import logger


class RecommendationService:
    @staticmethod
    async def get_recommendations(db: AsyncSession, work_req_id: UUID) -> list[dict[str, Any]]:
        # 1. Fetch the work requirement
        work_req = await work_requirement_service.get_work_requirement(db, work_req_id)
        if not work_req:
            raise ValueError("Work Requirement not found")

        # 2. Generate vector for the work description
        search_text = f"Category: {work_req.category}. Task: {work_req.description}"
        query_vector = await generate_work_query_embedding(search_text)

        if not query_vector:
            raise ValueError("Failed to generate AI embedding for the work requirement")

        # 3. Fetch eligible vendors and similarity scores from the repository
        rows = await vendor_repo.get_recommendation_candidates(
            db,
            location=work_req.location,
            query_vector=query_vector
        )

        # 4. Soft Scoring (Deterministic calculation out of 100)
        recommendations = []
        for vendor, distance in rows:
            # Semantic Score (40 pts) -> Cosine similarity is (1 - distance)
            similarity = max(0.0, 1.0 - distance)
            semantic_score = similarity * 40.0

            # Rating Score (30 pts) -> (rating / 5.0) * 30
            rating_score = (vendor.rating / 5.0) * 30.0 if vendor.rating else 0.0

            # Budget Fit Score (30 pts)
            budget_score = 0.0
            if vendor.max_budget_capacity:
                if vendor.max_budget_capacity >= work_req.estimated_value:
                    budget_score = 30.0
                else:
                    # Partial points if they are smaller than the required budget
                    ratio = vendor.max_budget_capacity / work_req.estimated_value
                    budget_score = ratio * 30.0

            total_score = round(semantic_score + rating_score + budget_score, 2)

            recommendations.append({
                "vendor_id": str(vendor.id),
                "name": vendor.name,
                "category": vendor.category,
                "score": total_score,
                "breakdown": {
                    "semantic_match_score": round(semantic_score, 2),
                    "rating_score": round(rating_score, 2),
                    "budget_score": round(budget_score, 2)
                },
                "contact_email": vendor.contact_email
            })

        # 5. Sort by highest score first
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations

    @staticmethod
    async def trigger_report(redis_pool: Any, work_req_id: UUID) -> dict[str, Any]:
        if not redis_pool:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Queue service unavailable.")

        await redis_pool.enqueue_job("generate_report_task", work_req_id)
        return {
            "message": "Report generation started in the background. Operations team will be notified upon completion.",
            "work_requirement_id": work_req_id
        }

    @staticmethod
    async def generate_report(db: AsyncSession, work_req_id: UUID) -> VendorReport | None:
        """Build the structured VendorReport for a work requirement."""
        work_req = await work_requirement_service.get_work_requirement(db, work_req_id)
        if not work_req:
            logger.error("Work requirement not found in worker.")
            return None

        recommendations = await RecommendationService.get_recommendations(db, work_req_id)
        if not recommendations:
            logger.warning(f"No recommendations for work_req {work_req_id}; skipping report.")
            return None

        top_3 = recommendations[:3]

        logger.info("Calling Gemini for structured vendor report...")
        return await generate_recommendation_report(
            work_requirement_id=str(work_req_id),
            work_title=work_req.title,
            work_desc=work_req.description,
            estimated_value=work_req.estimated_value,
            top_vendors=top_3,
        )


recommendation_service = RecommendationService()

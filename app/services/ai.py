import json
from google import genai
from typing import List, Optional
from app.config.settings import settings
from app.schemas.report import VendorReport
from app.utils.logger import logger

# Initialize the new SDK client
# It will automatically pick up GEMINI_API_KEY from environment,
# but passing it explicitly from our Pydantic settings is safer for production.
client = genai.Client(api_key=settings.GEMINI_API_KEY)

async def generate_vendor_embedding(text: str) -> Optional[List[float]]:
    """
    Generates a 768-dimensional vector embedding for a vendor using Gemini.
    Uses the native async interface (client.aio).
    """
    if not text or not text.strip():
        return None

    try:
        # Using the async client
        result = await client.aio.models.embed_content(
            model=settings.GEMINI_EMBEDDING_MODEL,
            contents=text,
            config={
                'task_type': 'RETRIEVAL_DOCUMENT',
                'output_dimensionality': settings.GEMINI_EMBEDDING_DIMENSIONS
            }
        )
        return result.embeddings[0].values
    except Exception as e:
        logger.error(f"Failed to generate embedding: {e}")
        return None


async def generate_work_query_embedding(text: str) -> Optional[List[float]]:
    """Generates an embedding for a work requirement (Search Query)."""
    if not text or not text.strip():
        return None

    try:
        result = await client.aio.models.embed_content(
            model=settings.GEMINI_EMBEDDING_MODEL,
            contents=text,
            config={
                'task_type': 'RETRIEVAL_QUERY', # Optimized for search queries
                'output_dimensionality': settings.GEMINI_EMBEDDING_DIMENSIONS
            }
        )
        return result.embeddings[0].values
    except Exception as e:
        logger.error(f"Failed to generate query embedding: {e}")
        return None


async def generate_recommendation_report(
    work_requirement_id: str,
    work_title: str,
    work_desc: str,
    estimated_value: float,
    top_vendors: list,
) -> Optional[VendorReport]:
    """
    Generate a **structured** vendor justification report via Gemini.

    Uses Gemini's JSON-mode with a Pydantic response_schema so the model is
    forced to return output matching `VendorReport` — no fragile string parsing.
    """
    if not top_vendors:
        return None

    prompt = f"""
You are a procurement analyst preparing a vendor recommendation report for an
operations team. Base every claim on the data provided — do not invent vendors,
scores, or contact details.

WORK REQUIREMENT
- id: {work_requirement_id}
- title: {work_title}
- description: {work_desc}
- estimated_value: {estimated_value}

TOP VENDORS (already ranked by our internal 40/30/30 score)
{json.dumps(top_vendors, indent=2)}

Produce the report as JSON matching the provided schema:
- `headline` — one-line takeaway an executive can read in 3 seconds.
- `executive_summary` — 2–3 sentences on the decision and its rationale.
- `primary_recommendation` — the top-scoring vendor with a substantive
  justification (mention semantic fit, rating, and budget headroom explicitly)
  and any vendor-specific risks (budget, rating, capacity, etc.).
- `alternatives` — up to 2 runner-ups, best first, each with a shorter
  justification and their own risks.
- `overall_risks` — cross-cutting concerns not tied to a single vendor
  (e.g. thin candidate pool, low semantic scores across the board).
- `confidence` — LOW / MEDIUM / HIGH, reflecting score spread and data quality.

Set `work_requirement_id` to "{work_requirement_id}" exactly.
""".strip()

    try:
        result = await client.aio.models.generate_content(
            model=settings.GEMINI_GENERATION_MODEL,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": VendorReport,
                "temperature": 0.2,
            },
        )

        parsed = getattr(result, "parsed", None)
        if isinstance(parsed, VendorReport):
            return parsed
        # Fallback: parse the raw JSON text if the SDK didn't auto-parse.
        return VendorReport.model_validate_json(result.text)
    except Exception as e:
        logger.error(f"Failed to generate structured vendor report: {e}")
        return None
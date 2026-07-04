from fastapi import APIRouter
from app.api.v1.endpoints import health, vendors, work_requirements, recommendations

api_router = APIRouter()

api_router.include_router(health.router, tags=["System"])
api_router.include_router(vendors.router, prefix="/vendors", tags=["Vendors"])
api_router.include_router(work_requirements.router, prefix="/work-requirements", tags=["Work Requirements"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
from app.models.work_requirement import WorkRequirement
from app.repository.base import BaseRepository
from app.schemas.work_requirement import WorkRequirementCreate, WorkRequirementUpdate


class RepositoryWorkRequirement(
    BaseRepository[WorkRequirement, WorkRequirementCreate, WorkRequirementUpdate]
):
    pass


work_req_repo = RepositoryWorkRequirement(WorkRequirement)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.v1.dependencies import get_current_user, require_admin
from app.db.session import get_db
from app.schemas.job_template import JobTemplateCreate, JobTemplateResponse, JobTemplateUpdate
from app.schemas.response import APIResponse
from app.services.job_template import JobTemplateService
from app.models.user import User


job_template_router = APIRouter(prefix="/job-templates", tags=["Job Templates"])

@job_template_router.get("", response_model=APIResponse[list[JobTemplateResponse]], dependencies=[Depends(get_current_user), Depends(require_admin)])
def get_job_templates(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    data = JobTemplateService.get_job_templates(db)
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Job templates retrieved successfully",
        data=data,
        error=None
    )


@job_template_router.get("/{template_id}", response_model=APIResponse[JobTemplateResponse], dependencies=[Depends(get_current_user), Depends(require_admin)])
def get_job_template(template_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    data = JobTemplateService.get_job_template_by_id(db, template_id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job template not found")
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Job template retrieved successfully",
        data=data,
        error=None
    )


@job_template_router.post("", response_model=APIResponse[JobTemplateResponse], dependencies=[Depends(require_admin), Depends(get_current_user)])
def create_job_template(
    payload: JobTemplateCreate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)
):
    
    data = JobTemplateService.create_job_template(db, payload, created_by=current_user.id)

    return APIResponse(
        status_code=status.HTTP_201_CREATED,
        message="Job template created successfully",
        data=data,
        error=None
    )


@job_template_router.put("/{template_id}", response_model=APIResponse[JobTemplateResponse], dependencies=[Depends(require_admin), Depends(get_current_user)])
def update_job_template(template_id: UUID, payload: JobTemplateUpdate, db: Session = Depends(get_db)):
    data = JobTemplateService.update_template(db, template_id, payload)
    
    return APIResponse(
        status_code=status.HTTP_200_OK,
        message="Job template updated successfully",
        data=data,
        error=None
    )


@job_template_router.delete("/{template_id}", response_model=APIResponse[None], dependencies=[Depends(require_admin), Depends(get_current_user)])
def delete_job_template(template_id: UUID, db: Session = Depends(get_db)):
    JobTemplateService.delete_template(db, template_id)
    return APIResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        message="Job template deleted successfully",
        data=None,
        error=None
    )
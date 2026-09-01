from datetime import datetime, timezone
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.skills_utils import merge_skills
from app.models.job_template import JobTemplate
from app.repository.job_template import (
    create_job_template,
    delete_job_template,
    get_job_template_by_id,
    get_job_templates,
    update_job_template,
)
from app.schemas.job_template import JobTemplateCreate, JobTemplateUpdate


class JobTemplateService:

    @staticmethod
    def get_job_templates(db: Session):
        data = get_job_templates(db)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No job templates found")
        return data

    @staticmethod
    def get_job_template_by_id(db: Session, job_template_id: UUID):
        data = get_job_template_by_id(db, job_template_id)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job template not found")
        return data

    @staticmethod
    def create_job_template(db: Session, payload: JobTemplateCreate, created_by: UUID):
        if payload.skills:
            seen_skills = set()
            for skill_dict in payload.skills:
                for skill_id in skill_dict.keys():
                    if skill_id in seen_skills:
                        raise HTTPException(
                            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Duplicate skill selected: {skill_id}. Each skill can only be added once.",
                        )
                    seen_skills.add(skill_id)
        try:
            data = create_job_template(db=db, created_by=created_by, payload=payload)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        return data

    @staticmethod
    def update_template(db: Session, template_id: UUID, payload: JobTemplateUpdate):
        template = get_job_template_by_id(db, template_id)
        if not template:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job template not found")

        update_data = payload.model_dump(exclude_unset=True)

        if "skills" in update_data:
            new_skills = update_data["skills"]
            if new_skills:
                seen_skills = set()
                for skill_dict in new_skills:
                    for skill_id in skill_dict.keys():
                        if skill_id in seen_skills:
                            raise HTTPException(
                                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail=f"Duplicate skill selected: {skill_id}. Each skill can only be added once.",
                            )
                        seen_skills.add(skill_id)
            update_data["skills"] = merge_skills(template.skills, new_skills)

        for key, value in update_data.items():
            setattr(template, key, value)

        return update_job_template(db, template)

    @staticmethod
    def delete_template(db: Session, template_id: UUID) -> None:
        template = get_job_template_by_id(db, template_id)
        if not template:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job template not found")
        template.deleted_at = datetime.now(timezone.utc)
        delete_job_template(db, template)
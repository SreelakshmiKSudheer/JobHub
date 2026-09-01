from sqlalchemy.orm import Session
from uuid import UUID

from app.models.job_template import JobTemplate
from app.schemas.job_template import JobTemplateCreate

def get_job_templates(db: Session):
    return db.query(JobTemplate).filter(JobTemplate.deleted_at.is_(None)).all()

def get_job_template_by_id(db: Session, job_template_id: UUID):
    return db.query(JobTemplate).filter(JobTemplate.id == job_template_id, JobTemplate.deleted_at.is_(None)).one_or_none()

def create_job_template(db: Session, payload: JobTemplateCreate, created_by: UUID):
    formatted_skills = None
    if payload.skills:
        formatted_skills = [
            {str(key): value.value for key, value in skill_dict.items()} 
            for skill_dict in payload.skills
        ]

    template = JobTemplate(
        **payload.model_dump(exclude={"skills"}),
        skills=formatted_skills,
        created_by=created_by,
    )
    
    db.add(template)
    db.commit()
    db.refresh(template)
    
    return template

def update_job_template(db: Session, template: JobTemplate):
    db.commit()
    db.refresh(template)
    return template

def delete_job_template(db: Session, template: JobTemplate):
    db.add(template)
    db.commit()
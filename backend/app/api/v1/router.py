from fastapi import APIRouter

from app.api.v1.application import application_router
from app.api.v1.audit_log import audit_log_router
from app.api.v1.auth import auth_router
from app.api.v1.department import department_router
from app.api.v1.designation import designation_router
from app.api.v1.employee import employee_router
from app.api.v1.job_posting import job_posting_router
from app.api.v1.job_template import job_template_router
from app.api.v1.notification import notification_router
from app.api.v1.skill import skill_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(department_router)
api_router.include_router(designation_router)
api_router.include_router(skill_router)
api_router.include_router(job_template_router)
api_router.include_router(job_posting_router)
api_router.include_router(employee_router)
api_router.include_router(application_router)
api_router.include_router(notification_router)
api_router.include_router(audit_log_router)
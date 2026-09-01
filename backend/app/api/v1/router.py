from fastapi import APIRouter

from app.api.v1.auth import auth_router
from app.api.v1.department import department_router
from app.api.v1.designation import designation_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(department_router)
api_router.include_router(designation_router)
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.api.v1.router import api_router
import app.db.base

app = FastAPI(
    title="Job Hub API",
    version="1.0.0",
)

# Enable CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# standard HTTP exceptions
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exception: StarletteHTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "status_code": exception.status_code,
            "message": exception.detail,
            "data": None,
            "error": exception.detail  
        }
    )

# validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exception: RequestValidationError):
    errors = exception.errors()
    error_msg = f"{errors[0]['loc'][-1]}: {errors[0]['msg']}" if errors else "Validation Error"
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Payload validation failed.",
            "data": None,
            "error": error_msg
        }
    )
    
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status_code": 500,
            "message": "Internal Server Error",
            "data": None,
            "error": str(exc) 
        }
    )
    
app.include_router(api_router, prefix="/v1")
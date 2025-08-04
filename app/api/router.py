from fastapi import APIRouter
from app.api.endpoints.tasks import router as tasks_router
# from app.api.endpoints.auth import router as auth_router
# from app.api.endpoints.users import router as users_router

api_router = APIRouter()


# api_router.include_router(auth_router, prefix="/auth", tags=["auth"])


# api_router.include_router(users_router, prefix="/users", tags=["users"])

api_router.include_router(
    tasks_router,
    prefix="/tasks",
    tags=["tasks"],
)


@api_router.get("/", summary="API root")
def api_root():
    return {
        "message": "Welcome to ToDo API",
        "version": "1.0.0",
        "endpoints": {
            "tasks": "/api/tasks",
            # "auth": "/api/auth",
            # "users": "/api/users",
        },
    }

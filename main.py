from fastapi import FastAPI
from app.core.users import fastapi_users, auth_backend
from app.schemas.users import UserRead, UserCreate
from app.api.epic import router as epic_router
from app.api.task import router as task_router
app = FastAPI()


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(epic_router, prefix="/epics", tags=["epics"])

app.include_router(task_router, prefix="/tasks", tags=["tasks"])

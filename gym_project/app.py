from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from gym_project.api.auth import routes as auth_routes
from gym_project.api.employee import routes as employee_routes
from gym_project.api.financial import routes as financial
from gym_project.api.users import routes as users_routes
from gym_project.infra.Entities.entities import create_database

app = FastAPI()

BASE_PATH = "/api/gym"


@app.on_event("startup")
async def startup_event() -> None:
    await create_database()


@app.get("/")
async def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")


app.include_router(users_routes.router, prefix=f"{BASE_PATH}/users", tags=["users"])
app.include_router(
    employee_routes.router, prefix=f"{BASE_PATH}/employees", tags=["employees"]
)
app.include_router(auth_routes.router, prefix=f"{BASE_PATH}/auth", tags=["auth"])
app.include_router(
    financial.router, prefix=f"{BASE_PATH}/financial", tags=["financial"]
)

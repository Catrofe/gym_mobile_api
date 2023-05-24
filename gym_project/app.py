from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from gym_project.api.employee import routes as employee_routes
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

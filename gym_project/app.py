from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from gym_project.api.users import routes as users_routes

app = FastAPI()

BASE_PATH = "/api/gym"

@app.on_event("startup")
async def startup_event() -> None:
    from gym_project.infra.Entities.entities import DATABASE
    await DATABASE.setup_db()

@app.get("/")
async def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")

app.include_router(users_routes.router, prefix=f"{BASE_PATH}/users", tags=["users"])
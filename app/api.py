import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware


from app.routes.post import posts_router
from app.routes.user import users_router
from app.routes.auth import auth_router


load_dotenv(".env")

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

app.include_router(posts_router)
app.include_router(users_router)
app.include_router(auth_router)


@app.get("/", tags=["Health check"])
def health_check() -> dict:
    return {"message": "Pong!"}

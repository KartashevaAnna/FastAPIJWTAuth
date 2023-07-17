import os

import fastapi

from dotenv import load_dotenv
from fastapi_sqlalchemy import DBSessionMiddleware

import config
from app.routes.auth import auth_router
from app.routes.healthcheck import ping_router
from app.routes.like import likes_router
from app.routes.post import posts_router
from app.routes.user import users_router

load_dotenv(".env")

app = fastapi.FastAPI(
    title="Simple blog",
    description="Basic blog with JWT-based authentication. Posts and likes",
    version="1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    debug=config.DEBUG)

app.add_middleware(DBSessionMiddleware, db_url=config.DATABASE_URL)

app.include_router(posts_router)
app.include_router(auth_router)
app.include_router(ping_router)
app.include_router(likes_router)
app.include_router(users_router)

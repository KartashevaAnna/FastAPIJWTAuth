import os

import fastapi
import loguru
import uvicorn
from dotenv import load_dotenv
from fastapi_sqlalchemy import DBSessionMiddleware

import config
from app.routes.auth import auth_router
from app.routes.healthcheck import ping_router
from app.routes.like import likes_router
from app.routes.post import posts_router
from app.routes.user import users_router
from utils.logger import setup_logging

load_dotenv(".env")


def build_app(logger) -> fastapi.FastAPI:
    app = fastapi.FastAPI(
        title="Simple blog",
        description="Basic blog with JWT-based authentication. Posts and likes",
        version="1.0",
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
        debug=config.DEBUG,
        logger=logger,
    )

    if not config.DEBUG:
        app.docs_url = app.redoc_url = app.openapi_url = None

    app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

    app.include_router(posts_router)
    app.include_router(auth_router)
    app.include_router(ping_router)
    app.include_router(likes_router)

    if config.DEBUG:
        app.include_router(users_router)

    return app


def main():
    logger = setup_logging(loguru.logger)
    uvicorn.run(build_app(logger), host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()

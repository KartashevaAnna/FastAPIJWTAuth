from fastapi import APIRouter

ping_router = APIRouter(tags=["Healthcheck"])


@ping_router.get("/ping")
def health_check() -> str:
    """Checks that the app is running. Returns Pong for Ping."""
    return "Pong!"

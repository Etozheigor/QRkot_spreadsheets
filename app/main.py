from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.logging.logging import configure_logging

app = FastAPI(title=settings.app_title)
app.include_router(main_router)
configure_logging()
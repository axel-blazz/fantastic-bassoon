from fastapi import FastAPI
from api.auth import router as auth_router
from core.config import settings as Config
from core.logging import setup_logging

logger = setup_logging()

app = FastAPI(title=Config.APP_NAME)

app.include_router(auth_router)

@app.get("/")
def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}
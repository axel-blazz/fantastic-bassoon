from fastapi import FastAPI
from api.auth import router as auth_router
from api import incidents
from core.config import settings as Config
from core.logging import setup_logging
from db.base import Base
from db.session import engine
import warnings

warnings.filterwarnings("ignore", module="passlib")

logger = setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=Config.APP_NAME)

app.include_router(auth_router)
app.include_router(incidents.router)

@app.get("/")
def health():
    logger.info("Health check endpoint called")
    return {"status": "ok"}

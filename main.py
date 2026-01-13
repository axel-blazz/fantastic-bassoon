from fastapi import FastAPI
from api.auth import router as auth_router
from core.config import settings as Config

app = FastAPI(title=Config.APP_NAME)

app.include_router(auth_router)

@app.get("/")
def health():
    return {"status": "ok"}
# app/main.py
from fastapi import FastAPI
from app.api.v1 import users, auth
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/health")
def health():
    return {"status": "ok"}

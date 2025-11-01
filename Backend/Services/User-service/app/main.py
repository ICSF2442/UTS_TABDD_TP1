# app/main.py
from fastapi import FastAPI
from app.api.v1 import users, auth, drivers, notifications, itineraries
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(drivers.router)
app.include_router(notifications.router)
app.include_router(itineraries.router)


@app.get("/health")
def health():
    return {"status": "ok"}

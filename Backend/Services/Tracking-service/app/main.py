from fastapi import FastAPI
from app.application.api.v1 import tracking

app = FastAPI(title="Tracking Service")

app.include_router(tracking.router)

@app.get("/")
def root():
    return {"status": "Tracking Service is running"}

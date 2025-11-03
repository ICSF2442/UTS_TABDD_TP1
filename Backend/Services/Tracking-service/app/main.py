from fastapi import FastAPI
from application.api.v1.tracking import router as tracking_router

app = FastAPI(title="Tracking Service API")

app.include_router(tracking_router)

@app.get("/")
def root():
    return {"message": "Tracking Service is running"}

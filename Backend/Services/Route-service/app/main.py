from fastapi import FastAPI
from application.api.v1.route import router as routes_router

app = FastAPI(title="Urban Transportation Route Service")

app.include_router(routes_router)

@app.get("/")
def root():
    return {"message": "Route Service API is running"}

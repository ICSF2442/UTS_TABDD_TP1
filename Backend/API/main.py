from fastapi import FastAPI
from routers import tracking_mock

app = FastAPI(title="API Gateway")

app.include_router(tracking_mock.router)

@app.get("/")
def root():
    return {"status": "API running"}

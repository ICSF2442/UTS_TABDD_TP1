from fastapi import FastAPI
from app.api.v1.routes import router as routes_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Microserviço de otimização de rotas urbanas"
)

app.include_router(routes_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Optimization Service - Urban Transportation System",
        "version": settings.VERSION
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "optimization"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
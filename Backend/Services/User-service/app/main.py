from fastapi import FastAPI
from app.core.config import settings
from app.api import auth, users

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Microserviço de gestão de utilizadores",
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True
    }
)

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {
        "message": "User Service - Urban Transportation System",
        "version": settings.VERSION
    }

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.VERSION,
        description="Microserviço de gestão de utilizadores com autenticação JWT",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    public_paths = ["/", "/auth/login", "/auth/register"]
    
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete", "patch"]:
                if path not in public_paths and not path.startswith("/docs") and not path.startswith("/redoc"):
                    openapi_schema["paths"][path][method]["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
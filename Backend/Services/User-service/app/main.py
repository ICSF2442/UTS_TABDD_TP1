from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME, 
    version=settings.VERSION,
    swagger_ui_parameters={
        "persistAuthorization": True,
        "displayRequestDuration": True
    }
)

try:
    from app.api.v1 import auth
    app.include_router(auth.router)
    print("Auth router carregado")
except ImportError as e:
    print(f"Auth router não carregado: {e}")

try:
    from app.api.v1 import users
    app.include_router(users.router)
    print("Users router carregado")
except ImportError as e:
    print(f"Users router não carregado: {e}")

@app.get("/")
def read_root():
    return {"message": "User Service API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Configuracao da autenticacao no Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.VERSION,
        description="API com autenticacao JWT",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    public_paths = ["/", "/health", "/auth/login"]
    
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete", "patch"]:
                if path not in public_paths:
                    openapi_schema["paths"][path][method]["security"] = [{"Bearer": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
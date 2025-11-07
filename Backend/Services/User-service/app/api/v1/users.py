from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.infrastructure.db.connection import get_db
from app.core.services.user_service import UserService
from app.api.v1.auth import get_current_user, require_role

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", summary="Criar usuário")
def create_user(
    name: str,
    email: str, 
    password: str,
    role: str = "user",
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))  # Apenas admin
):
    user_service = UserService(db)
    
    try:
        created_user = user_service.create_user(name, email, password, role)
        
        return {
            "message": "User criado com sucesso",
            "user_id": created_user.user_id,
            "name": created_user.name,
            "email": created_user.email,
            "role": created_user.role
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar user: {str(e)}")

@router.get("/", summary="Listar usuários")
def get_all_users(
    skip: int = Query(0, description="Número de registos a saltar"),
    limit: int = Query(100, description="Número máximo de registos a retornar"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_service = UserService(db)
    
    try:
        users = user_service.get_all_users(skip, limit)
        
        return {
            "users": [
                {
                    "user_id": user.user_id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "created_at": user.created_at
                }
                for user in users
            ],
            "total": len(users)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar users: {str(e)}")

@router.get("/{user_id}", summary="Obter usuário")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_service = UserService(db)
    
    try:
        user = user_service.get_user_by_id(user_id)
        
        return {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter user: {str(e)}")

@router.put("/{user_id}", summary="Atualizar usuário")
def update_user(
    user_id: int,
    name: str = None,
    email: str = None,
    password: str = None,
    role: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))  # Apenas admin
):
    user_service = UserService(db)
    
    try:
        updated_user = user_service.update_user(user_id, name, email, password, role)
        
        return {
            "message": "User atualizado com sucesso",
            "user_id": updated_user.user_id,
            "name": updated_user.name,
            "email": updated_user.email,
            "role": updated_user.role
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar user: {str(e)}")

@router.delete("/{user_id}", summary="Eliminar usuário")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))  # Apenas admin
):
    user_service = UserService(db)
    
    try:
        user_service.delete_user(user_id)
        
        return {
            "message": "User eliminado com sucesso"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao eliminar user: {str(e)}")
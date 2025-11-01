from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.db.connection import SessionLocal
from app.infrastructure.db.driver_repository import DriverRepository
from app.domain.schemas.driver_schema import DriverCreate, DriverOut
from app.domain.models.user import User
from app.api.v1.users import get_current_user, require_role

router = APIRouter(prefix="/drivers", tags=["Drivers"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=DriverOut)
def add_driver(payload: DriverCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    repo = DriverRepository(db)

    if repo.find_by_license(payload.license_number):
        raise HTTPException(status_code=400, detail="Driver with this license already exists")

    driver = repo.add_driver(payload.user_id, payload.name, payload.license_number, payload.contact)
    return DriverOut(**driver.__dict__)


@router.get("/", response_model=list[DriverOut])
def get_all_drivers(db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    repo = DriverRepository(db)
    drivers = repo.get_all_drivers()
    return [DriverOut(**d.__dict__) for d in drivers]


@router.patch("/{driver_id}/deactivate", response_model=DriverOut)
def deactivate_driver(driver_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    repo = DriverRepository(db)
    driver = repo.deactivate_driver(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return DriverOut(**driver.__dict__)

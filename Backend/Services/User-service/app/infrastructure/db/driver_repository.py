from sqlalchemy.orm import Session
from app.infrastructure.db.base import DriverDB

class DriverRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_driver(self, user_id: int, name: str, license_number: str, contact: str | None):
        driver = DriverDB(user_id=user_id, name=name, license_number=license_number, contact=contact)
        self.db.add(driver)
        self.db.commit()
        self.db.refresh(driver)
        return driver

    def get_all_drivers(self):
        return self.db.query(DriverDB).all()

    def find_by_id(self, driver_id: int):
        return self.db.query(DriverDB).filter(DriverDB.driver_id == driver_id).first()

    def find_by_license(self, license_number: str):
        return self.db.query(DriverDB).filter(DriverDB.license_number == license_number).first()

    def deactivate_driver(self, driver_id: int):
        driver = self.find_by_id(driver_id)
        if driver:
            driver.active = False
            self.db.commit()
        return driver

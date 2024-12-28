from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/drivers", tags=["drivers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Driver)
def create_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    existing_driver = crud.get_driver(db, driver.id)
    if existing_driver:
        raise HTTPException(status_code=400, detail=f"Driver with number {driver.number} already exists.")
    
    return crud.create_driver(db, driver)


@router.get("/{driver_id}", response_model=schemas.Driver)
def read_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = crud.get_driver(db, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.get("/", response_model=list[schemas.Driver])
def read_drivers(db: Session = Depends(get_db)):
    drivers = crud.get_drivers(db)
    return drivers


@router.put("/{driver_id}", response_model=schemas.Driver)
def update_driver(driver_id: int, driver_update: schemas.DriverUpdate, db: Session = Depends(get_db)):
    driver = crud.update_driver(db, driver_id, driver_update)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.delete("/{driver_id}", response_model=schemas.Driver)
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = crud.delete_driver(db, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver

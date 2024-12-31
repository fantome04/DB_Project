from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal
from sqlalchemy.sql import func

router = APIRouter(prefix="")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/drivers/filter", tags=["drivers"])
def filter_drivers(nationality: str = None, team: str = None, db: Session = Depends(get_db)):
    drivers = crud.filter_drivers(db, nationality=nationality, team=team)
    if not drivers:
        raise HTTPException(status_code=404, detail="No drivers found with the given criteria.")
    return drivers

@router.get("/races/details", response_model=list[schemas.RaceDetails], tags=["races"])
def get_race_details(db: Session = Depends(get_db)):
    results = crud.get_race_details(db)
    if not results:
        raise HTTPException(status_code=404, detail="No results found with the given criteria.")
    return results

@router.put("/races/update-points", tags=["races"])
def update_race_points(place: int, db: Session = Depends(get_db)):
    result = crud.update_race_points(db, place=place)
    if result["updated_rows"] == 0:
        raise HTTPException(status_code=404, detail="No races found for the given place.")
    return result

@router.get("/drivers/total-points", response_model=list[schemas.DriverPoints], tags=["drivers"])
def get_driver_points(db: Session = Depends(get_db)):
    results = crud.get_driver_points(db)
    if not results:
        raise HTTPException(status_code=404, detail="No results found with the given criteria.")
    return [{"driver_id": driver_id, "total_points": total_points} for driver_id, total_points in results]

@router.get("/circuits/sorted", response_model=list[schemas.Circuit], tags=["circuits"])
def get_sorted_circuits(db: Session = Depends(get_db)):
    results = crud.get_sorted_circuits(db)
    if not results:
        raise HTTPException(status_code=404, detail="No results found with the given criteria.")
    return results
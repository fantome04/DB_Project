from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/races", tags=["races"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Race)
def create_race(race: schemas.RaceCreate, db: Session = Depends(get_db)):
    driver = crud.get_driver(db, race.driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail=f"Driver with id {race.driver_id} not found")
    
    circuit = crud.get_circuit(db, race.circuit_id)
    if not circuit:
        raise HTTPException(status_code=404, detail=f"Circuit with id {race.circuit_id} not found")

    return crud.create_race(db, race)


@router.get("/{driver_id}/{circuit_id}/{race_date}", response_model=schemas.Race)
def read_race(driver_id: int, circuit_id: int, race_date: str, db: Session = Depends(get_db)):
    try:
        race_date_parsed = datetime.strptime(race_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    db_race = crud.get_race(db, driver_id, circuit_id, race_date_parsed)
    if not db_race:
        raise HTTPException(status_code=404, detail="Race not found")
    return db_race


@router.get("/", response_model=list[schemas.Race])
def read_races(db: Session = Depends(get_db)):
    races = crud.get_races(db)
    return races


@router.put("/{driver_id}/{circuit_id}/{race_date}", response_model=schemas.Race)
def update_race(driver_id: int, circuit_id: int, race_date: str, race_update: schemas.RaceUpdate, db: Session = Depends(get_db)):
    try:
        race_date_parsed = datetime.strptime(race_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    db_race = crud.update_race(db, driver_id, circuit_id, race_date_parsed, race_update)
    if not db_race:
        raise HTTPException(status_code=404, detail="Race not found")
    return db_race


@router.delete("/{driver_id}/{circuit_id}/{race_date}", response_model=schemas.Race)
def delete_race(driver_id: int, circuit_id: int, race_date: str, db: Session = Depends(get_db)):
    try:
        race_date_parsed = datetime.strptime(race_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    db_race = crud.delete_race(db, driver_id, circuit_id, race_date_parsed)
    if not db_race:
        raise HTTPException(status_code=404, detail="Race not found")
    return db_race

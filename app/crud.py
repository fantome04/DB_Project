from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy.sql import func
import sqlalchemy as sa

def create_driver(db: Session, driver: schemas.DriverCreate):
    db_driver = models.Driver(**driver.model_dump())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver


def get_driver(db: Session, driver_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Driver).filter(models.Driver.id == driver_id).offset(skip).limit(limit).first()


def search_drivers_by_details(db: Session, pattern: str, skip: int = 0, limit: int = 10):
    query = f"%{pattern}%"
    return db.query(models.Driver).filter(models.Driver.details.cast(sa.Text).ilike(query)).offset(skip).limit(limit).all()


def filter_drivers(db: Session, nationality: str = None, team: str = None, skip: int = 0, limit: int = 10):
    query = db.query(models.Driver)
    if nationality:
        query = query.filter(models.Driver.nationality == nationality)
    if team:
        query = query.filter(models.Driver.team == team)
    return query.offset(skip).limit(limit).all()

def get_driver_points(db: Session, skip: int = 0, limit: int = 10):
    return db.query(
        models.Race.driver_id,
        func.sum(models.Race.points).label("total_points")
    ).group_by(models.Race.driver_id).offset(skip).limit(limit).all()

def get_drivers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Driver).offset(skip).limit(limit).all()

def update_driver(db: Session, driver_id: int, driver_update: schemas.DriverUpdate):
    db_driver = get_driver(db, driver_id)
    if db_driver:
        for key, value in driver_update.dict(exclude_unset=True).items():
            setattr(db_driver, key, value)
        db.commit()
        db.refresh(db_driver)
    return db_driver

def delete_driver(db: Session, driver_id: int):
    db_driver = get_driver(db, driver_id)
    if db_driver:
        db.delete(db_driver)
        db.commit()
        return db_driver

def create_circuit(db: Session, circuit: schemas.CircuitCreate):
    db_circuit = models.Circuit(**circuit.model_dump())
    db.add(db_circuit)
    db.commit()
    db.refresh(db_circuit)
    return db_circuit

def get_circuit(db: Session, circuit_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Circuit).filter(models.Circuit.id == circuit_id).offset(skip).limit(limit).first()

def get_circuits(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Circuit).offset(skip).limit(limit).all()

def get_sorted_circuits(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Circuit).order_by(models.Circuit.lap_record).offset(skip).limit(limit).all()

def update_circuit(db: Session, circuit_id: int, circuit_update: schemas.CircuitUpdate):
    db_circuit = get_circuit(db, circuit_id)
    if db_circuit:
        for key, value in circuit_update.dict(exclude_unset=True).items():
            setattr(db_circuit, key, value)
        db.commit()
        db.refresh(db_circuit)
    return db_circuit

def delete_circuit(db: Session, circuit_id: int):
    db_circuit = get_circuit(db, circuit_id)
    if db_circuit:
        db.delete(db_circuit)
        db.commit()
        return db_circuit

def create_race(db: Session, race: schemas.RaceCreate):
    db_race = models.Race(**race.dict())
    db.add(db_race)
    db.commit()
    db.refresh(db_race)
    return db_race

def get_race(db: Session, driver_id: int, circuit_id: int, race_date: str, skip: int = 0, limit: int = 10):
    return db.query(models.Race).filter(
        models.Race.driver_id == driver_id,
        models.Race.circuit_id == circuit_id,
        models.Race.race_date == race_date
    ).offset(skip).limit(limit).first()

def get_races(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Race).offset(skip).limit(limit).all()

def get_race_details(db: Session, skip: int = 0, limit: int = 10):
    results = db.query(
        models.Race,
        models.Driver.name.label("driver_name"),
        models.Circuit.name.label("circuit_name")
    ).join(models.Driver, models.Race.driver_id == models.Driver.id)\
     .join(models.Circuit, models.Race.circuit_id == models.Circuit.id).offset(skip).limit(limit).all()

    return [
        {
            "driver_id": race.driver_id,
            "circuit_id": race.circuit_id,
            "race_date": race.race_date,
            "driver_name": driver_name,
            "circuit_name": circuit_name,
            "place": race.place,
            "points": race.points
        }
        for race, driver_name, circuit_name in results
    ]


def update_race(db: Session, driver_id: int, circuit_id: int, race_date: str, race_update: schemas.RaceUpdate):
    race = get_race(db, driver_id, circuit_id, race_date)

    if not race:
        return None

    for key, value in race_update.model_dump(exclude_unset=True).items():
        setattr(race, key, value)

    db.commit()
    db.refresh(race)

    return race


def update_race_points(db: Session, place: int):
    updated_rows = db.query(models.Race).filter(models.Race.place == place).update(
        {models.Race.points: models.Race.points + 1}, synchronize_session=False
    )
    db.commit()
    return {"updated_rows": updated_rows}


def delete_race(db: Session, driver_id: int, circuit_id: int, race_date: str):
    race = get_race(db, driver_id, circuit_id, race_date)

    if not race:
        return None

    db.delete(race)
    db.commit()
    
    return race
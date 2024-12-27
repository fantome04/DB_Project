from sqlalchemy.orm import Session
from . import models, schemas


def create_driver(db: Session, driver: schemas.DriverCreate):
    db_driver = models.Driver(**driver.model_dump())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver


def get_driver(db: Session, driver_id: int):
    return db.query(models.Driver).filter(models.Driver.id == driver_id).first()


def get_drivers(db: Session):
    return db.query(models.Driver).all()


def update_driver(db: Session, driver_id: int, driver_update: schemas.DriverUpdate):
    db_driver = get_driver(db, driver_id)
    if db_driver:
        for key, value in driver_update.model_dump(exclude_unset=True).items():
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


def get_circuit(db: Session, circuit_id: int):
    return db.query(models.Circuit).filter(models.Circuit.id == circuit_id).first()


def get_circuits(db: Session):
    return db.query(models.Circuit).all()


def update_circuit(db: Session, circuit_id: int, circuit_update: schemas.CircuitUpdate):
    db_circuit = get_circuit(db, circuit_id)
    if db_circuit:
        for key, value in circuit_update.model_dump(exclude_unset=True).items():
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
    db_race = models.Race(**race.model_dump())
    db.add(db_race)
    db.commit()
    db.refresh(db_race)
    return db_race


def get_race(db: Session, driver_id: int, circuit_id: int, race_date: str):
    return db.query(models.Race).filter(
        models.Race.driver_id == driver_id,
        models.Race.circuit_id == circuit_id,
        models.Race.race_date == race_date
    ).first()


def get_races(db: Session):
    return db.query(models.Race).all()


def update_race(db: Session, driver_id: int, circuit_id: int, race_date: str, race_update: schemas.RaceUpdate):
    db_race = get_race(db, driver_id, circuit_id, race_date)
    if db_race:
        for key, value in race_update.model_dump(exclude_unset=True).items():
            setattr(db_race, key, value)
        db.commit()
        db.refresh(db_race)
    return db_race


def delete_race(db: Session, driver_id: int, circuit_id: int, race_date: str):
    db_race = get_race(db, driver_id, circuit_id, race_date)
    if db_race:
        db.delete(db_race)
        db.commit()
        return db_race

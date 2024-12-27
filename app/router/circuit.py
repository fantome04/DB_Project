from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/circuits", tags=["circuits"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Circuit)
def create_circuit(circuit: schemas.CircuitCreate, db: Session = Depends(get_db)):
    existing_circuit = crud.get_circuit_by_name(db, circuit.name)
    if existing_circuit:
        raise HTTPException(status_code=400, detail=f"Circuit with name '{circuit.name}' already exists.")
    
    return crud.create_circuit(db, circuit)


@router.get("/{circuit_id}", response_model=schemas.Circuit)
def read_circuit(circuit_id: int, db: Session = Depends(get_db)):
    db_circuit = crud.get_circuit(db, circuit_id)
    if not db_circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return db_circuit


@router.get("/", response_model=list[schemas.Circuit])
def read_circuits(db: Session = Depends(get_db)):
    circuits = crud.get_circuits(db)
    return circuits


@router.put("/{circuit_id}", response_model=schemas.Circuit)
def update_circuit(circuit_id: int, circuit_update: schemas.CircuitUpdate, db: Session = Depends(get_db)):
    db_circuit = crud.update_circuit(db, circuit_id, circuit_update)
    if not db_circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return db_circuit


@router.delete("/{circuit_id}", response_model=schemas.Circuit)
def delete_circuit(circuit_id: int, db: Session = Depends(get_db)):
    db_circuit = crud.delete_circuit(db, circuit_id)
    if not db_circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return db_circuit

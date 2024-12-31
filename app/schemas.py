from pydantic import BaseModel
from typing import Optional
from datetime import date

class DriverBase(BaseModel):
    id: int
    number: int
    name: str
    nationality: str
    team: str
    dob: date
    details: Optional[dict]

class DriverCreate(DriverBase):
    pass

class DriverUpdate(BaseModel):
    number: Optional[int] = None
    name: Optional[str] = None
    nationality: Optional[str] = None
    team: Optional[str] = None
    dob: Optional[date] = None

class DriverPoints(BaseModel):
    driver_id: int
    total_points: int

class Driver(DriverBase):
    class Config:
        from_attributes = True

class CircuitBase(BaseModel):
    id: int
    name: str
    location: str
    length: float
    laps: int
    lap_record: str

class CircuitCreate(CircuitBase):
    pass

class CircuitUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    length: Optional[float] = None
    laps: Optional[int] = None
    lap_record: Optional[str] = None

class Circuit(CircuitBase):
    class Config:
        from_attributes = True

class RaceBase(BaseModel):
    driver_id: int
    circuit_id: int
    race_date: date
    place: int
    points: int
    is_fastest_lap: bool
    start_place: int

class RaceCreate(RaceBase):
    pass

class RaceUpdate(BaseModel):
    place: Optional[int] = None
    points: Optional[int] = None
    is_fastest_lap: Optional[bool] = None

class RaceDetails(BaseModel):
    driver_id: int
    circuit_id: int
    race_date: date
    driver_name: str
    circuit_name: str
    place: int
    points: int


class Race(RaceBase):
    class Config:
        from_attributes = True

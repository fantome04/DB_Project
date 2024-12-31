from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DECIMAL
from .database import Base

class Driver(Base):
    __tablename__ = "driver"

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    name = Column(String(100))
    nationality = Column(String(50))
    team = Column(String(50))
    dob = Column(Date)


class Circuit(Base):
    __tablename__ = "circuit"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    location = Column(String(100))
    length = Column(DECIMAL(10, 2))
    laps = Column(Integer)
    lap_record = Column(String(50))

class Race(Base):
    __tablename__ = "race"

    driver_id = Column(Integer, ForeignKey("driver.id"), primary_key=True)
    circuit_id = Column(Integer, ForeignKey("circuit.id"), primary_key=True)
    race_date = Column(Date, primary_key=True)
    place = Column(Integer)
    points = Column(Integer)
    is_fastest_lap = Column(Boolean)
    start_place = Column(Integer)

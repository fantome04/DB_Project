from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import driver, circuit, race, analitics
import os

app = FastAPI(title="F1 REST API")

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

app.include_router(analitics.router)
app.include_router(driver.router)
app.include_router(circuit.router)
app.include_router(race.router)

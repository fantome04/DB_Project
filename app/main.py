from fastapi import FastAPI
from .routers import driver, circuit, race, analitics

app = FastAPI(title="F1 REST API")

app.include_router(analitics.router)
app.include_router(driver.router)
app.include_router(circuit.router)
app.include_router(race.router)

from fastapi import FastAPI
from .routers import driver, circuit, race

app = FastAPI(
    title="F1 REST API",
    description="API для управления данными о гонщиках, трассах и гонках Формулы-1",
    version="1.0.0"
)

app.include_router(driver.router)
app.include_router(circuit.router)
app.include_router(race.router)

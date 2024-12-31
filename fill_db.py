import requests
from faker import Faker
import random

BASE_URL = "http://127.0.0.1:8000"

fake = Faker()

def create_fake_drivers(n):
    for i in range(n):
        driver_data = {
            "id": i,
            "number": random.randint(1, 99999), 
            "name": fake.name(),               
            "nationality": fake.country(),   
            "team": random.choice(["Mercedes", "Red Bull", "Ferrari", "McLaren", "Alpine", "Aston Martin"]),
            "dob": fake.date_of_birth(minimum_age=18, maximum_age=45).isoformat(),
            "details": {
                "experience": random.choice(["rookie", "intermediate", "veteran"]),
                "wins": random.randint(0, 50),
                "podiums": random.randint(0, 100),
                "bio": fake.text(max_nb_chars=200)
            }
        }

        try:
            resp = requests.post(f"{BASE_URL}/drivers/", json=driver_data)
            if resp.status_code in (200, 201):
                print(f"[OK] Created driver: {driver_data['name']}")
            else:
                print(f"[ERROR] Failed to create driver: {resp.text}, {resp.status_code}")
        except Exception as e:
            print(f"[EXCEPTION] {e}")


def create_fake_circuits(n):
    for i in range(n):
        circuit_data = {
            "id": i,
            "name": fake.city() + " Circuit",  
            "location": fake.city(),         
            "length": round(random.uniform(3.0, 7.0), 3),
            "laps": random.randint(40, 80),
            "lap_record": f"1:{random.randint(15,59)}.{random.randint(100,999)}"
        }

        try:
            resp = requests.post(f"{BASE_URL}/circuits/", json=circuit_data)
            if resp.status_code in (200, 201):
                print(f"[OK] Created circuit: {circuit_data['name']}")
            else:
                print(f"[ERROR] Failed to create circuit: {resp.text}")
        except Exception as e:
            print(f"[EXCEPTION] {e}")


def create_fake_races(n):
    drivers_resp = requests.get(f"{BASE_URL}/drivers/")
    circuits_resp = requests.get(f"{BASE_URL}/circuits/")
    
    if drivers_resp.status_code != 200 or circuits_resp.status_code != 200:
        print("[ERROR] Could not fetch drivers or circuits for generating races.")
        return

    drivers = drivers_resp.json()
    circuits = circuits_resp.json()

    for _ in range(n):
        driver = random.choice(drivers)
        circuit = random.choice(circuits)

        race_data = {
            "driver_id": driver["id"],
            "circuit_id": circuit["id"],
            "race_date": fake.date_between(start_date="-1y", end_date="today").isoformat(),
            "place": random.randint(1, 20),
            "points": random.randint(0, 25),
            "is_fastest_lap": random.choice([True, False]),
            "start_place": random.randint(1, 20)
        }

        try:
            resp = requests.post(f"{BASE_URL}/races/", json=race_data)
            if resp.status_code in (200, 201):
                print(f"[OK] Created race for driver {driver['name']} at circuit {circuit['name']}")
            else:
                print(f"[ERROR] Failed to create race: {resp.text}")
        except Exception as e:
            print(f"[EXCEPTION] {e}")


if __name__ == "__main__":
    print("Creating fake drivers...")
    create_fake_drivers(n=1000)

    print("Creating fake circuits...")
    create_fake_circuits(n=1000)

    print("Creating fake races...")
    create_fake_races(n=1000)

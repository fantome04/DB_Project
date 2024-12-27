import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DB_NAME = "f1_db"
DB_USER = "username"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "8080"

def create_database():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE {DB_NAME} OWNER {DB_USER};")
        print(f"Database '{DB_NAME}' with owner {DB_USER} created successfully.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

def create_tables():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE Driver (
            id INT PRIMARY KEY,
            number INT,
            name VARCHAR(100),
            nationality VARCHAR(50),
            team VARCHAR(50),
            dob DATE
        );
        """)

        cursor.execute("""
        CREATE TABLE Circuit (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            location VARCHAR(100),
            length DECIMAL(10, 2),
            laps INT,
            lap_record VARCHAR(50)
        );
        """)

        cursor.execute("""
        CREATE TABLE Race (
            driver_id INT,
            circuit_id INT,
            race_date DATE,
            place INT,
            points INT,
            is_fastest_lap BOOLEAN,
            start_place INT,
            PRIMARY KEY (driver_id, circuit_id, race_date),
            FOREIGN KEY (driver_id) REFERENCES Driver(id),
            FOREIGN KEY (circuit_id) REFERENCES Circuit(id)
        );
        """)

        print("Tables created successfully.")

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_database()
    create_tables()
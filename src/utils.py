import psycopg2

from config import COUNTRIES, db_config
from src.api import NominatimAPI, OpenSkyAPI


def create_database(dbname):
    conn = psycopg2.connect(dbname="postgres", **db_config)
    cur = conn.cursor()
    conn.autocommit = True

    cur.execute(f"DROP DATABASE IF EXISTS {dbname}")
    cur.execute(f"CREATE DATABASE {dbname}")

    cur.close()
    conn.close()


def create_tables(dbname):
    conn = psycopg2.connect(dbname=dbname, **db_config)
    with conn as conn:
        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE countries (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE)"""
            )

            cur.execute(
                """CREATE TABLE airplanes (
                        id VARCHAR(20) PRIMARY KEY,
                        callsign VARCHAR(20),
                        baro_altitude FLOAT,
                        on_ground BOOLEAN,
                        velocity FLOAT,
                        country_id INTEGER REFERENCES countries(id))"""
            )

    conn.close()


def insert_data(dbname):
    conn = psycopg2.connect(dbname=dbname, **db_config)
    with conn as conn:
        with conn.cursor() as cur:
            for country in COUNTRIES:
                cur.execute("""INSERT INTO countries (name) VALUES (%s) RETURNING id""", (country,))
                country_id = cur.fetchone()[0]

                nm = NominatimAPI(country)
                coords = nm.get_data()
                open_sky = OpenSkyAPI(coords)
                airplanes = open_sky.get_data()

                for airplane in airplanes:
                    cur.execute(
                        """
                    INSERT INTO airplanes (id, callsign, baro_altitude, on_ground, velocity, country_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        callsign = EXCLUDED.callsign,
                        baro_altitude = EXCLUDED.baro_altitude,
                        on_ground = EXCLUDED.on_ground,
                        velocity = EXCLUDED.velocity,
                        country_id = EXCLUDED.country_id;
                    """,
                        (
                            airplane["id"],
                            airplane["callsign"],
                            airplane["baro_altitude"],
                            airplane["on_ground"],
                            airplane["velocity"],
                            country_id,
                        ),
                    )

    conn.close()

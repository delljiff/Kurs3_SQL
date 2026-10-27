import psycopg2

from config import db_config


def create_database(dbname):
    conn = psycopg2.connect(dbname='postgres', **db_config)
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
            cur.execute("""CREATE TABLE countries (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE)""")

            cur.execute("""CREATE TABLE airplanes (
                        id VARCHAR(20) PRIMARY KEY,
                        callsign VARCHAR(20),
                        baro_altitude FLOAT,
                        on_ground BOOLEAN,
                        velocity FLOAT)""")

    conn.close()


db_name = 'coursework_3'
create_database(db_name)
create_tables(db_name)
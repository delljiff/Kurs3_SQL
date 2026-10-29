import psycopg2

from config import db_config


class DBManager:
    def __init__(self, dbname):
        self.dbname = dbname

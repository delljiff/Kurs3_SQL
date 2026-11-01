import psycopg2

from config import db_config


class DBManager:
    def __init__(self, dbname):
        self.dbname = dbname

    def execute_query(self, query, params=None):
        conn = psycopg2.connect(dbname=self.dbname, **db_config)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    if cur.description:
                        return cur.fetchall()
                    return None
        finally:
            conn.close()


    def get_countries_and_aeroplanes_count(self):
        """
        Получает список всех стран и общее количество уникальных самолетов в базе.
        """
        query = """
        SELECT c.name, COUNT(DISTINCT a.id) AS airplane_count
        FROM countries c
        LEFT JOIN airplanes a ON c.id = a.country_id
        GROUP BY c.name
        ORDER BY c.name;
        """
        return self.execute_query(query)

    def get_all_aeroplanes(self):
        """
        Получает список всех воздушных судов
        """
        query = """
        SELECT id, callsign, baro_altitude, on_ground, velocity
        FROM airplanes
        ORDER BY id;
        """
        return self.execute_query(query)

    def get_avg_speed(self):
        """
        Получает среднюю скорость по самолетам
        """
        query = """
        SELECT AVG(velocity) AS avg_speed
        FROM airplanes
        WHERE velocity IS NOT NULL;
        """
        return self.execute_query(query)

    def get_aeroplanes_with_higher_speed(self):
        """
        Получает список всех самолетов, у которых скорость выше средней
        """
        query = """
        SELECT id, callsign, baro_altitude, on_ground, velocity
        FROM airplanes
        WHERE velocity > (SELECT AVG(velocity)
        FROM airplanes)
        ORDER BY velocity DESC;
        """
        return self.execute_query(query)

    def get_aeroplanes_with_keyword(self, keyword):
        """
        Получает список всех самолетов, в позывном которых содержатся переданные в метод символы
        """
        query = """
        SELECT id, callsign, baro_altitude, on_ground, velocity
        FROM airplanes
        WHERE callsign ILIKE %s
        ORDER BY callsign
        """
        search_pattern = f"%{keyword}%"
        return self.execute_query(query, (search_pattern,))

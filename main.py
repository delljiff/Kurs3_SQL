from src.db_manager import DBManager
from src.utils import create_database, create_tables, insert_data

db_name = "coursework_3"
create_database(db_name)
create_tables(db_name)
insert_data(db_name)

db_manager = DBManager(db_name)
print(db_manager.get_aeroplanes_with_keyword("MSR"))

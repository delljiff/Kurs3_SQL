from src.db_manager import DBManager
from src.utils import create_database, create_tables, insert_data

db_name = "coursework_3"
create_database(db_name)
create_tables(db_name)
insert_data(db_name)

db_manager = DBManager(db_name)

print("1. Вывести список всех стран и общее количество уникальных самолетов в базе")
print("2. Вывести список всех воздушных судов")
print("3. Вывести среднюю скорость по самолетам")
print("4. Вывести список всех самолетов, у которых скорость выше средней")
print("5. Вывести список всех самолетов, в позывном которых содержатся переданные символы")
print("6. Выход")
print("=" * 60)

while True:
    answer = input("\nВыберите необходимый пункт: ")

    if answer == "1":
        data = db_manager.get_countries_and_aeroplanes_count()
        for element in data:
            print(f"Страна: {element[0]:<20} | Самолетов: {element[1]}")

    elif answer == "2":
        data = db_manager.get_all_aeroplanes()
        for element in data:
            print(element)

    elif answer == "3":
        data = db_manager.get_avg_speed()
        print(f"Средняя скорость - {round(data[0][0], 2)} м/с")

    elif answer == "4":
        data = db_manager.get_aeroplanes_with_higher_speed()
        for element in data:
            print(element)

    elif answer == "5":
        keyboard_data = input("Введите 1-3 символа для поиска самолета по позывному: ")
        data = db_manager.get_aeroplanes_with_keyword(
            keyboard_data
        )
        if data:
            for element in data:
                print(element)
        else:
            print("Самолетов с таким позывным не найдено.")

    elif answer == "6":
        print("Выход из программы...")
        break

    else:
        print("Нет такой команды")

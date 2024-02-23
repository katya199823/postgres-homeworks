import csv

import psycopg2

from config import DATA_EMPLOYEES,DATA_CUSTOMERS, DATA_ORDERS


def open_data_file(data) -> list:
    """
    Открываем scv, перебираем и создаем список
    :data: путь до файла
    :return: сам список из словарей
    """
    new_list = []

    with open(data, encoding='utf-8') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            if row.get('employee_id'):
                row['employee_id'] = int(row['employee_id'])
            new_list.append(row)
    return new_list


def add_data_to_database(data_list: list, name_table: str) -> None:
    """
    Отправляем информацию в базу данных
    :data_list: список из словарей
    :name_table: название таблицы
    :column_count: кол-во столбцов
    """

    with psycopg2.connect(
            host='localhost',
            database='north',
            user='postgres',
            password= '12345'
    ) as conn:
        with conn.cursor() as cur:
            for data_info in data_list:
                count = '%s ' * len(data_info)
                val = tuple(data_info.values())
                cur.execute(f"INSERT INTO {name_table} VALUES ({', '.join(count.split())})", val)
                print(val)
    conn.close()


if __name__ == '__main__':
    data_employees = open_data_file(DATA_EMPLOYEES)
    add_data_to_database(data_employees, 'employees')

    data_customers = open_data_file(DATA_CUSTOMERS)
    add_data_to_database(data_customers, 'customers')

    data_orders = open_data_file(DATA_ORDERS)
    add_data_to_database(data_orders, 'orders')

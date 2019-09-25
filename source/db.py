import pymysql
import config
from source.file import *


def return_connection_string():
    return pymysql.connect(
        config.host,  # host
        "dan",  # username
        config.password,  # password
        "dan",  # database
    )


def get_sql(sql_string):
    connection = return_connection_string()
    rows = []
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_string)
            rows = cursor.fetchall()
    except:
        pass
    finally:
        connection.close()
        return rows


def write_sql(sql_string):
    connection = return_connection_string()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_string)
        connection.commit()
    except:
        pass
    finally:
        connection.close()


def get_all_people():
    query = "SELECT * FROM person"
    result = get_sql(query)
    return result


def save_person(name, age, favourite_drink_id):
    query = f"INSERT INTO person(name, age, favourite_drink_id) VALUES ('{name}', {age}, {favourite_drink_id})"
    write_sql(query)

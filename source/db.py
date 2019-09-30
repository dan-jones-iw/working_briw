import pymysql
import config
from source.file import *


# # # # # # # # # # # # # #
# Connecting to database  #
# # # # # # # # # # # # # #
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


# # # # # # # # # # #
# All actions on db #
# # # # # # # # # # #
def db_clean():
    query = "DELETE FROM orders"
    write_sql(query)

    query = "DELETE FROM round"
    write_sql(query)
    query = "ALTER TABLE round AUTO_INCREMENT = 1"
    write_sql(query)

    query = "DELETE FROM drink"
    write_sql(query)
    query = "ALTER TABLE drink AUTO_INCREMENT = 1"
    write_sql(query)

    query = "DELETE FROM person"
    write_sql(query)
    query = "ALTER TABLE person AUTO_INCREMENT = 1"
    write_sql(query)


# get from db
# from people
def get_all_people():
    query = "SELECT * FROM person"
    return get_sql(query)


def get_all_people_nice():
    query = "SELECT person_id, name FROM person"
    return get_sql(query)


def get_all_favourites():
    query = """ SELECT 
                    P.person_id, 
                    P.name,     
                    D.name
                FROM 
                    person AS P
                LEFT JOIN 
                    drink AS D ON P.favourite_drink_id = D.drink_id
            """
    return get_sql(query)


def get_id_of_person_from_name(name):
    query = f"SELECT person_id FROM person WHERE name = '{name}'"
    return get_sql(query)[0][0]


def get_name_of_person_from_id(person_id):
    query = f"SELECT name FROM person WHERE person_id = '{person_id}'"
    return get_sql(query)[0][0]


def get_number_of(table):
    query = f"SELECT max({table}_id) FROM {table}"
    return get_sql(query)[0][0]


def get_all_drink_nice():
    query = "SELECT drink_id, name FROM drink"
    return get_sql(query)


def get_round():
    query = "SELECT * FROM round"
    return get_sql(query)


def get_all_orders_from_round(round_id):
    query = f"SELECT * FROM orders WHERE round_id = {round_id}"
    return get_sql(query)


def get_all_orders_nice(round_id):
    query = f"""
    SELECT P.name, D.name FROM orders O 
        JOIN person P ON P.person_id = O.person_id
        JOIN drink D ON D.drink_id = O.drink_id
        WHERE O.round_id = {round_id}
"""
    return get_sql(query)


def get_max_round_id():
    query = "SELECT max(round_id) FROM round"
    return get_sql(query)[0][0]


def get_server_id_from_round_id(round_id):
    query = f"SELECT server_id FROM round WHERE round_id = {round_id}"
    return get_sql(query)[0][0]


# save to db

def save_person(name, age=None, favourite_drink_id=None):
    age_dummy = age if age else "NULL"
    favourite_drink_id_dummy = favourite_drink_id if favourite_drink_id else "NULL"
    query = f"INSERT INTO person(name, age, favourite_drink_id) VALUES ('{name.title()}', {age_dummy}, {favourite_drink_id_dummy})"
    write_sql(query)


def save_drink(name, temp=None):
    temp_dummy = temp if temp else "NULL"
    query = f"INSERT INTO drink(name, temp) VALUES ('{name.title()}', '{temp_dummy}')"
    write_sql(query)


def save_favourite(person_id, drink_id):
    query = f"UPDATE person SET favourite_drink_id = {drink_id} WHERE person_id = {person_id}"
    write_sql(query)


def save_order_to_round(person_id, drink_id, round_id):
    query = f"INSERT INTO orders(person_id, drink_id, round_id) VALUES({person_id}, {drink_id}, {round_id})"
    write_sql(query)


# create new round

def new_round(server_id):
    query = f"INSERT INTO round(server_id) VALUES({server_id})"
    write_sql(query)
    return get_max_round_id()


# update db

def update_age_of_person(person_id, age):
    query = f"UPDATE person SET age = {age} WHERE person_id = {person_id}"
    write_sql(query)


def update_drink_preference_of_person(person_id, drink_id):
    query = f"UPDATE person SET favourite_drink_id = {drink_id} WHERE person_id = {person_id}"
    write_sql(query)

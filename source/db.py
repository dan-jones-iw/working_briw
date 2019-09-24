import pymysql
import config


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


query = "INSERT INTO person(name, age) VALUES ('Dan', 22)"
write_sql(query)

query = "DELETE FROM person WHERE person_id > 10"
write_sql(query)

query = "SELECT * FROM person"
result = get_sql(query)
print(result)

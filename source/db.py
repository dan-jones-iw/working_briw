import pymysql
import pymysql.cursors
import config


class Database:
    def __init__(self):
        self.db = None
        self.cursor = None

    def connect_to_database(self):
        try:
            self.db = pymysql.connect(
                config.host,  # host
                "dan",  # username
                config.password,  # password
                "dan",  # database
            )
        except pymysql.MySQLError as e:
            print(e)

    def initialise_cursor(self):
        if self.cursor:
            return
        self.cursor = self.db.cursor()

    def read_people(self):
        self.initialise_cursor()
        self.cursor.execute("SELECT * FROM person")
        results = self.cursor.fetchall()
        return results

    def read_drink(self):
        self.initialise_cursor()
        self.cursor.execute("SELECT * FROM drink")
        results = self.cursor.fetchall()
        return results

    def write_line(self, line):
        self.initialise_cursor()
        self.cursor.exectute("")

    def close(self):
        self.db.close()


db = Database()
db.connect_to_database()
print(db.read_people())
print(db.read_drink())

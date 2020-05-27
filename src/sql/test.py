import os
import pymysql


def execute():
    connection = pymysql.Connect(
        host='localhost',
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        db_info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

    except pymysql.Error as e:
        print("Error while connecting to MySQL", e)
        for line in open("podroze_db.sql"):
            connection.cursor.execute(line)
    finally:
        return connection


def test():
    connection = execute()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_klienta FROM Klient WHERE id_klienta=1")

            result = cursor.fetchall()

            for x in result:
                print(x)

        with connection.cursor() as cursor:
            sql = "SHOW TABLES"
            cursor.execute(sql)
            result = cursor.fetchall()
            for f in result:
                print(f)

    finally:
        connection.close()

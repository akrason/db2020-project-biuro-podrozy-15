import os
import pymysql


def execute():

    database = os.getcwd() + "podroze_db.sql"
    connection = pymysql.Connect(
        host='localhost',
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except pymysql.Error as e:
        print("Error while connecting to MySQL", e)
        with open(database) as fp:
            line = fp.readline()
            cnt = 0
            while line:
                print("Line {}: {}".format(cnt, line.strip()))
                line = fp.readline()
                cnt += 1
                cursor.execute(line)
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

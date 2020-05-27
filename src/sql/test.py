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
        # with connection.cursor() as cursor:
        #     sql = "INSERT INTO t VALUES(%s)"
        #     cursor.execute(sql, 35)
        # connection.commit()

        with connection.cursor() as cursor:
            sql = "SELECT imie FROM Klient"
            cursor.execute(sql)
            result = cursor.fetchall()
            for f in result:
                print(f.get("imie"))
    finally:
        connection.close()
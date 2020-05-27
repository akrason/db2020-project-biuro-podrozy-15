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
    finally:
        cursor.execute("SELECT nazwisko FROM Klient WHERE id_klienta=1")

        result = cursor.fetchall()

        for x in result:
            print(x)
    # with connection.cursor() as cursor:
    #     sql = "INSERT INTO t VALUES(%s)"
    #     cursor.execute(sql, 35)
    # connection.commit()

    with connection.cursor() as cursor:
         sql = "SHOW TABLES"
         cursor.execute(sql)
         result = cursor.fetchall()
         for f in result:
             print(f)

    #connection.cursor().execute("CREATE TABLE Transport (id_transportu INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, koszt_transportu DECIMAL(8,2),typ_transportu ENUM('samolot','statek','pociąg','autobus','własny') NOT NULL, miejsce_wyjazdu VARCHAR(100))")




    connection.close()
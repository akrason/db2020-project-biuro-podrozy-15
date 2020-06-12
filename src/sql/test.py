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
            cursor.execute("select database();")

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


def test(kraj):
    connection = execute()
    try:
        with connection.cursor() as cursor:
            func = ("SELECT kraj,miasto,hotel.nazwa,hotel.nocleg_cena FROM miejsce \
                 INNER JOIN hotel ON miejsce.id_miejsca = hotel.id_miejsca \
                  WHERE kraj LIKE '%s'") % kraj
            cursor.execute(func)

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


def show_offers():
    connection = execute()
    try:
        with connection.cursor() as cursor:
            sql = ("SELECT m.kraj, m.miasto, h.nazwa, t.typ_transportu, t.miejsce_wyjazdu, cena, data_wyjazdu, \
                data_powrotu FROM oferta o \
                LEFT JOIN miejsce m ON m.id_miejsca = o.id_miejsca \
                INNER JOIN hotel h ON h.id_hotelu = o.id_hotelu \
                INNER JOIN transport t ON t.id_transportu = o.id_transportu;")
            cursor.execute(sql)
            result = cursor.fetchall()
            print("Dostępne oferty: ")
            for f in result:
                print(f)
    finally:
        connection.close()


def test_update(kraj,miasto):
    connection = execute()
    try:
        with connection.cursor() as cursor:
            sql = ("INSERT INTO podroze_db.miejsce (kraj, miasto) VALUES ( '%s', '%s');") % (kraj, miasto)
            cursor.execute(sql)
            sql1 =("SELECT kraj,miasto FROM miejsce WHERE kraj = '%s' AND miasto = '%s';") % (kraj, miasto)

            cursor.execute(sql1)
            result = cursor.fetchall()
            print("Zmiany:")

            for f in result:
                print(f)

            ask = input("Czy chcesz wprowadzić następujące zmiany?(Y/N): ")
            if ask == "Y":
                connection.commit()
                do_testu()
            else:
                connection.rollback()
                do_testu()
    finally:
        connection.close()

def do_testu():
    connection = execute()
    try:
        with connection.cursor() as cursor:
            sql = ("SElECT * FROM miejsce")
            cursor.execute(sql)
            result = cursor.fetchall()
            for f in result:
                print(f)
    finally:
        connection.close()

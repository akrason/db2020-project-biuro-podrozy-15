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


def show_places():
    def show_offers():
        connection = execute()
        try:
            with connection.cursor() as cursor:
                sql = ("SELECT * FROM miejsce;")
                cursor.execute(sql)
                result = cursor.fetchall()
                print("Miejsca znajdujące się w bazie: ")
                for f in result:
                    print(f)
        finally:
            connection.close()


def add_place():
    connection = execute()
    kraj = input("Podaj państwo jakie chcesz dodać: ")
    miasto = input("Podaj miasto jakie chcesz dodać: ")

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
            else:
                connection.rollback()
                fix_autoincrement(miasto,'miejsce')
    finally:
        connection.close()


def fix_autoincrement(var1, var2):
    connection = execute()
    try:
        with connection.cursor() as cursor:
            sql = ("SELECT MAX('%s') FROM %s")%(var1,var2)
            cursor.execute(sql)
            result = cursor.fetchall()
            sql1=("ALTER TABLE '%s' AUTO_INCREMENT = result")%var2
            cursor.execute(sql1)

    finally:
        connection.close()


def add_hotel():
    nazwa = input("Podaj nazwę hotelu: ")
    cena = input("Podaj cenę za nocleg: ")
    show_places()
    q1 = input("Czy miejsce znajduje się w bazie? (Y/N)")
    if q1 == "N":
        add_place()
    elif q1 == "Y":
        miejsce = input("Podaj id miejsca: ")

    connection = execute()

    try:
        with connection.cursor() as cursor:
            sql = ("INSERT INTO podroze_db.hotel (nocleg_cena, id_miejsca, nazwa) \
            VALUES ( '%s', %d,'%s');") % (cena, miejsce, nazwa)
            cursor.execute(sql)
            cursor.execute(sql)
            sql1 = ("SELECT nocleg_cena, nazwa FROM hotel WHERE nazwa = '%s';") % (nazwa)

            cursor.execute(sql1)
            result = cursor.fetchall()

            print("Zmiany:")

            for f in result:
                print(f)

            ask = input("Czy chcesz wprowadzić następujące zmiany?(Y/N): ")
            if ask == "Y":
                connection.commit()
            else:
                connection.rollback()
                fix_autoincrement(nazwa, 'hotel')
    finally:
        connection.close()

def login_klient(nazwa):
    connection = execute()
    try:
        with connection.cursor() as cursor:
            sql = ("SELECT email,haslo FROM klient")
            cursor.execute(sql)
            result = cursor.fetchall()
            print("Dostępne oferty: ")
            for f in result:
                if nazwa == f['email']:
                    x = True
                    passwd = input("Podaj hasło: ")
                    if passwd == f['haslo']:
                        return 1
                    else:
                        print("Błędne hasło")
                    break
                else:
                    x = False
            if not x:
                return 2
            else:
                return 3


    finally:
        connection.close()

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


def find_place(kraj):
    connection = execute()
    try:
        with connection.cursor() as cursor:
            func = ("SELECT kraj,miasto FROM miejsce \
                  WHERE kraj LIKE '%s'") % kraj
            cursor.execute(func)

            result = cursor.fetchall()

            for x in result:
                print(x)

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
            i = 1
            for f in result:
                print(i, ".", f)
                i += 1
    finally:
        connection.close()


def show_places():
    connection = execute()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM miejsce;"
            cursor.execute(sql)
            result = cursor.fetchall()
            print("Miejsca znajdujące się w bazie: ")
            for f in result:
                print(f)
    finally:
        connection.close()


def show_hotels(miejsce):
    connection = execute()
    try:
        with connection.cursor() as cursor:
            sql = ("SELECT kraj,miasto,hotel.nazwa,hotel.nocleg_cena FROM miejsce\
            INNER JOIN hotel ON miejsce.id_miejsca = hotel.id_miejsca\
            WHERE kraj LIKE '%s';") % miejsce
            cursor.execute(sql)
            result = cursor.fetchall()

            for x in result:
                print(x)

    finally:
        connection.close()


def add_place():
    connection = execute()
    kraj = input("Podaj państwo jakie chcesz dodać: ")
    miasto = input("Podaj miasto jakie chcesz dodać: ")

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO podroze_db.miejsce (kraj, miasto) VALUES ( '%s', '%s');" % (kraj, miasto)
            cursor.execute(sql)
            sql1 = "SELECT kraj,miasto FROM miejsce WHERE kraj = '%s' AND miasto = '%s';" % (kraj, miasto)

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
                fix_autoincrement('id_miejsca', 'miejsce')
    finally:
        connection.close()


def fix_autoincrement(var1, var2):
    connection = execute()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT MAX(%s) FROM %s" % (var1, var2)
            cursor.execute(sql)
            result = cursor.fetchall()
            key = list(result[0].keys())
            key = key[0]
            sql1 = "ALTER TABLE %s AUTO_INCREMENT = %d" % (var2, result[0][key])
            cursor.execute(sql1)
            cursor.commit()

    finally:
        connection.close()


def add_hotel():
    connection = execute()

    nazwa = input("Podaj nazwę hotelu: ")
    cena = input("Podaj cenę za nocleg: ")
    show_places()
    q1 = input("Czy miejsce znajduje się w bazie? (Y/N)")
    if q1 == "N":
        add_place()
    elif q1 == "Y":
        miejsce = int(input("Podaj id miejsca: "))

    try:
        with connection.cursor() as cursor:
            sql = ("INSERT INTO podroze_db.hotel (nocleg_cena, id_miejsca, nazwa) \
            VALUES ( '%s', %d,'%s');") % (cena, miejsce, nazwa)
            cursor.execute(sql)
            sql1 = "SELECT nocleg_cena, nazwa FROM hotel WHERE nazwa = '%s';" % nazwa

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
                fix_autoincrement('id_hotelu', 'hotel')
    finally:
        connection.close()


def add_offer():
    connection = execute()

    ilosc = int(input("Podaj ilość dostępnych miejsc: "))
    show_places()
    miejsce = int(input("Podaj id miejsca: "))
    data_w = input("Data wyjazdu: ")
    data_p = input("Data powrotu: ")
    transport = 11

    try:
        with connection.cursor() as cursor:
            sql = ("SELECT id_hotelu,nazwa,nocleg_cena FROM hotel \
            LEFT JOIN miejsce m ON m.id_miejsca = hotel.id_miejsca;")
            cursor.execute(sql)
            result = cursor.fetchall()
            print("Baza hoteli w danym miejscu: ")
            for f in result:
                print(f)

        hotel = int(input("Podaj id hotelu: "))

        with connection.cursor() as cursor:
            sql = "SELECT nocleg_cena FROM hotel WHERE id_hotelu = %d;" % hotel
            cursor.execute(sql)
            hotel_cena = cursor.fetchall()
            hotel_cena = hotel_cena['nocleg_cena']

        cena = 14 * hotel_cena

        with connection.cursor() as cursor:
            sql = ("INSERT INTO podroze_db.oferta(cena, ilosc_miejsc, id_miejsca,\
            id_transportu, id_hotelu, data_wyjazdu, data_powrotu) VALUES (%d,%d,%d,%d,%d,%s,%s);") \
                  % (cena, ilosc, miejsce, transport, hotel, data_w, data_p)
            cursor.execute(sql)

            ask = input("Czy chcesz wprowadzić następujące zmiany?(Y/N): ")
            if ask == "Y":
                connection.commit()
            else:
                connection.rollback()
                fix_autoincrement('id_oferty', 'oferta')
    finally:
        connection.close()


def login_klient(nazwa):
    connection = execute()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT email,haslo FROM klient"
            cursor.execute(sql)
            result = cursor.fetchall()
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

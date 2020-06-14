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
                INNER JOIN transport t ON t.id_transportu = o.id_transportu")

            print("""Sortuj według:
            1. Cena(najniższa)
            2. Cena(najwyższa)
            3. Miejsce(od A do Z)
            4. Miejsce(od Z do A)
            5. Najpopularniejsze
            6. Najmniej popularne
            """)
            ask = int(input(""))
            if ask == 1:
                add = ' ORDER BY cena;'
                sql = sql + add
            elif ask == 2:
                add = ' ORDER BY cena DESC;'
                sql = sql + add
            elif ask == 3:
                add = ' GROUP BY h.nazwa ORDER BY m.miasto;'
                sql = sql + add
            elif ask == 4:
                add = ' GROUP BY h.nazwa ORDER BY miasto DESC;'
                sql = sql + add
            elif ask == 5:
                sql = ("SELECT m.kraj, m.miasto, h.nazwa, t.typ_transportu, t.miejsce_wyjazdu, cena, data_wyjazdu, \
                data_powrotu, COUNT(r.id_rezerwacji) AS LiczbaKupionych FROM oferta o \
                LEFT JOIN miejsce m ON m.id_miejsca = o.id_miejsca \
                INNER JOIN hotel h ON h.id_hotelu = o.id_hotelu \
                INNER JOIN transport t ON t.id_transportu = o.id_transportu\
                LEFT JOIN rezerwacja r ON r.id_oferty = o.id_oferty \
                GROUP BY h.nazwa ORDER BY LiczbaKupionych DESC;")
            elif ask == 6:
                sql = ("SELECT m.kraj, m.miasto, h.nazwa, t.typ_transportu, t.miejsce_wyjazdu, cena, data_wyjazdu, \
                data_powrotu, COUNT(r.id_rezerwacji) AS LiczbaKupionych FROM oferta o \
                LEFT JOIN miejsce m ON m.id_miejsca = o.id_miejsca \
                INNER JOIN hotel h ON h.id_hotelu = o.id_hotelu \
                INNER JOIN transport t ON t.id_transportu = o.id_transportu\
                LEFT JOIN rezerwacja r ON r.id_oferty = o.id_oferty \
                GROUP BY h.nazwa ORDER BY LiczbaKupionych ASC;")
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
            sql = ("SELECT  hotel.id_hotelu, kraj,miasto,hotel.nazwa,hotel.nocleg_cena FROM miejsce\
            INNER JOIN hotel ON miejsce.id_miejsca = hotel.id_miejsca\
            WHERE kraj LIKE '%s';") % miejsce
            cursor.execute(sql)
            result = cursor.fetchall()

            for x in result:
                print(x)

    finally:
        connection.close()


def show_transport():
    connection = execute()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM transport"
            cursor.execute(sql)
            result = cursor.fetchall()
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
            connection.commit()

    finally:
        connection.close()


def add_hotel():
    nazwa = input("Podaj nazwę hotelu: ")
    cena = input("Podaj cenę za nocleg: ")
    show_places()
    q1 = input("Czy miejsce znajduje się w bazie? (Y/N)")
    if q1 == "N":
        add_place()
    miejsce = int(input("Podaj id miejsca: "))

    connection = execute()
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
    ilosc = int(input("Podaj ilość dostępnych miejsc: "))
    show_places()
    miejsce = int(input("Podaj id miejsca: "))
    data_w = input("Data wyjazdu: ")
    data_p = input("Data powrotu: ")
    show_transport()
    transport = int(input("Podaj id transportu: "))
    connection = execute()
    try:
        with connection.cursor() as cursor:
            sql = ("SELECT id_hotelu,nazwa,nocleg_cena FROM hotel \
            WHERE id_miejsca = %d;") % miejsce
            cursor.execute(sql)
            result = cursor.fetchall()
            print("Baza hoteli w danym miejscu: ")
            for f in result:
                print(f)
        ask = input("Czy chcesz dodać nowy hotel? (Y/N) ")
        if ask == "Y":
            add_hotel()

        with connection.cursor() as cursor:
            sql = ("SELECT id_hotelu,nazwa,nocleg_cena FROM hotel \
            WHERE id_miejsca = %d;") % miejsce
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
            hotel_cena = list(hotel_cena)
            hotel_cena = hotel_cena[0]['nocleg_cena']

        with connection.cursor() as cursor:
            sql = "SELECT koszt_transportu FROM transport WHERE id_transportu = %d;" % transport
            cursor.execute(sql)
            transport_cena = cursor.fetchall()
            transport_cena = list(transport_cena)
            transport_cena = transport_cena[0]['koszt_transportu']

        with connection.cursor() as cursor:
            sql = "SELECT DATEDIFF('%s','%s');" % (data_p, data_w)
            cursor.execute(sql)
            dni = cursor.fetchall()
            key = list(dni[0].keys())
            key = key[0]
            dni = dni[0][key]

        cena = dni * hotel_cena + 2 * transport_cena

        with connection.cursor() as cursor:
            sql = ("INSERT INTO podroze_db.oferta(cena, ilosc_miejsc, id_miejsca,\
            id_transportu, id_hotelu, data_wyjazdu, data_powrotu) VALUES (%d,%d,%d,%d,%d,'%s','%s');") \
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


def add_user():
    connection = execute()

    print("Podaj swoje dane.")
    email = input("Adres e-mail: ")
    haslo1 = input("Podaj hasło: ")
    haslo2 = input("Powtórz hasło: ")
    while haslo1 != haslo2:
        print("Podane hasła różnią się")
        haslo1 = input("Podaj hasło: ")
        haslo2 = input("Powtórz hasło: ")
    imie = input("Imię: ")
    nazwisko = input("Nazwisko: ")
    nr = int(input("Nr telefonu: "))

    sql = "INSERT INTO podroze_db.klient(imie, nazwisko, email,\
            nr_telefonu, haslo) VALUES ('%s', '%s', '%s', '%d', '%s')" % \
          (imie, nazwisko, email, nr, haslo1)

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)

            ask = input("Czy chcesz wprowadzić następujące zmiany?(Y/N): ")
            if ask == "Y":
                connection.commit()
            else:
                connection.rollback()
                fix_autoincrement("id_klienta", "klient")
    finally:
        connection.close()


def add_reservation(nazwa):
    connection = execute()
    try:
        with connection.cursor() as cursor:
            osoby = int(input("Podaj liczbę osób: "))
            sql = ("SELECT o.id_oferty,m.kraj, m.miasto, h.nazwa,  cena, data_wyjazdu, data_powrotu FROM oferta o \
                    LEFT JOIN miejsce m ON m.id_miejsca = o.id_miejsca \
                    INNER JOIN hotel h ON h.id_hotelu = o.id_hotelu \
                    WHERE o.ilosc_miejsc > %d") % osoby

            cursor.execute(sql)
            row = cursor.fetchall()
            for f in row:
                print(f)
            id_o = int(input("Wybierz id oferty: "))

            sql1 = "SELECT id_klienta FROM klient \
                   WHERE klient.email = '%s'" % nazwa
            cursor.execute(sql1)
            id = cursor.fetchall()
            klient = list(id)
            klient = klient[0]['id_klienta']

            sql2 = "INSERT INTO podroze_db.rezerwacja (liczba_osob, data_rezerwacji,\
                         platnosc, id_klienta, id_oferty) VALUES (%d, LOCALTIME(), 0, %d, %d);" % (osoby, klient, id_o)
            cursor.execute(sql2)

            sql3 = "SELECT ilosc_miejsc FROM oferta WHERE id_oferty = '%s'" % id_o
            cursor.execute(sql3)
            miejsca = cursor.fetchall()
            oferta = list(miejsca)
            oferta = oferta[0]['ilosc_miejsc']
            oferta = oferta - osoby

            sql4 = "UPDATE oferta SET ilosc_miejsc = '%d' WHERE id_oferty =  '%d'" % (oferta, id_o)
            cursor.execute(sql4)
            ask = input("Czy chcesz wprowadzić następujące zmiany?(Y/N): ")
            if ask == "Y":
                connection.commit()
            else:
                connection.rollback()
                fix_autoincrement('id_rezerwacji', 'rezerwacja')
    finally:
        connection.close()


def delete_reservation(email):
    connection = execute()

    try:
        with connection.cursor() as cursor:
            sql = ("SELECT rezerwacja.id_rezerwacji, klient.imie, klient.nazwisko, miejsce.kraj, miejsce.miasto,\
            hotel.nazwa, rezerwacja.liczba_osob, rezerwacja.data_rezerwacji,\
            oferta.data_wyjazdu, oferta.data_powrotu, oferta.cena,\
            transport.typ_transportu, transport.miejsce_wyjazdu FROM klient\
            INNER JOIN rezerwacja ON rezerwacja.id_klienta=klient.id_klienta\
            INNER JOIN oferta ON rezerwacja.id_oferty=oferta.id_oferty\
            INNER JOIN transport ON oferta.id_transportu=transport.id_transportu\
            INNER JOIN hotel ON oferta.id_hotelu=hotel.id_hotelu\
            INNER JOIN miejsce ON hotel.id_miejsca=miejsce.id_miejsca WHERE klient.email = '%s';") % email
            cursor.execute(sql)

            result = cursor.fetchall()
            print("Moje rezerwacje: ")
            for f in result:
                print(f)

            id_r = int(input("Wybierz id rezerwacji do usunięcia:"))

            sql1 = ("SELECT platnosc FROM rezerwacja INNER JOIN klient ON rezerwacja.id_klienta =\
                    klient.id_klienta WHERE klient.email = '%s'\
                    AND rezerwacja.id_rezerwacji = '%d'") % (email, id_r)
            cursor.execute(sql1)
            platnosc = cursor.fetchall()
            if not platnosc:
                print("Brak rezerwacji o podanym id")
            else:
                status = list(platnosc)
                status = status[0]['platnosc']
                if status == 1:
                    print("Nie można usunąć opłaconej rezerwacji!")
                elif status == 0:
                    sql2 = ("SELECT liczba_osob FROM rezerwacja\
                     WHERE id_rezerwacji = '%d'") % id_r
                    cursor.execute(sql2)
                    liczba_o = cursor.fetchall()
                    l_o = list(liczba_o)
                    l_o = l_o[0]['liczba_osob']

                    sql3 = ("SELECT rezerwacja.id_oferty FROM rezerwacja\
                    WHERE id_rezerwacji = '%d'") % id_r
                    cursor.execute(sql3)
                    id_of = cursor.fetchall()
                    id_o = list(id_of)
                    id_o = id_o[0]['id_oferty']

                    sql4 = "DELETE FROM rezerwacja WHERE id_rezerwacji = '%d'" % id_r
                    cursor.execute(sql4)

                    sql5 = "SELECT ilosc_miejsc FROM oferta WHERE id_oferty = '%d'" % id_o
                    cursor.execute(sql5)
                    liczba_miejsc = cursor.fetchall()
                    lm = list(liczba_miejsc)
                    lm = lm[0]['ilosc_miejsc']
                    lm = lm + l_o

                    sql6 = ("UPDATE oferta SET ilosc_miejsc = '%d'\
                     WHERE id_oferty = '%d'") % (lm, id_o)
                    cursor.execute(sql6)

                    ask = input("Czy chcesz wprowadzić następujące zmiany?(Y/N): ")
                    if ask == "Y":
                        connection.commit()
                    else:
                        connection.rollback()
    finally:
        connection.close()


def my_reservations(email):
    connection = execute()

    try:
        with connection.cursor() as cursor:
            sql = ("SELECT klient.imie, klient.nazwisko, miejsce.kraj, miejsce.miasto,\
                hotel.nazwa, rezerwacja.liczba_osob, rezerwacja.data_rezerwacji,\
                oferta.data_wyjazdu, oferta.data_powrotu, oferta.cena,\
                transport.typ_transportu, transport.miejsce_wyjazdu FROM klient\
                INNER JOIN rezerwacja ON rezerwacja.id_klienta=klient.id_klienta\
                INNER JOIN oferta ON rezerwacja.id_oferty=oferta.id_oferty\
                INNER JOIN transport ON oferta.id_transportu=transport.id_transportu\
                INNER JOIN hotel ON oferta.id_hotelu=hotel.id_hotelu\
                INNER JOIN miejsce ON hotel.id_miejsca=miejsce.id_miejsca WHERE klient.email = '%s';") % email
            cursor.execute(sql)

            result = cursor.fetchall()
            print("Moje rezerwacje: ")
            for f in result:
                print(f)

            connection.commit()
    finally:
        connection.close()


def update_hotel():
    kraj = input("W jakim kraju znajduje się hotel? ")
    show_hotels(kraj)
    hotel = int(input("Wybierz id hotelu: "))
    cena = float(input("Wpisz nową cenę: "))
    connection = execute()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE hotel SET nocleg_cena = %d WHERE id_hotelu = %d" % (cena, hotel)
            cursor.execute(sql)
            ask = input("Czy chcesz wprowadzić następujące zmiany?(Y/N): ")
            if ask == "Y":
                connection.commit()

            else:
                connection.rollback()

    finally:
        connection.close()


def update_payment():

    klient = int(input("Podaj id klienta: "))
    platnosc = input("Czy klient zapłacił za rezerwację?(Y/N):  ")
    if platnosc == "Y":
        p = 1
    else:
        p = 0

    connection = execute()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM rezerwacja Where id_klienta = %d"%klient
            cursor.execute(sql)

            result = cursor.fetchall()
            print("Rezerwacje klienta: ")
            for f in result:
                print(f)

        rez = int(input("Podaj id rezerwacji: "))

        with connection.cursor() as cursor:
            sql = "UPDATE rezerwacja SET platnosc = %d WHERE id_rezerwacji = %d" % (p, rez)
            cursor.execute(sql)
            connection.commit()
    finally:
        connection.close()


def delete_res():
    connection = execute()
    try:
        with connection.cursor() as cursor:

            klient = int(input("Podaj id klienta: "))
            sql = "SELECT * FROM rezerwacja Where id_klienta = %d" % klient
            cursor.execute(sql)

            result = cursor.fetchall()
            print("Rezerwacje klienta: ")
            for f in result:
                print(f)

            rez = int(input("Podaj id rezerwacji: "))
            sql1 = "DELETE FROM rezerwacja WHERE id_rezerwacji = %d" % rez
            cursor.execute(sql1)

            ask = input("Czy chcesz wprowadzić następujące zmiany?(Y/N): ")
            if ask == "Y":
                connection.commit()

            else:
                connection.rollback()

    finally:
        connection.close()

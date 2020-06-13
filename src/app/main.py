import src.sql.test as api


def panel_pracownika():
    print("""
1. Dodawanie miejsca do bazy
2. Dodawanie hotelu do bazy
3. Dodawanie oferty
""") # jakieś updates i selecty jeszcze tu, na sam koniec exit
    ask = int(input("Wybierz jedną z opcji: \n"))
    if ask == 1:
        api.add_place()
    elif ask == 2:
        api.add_hotel()
    elif ask == 3:
        api.add_offer()


def panel_klienta():
    print("""
1. Dostępne oferty
2. Wyszukaj miejsce
3. Wykonaj rezerwacje
OSTATNI. Wyjście""")
    ask = int(input("Wybierz jedną z opcji: \n"))
    if ask == 1:
        print("""Sortuj według:
1. Cena(najniższa)
2. Cena(najwyższa)
3. Miejsce(od A do Z)
4. Miejsce(od Z do A)
5. Najpopularniejsze
6. Najmniej popularne""") #popularność group by rezerwacje
        api.show_offers()
    elif ask == 2:
        miejsce = input("Kraj: ")
        api.find_place(miejsce)
        q1 = input("Czy chcesz zobaczyć hotele w danym kraju? (Y/N)")
        if q1 == "Y":
            api.show_hotels(miejsce)
    elif ask == 3:
        api.show_offers()
        oferta = int(input("Którą ofertę wybierasz?"))
        #tutaj insert rezerwacji ze zmiana transportu i zmiana ceny wtedy cena = dni* hotel + 2*transport
    else:
        sys.exit()


def start():
    print(""" Witaj!
    
1. Logowanie do panelu pracownika
2. Logowanie jako klient
3. Rejestracja
4. Koniec
""")
    ask = int(input("Wybierz jedną z opcji: \n"))
    if ask == 1:
        haslo = input("Podaj hasło: ")
        if haslo == "podroze":
            while 1:
                panel_pracownika()
        else:
            print("Błędne hasło")
            start()
    elif ask == 2:
        nazwa = input("Podaj adres e-mail:")
        value = api.login_klient(nazwa)
        if value == 1:
            print("Zostałeś zalogowany")
            while 1:
                panel_klienta()
        elif value == 2:
            print("Nie ma takie użytkownika w bazie. Spróbuj jeszcze raz lub zarejestruj się")
            start()
        else:
            print("Spróbuj jeszcze raz!")
            start()
    elif ask == 3:
        # Tu trzeba dodać insert klienta

        start()
        pass
    elif ask == 4:
        sys.exit()


if __name__ == '__main__':
    import sys
    start()

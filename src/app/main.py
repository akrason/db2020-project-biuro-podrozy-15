import src.sql.test as api

api.execute()
api.test("Hiszpania")
api.show_offers()


def panel_pracownika():
    print("""
1. Dodawanie miejsca do bazy
2. Dodawanie hotelu do bazy
3. Dodawanie oferty
""")

def panel_klienta():
    print("""
1. Dostępne oferty
2. Wyszukaj miejsce
3. Wykonaj rezerwacje""")
    ask = int(input("Wybierz jedną z opcji: \n"))
    if ask == 1:
        api.show_offers()


def start():
    print(""" Witaj!
    
1. Logowanie do panelu pracownika
2. Logowanie jako klient
3. Rejestracja
""")
    ask = int(input("Wybierz jedną z opcji: \n"))
    if ask == 1:
        haslo = input("Podaj hasło: ")
        if haslo == "podroze":
            panel_pracownika()
        else:
            print("Błędne hasło")
    elif ask == 2:
        nazwa = input("Podaj adres e-mail:")
        value = api.login_klient(nazwa)
        if value == 1:
            print("Zostałeś zalogowany")
            panel_klienta()
        elif value == 2:
            print("Nie ma takie użytkownika w bazie. Spróbuj jeszcze raz lub zarejestruj się")
        else:
            print("Spróbuj jeszcze raz!")
    elif ask == 3:
        # Tu trzeba dodać insert klienta
        pass


if __name__ == '__main__':
    import sys

    start()


import src.sql.test as api
import src.app.modules.klient as klient
import src.app.modules.pracownik as pracownik


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
                pracownik.panel_pracownika()
        else:
            print("Błędne hasło")
            start()
    elif ask == 2:
        nazwa = input("Podaj adres e-mail:")
        value = api.login_klient(nazwa)
        if value == 1:
            print("Zostałeś zalogowany")
            while 1:
                klient.panel_klienta(nazwa)
        elif value == 2:
            print("Nie ma takie użytkownika w bazie. Spróbuj jeszcze raz lub zarejestruj się")
            start()
        else:
            print("Spróbuj jeszcze raz!")
            start()
    elif ask == 3:
        api.add_user()

        start()
        pass
    elif ask == 4:
        sys.exit()


if __name__ == '__main__':
    import sys
    start()

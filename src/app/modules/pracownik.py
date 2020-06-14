import src.sql.test as api
import sys


def panel_pracownika():
    print("""
1. Dodawanie miejsca do bazy
2. Dodawanie hotelu do bazy
3. Dodawanie oferty
4. Powrót do menu
5. Exit
""") # jakieś updates i selecty jeszcze tu, na sam koniec exit
    ask = int(input("Wybierz jedną z opcji: \n"))
    if ask == 1:
        api.add_place()
    elif ask == 2:
        api.add_hotel()
    elif ask == 3:
        api.add_offer()
    elif ask == 4:
        pass
    elif ask == 5:
        sys.exit()
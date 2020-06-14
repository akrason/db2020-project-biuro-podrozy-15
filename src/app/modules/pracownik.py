import src.sql.test as api
import sys


def panel_pracownika():
    print("""
1. Dodawanie miejsca do bazy
2. Dodawanie hotelu do bazy
3. Dodawanie oferty
4. Nowa cena noclegu w hotelu
5. Aktualizacja stanu płatności rezerwacji
6. Powrót do menu
7. Wyjście
""")
    ask = int(input("Wybierz jedną z opcji: \n"))
    if ask == 1:
        api.add_place()
    elif ask == 2:
        api.add_hotel()
    elif ask == 3:
        api.add_offer()
    elif ask == 4:
        api.update_hotel()
    elif ask == 5:
        api.update_payment()
    elif ask == 6:
        return 2
    elif ask == 7:
        sys.exit()
    return 1

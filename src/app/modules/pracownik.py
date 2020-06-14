import src.sql.funkcje as api
import sys


def panel_pracownika():
    print("""
1. Dodawanie miejsca do bazy
2. Dodawanie hotelu do bazy
3. Dodawanie oferty
4. Nowa cena noclegu w hotelu
5. Aktualizacja stanu płatności rezerwacji
6. Usunięcie rezerwacji
7. Powrót do menu
8. Exit
""")  # jakieś updates i selecty jeszcze tu, na sam koniec exit
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
        api.delete_res()
    elif ask == 7:
        return 2
    elif ask == 8:
        sys.exit()
    return 1

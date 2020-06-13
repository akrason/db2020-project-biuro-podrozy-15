import src.sql.test as api
import sys


def panel_klienta(email):
    print("""
1. Dostępne oferty
2. Wyszukaj miejsce
3. Wykonaj rezerwacje
4. Moje rezerwacje
OSTATNI. Wyjście""")
    ask = int(input("Wybierz jedną z opcji: \n"))
    if ask == 1:
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
    elif ask == 4:
        api.my_reservations(email)
    else:
        sys.exit()
# Wytyczne do projektu z przedmiotu Bazy Danych 2020

| Kierunek              | Przedmiot   | Semestr | Rok akademicki |
| :-------------------: | :---------: | :-----: | :------------: |
| Informatyka Stosowana | Bazy danych | 4       | 2019/2020      |

## Informacje wstępne
Projekt z przedmiotu Bazy Danych realizowany jest w grupach dwuosobowych. Celem projektu jest **zaprojektowanie** oraz **implementacja** systemu bazodanowego na wylosowany przez grupę temat. Grupa ma prawo zmienić temat na inny, wybrany przez siebie, jednak nie może się on znajdować na zbiorczej liście.

## Struktura projektu
```bash
.
├── /resources/    # Pliki zasobów w projekcie (SS, rysunki, schematy)
│   └── /README.md # Opis projektu w formie pliku markdown
├── /src/          # Katalog główny projektu
│   ├── /app/      # Kod źródłowy aplikacji
│   └── /sql/      # Zapytania SQL
├── /.gitignore    # Pliki i foldery pomijane przy commitowaniu do repozytorium
└── /README.md     # Opis projektu: wytyczne
```
Projekt składa się z trzech części - projektu bazy danych, zaimplementowania funkcjonalności za pomocą języka SQL oraz wykorzystaniem napisanych zapytań w aplikacji.

### Projekt bazy danych
Pierwszym etapem projektu jest stworzenie schematu bazy danych i jego wizualizacja przy pomocy diagramu ERD. Diagram należy przechowywać w repozytorium i zaprezentować w postaci pliku markdown. [Przykładowy plik](resources/example.md) znajduje się w katalogu resources. Najlepszym rozwiązaniem będzie zastąpienie treści tego pliku opisem projektu.

Schemat bazy powinien być przemyślany i zawierać niezbędne encje oraz łączące je relacje. Niedopuszczalne jest, aby diagram był niespójny - wszystkie encje powinny być połączone w _jeden spójny system_. Liczba encji na schemacie oraz szczegółowość ich opisu wpływa na ocenę końcową.

W miarę możliwości, encje należy rozstawiać w sposób niwelujący przecięcia lub minimalizujący ich liczbę. Zbyt duża liczba połączeń na schemacie może być przyczyną wystąpienia przecięć. Wówczas należy przeanalizować schemat i w razie konieczności usunąć zbędne powiązania między encjami.

### Implementacja zapytań SQL
Przygotowany schemat bazy danych ma służyć, by przechowywać stan aplikacji, co pozwala na realizowanie wielu z jej funkcjonalności. W odniesieniu do oprogramowania, funkcjonalność pozwala na zrealizowanie potrzeby użytkownika w ściśle określonych warunkach. Inaczej, jest to możliwość oferowana przez system informatyczny, spełniająca wymagania jego użytkowników.

Funkcjonalność składa się ze zbioru funkcji (sekwencji kroków), który umożliwia uzyskanie finalnego rezultatu, jakiego spodziewa się użytkownik. Na poziomie oprogramowania może to być metoda klasy, cała klasa a czasem nawet moduł.

Państwa zadaniem będzie zaimplementowanie strony bazodanowej, która jest podstawą do zrealizowania wielu funkcjonalności klasycznego systemu informatycznego. Schemat bazy danych został wykonany w poprzednim etapie niniejszego projektu. W tym z kolei należy napisać odpowiednie CRUDy (INSERT, UPDATE, DELETE oraz proste jednotabelowe SELECTy) oraz zapytania grupy DQL (ang. _Data Query Language_), które na poziomie aplikacji dostarczą możliwości do implementacji interfejsu użytkownika, zaspokajających wymagania uzytkowników projektowanego systemu. Definicja tych potrzeb należy do Was: należy je sformułować w formie opisowej (zdanie lub kilka zdań) a następnie napisać jako zapytanie lub grupę zapytań SQL (patrz punkt 3 poniżej: jest to przykład wykorzystania podzapytań). W kolejnym etapie zapytania te mają zostać wykorzystane w prostej aplikacji.

Przykłady funkcjonalności w kontekście bazodanowym:
1. Przeszukiwanie samochodu po pojemności silnika i marce. Dodatkowo użytkownik systemu życzy sobie posortować wyniki wyszukiwania po liczbie koni mechanicznych.
    ```sql
    SELECT m.mark_name, c.model, m.in_produce, c.no_doors, c.engine_displacement, c.hp
    FROM Car c
    LEFT JOIN Mark m ON c.mark_id=m.mark_id
    ORDER BY c.hp;
    ```
    Wybór kolumn zależy od poziomu szczegółowości systemu.
2. Wyświetlenie ile samochodów danej marki znajduje się aktualnie w sprzedaży. Na początku wyświetl marki z największą liczbą samochodów.
    ```sql
    SELECT COUNT(c.mark_id) AS cars_count, m.mark_name
    FROM Car c
    LEFT JOIN Mark m ON c.mark_id=m.mark_id
    GROUP BY m.mark_name
    ORDER BY cars_count DESC;
    ```
3. Aktualizacja bieżącej ceny pojazdu na podstawie tabeli żniżek dla aut wyprodukowanych w zeszłym roku.
    ```sql
    UPDATE Car c
    SET
        c.price = c.price * (
            SELECT d.val
            FROM Discount d
            WHERE d.criteria='prev_year'
        )
    WHERE c.production_year = YEAR(CURDATE()) - 1;
    ```

### Aplikacja
Etapem ostatnim projektu jest zaimplementowanie prostej aplikacji (najlepiej konsolowej) do wizualizacji projektu systemu. Preferowany jest język Python w połączeniu z biblioteką [ _pymysql_](https://pymysql.readthedocs.io/en/latest/).
Aplikacja powinna wykorzystywać napisane wcześniej zapytania SQL (CRUD+DQL), by zrealizować wylistowane w opisie systemu funkcjonalności. Apka **nie może** mieć formy **wyłącznie** switcha:
```java
switch(choice) {
    case 1: func1(args); break;
    case 2: func2(args); break;
    //etc
    default: print(message);
}
```
gdyż nie taki jest cel jej implementacji. Poprawne rozwiązanie może zawierać w sobie takie rozgałęzienie opcji wyboru, jednak należy pamiętać o odpowiednim przepływie informacji - należy umożliwić interakcję z użytkownikiem. Przykładowe drzewo interakcji:

```java
// Wprowadź swój numer klienta
// Wyświetl listę możliwych operacji
// 1. Kup bilet
    // Wybierz rodzaj ulgi
        // a. Ulga ustawowa
        // b. Ulga samorządowa
        // c. Bilet normalny
    // Wprowadź liczbę biletów, którą chcesz kupić
    // Informacja zwrotna z systemu czy udało się kupić bilety lub wyjaśnienie co spowodowało błąd
    callSqlFunctionAndShowOutput(input);
// 2. Zwróć niewykorzystany bilet
    // Wyświetl bilety, które nie zostały wykorzystane
    // Wybierz bilet, który chcesz zwrócić
    // Informacja zwrotna z systemu czy udało się zwrócić bilet lub wyjaśnienie co spowodowało błąd
    callSqlFunctionAndShowOutput(input);
// 3. Sprawdź swoje bilety
    // Wyświetl listę wszystkich biletów, zakupionych przez użytkownika
    callSqlFunctionAndShowOutput(viewId);
// 4. Wyjście z programu
    exit();
```

Jest to przykład ilustrujący przepływ informacji w systemie. W zależności od wprowadzonych informacji (`input`) wywoyłane będzie inne zapytanie SQL. Obiekt `viewId` można traktować jako numer widoku, np. pod numerem 4 wywoływany jest widok wszystkich biletów (zapytanie SELECT). Jednak finalny kod aplikacji powinien być dostosowany pod konkretny projekt a wywołania funkcji odnosić się do obiektów związanych z systemem, np. `user.addNewTickets(discountType, ticketCount)`.

Proszę pamiętać, że aplikacja jest **dla Was**, nie dla mnie i ma Wam pomóc w zrozumieniu funkcji baz danych w wytwarzaniu oprogramowania. Z punktu widzenia wyłącznie tego projektu, implementacja apki ma Wam pomóc w dwójnasób:
* Łatwiej jest definiować zapytania pod funkcjonalności, których działanie można zweryfikować.
* Implementując UI pod zapytania zwiększa się szansa na wykrycie błędów w samym schemacie lub zapytaniu.

Napisanie aplikacji jest obowiązkowe do zaliczenia projektu, jednak jej jakość nie będzie w znacznym stopniu wpływała na ocenę z projektu.

### Przykładowy projekt
Przykładowy projekt znajdą Państwo w przygotowanym przeze mnie [repozytorium](https://github.com/phajder-databases/sample-project). Proszę, aby Państwo nie kopiowali 1:1 mojej wizji. Podany projekt ma charakter wyłącznie poglądowy i jest niewystarczający do uzyskania pozytywnej oceny.

## Wymagania i kryteria oceny
Ocena z projektu będzie średnią ważoną trzech czynników:

| Lp. |       Czynnik       |  Waga |
| :-: | :------------------ | :---: |
|  1  | Projekt bazy danych |  0.3  |
|  2  | Implementacja SQL   |  0.6  |
|  3  | Aplikacja           |  0.1  |

Do uzyskania pozytywnej oceny konieczne jest wykonanie wszystkich trzech części oraz wykonanie stosownego opisu w pliku [README.md](project/README.md). Cała praca powinna znajdować się w wygenerowanym na Github Classroom repozytorium.

Dla każdej z części obowiązują następujące wymagania:
1. Schemat bazy danych powinien składać się z co najmniej 5 encji, jednak ich faktyczna liczba powinna wynikać z realizowanego tematu oraz być zwiększana w oparciu o zdefiniowane przez Was funkcjonalności. Nie należy jednak tego rozumieć na zasadzie 1 encja = 1 funkcjonalność. Dodatkowe informacje:
    1. Każda z encji musi podsiadać klucz główny i, jeśli to możliwe, powinien być to klucz naturalny, np. numer albumu studenta jest dobrym kluczem naturalnym, jednak numer PESEL obywatela już nie ze względów bezpieczeństwa. Numer ISBN książki jest klasycznym przykładem klucza naturalnego, gdyż jest unikalny i każda książka go posiada. Z przyczyn technicznych nie należy stosować kluczy złożonych, gdyż utrudni to pracę z relacjami (wyjątkiem mogą być tabele pośrednie relacji m..n, jednak tylko w przypadku gdy nie posiada ona innych kolumn).
    2. Na schemacie nie mogą znajdować się rozłączne fragmenty, w nomenklaturze teoriografowej, schemat powinien być spójny.
    3. Nie należy sztucznie pompować schematu w dodatkowe encje lub atrybuty, jeżeli nie ma to podparcia w późniejszej implementacji zapytań. Na schemacie powinny zostać zawarte wyłącznie wykorzystywane elementy.
2. Najważniejszą częścią projektu jest implementacja zapytań SQL, realizujących wskazane w projekcie funkcjonalności.
    1. Każda z funkcjonalności musi składać się z _co najmniej jednego_ zapytania. Nie dopuszcza się sytuacji, w której jedno zapytanie realizuje więcej niż jedną funkcjonalność.
    2. W zależności od wykorzystanej palety klauzul (JOIN'y, unie, GROUP BY'e, HAVING'i, podzapytania - to w granicach rozsądku, może jakieś CTE jak zdążymy przerobić) przyznawane będą różne liczby punktów.
        1. Ważne jest, aby zapytania nie były przesadnie rozbudowane, gdyż to sprawia więcej bólu niż przynosi korzyści.
        2. Będę patrzył również na _sensowność_ zapytania. Uważajcie więc na _over-engineering_. Nie powinno być przerostu formy nad treścią.
    3. Ocena zależeć będzie również od liczby zaproponowanych funkcjonalności. W standardowych przypadkach można przyjąć, że max punktów jest za 12 funkcjonalności (po 5% max punktów za zapytanie). Jeżeli będą to zapytania w stylu zagnieżdżonych w sobie grupowań, mogę to zaliczać x2.
    4. Jeśli schemat będzie przejrzysty a opis projektu schludny, to dużo łatwiej jest mi ocenić jego jakość. Należy jak najmniej pozostawić domysłom. Dobrym założeniem w opisie tej części będzie, że czytelnik (tj. ja) ma mierne pojęcie o bazach danych.
    5. Wszystkie zapytania, wraz z funkcjonalnością jaką realizują oraz krótkim opisem, powinny znaleźć się w opisie projektu.
3. Ostatnim elementem oceny będzie aplikacja, jednak jak łatwo zauważyć, nie jest ona wysoko punktowana. Dobra aplikacja będzie mieć głównie wpływ w przyadku, gdy waham się pomiędzy ocenami.
    1. W opisie projektu powinny znaleźć się 2-3 snippety, w jaki sposób realizujecie zapytania do bazy. Opis będzie wtedy kompletny.
    2. Aplikacja jest zwieńczeniem Waszej pracy z jednej strony, z drugiej natomiast pozwoli Wam wyłapać błędy. Możecie więc przyjąć jedną z dwóch taktyk. Wybierzcie mądrze, w zależności od tego jak Wam się najlepiej pracuje:
        1. Podejście iteracyjne - po każdym kamieniu milowym (ustalajcie sobie je jak chcecie) dokonujecie implementacji w aplikacji. W ten sposób unikniecie długiej męki pod koniec.
        2. Implementacja apki pod sam koniec - w ten sposób skupicie się głównie na projekcie bazy, jednak w razie rażących błędów, może okazać się, że braknie później czasu na poprawę.
    3. Dobrze byłoby też zawrzeć krótki opis (1-2 komendy, 2-3 zdania) jak aplikację uruchomić oraz jak ją obsługiwać, np. można przedstawić jeden prosty usecase.

Jeżeli coś jest niejasne, bardzo proszę o zakładanie Issues. W ten sposób wszyscy będziecie mieć dostęp do mojej odpowiedzi na czyjeś wątpliwości. Będę też informował w takim Issues o wprowadzonych zmianach.

## Narzędzia
1. [_Projekt bazy danych_](#projekt-bazy-danych): diagram powinien być czytelny, więc należy go wyeksportować do formatu wektorowego, najlepiej SVG. Do tego celu można wykorzystać następujące narzędzia:
    1. [DrawIO](https://drawio-app.com/). Przykład dołączenia diagramów DrawIO do pliku markdown znajdą Państwo w [wiki DrawIO](https://github.com/jgraph/drawio/wiki/Embed-Diagrams) oraz na [ich repo](https://github.com/jgraph/drawio-github).
    2. [Visual Paradigm](https://www.visual-paradigm.com/tutorials/how-to-model-relational-database-with-erd.jsp). Plik projektu VP nie musi znajdować się na repo, wystarczy tylko wyeksportowana grafika.
    3. Niektóre IDE do pracy z BD mają wbudowane narzędzia do generacji takich diagramów, np. [SQL Server Management Studio](https://stackoverflow.com/questions/32379038/how-to-generate-entity-relationship-er-diagram-of-a-database-using-microsoft-s) dla MSSQL czy [DataGrip](https://www.jetbrains.com/help/datagrip/creating-diagrams.html).
2. [_Implementacja zapytań SQL_](#implementacja-zapytań-sql): do pisania zapytań SQL można wykorzystać dowolne IDE, pozwalające na pracę z bazami danych:
    1. [Squirrel SQL](http://squirrel-sql.sourceforge.net/) jest lekkim Javowym klientem do obsługi połączeń z bazami danych.
    2. [DataGrip](https://www.jetbrains.com/datagrip/) multiplatformowy klient do połączeń z bazami danych. Wymagana jest licencja, by z niego korzystać, jednak studenci i pracownicy uczelni mają ją za darmo. Trzeba tylko zarejestrować się z mailem w domenie edu.
    3. [Narzędzia JetBrains'a](https://www.jetbrains.com/help/pycharm/managing-data-sources.html) mają dostępny plugin do obsługi baz danych, więc można połączyć pracę z bazą i implementację w Pythonie w PyCharm'ie.
    4. **Uwaga**: do połączenia z bazą danych wymagany jest odpowiedni sterownik. [Czym jest sterownik?](https://www.jdatalab.com/information_system/2017/02/16/database-driver.html) W DataGrip'ie to jeden przycisk, w Squirrelu trzeba dodać go w [odpowiedni sposób](http://home.agh.edu.pl/~phajder/2020_IS_BD/extra/SquirrelConfig.pdf).
3. [_Aplikacja_](#aplikacja): do implementacji aplikacji zalecam wykorzystanie języka Python w połączeniu z biblioteką do bazy mysql - [_pymysql_](https://pymysql.readthedocs.io/en/latest/). Do pracy można wykorzystać następujace IDE:
    1. [PyCharm](https://www.jetbrains.com/pycharm/) od JetBrainsa. Wersja community powinna być wystarczająca. Znacząco uprości to też pracę z gitem.
    2. [Visual Studio Code](https://code.visualstudio.com/). Małe IDE, które można rozbudować pod własne potrzeby. Konieczne będzie zainstalowanie [pluginu do Pythona](https://github.com/Microsoft/vscode-python) przez menedżer pluginów. Dostępne są też narzędzia do pracy z SQLem.
    3. Dopuszczalne jest wykorzystanie innego języka programowania, np. Java, C#, js, przy czym prosiłbym o indywidualny kontakt w takiej sytuacji. Nie wolno wykorzystywać frameworków typu ORM, gdyż projekt polega na pisaniu zapytań SQL.

## Uwagi i wskazówki
1. Najważniejsza sprawa na początek - niezależnie czy zajęcia wrócą do normalnej formy czy do końca semestru będą prowadzone zdalnie, pamiętajcie jedną rzecz: **Ja się nie domyślę, że czegoś nie potraficie zrobić lub czegoś nie rozumiecie**. Musicie koniecznie się ze mną komunikować, gdyż podczas oddawania projektu nie chcę słyszeć _myśmy nie wiedzieli..._ Jestem tu po to, żeby Wam pomóc i wyjaśnić wątpliwości, jednak musicie mi dawać odpowiednio wcześnie znać.
2. Do pracy nad projektem wymagana jest praca na repozytorium gitowym. Informacje na ten temat przekażę Państwu w ramach wykładu z _Administracji Sieciami Komputerowymi_. Nieumiejętna praca z takim repozytorium może nie tylko przysporzyć problemów, ale również doprowadzić to całkowitej _utylizacji_ Waszego projektu. Dopóki nie będziecie czuć się pewnie z gitem, trzymajcie sobie gdzieś kopię plików (nie kopiujcie całego repo, bo jest tam katalog _.git_, który może Wam bardzo wiele namieszać, gdybyście spróbowali nadpisywać jego pliki).
3. Celem napisania aplikacji do obsługi bazy danych jest zrozumienie sensu wykorzystywania baz danych. Taka aplikacja może Państwu pomóc w ocenie, czy dane zapytanie zostało poprawnie napisane. Powinna również ocenę poprawności schematu.
4. Ocenę będę rozpoczynał od czytania opisu. Gdy coś będzie niejasne lub czegoś nie będę rozumiał, będę pytał Was zaglądając do umieszczonego kodu. Im lepszy opis, tym mniej wątpliwości mieć będę i tym lepszą ocenę wystawię.
5. Jako że projekt jest dwuosobowy, dzielcie się pracą. Ładnie będzie później to widać w repozytorium a przy okazji nauczycie się w nim pracować w małej, ale jednak grupie. O ile tworzenie schematu ciężko będzie zrealizować w formie dzielonej, o tyle już pisanie funkcjonalności zdecydowanie da się prowadzić równolegle. To samo tyczy się aplikacji.
6. Gdy będę miał wątpliwości czy obie osoby mają równomierny wkład w projekt, będę zerkał w historię commitów. Może warto jednak o to zadbać?

## Przydatne materiały
1. Poza wykładem z ASK, dołączam tutaj przykładowe źródła dotyczące gita:
    1. [Pro Git by Scott Chacon](https://git-scm.com/book/pl/v2);
    2. [Git basics by Academind](https://academind.com/learn/web-dev/git-the-basics/);
    3. Nie jestem zwolennikiem zaczynania nauki od YT, bo często _prowadzący_ popełnia sporo błędów lub wprowadza skróty myślowe, jednak te trzy filmy zasługują na uznanie i mogę je polecić z czystym sumieniem:
        1. [Git - core concepts](https://www.youtube.com/watch?v=uR6G2v_WsRA);
        2. [Git - branching and merging](https://www.youtube.com/watch?v=FyAAIHHClqI);
        3. [Git - remotes](https://www.youtube.com/watch?v=Gg4bLk8cGNo);
2. Projektowanie baz danych:
    1. [Wykład o projektowaniu BD](https://docs.google.com/presentation/d/1ZLtBj2qpUruyJmJaJmpjUP3DGLLbHKZt3ADerRlyp3U) z kursu CS145 na Stanford;
    2. Wykłady od Piotra Macioła;
3. Diagramy ERD:
    1. [Entiti Relationship Diagram](https://www.smartdraw.com/entity-relationship-diagram/) w Internecie;
    2. [Model ER wiki](https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model);
    3. [Wykład o modelach ER](https://docs.google.com/presentation/d/1-2I78MMznp_8HZytF1YOdsLlTABlRiKasJH9ffriwHg) z kursu CS145 na Stanford;
4. Język SQL:
    1. [Tech on the Net](https://www.techonthenet.com/mysql/index.php);
    2. [Geeks for Geeks](https://www.geeksforgeeks.org/sql-ddl-dql-dml-dcl-tcl-commands/);
    3. Dokumentacja: [mysql](https://dev.mysql.com/doc/) lub [mariadb](https://mariadb.com/kb/en/documentation/);
    4. Instrukcje na [mojej stronie](http://home.agh.edu.pl/~phajder/2020_IS_BD/).
5. Najlepszym przyjacielem niniejszego projektu powinien być znany wszystkim Internet.
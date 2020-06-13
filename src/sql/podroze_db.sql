DROP DATABASE IF EXISTS podroze_db;
CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'podroze';

CREATE DATABASE IF NOT EXISTS podroze_db CHARACTER SET utf8 COLLATE utf8_polish_ci;

FLUSH PRIVILEGES;


USE podroze_db;



create table klient
(
    id_klienta  int(6) unsigned auto_increment primary key,
    imie        varchar(30)     not null,
    nazwisko    varchar(30)     not null,
    email       varchar(50)     not null,
    nr_telefonu int(9) unsigned not null,
    haslo varchar(30) not null
);

create table miejsce
(
    id_miejsca int(6) unsigned auto_increment primary key,
    kraj       varchar(50) null,
    miasto     varchar(50) null
);

create table hotel
(
    id_hotelu   int(6) unsigned auto_increment primary key,
    nocleg_cena decimal(6, 2)   null,
    id_miejsca  int(6) unsigned null,
    nazwa       varchar(50)     null,
    constraint hotel_ibfk_1 foreign key (id_miejsca) references miejsce (id_miejsca)
);

create index id_miejsca
    on hotel (id_miejsca);

create table transport
(
    id_transportu    int(6) unsigned auto_increment primary key,
    koszt_transportu decimal(8, 2)                                             null,
    typ_transportu   enum ('samolot', 'statek', 'pociąg', 'autobus', 'własny') not null,
    miejsce_wyjazdu  varchar(100)                                              null
);

create table oferta
(
    id_oferty     int(6) unsigned auto_increment primary key,
    cena          decimal(8, 2)   null,
    ilosc_miejsc  int(6)          null,
    id_miejsca    int(6) unsigned null,
    id_transportu int(6) unsigned null,
    id_hotelu     int(6) unsigned null,
    data_wyjazdu  datetime        null,
    data_powrotu  datetime        null,
    constraint oferta_ibfk_1
        foreign key (id_miejsca) references miejsce (id_miejsca),
    constraint oferta_ibfk_2
        foreign key (id_transportu) references transport (id_transportu),
    constraint oferta_ibfk_3
        foreign key (id_hotelu) references hotel (id_hotelu)
);

create index id_hotelu
    on oferta (id_hotelu);

create index id_miejsca
    on oferta (id_miejsca);

create index id_transportu
    on oferta (id_transportu);

create table rezerwacja
(
    id_rezerwacji   int(6) unsigned auto_increment primary key,
    liczba_osob     int(6)          null,
    data_rezerwacji datetime        null,
    platnosc        tinyint(1)      null,
    id_klienta      int(6) unsigned null,
    id_oferty       int(6) unsigned null,
    constraint rezerwacja_ibfk_1
        foreign key (id_klienta) references klient (id_klienta),
    constraint rezerwacja_ibfk_2
        foreign key (id_oferty) references oferta (id_oferty)
);

CREATE INDEX id_klienta
    on rezerwacja (id_klienta);

CREATE INDEX id_oferty
    ON rezerwacja (id_oferty);


INSERT INTO podroze_db.klient (id_klienta, imie, nazwisko, email, nr_telefonu,haslo) VALUES (1, 'Geralt', 'z Rivii', 'rzeznikzBlaviken@gmail.com', 234765894,'1a2s');
INSERT INTO podroze_db.klient (id_klienta, imie, nazwisko, email, nr_telefonu,haslo) VALUES (2, 'Triss', 'Merigold', 'czarymary@temeria.org', 123456789, '3d4f');
INSERT INTO podroze_db.klient (id_klienta, imie, nazwisko, email, nr_telefonu,haslo) VALUES (3, 'Yennefer', 'z Vengerbergu', 'szybkabryka78@brrrum.com', 859473665,'2s4f');
INSERT INTO podroze_db.klient (id_klienta, imie, nazwisko, email, nr_telefonu,haslo) VALUES (4, 'Cirilla', 'Riannon', 'kindersurprajs@muuu.me', 958447337,'3d6h');
INSERT INTO podroze_db.klient (id_klienta, imie, nazwisko, email, nr_telefonu,haslo) VALUES (5, 'Radowid', 'Srogi', 'wiecznyogien@onet.re', 684495865,'1a7j');
INSERT INTO podroze_db.klient (id_klienta, imie, nazwisko, email, nr_telefonu,haslo) VALUES (6, 'Harry', 'Potter', 'blyskawica15@gmail.com', 152635178,'3d9l');
INSERT INTO podroze_db.klient (id_klienta, imie, nazwisko, email, nr_telefonu,haslo) VALUES (7, 'Bilbo', 'Baggins', 'myprecious@interia.org', 185356629,'1a6h');
INSERT INTO podroze_db.klient (id_klienta, imie, nazwisko, email, nr_telefonu,haslo) VALUES (8, 'Gandalf', 'Szary', 'ushallnot@pass.com', 965187264,'1a8k');
INSERT INTO podroze_db.klient (id_klienta, imie, nazwisko, email, nr_telefonu,haslo) VALUES (9, 'Albus', 'Dumbledore', 'cytrynowe@dropsy.me', 189347512,'2s5g');
INSERT INTO podroze_db.klient (id_klienta, imie, nazwisko, email, nr_telefonu,haslo) VALUES (10, 'Paul', 'Walker', 'czerwonastrzala@onet.re', 665798246, '4f2s');

INSERT INTO podroze_db.miejsce (id_miejsca, kraj, miasto) VALUES (1, 'Polska', 'Zakopane');
INSERT INTO podroze_db.miejsce (id_miejsca, kraj, miasto) VALUES (2, 'Polska', 'Gdańsk');
INSERT INTO podroze_db.miejsce (id_miejsca, kraj, miasto) VALUES (3, 'Polska', 'Olsztyn');
INSERT INTO podroze_db.miejsce (id_miejsca, kraj, miasto) VALUES (4, 'Polska', 'Ciechocinek');
INSERT INTO podroze_db.miejsce (id_miejsca, kraj, miasto) VALUES (5, 'Hiszpania', 'Sewilla');
INSERT INTO podroze_db.miejsce (id_miejsca, kraj, miasto) VALUES (6, 'Grecja', 'Saloniki');
INSERT INTO podroze_db.miejsce (id_miejsca, kraj, miasto) VALUES (7, 'Włochy', 'Turyn');
INSERT INTO podroze_db.miejsce (id_miejsca, kraj, miasto) VALUES (8, 'Hiszpania', 'Barcelona');
INSERT INTO podroze_db.miejsce (id_miejsca, kraj, miasto) VALUES (9, 'USA', 'Chicago');
INSERT INTO podroze_db.miejsce (id_miejsca, kraj, miasto) VALUES (10, 'Kanada', 'Toronto');
INSERT INTO podroze_db.miejsce (id_miejsca, kraj, miasto) VALUES (11, 'Japonia', 'Kioto');
INSERT INTO podroze_db.miejsce (id_miejsca, kraj, miasto) VALUES (12, 'Francja', 'Lyon');

INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (1, 100.56, 5, 'El Pingüino');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (2, 255.78, 12, 'Paradis');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (3, 92.00, 2, 'Smart');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (4, 390.15, 6, 'Poseidon');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (5, 120.24, 10, 'Pied-a-Terre');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (6, 160.0, 7, 'Casena di Colli');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (7, 95.50, 1, 'PRL');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (8, 262.0, 9, 'Freehand');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (9, 273.0, 3, 'HP Park');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (10, 152.0, 8, 'Passeig de Gracia');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (11, 229.0, 4, 'Akacja');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (12, 112.0, 11, 'Khaosan Kyoto');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (13, 126, 5, 'Un Patio al Sur');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (14, 681, 12, 'Le Royal Lyon');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (15, 329, 2, 'Boutique');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (16, 199, 6, 'Egnatia');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (17, 205, 10, 'The Roncey');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (18, 219, 7, 'Plaza');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (19, 233, 1, 'Biała owca');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (20, 264, 9, 'Found');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (21, 305, 3, 'Przystań');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (22, 199, 8, 'Catalonia Park');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (23, 160, 4, 'TeoDorka');
INSERT INTO podroze_db.hotel (id_hotelu, nocleg_cena, id_miejsca, nazwa) VALUES (24, 60, 11, 'Ohto');

INSERT INTO podroze_db.transport (id_transportu, koszt_transportu, typ_transportu, miejsce_wyjazdu) VALUES (1, 750, 'samolot', 'Warszawa');
INSERT INTO podroze_db.transport (id_transportu, koszt_transportu, typ_transportu, miejsce_wyjazdu) VALUES (2, 40, 'pociąg', 'Kraków');
INSERT INTO podroze_db.transport (id_transportu, koszt_transportu, typ_transportu, miejsce_wyjazdu) VALUES (3, 650, 'samolot', 'Kraków');
INSERT INTO podroze_db.transport (id_transportu, koszt_transportu, typ_transportu, miejsce_wyjazdu) VALUES (4, 200, 'statek', 'Gdańsk');
INSERT INTO podroze_db.transport (id_transportu, koszt_transportu, typ_transportu, miejsce_wyjazdu) VALUES (5, 700, 'samolot', 'Gdańsk');
INSERT INTO podroze_db.transport (id_transportu, koszt_transportu, typ_transportu, miejsce_wyjazdu) VALUES (6, 600, 'samolot', 'Katowice');
INSERT INTO podroze_db.transport (id_transportu, koszt_transportu, typ_transportu, miejsce_wyjazdu) VALUES (7, 150, 'statek', 'Szczecin');
INSERT INTO podroze_db.transport (id_transportu, koszt_transportu, typ_transportu, miejsce_wyjazdu) VALUES (8, 24, 'pociąg', 'Kraków');
INSERT INTO podroze_db.transport (id_transportu, koszt_transportu, typ_transportu, miejsce_wyjazdu) VALUES (9, 31.5, 'pociąg', 'Warszawa');
INSERT INTO podroze_db.transport (id_transportu, koszt_transportu, typ_transportu, miejsce_wyjazdu) VALUES (10, 48.2, 'pociąg', 'Wrocław');
INSERT INTO podroze_db.transport (id_transportu, koszt_transportu, typ_transportu, miejsce_wyjazdu) VALUES (11, 0, 'własny', '___');

INSERT INTO podroze_db.oferta(id_oferty, cena, ilosc_miejsc, id_miejsca, id_transportu, id_hotelu, data_wyjazdu, data_powrotu) VALUES (1,14*219+2*600,36,7,6,18,'2020-07-03 14:30:00','2020-07-17 19:00:00');
INSERT INTO podroze_db.oferta(id_oferty, cena, ilosc_miejsc, id_miejsca, id_transportu, id_hotelu, data_wyjazdu, data_powrotu) VALUES (2,14*152+2*750,36,8,1,10,'2020-07-10 16:30:00','2020-07-24 09:00:00');
INSERT INTO podroze_db.oferta(id_oferty, cena, ilosc_miejsc, id_miejsca, id_transportu, id_hotelu, data_wyjazdu, data_powrotu) VALUES (3,7*273+2*40,20,3,2,9,'2020-07-03 14:30:00','2020-07-10 19:00:00');
INSERT INTO podroze_db.oferta(id_oferty, cena, ilosc_miejsc, id_miejsca, id_transportu, id_hotelu, data_wyjazdu, data_powrotu) VALUES (4,14*199+2*650,46,8,3,22,'2020-07-30 9:30:00','2020-08-13 19:45:00');

 
COMMIT;
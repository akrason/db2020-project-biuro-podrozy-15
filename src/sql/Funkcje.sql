--1.sortowanie alfabetyczne miejsc podróży
-- a) od A do Z;
SELECT kraj,miasto,hotel.nazwa,hotel.nocleg_cena FROM miejsce
INNER JOIN hotel ON miejsce.id_miejsca = hotel.id_miejsca
ORDER BY kraj ASC;
-- b) od Z do A;
SELECT kraj,miasto,hotel.nazwa,hotel.nocleg_cena FROM miejsce
INNER JOIN hotel ON miejsce.id_miejsca = hotel.id_miejsca 
ORDER BY kraj DESC;
--2. szukanie miejsca - kraju w bazie %s to odpowiednia nazwa
SELECT kraj,miasto,hotel.nazwa,hotel.nocleg_cena FROM miejsce
INNER JOIN hotel ON miejsce.id_miejsca = hotel.id_miejsca
WHERE kraj LIKE '%s';
--3. szukanie miejsca - miasta i hotelów w bazie -%s to odpowiednia nazwa
SELECT kraj,miasto,hotel.nazwa,hotel.nocleg_cena FROM miejsce
INNER JOIN hotel ON miejsce.id_miejsca = hotel.id_miejsca
WHERE miasto LIKE '%s';
--4. dodanie nowego klienta (%) imie,nazwisko,email,numer
BEGIN;
INSERT INTO podroze_db.klient ( imie, nazwisko, email, nr_telefonu) VALUES ( '%s', '%s', '%s', %d);
SELECT imie, nazwisko, email, nr_telefonu FROM klient WHERE imie = "%s" AND nazwisko = "%s";
--czy na pewno chcesz wprowadzic zmiany?
--tak
COMMIT;
--nie
ROLLBACK;
--dodanie nowego miejsca
BEGIN;
INSERT INTO podroze_db.miejsce (kraj, miasto) VALUES ( '%s', '%s');
SELECT kraj,miasto FROM klient WHERE kraj = "%s" AND miasto = "%s";
--czy na pewno chcesz wprowadzic zmiany?
--tak
COMMIT;
--nie
ROLLBACK;
--zaaktualizowanie cen w hotelu
BEGIN;
UPDATE hotel SET nocleg_cena = %d WHERE nazwa = "%s";
SELECT nocleg_cena,nazwa FROM hotel WHERE nazwa = "%s";
--czy na pewno chcesz wprowadzic zmiany?
--tak
COMMIT;
--nie
ROLLBACK;

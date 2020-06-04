--sortowanie alfabetyczne miejsc podróży
--od A do Z;
SELECT kraj,miasto,hotel.nazwa,hotel.nocleg_cena FROM miejsce
INNER JOIN hotel ON miejsce.id_miejsca = hotel.id_miejsca
ORDER BY kraj ASC;
--od Z do A;
SELECT kraj,miasto,hotel.nazwa,hotel.nocleg_cena FROM miejsce
INNER JOIN hotel ON miejsce.id_miejsca = hotel.id_miejsca 
ORDER BY kraj DESC;
--szukanie miejsca - kraju w bazie %s to odpowiednia nazwa
SELECT kraj,miasto,hotel.nazwa,hotel.nocleg_cena FROM miejsce
INNER JOIN hotel ON miejsce.id_miejsca = hotel.id_miejsca
WHERE kraj LIKE '%s';
--szukanie miejsca - miasta i hotelów w bazie -%s to odpowiednia nazwa
SELECT kraj,miasto,hotel.nazwa,hotel.nocleg_cena FROM miejsce
INNER JOIN hotel ON miejsce.id_miejsca = hotel.id_miejsca
WHERE miasto LIKE '%s';
--dodanie nowego klienta (%) imie,nazwisko,email,numer
INSERT INTO podroze_db.klient ( imie, nazwisko, email, nr_telefonu) VALUES ( '%s', '%s', '%s', %d);
--dodanie nowego miejsca
INSERT INTO podroze_db.miejsce (kraj, miasto) VALUES ( '%s', '%s');
--zaaktualizowanie cen w hotelu
UPDATE hotel SET nocleg_cena = %d WHERE nazwa = "%s";


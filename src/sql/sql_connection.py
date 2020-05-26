import mysql.connector
from mysql.connector import Error

try:
    db = mysql.connector.connect(
        host='localhost',                             
        database='podroze_db',
        user='admin',
        password='5cf3897d24dd0883b5d3721b6de2594d023ece6f2fbcc2ddcacc37930548c9c6'
        )
                                         
    if db.is_connected():
        db_Info = db.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = db.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (db.is_connected()):

        #cursor.execute("CREATE TABLE Klient (id_klienta INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, imie VARCHAR(30) NOT NULL, nazwisko VARCHAR(30) NOT NULL, email VARCHAR(50) NOT NULL, nr_telefonu INT(9) UNSIGNED NOT NULL)")
        #cursor.execute("DROP TABLE MyGuests")
        
        #sql="INSERT INTO Klient (imie, nazwisko, email, nr_telefonu) VALUES (%s, %s, %s, %s)"
        #val = ("Jan", "Kowalski", "jkowal@gmail.com", '234765894')
        #cursor.execute(sql, val)
        #db.commit()

        #print("ID: ", cursor.lastrowid)
        cursor.execute("SELECT * FROM Klient")

        result = cursor.fetchall()

        for x in result:
            print(x)
        

        cursor.close()
        db.close()
        print("MySQL connection is closed")
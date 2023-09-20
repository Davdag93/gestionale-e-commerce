import mysql.connector
import pages.register as reg

def nuovo_utente():
    # Colleghiamo il DB
    db = mysql.connector.connect(
        host="localhost",
        user="root",        # abbiamo la possibilità di creare degli user e di impostare ovviamente una password per il DB nascondendola magari con un file .env
        password="",
        database="pharmazon"
    )

    cursore = db.cursor()

    new_user = "INSERT INTO `utenti`(`nome`, `cognome`, `username`, `password`) VALUES (%s,%s,%s,%s)"
    values = ...
    cursore.execute(new_user,values)
    db.commit()
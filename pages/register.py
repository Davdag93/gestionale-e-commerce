from tkinter import * 
from tkinter import messagebox  # per generare messaggi pop-up
import mysql.connector  # per collegare il db
from mysql.connector import errorcode   # per prendere gli errori dal db
import bcrypt   # per cryptare la password
import pages.login as log   # per importare funzionalità da altre pagine
import re # per l'utilizzo delle regex


def show_register_page():

    #funzione che chiude la pagina corrente e apre la pagina login
    def login():
        register.destroy()
        log.show_login_page()

    #funzione di validazione della password - fatta in una funzione a se per motivi di possibile riuso e manutenibilità nel tempo
    def valida_password(password):
        # La password deve contenere almeno 8 caratteri
        # Almeno una lettera maiuscola, almeno un numero e almeno un simbolo speciale tra !?@#$%£&
        password_pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!?\@#\$%\£&])[A-Za-z\d!?\@#\$%\£&]{8,}$'     # regex
        return re.match(password_pattern, password) is not None     # cerca un match tra la stringa password e la regex se esiste crea un oggetto match con la corrispondenza trovata e verifichiamo che l'oggetto restituito sia diverso da None


    #funzione che prende i valori dai campi input e verifica che sia tutto compilato e salva nel db 
    def nuovo_utente():
        val_nome = input_nome.get() # prendiamo i valori dai campi input
        val_cognome = input_cognome.get()
        val_username = input_username.get().replace(" ", "")    #rimuoviamo qualsiasi spazio bianco presente all'interno della stringa inizio, nel mezzo, alla fine.
        val_psw = input_psw.get().replace(" ", "")
        val_psw2 = input_psw2.get().replace(" ", "")

        username_pattern = r"^[a-zA-Z0-9_]+$"   # regex per non consentire l'uso dei simboli tranne l'underscore nell'username

        try:
            if val_nome == "" or val_cognome == "" or val_username == "" or val_psw == "" or val_psw2 == "":    # verifichiamo che i campi siano tutti compilati
                print("campi lasciati vuoti")
                messagebox.showwarning(title="Attenzione!", message="Devi riempire tutti i campi per effettuare la registrazione")  #messaggi pop-up

            elif not re.match(username_pattern, val_username):    #come per la psw cerchiamo una corrispondenza tra regex e username scelto dall'utente, se questa non viene trovata allora generiamo un pop-up d'errore per segnalare il problema
                print("Errore: L'username non è valido.")
                messagebox.showwarning(title="Attenzione!", message="L'username non è valido. Puoi utilizzare solo lettere minuscole, lettere maiuscole, numeri e il carattere underscore.")
                return

            elif val_psw != val_psw2:   # verifichiamo che l'utente non abbia fatto errori nel ripetere la password
                print("errore password non coincidenti!")
                messagebox.showwarning(title="Attenzione!", message="Password e Ripeti Password non coincidono..")

            elif not valida_password(val_psw):  # richiamiamo la funzione valida_password e verifichiamo se è ha superato la validazione o meno
                print("Errore: La password non soddisfa i requisiti.")
                messagebox.showwarning(title="Attenzione!", message="La password deve contenere almeno 8 caratteri, almeno una lettera maiuscola, almeno un numero e almeno uno dei seguenti simboli: !?@#$%£&")
                return  

            else:   # se ha superato tutti i controlli allora procediamo al cryptaggio della password, collegamento al DB, inserimento in tabella e chiusura del DB
                # Crittografa la password
                hashed_password = bcrypt.hashpw(val_psw.encode('utf-8'), bcrypt.gensalt())

                # Colleghiamo il DB
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",        # abbiamo la possibilità di creare degli user e di impostare ovviamente una password per il DB nascondendola magari con un file .env
                    password="",
                    database="pharmazon"    #nome del database
                )
                cursore = db.cursor()   # ci permette di effettuare le chiamate al db

                new_user = "INSERT INTO `utenti`(`nome`, `cognome`, `username`, `password`) VALUES (%s,%s,%s,%s)"   #inserimento valori in tabella utenti
                values = (val_nome, val_cognome, val_username, hashed_password.decode('utf-8')) # Converto l'hash crittografico binario (byte) in una stringa Unicode leggibile prima di inserirlo nel database, poiché il campo del database è di tipo stringa.
                cursore.execute(new_user,values)    # associamo la chiamata INSERT ai valori

                db.commit() #convalidiamo l'inserimento in tabella
                db.close()  #chiudiamo la connessione con il db

                messagebox.showinfo(title="Account creato!", message="Account creato con successo!")
                print("account creato con successo")

                login() #chiudiamo la scheda corrente e apriamo la scheda login

        except mysql.connector.Error as err:    # prendiamo gli erorri generati dal DB 

            if err.errno == errorcode.ER_DUP_ENTRY:
                # Se l'errore è dovuto a un duplicato di chiave unica (ER_DUP_ENTRY)
                print("Errore: Username già in uso!")
                messagebox.showwarning(title="Attenzione!", message="Username già in uso. Scegli un altro username.")

            else:
                # Altro tipo di errore
                print("Errore MySQL:", err)
                messagebox.showerror(title="Errore!", message="Si è verificato un errore durante la registrazione.")


    ##### GUI ######

    register = Tk()

    # Ottiene la larghezza e l'altezza dello schermo
    screen_width = register.winfo_screenwidth()
    screen_height = register.winfo_screenheight()

    # Calcola la posizione centrale della finestra
    x = (screen_width / 2) - (300 / 2)
    y = (screen_height / 2) - (440 / 2)

    # Disabilita il resize della finestra
    register.resizable(width=False, height=False)

    register.geometry("%dx%d+%d+%d" % (300, 440, x, y))
    register.wm_iconbitmap("./favicon.ico")
    register.title("Pharmazon")
    register.configure(bg="lightblue")

    #Register label
    label_title = Label(register, text="REGISTER", fg="blue", font=("Roman", 22), bg="lightblue")
    label_title.grid(column=0, row=0, padx=20, pady=30, sticky=W)  


    #Nome
    label_nome = Label(register, text="Nome", bg="lightblue")
    label_nome.grid(column=0, row=1, padx=20, pady=10, sticky=W)

    input_nome = Entry(register, width=20)
    input_nome.grid(column=1, row=1, sticky=W)

    #Cognome
    label_cognome = Label(register, text="Cognome", bg="lightblue")
    label_cognome.grid(column=0, row=2, padx=20, pady=10, sticky=W)

    input_cognome = Entry(register, width=20)
    input_cognome.grid(column=1, row=2, sticky=W)

    #Username
    label_username = Label(register, text="Username", bg="lightblue")
    label_username.grid(column=0, row=3, padx=20, pady=10, sticky=W)

    input_username = Entry(register, width=20)
    input_username.grid(column=1, row=3, sticky=W)

    #Password
    label_psw = Label(register, text="Password", bg="lightblue")
    label_psw.grid(column=0, row=4, padx=20, pady=10, sticky=W)

    input_psw = Entry(register, width=20, show="*")
    #input_psw.insert(0, "inserisciPSW")
    input_psw.grid(column=1, row=4, padx=0, sticky=W)

    #Ripeti Password
    label_psw2 = Label(register, text="Ripeti Password", bg="lightblue")
    label_psw2.grid(column=0, row=5, padx=20, pady=10, sticky=W)

    input_psw2 = Entry(register, width=20, show="*")
    input_psw2.grid(column=1, row=5, padx=0, sticky=W)


    #Button Invio Dati Register
    btn_invio = Button(register, text="Invio", width=6, height=1, bg="blue",fg="white", command=nuovo_utente)
    btn_invio.grid(column=0, row=6, pady=5, sticky=E, columnspan=2)

    # Rimando a login
    label_siAccount = Label(register, text="Se hai già un account vai su", bg="lightblue")
    label_siAccount.grid(column=0, row=7, padx=(30,0), pady=(20,0), columnspan=2)

    btn_siAccount = Button(register, text="Login", width=12, height=1, bg="green",fg="white", command=login)
    btn_siAccount.grid(column=0, row=8, padx=(35,0),pady=5, columnspan=2)


    register.mainloop()
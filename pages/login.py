from tkinter import * 
from tkinter import messagebox
import pages.register as reg
import pages.homepage as Hpg
import mysql.connector  # per collegare il db
from mysql.connector import errorcode   # per prendere gli errori dal db
import bcrypt   # per cryptare la password

#database
email = "a"
password = "a"

def show_login_page():

    def register():
        login.destroy()
        reg.show_register_page()


    def funcLogin():
        val_username = input_username.get()
        val_psw = input_psw.get()

        try: 

            # Colleghiamoci al database
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="pharmazon"
            )
            cursore = db.cursor()

            # Esegui una query per ottenere la password crittografata dall'username fornito
            cursore.execute("SELECT password FROM utenti WHERE username = %s", (val_username,))
            result = cursore.fetchone() # ci restituisce solo 1 elemento 

            # Chiudi la connessione al database
            db.close()

            if result is not None:
                # Estrai la password crittografata dal risultato della query
                stored_password = result[0]

                # Confronta la password fornita dall'utente con quella crittografata nel database
                if bcrypt.checkpw(val_psw.encode('utf-8'), stored_password.encode('utf-8')):
                    print("Login riuscito!")
                    login.destroy()
                    Hpg.show_homepage()
                    return True
                else:
                    print("Password errata. Accesso negato.")
                    return False
            else:
                print("Utente non trovato.")
                return False
        except  mysql.connector.Error as err:
            # Altro tipo di errore
            print("Errore MySQL:", err)
            messagebox.showerror(title="Errore!", message="Si è verificato un errore durante la login.")




    ##### GUI ######
    login = Tk()

    # Ottiene la larghezza e l'altezza dello schermo
    screen_width = login.winfo_screenwidth()
    screen_height = login.winfo_screenheight()

    # Calcola la posizione centrale della finestra
    x = (screen_width / 2) - (270 / 2)
    y = (screen_height / 2) - (320 / 2)

    login.geometry("%dx%d+%d+%d" % (270, 320, x, y))
    login.wm_iconbitmap("./favicon.ico")
    login.title("Pharmazon")
    login.configure(bg="lightblue")

    # Disabilita il resize della finestra
    login.resizable(width=False, height=False)

    #Login label
    label_title = Label(login, text="LOGIN", fg="green", font=("Roman", 22), bg="lightblue")
    label_title.grid(column=0, row=0, padx=20, pady=30, sticky=W)  


    #Username
    label_username = Label(login, text="Username", bg="lightblue")
    label_username.grid(column=0, row=1, padx=20, pady=10, sticky=W)

    input_username = Entry(login, width=20)
    input_username.grid(column=1, row=1, sticky=W)


    #Password
    label_psw = Label(login, text="Password", bg="lightblue")
    label_psw.grid(column=0, row=2, padx=20, pady=10, sticky=W)

    input_psw = Entry(login, width=20, show="*")
    input_psw.grid(column=1, row=2, padx=0, sticky=W)


    #Button Invio Dati Login
    btn_invio = Button(login, text="Invio", width=6, height=1, bg="green",fg="white", command=funcLogin)
    btn_invio.grid(column=0, row=4, pady=5, sticky=E, columnspan=2)

    # Rimando a register
    label_noAccount = Label(login, text="Se non hai un account vai su", bg="lightblue")
    label_noAccount.grid(column=0, row=6, padx=(40,0), pady=(20,0), columnspan=2)

    btn_noAccount = Button(login, text="Register", width=12, height=1, bg="blue",fg="white", command=register)
    btn_noAccount.grid(column=0, row=7, padx=(50,0),pady=5, sticky=N, columnspan=2)


    login.mainloop()
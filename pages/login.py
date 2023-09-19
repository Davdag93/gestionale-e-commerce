from tkinter import * 
from tkinter import messagebox
import pages.register as reg
import pages.homepage as Hpg

#database
email = "a"
password = "a"

def show_login_page():

    def register():
        login.destroy()
        reg.show_register_page()


    def funcLogin():
        val_email = input_email.get()
        val_psw = input_psw.get()

        if val_email == email and val_psw == password:
            print("Login effettuata")
            login.destroy()

            ####################
            # HOMEPAGE #
            ####################
            Hpg.show_homepage() 

        elif val_email == email and val_psw != password:
            print("Password errata")
            messagebox.showerror(title="Errore!", message="Password errata..")
        elif val_email != email and val_psw == password:
            print("Email errata!")
            messagebox.showerror(title="Errore!", message="Email errata..")
        else:
            print("Tutto sbagliato riprova!")
            messagebox.showerror(title="Errore!", message="Indirizzo email e password errati..")



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
    label_email = Label(login, text="Username", bg="lightblue")
    label_email.grid(column=0, row=1, padx=20, pady=10, sticky=W)

    input_email = Entry(login, width=20)
    input_email.grid(column=1, row=1, sticky=W)


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
from tkinter import * 
from tkinter import messagebox
import pages.login as log


def show_register_page():

    def login():
        register.destroy()
        log.show_login_page()


    """     def funcRegister():
        val_email = input_email.get()
        val_psw = input_psw.get()

        if val_email == email and val_psw == password:
            print("Login effettuata")
            register.destroy()

            ####################
                # LOGIN #
            ####################
            # wpage.show_welcome_page() 

        elif val_email == email and val_psw != password:
            print("Password errata")
            messagebox.showerror(title="Errore!", message="Password errata..")
        elif val_email != email and val_psw == password:
            print("Email errata!")
            messagebox.showerror(title="Errore!", message="Email errata..")
        else:
            print("Tutto sbagliato riprova!")
            messagebox.showerror(title="Errore!", message="Indirizzo email e password errati..") """



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
    label_nome = Label(register, text="Cognome", bg="lightblue")
    label_nome.grid(column=0, row=2, padx=20, pady=10, sticky=W)

    input_nome = Entry(register, width=20)
    input_nome.grid(column=1, row=2, sticky=W)

    #Username
    label_nome = Label(register, text="Username", bg="lightblue")
    label_nome.grid(column=0, row=3, padx=20, pady=10, sticky=W)

    input_nome = Entry(register, width=20)
    input_nome.grid(column=1, row=3, sticky=W)

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
    btn_invio = Button(register, text="Invio", width=6, height=1, bg="blue",fg="white", command="")
    btn_invio.grid(column=0, row=6, pady=5, sticky=E, columnspan=2)

    # Rimando a login
    label_siAccount = Label(register, text="Se hai già un account vai su", bg="lightblue")
    label_siAccount.grid(column=0, row=7, padx=(30,0), pady=(20,0), columnspan=2)

    btn_siAccount = Button(register, text="Login", width=12, height=1, bg="green",fg="white", command=login)
    btn_siAccount.grid(column=0, row=8, padx=(35,0),pady=5, columnspan=2)


    register.mainloop()
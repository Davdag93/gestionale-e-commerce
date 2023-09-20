from tkinter import *
import pages.login as log   # per importare funzionalità da altre pagine
import pages.register as reg

# funzione che chiude la finestra corrente e apre la nuova finestra
def login():
    main.destroy()
    log.show_login_page()

def register():
    main.destroy()
    reg.show_register_page()

main = Tk()

# Ottiene la larghezza e l'altezza dello schermo
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()

# Calcola la posizione centrale della finestra nello schermo
x = (screen_width / 2) - (400 / 2)
y = (screen_height / 2) - (370 / 2)

# Imposta la dimensione della finestra e dove posizionarla
main.geometry("%dx%d+%d+%d" % (400, 370, x, y))

# Disabilita il resize della finestra
main.resizable(width=False, height=False)

main.wm_iconbitmap("favicon.ico")   # favicon finestra
main.title("Pharmazon")                 # titolo finestra
main.configure(bg="lightblue")      # imposta il colore di sfondo

# Nome Azienda label
label_title = Label(main, text="PHARMAZON", fg="blue", font=("Roman", 22), bg="lightblue")
label_title.grid(column=0, row=0, padx=130, pady=(30,20), sticky=W)   # si può mettere anche il columnspan ed il rowspan per unire più colonne/righe

# Descripaion label
label_description = Label(main, text="Gestionale di riferimento \n per gli ordini effettuati sul sito web \n https://www.pharmazon.it/", fg="black", font=("helvetica", 13), bg="lightblue")
label_description.grid(column=0, row=1, padx=50, pady=10, sticky=N)   # si può mettere anche il columnspan ed il rowspan per unire più colonne/righe

# Button login
btn_login = Button(main, text="Login", width=12, height=1,fg="white", bg="green", command=login)
btn_login.grid(column=0, row=2, pady=(30,5), sticky=N, columnspan=1)

# Button register
btn_register = Button(main, text="Registrazione", width=12, height=1,fg="white", bg="blue", command=register)
btn_register.grid(column=0, row=3, pady=(5, 15), sticky=N, columnspan=3)

# Button label
label_button = Label(main, text="Fai la login o la registrazione", fg="black", font=("helvetica", 11), bg="lightblue")
label_button.grid(column=0, row=4, padx=50, sticky=N)


main.mainloop() # tiene aperta la finestra
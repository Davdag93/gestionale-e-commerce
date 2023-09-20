from tkinter import *
import pages.login as log
import pages.gst_prodotti as gst_prd
import pages.ordini as ord
import pages.reg_notifiche as reg_not
from PIL import Image, ImageTk


def show_homepage():

    ##### FUNC #####
    def chiudi():
        homepage.quit() # chiude l'intera applicazione

    def login():
        homepage.destroy()
        log.show_login_page()

    def gst_prodotti():
        homepage.destroy()
        gst_prd.show_gst_prodotti()

    def ordini():
        homepage.destroy()
        ord.show_ordini()
    
    def reg_notifiche():
        homepage.destroy()
        reg_not.show_reg_not()


    ##### GUI ######
    homepage = Tk()

    # Funzione vuota che rende inutilizzabile il tasto X della finestra windows
    def do_nothing():
        return

    # Assegnamo una nostra funzione al pulsante X di chiusura della finestra windows
    homepage.protocol("WM_DELETE_WINDOW",do_nothing)
    
    # Ottiene la larghezza e l'altezza dello schermo
    screen_width = homepage.winfo_screenwidth()
    screen_height = homepage.winfo_screenheight()

    # Calcola la posizione centrale della finestra
    x = (screen_width / 2) - (600 / 2)
    y = (screen_height / 2) - (400 / 2)

    homepage.geometry("%dx%d+%d+%d" % (600, 400, x, y))
    homepage.wm_iconbitmap("./favicon.ico")
    homepage.title("Pharmazon")
    homepage.configure(bg="lightblue")

    # Disabilita il resize della finestra
    homepage.resizable(width=False, height=False)

    # LOGO
    # Carica l'immagine
    original_image = Image.open("./python.gif")

    # Specifica le nuove dimensioni
    new_width = 50
    new_height = 50

    # Ridimensiona l'immagine
    resized_image = original_image.resize((new_width, new_height))

    # Converti l'immagine ridimensionata in un formato tkinter-friendly
    logo = ImageTk.PhotoImage(resized_image)
    labelLogo = Label(homepage, image=logo)
    labelLogo.grid(column=0, row=0, padx=(15,10), pady=10, sticky=W)

    # bottone per chiudere il programma
    btn_chiudi = Button(homepage, text="CHIUDI", width=8, height=1, bg="#d63031", command=chiudi)
    btn_chiudi.grid(column=4, row=0, sticky=E)

    # bottoni
    btn_gestione_prodotti = Button(homepage, text="GESTIONE PRODOTTI", width=30, height=2, bg="#e67e22",fg="white", command=gst_prodotti)
    btn_gestione_prodotti.grid(column=1, row=1, padx=(110,20), pady=(50, 5), sticky=N, columnspan=2)

    btn_ordini = Button(homepage, text="ORDINI", width=30, height=2, bg="#0984e3",fg="white", command=ordini)
    btn_ordini.grid(column=1, row=2, padx=(110,20), pady=5, sticky=N, columnspan=2)

    btn_ordini = Button(homepage, text="REGISTRO NOTIFICHE", width=30, height=2, bg="#27ae60",fg="white", command=reg_notifiche)
    btn_ordini.grid(column=1, row=3, padx=(110,20), pady=(5, 80), sticky=N, columnspan=2)

    # utente loggato
    utente_on=Label(homepage, text="Utente Ciccio", bg="lightblue")
    utente_on.grid(column=3, row=5, padx=5, pady=5, sticky=W)

    # bottone per sloggarsi e riloggarsi con un altro account
    btn_logout = Button(homepage, text="LOGOUT", width=8, height=1, bg="#e17055", command=login)
    btn_logout.grid(column=4, row=5, sticky=E,)
    

    homepage.mainloop()
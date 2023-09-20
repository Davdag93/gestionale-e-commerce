from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pages.homepage as Hpg
import pages.nuovo_prodotto as New_Prd


def show_gst_prodotti():

    ####### FUNC #######
    def chiudi():
        gst_prodotti.quit() # chiude l'intera applicazione

    def indietro():
        gst_prodotti.destroy()
        Hpg.show_homepage()

    def aggiorna():
        gst_prodotti.destroy()
        show_gst_prodotti()

    def nuovo():
        New_Prd.show_nuovo_prodotto()

    def modifica():
        pass 

    ######## GUI ########
    gst_prodotti = Tk()

    # Funzione vuota che rende inutilizzabile il tasto X della finestra windows
    def do_nothing():
        return

    # Assegnamo una nostra funzione al pulsante X di chiusura della finestra windows
    gst_prodotti.protocol("WM_DELETE_WINDOW",do_nothing)

    # Ottiene la larghezza e l'altezza dello schermo
    screen_width = gst_prodotti.winfo_screenwidth()
    screen_height = gst_prodotti.winfo_screenheight()

    # Calcola la posizione centrale della finestra
    x = (screen_width / 2) - (635 / 2)
    y = (screen_height / 2) - (400 / 2)

    gst_prodotti.geometry("%dx%d+%d+%d" % (635, 400, x, y))
    gst_prodotti.wm_iconbitmap("./favicon.ico")
    gst_prodotti.title("Pharmazon")
    gst_prodotti.configure(bg="lightblue")

    # Disabilita il resize della finestra
    gst_prodotti.resizable(width=False, height=False)
    
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
    labelLogo = Label(gst_prodotti, image=logo)
    labelLogo.grid(column=0, row=0, padx=(15,10), pady=10, sticky=W)

    # bottone per tornare indietro
    btn_indietro = Button(gst_prodotti, text="←", width=8, height=1, command=indietro)
    btn_indietro.grid(column=2, row=0, padx=(0,73), sticky=E)

    # bottone per chiudere il programma
    btn_chiudi = Button(gst_prodotti, text="CHIUDI", width=8, height=1, bg="#d63031", command=chiudi)
    btn_chiudi.grid(column=2, row=0, sticky=E)

    # titolo scheda 
    label_title = Label(gst_prodotti, text="Elenco Prodotti A-z", bg="lightblue", font=("helvetica", 18))
    label_title.grid(column=0, row=1, padx=30, pady=(15, 5), sticky=W)

    # bottone per aggiungere un prodotto
    btn_aggiungi = Button(gst_prodotti, text="Nuovo", width=8, font=("",10), height=1, command=nuovo)
    btn_aggiungi.grid(column=2, row=1, padx=(0,50), sticky=E)

    # bottone per aggiornare la tabella
    btn_aggiorna = Button(gst_prodotti, text="⭮", width=4, font=("",10), height=1, command=aggiorna)
    btn_aggiorna.grid(column=2, row=1, padx=(0,0), sticky=E)

    # DEFINIAMO LA TABELLA
    colonne = ('codice', 'prodotto', 'Qnt.', 'prezzo')
    tabella = ttk.Treeview(gst_prodotti, columns=colonne, show='headings')

    tabella.heading('codice', text='CODICE')
    tabella.heading('prodotto', text='PRODOTTO')
    tabella.heading('Qnt.', text='QNT. MAGAZZINO')
    tabella.heading('prezzo', text="PREZZO")

    tabella.column('codice', width=100, anchor='center')
    tabella.column('prodotto', width=250, anchor='center')
    tabella.column('Qnt.', width=150, anchor='center')
    tabella.column('prezzo', width=100, anchor='center')

    righe = []
    for n in range(1,50):
        righe.append((f'{n}', f'prodotto ssdakehi {n}', f'{n}',f'{n}'))

    for riga in righe:
        tabella.insert('', END, values=riga)


    tabella.grid(column=0, row=2, padx=(15, 0), sticky=NSEW, columnspan=3)
    scrollbar = ttk.Scrollbar(gst_prodotti, orient=VERTICAL, command=tabella.yview)
    scrollbar.grid(column=3, row=2, sticky=NS)
    tabella.configure(yscrollcommand=scrollbar.set)


    gst_prodotti.mainloop()

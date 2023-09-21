from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pages.homepage as Hpg


def show_ordini():

    ####### FUNC #######
    def chiudi():
        ordini.destroy()  # chiudiamo la finestra corrente
        ordini.quit() # chiude l'intera applicazione

    def indietro():
        ordini.destroy()
        Hpg.show_homepage()

    def aggiorna():
        ordini.destroy()
        show_ordini()

    

    ######## GUI ########
    ordini = Tk()

    # Funzione vuota che rende inutilizzabile il tasto X della finestra windows
    def do_nothing():
        return

    # Assegnamo una nostra funzione al pulsante X di chiusura della finestra windows
    ordini.protocol("WM_DELETE_WINDOW",do_nothing)

    # Ottiene la larghezza e l'altezza dello schermo
    screen_width = ordini.winfo_screenwidth()
    screen_height = ordini.winfo_screenheight()

    # Calcola la posizione centrale della finestra
    x = (screen_width / 2) - (1030 / 2)
    y = (screen_height / 2) - (400 / 2)

    ordini.geometry("%dx%d+%d+%d" % (1030, 400, x, y))
    ordini.wm_iconbitmap("./favicon.ico")
    ordini.title("Pharmazon")
    ordini.configure(bg="lightblue")

    # Disabilita il resize della finestra
    ordini.resizable(width=False, height=False)
    
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
    labelLogo = Label(ordini, image=logo)
    labelLogo.grid(column=0, row=0, padx=(15,10), pady=10, sticky=W)

    # bottone per tornare indietro
    btn_indietro = Button(ordini, text="←", width=8, height=1, command=indietro)
    btn_indietro.grid(column=2, row=0, padx=(0,73), sticky=E)

    # bottone per chiudere il programma
    btn_chiudi = Button(ordini, text="CHIUDI", width=8, height=1, bg="#d63031", command=chiudi)
    btn_chiudi.grid(column=2, row=0, sticky=E)

    # titolo scheda 
    label_title = Label(ordini, text="Elenco Ordini", bg="lightblue", font=("helvetica", 18))
    label_title.grid(column=0, row=1, padx=30, pady=(15, 5), sticky=W)


    # bottone per aggiornare la tabella
    btn_aggiorna = Button(ordini, text="⭮", width=4, font=("",10), height=1, command=aggiorna)
    btn_aggiorna.grid(column=2, row=1, padx=(0,0), sticky=E)

    # DEFINIAMO LA TABELLA
    colonne = ('cod. spedizione','cod. prodotto', 'prodotto', 'Qnt.', 'prezzo')
    tabella = ttk.Treeview(ordini, columns=colonne, show='headings')

    tabella.heading('cod. spedizione', text='COD. SPEDIZIONE')
    tabella.heading('cod. prodotto', text='COD. PRODOTTO')
    tabella.heading('prodotto', text='PRODOTTO')
    tabella.heading('Qnt.', text='QNT. MAGAZZINO')
    tabella.heading('prezzo', text="PREZZO")

    righe = []
    for n in range(1,50):
        righe.append((f'8SD5FAA5{n}', f'TQYS55D{n}', f'Pappardelle {n}',f'{n}', f'€ {n}'))

    for riga in righe:
        tabella.insert('', END, values=riga)

    tabella.grid(column=0, row=2, padx=(15, 0), sticky=NSEW, columnspan=3)
    scrollbar = ttk.Scrollbar(ordini, orient=VERTICAL, command=tabella.yview)
    scrollbar.grid(column=3, row=2, sticky=NS)
    tabella.configure(yscrollcommand=scrollbar.set)


    ordini.mainloop()

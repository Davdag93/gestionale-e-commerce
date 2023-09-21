from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pages.homepage as Hpg


def show_reg_not():

    ####### FUNC #######
    def chiudi():
        reg_not.destroy()  # chiudiamo la finestra corrente
        reg_not.quit() # chiude l'intera applicazione

    def indietro():
        reg_not.destroy()
        Hpg.show_homepage()

    def aggiorna():
        reg_not.destroy()
        show_reg_not()

    ######## GUI ########
    reg_not = Tk()

    # Funzione vuota che rende inutilizzabile il tasto X della finestra windows
    def do_nothing():
        return

    # Assegnamo una nostra funzione al pulsante X di chiusura della finestra windows
    reg_not.protocol("WM_DELETE_WINDOW",do_nothing)

    # Ottiene la larghezza e l'altezza dello schermo
    screen_width = reg_not.winfo_screenwidth()
    screen_height = reg_not.winfo_screenheight()

    # Calcola la posizione centrale della finestra
    x = (screen_width / 2) - (650 / 2)
    y = (screen_height / 2) - (400 / 2)

    reg_not.geometry("%dx%d+%d+%d" % (650, 400, x, y))
    reg_not.wm_iconbitmap("./favicon.ico")
    reg_not.title("Pharmazon")
    reg_not.configure(bg="lightblue")

    # Disabilita il resize della finestra
    reg_not.resizable(width=False, height=False)
    
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
    labelLogo = Label(reg_not, image=logo)
    labelLogo.grid(column=0, row=0, padx=(15,10), pady=10, sticky=W)

    # bottone per tornare indietro
    btn_indietro = Button(reg_not, text="←", width=8, height=1, command=indietro)
    btn_indietro.grid(column=2, row=0, padx=(0,73), sticky=E)

    # bottone per chiudere il programma
    btn_chiudi = Button(reg_not, text="CHIUDI", width=8, height=1, bg="#d63031", command=chiudi)
    btn_chiudi.grid(column=2, row=0, sticky=E)

    # titolo scheda 
    label_title = Label(reg_not, text="Elenco Notifiche", bg="lightblue", font=("helvetica", 18))
    label_title.grid(column=0, row=1, padx=30, pady=(15, 5), sticky=W)


    # bottone per aggiornare la tabella
    btn_aggiorna = Button(reg_not, text="⭮", width=4, font=("",10), height=1, command=aggiorna)
    btn_aggiorna.grid(column=2, row=1, padx=(0,0), sticky=E)

    # DEFINIAMO LA TABELLA
    colonne = ('cod. notifica','notifica', 'data e ora')
    tabella = ttk.Treeview(reg_not, columns=colonne, show='headings')

    tabella.heading('cod. notifica', text='COD. NOTIFICA')
    tabella.heading('notifica', text='NOTIFICA')
    tabella.heading('data e ora', text='DATA E ORA')

    righe = []
    for n in range(1,50):
        righe.append((f'8SD5FAA5{n}', f'TQYS55D{n}', f'Pappardelle {n}'))

    for riga in righe:
        tabella.insert('', END, values=riga)

    tabella.grid(column=0, row=2, padx=(15, 0), sticky=NSEW, columnspan=3)
    scrollbar = ttk.Scrollbar(reg_not, orient=VERTICAL, command=tabella.yview)
    scrollbar.grid(column=3, row=2, sticky=NS)
    tabella.configure(yscrollcommand=scrollbar.set)


    reg_not.mainloop()

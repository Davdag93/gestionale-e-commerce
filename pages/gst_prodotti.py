from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pages.homepage as Hpg
import pages.nuovo_prodotto as New_Prd
import mysql.connector  # per collegare il db
from tkinter import messagebox
import pages.modifica as mod


def show_gst_prodotti():

    ####### FUNC #######
    def chiudi():
        gst_prodotti.destroy()  # chiudiamo la finestra corrente
        gst_prodotti.quit() # chiude l'intera applicazione

    def indietro():
        gst_prodotti.destroy()
        Hpg.show_homepage()

    def aggiorna():
        popola_tabella()

    def nuovo():
        New_Prd.show_nuovo_prodotto()


    # LA FUNZIONE popola_tabella() E' STATA DICHIARATA DOPO LA CREAZIONE DELLA TABELLA

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
    y = (screen_height / 2) - (410 / 2)

    gst_prodotti.geometry("%dx%d+%d+%d" % (635, 410, x, y))
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
    label_title = Label(gst_prodotti, text="Elenco Prodotti A-Z", bg="lightblue", font=("helvetica", 18))
    label_title.grid(column=0, row=1, padx=30, pady=(15, 5), sticky=W)

    # bottone per aggiungere un prodotto
    btn_aggiungi = Button(gst_prodotti, text="Nuovo", width=8, font=("",10),bg="#05c46b", height=1, command=nuovo)
    btn_aggiungi.grid(column=2, row=1, padx=(0,50), sticky=E)

    # bottone per aggiornare la tabella
    btn_aggiorna = Button(gst_prodotti, text="⭮", width=4, font=("",10), height=1, command=aggiorna)
    btn_aggiorna.grid(column=2, row=1, padx=(0,0), sticky=E)

    # DEFINIAMO LA TABELLA
    colonne = ('codice', 'prodotto', 'Qnt.', 'prezzo')
    tabella = ttk.Treeview(gst_prodotti, columns=colonne, show='headings', selectmode='browse')

    tabella.heading('codice', text='CODICE')
    tabella.heading('prodotto', text='PRODOTTO')
    tabella.heading('Qnt.', text='QNT. MAGAZZINO')
    tabella.heading('prezzo', text="PREZZO")

    tabella.column('codice', width=100, anchor='center')
    tabella.column('prodotto', width=250, anchor='center')
    tabella.column('Qnt.', width=150, anchor='center')
    tabella.column('prezzo', width=100, anchor='center')

    tabella.grid(column=0, row=2, padx=(15, 0), sticky=NSEW, columnspan=3)
    scrollbar = ttk.Scrollbar(gst_prodotti, orient=VERTICAL, command=tabella.yview)
    scrollbar.grid(column=3, row=2, sticky=NS)
    tabella.configure(yscrollcommand=scrollbar.set)

    ##############################
        # FUNC #        FACENDO RIFERIMENTO ALLA VARIABILE TABELLA, BISOGNA SPOSTARE LA FUNZIONE IN BASSO PER QUESTIONI DI NameError
    ##############################

    # Funzione per popolare la tabella con i dati dal database da tabella prodotti
    def popola_tabella():
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="pharmazon"
            )

            cursore = db.cursor()
            cursore.execute("SELECT `codice_prodotto`, `nome_prodotto`, `quantita`, `prezzo` FROM `prodotti` ORDER BY `nome_prodotto` ASC;")

            # Rimuovi tutte le righe esistenti nella tabella prima di inserire i dati aggiornati
            for riga in tabella.get_children(): 
                tabella.delete(riga)

            for riga in cursore:    # dopo aver pulito la tabella la ripopoliamo con i dati aggiornati
                tabella.insert('', END, values=riga)

            cursore.close()
            db.close()  # chiudiamo la connessiane al db
        except mysql.connector.Error as err:
            print("Errore MySQL:", err)
            messagebox.showerror(title="Errore!", message="Errore nel caricamento dei dati, chiudere e riaprire il programma")

    # Chiamata iniziale per popolare la tabella all'avvio dell'applicazione
    popola_tabella()


    def modifica():
        # Ottieni l'elemento selezionato dalla tabella
        selected_item = tabella.selection() 
        if selected_item:
            item = tabella.item(selected_item) 
            values = item["values"]
            mod.show_modifica_prodotto(values)
            print(values)
        else: 
            print("non hai selezionato nessun elemento dalla lista")
            messagebox.showinfo(title="Not Found!", message="Nessun elemento selezionato")


    def elimina():
        # Ottieni l'elemento selezionato dalla tabella
        selected_item = tabella.selection() 
        if selected_item:
            item = tabella.item(selected_item) 
            values = item["values"]
            #con la messagebox.askyesno verifichiamo che l'utente sia sicuro dell'eliminazione del prodotto
            conferma = messagebox.askyesno("Conferma eliminazione", f"Confermi l'eliminazione del prodotto '{values[1]}' con codice '{values[0]}'?")
            if conferma:
                try:
                    # Connessione al database
                    db = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="pharmazon"
                    )

                    # ID dell'elemento da eliminare
                    id_da_eliminare = values[0]

                    # Creazione del cursore
                    cursore = db.cursor()

                    # Query SQL con il segnaposto
                    query = "DELETE FROM prodotti WHERE codice_prodotto = %s"

                    # Esecuzione della query con il valore dell'ID
                    cursore.execute(query, (id_da_eliminare,))

                    # Conferma l'eliminazione nel database
                    db.commit()

                    # Chiusura del cursore e della connessione
                    cursore.close()
                    db.close()
                    print(f"Eliminazione confermata del prodotto {values[0]}")
                    messagebox.showinfo(title="Success!", message=f"Il prodotto con codice {values[0]} è stato eliminato con successo!")
                except mysql.connector.Error as err:
                    print("Errore MySQL:", err)
                    messagebox.showerror(title="Errore!", message="Errore nel caricamento dei dati, chiudere e riaprire il programma")
            else:
                messagebox.showinfo(title="Eliminazione Annullata", message="Hai annullato l'eliminazione del prodotto")
            print(values)
        else: 
            print("non hai selezionato nessun elemento dalla lista")
            messagebox.showinfo(title="Not Found!", message="Nessun elemento selezionato")


    # bottone per modificare un prodotto dalla tabella
    btn_modifica = Button(gst_prodotti, text="Modifica", width=8, bg="#ffc048", font=("",10), height=1, command=modifica)
    btn_modifica.grid(column=2, row=3, padx=(0,80),pady=(10, 5), sticky=E)

    # bottone per eliminare un prodotto dalla tabella
    btn_elimina = Button(gst_prodotti, text="Elimina", width=8, bg="#ff7979", font=("",10), height=1, command=elimina)
    btn_elimina.grid(column=2, row=3, padx=(0,0),pady=(10, 5), sticky=E)

    gst_prodotti.mainloop()

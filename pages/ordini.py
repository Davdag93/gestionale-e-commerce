from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pages.homepage as Hpg
import mysql.connector  # per collegare il db
from mysql.connector import errorcode   # per prendere gli errori dal db
from tkinter import messagebox
import pages.modifica_ordine as mod_ord
import random
import string


def show_ordini(username):

    ####### FUNC #######
    def chiudi():
        ordini.destroy()  # chiudiamo la finestra corrente
        ordini.quit() # chiude l'intera applicazione

    def indietro():
        ordini.destroy()
        Hpg.show_homepage(username)

    def aggiorna():
        popola_tabella()
        print("aggiornata")

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
    x = (screen_width / 2) - (880 / 2)
    y = (screen_height / 2) - (405 / 2)

    ordini.geometry("%dx%d+%d+%d" % (880, 405, x, y))
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
    colonne = ('cod. spedizione','cod. prodotto', 'Qnt.', 'prezzo', 'data_ora', 'id_cliente', 'stato_ordine')
    tabella = ttk.Treeview(ordini, columns=colonne, show='headings')

    tabella.heading('cod. spedizione', text='COD. SPEDIZIONE')
    tabella.heading('cod. prodotto', text='COD. PRODOTTO')
    tabella.heading('Qnt.', text='QNT.')
    tabella.heading('prezzo', text='PREZZO UNITÀ')
    tabella.heading('data_ora', text="DATA ORA")
    tabella.heading('id_cliente', text="ID CLIENTE")
    tabella.heading('stato_ordine', text="STATO")

    tabella.column('cod. spedizione', width=150, anchor='center')
    tabella.column('cod. prodotto', width=110, anchor='center')
    tabella.column('Qnt.', width=60, anchor='center')
    tabella.column('prezzo', width=110, anchor='center')
    tabella.column('data_ora', width=150, anchor='center')
    tabella.column('id_cliente', width=100, anchor='center')
    tabella.column('stato_ordine', width=150, anchor='center')

    tabella.grid(column=0, row=2, padx=(15, 0), sticky=NSEW, columnspan=3)
    scrollbar = ttk.Scrollbar(ordini, orient=VERTICAL, command=tabella.yview)
    scrollbar.grid(column=3, row=2, sticky=NS)
    tabella.configure(yscrollcommand=scrollbar.set)

    ##############################
        # FUNC #        FACENDO RIFERIMENTO ALLA VARIABILE TABELLA, BISOGNA SPOSTARE LA FUNZIONE IN BASSO PER QUESTIONI DI NameError
    ##############################

    # Funzione per popolare la tabella con i dati dal database da tabella ordini
    def popola_tabella():
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="pharmazon"
            )

            cursore = db.cursor()
            cursore.execute("SELECT `cod_spedizione`, `cod_prodotto`, `quantita`, `prezzo_unita`, `data_ora`, `id_cliente`, `stato_ordine` FROM `ordini` ORDER BY `data_ora` DESC;;")

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
            mod_ord.show_modifica_ordine(values)
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
                    query = "DELETE FROM ordini WHERE codice_prodotto = %s"

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

    def codice_spedizione():
        # Ottieni l'elemento selezionato dalla tabella
        selected_item = tabella.selection() 
        if selected_item:
            item = tabella.item(selected_item) 
            values = item["values"]

        if values[0] == None:
            # Genera 4 numeri casuali
            numeri = ''.join(random.choice(string.digits) for _ in range(4))
            # Genera 6 caratteri (lettere maiuscole) casuali
            lettere = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))
            # Combina numeri e lettere in modo casuale
            codice = ''.join(random.sample(numeri + lettere, 10))
            print(codice)

            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="pharmazon"
                )
                cod_p = values[1]
                data_ora = values[4]
                id_cliente = values[5]
                print("i valori",cod_p, data_ora, id_cliente)
                cursore = db.cursor()
                query = "SELECT `id_o` FROM `ordini` WHERE `cod_prodotto` = %s AND `data_ora` = %s AND `id_cliente` = %s"
                val = cod_p, data_ora, id_cliente
                cursore.execute(query, val)
                id_o = cursore.fetchone()
                id = id_o[0]
                print("l'id dell'ordine",id)

                cursore.close()
                db.close()  # chiudiamo la connessiane al db
                add_code(id, codice)
                messagebox.showinfo(title="Codice assegnato!",message="Codice di spedizione assegnato correttamente!")
            except mysql.connector.Error as err:
                messagebox.showerror(title="Errore", message="Errore nell'esecuzione dell'operazione. chiudi e riapri il programma.")
                print("Errore MySQL nel trovare l'ID del prodotto:", err)

        else: 
            messagebox.showinfo(title="Operazione rifiutata", message="L'ordine ha già un codice assegnato.")

    def add_code(id, codice):
        try:
            # Collegamento al database
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="pharmazon"
            )
            # query SQL che modifica
            update_query = "UPDATE `ordini` SET `cod_spedizione`= %s WHERE `id_o` = %s"

            cursore = db.cursor()
            cursore.execute(update_query, (codice, id)) 

            db.commit()
            cursore.close()
            db.close()

            messagebox.showinfo(title="Ordine aggiornato!", message="Codice di spedizione assegnato con successo!")
            print("Codice di spedizione assegnato con successo!")
        except mysql.connector.Error as err:    # prendiamo gli erorri generati dal DB 

            if err.errno == errorcode.ER_DUP_ENTRY:
                # Se l'errore è dovuto a un duplicato di chiave unica (ER_DUP_ENTRY)
                print("Attenzione!")
                messagebox.showwarning(title="Attenzione!", message="Codice prodotto già memorizzato. Andare su Modifica per quel prodotto.")
            else:
                # Altro tipo di errore
                print("Errore MySQL:", err)
                messagebox.showerror(title="Errore!", message="Si è verificato un errore durante l'inserimento.")


    # bottone per generare il codice di spedizione
    btn_genera_cod = Button(ordini, text="Assegna COD.", width=12, bg="lightgreen", font=("",10), height=1, command=codice_spedizione)
    btn_genera_cod.grid(column=2, row=3, padx=(0,160),pady=(10, 5), sticky=E)

    # bottone per modificare un prodotto dalla tabella
    btn_modifica = Button(ordini, text="Modifica", width=8, bg="#ffc048", font=("",10), height=1, command=modifica)
    btn_modifica.grid(column=2, row=3, padx=(0,80),pady=(10, 5), sticky=E)

    # bottone per eliminare un prodotto dalla tabella
    btn_elimina = Button(ordini, text="Elimina", width=8, bg="#ff7979", font=("",10), height=1, command=elimina)
    btn_elimina.grid(column=2, row=3, padx=(0,0),pady=(10, 5), sticky=E)


    ordini.mainloop()

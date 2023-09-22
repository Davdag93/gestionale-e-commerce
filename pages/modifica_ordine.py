from tkinter import * 
from tkinter import ttk
from tkinter import messagebox
import mysql.connector  # per collegare il db
from mysql.connector import errorcode   # per prendere gli errori dal db


def show_modifica_ordine(values):

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
    except mysql.connector.Error as err:
        print("Errore MySQL nel trovare l'ID del prodotto:", err)

        #funzione che prende i valori dai campi input e verifica che sia tutto compilato e salva nel db 
    def modifica_ordine():
        val_code_sp = input_code_sp.get().replace(" ", "").upper() # prendiamo i valori dai campi input, rimuoviamo ogni spazio e lo memorizziamo tutto maiuscolo
        val_qnt = input_qnt.get().replace(" ", "")    #rimuoviamo qualsiasi spazio bianco presente all'interno della stringa inizio, nel mezzo, alla fine.  
        val_prez = input_prezzo.get().replace(" ", "").replace(".", ",")  # rimuoviamo ogni spazio bianco e sostituiamo il . con la virgola in caso di erorre durante l'inserimento
        val_prezzo = val_prez[0] + " " + val_prez[1:]   #rimettiamo 1 singolo spazio tra il simbolo € ed il prezzo, in modo tale che nel db non ci possano essere errori
        val_stato_ord = input_stato_ord.get().strip() # rimuoviamo gli spazi dall'inizio e dalla fine della stringa e mettiamo la prima lettera maiuscola
     
        try:
            if val_code_sp == "" or val_stato_ord == "" or val_qnt == "" or val_prezzo == "":    # verifichiamo che i campi siano tutti compilati
                print("campi lasciati vuoti")
                messagebox.showwarning(title="Attenzione!", message="Devi riempire tutti i campi per effettuare correttamente l'inserimento")  #messaggi pop-up

            else:
                # Chiedi conferma all'utente
                conferma = messagebox.askokcancel("Conferma Modifica", f"Confermi l'aggiornamento dell'ordine con codice {val_code_sp}?")
            
                if conferma:
                    # Collegamento al database
                    db = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="pharmazon"
                    )
                    # dizionario con i valori dei placeholder
                    update_values = val_code_sp, val_qnt, val_prezzo, val_stato_ord, id
                    # query SQL che modifica
                    update_query = "UPDATE `ordini` SET `cod_spedizione`= %s,`quantita`= %s,`prezzo_unita`= %s,`stato_ordine`= %s WHERE `id_o` = %s"

                    cursore = db.cursor()
                    cursore.execute(update_query, update_values) 

                    db.commit()
                    cursore.close()
                    db.close()

                    messagebox.showinfo(title="Ordine aggiornato!", message="Ordine aggiornato con successo!")
                    print("Ordine aggiornato con successo")
                    mod_ordine.destroy()
                else:
                    print("Modifica annullata")

        except mysql.connector.Error as err:    # prendiamo gli erorri generati dal DB 

            if err.errno == errorcode.ER_DUP_ENTRY:
                # Se l'errore è dovuto a un duplicato di chiave unica (ER_DUP_ENTRY)
                print("Attenzione!")
                messagebox.showwarning(title="Attenzione!", message="Codice spedizione già in uso.")

            else:
                # Altro tipo di errore
                print("Errore MySQL:", err)
                messagebox.showerror(title="Errore!", message="Si è verificato un errore durante l'inserimento.")


    ##### GUI ######

    mod_ordine = Tk()

    # Ottiene la larghezza e l'altezza dello schermo
    screen_width = mod_ordine.winfo_screenwidth()
    screen_height = mod_ordine.winfo_screenheight()

    # Calcola la posizione centrale della finestra
    x = (screen_width / 2) - (340 / 2)
    y = (screen_height / 2) - (400 / 2)

    # Disabilita il resize della finestra
    mod_ordine.resizable(width=False, height=False)

    mod_ordine.geometry("%dx%d+%d+%d" % (340, 400, x, y))
    mod_ordine.wm_iconbitmap("./favicon.ico")
    mod_ordine.title("Pharmazon")
    mod_ordine.configure(bg="lightblue")

    #Modifica Ordine label
    label_title = Label(mod_ordine, text="Modifica Ordine", font=("helvetica", 16), bg="lightblue")
    label_title.grid(column=0, row=0, padx=(20,0), pady=30, sticky=W)  


    #Codice Spedizione
    label_code_sp = Label(mod_ordine, text="Codice Spedizione", bg="lightblue")
    label_code_sp.grid(column=0, row=1, padx=20, pady=10, sticky=W)

    input_code_sp = Entry(mod_ordine, width=20)
    input_code_sp.insert(0, values[0])
    input_code_sp.grid(column=1, row=1, sticky=W)

    #Stato ordine
    label_stato_ord = Label(mod_ordine, text="Stato ordine", bg="lightblue")
    label_stato_ord.grid(column=0, row=2, padx=20, pady=10, sticky=W)

    stato = StringVar()
    input_stato_ord = ttk.Combobox(mod_ordine, textvariable=stato, width=17)
    input_stato_ord['values'] = ["Nuovo", "In lavorazione", "Spedito"]
    input_stato_ord['state'] = 'readonly'
    """ Entry(mod_ordine, width=20)
    input_stato_ord.insert(0, values[1]) """
    input_stato_ord.grid(column=1, row=2, sticky=W)

    """ def stato_selezionato():
        nuovo_stato = stato.get()
        print(nuovo_stato)
    input_stato_ord.bind('<<ComboboxSelected>>', stato_selezionato) """

    #Quantità prodotto
    label_qnt = Label(mod_ordine, text="Qnt.", bg="lightblue")
    label_qnt.grid(column=0, row=3, padx=20, pady=10, sticky=W)

    input_qnt = Entry(mod_ordine, width=20)
    input_qnt.insert(0, values[2])
    input_qnt.grid(column=1, row=3, sticky=W)

    #Prezzo prodotto
    label_prezzo = Label(mod_ordine, text="Prezzo", bg="lightblue")
    label_prezzo.grid(column=0, row=4, padx=20, pady=10, sticky=W)

    input_prezzo = Entry(mod_ordine, width=20)
    input_prezzo.insert(0, values[3])
    input_prezzo.grid(column=1, row=4, sticky=W)

    #Button Inserimento nuovo prodotto
    btn_invio = Button(mod_ordine, text="Invia", width=6, height=1, bg="#ffc048", command=modifica_ordine)
    btn_invio.grid(column=0, row=6, pady=5, sticky=E, columnspan=2)

    label_info = Label(mod_ordine, text="Per modificare più prodotti,\n ripetere più volte l'operazione", bg="lightblue")
    label_info.grid(column=0, row=7, padx=(30,0), pady=(30,0), columnspan=2)


    mod_ordine.mainloop()
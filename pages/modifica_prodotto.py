from tkinter import * 
from tkinter import messagebox
import mysql.connector  # per collegare il db
from mysql.connector import errorcode   # per prendere gli errori dal db


def show_modifica_prodotto(values):

    # funzione che pulisce i campi input, da chiamare dopo l'inserimento dei dati nel DB in modo da preparare il form per un nuovo inserimento
    def pulisci_campi():
        input_code.delete(0, 'end')
        input_nome.delete(0, 'end')
        input_qnt.delete(0, 'end')
        input_prezzo.delete(0, 'end')

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pharmazon"
        )
        cod_p = values[0]
        print("il cod prodotto",cod_p)
        cursore = db.cursor()
        cursore.execute("SELECT `id_p` FROM `prodotti` WHERE `codice_prodotto` = %s", (cod_p,))
        id_p = cursore.fetchone()
        id = id_p[0]
        print("l'id",id)

        cursore.close()
        db.close()  # chiudiamo la connessiane al db
    except mysql.connector.Error as err:
        print("Errore MySQL nel trovare l'ID del prodotto:", err)

        #funzione che prende i valori dai campi input e verifica che sia tutto compilato e salva nel db 
    def modifica_prodotto():
        val_code = input_code.get().replace(" ", "").upper() # prendiamo i valori dai campi input, rimuoviamo ogni spazio e lo memorizziamo tutto maiuscolo
        val_nome = input_nome.get().strip().capitalize() # rimuoviamo gli spazi dall'inizio e dalla fine della stringa e mettiamo la prima lettera maiuscola
        val_qnt = input_qnt.get().replace(" ", "")    #rimuoviamo qualsiasi spazio bianco presente all'interno della stringa inizio, nel mezzo, alla fine.
        val_prez = input_prezzo.get().replace(" ", "").replace(".", ",")  # rimuoviamo ogni spazio bianco e sostituiamo il . con la virgola in caso di erorre durante l'inserimento
        val_prezzo = val_prez[0] + " " + val_prez[1:]   #rimettiamo 1 singolo spazio tra il simbolo € ed il prezzo, in modo tale che nel db non ci possano essere errori
        try:
            if val_code == "" or val_nome == "" or val_qnt == "" or val_prezzo == "":    # verifichiamo che i campi siano tutti compilati
                print("campi lasciati vuoti")
                messagebox.showwarning(title="Attenzione!", message="Devi riempire tutti i campi per effettuare correttamente l'inserimento")  #messaggi pop-up

            elif len(val_code) != 5:
                print("codice prodotto errato")
                messagebox.showwarning(title="Attenzione!", message="Il codice prodotto non è valido, verificarne la lunghezza")
            
            else:
                # Chiedi conferma all'utente
                conferma = messagebox.askokcancel("Conferma Modifica", f"Confermi l'aggiornamento del prodotto {val_nome} con codice {val_code}?")
            
                if conferma:
                    # Collegamento al database
                    db = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="pharmazon"
                    )
                    # dizionario con i valori dei placeholder
                    update_values = val_code, val_nome, val_qnt, val_prezzo, id
                    # query SQL che modifica
                    update_query = "UPDATE `prodotti` SET `codice_prodotto` = %s, `nome_prodotto` = %s, `quantita` = %s, `prezzo` = %s WHERE `id_p` = %s"

                    cursore = db.cursor()
                    cursore.execute(update_query, update_values) 

                    db.commit()
                    cursore.close()
                    db.close()

                    messagebox.showinfo(title="Prodotto aggiornato!", message="Prodotto aggiornato con successo!")
                    print("Prodotto aggiornato con successo")
                    pulisci_campi()
                else:
                    print("Modifica annullata")

        except mysql.connector.Error as err:    # prendiamo gli erorri generati dal DB 

            if err.errno == errorcode.ER_DUP_ENTRY:
                # Se l'errore è dovuto a un duplicato di chiave unica (ER_DUP_ENTRY)
                print("Attenzione!")
                messagebox.showwarning(title="Attenzione!", message="Codice prodotto già memorizzato. Andare su Modifica per quel prodotto.")

            else:
                # Altro tipo di errore
                print("Errore MySQL:", err)
                messagebox.showerror(title="Errore!", message="Si è verificato un errore durante l'inserimento.")


    ##### GUI ######

    mod_prodotto = Tk()

    # Ottiene la larghezza e l'altezza dello schermo
    screen_width = mod_prodotto.winfo_screenwidth()
    screen_height = mod_prodotto.winfo_screenheight()

    # Calcola la posizione centrale della finestra
    x = (screen_width / 2) - (340 / 2)
    y = (screen_height / 2) - (400 / 2)

    # Disabilita il resize della finestra
    mod_prodotto.resizable(width=False, height=False)

    mod_prodotto.geometry("%dx%d+%d+%d" % (340, 400, x, y))
    mod_prodotto.wm_iconbitmap("./favicon.ico")
    mod_prodotto.title("Pharmazon")
    mod_prodotto.configure(bg="lightblue")

    #Register label
    label_title = Label(mod_prodotto, text="Modifica Prodotto", font=("helvetica", 16), bg="lightblue")
    label_title.grid(column=0, row=0, padx=(20,0), pady=30, sticky=W)  


    #Codice prodotto
    label_code = Label(mod_prodotto, text="Codice", bg="lightblue")
    label_code.grid(column=0, row=1, padx=20, pady=10, sticky=W)

    input_code = Entry(mod_prodotto, width=20)
    input_code.insert(0, values[0])
    input_code.grid(column=1, row=1, sticky=W)

    #Nome prodotto
    label_nome = Label(mod_prodotto, text="Prodotto", bg="lightblue")
    label_nome.grid(column=0, row=2, padx=20, pady=10, sticky=W)

    input_nome = Entry(mod_prodotto, width=20)
    input_nome.insert(0, values[1])
    input_nome.grid(column=1, row=2, sticky=W)

    #Quantità prodotto
    label_qnt = Label(mod_prodotto, text="Qnt.", bg="lightblue")
    label_qnt.grid(column=0, row=3, padx=20, pady=10, sticky=W)

    input_qnt = Entry(mod_prodotto, width=20)
    input_qnt.insert(0, values[2])
    input_qnt.grid(column=1, row=3, sticky=W)

    #Prezzo prodotto
    label_prezzo = Label(mod_prodotto, text="Prezzo", bg="lightblue")
    label_prezzo.grid(column=0, row=4, padx=20, pady=10, sticky=W)

    input_prezzo = Entry(mod_prodotto, width=20)
    input_prezzo.insert(0, values[3])
    input_prezzo.grid(column=1, row=4, sticky=W)

    #Button Inserimento nuovo prodotto
    btn_invio = Button(mod_prodotto, text="Invia", width=6, height=1, bg="#ffc048", command=modifica_prodotto)
    btn_invio.grid(column=0, row=6, pady=5, sticky=E, columnspan=2)

    label_info = Label(mod_prodotto, text="Per modificare più prodotti,\n ripetere più volte l'operazione", bg="lightblue")
    label_info.grid(column=0, row=7, padx=(30,0), pady=(30,0), columnspan=2)


    mod_prodotto.mainloop()
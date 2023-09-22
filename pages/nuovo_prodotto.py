from tkinter import * 
from tkinter import messagebox
import mysql.connector  # per collegare il db
from mysql.connector import errorcode   # per prendere gli errori dal db


def show_nuovo_prodotto():

    # funzione che pulisce i campi input, da chiamare dopo l'inserimento dei dati nel DB in modo da preparare il form per un nuovo inserimento
    def pulisci_campi():
        input_code.delete(0, 'end')
        input_nome.delete(0, 'end')
        input_qnt.delete(0, 'end')
        input_prezzo.delete(0, 'end')

        #funzione che prende i valori dai campi input e verifica che sia tutto compilato e salva nel db 
    def nuovo_prodotto():
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

            else:   # collegamento al DB, inserimento in tabella e chiusura del DB
                # Colleghiamo il DB
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",        # abbiamo la possibilità di creare degli user e di impostare ovviamente una password per il DB nascondendola magari con un file .env
                    password="",
                    database="pharmazon"    #nome del database
                )
                cursore = db.cursor()   # ci permette di effettuare le chiamate al db

                new_prod = "INSERT INTO `prodotti`(`codice_prodotto`, `nome_prodotto`, `quantita`, `prezzo`) VALUES (%s,%s,%s,%s)"   #inserimento valori nella tabella prodotti
                values = (val_code, val_nome, val_qnt, val_prezzo) 
                cursore.execute(new_prod,values)    # associamo la chiamata INSERT ai valori

                db.commit() #convalidiamo l'inserimento in tabella
                cursore.close() # chiudiamo il cursore
                db.close()  #chiudiamo la connessione con il db

                messagebox.showinfo(title="Prodotto inserito!", message="Prodotto inserito con successo!")
                print("prodotto inserito con successo")
                nv_prodotto.destroy()

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

    nv_prodotto = Tk()

    # Ottiene la larghezza e l'altezza dello schermo
    screen_width = nv_prodotto.winfo_screenwidth()
    screen_height = nv_prodotto.winfo_screenheight()

    # Calcola la posizione centrale della finestra
    x = (screen_width / 2) - (340 / 2)
    y = (screen_height / 2) - (400 / 2)

    # Disabilita il resize della finestra
    nv_prodotto.resizable(width=False, height=False)

    nv_prodotto.geometry("%dx%d+%d+%d" % (340, 400, x, y))
    nv_prodotto.wm_iconbitmap("./favicon.ico")
    nv_prodotto.title("Pharmazon")
    nv_prodotto.configure(bg="lightblue")

    #Register label
    label_title = Label(nv_prodotto, text="Nuovo Prodotto", font=("helvetica", 16), bg="lightblue")
    label_title.grid(column=0, row=0, padx=(20,0), pady=30, sticky=W)  


    #Codice prodotto
    label_code = Label(nv_prodotto, text="Codice", bg="lightblue")
    label_code.grid(column=0, row=1, padx=20, pady=10, sticky=W)

    input_code = Entry(nv_prodotto, width=20)
    input_code.grid(column=1, row=1, sticky=W)

    #Nome prodotto
    label_nome = Label(nv_prodotto, text="Prodotto", bg="lightblue")
    label_nome.grid(column=0, row=2, padx=20, pady=10, sticky=W)

    input_nome = Entry(nv_prodotto, width=20)
    input_nome.grid(column=1, row=2, sticky=W)

    #Quantità prodotto
    label_qnt = Label(nv_prodotto, text="Qnt.", bg="lightblue")
    label_qnt.grid(column=0, row=3, padx=20, pady=10, sticky=W)

    input_qnt = Entry(nv_prodotto, width=20)
    input_qnt.grid(column=1, row=3, sticky=W)

    #Prezzo prodotto
    label_prezzo = Label(nv_prodotto, text="Prezzo", bg="lightblue")
    label_prezzo.grid(column=0, row=4, padx=20, pady=10, sticky=W)

    input_prezzo = Entry(nv_prodotto, width=20)
    input_prezzo.insert(0, "€ -,--")
    input_prezzo.grid(column=1, row=4, sticky=W)

    #Button Inserimento nuovo prodotto
    btn_invio = Button(nv_prodotto, text="Invia", width=6, height=1, bg="blue",fg="white", command=nuovo_prodotto)
    btn_invio.grid(column=0, row=6, pady=5, sticky=E, columnspan=2)

    label_info = Label(nv_prodotto, text="Per inserire più prodotti,\n ripetere più volte l'operazione", bg="lightblue")
    label_info.grid(column=0, row=7, padx=(30,0), pady=(30,0), columnspan=2)


    nv_prodotto.mainloop()
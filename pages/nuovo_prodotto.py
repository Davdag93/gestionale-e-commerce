from tkinter import * 
from tkinter import messagebox


def show_nuovo_prodotto():


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
    input_prezzo.insert(0, "€ ")
    input_prezzo.grid(column=1, row=4, sticky=W)

    #Button Inserimento nuovo prodotto
    btn_invio = Button(nv_prodotto, text="Invia", width=6, height=1, bg="blue",fg="white", command="")
    btn_invio.grid(column=0, row=6, pady=5, sticky=E, columnspan=2)

    label_info = Label(nv_prodotto, text="Per inserire più prodotti,\n ripetere più volte l'operazione", bg="lightblue")
    label_info.grid(column=0, row=7, padx=(30,0), pady=(30,0), columnspan=2)


    nv_prodotto.mainloop()
from tkinter import *
from tkinter import messagebox
from vakcinisanje import *
from tkinter.ttk import Combobox
import datetime
from datetime import date


class PristupPotvrdama(Toplevel):

    def popuni_listu(self, potvrda):
        self.__lista_listbox.delete(0, END)
        for potvrde in potvrda:
            self.__lista_listbox.insert(END,
                                        "{} {} {}".format(potvrde.gradjani.ime, potvrde.gradjani.prezime, potvrde.datumtoString))
        self.__izmena_button['state'] = DISABLED
        self.__obrisi_button['state'] = DISABLED

    def popuni_labele(self, potvrda):
        self.__labela_sifra["text"] = potvrda.sifra
        self.__labela_datum_izdavanja["text"] = potvrda.datum
        self.__labela_datum_vakcinacije["text"] = potvrda.doza.datum
        self.__labela_gradjanin_ime["text"] = potvrda.gradjani.ime
        self.__labela_gradjanin_prezime["text"] = potvrda.gradjani.prezime
        self.__labela_radnik_ime["text"] = potvrda.zdrRadnik.ime
        self.__labela_radnik_prezime["text"] = potvrda.zdrRadnik.prezime

    def ocisti_labele(self):
        self.__labela_sifra["text"] = ""
        self.__labela_datum_izdavanja["text"] = ""
        self.__labela_datum_vakcinacije["text"] = ""
        self.__labela_gradjanin_ime["text"] = ""
        self.__labela_gradjanin_prezime["text"] = ""
        self.__labela_radnik_ime["text"] = ""
        self.__labela_radnik_prezime["text"] = ""

    def promena_selekcije_u_listbox(self, event=None):
        if not self.__lista_listbox.curselection():
            self.ocisti_labele()
            self.__izmena_button['state'] = DISABLED
            self.__obrisi_button['state'] = DISABLED
            return

        indeks = self.__lista_listbox.curselection()[0]
        naziv = self.__lista_listbox.get(indeks)
        potvrda = 0
        for i in self.__podaci.potvrde:
            if str(i.gradjani.ime + " " + i.gradjani.prezime + " " + i.datumtoString) == naziv:
                potvrda = i
        self.popuni_labele(potvrda)

        self.__izmena_button['state'] = NORMAL
        self.__obrisi_button['state'] = NORMAL

    def filtriranje_listbox(self, var, index, mode):
        self.ocisti_labele()
        self.__izmena_button['state'] = DISABLED
        self.__obrisi_button['state'] = DISABLED
        self.__lista_listbox.delete(0, END)
        text = self.__pretraga_entry.get()
        for potvtrda in self.__podaci.potvrde:
            if text.upper() in str(potvtrda.gradjani.ime + potvtrda.gradjani.prezime).upper():
                self.__lista_listbox.insert(END, "{} {}".format(potvtrda.gradjani.ime, potvtrda.gradjani.prezime))

    def brisanje(self, indeks):
        self.__podaci.doze.pop(indeks)
        self.update()
        Podaci.sacuvaj(self.__podaci)
        self.popuni_listu(self.__podaci.potvrde)
        self.__pretraga_entry["text"] = ""
        self.ocisti_labele()

    def izmena(self, indeks, jmbgIzmene):

        class Izmena(Toplevel):

            def izlaz(self):
                self.destroy()

    def dodavanje(self):

        class Dodavanje(Toplevel):

            def izlaz(self):
                self.destroy()

    def __init__(self, root, podaci):
        super().__init__(root)
        self.__podaci = podaci
        self.__otkazano = True

        self.title("Potvrde")
        self.minsize(400, 200)
        self.geometry('+350+100')
        # self.iconbitmap('c:/Users/Jovana/Desktop/ftn.ico')
        self.iconbitmap('c:/Users/korisnik/Desktop/InfoCentar za vakcinisanje/ftn.ico')
        # izbrisi ovu moju putanju i postavi ovu iznad svoju za sliku

        potvrde_frame = Frame(self, padx=5, pady=5)
        potvrde_frame.pack(expand=1)

        self.__dodaj_button = Button(potvrde_frame, width=10, command=self.dodavanje, text="Dodaj")
        self.__dodaj_button.grid(row=0, column=1, sticky=W)

        self.__izmena_button = Button(potvrde_frame, width=10, command=self.indeksiranje1, text="Izmeni")
        self.__izmena_button.grid(row=1, column=1, sticky=W)

        self.__obrisi_button = Button(potvrde_frame, width=10, command=self.indeksiranje2, text="Obrisi")
        self.__obrisi_button.grid(row=2, column=1, sticky=W)

        self.__pretraga = StringVar(root)
        self.__pretraga.trace_add("write", self.filtriranje_listbox)
        self.__pretraga_entry = Entry(potvrde_frame, width=20, textvariable=self.__pretraga)
        self.__pretraga_entry.grid(row=3, column=1, sticky=W)

        self.__lista_listbox = Listbox(potvrde_frame, activestyle="none", exportselection=False, width=35)
        self.__lista_listbox.grid(row=4, column=1, sticky=W)

        Label(potvrde_frame, text="Sifra:").grid(row=5, sticky=E)
        self.__labela_sifra = Label(potvrde_frame, text="")
        self.__labela_sifra.grid(row=5, column=1, sticky=W)
        Label(potvrde_frame, text="Datum izdavanja potvrde:").grid(row=6, sticky=E)
        self.__labela_datum_izdavanja = Label(potvrde_frame, text="")
        self.__labela_datum_izdavanja.grid(row=6, column=1, sticky=W)
        Label(potvrde_frame, text="Datum vakcinacije:").grid(row=7, sticky=E)
        self.__labela_datum_vakcinacije = Label(potvrde_frame, text="")
        self.__labela_datum_vakcinacije.grid(row=7, column=1, sticky=W)
        Label(potvrde_frame, text="Ime gradjanina:").grid(row=8, sticky=E)
        self.__labela_gradjanin_ime = Label(potvrde_frame, text="")
        self.__labela_gradjanin_ime.grid(row=8, column=1, sticky=W)
        Label(potvrde_frame, text="Prezime gradjanina:").grid(row=9, sticky=E)
        self.__labela_gradjanin_prezime = Label(potvrde_frame, text="")
        self.__labela_gradjanin_prezime.grid(row=9, column=1, sticky=W)
        Label(potvrde_frame, text="Ime zdravstvenog radnika:").grid(row=10, sticky=E)
        self.__labela_radnik_ime = Label(potvrde_frame, text="")
        self.__labela_radnik_ime.grid(row=10, column=1, sticky=W)
        Label(potvrde_frame, text="Prezime zdravstvenog radnika:").grid(row=11, sticky=E)
        self.__labela_radnik_prezime = Label(potvrde_frame, text="")
        self.__labela_radnik_prezime.grid(row=11, column=1, sticky=W)

        self.popuni_listu(self.__podaci.potvrde)
        self.__lista_listbox.bind("<<ListboxSelect>>", self.promena_selekcije_u_listbox)

        self.transient(root)
        # prozor se ne pojavljuje u taskbar-u, već samo njegov roditelj
        self.focus_force()
        # programski izazvani događaji
        self.grab_set()  # modalni

    def indeksiranje1(self):
        broj = self.__lista_listbox.curselection()[0]
        naziv = self.__lista_listbox.get(broj)
        indeks = 0
        for i in self.__podaci.potvrde:
            if naziv == str(i.gradjani.ime + " " + i.gradjani.prezime + " " + i.datumtoString):
                indeks = self.__podaci.potvrde.index(i)
        self.izmena(indeks, self.__podaci.potvrde[indeks].gradjani.jmbg)

    def indeksiranje2(self):
        broj = self.__lista_listbox.curselection()[0]
        naziv = self.__lista_listbox.get(broj)
        indeks = 0
        for i in self.__podaci.potvrde:
            if naziv == str(i.gradjani.ime + " " + i.gradjani.prezime + " " + i.datumtoString):
                indeks = self.__podaci.potvrde.index(i)
        odgovor = messagebox.askokcancel("Brisanje potvrde",
                                         "Brisanjem potvrde brisete i sve podatke vezane za nju. Da li ste sigurni da zelite da izbrisete potvrdu?",
                                         icon="warning")
        if odgovor:
            self.brisanje(indeks)

    @property
    def otkazano(self):
        return self.__otkazano
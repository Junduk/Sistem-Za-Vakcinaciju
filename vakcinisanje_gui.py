from gradjani import *
from zdravstveni_radnici import *
from vakcina import *
from doze import *
from potvrde import *
from sertifikati import *


class GlavniProzor(Tk):

    def komanda_izlaz(self):
        odgovor = messagebox.askokcancel("Izlaz iz programa", "Da li ste sigurni da zelite napustiti aplikaciju?",
                                         icon="warning")
        if odgovor:
            self.destroy()

    def komanda_gradjani(self):
        gradjani_prozor = PristupGradjanima(self, self.__podaci)
        self.wait_window(gradjani_prozor)
        if gradjani_prozor.otkazano:
            self.__listbox.delete(0, END)
            self.popuni_listbox(self.__podaci.gradjani)
            return

    def komanda_radnici(self):
        radnici_prozor = PristupZdravstvenimRadnicima(self, self.__podaci)
        self.wait_window(radnici_prozor)
        if radnici_prozor.otkazano:
            return

    def komanda_vakcina(self):
        vakcina_prozor = PristupVakcinama(self, self.__podaci)
        self.wait_window(vakcina_prozor)
        if vakcina_prozor.otkazano:
            return

    def komanda_doze(self):
        doze_prozor = PristupDozama(self, self.__podaci)
        self.wait_window(doze_prozor)
        if doze_prozor.otkazano:
            return

    def komanda_potvrde(self):
        potvrde_prozor = PristupPotvrdama(self, self.__podaci)
        self.wait_window(potvrde_prozor)
        if potvrde_prozor.otkazano:
            return

    def komanda_sertifikati(self):
        sertifikati_prozor = PristupSertifikatima(self, self.__podaci)
        self.wait_window(sertifikati_prozor)
        if sertifikati_prozor.otkazano:
            return

    def popuni_listbox(self, gradjani):
        self.__listbox.delete(0, END)
        for gradjanin in gradjani:  # za svaki proizvod iz liste
            self.__listbox.insert(END, "{} {}".format(gradjanin.ime, gradjanin.prezime))
        self.ocisti_labele()

    def popuni_labele(self, osoba):
        self.__labela_jmbg["text"] = osoba.jmbg
        self.__labela_ime["text"] = osoba.ime
        self.__labela_prezime["text"] = osoba.prezime
        self.__labela_datum_rodjenja["text"] = osoba.datumRodjenja
        self.__labela_pol["text"] = osoba.pol

    def ocisti_labele(self):
        self.__labela_jmbg["text"] = ""
        self.__labela_ime["text"] = ""
        self.__labela_prezime["text"] = ""
        self.__labela_datum_rodjenja["text"] = ""
        self.__labela_pol["text"] = ""

    def azuriranje(self, event=None):
        if not self.__listbox.curselection():
            self.ocisti_labele()
            return
        indeks = self.__listbox.curselection()[0]
        gradjani = self.__podaci.gradjani[indeks]
        self.popuni_labele(gradjani)

    def __init__(self, podaci):
        super().__init__()
        self.__podaci = podaci

        self.title("Projektni zadatak")
        self.minsize(700, 400)
        self.geometry('+350+100')
        # self.iconbitmap('c:/Users/Jovana/Desktop/ftn.ico')
        self.iconbitmap('c:/Users/korisnik/Desktop/InfoCentar za vakcinisanje/ftn.ico')
        # izbrisi ovu moju putanju i postavi ovu iznad svoju za sliku

        meni_bar = Menu(self)

        datoteka_menu = Menu(meni_bar, tearoff=0)
        datoteka_menu.add_command(label="Izlaz", command=self.komanda_izlaz)
        meni_bar.add_cascade(label="Datoteka", menu=datoteka_menu)

        self.__pristup_meni = Menu(meni_bar, tearoff=0)
        self.__pristup_meni.add_command(label="Gradjani", command=self.komanda_gradjani)
        self.__pristup_meni.add_command(label="Zdravstveni radnici", command=self.komanda_radnici)
        self.__pristup_meni.add_command(label="Vakcine", command=self.komanda_vakcina)
        self.__pristup_meni.add_command(label="Primljene doze", command=self.komanda_doze)
        self.__pristup_meni.add_command(label="Potvrde", command=self.komanda_potvrde)
        self.__pristup_meni.add_command(label="Sertifikati", command=self.komanda_sertifikati)
        meni_bar.add_cascade(label="Pristup", menu=self.__pristup_meni)

        self.config(menu=meni_bar)

        self.protocol("WM_DELETE_WINDOW", self.komanda_izlaz)

        # PRIKAZ LISTE OSOBA
        self.__listbox = Listbox(self, activestyle="none", exportselection=False)
        self.__listbox.pack(side=LEFT, fill=BOTH, expand=1)

        # FRAME
        frame = Frame(self, borderwidth=4, relief="ridge", padx=15, pady=15)
        frame.pack(side=RIGHT, fill=BOTH, expand=1)

        # LABELE UNUTAR FRAME-A
        self.__labela_jmbg = Label(frame, text="dd")
        self.__labela_ime = Label(frame, text="dd")
        self.__labela_prezime = Label(frame, text="dd")
        self.__labela_datum_rodjenja = Label(frame, text="dd")
        self.__labela_pol = Label(frame, text="dd")

        Label(frame, text="JMBG:").grid(row=0, sticky=E)
        Label(frame, text="Ime:").grid(row=1, sticky=E)
        Label(frame, text="Prezime:").grid(row=2, sticky=E)
        Label(frame, text="Datum rodjenja:").grid(row=3, sticky=E)
        Label(frame, text="Pol:").grid(row=4, sticky=E)

        self.__labela_jmbg.grid(row=0, column=1, sticky=W)
        self.__labela_ime.grid(row=1, column=1, sticky=W)
        self.__labela_prezime.grid(row=2, column=1, sticky=W)
        self.__labela_datum_rodjenja.grid(row=3, column=1, sticky=W)
        self.__labela_pol.grid(row=4, column=1, sticky=W)

        # LISTA SA LEVE STRANE
        self.popuni_listbox(self.__podaci.gradjani)
        self.focus_force()
        self.__listbox.bind("<<ListboxSelect>>", self.azuriranje)

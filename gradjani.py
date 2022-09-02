from tkinter import *
from tkinter import messagebox
from vakcinisanje import *
from tkinter.ttk import Combobox
import datetime


class PristupGradjanima(Toplevel):

    def sortiranjeGradjana(self):
        for x in self.__podaci.gradjani:
            indeks = self.__podaci.gradjani.index(x)
            if indeks != len(self.__podaci.gradjani) - 1:
                i = self.__podaci.gradjani[indeks + 1]
                if x.ime < i.ime:
                    k = x
                    self.__podaci.gradjani[indeks] = i
                    self.__podaci.gradjani[indeks + 1] = k
                elif x.ime == i.ime:
                    if x.prezime < i.prezime:
                        k = x
                        self.__podaci.gradjani[indeks] = i
                        self.__podaci.gradjani[indeks + 1] = k

    def popuni_listu(self, gradjani):
        self.__lista_listbox.delete(0, END)
        for gradjanin in gradjani:
            self.__lista_listbox.insert(END, "{} {}".format(gradjanin.ime, gradjanin.prezime))
        self.__izmena_button['state'] = DISABLED
        self.__obrisi_button['state'] = DISABLED

    def popuni_labele(self, gradjani):
        self.__labela_jmbg["text"] = gradjani.jmbg
        self.__labela_ime["text"] = gradjani.ime
        self.__labela_prezime["text"] = gradjani.prezime
        self.__labela_datum_rodjenja["text"] = gradjani.datumRodjenja
        self.__labela_pol["text"] = gradjani.pol
        self.__labela_broj_licne_karte["text"] = gradjani.brojLicneKarte

    def ocisti_labele(self):
        self.__labela_jmbg["text"] = ""
        self.__labela_ime["text"] = ""
        self.__labela_prezime["text"] = ""
        self.__labela_datum_rodjenja["text"] = ""
        self.__labela_pol["text"] = ""
        self.__labela_broj_licne_karte["text"] = ""

    def promena_selekcije_u_listbox(self, event=None):
        if not self.__lista_listbox.curselection():
            self.ocisti_labele()
            self.__izmena_button['state'] = DISABLED
            self.__obrisi_button['state'] = DISABLED
            return

        indeks = self.__lista_listbox.curselection()[0]
        naziv = self.__lista_listbox.get(indeks)
        gradjanin = 0
        for i in self.__podaci.gradjani:
            if str(i.ime + " " + i.prezime) == naziv:
                gradjanin = i
        self.popuni_labele(gradjanin)

        self.__izmena_button['state'] = NORMAL
        self.__obrisi_button['state'] = NORMAL

    def filtriranje_listbox(self, var, index, mode):
        self.ocisti_labele()
        self.__izmena_button['state'] = DISABLED
        self.__obrisi_button['state'] = DISABLED
        self.__lista_listbox.delete(0, END)
        text = self.__pretraga_entry.get()
        for gradjanin in self.__podaci.gradjani:
            if text.upper() in str(gradjanin.ime + gradjanin.prezime).upper():
                self.__lista_listbox.insert(END, "{} {}".format(gradjanin.ime, gradjanin.prezime))

    def brisanje(self, indeks):
        self.__podaci.gradjani.pop(indeks)
        self.update()
        Podaci.sacuvaj(self.__podaci)
        self.popuni_listu(self.__podaci.gradjani)
        self.__pretraga_entry["text"] = ""
        self.ocisti_labele()

    def izmena(self, indeks, jmbgIzmene):

        class Izmena(Toplevel):

            def izlaz(self):
                self.destroy()

            @property
            def otkazano(self):
                return self.__otkazano

            def izmeni(self):
                ime = self.ogranicenje_ime()
                if not ime:
                    return

                prezime = self.ogranicenje_prezime()
                if not prezime:
                    return

                datumRodjenja = self.ogranicenje_datum_rodjenja()
                if not datumRodjenja:
                    return

                pol = self.ogranicenje_pol()
                if not pol:
                    return

                self.__podaci.gradjani[indeks].ime = ime
                self.__podaci.gradjani[indeks].prezime = prezime
                self.__podaci.gradjani[indeks].datumRodjenja = datumRodjenja
                self.__podaci.gradjani[indeks].pol = pol

                self.update()
                Podaci.sacuvaj(self.__podaci)

                self.__otkazano = False
                self.destroy()

            def ogranicenje_ime(self):
                ime = self.__ime_entry.get()
                if len(ime) < 2:
                    messagebox.showerror("Greška", "Ime mora sadrzati bar 2 karaktera!")
                    return None
                return ime

            def ogranicenje_prezime(self):
                prezime = self.__prezime_entry.get()
                if len(prezime) < 2:
                    messagebox.showerror("Greška", "Prezime mora sadrzati bar 2 karaktera!")
                    return None
                return prezime

            def ogranicenje_datum_rodjenja(self):
                godina = int(self.__godina_spinbox.get())
                mesec = int(self.__mesec_spinbox.get())
                dan = int(self.__dan_spinbox.get())
                sat = int(self.__sat_spinbox.get())
                minut = int(self.__minut_spinbox.get())
                sekunda = int(self.__sekund_spinbox.get())
                if godina < 1900 or godina > 2022:
                    messagebox.showerror("Greška", "Ponovo unesite godinu!")
                    return None
                elif mesec < 1 or mesec > 12:
                    messagebox.showerror("Greška", "Ponovo unesite mesec!")
                    return None
                elif dan < 1 or dan > 31:
                    messagebox.showerror("Greška", "Ponovo unesite dan!")
                    return None
                elif mesec in [4, 6, 9, 11] and dan > 30:
                    messagebox.showerror("Greška", "Mesec ima manje dana!")
                    return None
                elif godina % 4 == 0 and mesec == 2 and dan > 29:
                    messagebox.showerror("Greška", "Mesec ima manje dana!")
                    return None
                elif godina % 4 != 0 and mesec == 2 and dan > 28:
                    messagebox.showerror("Greška", "Mesec ima manje dana!")
                    return None
                elif sat < 0 or sat > 24:
                    messagebox.showerror("Greška", "Ponovo unesite sat!")
                    return None
                elif minut < 0 or minut > 59:
                    messagebox.showerror("Greška", "Ponovo unesite minut!")
                    return None
                elif sekunda < 0 or sekunda > 59:
                    messagebox.showerror("Greška", "Ponovo unesite sekund!")
                    return None
                return str(datetime.datetime(godina, mesec, dan, sat, minut, sekunda))

            def ogranicenje_pol(self):
                pol = self.__pol_combobox.get()
                if pol == "":
                    messagebox.showerror("Greška", "Izaberite pol!")
                    return None
                return pol

            def __init__(self, root, podaci):
                super().__init__(root)
                self.__podaci = podaci
                self.__otkazano = True

                self.title("Izmena")
                self.minsize(400, 200)
                self.geometry('+350+100')
                # self.iconbitmap('c:/Users/Jovana/Desktop/ftn.ico')
                self.iconbitmap('c:/Users/korisnik/Desktop/InfoCentar za vakcinisanje/ftn.ico')
                # izbrisi ovu moju putanju i postavi ovu iznad svoju za sliku

                izmena_frame = Frame(self, padx=5, pady=5)
                izmena_frame.pack(expand=1)

                Label(izmena_frame, text="JMBG:").grid(row=0, sticky=E)
                self.__jmbg = StringVar(root)
                self.__jmbg_entry = Entry(izmena_frame, width=20, textvariable=self.__jmbg)
                self.__jmbg_entry.grid(row=0, column=1, sticky=W)
                self.__jmbg_entry.delete(0, END)
                self.__jmbg_entry.insert(0, self.__podaci.gradjani[indeks].jmbg)
                self.__jmbg_entry.config(state="disabled")

                Label(izmena_frame, text="Ime:").grid(row=1, sticky=E)
                self.__ime = StringVar(root)
                self.__ime_entry = Entry(izmena_frame, width=20, textvariable=self.__ime)
                self.__ime_entry.grid(row=1, column=1, sticky=W)
                self.__ime_entry.delete(0, END)
                self.__ime_entry.insert(0, self.__podaci.gradjani[indeks].ime)

                Label(izmena_frame, text="Prezime:").grid(row=2, sticky=E)
                self.__prezime = StringVar(root)
                self.__prezime_entry = Entry(izmena_frame, width=20, textvariable=self.__prezime)
                self.__prezime_entry.grid(row=2, column=1, sticky=W)
                self.__prezime_entry.delete(0, END)
                self.__prezime_entry.insert(0, self.__podaci.gradjani[indeks].prezime)

                Label(izmena_frame, text="Datum rodjenja:").grid(row=3, sticky=E)

                pomocni_frame = Frame(izmena_frame, padx=5, pady=5)
                pomocni_frame.grid(row=3, column=1, sticky=W)

                self.__vreme1 = IntVar(root)
                self.__godina_spinbox = Spinbox(pomocni_frame, width=5, from_=1900, increment=1, to=2022,
                                                textvariable=self.__vreme1)
                self.__godina_spinbox.grid(row=0, column=0, sticky=W)

                pomoc = str(datetime.datetime.strptime(self.__podaci.gradjani[indeks]
                                                       .datumRodjenja, "%Y-%m-%d %H:%M:%S") \
                            .strftime("%d/%m/%Y/%H/%M/%S")).split("/")
                self.__godina_spinbox.delete(0, END)
                self.__godina_spinbox.insert(0, pomoc[2])
                self.__vreme2 = IntVar(root)
                self.__mesec_spinbox = Spinbox(pomocni_frame, width=5, from_=1, increment=1, to=12,
                                               textvariable=self.__vreme2)
                self.__mesec_spinbox.grid(row=0, column=1, sticky=W)
                self.__mesec_spinbox.delete(0, END)
                self.__mesec_spinbox.insert(0, pomoc[1])
                self.__vreme3 = IntVar(root)
                self.__dan_spinbox = Spinbox(pomocni_frame, width=5, from_=1, increment=1, to=31,
                                             textvariable=self.__vreme3)
                self.__dan_spinbox.grid(row=0, column=2, sticky=W)
                self.__dan_spinbox.delete(0, END)
                self.__dan_spinbox.insert(0, pomoc[0])
                self.__vreme4 = IntVar(root)
                self.__sat_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=24,
                                             textvariable=self.__vreme4)
                self.__sat_spinbox.grid(row=0, column=3, sticky=W)
                self.__sat_spinbox.delete(0, END)
                self.__sat_spinbox.insert(0, pomoc[3])
                self.__vreme5 = IntVar(root)
                self.__minut_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=60,
                                               textvariable=self.__vreme5)
                self.__minut_spinbox.grid(row=0, column=4, sticky=W)
                self.__minut_spinbox.delete(0, END)
                self.__minut_spinbox.insert(0, pomoc[4])
                self.__vreme6 = IntVar(root)
                self.__sekund_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=60,
                                                textvariable=self.__vreme6)
                self.__sekund_spinbox.grid(row=0, column=5, sticky=W)
                self.__sekund_spinbox.delete(0, END)
                self.__sekund_spinbox.insert(0, pomoc[5])

                Label(izmena_frame, text="Pol:").grid(row=4, sticky=E)
                self.__pol = StringVar(root)
                self.__pol_combobox = Combobox(izmena_frame, textvariable=self.__pol)
                self.__pol_combobox.grid(row=4, column=1, sticky=W)
                self.__pol_combobox['values'] = ('Zensko', 'Musko')
                self.__pol_combobox.insert(0, self.__podaci.gradjani[indeks].pol)

                Label(izmena_frame, text="Broj licne karte:").grid(row=5, sticky=E)
                self.__broj_licne_karte = StringVar(root)
                self.__broj_licne_karte_entry = Entry(izmena_frame, width=20, textvariable=self.__broj_licne_karte)
                self.__broj_licne_karte_entry.grid(row=5, column=1, sticky=W)
                self.__broj_licne_karte_entry.insert(0, self.__podaci.gradjani[indeks].brojLicneKarte)
                self.__broj_licne_karte_entry.config(state="disabled")

                self.__izmeni_button = Button(izmena_frame, width=10, command=self.izmeni, text="Izmeni")
                self.__izmeni_button.grid(row=6, column=1, sticky=W)

                self.__izlaz_button = Button(izmena_frame, width=10, command=self.izlaz, text="Izlaz")
                self.__izlaz_button.grid(row=7, column=1, sticky=W)

        izmena_prozor = Izmena(self, self.__podaci)
        self.wait_window(izmena_prozor)
        if izmena_prozor.otkazano:
            return
        self.sortiranjeGradjana()
        self.popuni_listu(self.__podaci.gradjani)
        self.__pretraga_entry["text"] = ""
        self.__izmena_button['state'] = NORMAL
        self.__obrisi_button['state'] = NORMAL
        for x in self.__podaci.gradjani:
            if x.jmbg == jmbgIzmene:
                i = self.__podaci.gradjani.index(x)
                self.__lista_listbox.select_set(i)
                self.popuni_labele(self.__podaci.gradjani[i])

    def dodavanje(self):

        class Dodavanje(Toplevel):

            def izlaz(self):
                self.destroy()

            @property
            def otkazano(self):
                return self.__otkazano

            def dodaj(self):
                jmbg = self.ogranicenje_jmbg()
                if not jmbg:
                    return

                ime = self.ogranicenje_ime()
                if not ime:
                    return

                prezime = self.ogranicenje_prezime()
                if not prezime:
                    return

                datumRodjenja = self.ogranicenje_datum_rodjenja()
                if not datumRodjenja:
                    return

                pol = self.ogranicenje_pol()
                if not pol:
                    return

                brojLicneKarte = self.ogranicenje_licne_karte()
                if not brojLicneKarte:
                    return

                osoba = Osoba(jmbg, ime, prezime, datumRodjenja, pol)
                gradjanin = Gradjanin(osoba, brojLicneKarte)
                self.__podaci.gradjani.append(gradjanin)

                self.update()
                Podaci.sacuvaj(self.__podaci)

                self.__otkazano = False
                self.destroy()

            def ogranicenje_jmbg(self):
                jmbg = self.__jmbg_entry.get()
                if len(jmbg) != 13:
                    messagebox.showerror("Greška", "JMBG mora sadrzati 13 cifara!")
                    return None
                return jmbg

            def ogranicenje_ime(self):
                ime = self.__ime_entry.get()
                if len(ime) < 2:
                    messagebox.showerror("Greška", "Ime mora sadrzati bar 2 karaktera!")
                    return None
                return ime

            def ogranicenje_prezime(self):
                prezime = self.__prezime_entry.get()
                if len(prezime) < 2:
                    messagebox.showerror("Greška", "Prezime mora sadrzati bar 2 karaktera!")
                    return None
                return prezime

            def ogranicenje_datum_rodjenja(self):
                godina = int(self.__godina_spinbox.get())
                mesec = int(self.__mesec_spinbox.get())
                dan = int(self.__dan_spinbox.get())
                sat = int(self.__sat_spinbox.get())
                minut = int(self.__minut_spinbox.get())
                sekunda = int(self.__sekund_spinbox.get())
                if godina < 1900 or godina > 2022:
                    messagebox.showerror("Greška", "Ponovo unesite godinu!")
                    return None
                elif mesec < 1 or mesec > 12:
                    messagebox.showerror("Greška", "Ponovo unesite mesec!")
                    return None
                elif dan < 1 or dan > 31:
                    messagebox.showerror("Greška", "Ponovo unesite dan!")
                    return None
                elif mesec in [4, 6, 9, 11] and dan > 30:
                    messagebox.showerror("Greška", "Mesec ima manje dana!")
                    return None
                elif godina % 4 == 0 and mesec == 2 and dan > 29:
                    messagebox.showerror("Greška", "Mesec ima manje dana!")
                    return None
                elif godina % 4 != 0 and mesec == 2 and dan > 28:
                    messagebox.showerror("Greška", "Mesec ima manje dana!")
                    return None
                elif sat < 0 or sat > 24:
                    messagebox.showerror("Greška", "Ponovo unesite sat!")
                    return None
                elif minut < 0 or minut > 59:
                    messagebox.showerror("Greška", "Ponovo unesite minut!")
                    return None
                elif sekunda < 0 or sekunda > 59:
                    messagebox.showerror("Greška", "Ponovo unesite sekund!")
                    return None
                return str(datetime.datetime(godina, mesec, dan, sat, minut, sekunda))

            def ogranicenje_pol(self):
                pol = self.__pol_combobox.get()
                if pol == "":
                    messagebox.showerror("Greška", "Izaberite pol!")
                    return None
                return pol

            def ogranicenje_licne_karte(self):
                brojLicneKarte = self.__broj_licne_karte_entry.get()
                if len(brojLicneKarte) != 10:
                    messagebox.showerror("Greška", "Broj licne karte mora sadrzati 10 cifara!")
                    return None
                return brojLicneKarte

            def __init__(self, root, podaci):
                super().__init__(root)
                self.__podaci = podaci
                self.__otkazano = True

                self.title("Dodavanje")
                self.minsize(400, 200)
                self.geometry('+350+100')
                # self.iconbitmap('c:/Users/Jovana/Desktop/ftn.ico')
                self.iconbitmap('c:/Users/korisnik/Desktop/InfoCentar za vakcinisanje/ftn.ico')
                # izbrisi ovu moju putanju i postavi ovu iznad svoju za sliku

                dodavanje_frame = Frame(self, padx=5, pady=5)
                dodavanje_frame.pack(expand=1)

                Label(dodavanje_frame, text="JMBG:").grid(row=0, sticky=E)
                self.__jmbg = StringVar(root)
                self.__jmbg_entry = Entry(dodavanje_frame, width=20, textvariable=self.__jmbg)
                self.__jmbg_entry.grid(row=0, column=1, sticky=W)

                Label(dodavanje_frame, text="Ime:").grid(row=1, sticky=E)
                self.__ime = StringVar(root)
                self.__ime_entry = Entry(dodavanje_frame, width=20, textvariable=self.__ime)
                self.__ime_entry.grid(row=1, column=1, sticky=W)

                Label(dodavanje_frame, text="Prezime:").grid(row=2, sticky=E)
                self.__prezime = StringVar(root)
                self.__prezime_entry = Entry(dodavanje_frame, width=20, textvariable=self.__prezime)
                self.__prezime_entry.grid(row=2, column=1, sticky=W)

                Label(dodavanje_frame, text="Datum rodjenja:").grid(row=3, sticky=E)

                pomocni_frame = Frame(dodavanje_frame, padx=5, pady=5)
                pomocni_frame.grid(row=3, column=1, sticky=W)

                self.__vreme1 = IntVar(root)
                self.__godina_spinbox = Spinbox(pomocni_frame, width=5, from_=1900, increment=1, to=2022,
                                                textvariable=self.__vreme1)
                self.__godina_spinbox.grid(row=0, column=0, sticky=W)
                self.__vreme2 = IntVar(root)
                self.__mesec_spinbox = Spinbox(pomocni_frame, width=5, from_=1, increment=1, to=12,
                                               textvariable=self.__vreme2)
                self.__mesec_spinbox.grid(row=0, column=1, sticky=W)
                self.__vreme3 = IntVar(root)
                self.__dan_spinbox = Spinbox(pomocni_frame, width=5, from_=1, increment=1, to=31,
                                             textvariable=self.__vreme3)
                self.__dan_spinbox.grid(row=0, column=2, sticky=W)
                self.__vreme4 = IntVar(root)
                self.__sat_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=24,
                                             textvariable=self.__vreme4)
                self.__sat_spinbox.grid(row=0, column=3, sticky=W)
                self.__vreme5 = IntVar(root)
                self.__minut_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=60,
                                               textvariable=self.__vreme5)
                self.__minut_spinbox.grid(row=0, column=4, sticky=W)
                self.__vreme6 = IntVar(root)
                self.__sekund_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=60,
                                                textvariable=self.__vreme6)
                self.__sekund_spinbox.grid(row=0, column=5, sticky=W)

                Label(dodavanje_frame, text="Pol:").grid(row=4, sticky=E)
                self.__pol = StringVar(root)
                self.__pol_combobox = Combobox(dodavanje_frame, textvariable=self.__pol)
                self.__pol_combobox.grid(row=4, column=1, sticky=W)
                self.__pol_combobox['values'] = ('Zensko', 'Musko')

                Label(dodavanje_frame, text="Broj licne karte:").grid(row=5, sticky=E)
                self.__broj_licne_karte = StringVar(root)
                self.__broj_licne_karte_entry = Entry(dodavanje_frame, width=20, textvariable=self.__broj_licne_karte)
                self.__broj_licne_karte_entry.grid(row=5, column=1, sticky=W)

                self.__dodaj_button = Button(dodavanje_frame, width=10, command=self.dodaj, text="Dodaj")
                self.__dodaj_button.grid(row=6, column=1, sticky=W)

                self.__izlaz_button = Button(dodavanje_frame, width=10, command=self.izlaz, text="Izlaz")
                self.__izlaz_button.grid(row=7, column=1, sticky=W)

        dodavanje_prozor = Dodavanje(self, self.__podaci)
        self.wait_window(dodavanje_prozor)
        if dodavanje_prozor.otkazano:
            return

        self.popuni_listu(self.__podaci.gradjani)
        self.__izmena_button['state'] = NORMAL
        self.__obrisi_button['state'] = NORMAL
        self.__pretraga_entry["text"] = ""

    def __init__(self, root, podaci):
        super().__init__(root)
        self.__podaci = podaci
        self.__otkazano = True

        self.title("Gradjani")
        self.minsize(400, 200)
        self.geometry('+350+100')
        # self.iconbitmap('c:/Users/Jovana/Desktop/ftn.ico')
        self.iconbitmap('c:/Users/korisnik/Desktop/InfoCentar za vakcinisanje/ftn.ico')
        # izbrisi ovu moju putanju i postavi ovu iznad svoju za sliku

        gradjanin_frame = Frame(self, padx=5, pady=5)
        gradjanin_frame.pack(expand=1)

        self.__dodaj_button = Button(gradjanin_frame, width=10, command=self.dodavanje, text="Dodaj")
        self.__dodaj_button.grid(row=0, column=1, sticky=W)

        self.__izmena_button = Button(gradjanin_frame, width=10, command=self.indeksiranje1, text="Izmeni")
        self.__izmena_button.grid(row=1, column=1, sticky=W)

        self.__obrisi_button = Button(gradjanin_frame, width=10, command=self.indeksiranje2, text="Obrisi")
        self.__obrisi_button.grid(row=2, column=1, sticky=W)

        self.__pretraga = StringVar(root)
        self.__pretraga.trace_add("write", self.filtriranje_listbox)
        self.__pretraga_entry = Entry(gradjanin_frame, width=20, textvariable=self.__pretraga)
        self.__pretraga_entry.grid(row=3, column=1, sticky=W)

        self.__lista_listbox = Listbox(gradjanin_frame, activestyle="none", exportselection=False)
        self.__lista_listbox.grid(row=4, column=1, sticky=W)

        Label(gradjanin_frame, text="JMBG:").grid(row=5, sticky=E)
        self.__labela_jmbg = Label(gradjanin_frame, text="")
        self.__labela_jmbg.grid(row=5, column=1, sticky=W)
        Label(gradjanin_frame, text="Ime:").grid(row=6, sticky=E)
        self.__labela_ime = Label(gradjanin_frame, text="")
        self.__labela_ime.grid(row=6, column=1, sticky=W)
        Label(gradjanin_frame, text="Prezime:").grid(row=7, sticky=E)
        self.__labela_prezime = Label(gradjanin_frame, text="")
        self.__labela_prezime.grid(row=7, column=1, sticky=W)
        Label(gradjanin_frame, text="Datum rodjenja:").grid(row=8, sticky=E)
        self.__labela_datum_rodjenja = Label(gradjanin_frame, text="")
        self.__labela_datum_rodjenja.grid(row=8, column=1, sticky=W)
        Label(gradjanin_frame, text="Pol:").grid(row=9, sticky=E)
        self.__labela_pol = Label(gradjanin_frame, text="")
        self.__labela_pol.grid(row=9, column=1, sticky=W)
        Label(gradjanin_frame, text="Broj licne karte:").grid(row=10, sticky=E)
        self.__labela_broj_licne_karte = Label(gradjanin_frame, text="")
        self.__labela_broj_licne_karte.grid(row=10, column=1, sticky=W)

        self.__lista_doza_button = Button(gradjanin_frame, width=10, command=self.indeksiranje3, text="Lista doza")
        self.__lista_doza_button.grid(row=11, column=1, sticky=W)

        self.__lista_potvrda_button = Button(gradjanin_frame, width=10, command=self.indeksiranje4,
                                             text="Lista potvrda")
        self.__lista_potvrda_button.grid(row=12, column=1, sticky=W)

        self.__lista_sertifikata_button = Button(gradjanin_frame, width=10, command=self.indeksiranje5,
                                                 text="Lista sertifikata")
        self.__lista_sertifikata_button.grid(row=13, column=1, sticky=W)

        self.popuni_listu(self.__podaci.gradjani)
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
        for i in self.__podaci.gradjani:
            if naziv == str(i.ime + " " + i.prezime):
                indeks = self.__podaci.gradjani.index(i)
        self.izmena(indeks, self.__podaci.gradjani[indeks].jmbg)

    def indeksiranje2(self):
        broj = self.__lista_listbox.curselection()[0]
        naziv = self.__lista_listbox.get(broj)
        indeks = 0
        for i in self.__podaci.gradjani:
            if naziv == str(i.ime + " " + i.prezime):
                indeks = self.__podaci.gradjani.index(i)
        odgovor = messagebox.askokcancel("Brisanje gradjanina",
                                         "Brisanjem gradjanina brisete i sve podatke vezane za njega. Da li ste sigurni da zelite da izbrisete gradjanina?",
                                         icon="warning")
        if odgovor:
            self.brisanje(indeks)

    def indeksiranje3(self):
        try:
            broj = self.__lista_listbox.curselection()[0]
            naziv = self.__lista_listbox.get(broj)
            indeks = 0
            for i in self.__podaci.gradjani:
                if naziv == str(i.ime + " " + i.prezime):
                    indeks = self.__podaci.gradjani.index(i)
            if len(self.__podaci.gradjani[indeks].listaDoza) == 0:
                messagebox.showerror("Greška", "Osoba ne poseduje informacije o primljenoj dozi!")
            else:
                self.lista_doza(self.__podaci.gradjani[indeks].listaDoza)
        except IndexError:
            messagebox.showerror("Greška", "Izaberite osobu iz liste!")

    def indeksiranje4(self):
        try:
            broj = self.__lista_listbox.curselection()[0]
            naziv = self.__lista_listbox.get(broj)
            indeks = 0
            for i in self.__podaci.gradjani:
                if naziv == str(i.ime + " " + i.prezime):
                    indeks = self.__podaci.gradjani.index(i)
            if len(self.__podaci.gradjani[indeks].listaPotvrda) == 0:
                messagebox.showerror("Greška", "Osoba ne poseduje informacije o potvrdi!")
            else:
                self.lista_potvrda(self.__podaci.gradjani[indeks].listaPotvrda)
        except IndexError:
            messagebox.showerror("Greška", "Izaberite osobu iz liste!")

    def indeksiranje5(self):
        try:
            broj = self.__lista_listbox.curselection()[0]
            naziv = self.__lista_listbox.get(broj)
            indeks = 0
            for i in self.__podaci.gradjani:
                if naziv == str(i.ime + " " + i.prezime):
                    indeks = self.__podaci.gradjani.index(i)
            if len(self.__podaci.gradjani[indeks].listaSertifikata) == 0:
                messagebox.showerror("Greška", "Osoba ne poseduje informacije o sertifikatu!")
            else:
                self.lista_sertifikata(self.__podaci.gradjani[indeks].listaSertifikata)
        except IndexError:
            messagebox.showerror("Greška", "Izaberite osobu iz liste!")

    def lista_doza(self, listaDoza):

        class Lista_doza(Toplevel):

            def izlaz(self):
                self.destroy()

            @property
            def otkazano(self):
                return self.__otkazano

            def __init__(self, root, podaci):
                super().__init__(root)
                self.__podaci = podaci
                self.__otkazano = True

                self.title("Lista doza")
                self.minsize(400, 200)
                self.geometry('+350+100')
                # self.iconbitmap('c:/Users/Jovana/Desktop/ftn.ico')
                self.iconbitmap('c:/Users/korisnik/Desktop/InfoCentar za vakcinisanje/ftn.ico')
                # izbrisi ovu moju putanju i postavi ovu iznad svoju za sliku

                lista_doza_frame = Frame(self, padx=5, pady=5)
                lista_doza_frame.pack(expand=1)

                Label(lista_doza_frame, text="Datum vakcinacije:").grid(row=0, sticky=E)
                self.__labela_datum_vakcinacije = Label(lista_doza_frame, text="")
                self.__labela_datum_vakcinacije.grid(row=0, column=1, sticky=W)
                Label(lista_doza_frame, text="Naziv vakcine:").grid(row=1, sticky=E)
                self.__labela_naziv_vakcine = Label(lista_doza_frame, text="")
                self.__labela_naziv_vakcine.grid(row=1, column=1, sticky=W)
                Label(lista_doza_frame, text="Serijski broj:").grid(row=2, sticky=E)
                self.__labela_serijski_broj = Label(lista_doza_frame, text="")
                self.__labela_serijski_broj.grid(row=2, column=1, sticky=W)
                Label(lista_doza_frame, text="Ime zdravstvenog radnika:").grid(row=3, sticky=E)
                self.__labela_ime_zdr_radnika = Label(lista_doza_frame, text="")
                self.__labela_ime_zdr_radnika.grid(row=3, column=1, sticky=W)
                Label(lista_doza_frame, text="Prezime zdravstvenog radnika:").grid(row=4, sticky=E)
                self.__labela_prezime_zdr_radnika = Label(lista_doza_frame, text="")
                self.__labela_prezime_zdr_radnika.grid(row=4, column=1, sticky=W)
                Label(lista_doza_frame, text="Zemlja:").grid(row=5, sticky=E)
                self.__labela_zemlja = Label(lista_doza_frame, text="")
                self.__labela_zemlja.grid(row=5, column=1, sticky=W)

                self.__izlaz_button = Button(lista_doza_frame, width=10, command=self.izlaz, text="Izlaz")
                self.__izlaz_button.grid(row=6, column=1, sticky=W)

                for x in listaDoza:
                    self.__labela_datum_vakcinacije["text"] = self.__labela_datum_vakcinacije[
                                                                  "text"] + x.datumtoString + ";\n"
                    self.__labela_naziv_vakcine["text"] = self.__labela_naziv_vakcine["text"] + x.vakcina.naziv + ";\n"
                    self.__labela_serijski_broj["text"] = self.__labela_serijski_broj["text"] + str(
                        x.vakcina.serijskiBroj) + ";\n"
                    self.__labela_ime_zdr_radnika["text"] = self.__labela_ime_zdr_radnika[
                                                                "text"] + x.zdrRadnik.ime + ";\n"
                    self.__labela_prezime_zdr_radnika["text"] = self.__labela_prezime_zdr_radnika[
                                                                    "text"] + x.zdrRadnik.prezime + ";\n"
                    self.__labela_zemlja["text"] = self.__labela_zemlja["text"] + x.zemlja + ";\n"

        lista_doza_prozor = Lista_doza(self, self.__podaci)
        self.wait_window(lista_doza_prozor)
        if lista_doza_prozor.otkazano:
            return

    def lista_potvrda(self, listaPotvrda):

        class Lista_potvrda(Toplevel):

            def izlaz(self):
                self.destroy()

            @property
            def otkazano(self):
                return self.__otkazano

            def __init__(self, root, podaci):
                super().__init__(root)
                self.__podaci = podaci
                self.__otkazano = True

                self.title("Lista potvrda")
                self.minsize(400, 200)
                self.geometry('+350+100')
                # self.iconbitmap('c:/Users/Jovana/Desktop/ftn.ico')
                self.iconbitmap('c:/Users/korisnik/Desktop/InfoCentar za vakcinisanje/ftn.ico')
                # izbrisi ovu moju putanju i postavi ovu iznad svoju za sliku

                lista_potvrda_frame = Frame(self, padx=5, pady=5)
                lista_potvrda_frame.pack(expand=1)

                Label(lista_potvrda_frame, text="Sifra potvrde:").grid(row=0, sticky=E)
                self.__labela_sifra = Label(lista_potvrda_frame, text="")
                self.__labela_sifra.grid(row=0, column=1, sticky=W)
                Label(lista_potvrda_frame, text="Datum izdavanja:").grid(row=1, sticky=E)
                self.__labela_datum = Label(lista_potvrda_frame, text="")
                self.__labela_datum.grid(row=1, column=1, sticky=W)
                Label(lista_potvrda_frame, text="Ime gradjanina:").grid(row=2, sticky=E)
                self.__labela_ime_gradjanina = Label(lista_potvrda_frame, text="")
                self.__labela_ime_gradjanina.grid(row=2, column=1, sticky=W)
                Label(lista_potvrda_frame, text="Prezime gradjanina:").grid(row=3, sticky=E)
                self.__labela_prezime_gradjanina = Label(lista_potvrda_frame, text="")
                self.__labela_prezime_gradjanina.grid(row=3, column=1, sticky=W)
                Label(lista_potvrda_frame, text="Zdravstvena ustanova:").grid(row=4, sticky=E)
                self.__labela_naziv_zdr_ustanove = Label(lista_potvrda_frame, text="")
                self.__labela_naziv_zdr_ustanove.grid(row=4, column=1, sticky=W)
                Label(lista_potvrda_frame, text="Ime zdravstvenog radnika:").grid(row=5, sticky=E)
                self.__labela_ime_zdr_radnika = Label(lista_potvrda_frame, text="")
                self.__labela_ime_zdr_radnika.grid(row=5, column=1, sticky=W)
                Label(lista_potvrda_frame, text="Prezime zdravstvenog radnika:").grid(row=6, sticky=E)
                self.__labela_prezime_zdr_radnika = Label(lista_potvrda_frame, text="")
                self.__labela_prezime_zdr_radnika.grid(row=6, column=1, sticky=W)

                self.__izlaz_button = Button(lista_potvrda_frame, width=10, command=self.izlaz, text="Izlaz")
                self.__izlaz_button.grid(row=7, column=1, sticky=W)

                for x in listaPotvrda:
                    self.__labela_sifra["text"] = self.__labela_sifra["text"] + str(x.sifra) + ";\n"
                    self.__labela_datum["text"] = self.__labela_datum["text"] + x.datumtoString + ";\n"
                    self.__labela_ime_gradjanina["text"] = self.__labela_ime_gradjanina[
                                                               "text"] + x.gradjani.ime + ";\n"
                    self.__labela_prezime_gradjanina["text"] = self.__labela_prezime_gradjanina[
                                                                   "text"] + x.gradjani.prezime + ";\n"
                    self.__labela_naziv_zdr_ustanove["text"] = self.__labela_naziv_zdr_ustanove[
                                                                   "text"] + x.zdrRadnik.naziv + ";\n"
                    self.__labela_ime_zdr_radnika["text"] = self.__labela_ime_zdr_radnika[
                                                                "text"] + x.zdrRadnik.ime + ";\n"
                    self.__labela_prezime_zdr_radnika["text"] = self.__labela_prezime_zdr_radnika[
                                                                    "text"] + x.zdrRadnik.prezime + ";\n"

        lista_potvrda_prozor = Lista_potvrda(self, self.__podaci)
        self.wait_window(lista_potvrda_prozor)
        if lista_potvrda_prozor.otkazano:
            return

    def lista_sertifikata(self, listaSertifikata):

        class Lista_sertifikata(Toplevel):

            def izlaz(self):
                self.destroy()

            @property
            def otkazano(self):
                return self.__otkazano

            def __init__(self, root, podaci):
                super().__init__(root)
                self.__podaci = podaci
                self.__otkazano = True

                self.title("Lista sertifikata")
                self.minsize(400, 200)
                self.geometry('+350+100')
                # self.iconbitmap('c:/Users/Jovana/Desktop/ftn.ico')
                self.iconbitmap('c:/Users/korisnik/Desktop/InfoCentar za vakcinisanje/ftn.ico')
                # izbrisi ovu moju putanju i postavi ovu iznad svoju za sliku

                lista_sertifikata_frame = Frame(self, padx=5, pady=5)
                lista_sertifikata_frame.pack(expand=1)

                Label(lista_sertifikata_frame, text="Sifra sertifikata:").grid(row=0, sticky=E)
                self.__labela_sifra = Label(lista_sertifikata_frame, text="")
                self.__labela_sifra.grid(row=0, column=1, sticky=W)
                Label(lista_sertifikata_frame, text="Datum izdavanja:").grid(row=1, sticky=E)
                self.__labela_datum = Label(lista_sertifikata_frame, text="")
                self.__labela_datum.grid(row=1, column=1, sticky=W)
                Label(lista_sertifikata_frame, text="Ime gradjanina:").grid(row=2, sticky=E)
                self.__labela_gradjanin_ime = Label(lista_sertifikata_frame, text="")
                self.__labela_gradjanin_ime.grid(row=2, column=1, sticky=W)
                Label(lista_sertifikata_frame, text="Prezime gradjanina:").grid(row=3, sticky=E)
                self.__labela_gradjanin_prezime = Label(lista_sertifikata_frame, text="")
                self.__labela_gradjanin_prezime.grid(row=3, column=1, sticky=W)

                self.__izlaz_button = Button(lista_sertifikata_frame, width=10, command=self.izlaz, text="Izlaz")
                self.__izlaz_button.grid(row=4, column=1, sticky=W)

                for x in listaSertifikata:
                    self.__labela_sifra["text"] = self.__labela_sifra["text"] + str(x.sifra) + ";\n"
                    self.__labela_datum["text"] = self.__labela_datum["text"] + x.datumtoString + ";\n"
                    self.__labela_gradjanin_ime["text"] = self.__labela_gradjanin_ime["text"] + x.gradjani.ime + ";\n"
                    self.__labela_gradjanin_prezime["text"] = self.__labela_gradjanin_prezime[
                                                                  "text"] + x.gradjani.prezime + ";\n"

        lista_sertifikata_prozor = Lista_sertifikata(self, self.__podaci)
        self.wait_window(lista_sertifikata_prozor)
        if lista_sertifikata_prozor.otkazano:
            return

    @property
    def otkazano(self):
        return self.__otkazano

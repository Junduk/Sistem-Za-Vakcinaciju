from tkinter import *
from tkinter import messagebox
from vakcinisanje import *
from tkinter.ttk import Combobox


class PristupZdravstvenimRadnicima(Toplevel):

    def popuni_listu(self, radnici):
        self.__lista_listbox.delete(0, END)
        for radnik in radnici:
            self.__lista_listbox.insert(END, "{} {}".format(radnik.ime, radnik.prezime))
        self.__izmena_button['state'] = DISABLED
        self.__obrisi_button['state'] = DISABLED

    def popuni_labele(self, radnici):
        self.__labela_jmbg["text"] = radnici.jmbg
        self.__labela_ime["text"] = radnici.ime
        self.__labela_prezime["text"] = radnici.prezime
        self.__labela_datum_rodjenja["text"] = radnici.datumRodjenjatoString
        self.__labela_pol["text"] = radnici.pol
        self.__labela_naziv_radnog_mesta["text"] = radnici.naziv

    def ocisti_labele(self):
        self.__labela_jmbg["text"] = ""
        self.__labela_ime["text"] = ""
        self.__labela_prezime["text"] = ""
        self.__labela_datum_rodjenja["text"] = ""
        self.__labela_pol["text"] = ""
        self.__labela_naziv_radnog_mesta["text"] = ""

    def promena_selekcije_u_listbox(self, event=None):
        if not self.__lista_listbox.curselection():
            self.ocisti_labele()
            self.__izmena_button['state'] = DISABLED
            self.__obrisi_button['state'] = DISABLED
            return

        indeks = self.__lista_listbox.curselection()[0]
        naziv = self.__lista_listbox.get(indeks)
        radnik = 0
        for i in self.__podaci.zdrRadnici:
            if str(i.ime + " " + i.prezime) == naziv:
                radnik = i
        self.popuni_labele(radnik)

        self.__izmena_button['state'] = NORMAL
        self.__obrisi_button['state'] = NORMAL

    def filtriranje_listbox(self, var, index, mode):
        self.ocisti_labele()
        self.__izmena_button['state'] = DISABLED
        self.__obrisi_button['state'] = DISABLED
        self.__lista_listbox.delete(0, END)
        text = self.__pretraga_entry.get()
        for radnik in self.__podaci.zdrRadnici:
            if text.upper() in str(radnik.ime + " " + radnik.prezime).upper():
                self.__lista_listbox.insert(END, "{} {}".format(radnik.ime, radnik.prezime))

    def brisanje(self, indeks):
        self.__podaci.zdrRadnici.pop(indeks)
        self.update()
        Podaci.sacuvaj(self.__podaci)
        self.popuni_listu(self.__podaci.zdrRadnici)
        self.__pretraga_entry["text"] = ""
        self.ocisti_labele()

    def izmena(self, indeks):

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

                nazivRadnogMesta = self.ogranicenje_naziva_radnog_mesta()
                if not nazivRadnogMesta:
                    return

                self.__podaci.zdrRadnici[indeks].ime = ime
                self.__podaci.zdrRadnici[indeks].prezime = prezime
                self.__podaci.zdrRadnici[indeks].datumRodjenja = datumRodjenja
                self.__podaci.zdrRadnici[indeks].pol = pol
                self.__podaci.zdrRadnici[indeks].naziv = nazivRadnogMesta

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

            def ogranicenje_naziva_radnog_mesta(self):
                nazivRadnogMesta = self.__naziv_radnog_mesta_entry.get()
                if len(nazivRadnogMesta) < 2:
                    messagebox.showerror("Greška", "Naziv mora sadrzati bar 2 karaktera!")
                    return None
                return nazivRadnogMesta

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
                self.__jmbg_entry.insert(0, self.__podaci.zdrRadnici[indeks].jmbg)
                self.__jmbg_entry.config(state="disabled")

                Label(izmena_frame, text="Ime:").grid(row=1, sticky=E)
                self.__ime = StringVar(root)
                self.__ime_entry = Entry(izmena_frame, width=20, textvariable=self.__ime)
                self.__ime_entry.grid(row=1, column=1, sticky=W)
                self.__ime_entry.delete(0, END)
                self.__ime_entry.insert(0, self.__podaci.zdrRadnici[indeks].ime)

                Label(izmena_frame, text="Prezime:").grid(row=2, sticky=E)
                self.__prezime = StringVar(root)
                self.__prezime_entry = Entry(izmena_frame, width=20, textvariable=self.__prezime)
                self.__prezime_entry.grid(row=2, column=1, sticky=W)
                self.__prezime_entry.delete(0, END)
                self.__prezime_entry.insert(0, self.__podaci.zdrRadnici[indeks].prezime)

                Label(izmena_frame, text="Datum rodjenja:").grid(row=3, sticky=E)

                pomocni_frame = Frame(izmena_frame, padx=5, pady=5)
                pomocni_frame.grid(row=3, column=1, sticky=W)

                pomoc = str(datetime.datetime.strptime(self.__podaci.zdrRadnici[indeks]
                                                       .datumRodjenja, "%Y-%m-%d %H:%M:%S") \
                            .strftime("%d/%m/%Y/%H/%M/%S")).split("/")
                self.__vreme1 = IntVar(root)
                self.__godina_spinbox = Spinbox(pomocni_frame, width=5, from_=1900, increment=1, to=2022,
                                                textvariable=self.__vreme1)
                self.__godina_spinbox.grid(row=0, column=0, sticky=W)
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
                self.__pol_combobox.delete(0, END)
                self.__pol_combobox.insert(0, self.__podaci.zdrRadnici[indeks].pol)

                Label(izmena_frame, text="Naziv radnog mesta:").grid(row=5, sticky=E)
                self.__naziv_radnog_mesta = StringVar(root)
                self.__naziv_radnog_mesta_entry = Entry(izmena_frame, width=20, textvariable=self.__naziv_radnog_mesta)
                self.__naziv_radnog_mesta_entry.grid(row=5, column=1, sticky=W)
                self.__naziv_radnog_mesta_entry.delete(0, END)
                self.__naziv_radnog_mesta_entry.insert(0, self.__podaci.zdrRadnici[indeks].naziv)

                self.__izmeni_button = Button(izmena_frame, width=10, command=self.izmeni, text="Izmeni")
                self.__izmeni_button.grid(row=6, column=1, sticky=W)

                self.__izlaz_button = Button(izmena_frame, width=10, command=self.izlaz, text="Izlaz")
                self.__izlaz_button.grid(row=7, column=1, sticky=W)

        izmena_prozor = Izmena(self, self.__podaci)
        self.wait_window(izmena_prozor)
        if izmena_prozor.otkazano:
            return

        self.popuni_listu(self.__podaci.zdrRadnici)
        self.__pretraga_entry["text"] = ""

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

                nazivRadnogMesta = self.ogranicenje_naziva_radnog_mesta()
                if not nazivRadnogMesta:
                    return

                osoba = Osoba(jmbg, ime, prezime, datumRodjenja, pol)
                radnik = ZdravstveniRadnik(osoba, nazivRadnogMesta)
                self.__podaci.zdrRadnici.append(radnik)

                self.update()
                Podaci.sacuvaj(self.__podaci)

                self.__otkazano = False
                self.destroy()

            def ogranicenje_jmbg(self):
                jmbg = self.__jmbg_entry.get()
                if len(jmbg) != 13:
                    messagebox.showerror("Greška", "JMBG mora sadrzati 13 cifara!")
                    return None
                for i in self.__podaci.zdrRadnici:
                    if i.jmbg == jmbg:
                        messagebox.showerror("Greška", "U sistemu vec postoji osoba sa ovim JMBG-om!")
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

            def ogranicenje_naziva_radnog_mesta(self):
                nazivRadnogMesta = self.__naziv_radnog_mesta_entry.get()
                if len(nazivRadnogMesta) < 2:
                    messagebox.showerror("Greška", "Naziv mora sadrzati bar 2 karaktera!")
                    return None
                return nazivRadnogMesta

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

                Label(dodavanje_frame, text="Naziv radnog mesta:").grid(row=5, sticky=E)
                self.__naziv_radnog_mesta = StringVar(root)
                self.__naziv_radnog_mesta_entry = Entry(dodavanje_frame, width=20,
                                                        textvariable=self.__naziv_radnog_mesta)
                self.__naziv_radnog_mesta_entry.grid(row=5, column=1, sticky=W)

                self.__dodaj_button = Button(dodavanje_frame, width=10, command=self.dodaj, text="Dodaj")
                self.__dodaj_button.grid(row=6, column=1, sticky=W)

                self.__izlaz_button = Button(dodavanje_frame, width=10, command=self.izlaz, text="Izlaz")
                self.__izlaz_button.grid(row=7, column=1, sticky=W)

        dodavanje_prozor = Dodavanje(self, self.__podaci)
        self.wait_window(dodavanje_prozor)
        if dodavanje_prozor.otkazano:
            return

        self.popuni_listu(self.__podaci.zdrRadnici)
        self.__pretraga_entry["text"] = ""

    def __init__(self, root, podaci):
        super().__init__(root)
        self.__podaci = podaci
        self.__otkazano = True

        self.title("Zdravstveni radnici")
        self.minsize(400, 200)
        self.geometry('+350+100')
        # self.iconbitmap('c:/Users/Jovana/Desktop/ftn.ico')
        self.iconbitmap('c:/Users/korisnik/Desktop/InfoCentar za vakcinisanje/ftn.ico')
        # izbrisi ovu moju putanju i postavi ovu iznad svoju za sliku

        radnik_frame = Frame(self, padx=5, pady=5)
        radnik_frame.pack(expand=1)

        self.__dodaj_button = Button(radnik_frame, width=10, command=self.dodavanje, text="Dodaj")
        self.__dodaj_button.grid(row=0, column=1, sticky=W)

        self.__izmena_button = Button(radnik_frame, width=10, command=self.indeksiranje1, text="Izmeni")
        self.__izmena_button.grid(row=1, column=1, sticky=W)

        self.__obrisi_button = Button(radnik_frame, width=10, command=self.indeksiranje2, text="Obrisi")
        self.__obrisi_button.grid(row=2, column=1, sticky=W)

        self.__pretraga = StringVar(root)
        self.__pretraga.trace_add("write", self.filtriranje_listbox)
        self.__pretraga_entry = Entry(radnik_frame, width=20, textvariable=self.__pretraga)
        self.__pretraga_entry.grid(row=3, column=1, sticky=W)

        self.__lista_listbox = Listbox(radnik_frame, activestyle="none", exportselection=False)
        self.__lista_listbox.grid(row=4, column=1, sticky=W)

        Label(radnik_frame, text="JMBG:").grid(row=5, sticky=E)
        self.__labela_jmbg = Label(radnik_frame, text="")
        self.__labela_jmbg.grid(row=5, column=1, sticky=W)
        Label(radnik_frame, text="Ime:").grid(row=6, sticky=E)
        self.__labela_ime = Label(radnik_frame, text="")
        self.__labela_ime.grid(row=6, column=1, sticky=W)
        Label(radnik_frame, text="Prezime:").grid(row=7, sticky=E)
        self.__labela_prezime = Label(radnik_frame, text="")
        self.__labela_prezime.grid(row=7, column=1, sticky=W)
        Label(radnik_frame, text="Datum rodjenja:").grid(row=8, sticky=E)
        self.__labela_datum_rodjenja = Label(radnik_frame, text="")
        self.__labela_datum_rodjenja.grid(row=8, column=1, sticky=W)
        Label(radnik_frame, text="Pol:").grid(row=9, sticky=E)
        self.__labela_pol = Label(radnik_frame, text="")
        self.__labela_pol.grid(row=9, column=1, sticky=W)
        Label(radnik_frame, text="Naziv radnog mesta:").grid(row=10, sticky=E)
        self.__labela_naziv_radnog_mesta = Label(radnik_frame, text="")
        self.__labela_naziv_radnog_mesta.grid(row=10, column=1, sticky=W)

        self.popuni_listu(self.__podaci.zdrRadnici)
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
        for i in self.__podaci.zdrRadnici:
            if naziv == str(i.ime + " " + i.prezime):
                indeks = self.__podaci.zdrRadnici.index(i)
        self.izmena(indeks)

    def indeksiranje2(self):
        broj = self.__lista_listbox.curselection()[0]
        naziv = self.__lista_listbox.get(broj)
        indeks = 0
        for i in self.__podaci.zdrRadnici:
            if naziv == str(i.ime + " " + i.prezime):
                indeks = self.__podaci.zdrRadnici.index(i)
        odgovor = messagebox.askokcancel("Brisanje zdravstvenog radnika",
                                         "Brisanjem radnika brisete i sve podatke vezane za njega. Da li ste sigurni da zelite da izbrisete radnika?",
                                         icon="warning")
        if odgovor:
            self.brisanje(indeks)

    @property
    def otkazano(self):
        return self.__otkazano

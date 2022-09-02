from tkinter import *
from tkinter import messagebox
from vakcinisanje import *
from datetime import date


class PristupVakcinama(Toplevel):

    def popuni_listu(self, vakcine):
        self.__lista_listbox.delete(0, END)
        for vakcina in vakcine:
            self.__lista_listbox.insert(END, "{} {}".format(vakcina.naziv, vakcina.serijskiBroj))
        self.__izmena_button['state'] = DISABLED
        self.__obrisi_button['state'] = DISABLED

    def popuni_labele(self, vakcine):
        self.__labela_naziv["text"] = vakcine.naziv
        self.__labela_serijski_broj["text"] = vakcine.serijskiBroj
        self.__labela_poreklo["text"] = vakcine.poreklo
        self.__labela_rok["text"] = vakcine.rok

    def ocisti_labele(self):
        self.__labela_naziv["text"] = ""
        self.__labela_serijski_broj["text"] = ""
        self.__labela_poreklo["text"] = ""
        self.__labela_rok["text"] = ""

    def promena_selekcije_u_listbox(self, event=None):
        if not self.__lista_listbox.curselection():
            self.ocisti_labele()
            self.__izmena_button['state'] = DISABLED
            self.__obrisi_button['state'] = DISABLED
            return

        indeks = self.__lista_listbox.curselection()[0]
        naziv = self.__lista_listbox.get(indeks)
        vakcina = 0
        for i in self.__podaci.vakcine:
            if str(i.naziv + " " + str(i.serijskiBroj)) == naziv:
                vakcina = i
        self.popuni_labele(vakcina)

        self.__izmena_button['state'] = NORMAL
        self.__obrisi_button['state'] = NORMAL

    def filtriranje_listbox(self, var, index, mode):
        self.ocisti_labele()
        self.__izmena_button['state'] = DISABLED
        self.__obrisi_button['state'] = DISABLED
        self.__lista_listbox.delete(0, END)
        text = self.__pretraga_entry.get()
        for vakcina in self.__podaci.vakcine:
            if text.upper() in str(vakcina.naziv + vakcina.serijskiBroj).upper():
                self.__lista_listbox.insert(END, "{} {}".format(vakcina.naziv, vakcina.serijskiBroj))

    def brisanje(self, indeks):
        self.__podaci.vakcine.pop(indeks)
        self.update()
        Podaci.sacuvaj(self.__podaci)
        self.popuni_listu(self.__podaci.vakcine)
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
                naziv = self.ogranicenje_naziva()
                if not naziv:
                    return

                serijskiBroj = self.ogranicenje_serijskog_broja()
                if not serijskiBroj:
                    return

                poreklo = self.ogranicenje_porekla()
                if not poreklo:
                    return

                rok = self.ogranicenje_roka()
                if not rok:
                    return

                self.__podaci.vakcine[indeks].naziv = naziv
                self.__podaci.vakcine[indeks].serijskiBroj = serijskiBroj
                self.__podaci.vakcine[indeks].poreklo = poreklo
                self.__podaci.vakcine[indeks].rok = rok

                self.update()
                Podaci.sacuvaj(self.__podaci)

                self.__otkazano = False
                self.destroy()

            def ogranicenje_naziva(self):
                naziv = self.__naziv_entry.get()
                if len(naziv) < 2:
                    messagebox.showerror("Greška", "Naziv mora sadrzati bar 2 karaktera!")
                    return None
                return naziv

            def ogranicenje_serijskog_broja(self):
                serijskiBroj = self.__serijski_broj_entry.get()
                if len(serijskiBroj) != 10:
                    messagebox.showerror("Greška", "Serijski broj mora sadrzati 10 cifara!")
                    return None
                return serijskiBroj

            def ogranicenje_porekla(self):
                poreklo = self.__poreklo_entry.get()
                if len(poreklo) < 2:
                    messagebox.showerror("Greška", "Zemlja porekla mora sadrzati bar 2 karaktera!")
                    return None
                return poreklo

            def ogranicenje_roka(self):
                danas = date.today().strftime("%d/%m/%Y").split("/")
                danasdan = int(danas[0])
                danasmesec = int(danas[1])
                danasgodina = int(danas[2])
                godina = int(self.__godina_spinbox.get())
                mesec = int(self.__mesec_spinbox.get())
                dan = int(self.__dan_spinbox.get())
                sat = int(self.__sat_spinbox.get())
                minut = int(self.__minut_spinbox.get())
                sekunda = int(self.__sekund_spinbox.get())
                if godina < danasgodina:
                    messagebox.showerror("Greška", "Ponovo unesite godinu!")
                    return None
                elif godina == danasgodina:
                    if mesec < danasmesec:
                        messagebox.showerror("Greška", "Ponovo unesite mesec!")
                        return None
                    elif mesec == danasmesec:
                        if dan <= danasdan:
                            messagebox.showerror("Greška", "Ponovo unesite dan!")
                            return None
                        else:
                            if mesec < 1 or mesec > 12:
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
                    else:
                        if mesec < 1 or mesec > 12:
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

                Label(izmena_frame, text="Naziv:").grid(row=0, sticky=E)
                self.__naziv = StringVar(root)
                self.__naziv_entry = Entry(izmena_frame, width=20, textvariable=self.__naziv)
                self.__naziv_entry.grid(row=0, column=1, sticky=W)
                self.__naziv_entry.delete(0, END)
                self.__naziv_entry.insert(0, self.__podaci.vakcine[indeks].naziv)

                Label(izmena_frame, text="Serijski broj:").grid(row=1, sticky=E)
                self.__serijski_broj = StringVar(root)
                self.__serijski_broj_entry = Entry(izmena_frame, width=20, textvariable=self.__serijski_broj)
                self.__serijski_broj_entry.grid(row=1, column=1, sticky=W)
                self.__serijski_broj_entry.delete(0, END)
                self.__serijski_broj_entry.insert(0, self.__podaci.vakcine[indeks].serijskiBroj)
                self.__serijski_broj_entry.config(state="disabled")

                Label(izmena_frame, text="Zemlja porekla:").grid(row=2, sticky=E)
                self.__poreklo = StringVar(root)
                self.__poreklo_entry = Entry(izmena_frame, width=20, textvariable=self.__poreklo)
                self.__poreklo_entry.grid(row=2, column=1, sticky=W)
                self.__poreklo_entry.delete(0, END)
                self.__poreklo_entry.insert(0, self.__podaci.vakcine[indeks].poreklo)

                Label(izmena_frame, text="Rok trajanja:").grid(row=3, sticky=E)

                pomocni_frame = Frame(izmena_frame, padx=5, pady=5)
                pomocni_frame.grid(row=3, column=1, sticky=W)
                pomoc = str(datetime.datetime.strptime(self.__podaci.vakcine[indeks]
                                                       .rok, "%Y-%m-%d %H:%M:%S") \
                            .strftime("%d/%m/%Y/%H/%M/%S")).split("/")
                self.__vreme1 = IntVar(root)
                self.__godina_spinbox = Spinbox(pomocni_frame, width=5, from_=2022, increment=1, to=3000,
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

                self.__izmeni_button = Button(izmena_frame, width=10, command=self.izmeni, text="Izmeni")
                self.__izmeni_button.grid(row=4, column=1, sticky=W)

                self.__izlaz_button = Button(izmena_frame, width=10, command=self.izlaz, text="Izlaz")
                self.__izlaz_button.grid(row=5, column=1, sticky=W)

        izmena_prozor = Izmena(self, self.__podaci)
        self.wait_window(izmena_prozor)
        if izmena_prozor.otkazano:
            return
        self.popuni_listu(self.__podaci.vakcine)
        self.__pretraga_entry["text"] = ""
        self.__izmena_button['state'] = NORMAL
        self.__obrisi_button['state'] = NORMAL

    def dodavanje(self):

        class Dodavanje(Toplevel):

            def izlaz(self):
                self.destroy()

            @property
            def otkazano(self):
                return self.__otkazano

            def dodaj(self):
                naziv = self.ogranicenje_naziva()
                if not naziv:
                    return

                serijskiBroj = self.ogranicenje_serijskog_broja()
                if not serijskiBroj:
                    return

                poreklo = self.ogranicenje_porekla()
                if not poreklo:
                    return

                rok = self.ogranicenje_roka()
                if not rok:
                    return

                vakcina = Vakcina(naziv, serijskiBroj, poreklo, rok)
                self.__podaci.vakcine.append(vakcina)

                self.update()
                Podaci.sacuvaj(self.__podaci)

                self.__otkazano = False
                self.destroy()

            def ogranicenje_naziva(self):
                naziv = self.__naziv_entry.get()
                if len(naziv) < 2:
                    messagebox.showerror("Greška", "Naziv mora sadrzati bar 2 karaktera!")
                    return None
                return naziv

            def ogranicenje_serijskog_broja(self):
                serijskiBroj = self.__serijski_broj_entry.get()
                if len(serijskiBroj) != 10:
                    messagebox.showerror("Greška", "Serijski broj mora sadrzati 10 cifara!")
                    return None
                return serijskiBroj

            def ogranicenje_porekla(self):
                poreklo = self.__poreklo_entry.get()
                if len(poreklo) < 2:
                    messagebox.showerror("Greška", "Zemlja porekla mora sadrzati bar 2 karaktera!")
                    return None
                return poreklo

            def ogranicenje_roka(self):
                danas = date.today().strftime("%d/%m/%Y").split("/")
                danasdan = int(danas[0])
                danasmesec = int(danas[1])
                danasgodina = int(danas[2])
                godina = int(self.__godina_spinbox.get())
                mesec = int(self.__mesec_spinbox.get())
                dan = int(self.__dan_spinbox.get())
                sat = int(self.__sat_spinbox.get())
                minut = int(self.__minut_spinbox.get())
                sekunda = int(self.__sekund_spinbox.get())
                if godina < danasgodina:
                    messagebox.showerror("Greška", "Ponovo unesite godinu!")
                    return None
                elif godina == danasgodina:
                    if mesec < danasmesec:
                        messagebox.showerror("Greška", "Ponovo unesite mesec!")
                        return None
                    elif mesec == danasmesec:
                        if dan <= danasdan:
                            messagebox.showerror("Greška", "Ponovo unesite dan!")
                            return None
                        else:
                            if mesec < 1 or mesec > 12:
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
                    else:
                        if mesec < 1 or mesec > 12:
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

                Label(dodavanje_frame, text="Naziv:").grid(row=0, sticky=E)
                self.__naziv = StringVar(root)
                self.__naziv_entry = Entry(dodavanje_frame, width=20, textvariable=self.__naziv)
                self.__naziv_entry.grid(row=0, column=1, sticky=W)

                Label(dodavanje_frame, text="Serijski broj:").grid(row=1, sticky=E)
                self.__serijski_broj = StringVar(root)
                self.__serijski_broj_entry = Entry(dodavanje_frame, width=20, textvariable=self.__serijski_broj)
                self.__serijski_broj_entry.grid(row=1, column=1, sticky=W)

                Label(dodavanje_frame, text="Zemlja porekla:").grid(row=2, sticky=E)
                self.__poreklo = StringVar(root)
                self.__poreklo_entry = Entry(dodavanje_frame, width=20, textvariable=self.__poreklo)
                self.__poreklo_entry.grid(row=2, column=1, sticky=W)

                Label(dodavanje_frame, text="Rok trajanja:").grid(row=3, sticky=E)

                pomocni_frame = Frame(dodavanje_frame, padx=5, pady=5)
                pomocni_frame.grid(row=3, column=1, sticky=W)
                pomoc = date.today().strftime("%d/%m/%Y").split("/")
                self.__vreme1 = IntVar(root)
                self.__godina_spinbox = Spinbox(pomocni_frame, width=5, from_=2022, increment=1, to=3000,
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
                self.__vreme5 = IntVar(root)
                self.__minut_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=60,
                                               textvariable=self.__vreme5)
                self.__minut_spinbox.grid(row=0, column=4, sticky=W)
                self.__vreme6 = IntVar(root)
                self.__sekund_spinbox = Spinbox(pomocni_frame, width=5, from_=0, increment=1, to=60,
                                                textvariable=self.__vreme6)
                self.__sekund_spinbox.grid(row=0, column=5, sticky=W)

                self.__dodaj_button = Button(dodavanje_frame, width=10, command=self.dodaj, text="Dodaj")
                self.__dodaj_button.grid(row=4, column=1, sticky=W)

                self.__izlaz_button = Button(dodavanje_frame, width=10, command=self.izlaz, text="Izlaz")
                self.__izlaz_button.grid(row=5, column=1, sticky=W)

        dodavanje_prozor = Dodavanje(self, self.__podaci)
        self.wait_window(dodavanje_prozor)
        if dodavanje_prozor.otkazano:
            return

        self.popuni_listu(self.__podaci.vakcine)
        self.__izmena_button['state'] = NORMAL
        self.__obrisi_button['state'] = NORMAL
        self.__pretraga_entry["text"] = ""

    def __init__(self, root, podaci):
        super().__init__(root)
        self.__podaci = podaci
        self.__otkazano = True

        self.title("Vakcine")
        self.minsize(400, 200)
        self.geometry('+350+100')
        # self.iconbitmap('c:/Users/Jovana/Desktop/ftn.ico')
        self.iconbitmap('c:/Users/korisnik/Desktop/InfoCentar za vakcinisanje/ftn.ico')
        # izbrisi ovu moju putanju i postavi ovu iznad svoju za sliku

        vakcina_frame = Frame(self, padx=5, pady=5)
        vakcina_frame.pack(expand=1)

        self.__dodaj_button = Button(vakcina_frame, width=10, command=self.dodavanje, text="Dodaj")
        self.__dodaj_button.grid(row=0, column=1, sticky=W)

        self.__izmena_button = Button(vakcina_frame, width=10, command=self.indeksiranje1, text="Izmeni")
        self.__izmena_button.grid(row=1, column=1, sticky=W)

        self.__obrisi_button = Button(vakcina_frame, width=10, command=self.indeksiranje2, text="Obrisi")
        self.__obrisi_button.grid(row=2, column=1, sticky=W)

        self.__pretraga = StringVar(root)
        self.__pretraga.trace_add("write", self.filtriranje_listbox)
        self.__pretraga_entry = Entry(vakcina_frame, width=20, textvariable=self.__pretraga)
        self.__pretraga_entry.grid(row=3, column=1, sticky=W)

        self.__lista_listbox = Listbox(vakcina_frame, activestyle="none", exportselection=False)
        self.__lista_listbox.grid(row=4, column=1, sticky=W)

        Label(vakcina_frame, text="Naziv:").grid(row=5, sticky=E)
        self.__labela_naziv = Label(vakcina_frame, text="")
        self.__labela_naziv.grid(row=5, column=1, sticky=W)
        Label(vakcina_frame, text="Serijski broj:").grid(row=6, sticky=E)
        self.__labela_serijski_broj = Label(vakcina_frame, text="")
        self.__labela_serijski_broj.grid(row=6, column=1, sticky=W)
        Label(vakcina_frame, text="Zemlja porekla:").grid(row=7, sticky=E)
        self.__labela_poreklo = Label(vakcina_frame, text="")
        self.__labela_poreklo.grid(row=7, column=1, sticky=W)
        Label(vakcina_frame, text="Rok trajanja:").grid(row=8, sticky=E)
        self.__labela_rok = Label(vakcina_frame, text="")
        self.__labela_rok.grid(row=8, column=1, sticky=W)

        self.popuni_listu(self.__podaci.vakcine)
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
        for i in self.__podaci.vakcine:
            if naziv == str(i.naziv + " " + str(i.serijskiBroj)):
                indeks = self.__podaci.vakcine.index(i)
        self.izmena(indeks)

    def indeksiranje2(self):
        broj = self.__lista_listbox.curselection()[0]
        naziv = self.__lista_listbox.get(broj)
        indeks = 0
        for i in self.__podaci.vakcine:
            if naziv == str(i.naziv + " " + str(i.serijskiBroj)):
                indeks = self.__podaci.vakcine.index(i)
        odgovor = messagebox.askokcancel("Brisanje vakcine",
                                         "Brisanjem vakcine brisete i sve podatke vezane za nju. Da li ste sigurni da zelite da izbrisete vakcinu?",
                                         icon="warning")
        if odgovor:
            self.brisanje(indeks)

    @property
    def otkazano(self):
        return self.__otkazano
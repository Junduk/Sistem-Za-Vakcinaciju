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
                                        "{} {} {}".format(potvrde.gradjani.ime, potvrde.gradjani.prezime,
                                                          potvrde.datumtoString))
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
        self.__podaci.potvrde.pop(indeks)
        self.update()
        Podaci.sacuvaj(self.__podaci)
        self.popuni_listu(self.__podaci.potvrde)
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
                sifra = self.ogranicenje_sifre()
                if not sifra:
                    return

                datum = self.ogranicenje_datuma()
                if not datum:
                    return

                doza = self.ogranicenje_doze()
                if not doza:
                    return

                gradjanin = self.ogranicenje_gradjanina()
                if not gradjanin:
                    return

                radnik = self.ogranicenje_radnika()
                if not radnik:
                    return

                self.__podaci.potvrde[indeks].sifra = sifra
                self.__podaci.potvrde[indeks].datum = datum
                self.__podaci.potvrde[indeks].doza = doza
                self.__podaci.potvrde[indeks].gradjanin = gradjanin
                self.__podaci.potvrde[indeks].zdrRadnik = radnik

                self.update()
                Podaci.sacuvaj(self.__podaci)

                self.__otkazano = False
                self.destroy()

            def ogranicenje_sifre(self):
                sifra = self.__sifra_entry.get()
                if len(sifra) != 8:
                    messagebox.showerror("Greška", "Sifra mora sadrzati 8 karaktera!")
                    return None
                return sifra

            def ogranicenje_datuma(self):
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
                if godina > danasgodina:
                    messagebox.showerror("Greška", "Ponovo unesite godinu!")
                    return None
                elif godina == danasgodina:
                    if mesec > danasmesec:
                        messagebox.showerror("Greška", "Ponovo unesite mesec!")
                        return None
                    elif mesec == danasmesec:
                        if dan > danasdan:
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

            def ogranicenje_doze(self):
                doza = self.__doza_combobox.get()
                if doza == "":
                    messagebox.showerror("Greška", "Izaberite dozu!")
                    return None
                for i in self.__podaci.doza:
                    if doza == i.gradjani.ime + " " + i.gradjani.prezime + " " + i.datum:
                        return i

            def ogranicenje_gradjanina(self):
                gradjanin = self.__gradjanin_combobox.get()
                if gradjanin == "":
                    messagebox.showerror("Greška", "Izaberite gradjanina!")
                    return None
                for i in self.__podaci.gradjani:
                    if gradjanin == i.ime + " " + i.prezime + " " + i.jmbg:
                        return i

            def ogranicenje_radnika(self):
                radnik = self.__radnik_combobox.get()
                if radnik == "":
                    messagebox.showerror("Greška", "Izaberite zdravstvenog radnika!")
                    return None
                for i in self.__podaci.zdrRadnici:
                    if radnik == i.ime + " " + i.prezime + " " + i.jmbg:
                        return i

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

                dodavanje_frame = Frame(self, padx=5, pady=5)
                dodavanje_frame.pack(expand=1)

                Label(dodavanje_frame, text="Sifra:").grid(row=0, sticky=E)
                self.__sifra = StringVar(root)
                self.__sifra_entry = Entry(dodavanje_frame, width=20, textvariable=self.__sifra)
                self.__sifra_entry.grid(row=0, column=1, sticky=W)
                self.__sifra_entry.delete(0, END)
                self.__sifra_entry.insert(0, self.__podaci.potvrde[indeks].sifra)
                self.__sifra_entry.config(state="disabled")

                Label(dodavanje_frame, text="Datum izdavanja:").grid(row=1, sticky=E)

                pomocni_frame = Frame(dodavanje_frame, padx=5, pady=5)
                pomocni_frame.grid(row=1, column=1, sticky=W)
                pomoc = str(datetime.datetime.strptime(self.__podaci.potvrde[indeks].datum, "%Y-%m-%d %H:%M:%S") \
                            .strftime("%d/%m/%Y/%H/%M/%S")).split("/")

                self.__vreme1 = IntVar(root)
                self.__godina_spinbox = Spinbox(pomocni_frame, width=5, from_=2016, increment=1, to=3000,
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

                Label(dodavanje_frame, text="Doza:").grid(row=2, sticky=E)
                self.__doza = StringVar(root)
                self.__doza_combobox = Combobox(dodavanje_frame, textvariable=self.__doza, width=35)
                self.__doza_combobox.grid(row=2, column=1, sticky=W)
                self.__doza_combobox.delete(0, END)
                self.__doza_combobox.insert(0, self.__podaci.potvrde[indeks].gradjani.ime + " "
                                            + self.__podaci.potvrde[indeks].gradjani.prezime + " "
                                            + self.__podaci.potvrde[indeks].datumtoString)
                niz1 = []
                for i in self.__podaci.doze:
                    niz1.append(i.gradjani.ime + " " + i.gradjani.prezime + " " + i.datumtoString)
                self.__doza_combobox['values'] = niz1

                Label(dodavanje_frame, text="Gradjanin:").grid(row=3, sticky=E)
                self.__gradjanin = StringVar(root)
                self.__gradjanin_combobox = Combobox(dodavanje_frame, textvariable=self.__gradjanin, width=35)
                self.__gradjanin_combobox.grid(row=3, column=1, sticky=W)
                self.__gradjanin_combobox.delete(0, END)
                self.__gradjanin_combobox.insert(0, self.__podaci.potvrde[indeks].gradjani.ime + " "
                                                 + self.__podaci.potvrde[indeks].gradjani.prezime + " "
                                                 + self.__podaci.potvrde[indeks].gradjani.jmbg)
                niz2 = []
                for i in self.__podaci.doze:
                    niz2.append(i.gradjani.ime + " " + i.gradjani.prezime + " " + i.gradjani.jmbg)
                self.__gradjanin_combobox['values'] = niz2

                Label(dodavanje_frame, text="Zdravstveni radnik:").grid(row=4, sticky=E)
                self.__radnik = StringVar(root)
                self.__radnik_combobox = Combobox(dodavanje_frame, textvariable=self.__radnik, width=35)
                self.__radnik_combobox.grid(row=4, column=1, sticky=W)
                self.__radnik_combobox.delete(0, END)
                self.__radnik_combobox.insert(0, self.__podaci.potvrde[indeks].zdrRadnik.ime + " "
                                              + self.__podaci.potvrde[indeks].zdrRadnik.prezime + " "
                                              + self.__podaci.potvrde[indeks].zdrRadnik.jmbg)
                niz3 = []
                for i in self.__podaci.zdrRadnici:
                    niz3.append(i.ime + " " + i.prezime + " " + i.jmbg)
                self.__radnik_combobox['values'] = niz3

                self.__dodaj_button = Button(dodavanje_frame, width=10, command=self.izmeni, text="Izmeni")
                self.__dodaj_button.grid(row=7, column=1, sticky=W)

                self.__izlaz_button = Button(dodavanje_frame, width=10, command=self.izlaz, text="Izlaz")
                self.__izlaz_button.grid(row=8, column=1, sticky=W)

        izmena_prozor = Izmena(self, self.__podaci)
        self.wait_window(izmena_prozor)
        if izmena_prozor.otkazano:
            return

        self.popuni_listu(self.__podaci.potvrde)
        self.__izmena_button['state'] = NORMAL
        self.__obrisi_button['state'] = NORMAL
        self.__pretraga_entry["text"] = ""

    def dodavanje(self):

        class Dodavanje(Toplevel):

            def izlaz(self):
                self.destroy()

            @property
            def otkazano(self):
                return self.__otkazano

            def dodaj(self):
                sifra = self.ogranicenje_sifre()
                if not sifra:
                    return

                datum = self.ogranicenje_datuma()
                if not datum:
                    return

                doza = self.ogranicenje_doze()
                if not doza:
                    return

                gradjanin = self.ogranicenje_gradjanina()
                if not gradjanin:
                    return

                radnik = self.ogranicenje_radnika()
                if not radnik:
                    return

                potvrda = Potvrda(sifra, datum, doza, gradjanin, radnik)
                self.__podaci.potvrde.append(potvrda)

                self.update()
                Podaci.sacuvaj(self.__podaci)

                self.__otkazano = False
                self.destroy()

            def ogranicenje_sifre(self):
                sifra = self.__sifra_entry.get()
                if len(sifra) != 8:
                    messagebox.showerror("Greška", "Sifra mora sadrzati 8 karaktera!")
                    return None
                return sifra

            def ogranicenje_datuma(self):
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
                if godina > danasgodina:
                    messagebox.showerror("Greška", "Ponovo unesite godinu!")
                    return None
                elif godina == danasgodina:
                    if mesec > danasmesec:
                        messagebox.showerror("Greška", "Ponovo unesite mesec!")
                        return None
                    elif mesec == danasmesec:
                        if dan > danasdan:
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

            def ogranicenje_doze(self):
                doza = self.__doza_combobox.get()
                if doza == "":
                    messagebox.showerror("Greška", "Izaberite dozu!")
                    return None
                for i in self.__podaci.doze:
                    if doza == i.gradjani.ime + " " + i.gradjani.prezime + " " + i.datumtoString:
                        return i

            def ogranicenje_gradjanina(self):
                gradjanin = self.__gradjanin_combobox.get()
                if gradjanin == "":
                    messagebox.showerror("Greška", "Izaberite gradjanina!")
                    return None
                for i in self.__podaci.gradjani:
                    if gradjanin == i.ime + " " + i.prezime + " " + i.jmbg:
                        return i

            def ogranicenje_radnika(self):
                radnik = self.__radnik_combobox.get()
                if radnik == "":
                    messagebox.showerror("Greška", "Izaberite zdravstvenog radnika!")
                    return None
                for i in self.__podaci.zdrRadnici:
                    if radnik == i.ime + " " + i.prezime + " " + i.jmbg:
                        return i

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

                Label(dodavanje_frame, text="Sifra:").grid(row=0, sticky=E)
                self.__sifra = StringVar(root)
                self.__sifra_entry = Entry(dodavanje_frame, width=20, textvariable=self.__sifra)
                self.__sifra_entry.grid(row=0, column=1, sticky=W)

                Label(dodavanje_frame, text="Datum izdavanja:").grid(row=1, sticky=E)

                pomocni_frame = Frame(dodavanje_frame, padx=5, pady=5)
                pomocni_frame.grid(row=1, column=1, sticky=W)

                self.__vreme1 = IntVar(root)
                self.__godina_spinbox = Spinbox(pomocni_frame, width=5, from_=2016, increment=1, to=3000,
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

                Label(dodavanje_frame, text="Doza:").grid(row=2, sticky=E)
                self.__doza = StringVar(root)
                self.__doza_combobox = Combobox(dodavanje_frame, textvariable=self.__doza, width=35)
                self.__doza_combobox.grid(row=2, column=1, sticky=W)
                niz1 = []
                for i in self.__podaci.doze:
                    niz1.append(i.gradjani.ime + " " + i.gradjani.prezime + " " + i.datumtoString)
                self.__doza_combobox['values'] = niz1

                Label(dodavanje_frame, text="Gradjanin:").grid(row=3, sticky=E)
                self.__gradjanin = StringVar(root)
                self.__gradjanin_combobox = Combobox(dodavanje_frame, textvariable=self.__gradjanin, width=35)
                self.__gradjanin_combobox.grid(row=3, column=1, sticky=W)
                niz2 = []
                for i in self.__podaci.potvrde:
                    niz2.append(i.gradjani.ime + " " + i.gradjani.prezime + " " + i.gradjani.jmbg)
                self.__gradjanin_combobox['values'] = niz2

                Label(dodavanje_frame, text="Zdravstveni radnik:").grid(row=4, sticky=E)
                self.__radnik = StringVar(root)
                self.__radnik_combobox = Combobox(dodavanje_frame, textvariable=self.__radnik, width=35)
                self.__radnik_combobox.grid(row=4, column=1, sticky=W)
                niz3 = []
                for i in self.__podaci.zdrRadnici:
                    niz3.append(i.ime + " " + i.prezime + " " + i.jmbg)
                self.__radnik_combobox['values'] = niz3

                self.__dodaj_button = Button(dodavanje_frame, width=10, command=self.dodaj, text="Dodaj")
                self.__dodaj_button.grid(row=7, column=1, sticky=W)

                self.__izlaz_button = Button(dodavanje_frame, width=10, command=self.izlaz, text="Izlaz")
                self.__izlaz_button.grid(row=8, column=1, sticky=W)

        dodavanje_prozor = Dodavanje(self, self.__podaci)
        self.wait_window(dodavanje_prozor)
        if dodavanje_prozor.otkazano:
            return

        self.popuni_listu(self.__podaci.potvrde)
        self.__izmena_button['state'] = NORMAL
        self.__obrisi_button['state'] = NORMAL
        self.__pretraga_entry["text"] = ""

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

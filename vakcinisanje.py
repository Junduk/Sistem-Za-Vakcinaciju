import datetime
import pickle


class Osoba:

    @property
    def jmbg(self):
        return self.__jmbg

    @jmbg.setter
    def jmbg(self, jmbg):
        self.__jmbg = jmbg

    @property
    def ime(self):
        return self.__ime

    @ime.setter
    def ime(self, ime):
        self.__ime = ime

    @property
    def prezime(self):
        return self.__prezime

    @prezime.setter
    def prezime(self, prezime):
        self.__prezime = prezime

    @property
    def datumRodjenja(self):
        return self.__datumRodjenja

    @datumRodjenja.setter
    def datumRodjenja(self, datumRodjenja):
        self.__datumRodjenja = datumRodjenja

    @property
    def pol(self):
        return self.__pol

    @pol.setter
    def pol(self, pol):
        self.__pol = pol

    def __init__(self, jmbg, ime, prezime, datumRodjenja, pol):
        self.__jmbg = jmbg
        self.__ime = ime
        self.__prezime = prezime
        self.__datumRodjenja = datumRodjenja
        self.__pol = pol

    def __str__(self):
        format_linije = "{:>5}: {}"

        return "\n".join([
            "",
            format_linije.format("JMBG", self.__jmbg),
            format_linije.format("Ime", self.__ime),
            format_linije.format("Prezime", self.__prezime),
            format_linije.format("Datum rodjenja", self.__datumRodjenja.strftime("%d.%m.%Y. %H:%M:%S")),
            format_linije.format("Pol", self.__pol)
        ])


class Gradjanin(Osoba):

    @property
    def brojLicneKarte(self):
        return self.__brojLicneKarte

    @brojLicneKarte.setter
    def brojLicneKarte(self, brojLicneKarte):
        self.__brojLicneKarte = brojLicneKarte

    @property
    def listaDoza(self):
        return self.__listaDoza

    @listaDoza.setter
    def listaDoza(self, listaDoza):
        self.__listaDoza.append(listaDoza)

    @property
    def listaPotvrda(self):
        return self.__listaPotvrda

    @listaPotvrda.setter
    def listaPotvrda(self, listaPotvrda):
        self.__listaPotvrda.append(listaPotvrda)

    @property
    def listaSertifikata(self):
        return self.__listaSertifikata

    @listaSertifikata.setter
    def listaSertifikata(self, listaSertifikata):
        self.__listaSertifikata.append(listaSertifikata)

    def __init__(self, osoba, brojLicneKarte, listaDoza, listaPotvrda, sertifikat):
        Osoba.__init__(self, osoba.jmbg, osoba.ime, osoba.prezime, osoba.datumRodjenja, osoba.pol)
        self.__brojLicneKarte = brojLicneKarte
        self.__listaDoza = []
        self.__listaDoza.append(listaDoza)
        self.__listaPotvrda = []
        self.__listaPotvrda.append(listaPotvrda)
        self.__listaSertifikata = []
        self.__listaSertifikata.append(sertifikat)

    def __str__(self):
        format_linije = "{:>5}: {}"

        return "\n".join([
            "",
            format_linije.format("Broj licne karte", self.__brojLicneKarte),
            format_linije.format("Lista doza", self.__listaDoza),
            format_linije.format("Lista potvrda", self.__listaPotvrda),
            format_linije.format("Sertifikat", self.__sertifikat.sifra)
        ])


class ZdravstveniRadnik(Osoba):

    @property
    def naziv(self):
        return self.__naziv

    @naziv.setter
    def naziv(self, naziv):
        self.__naziv = naziv

    def __init__(self, osoba, naziv):
        Osoba.__init__(self, osoba.jmbg, osoba.ime, osoba.prezime, osoba.datumRodjenja, osoba.pol)
        self.__naziv = naziv

    def __str__(self):
        format_linije = "{:>5}: {}"

        return "\n".join([
            "",
            format_linije.format("JMBG", self.jmbg),
            format_linije.format("Ime", self.ime),
            format_linije.format("Prezime", self.prezime),
            format_linije.format("Datum rodjenja", self.datumRodjenja),
            format_linije.format("Pol", self.pol),
            format_linije.format("Naziv", self.__naziv)
        ])

class Doza:

    @property
    def datum(self):
        return self.__datum

    @datum.setter
    def datum(self, datum):
        self.__datum = datum

    @property
    def vakcina(self):
        return self.__vakcina

    @vakcina.setter
    def vakcina(self, vakcina):
        self.__vakcina = vakcina

    @property
    def zdrRadnik(self):
        return self.zdrRadnik

    @zdrRadnik.setter
    def zdrRadnik(self, zdrRadnik):
        self.__zdrRadnik = zdrRadnik

    @property
    def zemlja(self):
        return self.__zemlja

    @zemlja.setter
    def zemlja(self, zemlja):
        self.__zemlja = zemlja

    @property
    def gradjanin(self):
        return self.__gradjanin

    @gradjanin.setter
    def gradjanin(self, gradjanin):
        self.__gradjanin = gradjanin

    def __init__(self, datum, vakcina, zdrRadnik, zemlja, gradjanin):
        self.__datum = datum
        self.__vakcina = vakcina
        self.__zdrRadnik = zdrRadnik
        self.__zemlja = zemlja
        self.__gradjanin = gradjanin

    def __str__(self):
        format_linije = "{:>5}: {}"

        return "\n".join([
            "",
            format_linije.format("Datum", self.__datum.strftime("%d.%m.%Y. %H:%M:%S")),
            format_linije.format("Vakcina", self.__vakcina.naziv),
            format_linije.format("Zdravstveni radnik", self.__zdrRadnik.ime),
            format_linije.format("Zemlja", self.__zemlja),
            format_linije.format("Gradjanin", self.__gradjanin.ime)
        ])


class Vakcina:

    @property
    def naziv(self):
        return self.__naziv

    @naziv.setter
    def naziv(self, naziv):
        self.__naziv = naziv

    @property
    def serijskiBroj(self):
        return self.__serijskiBroj

    @serijskiBroj.setter
    def serijskiBroj(self, serijskiBroj):
        self.__serijskiBroj = serijskiBroj

    @property
    def poreklo(self):
        return self.__poreklo

    @poreklo.setter
    def poreklo(self, poreklo):
        self.__poreklo = poreklo

    @property
    def rok(self):
        return self.__rok

    @rok.setter
    def rok(self, rok):
        self.__rok = rok

    def __init__(self, naziv, serijskiBroj, poreklo, rok):
        self.__naziv = naziv
        self.__serijskiBroj = serijskiBroj
        self.__poreklo = poreklo
        self.__rok = rok

    def __str__(self):
        format_linije = "{:>5}: {}"

        return "\n".join([
            "",
            format_linije.format("Naziv", self.__naziv),
            format_linije.format("Serijski broj", self.__serijskiBroj),
            format_linije.format("Zemlja porekla", self.__poreklo),
            format_linije.format("Rok trajanja", self.__rok.strftime("%d.%m.%Y. %H:%M:%S"))
        ])


class PotvrdaOIzvrsenojVakcinaciji:

    @property
    def sifra(self):
        return self.__sifra

    @sifra.setter
    def sifra(self, sifra):
        self.__sifra = sifra

    @property
    def datum(self):
        return self.__datum

    @datum.setter
    def datum(self, datum):
        self.__datum = datum

    @property
    def doza(self):
        return self.__doza

    @doza.setter
    def doza(self, doza):
        self.__doza = doza

    @property
    def gradjanin(self):
        return self.__gradjanin

    @gradjanin.setter
    def gradjanin(self, gradjanin):
        self.__gradjanin = gradjanin

    @property
    def zdrRadnik(self):
        return self.__zdrRadnik

    @zdrRadnik.setter
    def zdrRadnik(self, zdrRadnik):
        self.__zdrRadnik = zdrRadnik

    def __init__(self, sifra, datum, doza, gradjanin, zdrRadnik):
        self.__sifra = sifra
        self.__datum = datum
        self.__doza = doza
        self.__gradjanin = gradjanin
        self.__zdrRadnik = zdrRadnik

    def __str__(self):
        format_linije = "{:>5}: {}"

        return "\n".join([
            "",
            format_linije.format("Sifra", self.__sifra),
            format_linije.format("Datum", self.__datum.strftime("%d.%m.%Y. %H:%M:%S")),
            format_linije.format("Doza", self.__doza.vakcina.naziv),
            format_linije.format("Gradjanin", self.__gradjanin.ime),
            format_linije.format("Zdravstveni radnik", self.__zdrRadnik.ime)
        ])


class DigitalniSertifikat:

    @property
    def sifra(self):
        return self.__sifra

    @sifra.setter
    def sifra(self, sifra):
        self.__sifra = sifra

    @property
    def datum(self):
        return self.__datum

    @datum.setter
    def datum(self, datum):
        self.__datum = datum

    @property
    def gradjanin(self):
        return self.__gradjanin

    @gradjanin.setter
    def gradjanin(self, gradjanin):
        self.__gradjanin = gradjanin

    def __init__(self, sifra, datum, gradjanin):
        self.__sifra = sifra
        self.__datum = datum
        self.__gradjanin = gradjanin

    def __str__(self):
        format_linije = "{:>5}: {}"

        return "\n".join([
            "",
            format_linije.format("Sifra", self.__sifra),
            format_linije.format("Datum", self.__datum.strftime("%d.%m.%Y. %H:%M:%S")),
            format_linije.format("Gradjanin", self.__gradjanin.ime)
        ])


class Podaci:

    @property
    def osobe(self):
        return self.__osobe

    @property
    def gradjani(self):
        return self.__gradjani

    @property
    def zdrRadnici(self):
        return self.__zdrRadnici

    @property
    def doze(self):
        return self.__doze

    @property
    def vakcine(self):
        return self.__vakcine

    @property
    def potvrde(self):
        return self.__potvrde

    @property
    def sertifikati(self):
        return self.__sertifikati

    def __init__(self):
        self.__osobe = []
        self.__gradjani = []
        self.__zdrRadnici = []
        self.__doze = []
        self.__vakcine = []
        self.__potvrde = []
        self.__sertifikati = []

    @classmethod
    def napravi_pocetne(cls):
        podaci = Podaci()

        osobe = podaci.osobe
        osobe.append(Osoba("1234567890123", "Petar1", "Petrovic", datetime.datetime(1991, 12, 1, 12, 22, 37), "Musko"))
        osobe.append(
            Osoba("1234567890122", "Nikolina1", "Nikolic", datetime.datetime(1994, 7, 23, 23, 54, 11), "Zensko"))
        osobe.append(Osoba("1234567890121", "Petar2", "Petrovic", datetime.datetime(1992, 12, 1, 12, 22, 37), "Musko"))
        osobe.append(
            Osoba("1234567890120", "Nikolina2", "Nikolic", datetime.datetime(1995, 7, 23, 23, 54, 11), "Zensko"))
        osobe.append(Osoba("1234567890119", "Petar3", "Petrovic", datetime.datetime(1993, 12, 1, 12, 22, 37), "Musko"))
        osobe.append(
            Osoba("1234567890118", "Nikolina3", "Nikolic", datetime.datetime(1996, 7, 23, 23, 54, 11), "Zensko"))

        gradjani = podaci.gradjani
        gradjani.append(Gradjanin(osobe[0], 1234567890, "", "", ""))
        gradjani.append(Gradjanin(osobe[2], 1234567891, "", "", ""))
        gradjani.append(Gradjanin(osobe[5], 1234567892, "", "", ""))

        zdrRadnici = podaci.zdrRadnici
        zdrRadnici.append(ZdravstveniRadnik(osobe[1], "Dom Zdravlja Novi Sad"))

        vakcine = podaci.vakcine
        vakcine.append(Vakcina("Pfizer", 1234567890, "SAD", datetime.datetime(2023, 2, 20, 14, 14, 14)))
        vakcine.append(Vakcina("Sputnik", 1234567891, "Rusija", datetime.datetime(2023, 6, 11, 15, 15, 15)))

        doze = podaci.doze
        doze.append(Doza(datetime.datetime(2021, 10, 12, 16, 16, 16), vakcine[0], zdrRadnici[0], "SAD", gradjani[0]))
        doze.append(Doza(datetime.datetime(2022, 4, 12, 17, 17, 17), vakcine[0], zdrRadnici[0], "SAD", gradjani[0]))
        doze.append(Doza(datetime.datetime(2022, 10, 12, 18, 18, 18), vakcine[1], zdrRadnici[0], "Rusija", gradjani[1]))
        gradjani[0].listaDoza.append(doze[0])
        gradjani[0].listaDoza.append(doze[1])
        gradjani[1].listaDoza.append(doze[2])

        sertifikati = podaci.sertifikati
        sertifikati.append(DigitalniSertifikat(12345678, datetime.datetime(2022, 3, 14, 13, 13, 13), gradjani[0]))
        sertifikati.append(DigitalniSertifikat(12345678, datetime.datetime(2022, 3, 14, 13, 13, 13), gradjani[0]))
        sertifikati.append(DigitalniSertifikat(12345678, datetime.datetime(2022, 3, 14, 13, 13, 13), gradjani[1]))
        gradjani[0].listaSertifikata.append(sertifikati[0])
        gradjani[0].listaSertifikata.append(sertifikati[1])
        gradjani[1].listaSertifikata.append(sertifikati[2])

        potvrde = podaci.potvrde
        potvrde.append(
            PotvrdaOIzvrsenojVakcinaciji(12345678, datetime.datetime(2021, 10, 12, 19, 19, 19), doze[0], gradjani[0],
                                         zdrRadnici[0]))
        potvrde.append(
            PotvrdaOIzvrsenojVakcinaciji(12345678, datetime.datetime(2022, 4, 12, 20, 20, 20), doze[1], gradjani[0],
                                         zdrRadnici[0]))
        potvrde.append(
            PotvrdaOIzvrsenojVakcinaciji(12345678, datetime.datetime(2022, 10, 12, 21, 21, 21), doze[2], gradjani[1],
                                         zdrRadnici[0]))
        gradjani[0].listaSertifikata.append(potvrde[0])
        gradjani[0].listaSertifikata.append(potvrde[1])
        gradjani[1].listaSertifikata.append(potvrde[2])

        return podaci

    __naziv_datoteke = "podaci_vakcinisanje"

    @classmethod
    def ucitaj(cls):
        try:
            datoteka = open(cls.__naziv_datoteke, "rb")
            podaci = pickle.load(datoteka)
            datoteka.close()
        except FileNotFoundError:
            return Podaci.napravi_pocetne()

        return podaci

    @classmethod
    def sacuvaj(cls, podaci):
        datoteka = open(cls.__naziv_datoteke, "wb")
        pickle.dump(podaci, datoteka)
        datoteka.close()
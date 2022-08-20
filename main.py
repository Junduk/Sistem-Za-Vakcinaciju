from vakcinisanje_gui import *


def test():
    podaci = Podaci.ucitaj()
    if len(podaci.osobe) == 0:
        podaci = Podaci.napravi_pocetne()

    root = GlavniProzor(podaci)
    root.mainloop()

    Podaci.sacuvaj(podaci)


if __name__ == "__main__":
    test()

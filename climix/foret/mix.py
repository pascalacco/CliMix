# -*- coding: utf-8 -*-
from climix.foret.albre import Albre

technologies_connues = ('eolienneON', 'eolienneOFF', 'panneauPV', 'methanation', 'centraleNuc', 'biomasse', 'EPR2')


class Mix(Albre):
    def __init__(self, name=None, items_calculables=technologies_connues):
        super().__init__(name=name, items_calculables=items_calculables)


if __name__ == "__main__":
    import os
    chemin = os.path.dirname(os.path.realpath(__file__)) + "/../geographe/FR_metro/"

    Eu = Mix("EU")
    Fr = Mix("FR")
    metro = Mix("metro")
    metro.from_json(chemin+"mix_init.json")
    #metro.to_json(chemin+"FR_metro_init.json")
    #metro.from_json(chemin+"FR_metro_init.json")
    #metro.to_json(chemin+"FR_metro_init.json")
    Fr &= metro
    Eu &= Fr
    print(Eu)
    #Eu.to_json(chemin+"eu_init.json")
    print(dict(Eu))
    print(Eu@["EU", "FR", "metro", "hdf"])
    loc = "FR@metro@hdf@biomasse"
    print(Eu@loc)
    Eu -= Eu
    print(Eu)
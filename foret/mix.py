# -*- coding: utf-8 -*-
from foret.albre import Albre

technologies_connues = ('eolienneON', 'eolienneOFF', 'panneauPV', 'methanation', 'centraleNuc', 'biomasse', 'EPR2')


class Mix(Albre):
    def __init__(self, name=None, items_calculables=technologies_connues):
        super().__init__(name=name, items_calculables=items_calculables)


if __name__ == "__main__":

    """
    A REVOIR car mixes albre non compatible mixes initiaux !
    """
    Eu = Mix("EU")
    Fr = Mix("FR")
    metro = Mix("metro")
    metro.from_json("flaskapp/game_data/mix_init.json")
    metro.to_json("flaskapp/game_data/fr_metro_init.json")
    metro.from_json("flaskapp/game_data/fr_metro_init.json")
    metro.to_json("flaskapp/game_data/fr_metro_init.json")
    Fr &= metro
    Eu &= Fr
    print(Eu)
    Eu.to_json("flaskapp/game_data/eu_init.json")
    print(dict(Eu))
    print(Eu@["EU", "FR", "metro", "hdf"])
    loc = "FR@metro@hdf@biomasse"
    print(Eu@loc)
    Eu -= Eu
    print(Eu)
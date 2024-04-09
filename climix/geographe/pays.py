"""
Gère les données d'un pays :
    - le nom
    - les cartes (images) à afficher
    - la décomposition en régions et leurs noms
    - le mix initial
    - les limites de production des régions
    - les scenarios de
"""
import os, json
from climix.foret.mix import Mix


class pays :
    """ Tout un pays """
    chemin = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, nom="FR_metro", chemin=None):
        self.nom = nom
        if chemin is None:
            self.chemin = pays.chemin + "/" + nom + "/"
        else:
            self.chemin = chemin

    def get_fichier(self, fichier, ext=".json"):
        with open(self.chemin + fichier + ext, "r") as f:
            obj = json.load(f)
            return obj

    def get_mix_init(self):
        mix_init = Mix(self.nom)
        mix_init.from_json(self.chemin+self.nom+"_init.json")
        return mix_init


FR_metro = pays()

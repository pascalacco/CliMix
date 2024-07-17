# -*- coding: utf-8 -*-
import json


class Albre(dict):
    """Albre = ALgèbre d'arBREs

    Arbres sous forme de dict avec des opérateurs algébriques + -
    applicable à des feuilles de type "calculables"

    La forme dict permet de sauver/importer au format json l'arbre de manière lisible....

    """
    NOEUD = "Noeud"
    RACINE = "Racine"
    FEUILLE = "Feuille"
    NOM = "Nom"

    JSON_OPTS = {"indent": 4, "sort_keys": False, "ensure_ascii": False}

    def __init__(self, name=None, items_calculables=[]):
        super().__init__()
        self._TYPE = self.__class__.__name__
        self._PAS_MON_TYPE = "Pas_"+self._TYPE
        self.update({self._TYPE: Albre.RACINE})
        self.update({Albre.NOM: name})
        self.update({self._PAS_MON_TYPE: {}})
        self.calculables = items_calculables

    def est_calculable(self, key):
        return key in self.calculables

    @property
    def est_noeud(self):
        return self[self._TYPE] == Albre.NOEUD

    @property
    def est_feuille(self):
        return self[self._TYPE] == Albre.FEUILLE

    @property
    def nom(self):
        return self[Albre.NOM]

    @nom.setter
    def nom(self, nom):
        self[Albre.NOM] = nom

    def iter_arbres(self, keys=[]):
        yield keys, self
        if self.est_noeud:
            for nom_fils, arbre_fils in self.items():
                if Albre.NOM in arbre_fils:
                    yield from arbre_fils.iter_arbres([*keys, nom_fils])

    def from_dict(self, dico, racine=None):
        succes = False

        for key, value in dico.items():
            if key == Albre.NOM:
                self.update({Albre.NOM: value})
            elif key == self._PAS_MON_TYPE:
                self[self._PAS_MON_TYPE].update(value)
            elif key == self._TYPE:
                if not racine:
                    self[self._TYPE] = Albre.RACINE
                else:
                    self[self._TYPE] = racine
            elif self.est_calculable(key):
                self.update({key: value})
                self.update({self._TYPE: Albre.FEUILLE})
                succes = True
            elif type(value) is dict:
                composite = self.__class__(key)
                if composite.from_dict(value, racine=Albre.NOEUD):
                    self.update({key: composite})
                    if self.est_feuille:
                        self[self._TYPE] = Albre.NOEUD
                    succes = True
                else:
                    self[self._PAS_MON_TYPE].update({key: value})
            else:
                self[self._PAS_MON_TYPE].update({key: value})

        return succes

    def from_json(self, fichier):
        with open(fichier, "r") as f:
            prearbre = json.load(f)

        return self.from_dict(prearbre)

    def to_json(self, fichier, dump_non_arbre=True):
        dico = dict(self)
        if dump_non_arbre:
            dico.pop(self._PAS_MON_TYPE)
        with open(fichier, "w") as f:
            json.dump(dico, f, **self.JSON_OPTS)

    def __matmul__(self, noms):
        if not isinstance(noms, list):
            noms = noms.split("@")
        nom = noms[0]

        arbre = None
        for keys, un_arbre in self.iter_arbres():
            if un_arbre.nom == nom:
                arbre = un_arbre
                break

        if arbre is not None:
            for nom in noms[1:]:
                arbre = arbre[nom]
        return arbre

    def __iand__(self, b):
        name = b.nom
        if self.est_feuille:
            self[self._TYPE] = Albre.NOEUD

        if b[self._TYPE] == Albre.RACINE:
            b[self._TYPE] = Albre.NOEUD
        self.update({name: b})
        return self

    def __isub__(self, b):
        arbre = self @ b.nom
        for un_nom, un_arbre in arbre.iter_arbres():
            if un_arbre.est_feuille:
                for key, value in un_arbre.items():
                    if self.est_calculable(key):
                        un_arbre -= (b@un_nom)[key]

    def __str__(self):
        if self.est_feuille:
            str = Albre.FEUILLE + " : " + self.nom + "\n"
        else:
            str = Albre.NOEUD + " : \n"
            line = ""
            for keys, arbre in self.iter_arbres():
                if not keys:
                    nom = arbre.nom
                else:
                    nom = keys[-1]

                if arbre.est_feuille:

                    str += line + "___" + nom + "\n"
                    line = " " * (len(line) - 1) + "|"
                else:
                    line += "|" + nom + "|=="

        return str

    def __repr__(self):
        return self[self._TYPE] + " " + self.nom


class tree(Albre):
    def __init__(self, name=None, items_calculables=['eolienneON', 'eolienneOFF', 'panneauPV', 'methanation', 'centraleNuc', 'biomasse', 'EPR2']):
        super().__init__(name=name, items_calculables=items_calculables)


if __name__ == "__main__":
    technologies = ['eolienneON', 'eolienneOFF', 'panneauPV', 'methanation', 'centraleNuc', 'biomasse', 'EPR2']

    Eu = tree("EU")
    print(Eu)
    Fr = tree("FR")
    metro = tree("metro")
    metro.from_json("flaskapp/game_data/mix_init.json")
    metro.to_json("flaskapp/game_data/fr_metro_init.json")
    metro.from_json("flaskapp/game_data/fr_metro_init.json")
    Fr &= metro
    Eu &= Fr
    print(Eu)
    Eu.to_json("flaskapp/game_data/eu_init.json")
    print(dict(Eu))
    print(Eu @ ["EU", "FR", "metro", "hdf"])
    loc = "FR@metro@hdf@biomasse"
    print(Eu @ loc)
    Eu -= Eu
    print(Eu)
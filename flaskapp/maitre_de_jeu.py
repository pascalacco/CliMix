import os
import pandas as pd

from climix import stratege
import random

ceChemin = os.path.dirname(os.path.realpath(__file__)) + '/'
chemin_scenarios = ceChemin + "../climix/mix_data/"
#########################
### TOUT EST EN GW(h) ###
#########################

aleas = ["", "MEGC1", "MEGC2", "MEGC3", "MEMFDC1", "MEMFDC2", "MEMFDC3",
         "MECS1", "MECS2", "MECS3", "MEVUAPV1", "MEVUAPV2", "MEVUAPV3",
         "MEMDA1", "MEMDA2", "MEMDA3", "MEMP1", "MEMP2", "MEMP3",
         "MEGDT1", "MEGDT2", "MEGDT3"];

reg_convert = {
    "hdf": "Hauts-de-France",
    "bre": "Bretagne",
    "nor": "Normandie",
    "idf": "Ile-de-France",
    "est": "Grand Est",
    "cvl": "Centre-Val de Loire",
    "pll": "Pays de la Loire",
    "bfc": "Bourgogne-Franche-Comté",
    "naq": "Nouvelle-Aquitaine",
    "ara": "Auvergne-Rhône-Alpes",
    "occ": "Occitanie",
    "pac": "Provence-Alpes-Côte d'Azur",
    "cor": "Corse"
}

pion_convert = {
    "eolienneON": "Eoliennes on.",
    "eolienneOFF": "Eoliennes off.",
    "panneauPV": "Panneaux PV",
    "centraleNuc": "Ancien nuc.",
    "EPR2": "EPR 2",
    "methanation": "Méthanation",
    "biomasse": "Biomasse"
}


class errJeu(Exception):
    pass


def initialise_partie(dm):
    dm.init_partie()


def nouveau_mix(annee, mix, alea=random.choice(aleas)):
    nmix = mix.copy()
    nmix["annee"] = annee
    nmix["actif"] = True
    nmix["alea"] = alea
    nmix["capacites"] = nouv_capacite_alea(nmix, nmix['alea'])
    nmix["nb"] = calculer_nb(mix)
    nmix["actions"] = get_actions(nmix)
    return nmix


def recup_mix(dm, annee):
    mixes = dm.get_fichier("mixes")
    if annee in mixes:
        mix = mixes[annee]
    else:
        annee_precedente = (int(annee) - 5).__str__()
        if annee_precedente in mixes:
            mix = mixes[annee_precedente]
            if not mix["actif"]:
                mix = nouveau_mix(annee, mix)
                mixes[annee] = mix
                dm.set_fichier("mixes", mixes)
        else:
            raise Exception(
                "Accès au mix de l'année " + annee + " alors que l'année " + annee_precedente + " n'existe pas : ")
    return mix


def nouv_capacite_alea(mix, alea):
    capmax_info = mix["capacites"]
    # carte alea MECS (lance 1 / 2)
    if alea == "MECS1" or alea == "MECS2" or alea == "MECS3":
        for k in capmax_info:
            capmax_info[k]["eolienneON"] = int(capmax_info[k]["eolienneON"] * 0.4)

    if alea == "MECS2" or alea == "MECS3":
        capmax_info["occ"]["eolienneON"] *= 2
        capmax_info["occ"]["panneauPV"] *= 2

    # carte alea MEGDT (lance 2)
    if alea == "MEGDT2" or alea == "MEGDT3":
        capmax_info["naq"]["eolienneOFF"] += 1
        capmax_info["pac"]["eolienneOFF"] += 1
    return capmax_info


def get_actions(mix):
    replace_dict = {}
    annee = mix["annee"]
    annee_int = int(annee)
    for reg in mix["unites"]:
        replace_dict[reg] = {}
        for p in mix["unites"][reg]:
            replace_dict[reg][p] = {}

            nb = mix["nb"][reg][p]
            if p == "centraleNuc":
                duree = 40
                cap = 0
            elif p == "EPR2":
                duree = 40
                cap = 20 - nb
            elif p == "methanation":
                duree = 100
                cap = 40 - nb
            elif p == "eolienneON" or p == "eolienneOFF":
                duree = 15
                cap = mix["capacites"][reg][p] - nb
            else:
                duree = 100
                cap = mix["capacites"][reg][p] - nb

            for an in mix["unites"][reg][p]:
                if int(an) == annee_int - duree:
                    cap_fin_de_vie = min(0, cap)
                    replace_dict[reg][p][an] = {"action": "?",
                                                "valeur": "",
                                                "min": -mix["unites"][reg][p][an],
                                                "max": cap_fin_de_vie,
                                                "forcee": True,
                                                "date": annee}
                    cap -= cap_fin_de_vie

            if cap > 0:
                replace_dict[reg][p][annee] = {"action": "=",
                                               "valeur": "",
                                               "min": 0,
                                               "max": cap,
                                               "forcee": False,
                                               "date": annee}

    actions = {"alea":  {'actuel': mix["alea"], 'action': False},
               "stock": {'actuel': mix["stock"], 'nouv': mix["stock"]},
               "regions": replace_dict}

    return actions


def appliquer(actions, mix):
    new = mix.copy()

    if actions["alea"]['nouv'] != actions["alea"]['actuel']:
        actions["alea"]['action'] = True
        raise errJeu(f"Changement de l'aléa : Attendez 5 secondes que la page se recharge et refaites votre mix...")

    if actions["stock"]['nouv'] > actions["stock"]['actuel']:
        new['stock'] = actions["stock"]['nouv']
        actions["stock"]["action"] = actions["stock"]['nouv'] - actions["stock"]['actuel']

    elif actions["stock"]['nouv'] < actions["stock"]['actuel']:
        raise errJeu(f"On ne peut pas réduire le stock de batteries de {actions['stock']['actuel']} à {actions['stock']['nouv']} ! C'est gâcher")

    unites = {}
    for reg, region in actions["regions"].items():
        unites[reg] = {}
        for p, pion in region.items():
            unites[reg][p] = mix["unites"][reg][p].copy()
            for an, act in pion.items():
                if act["action"] == "?":
                    raise errJeu(f"Il faut décider pour la fin de vie de {p} en {reg} svp")
                if act["action"] == "-":
                    nb_vieux = new["unites"][reg][p][an]
                    act['nb_demanteles'] = -int(act['valeur'])
                    act['nb_renouveles'] = nb_vieux - act['nb_demanteles']
                    if act['date'] in new["unites"][reg][p]:
                        unites[reg][p][act['date']] += act['nb_renouveles']
                    elif act['nb_renouveles'] > 0:
                        unites[reg][p][act['date']] = act['nb_renouveles']
                    unites[reg][p].pop(an)
                if act["action"] == "+":
                    if an in new["unites"][reg][p]:
                        unites[reg][p][an] += act['valeur']
                    else:
                        unites[reg][p][an] = act['valeur']
    new['unites'] = unites
    new["nb"] = calculer_nb(new)
    new["actions"] = actions
    return new


def appliquer_a_dict(dico, fonc):
    res = {}
    for reg, region in dico.items():
        res[reg] = {}
        for p, pion in region.items():
            res[reg][p] = fonc(pion)
    return res


def sommer_dict(dico):
    new = dico.copy()
    for p in dico[next(iter(dico))]:
        new[p] = 0
    for reg, region in dico.items():
        for p, pion in region.items():
            new[p] += pion
    return new


def calculer_nb(mix):
    nb = appliquer_a_dict(dico=mix["unites"], fonc=lambda pion: sum(pion.values()))
    nb = sommer_dict(nb)
    return nb


def calculer(dm, annee, actions, scenario):
    try:
        mix = recup_mix(annee=annee, dm=dm)
        new = appliquer(actions, mix)
        dm.set_fichier(fichier="new", dico=new)
        mix["actions"] = actions
        mix["nb"] = new["nb"]
        dm.set_item_fichier(fichier='mixes', item=annee, val=mix)

        df = pd.read_hdf(chemin_scenarios + scenario + "_25-50.h5", "df")
        annee_en_cours = (mix['annee']).__str__()

        df = df.loc[annee_en_cours + "-1-1 0:0": annee_en_cours + "-12-31 23:0"]
        result, chroniques = stratege.simuler(demande=df["demande"].values,
                                              electrolyse=df["electrolyse"].values,
                                              mix=mix,
                                              nb=mix["nb"])

        chroniques["date"] = df.index.values
        dm.set_chroniques(chroniques)
        dm.set_item_fichier(fichier='resultats', item=annee, val=result)
        resp = ["success"]

    except errJeu as ex:
        if actions['alea']['action']:
            oldmix = recup_mix(annee=(int(annee)-5).__str__(), dm=dm)
            new = nouveau_mix(annee=annee, mix=oldmix, alea=actions["alea"]['nouv'])

            dm.set_item_fichier(fichier='mixes', item=annee, val=new)
            resp = ["aleaChangement", ex.__str__()]
        else:
            resp = ["errJeu", ex.__str__()]

    return resp


def check_max_pions(capmax_info, nbPions):
    for k in capmax_info:
        if (nbPions["eolienneON"] > capmax_info[k]["eolienneON"]
                or nbPions["eolienneOFF"] > capmax_info[k]["eolienneOFF"]
                or nbPions["panneauPV"] > capmax_info[k]["panneauPV"] - 11 * nbPions["eolienneON"]
                or nbPions["biomasse"] > capmax_info[k]["biomasse"] - 33 * nbPions["eolienneON"] - 3 * nbPions[
                    "panneauPV"]):
            pass
            # AVERTISSEMENT


def strat_stockage_main(mix, save, nbPions, nvPions, nvPionsReg, scenario):
    """Fonction principale

        Args:
            mix (dict) : donnees du plateau
            save (dict) : donnees du tour precedent
            nbPions (dict) : nombre de pions total pour chaque techno
            nvPions (dict) : nombre de nouveaux pions total pour chaque techno ce tour-ci
            nvPionsReg (dict) : nombre de pions total pour chaque techno
            df (string) : nom du scenario (fichier <scenario>_25-50.csv  de mix_data)

        Returns:
            result (dict) : tous les résultat de l'année

        Infos sur les unites de data :
            * eolienneON --> 1 unite = 10 parcs = 700 eoliennes
            * eolienneOFF --> 1 unite = 5 parcs = 400 eoliennes
            * panneauPV --> 1 unite = 10 parcs = 983 500 modules
            * centraleTherm --> 1 unite = 1 centrale
            * centraleNuc --> 1 unite = 1 reacteur
            * biomasse --> 1 unite = une fraction de flux E/S en methanation
    """

    df = pd.read_hdf(chemin_scenarios + scenario + "_25-50.h5", "df")
    annee_en_cours = (mix['annee']).__str__()

    df = df.loc[annee_en_cours + "-1-1 0:0": annee_en_cours + "-12-31 23:0"]
    result, save, chroniques = stratege.simulation(df["demande"].values, mix, save, nbPions, nvPions, nvPionsReg,
                                                   electrolyse=df["electrolyse"].values)

    chroniques["date"] = df.index.values
    return result, save, chroniques


def inputs_from_save_and_data(save, data):
    """calcule les arguments de main stratcockage

        Args:
            save (dict) : donnees saisies précédemment
            data (dict) : donnees du mix saisie en cours

        Returns:
            mix: data,
            save: save,
            nbPions: nbPions,
            nvPions: nvPions,
            nvPionsReg: nvPionsReg


    """

    save["carte"] = data["carte"]
    save["annee"] += 5
    save["stock"] = data["stock"]

    """

    if data["annee"] == 2030:
        save["hdf"]["centraleNuc"][0:6] = [1995, 1995, 1995, 1995, 1995, 1995]
        save["occ"]["centraleNuc"][0:2] = [2020, 2020]
        save["naq"]["centraleNuc"][0:6] = [1995, 1995, 1995, 1995, 2000, 2000]
        save["pac"]["centraleNuc"][0:8] = [2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000]
        save["cvl"]["centraleNuc"][0:7] = [2005, 2005, 2005, 2005, 2005, 2005, 2005]
        save["bfc"]["centraleNuc"][0:2] = [2005, 2005]
        save["est"]["centraleNuc"][0:5] = [2005, 2010, 2010, 2010, 2010]
        save["ara"]["centraleNuc"][0:3] = [2010, 2010, 2010]
        save["nor"]["centraleNuc"][0:8] = [2010, 2010, 2010, 2020, 2020, 2020, 2020, 2020]
    """
    # CALCUL NOMBRE DE NOUVEAU PIONS + TOTAL A CE TOUR
    nvPionsReg = {
        "hdf": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "idf": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "est": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "nor": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "occ": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "pac": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "bre": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "cvl": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "pll": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "naq": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "ara": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "bfc": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "cor": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0}
    }

    nvPions = {
        "eolienneON": 0,
        "eolienneOFF": 0,
        "panneauPV": 0,
        "methanation": 0,
        "EPR2": 0,
        "biomasse": 0
    }

    nbPions = {
        "eolienneON": 0,
        "eolienneOFF": 0,
        "panneauPV": 0,
        "methanation": 0,
        "centraleNuc": 0,
        "EPR2": 0,
        "biomasse": 0
    }

    for reg in save["capacite"]:
        nbPions["centraleNuc"] += data[reg]["centraleNuc"]
    if data["annee"] == 2030 and nbPions["centraleNuc"] != 47:
        raise errJeu(
            "Votre mix ne correspond pas au mix initial imposé. Veuillez vérifier le nombre de réacteurs dans chaque région.")
    else:
        nbPions["centraleNuc"] = 0

    for reg in save["capacite"]:
        for p in data[reg]:
            nbPions[p] += data[reg][p]

            if p == "eolienneON" or p == "eolienneOFF":
                eolSuppr = len(save[reg][p]) - data[reg][p]
                for i in range(eolSuppr):
                    if data["annee"] in save[reg][p]:
                        save[reg][p].remove(data["annee"])
                    elif data["annee"] - 15 in save[reg][p]:
                        save[reg][p].remove(data["annee"] - 15)
                    else:
                        raise errJeu(
                            f"On ne peut pas enlever {eolSuppr} jeunes {p} en {reg} leur age est {save[reg][p]}<br> Remetez {len(save[reg][p])} pions svp")

            if p != "centraleNuc":
                nvPionsReg[reg][p] = data[reg][p] - len(save[reg][p])
                nvPions[p] += data[reg][p] - len(save[reg][p])

                for i in range(nvPionsReg[reg][p]):
                    save[reg][p].append(data["annee"])
            else:
                nucSuppr = len(save[reg][p]) - data[reg][p]
                if nucSuppr < 0:
                    raise errJeu(
                        f"Impossible de créer {-nucSuppr} centrales nucléaires d'ancienne génération dans la région {reg}! Choisissez des EPR2 à la place.")
                for i in range(nucSuppr):
                    if (data["annee"] - 40) in save[reg][p]:
                        save[reg][p].remove(data["annee"] - 40)
                    else:
                        raise errJeu(
                            f"On ne peut pas enlever {eolSuppr} jeunes {p} en {reg} leur age est {save[reg][p]}<br> Remetez {len(save[reg][p])} pions svp")

    if data["alea"] == "MECS3":
        if nvPions["EPR2"] > 0:
            raise errJeu(
                f'La crise sociale en cours vous empêche de placer plus de réacteurs nucléaires (vous en avez ajouté {nvPions["EPR2"]}).')
    return {"mix": data, "save": save, "nbPions": nbPions, "nvPions": nvPions, "nvPionsReg": nvPionsReg}


def assert_capacitees(save, data):
    reponse = None
    nvPionsReg = {}
    # VERIF ANNEE / STOCK / CARTE / CAPACITE LEGITIMES
    if data["annee"] != save["annee"]:
        raise errJeu(
            "L'année sélectionnée ne correpond pas au tour actuel (valeur attendue:" + save["annee"].__str__() + ").")

    if data["stock"] < save["stock"]:
        raise errJeu(f'Vous ne pouvez pas enlever de batteries (valeur minimale: {save["stock"]}).')

    if (data["annee"] != 2030) and (data["carte"] != save["carte"]):
        raise errJeu(f'Vous ne pouvez pas changer de carte au milieu d''une partie (carte actuelle: {save["carte"]}).')

    for reg in save["capacite"]:
        nvPionsReg[reg] = {}
        for p in save["capacite"][reg]:
            # if p != "biomasse":
            surplus = data[reg][p] - save["capacite"][reg][p]
            nvPionsReg[reg][p] = data[reg][p].count(save["annee"])
            if (surplus > 0) and (nvPionsReg[reg][p]) > 0:
                raise errJeu(f'Vous avez placé trop de {p} en {reg} (maximum: {save["capacite"][reg][p]}).')
    return nvPionsReg


def applique_politique(code_pol, save, scenario):
    """Applique les choix politiques à la consommation

        Args :
            mix(dict) : mix initial
            save(dict) : mix à calculer


        Returns :
            save(dcit) : mix avec conso modifiée
    """
    ##Carte Choix politique --> 1 choix politique parmi les 3 proposes

    # Carte politique A

    if code_pol == "CPA1":
        save["varConso"] -= 1e4
    if code_pol == "CPA2":
        save["varConso"] -= 6e3

    # Carte politique B
    if code_pol == "CPB1":
        save["varConso"] += 4.92e3

    # Carte politique C
    if code_pol == "CPC1":
        save["varConso"] -= 2e4
    if code_pol == "CPC2":
        save["varConso"] -= 6.3e4

    # Carte politique D
    if code_pol == "CPD1":
        save["varConso"] += 6.8e4
    if code_pol == "CPD2":
        save["varConso"] -= 1e4

    # Carte politique E
    if code_pol == "CPE1":
        save["varConso"] += 1.03e5
    if code_pol == "CPE2":
        save["varConso"] += 6.7e4

    # Carte politique F
    if code_pol == "CPF1":
        save["varConso"] -= 3.5e4
    if code_pol == "CPF2":
        save["varConso"] -= 1.3e4

    import numpy as np
    from climix.stratege import H
    scenario += np.ones(H) * (save["varConso"] / H)

    return save, scenario

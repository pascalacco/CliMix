import pandas as pd

import stratege
import numpy as np
from flaskapp.constantes import *


                                #########################
                                ### TOUT EST EN GW(h) ###
                                #########################


class errJeu(Exception):
    pass




def strat_stockage_main(mix, save, nbPions, nvPions, nvPionsReg, scenario):
    """Fonction principale

        Args:
            mix (dict) : donnees du plateau
            save (dict) : donnees du tour precedent
            nbPions (dict) : nombre de pions total pour chaque techno
            nvPions (dict) : nombre de nouveaux pions total pour chaque techno ce tour-ci
            nvPionsReg (dict) : nombre de pions total pour chaque techno
            scenario (string) : nom du scenario (fichier <scenario>_25-50.csv  de mix_data)

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

    # Definition des scenarios (Negawatt, ADEME, RTE pour 2050)
    # Les autres scenarios sont faits mains à partir des donnees de Quirion

    # ADEME = pd.read_csv(dataPath+"mix_data/ADEME_25-50.csv", header=None)
    # ADEME.columns = ["heures", "d2050", "d2045", "d2040", "d2035", "d2030", "d2025"]

    scenario = pd.read_csv(dataPath + "mix_data/" + scenario + "_25-50.csv")
    # scenario.columns = ["heures", "d2050", "d2045", "d2040", "d2035", "d2030", "d2025"]

    # # RTE = pd.read_csv(dataPath+"mix_data/RTE_25-50.csv", header=None)
    # # RTE.columns = ["heures", "d2050", "d2045", "d2040", "d2035", "d2030", "d2025"]

    # # NEGAWATT = pd.read_csv(dataPath+"mix_data/NEGAWATT_25-50.csv", header=None)
    # # NEGAWATT.columns = ["heures", "d2050", "d2045", "d2040", "d2035", "d2030", "d2025"]

    annee_en_cours = (mix['annee'] - 5).__str__()
    if ("e" + annee_en_cours) in scenario:
        electrolyse = scenario["e" + annee_en_cours].values
    else:
        electrolyse = scenario["heures"].values * 0.



    result, save, chroniques = stratege.simulation(scenario["d" + annee_en_cours].values, mix, save, nbPions, nvPions, nvPionsReg,
                              electrolyse=electrolyse)

    chroniques['heures']= scenario["heures"]
    return result, save, chroniques


def inputs_from_save_and_data(save, mix):
    """calcule les arguments de main stratcockage

        Args:
            save (dict) : donnees saisies précédemment
            mix (dict) : donnees du mix saisie en cours

        Returns:
            mix: data,
            save: save,
            nbPions: nbPions,
            nvPions: nvPions,
            nvPionsReg: nvPionsReg


    """

    save["carte"] = mix["carte"]
    save["annee"] += 5
    save["stock"] = mix["stock"]





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
        nbPions["centraleNuc"] += mix[reg]["centraleNuc"]
    if mix["annee"] == 2030 and nbPions["centraleNuc"] != 47:
        raise errJeu(
            "Votre mix ne correspond pas au mix initial imposé. Veuillez vérifier le nombre de réacteurs dans chaque région.")
    else:
        nbPions["centraleNuc"] = 0

    for reg in save["capacite"]:
        for p in mix[reg]:
            nbPions[p] += mix[reg][p]

            if p == "eolienneON" or p == "eolienneOFF":
                eolSuppr = len(save[reg][p]) - mix[reg][p]
                for i in range(eolSuppr):
                    save[reg][p].remove(mix["annee"] - 15)

            if p != "centraleNuc":
                nvPionsReg[reg][p] = mix[reg][p] - len(save[reg][p])
                nvPions[p] += mix[reg][p] - len(save[reg][p])

                for i in range(nvPionsReg[reg][p]):
                    save[reg][p].append(mix["annee"])
            else:
                nucSuppr = len(save[reg][p]) - mix[reg][p]
                if nucSuppr < 0 :
                    raise errJeu(f"Impossible de créer {-nucSuppr} centrales nucléaires d'ancienne génération dans la région {reg}! Choisissez des EPR2 à la place.")
                for i in range(nucSuppr):
                    save[reg][p].remove(mix["annee"] - 40)

    if mix["alea"] == "MECS3":
        if nvPions["EPR2"] > 0:
            raise errJeu(
                f'La crise sociale en cours vous empêche de placer plus de réacteurs nucléaires (vous en avez ajouté {nvPions["EPR2"]}).')
    return {"mix": mix, "save": save, "nbPions": nbPions, "nvPions": nvPions, "nvPionsReg": nvPionsReg}


def assert_capacitees(save, data):
    reponse = None

    # VERIF ANNEE / STOCK / CARTE / CAPACITE LEGITIMES
    if data["annee"] != save["annee"]:
        raise errJeu(
            "L'année sélectionnée ne correpond pas au tour actuel (valeur attendue:" + save["annee"].__str__() + ").")

    if data["stock"] < save["stock"]:
        raise errJeu(f'Vous ne pouvez pas enlever de batteries (valeur minimale: {save["stock"]}).')

    if (data["annee"] != 2030) and (data["carte"] != save["carte"]):
        raise errJeu(f'Vous ne pouvez pas changer de carte au milieu d''une partie (carte actuelle: {save["carte"]}).')

    for reg in save["capacite"]:
        for p in save["capacite"][reg]:
            # if p != "biomasse":
            if data[reg][p] > save["capacite"][reg][p]:
                errDetails = [reg, p, save["capacite"][reg][p]]
                raise errJeu(f'Vous avez placé trop de {p} en {reg} (maximum: {save["capacite"][reg][p]}).')


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
    from stratege import H
    scenario += np.ones(H)*(save["varConso"]/H)

    return save, scenario



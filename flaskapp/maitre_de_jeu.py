import os
import pandas as pd

from climix import stratege, technologies
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
                    act['nb_nouvelles'] = act['valeur']

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
        chroniques, prod_renouvelables, puissances = stratege.simuler(demande=df["demande"].values,
                                              electrolyse=df["electrolyse"].values,
                                              mix=mix,
                                              nb=mix["nb"])

        result = calculer_resultats(mix, actions, chroniques, prod_renouvelables, puissances)
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


def calculer_resultats(mix, actions, chroniques, prod_renouvelables, puissances ):
    result = {}
    annuel = {item: sum(val) for item, val in chroniques.items()}
    renouv = appliquer_a_dict(actions['regions'], lambda dic: sum([act['nb_renouveles'] for an,act in dic.items() if 'nb_renouveles' in act]))
    nouv = appliquer_a_dict(actions['regions'], lambda dic: sum([act['nb_nouvelles'] for an, act in dic.items() if 'nb_nouvelles' in act]))
    renouv = sommer_dict(renouv)
    nouv = sommer_dict(nouv)

    result = result_prod_region(mix, annuel, chroniques, prod_renouvelables, puissances)
    result.update(result_couts(actions, annuel, renouv, nouv))

    # result.update(result_ressources(mix, save, nbPions, nvPions))
    return result

def result_couts(actions, annuel, renouv, nouv):
    prixGaz = 324.6e-6  # prix de l'electricite produite à partir du gaz/charbon --> moyenne des deux (35€ le MWh)
    prixNuc = 7.6e-6  # part du combustible dans le prix de l'electricite nucleaire (7.6€ le MWh)

    # carte alea MEGC (lance 1 / 3)
    if actions['alea']['actuel'] == "MEGC1" or actions['alea']['actuel'] == "MEGC2" or actions['alea']['actuel'] == "MEGC3":
        prixGaz *= 1.5  # alea1

    if actions['alea']['actuel'] == "MEGC3":
        prixNuc *= 1.4  # alea3

    # carte alea MEMP (lance 3)
    if actions['alea']['actuel'] == "MEMP3":
        prixGaz *= 1.3
        prixNuc *= 1.2



    cout = ((nouv["eolienneON"] + renouv["eolienneON"]) * 3.5 +
            (nouv["eolienneOFF"] + renouv["eolienneOFF"]) * 6 +
            nouv["panneauPV"] * 3.6 +
            nouv["EPR2"] * 8.6 +
            renouv["centraleNuc"] * 2 +
            nouv["biomasse"] * 0.12 +
            nouv["methanation"] * 4.85 +
            (actions['stock']['actuel']*0.8) +    # formule BIZARE  (B.PoutMax * 0.0012) / 0.003
            (annuel['Nprod'] * prixNuc) +
            (annuel['Gprod'] * prixGaz))
    # (S.PoutMax * 0.455) / 0.91 +

    #formule BIZARE
    #if mix["annee"] != 2030:
    #    cout += (10 - renouv["centraleNuc"]) * 0.5

    # budget à chaque tour sauf si carte evènement bouleverse les choses
    budget = 70

    # carte alea MEVUAPV : lance 3
    if actions['alea']['actuel'] == "MEVUAPV3":
        budget -= 10

    # carte MEMDA : lance 1 / 2
    if actions['alea']['actuel'] == "MEMDA1" or actions['alea']['actuel'] == "MEMDA2" or actions['alea']['actuel'] == "MEMDA3":
        budget += 3.11625   #BIZARE

    if actions['alea']['actuel'] == "MEMDA2" or actions['alea']['actuel'] == "MEMDA3":
        cout -= 1.445  #BIZARE

    # carte MEGDT : lance 1 / 3
    if actions['alea']['actuel'] == "MEGDT1" or actions['alea']['actuel'] == "MEGDT2" or actions['alea']['actuel'] == "MEGDT3":
        cout += 1. / 3. * nouv["pac"]["panneauPV"] * 3.6

    if actions['alea']['actuel'] == "MEGDT3":
        # cout += nouv["pll"]["eolienneOFF"]*1.2
        # d'après le rapport de stage, un pion d'éolienneOFF devrait coûter 6 Mds et non 1.2 Mds
        cout += nouv["pll"]["eolienneOFF"] * 6

    result = {"cout": round(cout),
              "budget": round(budget),
              }

    return result


def result_prod_region(mix, annuel, chroniques, prod_renouvelables, puissances):

    prodOn = int(annuel["prodOnshore"])
    prodOff = int(annuel["prodOffshore"])
    prodPv = int(annuel["prodPV"])
    prodEau = int(annuel["Lprod"] + annuel["rivprod"])
    prodNuc = int(annuel["Nprod"])
    prodGaz = int(annuel["Gprod"])
    prodPhs = int(annuel["Sprod"])
    prodBat = int(annuel["Bprod"])



    prodTotale = prodOn + prodOff + prodPv+ prodEau + prodNuc + prodGaz + prodPhs + prodBat

    gazBiomasse = mix['nb']["biomasse"] * 2 * 0.1 * 0.71 * stratege.H
    #  gaz =        nbPions      * nbCentraleParPion * puissance * fdc * nbHeures

    # note Hugo : il semble que cet effet soit mal implémenté : à tester
    # carte alea MEMFDC (lance 2 / 3)
    # un an de moins de biomasse en nouvelle aquitaine (impact sur cette année)
    if mix["alea"] == "MEMFDC2":
        gazBiomasse -= mix['nb']["naq"]["biomasse"] * 2. * 0.1 * 0.71 *  stratege.H

    s=chroniques["s"]
    p=chroniques["p"]

    nbS = 0
    nbP = 0

    listeSurplusQuotidien = [0] * 365
    listeSurplusHoraire = [0] * 24

    listePenuriesQuotidien = [0] * 365
    listePenuriesHoraire = [0] * 24

    for i in range(len(s)):
        if s[i] > 0:
            nbS += 1
            listeSurplusQuotidien[i // 24] += 1
            listeSurplusHoraire[i % 24] += 1
        if p[i] > 0:
            nbP += 1
            listePenuriesQuotidien[i // 24] += 1
            listePenuriesHoraire[i % 24] += 1

    consoGaz = (chroniques['Gstored'][0] - chroniques['Gstored'][-1]) * technologies.TechnoGaz.etaout
    prodGazFossile = consoGaz - gazBiomasse - annuel["electrolyse"]
    if prodGazFossile < 0.:
        prodGazFossile = 0.


    EmissionCO2 = prodOn * 10 + prodOff * 9 + prodPv * 55 + prodEau * 10 + prodNuc * 6 + prodGazFossile * 443  # variable EmissionCO2


    demane_annuelle = annuel["demande"]  # variable demande


    # calcul des productions par region


    # Puissance d'un pion
    powOnshore = 1.4
    powOffshore = 2.4
    powPV = 3

    nbTherm = 20
    nbThermReg = {
        "hdf": 0,
        "idf": 0,
        "est": 0,
        "nor": 0,
        "occ": 0,
        "pac": 0,
        "bre": 0,
        "cvl": 0,
        "pll": 0,
        "naq": 0,
        "ara": 0,
        "bfc": 0,
        "cor": 0
    }

    factNuc = 0 if (mix['nb']['EPR2'] + mix['nb']['centraleNuc'] == 0) else prodNuc / (mix['nb']['EPR2'] + mix['nb']['centraleNuc'])

    """

    ##Occitanie
    popOCC = 0.09  ##pourcentage population
    prodOCC = (np.array(fdc_off.occ) * mix["occ"]["eolienneOFF"] * powOffshore +
               np.array(fdc_on.occ) * mix["occ"]["eolienneON"] * powOnshore +
               np.array(fdc_pv.occ) * mix["occ"]["panneauPV"] * powPV +
               (mix["occ"]["EPR2"] - nvPionsReg["occ"]["EPR2"] + mix["occ"]["centraleNuc"]) * factNuc +
               nbThermReg["occ"] * prodGaz / nbTherm)

    ##Nouvelle-Aquitaine
    popNA = 0.09
    prodNA = (np.array(fdc_off.naq) * mix["naq"]["eolienneOFF"] * powOffshore +
              np.array(fdc_on.naq) * mix["naq"]["eolienneON"] * powOnshore +
              np.array(fdc_pv.naq) * mix["naq"]["panneauPV"] * powPV +
              (mix["naq"]["EPR2"] - nvPionsReg["naq"]["EPR2"] + mix["naq"]["centraleNuc"]) * factNuc +
              nbThermReg["naq"] * prodGaz / nbTherm)

    ##Bretagne
    popBRE = 0.05
    prodBRE = (np.array(fdc_off.bre) * mix["bre"]["eolienneOFF"] * powOffshore +
               np.array(fdc_on.bre) * mix["bre"]["eolienneON"] * powOnshore +
               np.array(fdc_pv.bre) * mix["bre"]["panneauPV"] * powPV +
               (mix["bre"]["EPR2"] - nvPionsReg["bre"]["EPR2"] + mix["bre"]["centraleNuc"]) * factNuc +
               nbThermReg["bre"] * prodGaz / nbTherm)

    ##Haut-de-France
    popHDF = 0.09
    prodHDF = (np.array(fdc_off.hdf) * mix["hdf"]["eolienneOFF"] * powOffshore +
               np.array(fdc_on.hdf) * mix["hdf"]["eolienneON"] * powOnshore +
               np.array(fdc_pv.hdf) * mix["hdf"]["panneauPV"] * powPV +
               (mix["hdf"]["EPR2"] - nvPionsReg["hdf"]["EPR2"] + mix["hdf"]["centraleNuc"]) * factNuc +
               nbThermReg["hdf"] * prodGaz / nbTherm)

    ##Pays de la Loire
    popPDL = 0.06
    prodPDL = (np.array(fdc_off.pll) * mix["pll"]["eolienneOFF"] * powOffshore +
               np.array(fdc_on.pll) * mix["pll"]["eolienneON"] * powOnshore +
               np.array(fdc_pv.pll) * mix["pll"]["panneauPV"] * powPV +
               (mix["pll"]["EPR2"] - nvPionsReg["pll"]["EPR2"] + mix["pll"]["centraleNuc"]) * factNuc +
               nbThermReg["pll"] * prodGaz / nbTherm)

    ##Auvergne-Rhône-Alpes
    popARA = 0.12
    prodARA = (np.array(fdc_on.ara) * mix["ara"]["eolienneON"] * powOnshore +
               np.array(fdc_pv.ara) * mix["ara"]["panneauPV"] * powPV +
               (mix["ara"]["EPR2"] - nvPionsReg["ara"]["EPR2"] + mix["ara"]["centraleNuc"]) * factNuc +
               nbThermReg["ara"] * prodGaz / nbTherm)

    ##Grand Est
    popGE = 0.08
    prodGE = (np.array(fdc_on.est) * mix["est"]["eolienneON"] * powOnshore +
              np.array(fdc_pv.est) * mix["est"]["panneauPV"] * powPV +
              (mix["est"]["EPR2"] - nvPionsReg["est"]["EPR2"] + mix["est"]["centraleNuc"]) * factNuc +
              nbThermReg["est"] * prodGaz / nbTherm)

    ##Normandie
    popNOR = 0.05
    prodNOR = (np.array(fdc_off.nor) * mix["nor"]["eolienneOFF"] * powOffshore +
               np.array(fdc_on.nor) * mix["nor"]["eolienneON"] * powOnshore +
               np.array(fdc_pv.nor) * mix["nor"]["panneauPV"] * powPV +
               (mix["nor"]["EPR2"] - nvPionsReg["nor"]["EPR2"] + mix["nor"]["centraleNuc"]) * factNuc +
               nbThermReg["nor"] * prodGaz / nbTherm)

    ##Bourgogne-Franche-Comte
    popBFC = 0.04
    prodBFC = (np.array(fdc_on.bfc) * mix["bfc"]["eolienneON"] * powOnshore +
               np.array(fdc_pv.bfc) * mix["bfc"]["panneauPV"] * powPV +
               (mix["bfc"]["EPR2"] - nvPionsReg["bfc"]["EPR2"] + mix["bfc"]["centraleNuc"]) * factNuc +
               nbThermReg["bfc"] * prodGaz / nbTherm)

    ##Centre Val de Loire
    popCVL = 0.04
    prodCVL = (np.array(fdc_on.cvl) * mix["cvl"]["eolienneON"] * powOnshore +
               np.array(fdc_pv.cvl) * mix["cvl"]["panneauPV"] * powPV +
               (mix["cvl"]["EPR2"] - nvPionsReg["cvl"]["EPR2"] + mix["cvl"]["centraleNuc"]) * factNuc +
               nbThermReg["cvl"] * prodGaz / nbTherm)

    ##PACA
    popPAC = 0.08
    prodPAC = (np.array(fdc_off.pac) * mix["pac"]["eolienneOFF"] * powOffshore +
               np.array(fdc_on.pac) * mix["pac"]["eolienneON"] * powOnshore +
               np.array(fdc_pv.pac) * mix["pac"]["panneauPV"] * powPV +
               (mix["pac"]["EPR2"] - nvPionsReg["pac"]["EPR2"] + mix["pac"]["centraleNuc"]) * factNuc +
               nbThermReg["pac"] * prodGaz / nbTherm)

    ##Ile-de-France
    popIDF = 0.19
    prodIDF = (np.array(fdc_on.idf) * mix["idf"]["eolienneON"] * powOnshore +
               np.array(fdc_pv.idf) * mix["idf"]["panneauPV"] * powPV +
               (mix["idf"]["EPR2"] - nvPionsReg["idf"]["EPR2"] + mix["idf"]["centraleNuc"]) * factNuc +
               nbThermReg["idf"] * prodGaz / nbTherm)

    ##Corse
    popCOR = 0.005
    prodCOR = (np.array(fdc_off.cor) * mix["cor"]["eolienneOFF"] * powOffshore +
               np.array(fdc_on.cor) * mix["cor"]["eolienneON"] * powOnshore +
               np.array(fdc_pv.cor) * mix["cor"]["panneauPV"] * powPV +
               (mix["cor"]["EPR2"] - nvPionsReg["cor"]["EPR2"] + mix["cor"]["centraleNuc"]) * factNuc +
               nbThermReg["cor"] * prodGaz / nbTherm)

    ##production totale sur le territoire
    prod = prodOCC + prodNA + prodBRE + prodHDF + prodPDL + prodARA + prodGE + prodNOR + prodBFC + prodCVL + prodPAC + prodIDF + prodCOR

    ##calcul des ratios (prod de la region/pros totale --> heure par heure)
    ratioOCC = np.zeros(H)
    ratioNA = np.zeros(H)
    ratioBRE = np.zeros(H)
    ratioHDF = np.zeros(H)
    ratioPDL = np.zeros(H)
    ratioARA = np.zeros(H)
    ratioGE = np.zeros(H)
    ratioNOR = np.zeros(H)
    ratioBFC = np.zeros(H)
    ratioCVL = np.zeros(H)
    ratioPAC = np.zeros(H)
    ratioIDF = np.zeros(H)
    ratioCOR = np.zeros(H)

    for i in range(H):
        ratioOCC[i] = prodOCC[i] / prod[i] if prod[i] != 0 else 0
        ratioNA[i] = prodNA[i] / prod[i] if prod[i] != 0 else 0
        ratioBRE[i] = prodBRE[i] / prod[i] if prod[i] != 0 else 0
        ratioHDF[i] = prodHDF[i] / prod[i] if prod[i] != 0 else 0
        ratioPDL[i] = prodPDL[i] / prod[i] if prod[i] != 0 else 0
        ratioARA[i] = prodARA[i] / prod[i] if prod[i] != 0 else 0
        ratioGE[i] = prodGE[i] / prod[i] if prod[i] != 0 else 0
        ratioNOR[i] = prodNOR[i] / prod[i] if prod[i] != 0 else 0
        ratioBFC[i] = prodBFC[i] / prod[i] if prod[i] != 0 else 0
        ratioCVL[i] = prodCVL[i] / prod[i] if prod[i] != 0 else 0
        ratioPAC[i] = prodPAC[i] / prod[i] if prod[i] != 0 else 0
        ratioIDF[i] = prodIDF[i] / prod[i] if prod[i] != 0 else 0
        ratioCOR[i] = prodCOR[i] / prod[i] if prod[i] != 0 else 0

        # print(ratioOCC)
    ##difference des rations prod et ratios pop regions par regions

    diffOCC = np.zeros(H)
    diffNA = np.zeros(H)
    diffBRE = np.zeros(H)
    diffHDF = np.zeros(H)
    diffPDL = np.zeros(H)
    diffARA = np.zeros(H)
    diffGE = np.zeros(H)
    diffNOR = np.zeros(H)
    diffBFC = np.zeros(H)
    diffCVL = np.zeros(H)
    diffPAC = np.zeros(H)
    diffIDF = np.zeros(H)
    diffCOR = np.zeros(H)

    diffOCC = ratioOCC - popOCC * np.ones(H)
    diffNA = ratioNA - popNA * np.ones(H)
    diffBRE = ratioBRE - popBRE * np.ones(H)
    diffHDF = ratioHDF - popHDF * np.ones(H)
    diffPDL = ratioPDL - popPDL * np.ones(H)
    diffARA = ratioARA - popARA * np.ones(H)
    diffGE = ratioGE - popGE * np.ones(H)
    diffNOR = ratioNOR - popNOR * np.ones(H)
    diffBFC = ratioBFC - popBFC * np.ones(H)
    diffCVL = ratioCVL - popCVL * np.ones(H)
    diffPAC = ratioPAC - popPAC * np.ones(H)
    diffIDF = ratioIDF - popIDF * np.ones(H)
    diffCOR = ratioCOR - popCOR * np.ones(H)

    ##moyenne sur les heures de l'annee des differences
    moyOCC = np.sum(diffOCC) / 8760 * 100
    moyNA = np.sum(diffNA) / 8760 * 100
    moyBRE = np.sum(diffBRE) / 8760 * 100
    moyHDF = np.sum(diffHDF) / 8760 * 100
    moyPDL = np.sum(diffPDL) / 8760 * 100
    moyARA = np.sum(diffARA) / 8760 * 100
    moyGE = np.sum(diffGE) / 8760 * 100
    moyNOR = np.sum(diffNOR) / 8760 * 100
    moyBFC = np.sum(diffBFC) / 8760 * 100
    moyCVL = np.sum(diffCVL) / 8760 * 100
    moyPAC = np.sum(diffPAC) / 8760 * 100
    moyIDF = np.sum(diffIDF) / 8760 * 100
    moyCOR = np.sum(diffCOR) / 8760 * 100

    moyAbsOCC = np.sum(np.abs(diffOCC)) / 8760 * 100
    moyAbsNA = np.sum(np.abs(diffNA)) / 8760 * 100
    moyAbsBRE = np.sum(np.abs(diffBRE)) / 8760 * 100
    moyAbsHDF = np.sum(np.abs(diffHDF)) / 8760 * 100
    moyAbsPDL = np.sum(np.abs(diffPDL)) / 8760 * 100
    moyAbsARA = np.sum(np.abs(diffARA)) / 8760 * 100
    moyAbsGE = np.sum(np.abs(diffGE)) / 8760 * 100
    moyAbsNOR = np.sum(np.abs(diffNOR)) / 8760 * 100
    moyAbsBFC = np.sum(np.abs(diffBFC)) / 8760 * 100
    moyAbsCVL = np.sum(np.abs(diffCVL)) / 8760 * 100
    moyAbsPAC = np.sum(np.abs(diffPAC)) / 8760 * 100
    moyAbsIDF = np.sum(np.abs(diffIDF)) / 8760 * 100
    moyAbsCOR = np.sum(np.abs(diffCOR)) / 8760 * 100
    
      transfert=                      {"occ": int(round(moyOCC)),
                            "naq": int(round(moyNA)),
                            "bre": int(round(moyBRE)),
                            "hdf": int(round(moyHDF)),
                            "pll": int(round(moyPDL)),
                            "ara": int(round(moyARA)),
                            "est": int(round(moyGE)),
                            "nor": int(round(moyNOR)),
                            "bfc": int(round(moyBFC)),
                            "cvl": int(round(moyCVL)),
                            "pac": int(round(moyPAC)),
                            "idf": int(round(moyIDF)),
                            "cor": int(round(moyCOR))
                            }
                            
                            
    """
    transfert={}
    result = {"carte": mix["carte"],
              "annee": mix["annee"],
              "alea": mix["alea"],
              "biogaz": round(gazBiomasse),
              "consoGaz": round(consoGaz),
              "GazElectrolyse": round(annuel["Gprod"]),
              "prodGazFossile": round(prodGazFossile),
              "demande": int(demane_annuelle), "production": prodTotale,
              "prodOnshore": prodOn, "puissanceEolienneON": round(mix['nb']["eolienneON"] * powOnshore, 2),
              "prodOffshore":prodOff,
              "puissanceEolienneOFF": round(mix['nb']["eolienneOFF"] * powOffshore, 2),
              "prodPv": prodPv, "puissancePV": round(mix['nb']["panneauPV"] * powPV, 2),
              "prodEau": prodEau,
              "prodNucleaire": prodNuc, "puissanceNucleaire": round(puissances['N'], 2),
              "prodGaz": prodGaz, "puissanceGaz": round(puissances['G'], 2),
              "prodPhs": prodPhs, "puissancePhs": round(puissances['S'], 2),
              "prodBatterie": prodBat, "puissanceBatterie": round(puissances['B'], 2),
              "co2": EmissionCO2,
              "nbSurplus": nbS, "nbPenuries": nbP,
              "surplusQuotidien": listeSurplusQuotidien, "surplusHoraire": listeSurplusHoraire,
              "penuriesQuotidien": listePenuriesQuotidien, "penuriesHoraire": listePenuriesHoraire,
              "transfert": transfert
              }

    return result


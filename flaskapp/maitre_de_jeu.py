import os
import pandas as pd

from climix import stratege, technologies
import random

from climix.technologies import infos


ceChemin = os.path.dirname(os.path.realpath(__file__)) + '/'

#########################
### TOUT EST EN GW(h) ###
#########################

aleas = ["", "MEGC1", "MEGC2", "MEGC3", "MEMFDC1", "MEMFDC2", "MEMFDC3",
         "MECS1", "MECS2", "MEVUAPV1", "MEVUAPV2", "MEVUAPV3",
         "MEMDA1", "MEMDA2", "MEMDA3", "MEMP1", "MEMP2", "MEMP3",
         "MEGDT1", "MEGDT2", "MEGDT3"] #, "MECS3"

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
    "methanation": "Power 2 Gaz",
    "biomasse": "Biomasse"
}
pion_short = {
    "eolienneON": "ONshore",
    "eolienneOFF": "OFFshore",
    "panneauPV": "PV",
    "centraleNuc": "Nuc.",
    "EPR2": "EPR2",
    "methanation": "P2G",
    "biomasse": "Bio"
}


class errJeu(Exception):
    pass


def initialise_partie(dm):
    dm.init_partie()


def nouveau_mix(annee, mix, alea=None):
    if alea is None:
        alea = random.choice(aleas)

    nmix = mix.copy()
    nmix["annee"] = annee
    nmix["actif"] = True
    nmix["alea"] = alea
    nmix["capacites"] = nouv_capacite_alea(nmix, nmix['alea'])
    nmix["nb"] = calculer_nb(mix, annee)
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

    for an in mixes:
        if mixes[an]["actif"]:
            annee_active = an
            break
        else:
            annee_active = an

    return mix, annee_active


def nouv_capacite_alea(mix, alea):
    capmax_info = mix["capacites"]
    # carte alea MECS (lance 1 / 2)
    if alea == "MECS1" or alea == "MECS2" or alea == "MECS3":
        for k in capmax_info:
            capmax_info[k]["eolienneON"] -= int(capmax_info[k]["eolienneON"] * 0.6)

    if alea == "MECS2" or alea == "MECS3":
        capmax_info["occ"]["eolienneON"] *= 2
        capmax_info["occ"]["panneauPV"] *= 2

    if alea == "MECS3":
        for k in capmax_info:
            capmax_info[k]["EPR2"]=0
            capmax_info[k]["centraleNuc"] = 0

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
                duree = 45
                if 'centraleNuc' in mix['capacites'][reg]:
                    cap = mix['capacites'][reg]['centraleNuc']-nb
                else:
                    cap = 0

            elif p == "EPR2":
                if 'EPR2' in mix['capacites'][reg]:
                    cap = mix['capacites'][reg]['EPR2']
                else:
                    cap = 20-nb
                duree = 45

            elif p == "methanation":
                duree = 100
                cap = 40 - nb

            elif p == "eolienneON" or p == "eolienneOFF":
                duree = 20
                cap = mix["capacites"][reg][p] - nb
            else:
                duree = 100
                cap = mix["capacites"][reg][p] - nb

            for an in mix["unites"][reg][p]:
                if int(an) + duree <= (annee_int - 5):
                    # unité en fin de vie
                    if ((annee_int - 10) < int(an) + duree) or annee_int == 2030:
                        # elle vient d'arriver en fin de vie, ou c'est le début de simu
                        cap_fin_de_vie = min(0, cap)
                        replace_dict[reg][p][an] = {"action": "?",
                                                    "valeur": "",
                                                    "min": -mix["unites"][reg][p][an],
                                                    "max": max(cap_fin_de_vie, -mix["unites"][reg][p][an]),
                                                    "forcee": True,
                                                    "date": an}
                        cap -= cap_fin_de_vie

            if cap > 0:
                replace_dict[reg][p][annee] = {"action": "=",
                                               "valeur": "",
                                               "min": 0,
                                               "max": cap,
                                               "forcee": False,
                                               "date": annee}

    actions = {"alea": {'actuel': mix["alea"], 'action': False},
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
        raise errJeu(
            f"On ne peut pas réduire le stock de batteries de {actions['stock']['actuel']} à {actions['stock']['nouv']} ! C'est gâcher")

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

                    unites[reg][p][act['date']] += act['valeur']
                    if unites[reg][p][act['date']] <= 0:
                        unites[reg][p].pop(act['date'])
                    """
                    if act['date'] in new["unites"][reg][p]:
                        unites[reg][p][act['date']] += act['nb_renouveles']
                    elif act['nb_renouveles'] > 0:
                        unites[reg][p][act['date']] = act['nb_renouveles']
                    unites[reg][p].pop(an)
                    """

                if act["action"] == "+":
                    if p == "EPR2":
                        l_annee = (int(an) + 5).__str__()
                        act["EPR2_en_construction"] = act['valeur']

                    else:
                        l_annee = an
                    if l_annee in new["unites"][reg][p]:
                        unites[reg][p][l_annee] += act['valeur']

                    else:
                        unites[reg][p][l_annee] = act['valeur']

                    act['nb_nouvelles'] = act['valeur']

                if act["action"] == "=":
                    if 'nb_nouvelles' in act:
                        act.pop('nb_nouvelles')
                    if "EPR2_en_construction" in act:
                        act.pop('EPR2_en_construction')

    new['unites'] = unites
    new["nb"] = calculer_nb(new, mix['annee'])
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


def calculer_nb(mix, annee):
    nb = appliquer_a_dict(dico=mix["unites"],
                          fonc=lambda pion: sum([val if int(an) <= int(annee) else 0 for an, val in pion.items()]))
    nb = sommer_dict(nb)
    return nb


budget_ratio = {'S1': 90./120.,
                'S2': 100./120.,
                'S3Enr': 110./120.,
                'S3Nuke': 110./120.
                }

def calculer(dm, annee, actions, scenario):
    try:
        mix, annee_active = recup_mix(annee=annee, dm=dm)
        new = appliquer(actions, mix)
        dm.set_fichier(fichier="new", dico=new)
        mix["actions"] = actions
        mix["nb"] = new["nb"]
        dm.set_item_fichier(fichier='mixes', item=annee, val=mix)

        annee_en_cours = (mix['annee']).__str__()

        if scenario=="2025Plat":
            df = dm.pays.get_scenario("S1")
            ##df = pd.read_hdf(chemin_scenarios + "S1_25-50.h5", "df")
            df = df.loc["2025-1-1 0:0":"2025-12-31 23:0"]
        else:
            #df = pd.read_hdf(chemin_scenarios + scenario + "_25-50.h5", "df")
            df = dm.pays.get_scenario(scenario)

            if int(annee_en_cours) >= 2050:
                df = df.loc["2050-1-1 0:0":"2050-12-31 23:0"]
            else:
                df = df.loc[annee_en_cours + "-1-1 0:0": annee_en_cours + "-12-31 23:0"]

        chroniques, prod_renouvelables, puissances = stratege.simuler(demande=df["demande"].values,
                                                                      electrolyse=df["electrolyse"].values,
                                                                      mix=mix,
                                                                      pays=dm.pays)


        result = calculer_resultats(mix, actions, chroniques, prod_renouvelables, puissances)
        if scenario in budget_ratio:
            result["budget"] *= budget_ratio[scenario]
        result["budget"] = round(result["budget"])
        chroniques["date"] = df.index.values
        dm.set_chroniques(chroniques, annee=annee)
        dm.set_item_fichier(fichier='resultats', item=annee, val=result)
        resp = ["success"]

    except errJeu as ex:
        if actions['alea']['action']:
            oldmix, annee_active = recup_mix(annee=(int(annee) - 5).__str__(), dm=dm)
            new = nouveau_mix(annee=annee, mix=oldmix, alea=actions["alea"]['nouv'])

            dm.set_item_fichier(fichier='mixes', item=annee, val=new)
            resp = ["aleaChangement", ex.__str__()]
        else:
            resp = ["errJeu", ex.__str__()]

    return resp


def calculer_resultats(mix, actions, chroniques, prod_renouvelables, puissances):
    result = {}
    annuel = {item: sum(val) for item, val in chroniques.items()}


    result = result_prod_region(mix, annuel, chroniques, prod_renouvelables, puissances)
    result.update(result_couts(actions, annuel, result['prodGazFossile']))


    # result.update(result_ressources(mix, save, nbPions, nvPions))
    return result


def result_couts(actions, annuel, prodGazFossile):

    renouv = appliquer_a_dict(actions['regions'], lambda dic: sum(
        [act['nb_renouveles'] for an, act in dic.items() if 'nb_renouveles' in act]))
    renouv = sommer_dict(renouv)

    nouv = appliquer_a_dict(actions['regions'],
                            lambda dic: sum([act['nb_nouvelles'] for an, act in dic.items() if 'nb_nouvelles' in act]))
    nouv = sommer_dict(nouv)

    demantele = appliquer_a_dict(actions['regions'], lambda dic: sum(
        [act['nb_demanteles'] for an, act in dic.items() if 'nb_demanteles' in act]))
    demantele = sommer_dict(demantele)


    prixGaz = technologies.TechnoGaz.prix
    prixNuc = technologies.TechnoNucleaire.prix

    # carte alea MEGC (lance 1 / 3)
    if actions['alea']['actuel'] == "MEGC1" or actions['alea']['actuel'] == "MEGC2" or actions['alea'][
        'actuel'] == "MEGC3":
        prixGaz *= 1.5  # alea1

    if actions['alea']['actuel'] == "MEGC3":
        prixNuc *= 1.4  # alea3

    # carte alea MEMP (lance 3)
    if actions['alea']['actuel'] == "MEMP3":
        prixGaz *= 1.3
        prixNuc *= 1.2

    # PACCO ajout *5 car 5 ans
    # Le cout du démentèlement nuke n'est pas pris en compte !"
    cout_gaz = prodGazFossile * prixGaz * 5.      #car 5 années
    cout_uranium = annuel['Nprod'] * prixNuc * 5. # car 5 années
    cout_construction = (
        (nouv["eolienneON"] + renouv["eolienneON"]) * infos["eolienneON"]["Cout"] +
        (nouv["eolienneOFF"] + renouv["eolienneOFF"]) * infos["eolienneOFF"]["Cout"] +
        (nouv["panneauPV"] + renouv["panneauPV"]) * infos["panneauPV"]["Cout"] +
        nouv["EPR2"] * infos["EPR2"]["Cout"] +
        renouv["centraleNuc"] * infos["centraleNuc"]["CoutRenouv"] +
        demantele["centraleNuc"] * infos["centraleNuc"]["CoutDemantele"] +
        nouv["biomasse"] * infos["biomasse"]["Cout"] +
        nouv["methanation"] *infos["methanation"]["Cout"] +
        (actions['stock']['nouv'] - actions['stock']['actuel']) *infos["batt"]["Cout"]
    )


    # (S.PoutMax * 0.455) / 0.91 +

    # formule BIZARE
    # if mix["annee"] != 2030:
    #    cout += (10 - renouv["centraleNuc"]) * 0.5

    # budget à chaque tour sauf si carte evènement bouleverse les choses
    #VIEUX
    #budget = 70.


    # Voir Calculer() et budget ratio pour une variation selon les scenarios
    budget = 120.

    # carte alea MEVUAPV : lance 3
    if actions['alea']['actuel'] == "MEVUAPV3":
        budget -= 10.

    # carte MEMDA : lance 1 / 2
    if actions['alea']['actuel'] == "MEMDA1" or actions['alea']['actuel'] == "MEMDA2" or actions['alea'][
        'actuel'] == "MEMDA3":
        budget += 3.11625  # BIZARE

    if actions['alea']['actuel'] == "MEMDA2" or actions['alea']['actuel'] == "MEMDA3":
        cout_construction -= 1.445  # BIZARE

    # carte MEGDT : lance 1 / 3
    if actions['alea']['actuel'] == "MEGDT1" or actions['alea']['actuel'] == "MEGDT2" or actions['alea'][
        'actuel'] == "MEGDT3":
        cout_construction += 1. / 3. * nouv["pac"]["panneauPV"] * 3.6

    if actions['alea']['actuel'] == "MEGDT3":
        # cout += nouv["pll"]["eolienneOFF"]*1.2
        # d'après le rapport de stage, un pion d'éolienneOFF devrait coûter 6 Mds et non 1.2 Mds
        cout_construction += nouv["pll"]["eolienneOFF"] * 6

    cout = cout_construction + cout_uranium + cout_gaz
    result = {"cout": round(cout*10.)/10.,
              "budget": round(budget*10.)/10.,
              "cout_gaz": round(cout_gaz*10.)/10.,
              "cout_uranium": round(cout_uranium*10.)/10.,
              "cout_construction": round(cout_construction*10.)/10.
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

    prodTotale = prodOn + prodOff + prodPv + prodEau + prodNuc + prodGaz + prodPhs + prodBat

    s = chroniques["s"]
    p = chroniques["p"]

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

    consoGazGlobale = (chroniques['Gstored'][0] - chroniques['Gstored'][-1])
    # PACCO compter l'hydro si le niveau du lac est plus bas c'est que l'on 
    # fait baisser le niveau d'étiage du lac. On considère que que ces GWh électrique
    # Lac auraient été consommés en utilisant du gaz...  
    #consoHydro = (chroniques['Lstored'][0] - chroniques['Lstored'][-1])
    #consoGazGlobale += consoHydro / G.etaout 
    
    
    consGazG2P = annuel['Gprod'] / technologies.TechnoGaz.etaout  # gaz brulé pour le G2P
    prodGazP2G = -annuel['Gcons'] * technologies.TechnoGaz.etain  # gaz produit par le P2G
    #PACCO TOdo passer dans techno
    prodGazBiomasse = mix['nb']["biomasse"] * 2 * 0.1 * 0.71 * stratege.H  # gaz produit en bio masse

    #  gaz =        nbPions      * nbCentraleParPion * puissance * fdc * nbHeures

    # note Hugo : il semble que cet effet soit mal implémenté : à tester
    # carte alea MEMFDC (lance 2 / 3)
    # un an de moins de biomasse en nouvelle aquitaine (impact sur cette année)
    if mix["alea"] == "MEMFDC2":
        prodGazBiomasse -= mix['nb']["naq"]["biomasse"] * infos["biomasse"]["PoutMax"]

    consGazFossile = annuel["electrolyse"] + consGazG2P - prodGazP2G - prodGazBiomasse
    if consGazFossile < 0.:
        consGazFossile = 0.

    EmissionCO2 = prodOn * infos["eolienneON"]["FacteurCO2"] \
        + prodOff * infos["eolienneOFF"]["FacteurCO2"] \
        + prodPv * infos["panneauPV"]["FacteurCO2"] \
        + prodEau * 10. \
        + prodNuc * infos["centraleNuc"]["FacteurCO2"]\
        + consGazFossile * 443.  # variable EmissionCO2
    # Pascal : 6 g/kWh pour nucléaire et toutes les prods en GWh => unitées en tonnes de CO2

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

    factNuc = 0 if (mix['nb']['EPR2'] + mix['nb']['centraleNuc'] == 0) else prodNuc / (
                mix['nb']['EPR2'] + mix['nb']['centraleNuc'])

    population = {'ara': 0.12, 'bfc': 0.04, 'bre': 0.05, 'cor': 0.005,
                  'cvl': 0.04, 'est': 0.08, 'hdf': 0.09, 'idf': 0.19,
                  'naq': 0.09, 'nor': 0.05, 'occ': 0.09, 'pac': 0.08,
                  'pll': 0.06}

    """
    np.array(fdc_off.occ) * mix["occ"]["eolienneOFF"] * powOffshore +
    np.array(fdc_on.occ) * mix["occ"]["eolienneON"] * powOnshore +
    np.array(fdc_pv.occ) * mix["occ"]["panneauPV"] * powPV +
    (mix["occ"]["EPR2"] - nvPionsReg["occ"]["EPR2"] + mix["occ"]["centraleNuc"]) * factNuc +
    nbThermReg["occ"] * prodGaz / nbTherm)
    """
    # ratio = {}
    prod = {}
    # diff = {}
    transfert = {}
    for reg in population:
        prod[reg] = (prod_renouvelables['regions'][reg]["eolienneOFF"].sum() +
                     prod_renouvelables['regions'][reg]["eolienneON"].sum() +
                     prod_renouvelables['regions'][reg]["panneauPV"].sum())
        prod[reg] += (mix['nb'][reg]["EPR2"] + mix['nb'][reg]["centraleNuc"]) * factNuc
        # prod[reg] += nbThermReg[reg] * prodGaz / nbTherm
        prod[reg] += prodGaz * population[reg]
        # ratio[reg] = prod[reg] / prodTotale
        # diff[reg] = ratio[reg] - population[reg]
        # transfert[reg] = int(diff[reg] * 100.)
        transfert[reg] = prod[reg] / (population[reg] * 68373433.)

    result = {"carte": mix["carte"],
              "annee": mix["annee"],
              "alea": mix["alea"],
              "biogaz": round(prodGazBiomasse),
              "consoGaz": round(consoGazGlobale),
              "electrolyse": round(annuel["electrolyse"]),
              "GazElectrolyse": round(prodGazP2G),
              "demandeG2P": round(consGazG2P),
              "prodGazFossile": round(consGazFossile),
              "demande": int(demane_annuelle), "production": prodTotale,
              "prodOnshore": prodOn, "puissanceEolienneON": round(mix['nb']["eolienneON"] * powOnshore, 2),
              "prodOffshore": prodOff,
              "puissanceEolienneOFF": round(mix['nb']["eolienneOFF"] * powOffshore, 2),
              "prodPv": prodPv, "puissancePV": round(mix['nb']["panneauPV"] * powPV, 2),
              "prodEau": prodEau, "puissanceEau": round(puissances['L'], 2),
              "prodNucleaire": prodNuc, "puissanceNucleaire": round(puissances['N'], 2),
              "prodGaz": consGazG2P, "puissanceGaz": round(puissances['G'], 2),
              "prodPhs": prodPhs, "puissancePhs": round(puissances['S'], 2),
              "prodBatterie": prodBat, "puissanceBatterie": round(puissances['B'], 2),
              "co2": EmissionCO2,
              "nbSurplus": nbS, "nbPenuries": nbP,
              "surplusQuotidien": listeSurplusQuotidien, "surplusHoraire": listeSurplusHoraire,
              "penuriesQuotidien": listePenuriesQuotidien, "penuriesHoraire": listePenuriesHoraire,
              "transfert": transfert
              }

    return result

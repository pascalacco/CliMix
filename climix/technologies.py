import os
import numpy as np
import pandas as pd


chemin = os.path.dirname(os.path.realpath(__file__))
chemin_donnees = chemin + "/mix_data"


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

#vieux PoutMaxBio = 2. * 0.1 * 0.71 * (24. * 365.)
#PACCO modif de Slachaize
PoutMaxBio = 0.5

""" VIEUX 
#  = nbCentraleParPion * puissance * fdc * nbHeures
infos = {
    "eolienneON":   {"PoutMax": 1.4,        "Cout" : 3.5,      "FacteurCO2": 10.},
    "eolienneOFF":  {"PoutMax": 2.4,        "Cout" : 6.,        "FacteurCO2": 9.},
    "panneauPV":    {"PoutMax": 3.,          "Cout" : 3.6,      "FacteurCO2": 55.},
    "centraleNuc":  {"PoutMax": 1.08,       "Cout" : 2.,        "FacteurCO2": 6.},
    "EPR2":         {"PoutMax": 1.67,       "Cout" : 8.6,      "FacteurCO2": 6.},
    "methanation":  {"PoutMax": None,       "Cout" : 4.85,     "FacteurCO2": 0.},
    "biomasse":     {"PoutMax": PoutMaxBio, "Cout" : 0.12,     "FacteurCO2": 0.},
    "batt":        {"PoutMax": 20.08/10.,  "Cout" : 0.8,      "FacteurCO2": 0.}
}

"""

"""
Donnée issues de l'ADEME

Cout du néclaire en divisant le parc par 56 réacteurs :
https://www.sortirdunucleaire.org/Prolongation-des-reacteurs-risques-et-couts

Nucléaire pion moyen 1139 
 16 arret complet en 2025. 
 Une moyenne de 6 réacteurs en révision décénale de 6 mais  par an.
 Donc facteur de charge décennal = (55-3)/55 
 
 Indisponibilité de 13 réacteurs (fissures et retard de maintenance covid)
 facteur de charge pessimiste de (55-3-13)/55 
 
 Bilan GES
 https://analysesetdonnees.rte-france.com/emissions/emission-ges
 
 
 
"""
PoutNuke = 1.139*(55-3-13)/55.
infos = {
    "eolienneON":   {"PoutMax": 1.4,        "Cout" : 3.5,      "FacteurCO2": 16.},
    "eolienneOFF":  {"PoutMax": 2.4,        "Cout" : 6.,        "FacteurCO2": 17.},
    "panneauPV":    {"PoutMax": 3.,          "Cout" : 3.6,      "FacteurCO2": 44.},
    "centraleNuc":  {"PoutMax": PoutNuke,    "CoutRenouv" : 2,  "FacteurCO2": 7. , "CoutDemantele": 0.5},
    "EPR2":         {"PoutMax": 1.67,       "Cout" : 8.6,      "FacteurCO2": 6.},
    "methanation":  {"PoutMax": None,       "Cout" : 4.85,     "FacteurCO2": 0.},
    "biomasse":     {"PoutMax": PoutMaxBio, "Cout" : 0.12,     "FacteurCO2": 107.},
    "batt":        {"PoutMax": 20.08/10.,  "Cout" : 0.8,      "FacteurCO2": 0.}
}



class Techno:
    """Classe regroupant toutes les technologies de stockage et de production pilotables

    """
    H = 24*365

    def __init__(self, nom, stock, etain, etaout, PoutMax, PinMax, capacité, H=H):
        """ Création de la Technologie de stockage/déstockage/production
        Args:
            nom (str): nom de la techno
            stock (array) : niveau des stocks à chaque heure
            etain (float) : coefficient de rendement a la charge
            etaout (float) : coefficient de rendement a la decharge
            PoutMax (float) : puissance maximale de décharge (flux sortant GW)
            PinMax (float) : puissance maximale de charge (flux entrant GW)
            capacité (float) : capacite maximale de stockage (GWh)

        Returns:
            l'objet de la classe créé (Techno)
        """
        self.nom = nom  # . nom de la techno
        if stock is None :
            stock=0
        if np.isscalar(stock):
            self.stock = np.ones(H) * stock
        else:
            self.stock = stock

        self.etain = etain  # . coefficient de rendement à la charge
        self.etaout = etaout  # . coefficient de rendement à la decharge
        self.PoutMax = PoutMax  # . capacite installee (flux sortant)
        self.PinMax = PinMax  # . capacite de charge d'une techno de stockage (flux entrant)
        self.capacité = capacité  # . Capacite maximale de stockage de la techno (Volume max)
        self.H = H
        self.set_décharge()
        self.set_recharge()


    def set_décharge(self, décharge=0):
        if np.isscalar(décharge):
            self.décharge = np.ones(self.H) * décharge
        else:
            self.décharge = décharge

    def set_recharge(self, recharge=0):
        if np.isscalar(recharge):
            self.recharge = np.ones(self.H) * recharge
        else:
            self.recharge = recharge

    def get_pertes(self):
        return self.décharge / self.etaout * (1 - self.etaout) + self.recharge * (1-self.etain)

    def Pout(self, k):
        """Renvoie la puissance maximum de décharge à l'heure k """
        return min(self.stock[k] * self.etaout, self.PoutMax-self.décharge[k]+self.recharge[k])

    def Pin(self, k):
        """Renvoie la puissance maximum de recharge à l'heure k """
        return min((self.capacité-self.stock[k]) / self.etain, self.PinMax-self.recharge[k]+self.recharge[k])

    def annuler_recharger(self, k, aanuler):
        """

        """
        vaannuler = min(aanuler, self.recharge[k])
        self.recharge[k] -= vaannuler
        self.stock[k:] -= vaannuler * self.etain
        return vaannuler

    def annuler_décharger(self, k, aanuler):
        # annulation d'ordre
        vaannuler = min(aanuler, self.décharge[k])
        self.décharge[k] -= vaannuler
        self.stock[k:] += vaannuler / self.etaout
        return vaannuler

    def recharger(self, k, astocker):
        """Recharge les moyens de stockage quand on a trop d'energie

        Args:
            k (int) : heure courante
            astocker (float) : qte d'energie a stocker (GWh/h)

        Returns:
            out (flout) : partie de astocker qui n'a pas pu être stockée
        """
        if astocker < 0:

            out = 0

        else:
            relargue = 0
            if self.décharge[k] > 0:
                relargue = self.annuler_décharger(k, astocker)
                astocker -= relargue

            vastoker = min(astocker , self.Pin(k))
            self.stock[k:] = self.stock[k] + vastoker * self.etain
            self.recharge[k] += vastoker
            out = vastoker + relargue

        return out


    def décharger(self, k, aproduire):
        """ Decharge les moyens de stockage quand on a besoin d'energie

        Args:
            k (int) : heure courante
            aproduire (float) : qte d'energie à récupérer

        Return:
            out (float) : le reste de ce qui n'a pas été produit
        """
        if aproduire <= 0:
            out = 0

        else:
            relargue = 0
            if self.recharge[k] > 0:
                relargue = self.annuler_recharger(k, aproduire)
                aproduire -= relargue

            vaproduire = min(aproduire, self.Pout(k))

            self.stock[k:] = self.stock[k] - vaproduire/self.etaout
            self.décharge[k] += vaproduire

            out = vaproduire + relargue

        return out


class TechnoStep(Techno):
    etain = 0.95
    etaout = 0.9
    """
        PACCO
        Rendement step entre 70% et 85%
        ici on a 95%*90 = 85,5%
        plutôt optimiste....
    """
    #vieux
    PoutMax = 9.3
    PinMax = 9.3
    capacité = 180

    """
    PACCO 
    https://www.revolution-energetique.com/dossiers/ou-se-trouvent-les-stations-de-transfert-denergie-par-pompage-step-en-france/

    Pomp.   Turb.  Cap 
    Gw      Gw      Gw.h

    1,160   1.79    53,7      Grand’Maison en Isère, d’une puissance en turbine de 1 790 MW ;
    0,870   0.92    38,8      Montézic 1
    0,630   0.73    3,65     Super-Bissorte en Savoie (730 MW) ;
    0,720   0.72    3,6       Revin dans les Ardennes (720 MW) ;
    0,480   0.46    2,76       Le Cheylas en Isère (460 MW)
    0,310   0.33    0,99       La Coche en Savoie (330 MW). 
            0.044   0.344     Le Pouget
            0.051   0.408     Sainte Croix
            0.073   0.576     Vouglans
    
    4,338   5.118   104.828   Total France 

            1.1     20         Redenat projet suspendu

    https://www.edf.fr/groupe-edf/produire-une-energie-respectueuse-du-climat/accelerer-le-developpement-des-energies-renouvelables/lenergie-hydraulique/nous-preparons-lavenir-de-lenergie-hydraulique/developpement-et-stockage-step
    Parle de 5.72GW...
    """
    # suggéré PACCO
    #PoutMax = 5.118 + 1.1     #projet suspendu...
    #PinMax = 4.338 + 1.1
    #capacité = 104.828 + 20.

    def __init__(self, nom='Step', stock=16,
                 etain=etain, etaout=etaout, PoutMax=PoutMax, PinMax=PinMax, capacité=capacité, H=Techno.H):
        super().__init__(nom=nom, stock=stock, etain=etain, etaout=etaout, PoutMax=PoutMax, PinMax=PinMax, capacité=capacité,
                         H=H)


class TechnoBatteries(Techno):
    """
    Calculé pour une capacité totale de 10 unités
    """
    etain = 0.95
    etaout = 0.9
    PoutMaxParUnite = infos["batt"]["PoutMax"]
    PinMaxParUnite = PoutMaxParUnite
    capaciteParUnite = 74.14/10.
    coutParUnite = infos["batt"]["Cout"]
    def __init__(self, nom='Batteries', stock=None,
                 etain=0.95, etaout=0.9, PoutMax=None, PinMax=None,
                 capacité=None, nb_units=1, H=Techno.H):

        self.nb_units = nb_units
        if PoutMax is None:
            PoutMax = nb_units * TechnoBatteries.PoutMaxParUnite
        if PinMax is None:
            PinMax = nb_units * TechnoBatteries.PinMaxParUnite
        if capacité is None:
            capacité = nb_units * TechnoBatteries.capaciteParUnite
        if stock is None:
            stock = capacité/2.

        super().__init__(nom=nom, stock=stock,
                         etain=etain, etaout=etaout, PoutMax=PoutMax, PinMax=PinMax,
                         capacité=capacité, H=H)


class TechnoGaz(Techno):
    """
       PACCO
        Suggestion PACCO selon https://www.edf.fr/groupe-edf/comprendre/production/thermique/thermique-a-flamme-en-chiffres
        Selon
       https://www.kelwatt.fr/prix/gaz-peg-cours-marche-gros
       le prox du Gaz sur le marché de gros (PEG) passe de
       2025 41  euro/MWh
       2026 33
       2027 28
       2028 25

       cela fait environ 30  euro/MW.h
       soit 30 kEuro/GW.h
       soit 30.10-6  Meuro/GW.h  Meuro = milliard d'euros


       Pour le cout combustible voir aussi :
       https://cereme.fr/wp-content/uploads/2022/07/C-12-Comparaison-des-couts-complets-de-production-de-lelectricite_.pdf
       Induire le cout indirect (B) dans le cout du combustible (A) du tableau cereme
       Attention cereme par GWH(élec) et prix GWH(thermique PCS)

       Gaz        224,6 €/MWh(é)(A) + 9,7(B) €/MWhé
           pour un cout du gaz 100€/Gwh thermique (cerem) et rendement 44.52% cela fait
           ramené en GWh(th)
       Gaz         100 €/MWh(th) (A) + 4.3(B) €/MWh(th)
       Le marché étant maintenant plutôt vers 30 €/MWH(th) que les 100€/MWh du cereme

       Je propose
       nucléaire 7,6(A) + 20,1(B) euro/MWh(élec)
       Gaz       35 (A) + 4.3(B)  euro/MWh(élec)

        Selon https://entreprises-collectivites.engie.fr/actualites/stockage-gaz-naturel-comment-france/
        Capacité de 132 TWH en stockage

        À voir
        https://www.data.gouv.fr/fr/datasets/sites-dinjection-de-biomethane-en-france/

        #etain
        # rendement du p2G et G2p de l'hydrogène à 25%
        # Comme les gaz sont mélangés on fait
        # etain(H2) * etaout(Gaz) = 0.25
        # d'où un fauc etain H2 à = 0.25/0.45 = 0.55
        # le vieux etain donne etain * etaout = 26.55%
        # ça semble correct

        Pout MAx :
        # source https://www.services-rte.com/fr/visualisez-les-donnees-publiees-par-rte/capacite-installee-de-production.html?activation_key%3D9410cc48-8e65-4ecb-aace-1e2e8a710cf3%26activation_type%3Dpublic=true
        # https://analysesetdonnees.rte-france.com/disponibilite-production
        #   GAZ 12.9 + Fioul 2.6 + charbon 1.8 =  17,3 15/03/2025
        Td dis 4 diesel * 0.44 + 9 Gaz * 2.015 + 12 GazComb
                1.76      + 18.135         +  6.64   =   26.85
    """
    #vieux
    #capacité = 10000000.
    #init_gaz = capacité / 2.
    #prix = 324.6e-6  # prix de l'electricite produite à partir du
    # gaz/charbon --> moyenne des deux (35€ le MWh) Erreur ! 350 €/MWh
    #prix = 32.46e-6  # vieux prix de l'electricite produite à partir du
    # gaz/charbon --> moyenne des deux (35€ le MWh) Corrigé
    #PoutMax = 34.44


    #suggéré PACCO
    capacité = 132000.  # PACCO
    capacité = 13200000. # sinon à cours de stock en Décembre S4 dès 2030
    init_gaz = capacité / 2.
    prix = 39.3e-6  # MillardEuro /GWh(th PCS)
    PoutMax = 18.54 # GWe installé en france en 2019....

    # Methanation : 1 pion = 10 unites de 100 MW = 1 GW
    # T = Techno('Centrale thermique', None, np.zeros(H), None, 1, 0.7725*nbTherm, None, None)
    # Puissance : 1.08 GWe (EDF)
    # Meme rendement
    etaout = 0.45
    # etaout = 35 à 40% jusqu'à 50%/60% avec cogénération nouvelles du gaz naturel

    #vieux etain = 0.59
    etain = 0.59
    

    PinMaxParUnite = 1.

    def __init__(self, nom='Gaz', stock=init_gaz,
                 etain=etain, etaout=etaout, PoutMax=PoutMax, PinMax=None,
                 capacité=capacité, nb_units=0, H=Techno.H):
        self.nb_units = nb_units

        if PinMax is None:
            PinMax = nb_units * TechnoGaz.PinMaxParUnite

        super().__init__(nom=nom, stock=stock,
                         etain=etain, etaout=etaout, PoutMax=PoutMax, PinMax=PinMax,
                         capacité=capacité, H=H)


class TechnoLacs(Techno):
    """
    ========
    Les Lacs
    ========

    Retenues pilotables alimentées par les pluies et fontes de neige.
    Seulement turbinage pour production.
    Pas de stockage

    Capacité
    --------

    Sur le graphe des capacités on voit (GWh)
    =====   =======     =========   ==============  ========    ================
    Année   Janvier     Min(Mars)   Max(Juil Aout)  Decembre    Stockage Dec-Jan
    =====   =======     =========   ==============  ========    ================
    2017    1731        839         2550            1493        -224
    2018    1577        586         2869            2164        587
    2020    2780        1513        3100            2532        248

    On prévoit une capacité moyenne en janvier de 2000 GWh

    Pout
    ----
    Sur RTE 25.8 au total il faut enlever STEP

    Recharge
    --------
    Les données lake inflows du modèle éole ("/lake_inflows.csv") donnent
    entre 800 et 1900 GWh par mois


    2020 Lacs - > 18600 GWh produits + 248 stockés => 18848 GWh lake inflows
    inflow par heure 18848/8766 = 2.15 GWh/h



    Sources
    -------
        - https://analysesetdonnees.rte-france.com/production/reserve-hydraulique


    #PACCO https://analysesetdonnees.rte-france.com/disponibilite-production
    """
    duree_mois = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])*24
    etain = 1
    etaout = 1

    #vieux
    #PoutMax = 10
    #PinMax = 10

    # suggéré PACCO
    PoutMax = 25.8 - TechnoStep.PoutMax
    PinMax = 10

    # vieux
    #capacité = TechnoStep.capacité
    capacité = 4000.
    capacité_initiale = 2800.
    def __init__(self, nom='Lacs', stock=None,
                 etain=etain, etaout=etaout, PoutMax=PoutMax, PinMax=PinMax,
                 capacité=capacité, H=Techno.H):


        super().__init__(nom=nom, stock=stock,
                         etain=etain, etaout=etaout, PoutMax=PoutMax, PinMax=PinMax,
                         capacité=capacité, H=H)

        if stock is None:
            self.set_stock_et_cons_from_csv()

        self.Pout_Regulation = True

    def Pout(self, k):
        """Renvoie la puissance maximum de décharge à l'heure k """

        if self.Pout_Regulation:
            # on veut un pic verrs Aout avant de revenir au stock de janvier
            kpla = 6 * 30 * 24 # mois d'Ju
            kpic = 10 * 30 * 24 # mois d'Oct
            p_moy = None
            if k > kpic:
                #Novembre à janvier on lache un peu retour à 2500
                horizon_vidage = 24 * 30 *3 # 0 en 1 mois
                objectif = self.capacité_initiale # revenir au stock initial
                kobj = self.H
                inflow_restante = self.recharge[k:].sum()
                p_moy = max(0, (self.stock[k] - objectif + inflow_restante)/(self.H-k))
                """if self.stock[k] + inflow_restante > objectif:
                    p_obj = self.PoutMax
                else:
                    p_obj = 0"""

            elif k > kpla:
                #Juin à Novembre on maintien à 3500 max
                horizon_vidage = 24 * 30 *4  # 0 en 15 jours
                objectif = 3500.
                kobj = kpic
                inflow_restante = self.recharge[k:kpic].sum()
            else :
                #Janvier à Juin on lache et gère le min
                if k < 24*30:
                    # pas trop avant fevrier
                    horizon_vidage = 24 * 30 * 3  # 0 en 15 jours
                else:
                    #là gros pic Fevrier on lache !
                    horizon_vidage = 24 * 10  # 0 en 15 jours
                objectif = 3500.
                kobj = kpla
                inflow_restante = self.recharge[k:kpla].sum()

            # marge stock : est-il possible de revenir au stock initial en fin d'année
            if self.stock[k] + inflow_restante < objectif :
                pout_obj = 0
            else:
                pout_obj = (self.stock[k] - objectif + inflow_restante)

            if (k+horizon_vidage) > self.H:
                inflow_avant_vidage = self.recharge[k:].sum() + self.recharge[0:(k+horizon_vidage-self.H)].sum()
            else:
                inflow_avant_vidage = self.recharge[k:(k+horizon_vidage)].sum()

            # Pout pour atteindre stock 0 en temps heures
            pout_vidage = max(0, (self.stock[k]+inflow_avant_vidage)/horizon_vidage)

            if p_moy is None:
                p_moy = min(pout_obj, pout_vidage)

                if p_moy >= self.PoutMax:
                    p_k = self.PoutMax
                else:
                    p_k = p_moy - min(p_moy, self.PoutMax - p_moy) * np.cos(float(k % 24)/24.*2.*np.pi)
                    #p_k = p_moy * (1-np.cos(float(k % 24)/24.*2.*np.pi))
            else:
                p_k = p_moy

            return min(self.stock[k], p_k, self.PoutMax-self.décharge[k])
        else:
            return min(self.stock[k], self.PoutMax-self.décharge[k])

    def set_Pout_urgent(self):
        self.Pout_Regulation = False

    def set_Pout_regulation(self):
        self.Pout_Regulation = True

    def set_stock_et_cons_from_csv(self, fichier=chemin_donnees + "/lake_inflows.csv"):
        lake = pd.read_csv(fichier, header=None)
        lake.columns = ["month", "prod2"]
        lakeprod = np.array(lake.prod2)

        # Calcul de ce qui est stocke dans les lacs pour chaque mois
        self.stock = np.ones(self.H)*self.capacité_initiale
        k = 0
        for m in range(12):
            ksuiv = k + TechnoLacs.duree_mois[m]
            self.recharge[k:ksuiv] = lakeprod[m] * 1000./self.duree_mois[m]
            k = ksuiv

    def recharger(self, k):
        self.stock[k:] += self.recharge[k]
        if self.stock[k]  > self.capacité:
            surplus = self.stock[k] - self.capacité
        else:
            surplus = 0
        self.recharge[k] = 0
        return surplus

    def produire_minimum(self, k):
        surplus = self.recharger(k)
        produit = self.décharger(k, surplus)

        kpic = 10 * 30 * 24 # mois d'Oct
        if k > kpic:
            objectif = self.capacité_initiale # revenir au stock initial
            kobj = self.H
            inflow_restante = self.recharge[k:].sum()
            p_moy = max(0, (self.stock[k] - objectif + inflow_restante)/(self.H-k))
            produit += self.décharger(k, p_moy)

        return produit

    def décharger(self, k, aproduire):
        """ Decharge les moyens de stockage quand on a besoin d'energie

        Args:
            self : technologie de stockage a utiliser pour la production (batterie, phs, ...)
            k (int) : heure courante
            aproduire (float) : qte d'energie a fournir
            endmonthlake (array) : qte d'energie restante dans les lacs jusqu'a la fin du mois
            executer (boolean) : indique si l'energie dechargee est a prendre en compte pour la production globale (faux pour les echanges internes)
        """
        if aproduire <= 0:
            out = 0

        else:

            vaproduire = min(aproduire, self.Pout(k))

            self.stock[k:] = self.stock[k] - vaproduire/self.etaout
            self.décharge[k] += vaproduire

            out = vaproduire

        return out

def fc_min_max_nuke(k, Pmax=1):
    """ Renvoie la puissance dispo actuellement pour le nucleaire, par rapport a la puissance max

    Args:
        k (int) : heure courante

    Sur ATH : pas de penurie avec 56 centrales min.
    Sur ATL : 28 centrales min. (50%)
    Diviser en 4 ou 8 groupes (plutôt 8 pour les besoins humains)
    1/8 = 0.125, 7/8 = 0.875
    2180, 2920, 3650, 4400, 5130, 5900, 6732, 7580
    Tiers de 8760 : 2920(4*730), 5840, 8460
    DANS le dernier tiers : 50% croissance lineaire min, 25% baisse de 20% prod min/max, 25% arret
    """

    # La production nucleaire est divisee en 8 groupes, chacun a son cycle d'arret.
    # Dans cette fonction, on regarde dans quel partie du cycle on est pour chaque groupe,
    # pour calibrer la production min et max.

    H = 8760
    N = 8
    n = 1 / N

    # Intervalles des 3 parties importantes du cycle, pour chaque groupe
    A_ranges = [((2180 + 6570) % H, (2180 + 8030) % H), ((2920 + 6570) % H, (2920 + 8030) % H),
                ((3650 + 6570) % H, (3650 + 8030) % H), ((4400 + 6570) % H, (4400 + 8030) % H),
                ((5130 + 6570) % H, (5130 + 8030) % H), ((5900 + 6570) % H, (5900 + 8030) % H),
                ((6732 + 6570) % H, (6732 + 8030) % H), ((7580 + 6570) % H, (7580 + 8030) % H)]

    B_ranges = [((2180 + 8030) % H, 2180), ((2920 + 8030) % H, 2920), ((3650 + 8030) % H, 3650),
                ((4400 + 8030) % H, 4400), ((5130 + 8030) % H, 5130), ((5900 + 8030) % H, 5900),
                ((6732 + 8030) % H, 6732), ((7580 + 8030) % H, 7580)]

    C_ranges = [(2180, (2180 + 730) % H), (2920, (2920 + 730) % H), (3650, (3650 + 730) % H),
                (4400, (4400 + 730) % H), (5130, (5130 + 730) % H), (5900, (5900 + 730) % H),
                (6732, (6732 + 730) % H), (7580, (7580 + 730) % H)]

    inA = [lower <= k < upper for (lower, upper) in A_ranges]
    inB = [lower <= k < upper for (lower, upper) in B_ranges]
    inC = [lower <= k < upper for (lower, upper) in C_ranges]

    sMin = 0
    sMax = 0

    # Pour chaque groupe, on regarde sa zone et on ajuste son min et son max
    for i in range(N):
        if inA[i]:
            start = A_ranges[i][0]
            sMin += n * (0.2 + 0.00054795 * (k - start))
            sMax += n * 1
        elif inB[i]:
            start = B_ranges[i][0]
            sMin += n * (1 - 0.00027397260274 * (k - start))
            sMax += n * (1 - 0.00027397260274 * (k - start))
        elif inC[i]:
            sMin += n * 0
            sMax += n * 0
        else:
            sMin += n * 0.2
            sMax += n * 1

    return sMin*Pmax, sMax*Pmax

class TechnoNucleaire(Techno):
    """
        #vieux
         7.6e-6  Meuro/GWh part du combustible dans le prix de l'electricite
                    # nucleaire (7.6€ le MWh)

         Pour le cout combustible voir  :
       https://cereme.fr/wp-content/uploads/2022/07/C-12-Comparaison-des-couts-complets-de-production-de-lelectricite_.pdf
       Induire le cout indirect (B) dans le cout du combustible (A) du tableau cereme

       Je propose
       nucléaire 7,6(A) + 20,1(B) + 0.1 (F) euro/MWh(élec) EPR2 = 27.8

       Si on reagarde ancien nuke
        Nucléare A+B+F = 43,2  €/MWh
    """


    #vieux
    #prix = 7.6e-6  # Meuro/GWh part du combustible dans le prix de l'electricite
                    # nucleaire (7.6€ le MWh)
    #suggéré PACCO
    prix = 43.2e-6   # Meuro/GWh(élec) part du combustible dans le prix de l'electricite (ancien Nuke)


    PoutMaxParUniteEPR2 = infos["EPR2"]["PoutMax"]
    PoutMaxParUniteEPR = infos["centraleNuc"]["PoutMax"]

    ramp_up = 0.25           # % de PoutMax /heure
    ramp_down = ramp_up

    def __init__(self, nom='Nucléaire', PoutMax=None, décharge_init=None,
                 nb_units_EPR=0, nb_units_EPR2=0, H=Techno.H, ramp_up=ramp_up, ramp_down=ramp_down):

        self.nb_units_EPR = nb_units_EPR
        self.nb_units_EPR2 = nb_units_EPR2

        if PoutMax is None:
            PoutMax = (TechnoNucleaire.PoutMaxParUniteEPR * nb_units_EPR +
                       TechnoNucleaire.PoutMaxParUniteEPR2 * nb_units_EPR2)

        self.ramp_up = ramp_up * PoutMax            #GW/h
        self.ramp_down = ramp_down * PoutMax        #GW/h

        super().__init__(nom=nom, stock=None,
                         etain=None, etaout=1, PoutMax=PoutMax, PinMax=None,
                         capacité=None, H=H)

        if décharge_init is not None:
            self.set_décharge_init(décharge_init)

        self.fc_nuke = [fc_min_max_nuke(k, self.PoutMax) for k in range(self.H)]

    def set_décharge_init(self, décharge_init):
        if np.isscalar(décharge_init):
            self.décharge = décharge_init*np.ones(self.H)
        else:
            self.décharge = décharge_init


    def get_pout_effectives(self, k):
        return self.fc_nuke[k]

    def p_min_effective(self, k):
        return self.fc_nuke[k][0]
    def p_max_effective(self, k):
        return self.fc_nuke[k][1]

    def Pout(self, k):
        if k > 0:
            return min(self.p_max_effective(k) - self.décharge[k],
                       self.décharge[k-1]+self.ramp_up - self.décharge[k])
        else:
            return self.p_max_effective(k) - self.décharge[k]

    def Pout_min(self, k):
        if k > 0:
            return max(self.p_min_effective(k) - self.décharge[k],
                       self.décharge[k-1] - self.ramp_down - self.décharge[k])
        else:
            return self.p_min_effective(k) - self.décharge[k]

    def pilote_prod(self, k, aproduire):
        """ Lance la production des centrales nucleaires

        Args:
            self : objet à utiliser pour la production  (ici, Techno Nucleaire)
            k (int) : heure courante
            aproduire (float) : qte d'energie a fournir
        """
        # Si la demande est trop faible ou nulle, on produit quand meme à hauteur de 20%

        le_max = self.Pout(k)
        le_min = self.Pout_min(k)

        if aproduire > le_max:
            temp = le_max
        elif aproduire > le_min:
            temp = aproduire
        else:
            temp = le_min

        self.décharge[k] += temp

        return temp

    def pilot_annule_prod(self, k, aannuler):
        vaannuler = min(aannuler, - self.Pout_min(k))
        self.décharge[k] -= vaannuler
        return vaannuler


def thermProd(tec, k, aproduire):
    """ Lance la production des centrales thermiques

    Args:
        tec : objet à utiliser pour la production  (ici, Techno Thermique)
        k (int) : heure courante
        aproduire (float) : qte d'energie a fournir
    """
    if aproduire <= 0:
        out = 0

    else:
        temp = min(aproduire / tec.etaout, tec.PoutMax / tec.etaout)
        tec.décharge[k] = temp * tec.etaout
        out = aproduire - tec.décharge[k]

    return out


def test_technoLacs():
    import matplotlib.pyplot as plt
    L = TechnoLacs()
    plt.title("Test des lacs")
    plt.subplot(313)
    plt.grid()
    plt.plot(L.recharge, 'k--')
    plt.ylabel('stock avant et après')
    reste = np.zeros(Techno.H)
    aproduire = reste.copy()
    for k in range(Techno.H):
        L.recharger(k)
        L.produire_minimum(k)
        if 2000 < k < 3600:
            val=15
            aproduire[k] +=val
            reste[k] += val - L.décharger(k=k, aproduire=val)

        if 6000 < k < 6400:
            val = 1
            aproduire[k] +=val
            reste[k] += val - L.décharger(k=k, aproduire=val)

        if 6200 < k < 6800:
            val = 1
            aproduire[k] +=val
            reste[k] += val- L.décharger(k=k, aproduire=val)

        if 4000 < k < 5000:
            val = 10
            aproduire[k] += val
            reste[k] += val - L.décharger(k=k, aproduire=val)

        if 8000 < k < 8500:
            val = -5
            aproduire[k] += val
            reste[k] += val - L.décharger(k=k, aproduire=val)
        else:
            val = 0
            aproduire[k] += val
            reste[k] += val - L.décharger(k=k, aproduire=0)

    plt.subplot(311)
    plt.plot(L.stock, 'r')
    plt.subplot(312)
    plt.plot(aproduire, 'b--')
    plt.plot(reste, 'r')
    plt.legend(['aproduire', 'reste'])
    plt.grid()
    plt.subplot(313)
    plt.plot(L.décharge, 'g')
    plt.plot(aproduire-reste, 'b.')
    plt.legend(['décharge(prod)', 'aprod - reste'])
    plt.show()

def test_generique(T=None):
    import matplotlib.pyplot as plt
    N= 50

    if T is None:
        T= Techno(nom="generique", stock=50, etain=0.75, etaout=0.25, PoutMax=1, PinMax=10, capacité=100, H=50)

    astocker = np.zeros(N)
    reste = np.zeros(N)
    Pin = np.zeros(N)
    Pout = np.zeros(N)

    for k in range(N):
        val = 0
        if 10 < k <= 20:
            val = (T.capacité-T.stock[0])/10/T.etain *2
        if 30 < k <= 40:
            val = - T.capacité /10*T.etaout *2

        if val>0:
            reste[k] = val - T.recharger(k,val)
        else:
            reste[k] = -val -T.décharger(k, -val)

        start_surcroit = 32
        if start_surcroit< k <=start_surcroit+10 :
            val += -val / 2.
            reste[k] = val - T.recharger(k, val )

        if start_surcroit+5< k <=start_surcroit+10 :
            val += -val * 2
            reste[k] = val - T.recharger(k, val )

        astocker[k] = val

        Pin[k] += T.Pin(k)
        Pout[k] += T.Pout(k)

    plt.subplot(311)
    plt.plot(T.stock, 'k--')
    plt.grid()
    plt.subplot(312)
    plt.plot(astocker, 'k--')
    plt.plot(-T.décharge,'b')
    plt.plot(T.recharge, 'r')
    plt.plot(reste, 'g--')

    plt.subplot(313)
    plt.plot(astocker, 'k--')
    plt.plot(reste, 'g--')
    plt.show()

def test_technoNucleaire():
    import matplotlib.pyplot as plt

    N = TechnoNucleaire(nb_units_EPR=46, nb_units_EPR2=0, décharge_init=0.1)
    fc_nuke = [N.get_pout_effectives(k) for k in range(1, 365 * 24)]
    aproduire = np.zeros(N.H)
    reste = np.zeros(N.H)
    Pout = np.zeros(N.H)

    for k in range(N.H):
        aproduire[k]=0.2*N.PoutMax
        if 500 < k <= 2000:
            aproduire[k] = aproduire[k-1] + 1/1000.*N.PoutMax
        if 2000 < k <= 3500:
            aproduire[k] = aproduire[k - 1] - 1 / 1000.*N.PoutMax

        reste[k] +=  aproduire[k] - N.pilote_prod(k, aproduire[k])
        if 5000 < k <= 8000:
            reste[k] += 0.4*N.PoutMax - N.pilote_prod(k, 0.4*N.PoutMax)
        if 6000 < k <= 8000:
            reste[k] += 0.2*N.PoutMax - N.pilote_prod(k, 0.2*N.PoutMax)
        if 7000 < k <= 8000:
            reste[k] += 0.4*N.PoutMax - N.pilote_prod(k, 0.4*N.PoutMax)

        Pout[k] = N.Pout(k)

    plt.subplot(211)
    plt.plot(fc_nuke)
    plt.plot(N.décharge,'b-+')
    plt.grid()
    plt.subplot(212)
    plt.plot(aproduire, 'k')
    plt.plot(reste, 'g')
    plt.plot(Pout,'r')
    plt.grid()
    plt.show()


if __name__ == "__main__":
    test_technoLacs()
    #test_technoNucleaire()
    #test_generique()
    #test_generique(TechnoStep(H=50))
    #test_generique(TechnoBatteries(nb_units=1, H=50))
    #test_generique(TechnoGaz(nb_units=10, H=50))

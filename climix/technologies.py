import os
import numpy as np
import pandas as pd


chemin = os.path.dirname(os.path.realpath(__file__))
chemin_donnees = chemin + "/mix_data"

class Techno:
    """Classe regroupant toutes les technologies de stockage et de production pilotables

    """
    H = 24*365
    def __init__(self, nom, stock, décharge, etain, etaout, Pout, Pin, capacité, H=H):
        """ Créateur de la classe
        Args:
            nom (str): nom de la techno
            stock (array) : niveau des stocks a chaque heure
            décharge (array) : ce qui est produit chaque heure
            etain (float) : coefficient de rendement a la charge
            etaout (float) : coefficient de rendement a la decharge
            Pout (float) : capacite installee (flux sortant)
            Pin (float) : capacite de charge (flux entrant)
            vol (float) : capacite maximale de stockage

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

        if décharge is None :
            décharge=0
        if np.isscalar(décharge):
            self.décharge = np.ones(H) * décharge
        else:
            self.décharge = décharge
        self.etain = etain  # . coefficient de rendement à la charge
        self.etaout = etaout  # . coefficient de rendement à la decharge
        self.Pout = Pout  # . capacite installee (flux sortant)
        self.Pin = Pin  # . capacite de charge d'une techno de stockage (flux entrant)
        self.capacité = capacité  # . Capacite maximale de stockage de la techno (Volume max)
        self.H = H

    def charger(self, k, astocker):
        """Recharge les moyens de stockage quand on a trop d'energie

        Args:
            self : technologie de stockage a recharger (batterie, phs, ...)
            k (int) : heure courante
            astocker (float) : qte d'energie a stocker

        Returns:
            out()
        """
        if astocker == 0:
            out = 0

        else:
            temp = min(astocker * self.etain, self.capacité - self.stock[k - 1], self.Pin * self.etain)
            self.stock[k:] = self.stock[k - 1] + temp
            out = astocker - temp / self.etain

        return out


    def décharger(self, k, aproduire, prod=True):
        """ Decharge les moyens de stockage quand on a besoin d'energie

        Args:
            self : technologie de stockage a utiliser pour la production (batterie, phs, ...)
            k (int) : heure courante
            aproduire (float) : qte d'energie a fournir
            endmonthlake (array) : qte d'energie restante dans les lacs jusqu'a la fin du mois
            prod (boolean) : indique si l'energie dechargee est a prendre en compte pour la production globale (faux pour les echanges internes)
        """
        if aproduire <= 0:
            out = 0

        else:
            temp = min(aproduire / self.etaout, self.stock[k], self.Pout / self.etaout)


            if prod:
                self.stock[k:] = self.stock[k] - temp
                self.décharge[k] = temp * self.etaout

            out = aproduire - temp * self.etaout

        return out


class TechnoStep(Techno) :
    def __init__(self, nom='Step', stock=16, décharge=0,
                 etain=0.95, etaout=0.9, Pout=9.3, Pin=9.3, capacité=180, H=Techno.H):

        super().__init__(nom=nom, stock=stock, décharge=décharge,
                         etain=etain, etaout=etaout, Pout=Pout, Pin=Pin,
                         capacité=capacité, H=H)


class TechnoBatteries(Techno):
    def __init__(self, nom='Batteries', stock=None, décharge=0,
                 etain=0.95, etaout=0.9, Pout=None, Pin=None,
                 capacité=180, nb_units=1, H=Techno.H):

        if Pout is None:
            Pout = nb_units / 10. * 20.08
        if Pin is None:
            Pin = Pout
        if capacité is None:
            capacité = nb_units/ 10. * 74.14
        if stock is None:
            stock = capacité/2.

        super().__init__(nom=nom, stock=stock, décharge=décharge,
                         etain=etain, etaout=etaout, Pout=Pout, Pin=Pin,
                         capacité=capacité, H=H)


class TechnoGaz(Techno):
    volume_gaz = 10000000.
    init_gaz = volume_gaz / 2.
    # Methanation : 1 pion = 10 unites de 100 MW = 1 GW
    # T = Techno('Centrale thermique', None, np.zeros(H), None, 1, 0.7725*nbTherm, None, None)
    # Puissance : 1.08 GWe (EDF)
    # Meme rendement

    def __init__(self, nom='Gaz', stock=init_gaz, décharge=0,
                 etain=0.59, etaout=0.45, Pout=34.44, Pin=None,
                 capacité=volume_gaz, nb_units=0, H=Techno.H):

        if Pin is None:
            Pin = nb_units * 1.

        super().__init__(nom=nom, stock=stock, décharge=décharge,
                         etain=etain, etaout=etaout,
                         Pout=Pout, Pin=Pin,
                         capacité=capacité, H=H)


class TechnoLacs(Techno):
    # Puissance centrales territoire : 18.54 GWe repartis sur 24 centrales (EDF)
    # Rendement meca (inutile ici) : ~35% generalement (Wiki)

    horlake = np.array(
        [0, 31,
         31 + 28,
         31 + 28 + 31,
         31 + 28 + 31 + 30,
         31 + 28 + 31 + 30 + 31,
         31 + 28 + 31 + 30 + 31 + 30,
         31 + 28 + 31 + 30 + 31 + 30 + 31 ,
         31 + 28 + 31 + 30 + 31 + 30 + 31 + 31,
         31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30,
         31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 ,
         31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30,
         31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31]) * 24


    def __init__(self, nom='Lacs', stock=None, décharge=0,
                 etain=1, etaout=1, Pout=10, Pin=10,
                 capacité=2000, H=Techno.H):

        self.endmonthlake = np.zeros(H)
        for k in range(12):
            self.endmonthlake[TechnoLacs.horlake[k]:TechnoLacs.horlake[k + 1]] = int(TechnoLacs.horlake[k + 1])

        super().__init__(nom=nom, stock=stock, décharge=décharge,
                         etain=etain, etaout=etaout, Pout=Pout, Pin=Pin,
                         capacité=capacité, H=H)

        if stock is None:
            self.set_stock_from_csv()

    def set_stock_from_csv(self, fichier=chemin_donnees+"/lake_inflows.csv"):
        lake = pd.read_csv(fichier, header=None)
        lake.columns = ["month", "prod2"]
        lakeprod = np.array(lake.prod2)

        # Calcul de ce qui est stocke dans les lacs pour chaque mois
        self.stock = np.zeros(self.H)
        for k in range(12):
            self.stock[TechnoLacs.horlake[k]:TechnoLacs.horlake[k + 1]] = 1000. * lakeprod[k]


    def décharger(self, k, aproduire, prod=True):
        """ Decharge les moyens de stockage quand on a besoin d'energie

        Args:
            self : technologie de stockage a utiliser pour la production (batterie, phs, ...)
            k (int) : heure courante
            aproduire (float) : qte d'energie a fournir
            endmonthlake (array) : qte d'energie restante dans les lacs jusqu'a la fin du mois
            prod (boolean) : indique si l'energie dechargee est a prendre en compte pour la production globale (faux pour les echanges internes)
        """
        if aproduire <= 0:
            out = 0

        else:
            temp = min(aproduire / self.etaout, self.stock[k], self.Pout / self.etaout)

            if prod:
                self.stock[k:int(self.endmonthlake[k])] = self.stock[k] - temp
                self.décharge[k] = temp * self.etaout

            out = aproduire - temp * self.etaout

        return out


def fc_min_max_nuke(k):
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

    return sMin, sMax

class TechnoNucleaire(Techno):

    def __init__(self, nom='Nucléaire', stock=None, décharge=0,
                 etain=None, etaout=1., Pout=None, Pin=None,
                 capacité=None, nb_units_EPR=0, nb_units_EPR2=0, H=Techno.H):

        if Pout is None:
            Pout = 1.08 * nb_units_EPR + 1.67 * nb_units_EPR2

        super().__init__(nom=nom, stock=stock, décharge=décharge,
                         etain=etain, etaout=etaout,
                         Pout=Pout, Pin=Pin,
                         capacité=capacité)

    def get_p_min_max(self, k):
        fc_min, fc_max = fc_min_max_nuke(k)
        P_max = fc_max * self.Pout
        P_min = fc_min * self.Pout
        return P_min, P_max

    def pilote_prod(self, k, aproduire):
        """ Lance la production des centrales nucleaires

        Args:
            self : objet à utiliser pour la production  (ici, Techno Nucleaire)
            k (int) : heure courante
            aproduire (float) : qte d'energie a fournir
        """
        if aproduire <= 0:
            out = 0

        else:
            # Si la demande est trop faible ou nulle, on produit quand meme à hauteur de 20%
            P_min, P_max = self.get_p_min_max(k)

            if aproduire > P_max:
                temp = P_max
            elif aproduire > P_min:
                temp = aproduire
            else:
                temp = P_min

            self.décharge[k] = temp

            out = aproduire - self.décharge[k]

        return out


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
        temp = min(aproduire / tec.etaout, tec.Pout / tec.etaout)
        tec.décharge[k] = temp * tec.etaout
        out = aproduire - tec.décharge[k]

    return out

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    fc_nuke = [fc_min_max_nuke(k) for k in range(1, 365 * 24)]
    plt.plot(fc_nuke)
    plt.show()
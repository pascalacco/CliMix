import numpy as np
from collections import Counter
import sys
import json
import pandas as pd
import os
import datetime

                                #########################
                                ### TOUT EST EN GW(h) ###
                                #########################

np.seterr('raise') # A ENLEVER SUR LE CODE FINAL

# Fonction qui pour un nombre donné renvoie 0 s'il est négatif, et le nombre en question sinon
# 
# @params
# x (float) : nombre à tester
def indic(x):
    return x if x > 0 else 0


# Classe regroupant toutes les technologies de stockage et de production pilotables
#
# @params
# name (str) : nom de la techno
# stored (array) : niveau des stocks a chaque heure
# prod (array) : ce qui est produit chaque heure
# etain (float) : coefficient de rendement a la charge
# etaout (float) : coefficient de rendement a la decharge
# Q (float) : capacite installee (flux sortant)
# S (float) : capacite de charge (flux entrant)
# vol (float) : capacite maximale de stockage
class Techno:
    def __init__(self, name, stored, prod, etain, etaout, Q, S, Vol):
        self.name = name     # nom de la techno
        self.stored = stored # ce qui est stocké
        self.prod = prod     # ce qui est produit
        self.etain = etain     # coefficient de rendement à la charge
        self.etaout = etaout   # coefficient de rendement à la décharge
        self.Q=Q             # capacité installée (flux sortant)
        self.S=S             # capacité de charge d'une techno de stockage (flux entrant)
        self.vol=Vol         # Capacité maximale de stockage de la techno (Volume max)


# Recharge les moyens de stockage quand on a trop d'energie
#
# @params
# tec : technologie de stockage a recharger (batterie, phs, ...)
# k (int) : heure courante
# astocker (float) : qte d'energie a stocker
def load(tec, k, astocker):
    if astocker == 0:
        out = 0

    else:
        temp = min(astocker*tec.etain, tec.vol-tec.stored[k-1], tec.S*tec.etain)
        tec.stored[k:] = tec.stored[k-1] + temp
        out = astocker - temp / tec.etain
    
    return out


# Decharge les moyens de stockage quand on a besoin d'energie
#
# @params
# tec : technologie de stockage a utiliser pour la production (batterie, phs, ...)
# k (int) : heure courante
# aproduire (float) : qte d'energie a fournir
# endmonthlake (array) : qte d'energie restante dans les lacs jusqu'a la fin du mois
# prod (boolean) : indique si l'energie dechargee est a prendre en compte pour la production globale (faux pour les echanges internes)
def unload(tec, k, aproduire, endmonthlake, prod=True):
    if aproduire <= 0:
        out = 0

    else:
        temp = min(aproduire/tec.etaout, tec.stored[k], tec.Q/tec.etaout)

        if tec.name == 'Lake':
            tec.stored[k:int(endmonthlake[k])] = tec.stored[k] - temp
        else:
            tec.stored[k:] = tec.stored[k] - temp

        if prod:
            tec.prod[k] = temp * tec.etaout

        out = aproduire - temp * tec.etaout

    
    return out


# Renvoie la puissance dispo actuellement pour le nucleaire, par rapport a la puissance max
#
# @params
# k (int) : heure courante
def cycle(k):

    # Sur ATH : pas de pénurie avec 56 centrales min.
    # Sur ATL : 28 centrales min. (50%)
    # Diviser en 4 ou 8 groupes (plutôt 8 pour les besoins humains)
    # 1/8 = 0.125, 7/8 = 0.875
    # 2180, 2920, 3650, 4400, 5130, 5900, 6732, 7580
    # Tiers de 8760 : 2920(4*730), 5840, 8460
    # DANS le dernier tiers : 50% croissance linéaire min, 25% baisse de 20% prod min/max, 25% arrêt

    # La production nucléaire est divisée en 8 groupes, chacun a son cycle d'arrêt. 
    # Dans cette fonction, on regarde dans quel partie du cycle on est pour chaque groupe, 
    # pour calibrer la production min et max.

    H = 8760
    N = 8
    n = 1/N
    
    # Intervalles des 3 parties importantes du cycle, pour chaque groupe
    A_ranges = [((2180+6570)%H,(2180+8030)%H), ((2920+6570)%H,(2920+8030)%H), 
               ((3650+6570)%H,(3650+8030)%H), ((4400+6570)%H,(4400+8030)%H),
               ((5130+6570)%H,(5130+8030)%H), ((5900+6570)%H,(5900+8030)%H),
               ((6732+6570)%H,(6732+8030)%H), ((7580+6570)%H,(7580+8030)%H)]
    
    B_ranges = [((2180+8030)%H,2180), ((2920+8030)%H,2920), ((3650+8030)%H,3650),
               ((4400+8030)%H,4400), ((5130+8030)%H,5130), ((5900+8030)%H,5900),
               ((6732+8030)%H,6732), ((7580+8030)%H,7580)]
    
    C_ranges = [(2180, (2180+730)%H), (2920, (2920+730)%H), (3650, (3650+730)%H),
               (4400, (4400+730)%H), (5130, (5130+730)%H), (5900, (5900+730)%H),
               (6732, (6732+730)%H), (7580, (7580+730)%H)]

    inA = [lower <= k < upper for (lower, upper) in A_ranges]
    inB = [lower <= k < upper for (lower, upper) in B_ranges]
    inC = [lower <= k < upper for (lower, upper) in C_ranges]
    
    sMin = 0
    sMax = 0
    
    # Pour chaque groupe, on regarde sa zone et on ajuste son min et son max
    for i in range(N):
        if inA[i]:
            start = A_ranges[i][0]
            sMin += n * (0.2 + 0.00054795*(k-start))
            sMax += n * 1
        elif inB[i]:
            start = B_ranges[i][0]
            sMin += n * (1 - 0.00027397260274*(k-start))
            sMax += n * (1 - 0.00027397260274*(k-start))
        elif inC[i]:
            sMin += n * 0
            sMax += n * 0
        else:
            sMin += n * 0.2
            sMax += n * 1
    
    return (sMin, sMax)


# Lance la production des centrales nucléaires
#
# @params
# tec : objet à utiliser pour la production  (ici, Techno Nucleaire)
# k (int) : heure courante
# aproduire (float) : qte d'energie a fournir
def nucProd(tec, k, aproduire):
    if aproduire <= 0:
        out = 0

    else:
        # Si la demande est trop faible ou nulle, on produit quand même à hauteur de 20%
        MinMax = cycle(k)
        Pmin = MinMax[0]
        Pmax = MinMax[1]
        
        if aproduire > tec.Q/tec.etaout * Pmin:
            temp = min(aproduire/tec.etaout, tec.Q*Pmax/tec.etaout)
            tec.prod[k] = temp * tec.etaout
        else:
            tec.prod[k] = tec.Q / tec.etaout * Pmin
        
        out = aproduire - tec.prod[k]
    
    return out


# Lance la production des centrales thermiques
#
# @params
# tec : objet à utiliser pour la production  (ici, Techno Thermique)
# k (int) : heure courante
# aproduire (float) : qte d'energie a fournir
def thermProd(tec, k, aproduire):
    if aproduire <= 0:
        out = 0

    else:
        temp = min(aproduire/tec.etaout, tec.Q/tec.etaout)
        tec.prod[k] = temp * tec.etaout
        out = aproduire - tec.prod[k]
    
    return out


# 1ere methode de calcul des seuils de stock
#
# @params
# y1 (array) : heures avec surplus
# y2 (array) : heures avec penuries
# y3 (array) : heures sans surplus ni penurie 
# stockmax (float) : capacite max des batteries + phs
def certitudeglobal(y1, y2, y3, stockmax):
    certitude_interval = np.zeros(3)
    
    ##distribution écretage : min, max, moyenne et écart-type
    if y1[y1!=-1].size > 0:
        emoy = np.mean(y1[y1!=-1]) ##moyenne de l'échantillon //
        eetype = np.std(y1[y1!=-1]) ##ecart-type de l'échantillon //
        certitude_interval[1] = emoy - 2.33 * eetype / np.sqrt(len(y1[y1!=-1])) ##99% sur écretage (valeur sup de l'IC)
    else:
        # Si jamais de surplus
        certitude_interval[1] = stockmax - 10

    ##distribution pénurie : min, max, moyenne, écart-type
    if y2[y2!=-1].size > 0:
        pmoy = np.mean(y2[y2!=-1])
        petype = np.std(y2[y2!=-1])
        certitude_interval[0] = pmoy + 1.76 * petype / np.sqrt(len(y2[y2!=-1])) ##98% sur pénurie (valeur inf de l'IC)
    else:
        # Si jamais de pénurie
        certitude_interval[0] = 10
    
    certitude_interval[2] = (certitude_interval[0] + certitude_interval[1]) / 2 ##valeur moyenne entre 98% et 99% 

    return certitude_interval

    
# 2e methode de calcul des seuils de stock
#
# @params
# a (array) : heures avec surplus
# b (array) : heures avec penuries
# c (array) : heures sans surplus ni penurie 
# crit (float) : critere de separation des penuries (ex: si 0.2, on garde 20% des penuries d'un cote, 80% de l'autre)
# mode (str) : vaut 'u' ou 'd' selon qu'on veuille se placer au dessus ou en dessous du seuil
def seuil(a, b, c, crit, mode):
        
    y1 = np.copy(a)
    y2 = np.copy(b)
    y3 = np.copy(c)
    
    
    for i in range (len(y1)):
        y3[i] = -1 if (y1[i]==y3[i] or y2[i]==y3[i]) else y3[i]
        
    
    bestRatio = -1
    bestStock = -1
    
    for s in range(270):
        nbPen = 0
        nbSeuil = 0
    
        for i in range (len(y1)):
            if mode == "u":
                if y1[i] >= s or y3[i] >= s:
                    nbSeuil += 1
                elif y2[i] >= s:
                    nbSeuil += 1
                    nbPen += 1
            else:
                if 0 <= y1[i] <= s or 0 <= y3[i] <= s:
                    nbSeuil += 1
                elif 0 <= y2[i] <= s:
                    nbSeuil += 1
                    nbPen += 1
        
        if nbSeuil != 0:
            ratio = nbPen / nbSeuil
            if abs(ratio-crit) < abs(bestRatio-crit):
                bestRatio = ratio
                bestStock = s
                
    
    return bestStock


# Premiere strat de stockage naive
#
# @params
# prodres (array) : production residuelle sur l'annee
# H (int) : nombre d'heures dans l'annee
# Battery - Nuclear : objets de la classe Techno
# endmonthlake (array) : contient la qte d'energie restante dans les lacs jusqu'a la fin de chaque mois
def StratStockage(prodres, H, Phs, Battery, Gas, Lake, Nuclear, endmonthlake):
    Surplus=np.zeros(H)
    ##Ajout paramètre Penurie
    Manque = np.zeros(H)
    #Definition d'un ordre sur les differentes technologies de stockage et destockage
    Tecstock= {"Phs":Phs , "Battery":Battery , "Gas":Gas}
    Tecstock2= {"Gas":Gas , "Phs":Phs , "Battery":Battery}
        
    Tecdestock= {"Battery":Battery , "Phs":Phs , "Gas":Gas , "Lake":Lake}
    
    for k in range(1,H):
        if prodres[k]>0:
            
            # La production min de nucléaire s'ajoute à la qté d'énergie à stocker
            nucMin = nucProd(Nuclear, k, 0)
            Astocker = prodres[k] + abs(nucMin)
            
            for tec in Tecstock:
                Astocker = load(Tecstock[tec], k, Astocker)

            Surplus[k] = Astocker

        else:
            Aproduire = -prodres[k]
            
            Aproduire = nucProd(Nuclear, k, Aproduire)
            
            for tec in Tecdestock:
                Aproduire = unload(Tecdestock[tec], k, Aproduire, endmonthlake)
                
            ##liste penurie --> pour savoir si il y a pénurie dans la production d'électricité 
            Manque[k] = Aproduire
                
    return Surplus, Manque


# Strat de stockage optimisee
#
# @params
# prodres (array) : production residuelle sur l'annee
# H (int) : nombre d'heures dans l'annee
# Battery - Nuclear : objets de la classe Techno
# I0, I1, I2 (array) : seuils de stockage dirigeant la strat de stockage, et déduits de la strat naive
# endmonthlake (array) : contient la qte d'energie restante dans les lacs jusqu'a la fin de chaque mois
def StratStockagev2(prodres, H, Phs, Battery, Gas, Lake, Nuclear, I0, I1, I2, endmonthlake):
    Surplus=np.zeros(H)
    ##Ajout paramètre Penurie
    Manque = np.zeros(H)
    
    #Definition d'un ordre sur les differentes technologies de stockage et destockage
    Tecstock2= {"Gas":Gas , "Phs":Phs , "Battery":Battery} ##on stocke du gaz zone 1,2
    Tecstock3= {"Phs":Phs , "Battery":Battery , "Gas":Gas} ## zone 3
    Tecstock4 = {"Battery":Battery , "Phs":Phs , "Gas":Gas} ## zone 4
        
    Tecdestock1= {"Battery":Battery , "Phs":Phs , "Gas":Gas , "Lake":Lake} #zone 1
    Tecdestock2 = {"Phs":Phs , "Battery":Battery , "Gas":Gas , "Lake":Lake} ## zone 2
    Tecdestock3 = {"Gas":Gas , "Battery":Battery , "Phs":Phs , "Lake":Lake} ## zone 3,4
    
    for k in range(H):
        stock_PB = Phs.stored[k] + Battery.stored[k]
        
        # Suivant le niveau de stock, on change l'ordre de dé/stockage et on fait du power2gaz ou
        # gaz2power si besoin
        
        if 0 <= stock_PB < I0[k%24] :
            strat_stock = Tecstock4
            strat_destock = Tecdestock3
            qteInit = min(Gas.Q, Phs.S+Battery.S)
            reste = unload(Gas, k, qteInit, endmonthlake, prod=False)
            reste = load(Battery, k, qteInit-reste)
            load(Phs, k, reste)
            
        elif I0[k%24] <= stock_PB < I1[k%24] :
            strat_stock = Tecstock3
            strat_destock = Tecdestock3
            
        elif I1[k%24] <= stock_PB < I2[k%24] :
            strat_stock = Tecstock2
            strat_destock = Tecdestock2
            
        else :
            strat_stock = Tecstock2
            strat_destock = Tecdestock1
            qteInit = min(Phs.Q+Battery.Q, Gas.S)
            reste = unload(Battery, k, qteInit, endmonthlake, prod=False)
            reste = unload(Phs, k, reste, endmonthlake, prod=False)
            load(Gas, k, qteInit-reste)
            
            
        
        if prodres[k]>0 :
            # La production min de nucléaire s'ajoute à la qté d'énergie à stocker
            nucMin = nucProd(Nuclear, k, 0)
            Astocker = prodres[k] + abs(nucMin)
            
            for tec in strat_stock:
                Astocker = load(strat_stock[tec], k, Astocker)

            Surplus[k] = Astocker

        else:
            Aproduire = -prodres[k]

            Aproduire = nucProd(Nuclear, k, Aproduire)

            for tec in strat_destock:
                Aproduire = unload(strat_destock[tec], k, Aproduire, endmonthlake)
            
            ##liste penurie --> pour savoir si il y a pénurie dans la production d'électricité 
            Manque[k]=Aproduire
            
                
    return Surplus, Manque


#Quantification des émissions de CO2 et de la consommation d'électricité dues aux usages
#tour (int): tour de jeu : 1,2,3,4,5
#agr (char): réponse A,B,C,D ou "" à la question sur le type d'alimentation/agriculture
#mob (char): réponse A,B,C,D ou "" à la question sur le type de mobilités
#bat (char): réponse A,B,C,D ou "" à la question sur le type de bâtiment
#ind (char): réponse A,B,C,D ou "" à la question sur le type d'industrie/biens de consommation
#voit (char): réponse A,B,C ou "" à la question catégorie voiture
#pl (char): réponse A ou "" à la question catégorie poids lourds
#avi (char): réponse A,B,C,D ou "" à la question catégorie avion

#vos (int): nombre de kilomètres effectués par une personne dans une année en voiture essence
#voe (int): nombre de kilomètres effectués par une personne dans une année en voiture électrique
#tra (int): nombre de kilomètres effectués par une personne dans une année en train
#vel (int): nombre de kilomètres effectués par une personne dans une année en vélo électrique
#met (int): nombre de kilomètres effectués par une personne dans une année en métro
#bus (int): nombre de kilomètres effectués par une personne dans une année en bus
#bue (int): nombre de kilomètres effectués par une personne dans une année en bus électrique
#voli (int): nombre de vols intérieurs effectués par une personne dans une année
#vole (int): nombre de vols en europe effectués par une personne dans une année
#volin (int): nombre de vols internationnaux effectués par une personne dans une année
#pm (int): nombre de petits meubles neufs achetés par an par une personne
#gm (int): nombre de gros meubles neufs achetés par an par une personne
#pee (int) : nombre de petits équipements électroménagers neufs achetés par an par une personne
#gee (int): nombre de gros équipements électroménagers neufs achetés par an par une personne
#smart (int): nombre de smartphones neufs achetés par an par une personne
#eei (int): nombre d'équipements électroniques intermédiaires neufs achetés par an par une personne
#geel (int) : nombre de gros équipements électroniques neufs achetés par an par une personne

def Usages(tour, agr, mob, bat, ind, voit, pl, avi, vos, voe, tra, vel, met, bus, 
            bue, voli, vole, volin, pm, gm, pee, gee, smart, eei, geel):

    demande = 0 #(en TWh)
    emission = 0 #(en tonnes de CO2)

    #réponse 1 : agr 
    if agr == "A":
        demande += 10
        emission +=0.72
    if agr == "B":
        demande += 29
        emission += 0.89
    if agr == "C":
        demande += 62
        emission += 1.24
    if agr == "D":
        demande += 72
        emission += 1.4
    
    #réponse 2 : mob 
    if mob == "A":
        demande += 150
    if mob == "B":
        demande += 150
    if mob == "C":
        demande += 200
    if mob == "D":
        demande += 225
    
     #réponse 3 : bat 
    if bat == "A":
        demande += 220
    if bat == "B":
        demande += 250
    if bat == "C":
        demande += 300
    if bat == "D":
        demande += 375
    
     #réponse 3 : ind 
    if ind == "A":
        demande += 250
    if ind == "B":
        demande += 250
    if ind == "C":
        demande += 300
    if ind == "D":
        demande += 400

    #réponse voit
    if voit == "A":
        demande += 66
    if ind == "B":
        demande += 90
   
   #réponse pl
    if voit == "A":
        demande += 4.92
 
    #réponse avi
    if avi == "D":
        demande += 2.450

    emission += vos*2e-4 + voe*1e-4 + vel*1e-5 + bus*1e-4 + voli*0.26 + vole*0.47 + volin*1.82 + pm*0.1 + gm*0.3 + pee*0.04 + gee*0.25 + smart*0.03 + eei*0.1 + geel*0.4
    demande += vel*5.3136e-6*(660000)*(tour) + met*1.5e-3 + bue*1.3e-9

    return demande, emission



# Optimisation de stratégie de stockage et de déstockage du Mix énergetique
#
# @params
# scenario (array) : scenario de consommation heure par heure
# titre (int) : annee de deroulement du scenario (25, 30, 35, 40, 45, 50)
# est - cor (dict) : contient le nombre d'installations pour la region concernee
# nbOn - nbBio (int) : nombre de pions eoliennes onshore, offshore, ..., de biomasse
# factStock (float) : facteur de qte de stockage, entre 0 et 1
# cout (int) : cout cumulé des tours précédent
# alea (str) : code d'une carte alea
def mix(scenario, annee, hdf, idf, est, nor, occ, pac, bre, cvl, pll, naq, ara, bfc, cor, 
        nbOn, nbOff, nbPv, nbNuc, nbMeth, nbBio, factStock, alea, save, carte, group):

    H = 8760

    save["carte"] = carte
    save["annee"] = annee + 5
    save["stock"] = factStock

    #actualisation : pour chaque technologie --> nombre posé à ce tour (titre)
    save["nvPions"]["nbeolON"] = nbOn - save["pions"]["nbeolON"]
    save["nvPions"]["nbeolOFF"] = nbOff - save["pions"]["nbeolOFF"]
    save["nvPions"]["nbPV"] = nbPv - save["pions"]["nbPV"]
    save["nvPions"]["nbNuc"] = indic(nbNuc - save["pionsInit"]["nbNuc"] - save["pions"]["nbNuc"])
    save["nvPions"]["nbMeth"] = nbMeth - save["pions"]["nbMeth"]
    save["nvPions"]["nbBio"] = nbBio - save["pions"]["nbBio"]

    save["pions"]["nbeolON"] = nbOn
    save["pions"]["nbeolOFF"] = nbOff
    save["pions"]["nbPV"] = nbPv
    save["pions"]["nbNuc"] = indic(nbNuc - save["pionsInit"]["nbNuc"])
    save["pions"]["nbMeth"] = nbMeth
    save["pions"]["nbBio"] = nbBio

    save["nvPionsParReg"]["hdf"]["Nucleaire"] = indic(hdf["centraleNuc"] - save["pionsParReg"]["hdf"]["Nucleaire"] - save["pionsParRegInit"]["hdf"]["Nucleaire"])
    save["nvPionsParReg"]["idf"]["Nucleaire"] = indic(idf["centraleNuc"] - save["pionsParReg"]["idf"]["Nucleaire"] - save["pionsParRegInit"]["idf"]["Nucleaire"])
    save["nvPionsParReg"]["occ"]["Nucleaire"] = indic(occ["centraleNuc"] - save["pionsParReg"]["occ"]["Nucleaire"] - save["pionsParRegInit"]["occ"]["Nucleaire"])
    save["nvPionsParReg"]["naq"]["Nucleaire"] = indic(naq["centraleNuc"] - save["pionsParReg"]["naq"]["Nucleaire"] - save["pionsParRegInit"]["naq"]["Nucleaire"])
    save["nvPionsParReg"]["est"]["Nucleaire"] = indic(est["centraleNuc"] - save["pionsParReg"]["est"]["Nucleaire"] - save["pionsParRegInit"]["est"]["Nucleaire"])
    save["nvPionsParReg"]["nor"]["Nucleaire"] = indic(nor["centraleNuc"] - save["pionsParReg"]["nor"]["Nucleaire"] - save["pionsParRegInit"]["nor"]["Nucleaire"])
    save["nvPionsParReg"]["bre"]["Nucleaire"] = indic(bre["centraleNuc"] - save["pionsParReg"]["bre"]["Nucleaire"] - save["pionsParRegInit"]["bre"]["Nucleaire"])
    save["nvPionsParReg"]["ara"]["Nucleaire"] = indic(ara["centraleNuc"] - save["pionsParReg"]["ara"]["Nucleaire"] - save["pionsParRegInit"]["ara"]["Nucleaire"])
    save["nvPionsParReg"]["bfc"]["Nucleaire"] = indic(bfc["centraleNuc"] - save["pionsParReg"]["bfc"]["Nucleaire"] - save["pionsParRegInit"]["bfc"]["Nucleaire"])
    save["nvPionsParReg"]["pll"]["Nucleaire"] = indic(pll["centraleNuc"] - save["pionsParReg"]["pll"]["Nucleaire"] - save["pionsParRegInit"]["pll"]["Nucleaire"])
    save["nvPionsParReg"]["cvl"]["Nucleaire"] = indic(cvl["centraleNuc"] - save["pionsParReg"]["cvl"]["Nucleaire"] - save["pionsParRegInit"]["cvl"]["Nucleaire"])
    save["nvPionsParReg"]["cor"]["Nucleaire"] = indic(cor["centraleNuc"] - save["pionsParReg"]["cor"]["Nucleaire"] - save["pionsParRegInit"]["cor"]["Nucleaire"])
    save["nvPionsParReg"]["pac"]["Nucleaire"] = indic(pac["centraleNuc"] - save["pionsParReg"]["pac"]["Nucleaire"] - save["pionsParRegInit"]["pac"]["Nucleaire"])

    save["pionsParReg"]["hdf"]["Nucleaire"] = indic(hdf["centraleNuc"] - save["pionsParRegInit"]["hdf"]["Nucleaire"])
    save["pionsParReg"]["idf"]["Nucleaire"] = indic(idf["centraleNuc"] - save["pionsParRegInit"]["idf"]["Nucleaire"])
    save["pionsParReg"]["occ"]["Nucleaire"] = indic(occ["centraleNuc"] - save["pionsParRegInit"]["occ"]["Nucleaire"])
    save["pionsParReg"]["naq"]["Nucleaire"] = indic(naq["centraleNuc"] - save["pionsParRegInit"]["naq"]["Nucleaire"])
    save["pionsParReg"]["est"]["Nucleaire"] = indic(est["centraleNuc"] - save["pionsParRegInit"]["est"]["Nucleaire"])
    save["pionsParReg"]["nor"]["Nucleaire"] = indic(nor["centraleNuc"] - save["pionsParRegInit"]["nor"]["Nucleaire"])
    save["pionsParReg"]["bre"]["Nucleaire"] = indic(bre["centraleNuc"] - save["pionsParRegInit"]["bre"]["Nucleaire"])
    save["pionsParReg"]["ara"]["Nucleaire"] = indic(ara["centraleNuc"] - save["pionsParRegInit"]["ara"]["Nucleaire"])
    save["pionsParReg"]["bfc"]["Nucleaire"] = indic(bfc["centraleNuc"] - save["pionsParRegInit"]["bfc"]["Nucleaire"])
    save["pionsParReg"]["pll"]["Nucleaire"] = indic(pll["centraleNuc"] - save["pionsParRegInit"]["pll"]["Nucleaire"])
    save["pionsParReg"]["cvl"]["Nucleaire"] = indic(cvl["centraleNuc"] - save["pionsParRegInit"]["cvl"]["Nucleaire"])
    save["pionsParReg"]["cor"]["Nucleaire"] = indic(cor["centraleNuc"] - save["pionsParRegInit"]["cor"]["Nucleaire"])
    save["pionsParReg"]["pac"]["Nucleaire"] = indic(pac["centraleNuc"] - save["pionsParRegInit"]["pac"]["Nucleaire"])


    #actualisation des nouvelles technologies renouvelables posées dans chaque région

    
    save["nvPionsParReg"]["pac"]["panneauPV"] = pac["panneauPV"] - save["pionsParReg"]["pac"]["panneauPV"]
    save["pionsParReg"]["pac"]["panneauPV"] = pac["panneauPV"]

    save["nvPionsParReg"]["pll"]["eolienneOFF"] = pll["eolienneOFF"] - save["pionsParReg"]["pll"]["eolienneOFF"]
    save["pionsParReg"]["pll"]["eolienneOFF"] = pll["eolienneOFF"]


    #carte aléa MEVUAPV  (lancé dé 1 / 2)
    if alea == "MEVUAPV1" or alea == "MEVUAPV2" or alea == "MEVUPV3": 
        save["consoVE"] = 9e4
        scenario += np.ones(H) * (9e4/H)
    
    if alea == "MEVUAPV2" or alea == "MEVUAPV3":
        save["innovPV"] = 0.15

    #carte aléa MEMDA (lancé 3)
    if alea == "MEMDA3":
        scenario = 0.95 * scenario

    fdc_on = pd.read_csv("/var/www/html/flaskapp/mix_data/fdc_on.csv")
    fdc_off = pd.read_csv("/var/www/html/flaskapp/mix_data/fdc_off.csv")
    fdc_pv = pd.read_csv("/var/www/html/flaskapp/mix_data/fdc_pv.csv")
    
    prodOnshore = np.zeros(H)
    prodOffshore = np.zeros(H)
    prodPV = np.zeros(H)

    # Puissance d'un pion
    powOnshore = 1.4
    powOffshore = 2.4
    powPV = 3

    # On fait la somme des prods par region pour chaque techno (FacteurDeCharge * NbPions * PuissanceParPion)
    prodOffshore += np.array(fdc_off.occ) * occ["eolienneOFF"] * powOffshore
    prodOnshore += np.array(fdc_on.occ) * occ["eolienneON"] * powOnshore
    prodPV += np.array(fdc_pv.occ) * occ["panneauPV"] * powPV

    prodOffshore += np.array(fdc_off.naq) * naq["eolienneOFF"] * powOffshore
    prodOnshore += np.array(fdc_on.naq) * naq["eolienneON"] * powOnshore
    prodPV += np.array(fdc_pv.naq) * naq["panneauPV"] * powPV

    prodOffshore += np.array(fdc_off.bre) * bre["eolienneOFF"] * powOffshore
    prodOnshore += np.array(fdc_on.bre) * bre["eolienneON"] * powOnshore
    prodPV += np.array(fdc_pv.bre) * bre["panneauPV"] * powPV

    prodOffshore += np.array(fdc_off.hdf) * hdf["eolienneOFF"] * powOffshore
    prodOnshore += np.array(fdc_on.hdf) * hdf["eolienneON"] * powOnshore
    prodPV += np.array(fdc_pv.hdf) * hdf["panneauPV"] * powPV

    prodOffshore += np.array(fdc_off.pll) * pll["eolienneOFF"] * powOffshore
    prodOnshore += np.array(fdc_on.pll) * pll["eolienneON"] * powOnshore
    prodPV += np.array(fdc_pv.pll) * pll["panneauPV"] * powPV

    prodOnshore += np.array(fdc_on.ara) * ara["eolienneON"] * powOnshore
    prodPV += np.array(fdc_pv.ara) * ara["panneauPV"] * powPV

    prodOnshore += np.array(fdc_on.est) * est["eolienneON"] * powOnshore
    prodPV += np.array(fdc_pv.est) * est["panneauPV"] * powPV

    prodOffshore += np.array(fdc_off.nor) * nor["eolienneOFF"] * powOffshore
    prodOnshore += np.array(fdc_on.nor) * nor["eolienneON"] * powOnshore
    prodPV += np.array(fdc_pv.nor) * nor["panneauPV"] * powPV

    prodOnshore += np.array(fdc_on.bfc) * bfc["eolienneON"] * powOnshore
    prodPV += np.array(fdc_pv.bfc) * bfc["panneauPV"] * powPV

    #carte aléa MEMFDC (lancé 1)
    if alea == "MEMFDC1" or alea == "MEMFDC2" or alea == "MEMFDC3":
        prodOnshore += (np.array(fdc_on.cvl) * cvl["eolienneON"] * powOnshore) * 54/60
    else:
        prodOnshore += np.array(fdc_on.cvl) * cvl["eolienneON"] * powOnshore
    prodPV += np.array(fdc_pv.cvl) * cvl["panneauPV"] * powPV

    prodOffshore += np.array(fdc_off.pac) * pac["eolienneOFF"] * powOffshore
    prodOnshore += np.array(fdc_on.pac) * pac["eolienneON"] * powOnshore
    prodPV += np.array(fdc_pv.pac) * pac["panneauPV"] * powPV

    prodOffshore += np.array(fdc_off.cor) * cor["eolienneOFF"] * powOffshore
    prodOnshore += np.array(fdc_on.cor) * cor["eolienneON"] * powOnshore
    prodPV += np.array(fdc_pv.cor) * cor["panneauPV"] * powPV

    prodOnshore += np.array(fdc_on.idf) * idf["eolienneON"] * powOnshore
    prodPV += np.array(fdc_pv.idf) * idf["panneauPV"] * powPV

    # Aléa +15% prod PV
    prodPV += save["innovPV"] * prodPV



    # Definition des productions électriques des rivières et lacs 
    coefriv = 13
    river = pd.read_csv("/var/www/html/flaskapp/mix_data/run_of_river.csv", header=None)
    river.columns = ["heures", "prod2"]
    rivprod = np.array(river.prod2) * coefriv

    lake = pd.read_csv("/var/www/html/flaskapp/mix_data/lake_inflows.csv", header=None)
    lake.columns = ["month", "prod2"]
    lakeprod = np.array(lake.prod2)

    # Calcul de ce qui est stocké dans les lacs pour chaque mois
    horlake = np.array([0,31,31+28,31+28+31,31+28+31+30,31+28+31+30+31,31+28+31+30+31+30,31+28+31+30+31+30+31\
                ,31+28+31+30+31+30+31+31,31+28+31+30+31+30+31+31+30,31+28+31+30+31+30+31+31+30+31\
                ,31+28+31+30+31+30+31+31+30+31+30,31+28+31+30+31+30+31+31+30+31+30+31])*24

    storedlake = np.zeros(H)
    endmonthlake = np.zeros(H)
    for k in range(12):
        storedlake[horlake[k]:horlake[k+1]] = 1000*lakeprod[k]
    for k in range(12):
        endmonthlake[horlake[k]:horlake[k+1]] = int(horlake[k+1])


    # Calcul de la production residuelle
    # prodresiduelle = prod2006_offshore + prod2006_onshore + prod2006_pv + rivprod - scenario
    prodresiduelle = prodOffshore + prodOnshore + prodPV + rivprod - scenario


    # Techno params : name, stored, prod, etain, etaout, Q, S, vol

    initGaz = 80000
    gazBiomasse = nbBio * 2 * 0.1 * 0.71 * 6200

    #carte aléa MEMFDC (lancé 2 / 3)
    if alea == "MEMFDC2" or alea == "MEMFDC3":
        gazBio -= 0

    # Definition des differentes technologies
    # Methanation : 1 pion = 10 unités de 100 MW = 1 GW
    P=Techno('Phs', np.ones(H)*16, np.zeros(H), 0.95, 0.9, 9.3, 9.3, 180)
    B=Techno('Battery', np.ones(H)*2, np.zeros(H), 0.9, 0.95, factStock/10*20.08, factStock/10*20.08, factStock/10*74.14)
    G=Techno('Gaz', np.ones(H)*(initGaz+gazBiomasse), np.zeros(H), 0.59, 0.45, 34.44, 1*nbMeth, 125000)    
    L=Techno('Lake', storedlake, np.zeros(H), 1, 1, 10, 10, 2000)

    # Puissance centrales territoire : 18.54 GWe répartis sur 24 centrales (EDF)
    # Rendement méca (inutile ici) : ~35% généralement (Wiki)
    # T = Techno('Centrale thermique', None, np.zeros(H), None, 1, 0.7725*nbTherm, None, None)
    
    # Puissance : 1.08 GWe (EDF)
    # Même rendement
    #réacteurs nucléaires effectifs qu'après 1 tour
    nbprodNuc = (nbNuc-save["nvPions"]["nbNuc"])
    N = Techno('Réacteur nucléaire', None, np.zeros(H), None, 1, 1.08*nbprodNuc, None, None)
    
    
    if alea == "MEMFDC3" :
        N.Q *= 45 / 60

        
    # résultats de la strat initiale
    # Renvoie Surplus,Pénurie et met à jour Phs,Battery,Methanation,Lake,Therm,Nuc
    s, p = StratStockage(prodresiduelle, H, P, B, G, L, N, endmonthlake)
    
    
    #############################
    ## NUAGES DE POINTS POUR OPTIMISER LE STOCKAGE
    
    stockage_PB = np.zeros(365) ##liste qui va servir à enregister les stockages Phs + Battery à l'heure H pour tous les jours
    
    stockmax = B.vol + P.vol ##stockage maximum total = max total stockage Phs + max total stockage Battery    
    
    ##listes pour écrêtage : x1 enregistre les jours où le lendemain il y a écrêtage
    ##y1 enregistre la valeur du stock Phs + Battery où le lendemain il y a écrêtage
    x1 = np.ones(365)*(-1)
    y1 = np.ones(365)*(-1)
    
    ##pareil que précèdemment mais pour lendemains avec pénurie
    x2 = np.ones(365)*(-1)
    y2 = np.ones(365)*(-1)
    
    ##pareil que précèdemment mais pour lendemains avec demande satisfaite et sans perte
    x3 = np.ones(365)*(-1)
    y3 = np.ones(365)*(-1)
    
    ##on enlevera les -1 des listes x1, x2, x3, y1, y2, y3 pour ne récupérer que les points essentiels
        
    StockPB = P.stored + B.stored ##valeur des deux stocks 
    
    
    ###############################################################################
    ##Certitude interval pour toutes les heures
    certitude_interval_inf = np.zeros(24)
    certitude_interval_sup = np.zeros(24)
    certitude_interval_med = np.zeros(24)
    
    seuils_top = np.zeros(24)
    seuils_mid = np.zeros(24)
    seuils_bot = np.zeros(24)
    
    for h1 in range(24):
        for jour in range(365): ##on regarde tous les jours de l'année
        
            stockage_PB[jour]=StockPB[jour*24 + h1] #Au jour jour, valeur du stock Phs + Battery
        
            ##on regarde dans les 24h qui suivent si il y a écrêtage, pénurie ou aucun des deux
            for h2 in range(24): 
                t = (jour*24 + h1 + h2) % H
                
                if s[t] > 0 and StockPB[t] >= stockmax : ##cas écrêtage
                    x1[jour] = jour + 1 ##on note le jour précèdant jour avec écrêtage
                    y1[jour] = stockage_PB[jour] ##on note le stock du jour précèdant jour avec écrêtage
            
                elif p[t] > 0 : ##cas pénurie
                    x2[jour] = jour + 1 ##mêmes explications mais pour pénurie
                    y2[jour] = stockage_PB[jour]
                
                else : ##cas ni écrêtage, ni pénurie
                    x3[jour] = jour + 1 ##mêmes explications mais avec ni écrêtage, ni pénurie
                    y3[jour] = stockage_PB[jour]
                
                if x1[jour] == x2[jour]: ##si écretage et pénurie le même jour, on considère que c'est une pénurie 
                    x1[jour] = -1
                    y1[jour] = -1
            
            
        int_glob = certitudeglobal(y1, y2, y3, stockmax)
        certitude_interval_inf[h1] = int_glob[0]
        certitude_interval_sup[h1] = int_glob[1]
        certitude_interval_med[h1] = int_glob[2]
        
        seuils_top[h1] = seuil(y1, y2, y3, 0.02, "u")
        seuils_bot[h1] = seuil(y1, y2, y3, 0.9, "d")
        seuils_mid[h1] = (seuils_top[h1] + seuils_bot[h1]) / 2
        
    
        
        
    # Renvoie Surplus,Pénurie, et met à jour les technos
    
    #Décommenter pour méthode 1 (intervalles de confiance)
    s, p = StratStockagev2(prodresiduelle, H, P, B, G, L, N,
                        certitude_interval_inf, certitude_interval_med, certitude_interval_sup, endmonthlake)
    
    #Décommenter pour méthode 2 (recherche itérative du meilleur seuil)
    #s,p=StratStockagev2(prodresiduelle, H, P, B, M, L, T, N,
    #                    seuils_bot, seuils_mid, seuils_top, endmonthlake)
    
    
    ####Demande des choix de la fiche Usage à l'utilisateur
    # choix_utilisateur = input("Entrez les valeurs séparées par des espaces : ")

    # # Diviser la chaîne en valeurs individuelles
    # liste = choix_utilisateur.split(',')

    # valeurs = [float(valeur) for valeur in liste]

    # # Appeler la fonction avec les valeurs fournies par l'utilisateur
    # d, e = Usages(valeurs)

    

    # Infos qu'on peut retourner (plusieurs axes temporels et 2 stratégies sont possibles):
    # - Stock PHS / Batteries 
    # - Combien de surpus / pénurie ***
    # - Evolution des seuils
    # - (Mix des 2 premiers points)
    # - Stocks de gaz ***
    # - Courbes de production X demande ***
    # - Prod résiduelle
    # - CO2 ***

    prodOn = int(np.sum(prodOnshore))
    prodOff = int(np.sum(prodOffshore))
    prodPv = int(np.sum(prodPV))
    prodEau = int(np.sum(L.prod + rivprod))
    prodNuc = int(np.sum(N.prod))
    prodGaz = int(np.sum(G.prod))
    prodPhs = int(np.sum(P.prod))
    prodBat = int(np.sum(B.prod))

    


    prodTotale = prodOn + prodOff + prodPv + prodEau + prodNuc + prodGaz + prodPhs + prodBat


    ##calcul des productions par région
    nbTherm = 20

    ##Occitanie
    popOCC = 0.09 ##pourcentage population
    prodOCC = (np.array(fdc_off.occ)*occ["eolienneOFF"]*powOffshore + 
                np.array(fdc_on.occ)*occ["eolienneON"]*powOnshore + 
                np.array(fdc_pv.occ)*occ["panneauPV"]*powPV + 
                (occ["centraleNuc"]-save["nvPionsParReg"]["occ"]["Nucleaire"]) *prodNuc/nbprodNuc +
                save["pionsParRegInit"]["occ"]["Thermique"] * prodGaz / nbTherm)

    ##Nouvelle-Aquitaine
    popNA = 0.09
    prodNA = (np.array(fdc_off.naq)*naq["eolienneOFF"]*powOffshore + 
                np.array(fdc_on.naq)*naq["eolienneON"]*powOnshore + 
                np.array(fdc_pv.naq)*naq["panneauPV"]*powPV + 
                (naq["centraleNuc"]-save["nvPionsParReg"]["naq"]["Nucleaire"]) *prodNuc/nbprodNuc + 
                save["pionsParRegInit"]["naq"]["Thermique"] * prodGaz / nbTherm)

    ##Bretagne
    popBRE = 0.05
    prodBRE = (np.array(fdc_off.bre)*bre["eolienneOFF"]*powOffshore +
                np.array(fdc_on.bre)*bre["eolienneON"]*powOnshore +
                np.array(fdc_pv.bre)*bre["panneauPV"]*powPV + 
                (bre["centraleNuc"]-save["nvPionsParReg"]["bre"]["Nucleaire"]) *prodNuc/nbprodNuc + 
                save["pionsParRegInit"]["bre"]["Thermique"] * prodGaz / nbTherm)

    ##Haut-de-France
    popHDF = 0.09
    prodHDF = (np.array(fdc_off.hdf)*hdf["eolienneOFF"]*powOffshore +
                np.array(fdc_on.hdf)*hdf["eolienneON"]*powOnshore +
                np.array(fdc_pv.hdf)*hdf["panneauPV"]*powPV + 
                (hdf["centraleNuc"]-save["nvPionsParReg"]["hdf"]["Nucleaire"]) *prodNuc/nbprodNuc + 
                save["pionsParRegInit"]["hdf"]["Thermique"] * prodGaz / nbTherm)

    ##Pays de la Loire
    popPDL = 0.06
    prodPDL = (np.array(fdc_off.pll)*pll["eolienneOFF"]*powOffshore +
                np.array(fdc_on.pll)*pll["eolienneON"]*powOnshore +
                np.array(fdc_pv.pll)*pll["panneauPV"]*powPV + 
                (pll["centraleNuc"]-save["nvPionsParReg"]["pll"]["Nucleaire"]) *prodNuc/nbprodNuc + 
                save["pionsParRegInit"]["pll"]["Thermique"] * prodGaz / nbTherm)

    ##Auvergne-Rhône-Alpes
    popARA = 0.12
    prodARA = (np.array(fdc_on.ara)*ara["eolienneON"]*powOnshore +
                np.array(fdc_pv.ara)*ara["panneauPV"]*powPV +
                (ara["centraleNuc"]-save["nvPionsParReg"]["ara"]["Nucleaire"]) *prodNuc/nbprodNuc + 
                save["pionsParRegInit"]["ara"]["Thermique"] * prodGaz / nbTherm)

    ##Grand Est
    popGE = 0.08
    prodGE = (np.array(fdc_on.est)*est["eolienneON"]*powOnshore +
                np.array(fdc_pv.est)*est["panneauPV"]*powPV +
                (est["centraleNuc"]-save["nvPionsParReg"]["est"]["Nucleaire"]) *prodNuc/nbprodNuc + 
                save["pionsParRegInit"]["est"]["Thermique"] * prodGaz / nbTherm)

    ##Normandie
    popNOR = 0.05
    prodNOR = (np.array(fdc_off.naq)*nor["eolienneOFF"]*powOffshore +
                np.array(fdc_on.nor)*nor["eolienneON"]*powOnshore +
                np.array(fdc_pv.nor)*nor["panneauPV"]*powPV + 
                (nor["centraleNuc"]-save["nvPionsParReg"]["nor"]["Nucleaire"]) *prodNuc/nbprodNuc + 
                save["pionsParRegInit"]["nor"]["Thermique"] * prodGaz / nbTherm)

    ##Bourgogne-Franche-Comté
    popBFC = 0.04
    prodBFC = (np.array(fdc_on.bfc)*bfc["eolienneON"]*powOnshore +
                np.array(fdc_pv.bfc)*bfc["panneauPV"]*powPV +
                (bfc["centraleNuc"]-save["nvPionsParReg"]["bfc"]["Nucleaire"]) *prodNuc/nbprodNuc + 
                save["pionsParRegInit"]["bfc"]["Thermique"] * prodGaz / nbTherm)

    ##Centre Val de Loire
    popCVL = 0.04
    prodCVL = (np.array(fdc_on.cvl)*cvl["eolienneON"]*powOnshore +
                np.array(fdc_pv.cvl)*cvl["panneauPV"]*powPV +
                (cvl["centraleNuc"]-save["nvPionsParReg"]["cvl"]["Nucleaire"]) *prodNuc/nbprodNuc + 
                save["pionsParRegInit"]["cvl"]["Thermique"] * prodGaz / nbTherm)

    ##PACA
    popPAC = 0.08
    prodPAC = (np.array(fdc_off.pac)*pac["eolienneOFF"]*powOffshore +
                np.array(fdc_on.pac)*pac["eolienneON"]*powOnshore +
                np.array(fdc_pv.pac)*pac["panneauPV"]*powPV + 
                (pac["centraleNuc"]-save["nvPionsParReg"]["pac"]["Nucleaire"]) *prodNuc/nbprodNuc + 
                save["pionsParRegInit"]["pac"]["Thermique"] * prodGaz / nbTherm)

    ##Ile-de-France
    popIDF = 0.19
    prodIDF = (np.array(fdc_on.idf)*idf["eolienneON"]*powOnshore +
                np.array(fdc_pv.idf)*idf["panneauPV"]*powPV +
                (idf["centraleNuc"]-save["nvPionsParReg"]["idf"]["Nucleaire"]) *prodNuc/nbprodNuc + 
                save["pionsParRegInit"]["idf"]["Thermique"] * prodGaz / nbTherm)

    ##Corse
    popCOR = 0.005
    prodCOR = (np.array(fdc_off.cor)*cor["eolienneOFF"]*powOffshore +
                np.array(fdc_on.cor)*cor["eolienneON"]*powOnshore +
                np.array(fdc_pv.cor)*cor["panneauPV"]*powPV + 
                (cor["centraleNuc"]-save["nvPionsParReg"]["cor"]["Nucleaire"]) *prodNuc/nbprodNuc + 
                save["pionsParRegInit"]["cor"]["Thermique"] * prodGaz / nbTherm)

    ##production totale sur le territoire
    prod = prodOCC + prodNA + prodBRE + prodHDF + prodPDL + prodARA + prodGE + prodNOR + prodBFC + prodCVL + prodPAC + prodIDF + prodCOR

    ##calcul des ratios (prod de la région/pros totale --> heure par heure)
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
        ratioOCC[i] = prodOCC[i]/prod[i]
        ratioNA[i] = prodNA[i]/prod[i]
        ratioBRE[i] = prodBRE[i]/prod[i]
        ratioHDF[i] = prodHDF[i]/prod[i]
        ratioPDL[i] = prodPDL[i]/prod[i]
        ratioARA[i] = prodARA[i]/prod[i]
        ratioGE[i] = prodGE[i]/prod[i]
        ratioNOR[i] = prodNOR[i]/prod[i]
        ratioBFC[i] = prodBFC[i]/prod[i]
        ratioCVL[i] = prodCVL[i]/prod[i]
        ratioPAC[i] = prodPAC[i]/prod[i]
        ratioIDF[i] = prodIDF[i]/prod[i]
        ratioCOR[i] = prodCOR[i]/prod[i]
    
    # print(ratioOCC)
    ##différence des rations prod et ratios pop régions par régions
    
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

    diffOCC = ratioOCC - popOCC*np.ones(H)
    diffNA = ratioNA - popNA*np.ones(H)
    diffBRE = ratioBRE - popBRE*np.ones(H)
    diffHDF = ratioHDF - popHDF*np.ones(H)
    diffPDL = ratioPDL - popPDL*np.ones(H)
    diffARA = ratioARA - popARA*np.ones(H)
    diffGE= ratioGE - popGE*np.ones(H)
    diffNOR = ratioNOR - popNOR*np.ones(H)
    diffBFC = ratioBFC - popBFC*np.ones(H)
    diffCVL = ratioCVL - popCVL*np.ones(H)
    diffPAC = ratioPAC - popPAC*np.ones(H)
    diffIDF = ratioIDF - popIDF*np.ones(H)
    diffCOR = ratioCOR - popCOR*np.ones(H)

    ##moyenne sur les heures de l'année des différences
    moyOCC = np.sum(diffOCC)/8760*100
    moyNA = np.sum(diffNA)/8760*100
    moyBRE = np.sum(diffBRE)/8760*100
    moyHDF = np.sum(diffHDF)/8760*100
    moyPDL = np.sum(diffPDL)/8760*100
    moyARA = np.sum(diffARA)/8760*100
    moyGE = np.sum(diffGE)/8760*100
    moyNOR = np.sum(diffNOR)/8760*100
    moyBFC = np.sum(diffBFC)/8760*100
    moyCVL = np.sum(diffCVL)/8760*100
    moyPAC = np.sum(diffPAC)/8760*100
    moyIDF = np.sum(diffIDF)/8760*100
    moyCOR = np.sum(diffCOR)/8760*100

    moyAbsOCC = np.sum(np.abs(diffOCC))/8760*100
    moyAbsNA = np.sum(np.abs(diffNA))/8760*100
    moyAbsBRE = np.sum(np.abs(diffBRE))/8760*100
    moyAbsHDF = np.sum(np.abs(diffHDF))/8760*100
    moyAbsPDL = np.sum(np.abs(diffPDL))/8760*100
    moyAbsARA = np.sum(np.abs(diffARA))/8760*100
    moyAbsGE = np.sum(np.abs(diffGE))/8760*100
    moyAbsNOR = np.sum(np.abs(diffNOR))/8760*100
    moyAbsBFC = np.sum(np.abs(diffBFC))/8760*100
    moyAbsCVL = np.sum(np.abs(diffCVL))/8760*100
    moyAbsPAC = np.sum(np.abs(diffPAC))/8760*100
    moyAbsIDF = np.sum(np.abs(diffIDF))/8760*100
    moyAbsCOR = np.sum(np.abs(diffCOR))/8760*100



    nbS = 0
    nbP = 0

    listeSurplusQuotidien = [0] * 365
    listeSurplusHoraire = [0] * 24

    listePenuriesQuotidien = [0] * 365
    listePenuriesHoraire = [0] * 24

    for i in range(len(s)):
        if s[i] > 0:
            nbS += 1
            listeSurplusQuotidien[i//24] += 1
            listeSurplusHoraire[i%24] += 1
        if p[i] > 0:
            nbP += 1
            listePenuriesQuotidien[i//24] += 1
            listePenuriesHoraire[i%24] += 1


    consoGaz = G.stored[0] - G.stored[8759]
    prodGazFossile = 0 if consoGaz < gazBiomasse else (consoGaz-gazBiomasse)*G.etaout

    EmissionCO2 = prodOn*10 + prodOff*9 + prodPv*55 + prodEau*10 + prodNuc*6 + prodGazFossile*443 #variable EmissionCO2
    save["co2"].append(EmissionCO2)
    demande = np.sum(scenario) #variable demande
    

    prixGaz = 324.6e-6 #prix de l'électricité produite à partir du gaz/charbon --> moyenne des deux (35€ le MWh)
    prixNuc = 7.6e-6 #part du combustible dans le prix de l'électricité nucléaire (7.6€ le MWh)

    #carte alea MEGC (lancé 1 / 3)
    if alea == "MEGC1" or alea == "MEGC2" or alea == "MEGC3":
        prixGaz *= 1.5 #alea1
    
    
    if alea == "MEGC3":
        prixNuc *= 1.4 #alea3


    #carte alea MEMP (lancé 3)
    if alea == "MEMP3":
        prixGaz *= 1.3
        prixNuc *= 1.2

    #variable cout (Md€) --> pour le tour titre
    cout = (save["nvPions"]["nbeolON"] * 3.5 + 
            save["nvPions"]["nbeolOFF"] * 1.2 + 
            save["nvPions"]["nbPV"] * 3.6 + 
            save["nvPions"]["nbNuc"] * 8.6 +
            save["nvPions"]["nbBio"] * 0.12 +
            (G.S * 0.004825) +
            (B.Q * 0.0012) / 0.003 + 
            (P.Q * 0.455) / 0.91 + 
            (prodNuc * prixNuc) +
            (prodGazFossile * prixGaz))


    #budget à chaque tour sauf si carte évènement bouleverse les choses
    budget = 80

    #carte alea MEVUAPV : lancé 3
    if alea == "MEVUAPV3":
        budget -= 10

    #carte MEMDA : lancé 1 / 2
    if alea == "MEMDA1" or alea == "MEMDA2" or alea == "MEMDA3":
        budget += 3.11625

    if alea == "MEMDA2" or alea == "MEMDA3":
        cout -= 1.445
    
    #carte MEGDT : lancé 1 / 3
    if alea == "MEGDT1" or alea == "MEGDT2" or alea == "MEGDT3":
        cout += 1/3*save["nvPionsParReg"]["pac"]["panneauPV"]*3.6

    if alea == "MEGDT3":
        cout += save["nvPionsParReg"]["pll"]["eolienneOFF"]*1.2

    
    Sol = nbOn*300 + nbOff*400 + nbPv*26 + nbNuc*1.5 + nbBio*0.8 #occupation au sol de toutes les technologies (km2)


    Uranium = save["scores"]["Uranium"] #disponibilité Uranium initiale
    if nbNuc > 0:
        Uranium -= 10 #à chaque tour où on maintient des technos nucléaires
    if save["nvPions"]["nbNuc"] > 0:
        Uranium -= 5*save["nvPions"]["nbNuc"]/2 #à chaque paire de réacteurs posées sur le territoire
    #carte aléa MEGC (lancé 2)
    if alea == "MEGC2" or alea == "MEGC3":
        Uranium -= 10 
    
    save["scores"]["Uranium"] = Uranium #actualisation du score Uranium


    Hydro = save["scores"]["Hydro"]#disponibilité Hydrocarbures et Charbon
    if prodGazFossile > 0:
        Hydro -= 20 #à chaque tour où on consomme du gaz fossile
    
    #carte aléa MEMP (lancé 2)
    if alea == "MEMP2" or alea == "MEMP3":
        Hydro -= 20

    save["scores"]["Hydro"] = Hydro #actualisation du score Hydro
    

    Bois = save["scores"]["Bois"]#disponibilité Bois
    if nbBio > 0:
        Bois -= nbBio + 1/2*Bois #au nombre de centrales Biomasse on enlève 1 quantité de bois --> au tour suivant 1/2 des stocks sont récupérés
    #carte aléa MEMP (lancé 1)
    if alea == "MEMP1" or alea == "MEMP2" or alea == "MEMP3":
        Bois -= 20

    save["scores"]["Bois"] = Bois #actualisation du score Bois
        

    dechet = save["scores"]["Dechet"]
    # dechet += nbTherm*2 + nbNuc*1 #déchets générés par les technologies Nucléaires et Thermiques
    dechet += nbNuc
    save["scores"]["Dechet"] = dechet

    capmax_info = save["capacite"]
    #carte alea MECS (lancé 1 / 2)
    if alea == "MECS1" or alea == "MECS2" or alea == "MECS3":
        for k in capmax_info:
            capmax_info[k]["eolienneON"] = int(capmax_info[k]["eolienneON"] * 0.4)

    if alea == "MECS2" or alea == "MECS3":
        capmax_info["occ"]["eolienneON"] *= 2
        capmax_info["occ"]["panneauPV"] *= 2

    #carte alea MEGDT (lancé 2)
    if alea == "MEGDT2" or alea == "MEGDT3":
        capmax_info["naq"]["eolienneOFF"] += 1
        capmax_info["pac"]["eolienneOFF"] += 1
    
    save["capacite"] = capmax_info

    for k in capmax_info : 
        if (nbOn > capmax_info[k]["eolienneON"] 
            or nbOff > capmax_info[k]["eolienneOFF"] 
            or nbPv > capmax_info[k]["panneauPV"]-11*nbOn
            or nbBio > capmax_info[k]["biomasse"]-33*nbOn-3*nbPv) :
            print("vous empiétez sur des territoires agricoles ou surfaces maritimes --> mécontentement de la population !!!")



    #modification du fichier save
    with open("/var/www/html/flaskapp/game_data/groupe{}/save_tmp.json".format(group), "w") as output:
        json.dump(save, output)


    result = {"carte":carte, 
                "annee":annee, 
                "alea":alea, 
                "cout":round(cout), 
                "sol":round(Sol/551695*100, 2),
                "stockGaz":list(G.stored),
                "biogaz":gazBiomasse,
                "demande":int(demande), "production":prodTotale,
                "scoreUranium":Uranium, "scoreHydro":Hydro, "scoreBois":Bois, "scoreDechets":dechet,
                "prodEolienneON":prodOn, "puissanceEolienneON":round(nbOn*powOnshore, 2),
                "prodEolienneOFF":prodOff, "puissanceEolienneOFF":round(nbOff*powOffshore, 2),
                "prodPV":prodPv, "puissancePV":round(nbPv*powPV, 2),
                "prodHydraulique":prodEau,
                "prodNucleaire":prodNuc, "puissanceNucleaire":round(N.Q, 2),
                "prodGaz":prodGaz, "puissanceGaz":round(G.Q, 2),
                "prodPhs":prodPhs, "puissancePhs":round(P.Q, 2),
                "prodBatterie":prodBat, "puissanceBatterie":round(B.Q, 2),
                "co2":save["co2"],
                "nbSurplus":nbS, "nbPenuries":nbP,
                "surplusQuotidien":listeSurplusQuotidien, "surplusHoraire":listeSurplusHoraire,
                "penuriesQuotidien":listePenuriesQuotidien, "penuriesHoraire":listePenuriesHoraire,
                "transfert":{"occ":int(round(moyOCC)),
                                "naq":int(round(moyNA)),
                                "bre":int(round(moyBRE)),
                                "hdf":int(round(moyHDF)),
                                "pll":int(round(moyPDL)),
                                "ara":int(round(moyARA)),
                                "est":int(round(moyGE)),
                                "nor":int(round(moyNOR)),
                                "bfc":int(round(moyBFC)),
                                "cvl":int(round(moyCVL)),
                                "pac":int(round(moyPAC)),
                                "idf":int(round(moyIDF)),
                                "cor":int(round(moyCOR))
                }
    }


    return result



# Fonction principale
#
# @params
# scenario (str) : au choix entre ADEME, RTE et Negawatt
# tour (int) : valeur parmi 25, 30, .., 45, 50
# est - cor (dict) : contient le nombre d'installations pour la region concernee
# nbOn - nbBio (int) : nombre de pions eoliennes onshore, offshore, ..., de biomasse
# factStock (float) : facteur de qte de stockage, entre 0 et 1
# alea (str) : code d'une carte alea        
def strat_stockage_main(data, group):
    nbNuc = 0
    nbMeth = 0
    nbBio = 0
    nbOn = 0
    nbOff = 0
    nbPv = 0

    # Infos sur les unités de data :
    # eolienneON --> 1 unité = 10 parcs = 700 eoliennes
    # eolienneOFF --> 1 unité = 5 parcs = 400 eoliennes
    # panneauPV --> 1 unité = 10 parcs = 983 500 modules
    # centraleTherm --> 1 unité = 1 centrale
    # centraleNuc --> 1 unité = 1 réacteur
    # biomasse --> 1 unité = une fraction de flux E/S en méthanation

    for k in data:
        if k!="annee" and k!="alea" and k!="stock" and k!="carte":
            nbNuc += data[k]["centraleNuc"]
            nbMeth += data[k]["methanation"]
            nbBio += data[k]["biomasse"]
            nbOn += data[k]["eolienneON"]
            nbOff += data[k]["eolienneOFF"]
            nbPv += data[k]["panneauPV"]


    # Definition des scenarios (Negawatt, ADEME, RTE pour 2050)
    # Les autres scenarios sont faits mains à partir des données de Quirion

    ADEME = pd.read_csv("/var/www/html/flaskapp/mix_data/ADEME_25-50.csv", header=None)
    ADEME.columns = ["heures", "d2050", "d2045", "d2040", "d2035", "d2030", "d2025"]

    RTE = pd.read_csv("/var/www/html/flaskapp/mix_data/RTE_25-50.csv", header=None)
    RTE.columns = ["heures", "d2050", "d2045", "d2040", "d2035", "d2030", "d2025"]

    NEGAWATT = pd.read_csv("/var/www/html/flaskapp/mix_data/NEGAWATT_25-50.csv", header=None)
    NEGAWATT.columns = ["heures", "d2050", "d2045", "d2040", "d2035", "d2030", "d2025"]

    ScenarList = {"ADEME":ADEME , "RTE":RTE , "NEGAWATT":NEGAWATT}

    #lecture du fichier save.json qui lit les données du tour précédent
    if data["annee"] == 2030:
        with open('/var/www/html/flaskapp/game_data/save_template.json', 'r') as f:
            save = json.load(f)
    
    else:
        with open('/var/www/html/flaskapp/game_data/groupe{}/save.json'.format(group), 'r') as f:
            save = json.load(f)

    # Entrée : scenario, nb technos
    result = mix(ADEME["d{}".format(data["annee"])],
            data["annee"],
            data["hdf"], data["idf"], data["est"], data["nor"], data["occ"], data["pac"], data["bre"], 
            data["cvl"], data["pll"], data["naq"], data["ara"], data["bfc"], data["cor"], 
            nbOn, nbOff, nbPv, nbNuc, nbMeth, nbBio, data["stock"], data["alea"], save, data["carte"], group)

    with open('/var/www/html/flaskapp/game_data/groupe{}/production_output.json'.format(group), 'w') as f:
            json.dump(result, f)
import random

from flaskapp.journal.texteur import *
from climix.technologies import infos


class Personnage:
    def __init__(self, nom, prenom, role, affiliation):
        self.nom = nom
        self.prenom = prenom
        self.role = role
        self.affiliation = affiliation

    def __repr__(self):
        return (f"Personnage(nom={self.nom}, prenom={self.prenom}, "
                f"rôle={self.role}, affiliation={self.affiliation}")

    def afficher_details(self):
        details = (
            f"Nom : {self.nom}\n"
            f"Prénom : {self.prenom}\n"
            f"Rôle : {self.role}\n"
            f"Affiliation : {self.affiliation}\n"
        )
        print(details)


def generer_listes_personnages(personnages):
    # Dictionnaire pour identifier les personnages selon leur fonction
    premier_ministre = next(p for p in personnages if p.role == "première ministre")
    pdg_photovoltaique = next(p for p in personnages if p.role == "PDG solaire")
    pdg_eolienne = next(p for p in personnages if p.role == "PDG éolien")
    leader_greenpeace = next(p for p in personnages if p.role == "greenpeace")
    syndicaliste_agricole = next(p for p in personnages if p.role == "texte_resultat")
    activiste = next(p for p in personnages if p.role == "activiste")  # Modifié ici
    elu = next(p for p in personnages if p.role == "élue")

    # Choix aléatoire pour la première apparition du PDG de l'entreprise éolienne
    premier_pdg = random.choice([pdg_photovoltaique, pdg_eolienne])
    autre_pdg = pdg_photovoltaique if premier_pdg == pdg_eolienne else pdg_eolienne

    # Choix aléatoire pour la première apparition de l'activiste
    premier_syndicaliste_activiste = random.choice([syndicaliste_agricole, activiste])
    autre_syndicaliste_activiste = syndicaliste_agricole if premier_syndicaliste_activiste == activiste else activiste

    # Choix aléatoire pour le syndicaliste
    premier_politique = random.choice([leader_greenpeace, elu])
    autre_politique = leader_greenpeace if premier_politique == elu else elu

    # Création des listes avec les contraintes ajustées
    listes = [
        [premier_ministre, premier_pdg, premier_syndicaliste_activiste],
        [autre_pdg, premier_politique, autre_syndicaliste_activiste],
        [premier_ministre, premier_pdg, autre_politique],
        [autre_pdg, premier_syndicaliste_activiste, premier_politique],
        [premier_ministre, autre_pdg, autre_politique]
    ]

    return listes


class Region:
    def __init__(self, nom, prefecture, sous_prefectures, villes_cotieres, foires_agricoles, personnalites, elus,
                 centrales_nucleaires, especes_terrestres, especes_marines):
        self.nom = nom
        self.prefecture = prefecture
        self.sous_prefectures = sous_prefectures
        self.villes_cotieres = villes_cotieres
        self.foires_agricoles = foires_agricoles
        self.personnalites = personnalites
        self.elus = elus
        self.centrales_nucleaires = centrales_nucleaires
        self.especes_terrestres = especes_terrestres
        self.especes_marines = especes_marines

    def afficher_infos(self):
        print(f"Nom : {self.nom}")
        print(f"Préfecture : {self.prefecture}")
        print(f"Sous-préfectures : {', '.join(self.sous_prefectures)}")
        print(f"Villes côtières : {', '.join(self.villes_cotieres)}")
        print(f"Foires agricoles : {', '.join(self.foires_agricoles)}")
        print(f"Personnalités : {', '.join(self.personnalites)}")
        print(f"Élus : {', '.join(self.elus)}")
        print(f"Centrales nucléaires : {', '.join(self.centrales_nucleaires)}")
        print(f"Espèces animales terrestres : {', '.join(self.especes_terrestres)}")
        print(f"Espèces animales marines : {', '.join(self.especes_marines)}")


class DataForGazette:

    def __init__(self,
                 emissions_co2=1234.56,
                 equilibre_enr_nucleaire=75,
                 regions_photovoltaiques=["Occitanie"],
                 regions_eolien_onshore=["Normandie", "Bretagne"],
                 regions_eolien_offshore=["Pays de la Loire"],
                 puissance_photovoltaique_tour=500,
                 puissance_photovoltaique_totale=15000,
                 puissance_eolienne_tour=1200,
                 puissance_eolienne_totale=25000,
                 regions_suppression_nucleaire=["Occitanie"],
                 regions_sous_production=["Bretagne"],
                 regions_methaniseur=["Bretagne", "Normandie"],
                 regions_centrales_nucleaires=["Pays de la Loire", "Occitanie"]
                 ):
        self.emissions_co2 = emissions_co2  # Emissions de CO2 (réel)
        self.equilibre_enr_nucleaire = equilibre_enr_nucleaire  # Equilibre ENR/Nucléaire (réel)
        self.regions_photovoltaiques = regions_photovoltaiques  # Régions Photovoltaiques (liste)
        self.regions_eolien_onshore = regions_eolien_onshore  # Régions Eolien Onshore (liste)
        self.regions_eolien_offshore = regions_eolien_offshore  # Région Eolien Offshore (liste)
        self.puissance_photovoltaique_tour = puissance_photovoltaique_tour  # Puissance Photovoltaique du tour (réel)
        self.puissance_photovoltaique_totale = puissance_photovoltaique_totale  # Puissance Photovoltaique totale (réel)
        self.puissance_eolienne_tour = puissance_eolienne_tour  # Puissance Eolienne du tour (réel)
        self.puissance_eolienne_totale = puissance_eolienne_totale  # Puissance Eolienne totale (réel)
        self.regions_suppression_nucleaire = regions_suppression_nucleaire  # Régions où on a supprimé des centrales nucléaires (liste)
        self.regions_sous_production = regions_sous_production  # Régions en sous production électrique (liste)
        self.regions_methaniseur = regions_methaniseur  # Régions avec des méthaniseurs (liste)
        self.regions_centrales_nucleaires = regions_centrales_nucleaires  # Régions avec des centrales nucléaires maintenues (liste)

    def afficher_infos(self):
        """Affiche les informations stockées dans l'objet."""
        print(f"Emissions de CO2 : {self.emissions_co2} tonnes")
        print(f"Équilibre ENR/Nucléaire : {self.equilibre_enr_nucleaire}")
        print(f"Régions Photovoltaïques : {', '.join(self.regions_photovoltaiques)}")
        print(f"Régions Eolien Onshore : {', '.join(self.regions_eolien_onshore)}")
        print(f"Régions Eolien Offshore : {', '.join(self.regions_eolien_offshore)}")
        print(f"Puissance Photovoltaïque du tour : {self.puissance_photovoltaique_tour} MW")
        print(f"Puissance Photovoltaïque totale : {self.puissance_photovoltaique_totale} MW")
        print(f"Puissance Eolienne du tour : {self.puissance_eolienne_tour} MW")
        print(f"Puissance Eolienne totale : {self.puissance_eolienne_totale} MW")
        print(f"Régions ayant supprimé des centrales nucléaires : {', '.join(self.regions_suppression_nucleaire)}")
        print(f"Régions en sous production électrique : {', '.join(self.regions_sous_production)}")
        print(f"Régions avec des méthaniseurs : {', '.join(self.regions_methaniseur)}")
        print(f"Régions avec des centrales nucléaires maintenues : {', '.join(self.regions_centrales_nucleaires)}")


def calculer_data(dm, annee):
    """
    Exploite les résultats pour obtenir des indicateur globaux et par régions pour influencer la rédaction du journal
    @param dm: permet d'accéder aux "resultats" de la partie
    @param annee: accéder au bon tour de la partie
    @return: datas par regions et globales nécessaires pour influencer la génération du journal
    """
    datas = DataForGazette()

    ## On exploite le fichier de résultats
    resultats = dm.get_fichier(fichier='resultats')[annee]

    datas.emissions_co2 = int(resultats["co2"])
    datas.puissance_photovoltaique_totale = int(resultats["puissancePV"] * 1000.0)  #GWH -> MWh
    datas.puissance_eolienne_totale = int(resultats["puissanceEolienneTotale"] * 1000.0)  #GWH -> MWh
    datas.equilibre_enr_nucleaire = int(resultats["equilibreEnrNucleaire"])

    neg_transfert = [
        resultats['transfert'][reg] for reg in resultats['transfert']
        if (resultats['transfert'][reg] < 0.)
    ]
    seuil = sum(neg_transfert) / len(neg_transfert)
    datas.regions_sous_production = [reg for reg in resultats['transfert'] if (resultats['transfert'][reg] < seuil)]

    ##  On exploite le fichier détaillé de mix
    mix = dm.get_item_fichier(fichier='mixes', item=annee)

    reg_technos = {}
    for techno in ("panneauPV", "eolienneON", "eolienneOFF", "methanation", "centraleNuc", "EPR2"):
        reg_technos[techno] = [reg for reg in mix['unites'] if mix['nb'][reg][techno] > 0]

    datas.regions_photovoltaiques = reg_technos["panneauPV"]
    datas.regions_eolien_offshore = reg_technos["eolienneOFF"]
    datas.regions_eolien_onshore = reg_technos["eolienneON"]
    datas.regions_methaniseur = reg_technos["methanation"]
    datas.regions_centrales_nucleaires = reg_technos['centraleNuc'] + reg_technos['EPR2']
    # region deux fois si les deux technos => plus de proba que si une seule...
    # sinon faire list(set(reg_technos['centraleNuc'] +  reg_technos['EPR2'])) pour même proba

    ## On exploite mix['actions'] pour repérer ce qui a été choisi dans le tour
    datas.regions_suppression_nucleaire = []
    datas.puissance_eolienne_tour = 0.
    datas.puissance_photovoltaique_tour = 0.
    for reg in mix['actions']['regions']:
        for annee, action in mix['actions']['regions'][reg]['centraleNuc'].items():
            if (("nb_demanteles" in action) and (action['nb_demanteles'] > 0)):
                datas.regions_suppression_nucleaire.append(reg)

        for annee, action in mix['actions']['regions'][reg]['panneauPV'].items():
            if (action["action"] == "+"):
                datas.puissance_photovoltaique_tour += action["valeur"] * infos['panneauPV']["PoutMax"] * 1000.

        for annee, action in mix['actions']['regions'][reg]['eolienneON'].items():
            if (action["action"] == "+"):
                datas.puissance_eolienne_tour += action["valeur"] * infos["eolienneON"]["PoutMax"] * 1000.

        for annee, action in mix['actions']['regions'][reg]['eolienneOFF'].items():
            if (action["action"] == "+"):
                datas.puissance_eolienne_tour += action["valeur"] * infos["eolienneOFF"]["PoutMax"] * 1000.

    return datas


# # Choix des sujets pour les différents rôles.


def choisir_infrastructure_et_region(personnage, data, seuil_puissance=1000):
    """
    Fonction qui choisit une infrastructure et une région basée sur le rôle du personnage
    et les données fournies par l'objet DataForGazette.

    :param personnage: L'objet personnage avec un attribut 'role' qui peut être 'PDG solaire', 'PDG éolien', 
                      'texte_resultat', 'activiste', 'greenpeace' ou 'elue'.
    :param data: L'objet de type DataForGazette contenant les informations régionales et de puissance.
    :param seuil_puissance: Seuil de puissance pour sélectionner les régions (par défaut 1000).
    :return: Un tuple contenant l'infrastructure et la région choisies.
    """
    if personnage.role == 'PDG solaire':
        if data.puissance_photovoltaique_tour > seuil_puissance:
            infrastructure = 'photovoltaïque'
            region = random.choice(data.regions_photovoltaiques)
        else:
            infrastructure = 'photovoltaïque'
            region = 'France'
        return infrastructure, region

    elif personnage.role == 'PDG éolien':
        if data.puissance_eolienne_tour > seuil_puissance:
            # Choisir entre éolien onshore et éolien offshore
            if data.regions_eolien_onshore and data.regions_eolien_offshore:
                if random.choice([True, False]):
                    infrastructure = 'éolien onshore'
                    region = random.choice(data.regions_eolien_onshore)
                else:
                    infrastructure = 'éolien offshore'
                    region = random.choice(data.regions_eolien_offshore)
            elif data.regions_eolien_onshore:
                infrastructure = 'éolien onshore'
                region = random.choice(data.regions_eolien_onshore)
            elif data.regions_eolien_offshore:
                infrastructure = 'éolien offshore'
                region = random.choice(data.regions_eolien_offshore)
            else:
                return "Aucune région éolienne disponible."
        else:
            infrastructure = 'éolien'
            region = 'France'

        return infrastructure, region

    elif personnage.role == 'texte_resultat':
        # Choisir une infrastructure parmi celles avec des régions non vides
        infrastructures_non_vides = []
        if data.regions_photovoltaiques:
            infrastructures_non_vides.append('photovoltaïque')
        if data.regions_eolien_onshore:
            infrastructures_non_vides.append('éolien onshore')
        if data.regions_methaniseur:  # Ajout du méthaniseur comme option
            infrastructures_non_vides.append('méthaniseur')

        if infrastructures_non_vides:
            infrastructure_choisie = random.choice(infrastructures_non_vides)
            if infrastructure_choisie == 'photovoltaïque':
                region = random.choice(data.regions_photovoltaiques)
            elif infrastructure_choisie == 'éolien onshore':
                region = random.choice(data.regions_eolien_onshore)
            elif infrastructure_choisie == 'méthaniseur':
                region = random.choice(data.regions_methaniseur)
        else:
            infrastructure_choisie = 'photovoltaïque'
            region = 'France'

        return infrastructure_choisie, region

    elif personnage.role == 'activiste':
        # Choisir une infrastructure parmi celles avec des régions non vides
        infrastructures_non_vides = []
        if data.regions_photovoltaiques:
            infrastructures_non_vides.append('photovoltaïque')
        if data.regions_eolien_onshore:
            infrastructures_non_vides.append('éolien onshore')
        if data.regions_eolien_offshore:
            infrastructures_non_vides.append('éolien offshore')
        if data.regions_methaniseur:  # Ajout du méthaniseur comme option
            infrastructures_non_vides.append('méthaniseur')

        if infrastructures_non_vides:
            infrastructure_choisie = random.choice(infrastructures_non_vides)
            if infrastructure_choisie == 'photovoltaïque':
                region = random.choice(data.regions_photovoltaiques)
            elif infrastructure_choisie == 'éolien onshore':
                region = random.choice(data.regions_eolien_onshore)
            elif infrastructure_choisie == 'éolien offshore':
                region = random.choice(data.regions_eolien_offshore)
            elif infrastructure_choisie == 'méthaniseur':
                region = random.choice(data.regions_methaniseur)
        else:
            infrastructure_choisie = 'photovoltaïque'
            region = 'France'

        return infrastructure_choisie, region

    elif personnage.role == 'greenpeace':
        # Logique pour le rôle Greenpeace
        if data.regions_centrales_nucleaires:  # Vérifie si des centrales ont été maintenues
            region = random.choice(data.regions_centrales_nucleaires)
            infrastructure = 'maintenue'
        else:  # Sinon, choisit parmi les régions où une centrale a été supprimée
            if data.regions_suppression_nucleaire:
                region = random.choice(data.regions_suppression_nucleaire)
                infrastructure = 'supprimée'
            else:
                return "Aucune région disponible pour Greenpeace."

        return infrastructure, region

    elif personnage.role == 'élue':
        # Logique pour le rôle Élu
        if data.regions_suppression_nucleaire:  # Vérifie si des centrales ont été supprimées
            region = random.choice(data.regions_suppression_nucleaire)
            infrastructure = 'supprimée'
        else:  # Sinon, choisit parmi les régions en sous-production
            if data.regions_sous_production:
                region = random.choice(data.regions_sous_production)
                infrastructure = 'sous-production'
            else:
                return "Aucune région disponible pour l'Élue."

        return infrastructure, region

    return "Aucune infrastructure ou région disponible selon les critères du personnage."


def generate_article(character, data, dictionnaire_regions, year):
    if character.role != 'première ministre':
        infrastructure, region_choisie = choisir_infrastructure_et_region(character, data)
        print(character.role)
        print(infrastructure)
        print(region_choisie)

    if character.role == 'greenpeace':
        texte = texte_greenpeace(character, dictionnaire_regions.get(region_choisie), infrastructure)
    elif character.role == 'texte_resultat':
        texte = texte_agriculteur(character, dictionnaire_regions.get(region_choisie), infrastructure)
    elif character.role == 'PDG solaire':
        texte = texte_pdg_solaire(character, dictionnaire_regions.get(region_choisie))
    elif character.role == 'PDG éolien':
        texte = texte_pdg_eolien(character, dictionnaire_regions.get(region_choisie))
    elif character.role == 'activiste':
        texte = texte_activiste(character, dictionnaire_regions.get(region_choisie), infrastructure)
    elif character.role == 'élue':
        texte = texte_elue(character, dictionnaire_regions.get(region_choisie), infrastructure)
    elif character.role == 'première ministre':
        texte = texte_premiere_ministre(character, data, year)
    else:
        texte = "Rôle non reconnu. Veuillez vérifier le personnage."

    return texte


def exemple(datas):
    personnages = [Personnage("Dossal", "Charles", "texte_resultat", "Paysans en colère")]

    personnages.append(Personnage("Rondepierre", "Aude", "activiste", "La nature avant les profits"))

    personnages.append(Personnage("Cros", "Marion", "PDG solaire", "Power Solar"))

    personnages.append(Personnage("Lachaize", "Sébastien", "PDG éolien", "Wind Power"))

    personnages.append(Personnage("Delga", "Carole", "élue", "Parti Socialiste"))

    personnages.append(Personnage("Acco", "Pascal", "greenpeace", "greenpeace"))

    personnages.append(
        Personnage(nom='Swift', prenom='Taylor', role='première ministre', affiliation='La République En Marche'))

    listes_personnages = generer_listes_personnages(personnages)

    character = random.choice(listes_personnages)  # Assurez-vous que perso6 est défini quelque part dans votre code

    from flaskapp.journal.france import dictionnaire_regions as regions

    article = generate_article(character[0], datas, regions, 2040)
    return article


if __name__ == "__main__":

    from flaskapp.journal.france import dictionnaire_regions, france_data, personnages

    data = france_data

    print(exemple(france_data, dictionnaire_regions))
    dictionnaire_regions = dictionnaire_regions

    # Exemple d'utilisation
    year = 2025
    article = texte_premiere_ministre(personnages[0], data, year)
    print(article)

    # Exemple d'utilisation
    character = personnages[4]
    article = generate_article(character, france_data, dictionnaire_regions, 2024)
    print(article)

    # %% [markdown]
    # # Quelques tests pour terminer.

    # %%
    perso2 = personnages[1]
    infrastructure2, region2 = choisir_infrastructure_et_region(perso2, data, dictionnaire_regions)
    print(region2)
    print(infrastructure2)
    texte_activiste(perso2, dictionnaire_regions.get(region2), infrastructure2)

    # %%
    infrastructure, region_choisie = choisir_infrastructure_et_region(perso2, data)
    print(infrastructure)
    print(region_choisie)
    texte_greenpeace(perso2, dictionnaire_regions.get(region_choisie), infrastructure)

    # %%
    listes_personnages = generer_listes_personnages(personnages)
    print(listes_personnages[0])

    # %%
    for i, liste in enumerate(listes_personnages, 1):
        print(f"Textes tour {i} : {[generate_article(p, data, dictionnaire_regions, 2024) for p in liste]}")
        print()
    # %%

    data.afficher_infos()

    # Génération du texte
    perso1 = personnages[0]
    print(texte_agriculteur(perso1, dictionnaire_regions.get("Normandie"), "photovoltaïque"))
    print()
    print(texte_agriculteur(perso1, dictionnaire_regions["Bretagne"], "méthaniseur"))
    print()
    print(texte_agriculteur(perso1, dictionnaire_regions["Bretagne"], "éolien onshore"))

    # %% [markdown]
    # # Génération texte activiste.

    # %%

    # Génération du texte
    print(texte_activiste(perso2, dictionnaire_regions["Centre-Val de Loire"], "photovoltaïque"))
    print()
    print(texte_activiste(perso2, dictionnaire_regions["Hauts-de-France"], "méthaniseur"))
    print()
    print(texte_activiste(perso2, dictionnaire_regions["Provence-Alpes-Côte d'Azur"], "éolien onshore"))
    print()
    print(texte_activiste(perso2, dictionnaire_regions["Bretagne"], "éolien offshore"))

    # Exemple d'utilisation
    # Définition d'un personnage
    perso3 = personnages[2]
    texte_resultat = texte_pdg_solaire(perso3, dictionnaire_regions["Occitanie"])
    print(texte_resultat)
    print()
    # Si on indique la région France, le personnage regrette les choix du gouvernement de ne pas en faire plus pour le secteur.
    texte_resultat = texte_pdg_solaire(perso3, dictionnaire_regions["France"])
    print(texte_resultat)

    # Exemple d'utilisation
    perso4 = personnages[3]
    texte_resultat = texte_pdg_eolien(perso4, dictionnaire_regions["Occitanie"])
    print(texte_resultat)
    print()
    # Variante où il n'y a pas suffisamment d'éolien posé.
    texte_resultat = texte_pdg_eolien(perso4, dictionnaire_regions["France"])
    print(texte_resultat)

    perso5 = personnages[4]
    # Générer un texte pour une situation "supprimée" (ville avec une centrale nucléaire)
    print(texte_elue(perso5, dictionnaire_regions["Pays de la Loire"], "supprimée"))
    print()
    # Générer un texte pour une situation de sous-production
    print(texte_elue(perso5, dictionnaire_regions["Occitanie"], "sous-production"))

    perso6 = personnages[5]

    # Cas d'une centrale supprimée
    print(texte_greenpeace(perso6, dictionnaire_regions["Occitanie"], "supprimée"))
    print()
    # Cas d'une centrale maintenue
    print(texte_greenpeace(perso6, dictionnaire_regions["Auvergne-Rhône-Alpes"], "maintenue"))

    # Exemple d'utilisation
    print(tirer_arguments_greenpeace())

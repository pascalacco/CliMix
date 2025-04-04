"""
Gère les données d'un pays :
    - le nom
    - les cartes (images) à afficher
    - la décomposition en régions et leurs noms
    - le mix initial
    - les limites de production des régions
    - les scenarios de
"""
import os, os.path, json, gzip,  pandas, numpy
from climix.foret.mix import Mix
import climix.stratege as stratege


class pays :
    """ Tout un pays """
    chemin = os.path.dirname(os.path.realpath(__file__))

    asso_technos={"eolienneON":"wind_onshore",
                  "panneauPV":"solar",
                  "eolienneOFF":"wind_offshore"}
    json_opts = {"indent": 4, "sort_keys": False}

    def __init__(self, nom="FR_metro", chemin=None):
        self.nom = nom
        if chemin is None:
            self.chemin = pays.chemin + "/" + nom + "/"
        else:
            self.chemin = chemin
        self.chemin_scenarios = self.chemin

        with open(self.chemin + "regions.json", "r") as f:
            self.asso_regions = json.load(f)
            self.regs = self.asso_regions.keys()

        with open(self.chemin + "association_annees.json", "r") as f:
            self.asso_annees = json.load(f)

    def get_fichier(self, fichier, ext=".json"):
        with open(self.chemin + fichier + ext, "r") as f:
            obj = json.load(f)
            return obj

    def get_mix_init(self):
        mix_init = Mix(self.nom)
        mix_init.from_json(self.chemin+self.nom+"_init.json")
        return mix_init

    def get_scenario(self, scenario):
        return pandas.read_hdf(self.chemin_scenarios + scenario + "_25-50.h5", "df")
    
    def gen_fdcs_meteo(self, annee, associe_l_annee = True) :
        """
        Lis les fichier csv des facteurs de charge et renvoie une structure
        """
        if associe_l_annee:
            annee = self.asso_annees[annee]

        fdcs={}
        for reg in self.regs :
            fdcs[reg] = {}
            region = self.asso_regions[reg]
            for techno in ["eolienneON", "panneauPV", "eolienneOFF"]:
                tech = pays.asso_technos[techno]
                filepath = self.chemin +"meteos/" + region +"/" + annee + "/" + tech + ".csv"
                if os.path.exists(filepath):

                    df = pandas.read_csv(filepath, index_col=0, parse_dates=[0])
                    # Enlève le 29 février pour les années bissextile (leap year)
                    df = df[(df.index.month != 2) | (df.index.day != 29)]
                    fdcs[reg][techno] = df["facteur_charge"].tolist()
                else:
                    fdcs[reg][techno] = numpy.zeros((stratege.H)).tolist()

        return fdcs

    def get_fdcs_meteo(self, annee, associe_l_annee = True) :
        if associe_l_annee:
            annee = self.asso_annees[annee]

        with gzip.open(self.chemin + "/meteos/fdcs_"+annee+".json.gzip", "rt", encoding='utf-8') as f:
            fdcs = json.load(f)
            return fdcs

    def dispatch_fdc_orignaux_dans_regions(self, annee):
        fdc_off = pandas.read_csv(self.chemin + "/meteos/fdc_off.csv")
        fdc_on = pandas.read_csv(self.chemin + "/meteos/fdc_on.csv")
        fdc_pv = pandas.read_csv(self.chemin + "/meteos/fdc_pv.csv")

        dftype = pandas.read_csv(self.chemin + '/meteos/Occitanie/2009/wind_onshore.csv')

        for reg in fdc_off.columns:
            rep = self.chemin+"meteos/"+self.asso_regions[reg]+"/"
            if not os.path.exists(rep+annee):
                os.mkdir(rep+annee)
            dftype["facteur_charge"] = fdc_off[reg]
            dftype.to_csv(rep + annee+ "/wind_offshore.csv", index=False)

        for reg in fdc_on.columns:
            rep = self.chemin+"meteos/"+self.asso_regions[reg]+"/"
            if not os.path.exists(rep+annee):
                os.mkdir(rep+annee)
            dftype["facteur_charge"] = fdc_on[reg]
            dftype.to_csv(rep + annee+ "/wind_onshore.csv", index=False)

        for reg in fdc_pv.columns:
            rep = self.chemin+"meteos/"+self.asso_regions[reg]+"/"
            if not os.path.exists(rep+annee):
                os.mkdir(rep+annee)
            dftype["facteur_charge"] = fdc_pv[reg]
            dftype.to_csv(rep + annee+ "/solar.csv", index=False)
def configurer_la_region_FR_metro():
    """ Génère les fichiers csv des regions et fdcs etc. une fois pour toutes pour FR_metro.
        Ces fichiers sont nécessaires à l'init d'un Pays()
    """
    asso_regions = {
        "occ": "Occitanie",
        "bre": "Bretagne",
        "nor": "Normandie",
        "pll": "Pays-de-la-Loire",
        "naq": "Nouvelle-Aquitaine",
        "idf": "Ile-de-France",
        "ara": "Auvergne-Rhone-Alpes",
        "bfc": "Bourgogne-Franche-Comte",
        "cor": "Corse",
        "pac": "Provence-Alpes-Cote-d-Azur",
        "est": "Grand-Est",
        "hdf": "Hauts-de-France",
        "cvl": "Centre-Val-de-Loire"
    }

    with open(pays.chemin + "/FR_metro/regions.json", "w") as f:
        json.dump(asso_regions, f, **pays.json_opts)

    asso_annees={"2025": "2004", "2030": "2009", "2035": "2013", "2040": "2019", "2045": "2018_bis", "2050": "2021",
                 "2055": "2021", "2060": "2021", "2065": "2021"}
    with open(pays.chemin + "/FR_metro/association_annees.json", "w") as f:
        json.dump(asso_annees, f, **pays.json_opts)
    FR_metro = pays()

    # Récupére les fichier fdc_on / off et pv de la première versio net dispatche dans
    #  les répertoires par région de Charles Dossal
    FR_metro.dispatch_fdc_orignaux_dans_regions("2018_bis")

    # Balaye les fichiers météo de Charles Dossal (un répertoire par région)
    for an in (list(range(2004, 2024))+["2018_bis"]):
        annee = an.__str__()
        fdcs = FR_metro.gen_fdcs_meteo(annee, associe_l_annee=False)
        with gzip.open(FR_metro.chemin + "/meteos/fdcs_"+annee+".json.gzip", "wt", encoding='utf-8') as f:
            print(annee)
            json.dump(fdcs, f, **pays.json_opts)


if __name__ == "__main__" :
    # Décommenter pour regénérer les fichiers
    # configurer_la_region_FR_metro()
    FR_metro = pays(nom="FR_metro")

    pandas.options.plotting.backend = "plotly"


    fdcs = FR_metro.get_fdcs_meteo("2018_bis",associe_l_annee=False)
    fdcs2018 = FR_metro.get_fdcs_meteo("2022",associe_l_annee=False)
    f_eon = pandas.DataFrame.from_dict({key: fdcs[key]['eolienneON'] for key in fdcs.keys()})
    f_eon2018 = pandas.DataFrame.from_dict({key: fdcs2018[key]['eolienneON'] for key in fdcs2018.keys()})
    fc_moy = f_eon.mean().mean().__str__()
    fc_moy2018 = f_eon2018.mean().mean().__str__()

    print("onSHORE ancienne version : " + fc_moy)
    print(f_eon.describe())
    print("onSHORE 2018 : " + fc_moy2018)
    print(f_eon2018.describe())

    plot = f_eon.plot(kind='line',title='On shore ancienne : '+ fc_moy)
    plot.show()
    plot = f_eon2018.plot(kind='line',title='On shore 2018 : '+ fc_moy2018)
    plot.show()

    f_eoff = pandas.DataFrame.from_dict({key: fdcs[key]['eolienneOFF'] for key in fdcs.keys()}).drop(columns=['occ','idf','ara','cvl','est','bfc'])
    f_eoff2018 = pandas.DataFrame.from_dict({key: fdcs2018[key]['eolienneOFF'] for key in fdcs2018.keys()}).drop(columns=['occ','idf','ara','cvl','est','bfc'])
    fc_moy = f_eoff.mean().mean().__str__()
    fc_moy2018 = (f_eoff2018).mean().mean().__str__()

    print("OFFSHORE ancienne version : "+ fc_moy)
    print(f_eoff.describe())
    print("OFFSHORE 2018 : "+ fc_moy2018)
    print(f_eoff2018.describe())
    plot = f_eoff.plot(kind='line',title='Off shore ancienne : '+ fc_moy)
    plot.show()
    plot = f_eoff2018.plot(kind='line', title='OFF shore 2018 : '+ fc_moy2018)
    plot.show()

    f_pv = pandas.DataFrame.from_dict({key: fdcs[key]['panneauPV'] for key in fdcs.keys()})
    f_pv2018 = pandas.DataFrame.from_dict({key: fdcs2018[key]['panneauPV'] for key in fdcs2018.keys()})
    fc_moy = f_pv.mean().mean().__str__()
    fc_moy2018 = (f_pv2018.mean().mean()).__str__()
    print("Solar ancienne version : "+ fc_moy)
    print(f_pv.describe())
    print("Solar 2018 : "+ fc_moy2018)
    print(f_pv2018.describe())
    plot = f_pv.plot(kind='line',title='PV ancienne : '+ fc_moy)
    plot.show()
    plot = f_pv2018.plot(kind='line',title='PV 2018 : '+ fc_moy2018)
    plot.show()

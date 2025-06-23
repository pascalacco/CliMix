import pandas
import pickle
import os
import json

from flaskapp.journal.utils import *
import climix.geographe.pays
import datetime


def sépare_groupe_de_equipe(nom):
    groupe = nom[0:-1]
    num_equipe = nom[-1]
    if num_equipe == 'e':
        num_equipe = "Dumbledore"
        groupe = nom[0:-10]
    return groupe, num_equipe


def normap(value, start1, stop1, start2, stop2):
    """
    Normalise la valeur value donnée dans les bornes 1 pour l'adapter aux bornes 2
    """
    OldRange = (stop1 - start1)
    if OldRange == 0:
        NewValue = start2
    else:
        NewRange = (stop2 - start2)
        NewValue = (((value - start1) * NewRange) / OldRange) + start2

    return NewValue


class Parties:
    """
        Gère la vision globale de toutes les parties

    """
    promos = ["IMACS", "MIC", "IC", "ICBE", "POUDLARD"]
    tds = ["A", "B", "C", "D", "E", "Serpentar"]
    equipe = ["1", "2", "3", "4", "5", "Dumbledore"]
    scenarios = ["S1", "S2", "S3Enr", "S3Nuke", "S4", "2025Plat"]
    chemin_archiveur = os.path.dirname(os.path.realpath(__file__))
    chemin_game_data_relatif = "game_data_2025/"
    chemin_game_data = chemin_archiveur + "/" + chemin_game_data_relatif

    def __init__(self, chemin=None, pays=None):
        if chemin is None:
            self.chemin = Parties.chemin_game_data
            os.makedirs(self.chemin, exist_ok=True)
            for promo in Parties.promos:
                for td in Parties.tds:
                    for equipe in Parties.equipe:
                        os.makedirs(self.chemin + promo + '_' + td + equipe, exist_ok=True)
                        for scenario in Parties.scenarios:
                            os.makedirs(self.chemin + promo + '_' + td + equipe + '/' + scenario, exist_ok=True)

        else:
            self.chemin = chemin

        if pays is None:
            self.pays = climix.geographe.pays.pays()
        else:
            self.pays = pays

        self.data_managers = {}

    def get_liste_equipes(self):
        grouplist = {}
        # list game_data games only directoires and teams on subdirectories
        for filename in os.listdir(self.chemin):

            # print(filename+' is a directory? '+str(os.path.isdir(os.path.join(dataPath+'game_data/',filename))))
            if os.path.isdir(os.path.join(self.chemin, filename)):
                # add key to the dictionary
                grouplist[filename] = []
                for fileteam in os.listdir(self.chemin + filename):
                    if os.path.isdir(os.path.join(self.chemin + filename, fileteam)):

                        dm, msg = self.get_data_manager(filename, fileteam)
                        if dm is not None and dm.est_ok():
                            currentYear = dm.get_annee_courante()
                        else:
                            currentYear = "-1"
                        # read the json file
                        # with open(self.chemin + filename + '/' + fileteam + '/mixes.json') as json_file:
                        #    data = json.load(json_file)
                        #    currentYear = 0
                        #    # get the first key of the json file
                        #    for key in data.keys():
                        #        # check if it's empty
                        #        currentYear = key
                        #        if data[key]['actif']:
                        #            break
                        grouplist[filename].append({'partie': fileteam, 'annee': currentYear})
                        # grouplist[filename]{'team':fileteam,'data':'data'})

        # grouplist = sorted(grouplist, key=lambda d: d['group']+d['team'])
        # sort the dictionary by key
        grouplist = dict(sorted(grouplist.items()))
        # sort the list of teams by team name
        for key in grouplist:
            grouplist[key] = sorted(grouplist[key], key=lambda d: d['partie'])

        return grouplist

    def get_liste_groupes_par_parties(self):
        grouplist = self.get_liste_equipes()
        groupes = {}
        for equipe in grouplist:
            groupe, num_equipe = sépare_groupe_de_equipe(equipe)
            if groupe not in groupes:
                groupes[groupe] = {}
            for partie in grouplist[equipe]:
                percent = normap(int(partie['annee'][:4]), 2020, 2050, 0, 100)
                partie['percent'] = percent
                partie['equipe'] = equipe
                if partie['partie'] not in groupes[groupe]:
                    groupes[groupe][partie['partie']] = {num_equipe: partie}
                else:
                    groupes[groupe][partie['partie']][num_equipe] = partie

        return groupes

    def effacer(self, liste):
        messages = ""
        for etiquette in liste:
            [promo, td, scenario, num] = etiquette.split("_")
            equipe = promo + "_" + td + num
            partie = scenario

            dm, mesg = self.get_data_manager(equipe, partie)
            if dm is not None:
                dm.reset()
                messages += "OK - " + dm.chemin + " effacé\n"
            else:
                messages += mesg
        return messages

    def get_data_manager(self, equipe, partie):
        if equipe in self.data_managers:
            if partie in self.data_managers[equipe]:
                return self.data_managers[equipe][partie], "ok"

        dm = DataManager(equipe, partie, pays=self.pays)

        if dm.est_ok():
            if equipe in self.data_managers:
                self.data_managers[equipe][partie] = dm
            else:
                self.data_managers[equipe] = {partie: dm}

            return self.data_managers[equipe][partie], "init"
        else:
            return None, "Mauvais ou pas de fichiers dans " + dm.chemin

    def compiler_resultats(self, liste):
        res_init = self.pays.get_init_fichier("resultats")
        annees = [int(annee) for annee in res_init]
        items = [item for item in res_init["2025"] if
                 isinstance(res_init["2025"][item], int) or isinstance(res_init["2025"][item], float)]
        compilation = {item: {} for item in items}

        for etiquette in liste:
            [promo, td, scenario, num] = etiquette.split("_")
            equipe = promo + "_" + td + num
            partie = scenario

            dm, mesg = self.get_data_manager(equipe, partie)
            if dm is not None:
                resultats = dm.get_results()
                for item in items:
                    compilation[item][etiquette] = [resultats[year][item] if item in resultats[year] else None
                                                    for year in resultats]
            else:
                compilation[item][etiquette + " Erreur !"] = [None for year in res_init]

        return compilation, annees

    def log(self, trace):
        with open(self.chemin_game_data + 'logs.txt', 'a', encoding="utf-8") as logs:
            logs.write("[{}] {} \n".format(datetime.datetime.now(), trace))


class DataManager:
    """
    DataManager gère les données d'une partie

    @ version de Jules Ripol (adaptée à "journal" le code qui génère les pages de journaux)
    @revision : rempalcer group par équipe et team par équipe

    """
    chemin_archiveur = Parties.chemin_archiveur
    chemin_game_data = Parties.chemin_game_data
    # chemin_init_partie = chemin_game_data

    fichiers = ["mixes", "resultats"]  # "save", "mix", "inputs",  "logs"
    fichiers_init = ["mixes", "resultats"]  # "save", "mix", "inputs", "logs"
    json_opts = {"indent": 4, "sort_keys": False}

    def __init__(self, equipe, partie, chemin=None, pays=None):

        self.equipe = equipe
        self.partie = partie
        if chemin is None:
            self.chemin = DataManager.chemin_game_data + "{}/{}/".format(equipe, partie)
        else:
            self.chemin = chemin

        if pays is None:
            self.pays = climix.geographe.pays.pays()
        else:
            self.pays = pays

        self.pays = climix.geographe.pays.pays()
        self.chemin_init_partie = self.pays.chemin

        self.data_managers = {}

        self.results_path = self.chemin + "game_data/{}/{}/resultats.json".format(equipe, partie)
        self.scores_path = self.chemin + "game_data/{}/{}/scores.json".format(equipe, partie)
        self.mix_path = self.chemin + "game_data/{}/{}/mix.json".format(equipe, partie)
        self.initial_mix_path = self.chemin + "game_data/mix_init.json"

        self.aggregated_mix_path = self.chemin + "game_data/{}/{}/mix_aggregated.json".format(equipe, partie)
        self.occasions_path = self.chemin + "game_data/{}/{}/occasions.json".format(equipe, partie)
        self.roles_path = self.chemin + "game_data/{}/{}/roles.json".format(equipe, partie)
        self.round_path = self.chemin + "game_data/{}/{}/current_round.pkl".format(equipe, partie)
        self.title_path = self.chemin + "game_data/{}/{}/annee.txt".format(equipe, partie)
        self.infos_path = self.chemin + "game_data/{}/{}/infos.json".format(equipe, partie)

    def init_fichier(self, fich, format=".json"):
        dico = self.pays.get_init_fichier(fich)

        with open(self.chemin + fich + format, "w", encoding="utf-8") as dst:
            json.dump(dico, dst, **DataManager.json_opts)

    def init_partie(self):
        os.makedirs(self.chemin, exist_ok=True)
        for fich in DataManager.fichiers_init:
            self.init_fichier(fich)

    def reset(self):
        filesToRemove = [os.path.join(self.chemin, f) for f in os.listdir(self.chemin)]
        # for f in filesToRemove:
        #    os.remove(f)
        # os.rmdir(self.chemin)
        os.makedirs(self.chemin, exist_ok=True)
        for filename in os.listdir(self.chemin):
            file_path = os.path.join(self.chemin, filename)
            try:
                os.unlink(file_path)
            except  Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def verif_fichier(self, fich, format=".json"):
        ok = True
        try:
            src = open(self.chemin + fich + format, "r", encoding="utf-8")
            dic = json.load(src)
        except:
            ok = False
        return ok

    def est_ok(self):
        ok = True
        for file in DataManager.fichiers:
            ok = ok and self.verif_fichier(fich=file)
        return ok

    def get_annee_courante(self):
        if self.est_ok():
            annee = self.get_annee()
        else:
            annee = "-1"
        return annee

    def get_fichier(self, fichier, ext=".json"):
        with open(self.chemin + fichier + ext, "r", encoding="utf-8") as f:
            obj = json.load(f)
            return obj

    def set_fichier(self, fichier, dico, ext=".json"):
        with open(self.chemin + fichier + ext, "w", encoding="utf-8") as f:
            json.dump(dico, f, **DataManager.json_opts)

    def cp_fichier(self, src, dst, ext=".json"):
        with open(self.chemin + src + ext, "r", encoding="utf-8") as src:
            dico = json.load(src)
            with open(self.chemin + dst + ext, "w", encoding="utf-8") as dst:
                json.dump(dico, dst, **DataManager.json_opts)
        return dico

    def set_item_fichier(self, fichier, item, val, ext=".json"):

        dico = self.get_fichier(fichier)

        dico[item] = val

        self.set_fichier(fichier, dico)
        return dico

    def get_item_fichier(self, fichier, item, ext=".json"):

        dico = self.get_fichier(fichier)

        return dico[item]

    def set_item_enfouis_dans_fichier(self, fichier, items, val, ext=".json"):

        dico = self.get_fichier(fichier)
        dicit = dico
        for un_item in items[:-1]:
            dicit = dicit[un_item]
        dicit[items[-1]] = val

        self.set_fichier(fichier, dico)
        return dico

    def set_chroniques(self, chroniques, annee):
        df = pandas.DataFrame(chroniques)
        df.to_hdf(path_or_buf=self.chemin + "chroniques_" + annee + ".hdf5", key='df', mode='w')
        # np.savez_compressed(self.chemin+"chroniques.npz", **chroniques)

    def get_chroniques(self, annee):
        df = pandas.read_hdf(path_or_buf=self.chemin + "chroniques_" + annee + ".hdf5", key='df')
        return df

    def get_annee(self):
        # read the json file
        try:
            mixes = self.get_mixes()
            results = self.get_results()

            annee = -1

            for key in results:
                if results[key] == {}:
                    break
                else:
                    if key in mixes:
                        if mixes[key]["actif"]:
                            annee = key + "-"
                        else:
                            annee = key

                    else:
                        return -2
            return annee

        except:
            return -1

    def get_results(self):
        return self.get_fichier(fichier="resultats")

    def get_mixes(self):
        return self.get_fichier(fichier="mixes")

    def get_mix(self):
        return self.get_fichier(fichier="mix")

    def sauve_tout(self, annee):
        import shutil
        from datetime import datetime
        date = datetime.today().strftime('%Y_%m_%d_%Hh_%Mmn')
        fichier = self.equipe + '_' + self.partie + '_' + annee + '_du_' + date
        shutil.make_archive(self.chemin + '../' + fichier, 'zip', self.chemin)
        return fichier + '.zip'

    def get_roles(self):
        return self.get_fichier(fichier='roles')

    def set_roles(self, dict_roles) :
        self.set_fichier(fichier='roles', dico=dict_roles)

    


"""
Code extérieur à l'archiveur
"""

json_opts = {"indent": 4, "sort_keys": True}

"""
def creer_dossier(chemin_dossier):
    if not os.path.exists(chemin_dossier):
        os.makedirs(chemin_dossier)


def get_rol(equipe, partie):
    data_role = DataManager(equipe=equipe, partie=partie).get_roles()
    return data_role

"""
if __name__ == "__main__":
    partie = Parties()
    # print(partie.get_group_list())
    print(partie.get_liste_equipes())

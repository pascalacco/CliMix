import pandas
import pickle
import os
import json

from flaskapp.journal.utils import *


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

    chemin_archiveur = os.path.dirname(os.path.realpath(__file__))
    chemin_game_data_relatif = "game_data/"
    chemin_game_data = chemin_archiveur + "/" + chemin_game_data_relatif
    def __init__(self, chemin=None):
        if chemin is None:
            self.chemin = Parties.chemin_game_data
        else:
            self.chemin = chemin
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
                    if os.path.isdir(os.path.join(self.chemin + filename, fileteam)) == True:

                        # read the json file
                        with open(self.self.chemin + filename + '/' + fileteam + '/resultats.json') as json_file:
                            data = json.load(json_file)
                            currentYear = 0
                            # get the first key of the json file
                            for key in data.keys():
                                # check if it's empty
                                if data[key] == {}:
                                    # remove the empty key
                                    currentYear = key
                                    print(currentYear)
                                    # exite the for loop
                                    break
                            grouplist[filename].append({'team': fileteam, 'data': currentYear})
                            # grouplist[filename]{'team':fileteam,'data':'data'})

        # grouplist = sorted(grouplist, key=lambda d: d['group']+d['team'])
        # sort the dictionary by key
        grouplist = dict(sorted(grouplist.items()))
        # sort the list of teams by team name
        for key in grouplist:
            grouplist[key] = sorted(grouplist[key], key=lambda d: d['team'])

        return grouplist

    def get_group_list(self):
        grouplist = self.get_liste_equipes()

        for equipe in grouplist:
            for partie in grouplist[equipe]:
                percent = normap(int(partie['data']), 2030, 2050, 0, 100)
                partie['percent'] = percent

        return grouplist

    def get_data_manager(self, equipe, partie):
        if equipe in self.data_managers:
            if partie in self.data_managers[equipe]:
                return self.data_managers[equipe][partie], "ok"

        dm = DataManager(equipe, partie)

        if dm.est_ok():
            if equipe in self.data_managers:
                self.data_managers[equipe][partie] = dm
            else:
                self.data_managers[equipe] = {partie:  dm}

            return self.data_managers[equipe][partie], "init"
        else:
            return None, "Mauvais fichiers dans " + dm.chemin



class DataManager:
    """
    DataManager gère les données d'une partie

    @ version de Jules Ripol (adaptée à "journal" le code qui génère les pages de journaux)
    @revision : rempalcer group par équipe et team par équipe

    """
    chemin_archiveur = Parties.chemin_archiveur
    chemin_game_data = Parties.chemin_game_data
    chemin_init_partie = chemin_game_data

    fichiers = ["mixes", "resultats"] #"save", "mix", "inputs",  "logs"
    fichiers_init = ["mixes", "resultats"] #"save", "mix", "inputs", "logs"
    json_opts = {"indent": 4, "sort_keys": False}

    def __init__(self, equipe, partie, chemin=None):

        self.equipe = equipe
        self.partie = partie
        if chemin is None:
            self.chemin = DataManager.chemin_game_data+"{}/{}/".format(equipe, partie)
        else:
            self.chemin = chemin
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
        with open(DataManager.chemin_init_partie + fich + "_init" + format, "r") as src:
            dico = json.load(src)
        with open(self.chemin + fich + format, "w") as dst:
            json.dump(dico, dst, **DataManager.json_opts)

    def init_partie(self):
        os.makedirs(self.chemin, exist_ok=True)
        for fich in DataManager.fichiers_init:
            self.init_fichier(fich)

    def reset(self):
        filesToRemove = [os.path.join(self.chemin, f) for f in os.listdir(self.chemin)]
        for f in filesToRemove:
            os.remove(f)
        os.rmdir(self.chemin)
        os.makedirs(self.chemin, exist_ok=True)
        for fich in DataManager.fichiers_init:
            self.init_fichier(fich)

    def verif_fichier(self, fich, format=".json"):
        ok = True
        try:
            src = open(self.chemin + fich + format, "r")
            dic = json.load(src)
        except:
            ok = False
        return ok

    def est_ok(self):
        ok = True
        for file in DataManager.fichiers:
            ok = ok and self.verif_fichier(fich=file)
        return ok

    def get_fichier(self, fichier, ext=".json"):
        with open(self.chemin+fichier+ext, "r") as f:
            obj = json.load(f)
            return obj

    def set_fichier(self, fichier, dico, ext=".json"):
        with open(self.chemin+fichier+ext, "w") as f:
            json.dump(dico, f, **DataManager.json_opts)

    def cp_fichier(self, src, dst, ext=".json"):
        with open(self.chemin+src+ext, "r") as src:
            dico = json.load(src)
            with open(self.chemin+dst+ext, "w") as dst:
                json.dump(dico, dst, **DataManager.json_opts)
        return dico

    def set_item_fichier(self, fichier, item, val, ext=".json"):

        dico = self.get_fichier(fichier)

        dico[item] = val

        self.set_fichier(fichier, dico)
        return dico

    def set_item_enfouis_dans_fichier(self, fichier, items, val, ext=".json"):

        dico = self.get_fichier(fichier)
        dicit=dico
        for un_item in items[:-1]:
            dicit = dicit[un_item]
        dicit[items[-1]]= val

        self.set_fichier(fichier, dico)
        return dico

    def set_chroniques(self, chroniques, annee):
        df = pandas.DataFrame(chroniques)
        df.to_hdf(path_or_buf=self.chemin+"chroniques_"+annee+".hdf5", key='df', mode='w')
        #np.savez_compressed(self.chemin+"chroniques.npz", **chroniques)

    def get_chroniques(self, annee):
        df = pandas.read_hdf(path_or_buf=self.chemin+"chroniques_"+annee+".hdf5", key='df')
        return df

    def get_annee(self):
        # read the json file
        with open(self.chemin+'resultats.json') as json_file:
            data = json.load(json_file)
            annee = 2050
            # get the first key of the json file
            for key in data.keys():
                # check if it's empty
                if data[key] == {}:
                    # remove the empty key
                    annee = key
                    print(annee)
                    # exite the for loop
                    break
            return annee

    def get_results(self):

        return self.get_fichier(fichier="resultats")

    def get_mix(self):
        return self.get_fichier(fichier="mix")

    def sauve_tout(self, annee):
        import shutil
        from datetime import datetime
        date = datetime.today().strftime('%Y_%m_%d_%Hh_%Mmn')
        fichier = self.equipe + '_' + self.partie + '_' + annee +'_du_' + date
        shutil.make_archive(self.chemin+'../'+fichier, 'zip', self.chemin)
        return fichier+'.zip'

        ###____________________________________________________________________________________
        ### Pas à jour
    def get_mdp(self):
        ## Aller chercher dans le bon fichier self.chemin/infos.json le mot de passe
        ## et return None si pas de fichier ou autre
        return None
    def get_info(self):
        with open(self.infos_path, 'r') as json_file:
            infos = json.load(json_file)
        return infos
        
    def set_round(self):
        current_round = -1
        with open(self.round_path, 'wb') as file:
            pickle.dump(current_round, file)

    def get_round(self):
        with open(self.round_path, 'rb') as file:
            current_round = pickle.load(file)
        return current_round

    def update_round(self):
        with open(self.round_path, 'rb') as file:
            current_round = pickle.load(file)
        current_round += 1
        with open(self.round_path, 'wb') as file:
            pickle.dump(current_round, file)

    def get_year(self):
        with open(self.results_path, 'r') as json_file:
            results = json.load(json_file)
        years = list(results.keys())
        round = self.get_round()
        return years[round]

    def set_roles(self, names):
        create_roles(names=names, path=self.roles_path)

    def get_roles(self):
        with open(self.roles_path, 'r') as json_file:
            roles = json.load(json_file)
        round = self.get_round()
        roles = {key: values[round] for key, values in roles.items()}
        return roles

    def set_mix_aggregated(self):
        with open(self.initial_mix_path, 'r') as json_file:
            mix = json.load(json_file)
        mix["annee"] = 2025
        mix = {"2025": mix}
        with open(self.aggregated_mix_path, 'w') as file:
            json.dump(mix, file)

    def set_scores(self):
        set_scores_dict(self.scores_path)

    def update_scores(self):
        current_round = self.get_round()
        update_scores_fn(self.scores_path, self.results_path, self.aggregated_mix_path, current_round)

    def set_occasions(self):
        set_occasions_dict(self.occasions_path)

    def update_title(self):
        years = ["2030", "2035", "2040", "2045", "2050"]
        current_round = self.get_round()
        output = "Année " + years[current_round]
        with open(self.title_path, 'w') as file:
            file.write(output)

    def set_title(self):
        output = "Année 2030"
        with open(self.title_path, 'w') as file:
            file.write(output)

    def get_title(self):
        with open(self.title_path, 'r') as file:
            title = file.read()
        return title

    def get_mix_aggregated(self):
        with open(self.aggregated_mix_path, 'rb') as file:
            mix_dict = json.load(file)
        return mix_dict


    def update_mix(self, data):
        with open(self.mix_path, "w") as dst:  #
            json.dump(data, dst)

    def update_mix_aggregated(self, data):
        year = self.get_year()
        mix_dict = self.get_mix_aggregated()
        mix_dict[year] = data
        with open(self.aggregated_mix_path, "w") as dst:
            json.dump(mix_dict, dst)


    def get_occasions(self):
        with open(self.occasions_path, "r") as f:
            occasions = json.load(f)
        return occasions

    def get_scores(self):
        with open(self.scores_path, "r") as f:
            scores = json.load(f)
        return scores

    def update_gpt_text(self, character_number, text):
        file_path = dataPath + "game_data/{}/{}/perso{}.txt".format(self.equipe, self.partie, character_number)
        with open(file_path, 'w') as file:
            file.write(text)

    def get_data_for_themes(self, role, theme):
        with open(self.scores_path, "r") as f:
            scores = json.load(f)
        return scores[role][theme][1]




"""
Code extérieur à l'archiveur
"""

json_opts = {"indent": 4, "sort_keys": True}


def creer_dossier(chemin_dossier):
    if not os.path.exists(chemin_dossier):
        os.makedirs(chemin_dossier)

def get_rol(equipe, partie):
    data_role = DataManager(equipe=equipe, partie=partie, chemin=dataPath).get_roles()
    return data_role


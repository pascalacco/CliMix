from constantes import *
from journal.utils import *
import json
import pickle


class Parties:
    """
        Gère la vision globale de toutes les parties

    """
    def __init__(self, dataPath):
        self.chemin = dataPath

    def get_liste_equipes(self):
        grouplist = {}
        # list game_data games only directoires and teams on subdirectories
        for filename in os.listdir(dataPath + 'game_data/'):

            # print(filename+' is a directory? '+str(os.path.isdir(os.path.join(dataPath+'game_data/',filename))))
            if os.path.isdir(os.path.join(dataPath + 'game_data/', filename)):
                # add key to the dictionary
                grouplist[filename] = []
                for fileteam in os.listdir(dataPath + 'game_data/' + filename):
                    if os.path.isdir(os.path.join(dataPath + 'game_data/' + filename, fileteam)) == True:

                        # read the json file
                        with open(
                                dataPath + 'game_data/' + filename + '/' + fileteam + '/resultats.json') as json_file:
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


class DataManager:
    """
    DataManager gère les données d'une partie

    @ version de Jules Ripol (adaptée à "journal" le code qui génère les pages de journaux)
    @revision : rempalcer group par équipe et team par équipe

    """
    def __init__(self, equipe, partie, dataPath):
        self.group = equipe
        self.team = partie
        self.results_path = dataPath + "game_data/{}/{}/resultats.json".format(equipe, partie)
        self.scores_path = dataPath + "game_data/{}/{}/scores.json".format(equipe, partie)
        self.mix_path = dataPath + "game_data/{}/{}/mix.json".format(equipe, partie)
        self.initial_mix_path = dataPath + "game_data/mix_init.json"
        self.aggregated_mix_path = dataPath + "game_data/{}/{}/mix_aggregated.json".format(equipe, partie)
        self.occasions_path = dataPath + "game_data/{}/{}/occasions.json".format(equipe, partie)
        self.roles_path = dataPath + "game_data/{}/{}/roles.json".format(equipe, partie)
        self.round_path = dataPath + "game_data/{}/{}/current_round.pkl".format(equipe, partie)
        self.title_path = dataPath + "game_data/{}/{}/annee.txt".format(equipe, partie)
        self.infos_path = dataPath + "game_data/{}/{}/infos.json".format(equipe, partie)
        
    
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

    def get_mix(self):
        with open(self.mix_path, 'r') as file:
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

    def get_results(self):
        with open(self.results_path, "r") as f:
            resultats = json.load(f)
        return resultats

    def get_occasions(self):
        with open(self.occasions_path, "r") as f:
            occasions = json.load(f)
        return occasions

    def get_scores(self):
        with open(self.scores_path, "r") as f:
            scores = json.load(f)
        return scores

    def update_gpt_text(self, character_number, text):
        file_path = dataPath + "game_data/{}/{}/perso{}.txt".format(self.group, self.team, character_number)
        with open(file_path, 'w') as file:
            file.write(text)

    def get_data_for_themes(self, role, theme):
        with open(self.scores_path, "r") as f:
            scores = json.load(f)
        return scores[role][theme][1]
import os
from flaskapp.archiveur import DataManager
from climix.geographe.pays import FR_metro
from flaskapp import maitre_de_jeu as mj
from climix import visualiseur as vi
if __name__ == "__main__":
    chemin = os.path.dirname(os.path.realpath(__file__))
    dataPath = chemin+"/../flaskapp/"
    partie ="S1"
    dm = DataManager(equipe="winn", partie=partie, chemin=dataPath)
    dm.init_partie()
    data = FR_metro.get_fichier("mix_init")
    save = FR_metro.get_fichier("save_init")

    data["carte"] = FR_metro.nom
    data["stock"] = 1
    data["annee"] = 2030
    data["stock"] = 10
    data["occ"]["methanation"] = 2
    data["pac"]["methanation"] = 2
    data["naq"]["methanation"] = 2
    data["occ"]["eolienneOFF"] = 1
    data["pac"]["eolienneOFF"] = 1
    data["naq"]["eolienneOFF"] = 1
    data["occ"]["panneauPV"] = 1
    data["pac"]["panneauPV"] = 1
    data["naq"]["panneauPV"] = 1
    data["occ"]["eolienneON"] = 1
    data["pac"]["eolienneON"] = 1
    data["naq"]["eolienneON"] = 1

    input = mj.inputs_from_save_and_data(save, data)

    annee = str(data["annee"])

    dm.set_item_fichier(fichier='inputs', item=annee, val=input)

    input["scenario"] = partie
    result, save, chroniques = mj.strat_stockage_main(**input)

    dm.set_chroniques(chroniques,annee)
    dm.set_fichier(fichier='save_tmp', dico=save)
    dm.set_item_fichier(fichier='resultats', item=annee, val=result)

    chroniques = dm.get_chroniques(annee)
    self = vi.vProduction(chroniques)
    #self.show(self.fig_prod())
    self.show(self.fig_stock())
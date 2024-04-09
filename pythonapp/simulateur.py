import os
from flaskapp.archiveur import DataManager
from climix.geographe.pays import FR_metro
from flaskapp import maitre_de_jeu as mj

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
    input = mj.inputs_from_save_and_data(save, data)

    annee = str(data["annee"])

    dm.set_item_fichier(fichier='inputs', item=annee, val=input)

    input["scenario"] = partie
    result, save, chroniques = mj.strat_stockage_main(**input)

    dm.set_chroniques(chroniques)
    dm.set_fichier(fichier='save_tmp', dico=save)
    dm.set_item_fichier(fichier='resultats', item=annee, val=result)

import os
import sys,json
sys.path.append('../')
from constantes import dataPath, host, CAS_SERVICE_URL, CAS_SERVER_URL
from flask import Blueprint, Flask,render_template, session,request, redirect, url_for, jsonify
from flask import current_app

from archiveur import Parties, DataManager

jeu_blueprint = Blueprint('jeu', __name__)

json_opts = {"indent": 4, "sort_keys": True}


def normap(value, start1, stop1, start2, stop2):
    OldRange = (stop1 - start1)
    if OldRange == 0:
        NewValue = start2
    else:
        NewRange = (stop2 - start2)
        NewValue = (((value - start1) * NewRange) / OldRange) + start2

    return NewValue


def get_group_list():
    grouplist = Parties(dataPath=dataPath).get_liste_equipes()

    for equipe in grouplist:
        for partie in grouplist[equipe] :
            percent = normap(int(partie['data']), 2030, 2050, 0, 100)
            partie['percent'] = percent

    return grouplist

def verif_fichier(fich, rep="", format=".json"):
    ok = True
    try:
        src = open(rep + "/" + fich + format, "r")
        dic = json.load(src)
    except :
        ok = False
    return ok

def creer_dossier(chemin_dossier):
    if not os.path.exists(chemin_dossier):
        os.makedirs(chemin_dossier)

def get_rol(equipe, partie):
    data_role = DataManager(equipe=equipe, partie=partie,dataPath=dataPath).get_roles()
    return data_role

    
@jeu_blueprint.route('/jeu/jeu_index')
def jeu_index():
    grouplist = get_group_list()
    return(render_template('jeux_index.html', username='username', grouplist=grouplist, role=session['role'], equipe=session['equipe'], partie=session['partie']))



@jeu_blueprint.route('/jeu/jeu_manual/<equipe>/<partie>')
def jeu_manual(equipe, partie):
    return(render_template('jeu_manual.html', equipe=equipe, partie=partie))


@jeu_blueprint.route('/jeu/jeu_index/manual/<equipe>/<partie>')
def manual(equipe, partie):
    
    ok = True
    data_dir = dataPath + "game_data/{}/{}".format(equipe, partie)
    for file in ["save", "mix", "resultats", "inputs", "logs"]:
        ok = ok and verif_fichier(fich=file, rep=data_dir)
    
    if ok:
        session['equipe'] = equipe
        session['partie'] = partie
        return(render_template("manual.html", annee_default_value= ''))
    else:
        return(redirect('/'))


@jeu_blueprint.route('/jeu/statut')
def statut():
    if session['role'] == 'voyeur':
        session['role'] = 'scribe'
    else:
        session['role'] = 'voyeur'
    return(redirect('/'))

@jeu_blueprint.route('/jeu/jeu_index/manual/oldmix')
def oldmix():
    return None

# @jeu_blueprint.route('/jeu/jeu_manual/<equipe>/<partie>')
# def jeu_manual(equipe, partie):
#     return(render_template('jeu_manual.html', equipe=equipe, partie=partie))

@jeu_blueprint.route('/jeu/jeu_init/<equipe>/<partie>', methods=['GET', 'POST'])
def jeu_init(equipe, partie):
    equipe = session['equipe']
    partie = session['partie']
    grouplist = get_group_list()
    chemin_dossier = f'game_data/{equipe}/{partie}'
    chemin_fichier = f'{chemin_dossier}/infos.json'
    scenario = None
    password = None
    player = []

    if request.method == 'POST':
        data = {
            'nom': request.form['nomInput'],
            'prenom': request.form['prenomInput'],
            'genre': request.form['genreInput'],
            'role': request.form['roleInput']
        }

        if not os.path.exists(chemin_dossier):
            os.makedirs(chemin_dossier, exist_ok=True)

        if os.path.exists(chemin_fichier):
            with open(chemin_fichier, 'r') as file:
                infos = json.load(file)
                n = len(infos) + 1
                infos["joueur"+str(n)] = data
        else:
            infos = {
                "scrib": {
                    'password': request.form['passwordInput'],
                    'scenario_ademe': request.form['scenarioInput']
                },
                "joueur1": data
            }

        with open(chemin_fichier, 'w') as file:
            json.dump(infos, file, indent=4)

    if os.path.exists(chemin_fichier):
        with open(chemin_fichier, 'r') as file:
            infos = json.load(file)
            scenario = infos['scrib']['scenario_ademe']
            password = infos['scrib']['password']
            for key, joueur in infos.items():
                if key.startswith('joueur'):
                    player.append({
                        'nom': joueur['nom'],
                        'prenom': joueur['prenom'],
                        'genre': joueur['genre'],
                        'role': joueur['role']
                    })

    return render_template('jeu_init.html', equipe=equipe, partie=partie, scenario = scenario, password = password, grouplist=get_group_list(), player=player)#, data_roles=get_rol(), player=player)

@jeu_blueprint.route('/jeu/authentification/<equipe>/<partie>')
def authentification(equipe, partie):
    session['equipe'] = equipe
    session['partie'] = partie
    dm = DataManager(equipe=equipe, partie=partie, dataPath=dataPath)
    if not os.path.exists(dm.infos_path):
        return (redirect('/jeu/jeu_init/<equipe>/<partie>'))
    else:
        return render_template("authentification.html", partie=partie, equipe=equipe)

@jeu_blueprint.route('/jeu/jeu_index/verification')
def verification_mdp():
    equipe = session['equipe']
    partie = session['partie']
    
    password_entered = request.form.get('password')
    dm = DataManager(equipe=equipe, partie=partie, dataPath=dataPath)
    
    if os.path.exists(dm.infos_path):
        with open(dm.infos_path, 'r') as json_file:
            infos = json.load(json_file)
            
    return None
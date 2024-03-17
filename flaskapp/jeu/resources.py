import os
import sys, json
from flaskapp.constantes import dataPath, host, CAS_SERVICE_URL, CAS_SERVER_URL
from flask import Blueprint, Flask, render_template, session, request, redirect, url_for, jsonify
from flask import current_app

from flaskapp.archiveur import Parties, DataManager

jeu_blueprint = Blueprint('jeu', __name__)


def get_parties_de_session():
    """
    Retourne les parties d'une session.
    Dictionnaire de type [equipe][partie] contenant le dict
    de la partie {pouvoir: , annee: }

    """

    if "parties" not in session:
        session['parties'] = {}

    return session.get("parties")


def get_partie_courante_de_session():
    """
        retourne les infos de la partie courante :

        equipe , partie, pouvoir, annee

    """
    parties = get_parties_de_session()

    if ("equipe" not in session) or ("partie" not in session):
        equipe = ""
        partie = ""
        pouvoir = ""
        annee = ""
    else:
        equipe = session.get('equipe')
        partie = session.get('partie')
        if (equipe in parties) and (partie in parties[equipe]):
            pouvoir = parties[equipe][partie]["pouvoir"]
            annee = parties[equipe][partie]["annee"]
        else:
            pouvoir = ""
            annee = ""

    return equipe, partie, pouvoir, annee


def verifie_bonne_route(equipe, partie):
    """
        Donne l'état de la route <équipe>/<partie> par rapport à la session de
        l'utilisateur stockée avec flask.session

        Returns: status, equipe, partie, pouvoir, annee, msg
        status  -> "Courante" s'il s'agit bien de la partie courante
                -> "Changement" il s'agit d'une partie en cours mais pas la courante
                -> "Nouvelle" : partie valide jamais rencontrée avant
                -> "Erreur" : ne correspond pas à une partie valide

    """
    equipe_courante, partie_courante, pouvoir, annee = get_partie_courante_de_session()

    if (equipe_courante == equipe) and (partie_courante == partie):
        return "Courante", equipe_courante, partie_courante, pouvoir, annee, None

    parties = get_parties_de_session()
    if (equipe in parties) and (partie in parties[equipe]):
        session['equipe'] = equipe
        session['partie'] = partie
        status = "Changement"
        err_msg = "Changement de partie"
    else:
        # TODO verifier le changement de partie
        dm = DataManager(equipe, partie)
        if dm.est_ok():
            session['equipe'] = equipe
            session['partie'] = partie
            status = "Nouvelle"
            msg = "prise en main de partie"
        else:
            erreur_msg = ('Erreur ' + 'pas de bon fichiers dans ' + dm.chemin + ' <a href="/"> Retour </a>', 404)
            return "Erreur", "", "", "", "", erreur_msg

        equipe, partie, pouvoir, annee = get_partie_courante_de_session()

        return status, equipe, partie, pouvoir, annee, msg


def set_scribe_de_partie_dans_session(equipe, partie):
    """

        Met à jour "parties" en ajoutant le pouvoir de Scribe à la session.

    """
    parties = get_parties_de_session()
    parties[equipe][partie]["pouvoir"] = "Scribe"
    session["parties"] = parties

@jeu_blueprint.route('/jeu/index')
def index():
    parties = get_parties_de_session()

    ## inutile à mon avis de savoir la partie courante pour la page index
    equipe, partie, pouvoir, annee = get_partie_courante_de_session()

    return render_template('jeux_index.html',
                            username = 'username',
                            grouplist = Parties().get_group_list(),  #Les parties de tout le serveur
                            parties = parties,                      # Les parties de la session courante du joueurs
                           ## La suite me parait inutile pour cette page
                           ## puisque il faut voir dans parties si un rôle existe
                            role=pouvoir,
                            equipe=equipe,
                            partie=partie
                           )


@jeu_blueprint.route('/jeu/init/<equipe>/<partie>/<pouvoir>')
def init(equipe, partie, pouvoir):

    status, equipe_courante, partie_courante, pouvoir_courant, annee, msg_erreur = verifie_bonne_route(equipe, partie)

    if (status == "Courante") or (status == "Changement"):
        # On revient éditer la partie en cours, ou une différente déjà prise en main

        if pouvoir_courant == pouvoir == "Scribe":
            # scribe veut modifier role ou mdp. Pas besoin de vérifier les droits

            return render_template('jeu_init.html', equipe=equipe, partie=partie, scenario="scenario", password="password",
                                   grouplist="grouplist", player="player")
        elif pouvoir == "Scribe":
            # On est non scribe et on veut devenir scribe : redirect à authentification check passwd?

            return redirect("/jeu/authentification/"+equipe+"/"+partie)

    elif (status == "Nouvelle") and (DataManager(equipe, partie).get_mdp() is not None):
        # partie nouvelle pour la session d'utilisateur mais déjà prise par un mot de passe de scribe
        # redirect vers authentification pour vérifier le mot de passe et passer scribe

        return redirect("/jeu/authentification/" + equipe + "/" + partie)

    elif status == "Nouvelle":
        # partie nouvelle et pas de mot de passe
        # page d'authentification avec set du passwd

        return render_template('jeu_init.html', equipe=equipe, partie=partie, scenario="scenario", password="password",
                               grouplist="grouplist", player="player")
    else :
        # fausse route
        return msg_erreur


@jeu_blueprint.route('/jeu/authentification/<equipe>/<partie>')
def authentification(equipe, partie):
    status, equipe, partie, pouvoir, annee, msg_erreur = verifie_bonne_route(equipe, partie)

    if pouvoir == "Scribe":
        return redirect('/jeu/init/'+equipe+'/'+partie+'/Scribe')
    else:
        return render_template("authentification.html", partie=partie, equipe=equipe)


@jeu_blueprint.route('/jeu/check_pwd/<equipe>/<partie>', methods=['POST', 'GET'])
def check_pswd(equipe, partie):
    mot_de_pass_ok = True
    if mot_de_pass_ok:
        set_scribe_de_partie_dans_session(equipe, partie)

    return redirect("/jeu/init/"+equipe+"/"+partie+"/Scribe")

@jeu_blueprint.route('/jeu/manual/<equipe>/<partie>')
def manual(equipe, partie):
    """
    Render du manual navigable en année
    """

    status, equipe, partie, pouvoir, annee, msg = verifie_bonne_route(equipe, partie)
    if status=="Courante":
        return render_template("manual.html", annee_default_value=annee)
    if status == "Changement":
        return render_template("manual.html", annee_default_value=annee)
    else:
        return msg



### Ici le vieux code à adpater/enlever


@jeu_blueprint.route('/jeu/jeu_init/<equipe>/<partie>', methods=['GET', 'POST'])
def jeu_init(equipe, partie):

    status, equipe, partie, pouvoir, annee, msg = verifie_bonne_route(equipe, partie)
    ok, erreur_msg = verifie_bonne_route(equipe, partie)
    if ok:

        #   equipe = session['equipe']
        #partie = session['partie']
        dm = DataManager(equipe, partie)
        grouplist = Parties().get_group_list()
        chemin_dossier = dm.chemin
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

        return render_template('jeu_init.html', equipe=equipe, partie=partie, scenario = scenario, password = password, grouplist=grouplist, player=player)#, data_roles=get_rol(), player=player)
    else:
        return erreur_msg


@jeu_blueprint.route('/jeu/jeu_index/verification')
def verification_mdp():
    equipe = session['equipe']
    partie = session['partie']
    
    password_entered = request.form.get('password')
    dm = DataManager(equipe=equipe, partie=partie, chemin=dataPath)
    
    if os.path.exists(dm.infos_path):
        with open(dm.infos_path, 'r') as json_file:
            infos = json.load(json_file)
            
    return None
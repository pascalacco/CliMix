from flask import Flask, request, jsonify, render_template, redirect, make_response, send_file
from flask_cors import CORS, cross_origin
import jinja2
import json


from flaskapp.admin.resources import admin_blueprint, parties


from flaskapp.archiveur import DataManager
from flaskapp import archiveur
from flaskapp import maitre_de_jeu
from climix import visualiseur

# Set up Flask:
app = Flask(__name__)
app.secret_key = 'fdsfds3215zez'
app.register_blueprint(admin_blueprint)

# Bypass CORS at the front end:
cors = CORS(app)
CORS(app, support_credentials=True)


@app.route('/index')
@cross_origin(support_credentials=True)
def home_html():
    return render_template("index.html")


@app.route('/set_group', methods=["POST"])
@cross_origin(support_credentials=True)
def set_group():

    data = request.get_json()
    equipe = data[0]
    partie = data[1]
    action = data[2]

    dm = DataManager(equipe=equipe, partie=partie)
    if action == "new":
        maitre_de_jeu.initialise_partie(dm)
    if dm.est_ok():
        resp = make_response(jsonify(["log_in_success"]))
        resp.set_cookie(key="groupe", value=equipe, samesite="Lax")
        resp.set_cookie(key="equipe", value=partie, samesite="Lax")
    else:
        if action != "new":
            resp = make_response(["err",
                                  "Partie " + equipe + "/" + partie + " n'existe pas. <br>Cliquez sur le bouton 'nouvelle partie' pour la créer "])
        else:
            resp = make_response(jsonify(["log_in_error pour " + equipe + "/" + partie]))
    return resp



@app.route('/enregistrer_noms/<equipe>/<partie>/')
def enregistrer_noms(equipe, partie):
    return make_response(render_template("enregistrer_noms.html", equipe=equipe, partie=partie, annee="2030"))

@app.route('/save_names', methods=["POST"])
@cross_origin(support_credentials=True)
def save_names():
    data = request.get_json()
    equipe = data["equipe"]
    partie = data["partie"]
    names = data["names"]
    pronouns = data["pronouns"]
    roles = data["roles"]
    roles_dict = {
        "names":names,
        "pronouns":pronouns,
        "roles":roles
    }
    dm, msg = parties.get_data_manager(equipe=equipe, partie=partie)

    with open(f"{dm.chemin}/roles.json", "w", encoding="utf-8") as f:

        json.dump(roles_dict, f, ensure_ascii=False, **DataManager.json_opts)
    
    return jsonify({"status": "success"})

@app.route('/saisie/<equipe>/<partie>/')
def saisie(equipe, partie):

    dm = DataManager(equipe=equipe, partie=partie)
    mix, annee_active = maitre_de_jeu.recup_mix(dm, "2030")
    resp = saisie_html(equipe=equipe, partie=partie, annee=annee_active)
    return resp


@app.route('/saisie/<equipe>/<partie>/<annee>')
def saisie_html(equipe, partie, annee):

    dm = DataManager(equipe=equipe, partie=partie)
    mix, annee_active = maitre_de_jeu.recup_mix(dm, annee)
    resp = make_response(
        render_template("saisie.html", equipe=equipe, partie=partie, annee=annee,
                        actif=mix['actif'], annee_active=annee_active,
                        unites=mix["unites"], nb=mix["nb"], capacites=mix["capacites"], actions=mix["actions"],
                        reg_convert=maitre_de_jeu.reg_convert, pion_convert=maitre_de_jeu.pion_convert,
                        pion_short=maitre_de_jeu.pion_short,
                        aleas=maitre_de_jeu.aleas)
    )
    return resp


@app.route('/get_mixes/<equipe>/<partie>')
def get_mixes_partie(equipe, partie, dm=None):

    if dm is None:
        dm = DataManager(equipe=equipe, partie=partie)

    mixes = dm.get_fichier(fichier='mixes')
    return jsonify(mixes)



@app.route('/get_mix/<equipe>/<partie>/<annee>')
def get_mix_annee(equipe, partie, annee, dm=None):
    """
        Récupère le bon mix avec le datamanger dm.
        Si l'année est la suivante créée un nouveau mix)
    :param equipe:
    :param partie:
    :param annee:
    :param dm: DataManager
    """

    if dm is None:
        dm = DataManager(equipe=equipe, partie=partie)

    mix, annee_active = maitre_de_jeu.recup_mix(dm=dm, annee=annee)
    return jsonify(mix)



@app.route('/calculer/<equipe>/<partie>/<annee>', methods=["POST"])
def calculer(equipe, partie, annee):
    try:
        dm = DataManager(equipe=equipe, partie=partie)
        actions = request.get_json()
        resp = maitre_de_jeu.calculer(dm=dm, annee=annee, actions=actions, scenario=partie)

    except maitre_de_jeu.errJeu as ex:

        resp = ["errJeu", ex.__str__()]

    resp = jsonify(resp)

    return resp


@app.route("/commit/<equipe>/<partie>/<annee>")
def commit(equipe, partie, annee):

    dm = DataManager(equipe=equipe, partie=partie)

    annee_suivante_int = int(annee) + 5
    annee_suivante = annee_suivante_int.__str__()
    new = dm.get_fichier("new")
    new["actif"] = False

    dm.set_item_fichier(fichier='mixes', item=annee, val=new)

    if annee_suivante_int > 2050:
        return redirect("/sauvegarder/" + equipe + "/" + partie + "/" + annee)
    else:
        return redirect("/saisie/" + equipe + "/" + partie + "/" + annee_suivante)



@app.route("/telecharger/<path:chemin>", methods=["GET"])
def telecharger(chemin):

    return send_file(chemin)


@app.route("/sauvegarder/<equipe>/<partie>/<annee>")
def sauvegarder(equipe, partie, annee):

    dm = DataManager(equipe=equipe, partie=partie)
    fichier = dm.sauve_tout(annee)
    repertoire_relatif = ("/telecharger/" +
                          archiveur.Parties.chemin_game_data_relatif +
                          equipe + "/")

    t = jinja2.Template('<a href="{{path_to_file}}" download="{{proposed_file_name}}">Télécharger</a>')
    return make_response(render_template('fin.html',
                                         equipe=equipe, partie=partie,
                                         annee=annee, annee_suivante=(int(annee)+5).__str__(),
                                         fichier=fichier,
                                         path_to_file=repertoire_relatif + fichier,
                                         proposed_file_name=fichier)
                         )



@app.route('/vues/<equipe>/<partie>/<annee>')
@app.route('/vues/<equipe>/<partie>/<annee>/<vue>')
def vues_html(equipe, partie, annee, vue="resultats"):
    dm, msg = parties.get_data_manager(equipe=equipe, partie=partie)

    vw = visualiseur.vuesClasses[vue](dm, annee, vue)
    vw.genere_jinja_parameters()
    jinja_params = vw.get_jinja_parameters()

    try:
        # return make_response(html)
        resp = make_response(
            render_template("vue_" + vue + ".html", **jinja_params)
        )
    except:
        resp = make_response(
            render_template("vue_generique.html", **jinja_params)
        )
    return resp



@app.route('/get_results/<equipe>/<partie>', methods=["GET"])
def get_results(equipe, partie):

    dm = DataManager(equipe=equipe, partie=partie)
    resultats = dm.get_fichier(fichier='resultats')
    return jsonify(resultats)



@app.route('/get_results')
@cross_origin()
def get_resultats():
    equipe = request.cookies.get("groupe")
    partie = request.cookies.get("equipe")
    return get_results(equipe, partie)


# TESTS EN LOCAL:

if __name__ == "__main__":
    app.run(debug=True)

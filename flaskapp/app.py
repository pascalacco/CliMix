from flask import Flask, request, jsonify, render_template, redirect, make_response
from flask_cors import CORS, cross_origin

import datetime
import traceback
import os

dataPath = os.path.dirname(os.path.realpath(__file__))+'/'

from bokeh.resources import INLINE

from flaskapp.archiveur import DataManager
from flaskapp import maitre_de_jeu
from climix import visualiseur

# Set up Flask:
app = Flask(__name__)


# Bypass CORS at the front end:
cors = CORS(app)
CORS(app, support_credentials=True)


@app.route('/')
@cross_origin(support_credentials=True)
def home_html():
    return render_template("index.html")


@app.route('/set_group', methods=["POST"])
@cross_origin(support_credentials=True)
def set_group():
    try:
        data = request.get_json()
        equipe = data[0]
        partie = data[1]
        action = data[2]

        dm = DataManager(equipe=equipe, partie=partie)
        if action == "new":
            dm.init_partie()

        if dm.est_ok():
            resp = make_response(jsonify(["log_in_success"]))
            resp.set_cookie(key="groupe", value=equipe, samesite="Lax")
            resp.set_cookie(key="equipe", value=partie, samesite="Lax")
        else:
            if action != "new":
                resp = make_response(["err", "Partie " + equipe +"/" + partie + " n'existe pas. <br>Cliquez sur le bouton 'nouvelle partie' pour la créer "])
            else:
                resp = make_response(jsonify(["log_in_error pour " +equipe + "/" + partie]))
    except:
        with open(dataPath + 'logs.txt', 'a') as logs:
            logs.write("[{}] {} \n".format(datetime.datetime.now(), traceback.format_exc()))

        resp = ["err", traceback.format_exc()]

    return resp


@app.route('/manual')
@app.route('/manual/')
@cross_origin(support_credentials=True)
def manual_html():
    try:
        group = request.cookies.get("groupe")
        team = request.cookies.get("equipe")

        if (group is None) or (team is None):
            resp = make_response(redirect("/"))
        else:
            resp = make_response(render_template("manual.html", group=group, team=team))

    except:
        with open(dataPath + 'logs.txt', 'a') as logs:
            logs.write("[{}] {} \n".format(datetime.datetime.now(), traceback.format_exc()))

        resp = ["err", traceback.format_exc()]

    return resp


@app.route('/get_mix')
@cross_origin(support_credentials=True)
def get_mix():
    try:
        equipe = request.cookies.get("groupe")
        partie = request.cookies.get("equipe")
        dm = DataManager(equipe=equipe, partie=partie)

        mix = dm.get_fichier("mix")

        return jsonify(mix)
    except:
        with open(dataPath + 'logs.txt', 'a') as logs:
            logs.write("[{}] {} \n".format(datetime.datetime.now(), traceback.format_exc()))

        return ["err", traceback.format_exc()]


# Create the production API POST endpoint:
@app.route("/production", methods=["POST"])
@cross_origin(supports_credentials=True)
def prodCompute():
    try:
        equipe = request.cookies.get("groupe")
        partie = request.cookies.get("equipe")
        dm = DataManager(equipe=equipe, partie=partie)

        data = request.get_json()
        save = dm.get_fichier("save")

        maitre_de_jeu.assert_capacitees(save, data)

        input = maitre_de_jeu.inputs_from_save_and_data(save, data)

        annee = str(data["annee"])

        dm.set_item_fichier(fichier='inputs', item=annee, val=input)

        input["scenario"] = partie
        result, save, chroniques = maitre_de_jeu.strat_stockage_main(**input)

        dm.set_chroniques(chroniques)
        dm.set_fichier(fichier='save_tmp', dico=save)
        dm.set_item_fichier(fichier='resultats', item=annee, val=result)

        resp = ["success"]

        dm.set_fichier(fichier='mix', dico=data)

    except maitre_de_jeu.errJeu as ex:
        resp = ["errJeu", ex.__str__()]

    except:
        with open(dataPath + 'logs.txt', 'a') as logs:
            logs.write("[{}] {} \n".format(datetime.datetime.now(), traceback.format_exc()))
        resp = ["err", traceback.format_exc()]
    resp = jsonify(resp)

    return resp


@app.route("/commit")
@cross_origin(supports_credentials=True)
def commitResults():
    try :
        equipe = request.cookies.get("groupe")
        partie = request.cookies.get("equipe")
        dm = DataManager(equipe=equipe, partie=partie)

        newSave = dm.cp_fichier(src='save_tmp', dst='save')
        mix = dm.set_item_fichier(fichier='mix', item='actif', val=False)

        if newSave["annee"] == 2055:
            return redirect("/")
        else:
            return redirect("/manual")

    except:
        with open(dataPath + 'logs.txt', 'a') as logs:
            logs.write("[{}] {} \n".format(datetime.datetime.now(), traceback.format_exc()))
        resp = ["err", traceback.format_exc()]
    resp = jsonify(resp)

    return resp

@app.route('/vues/<vue>')
@app.route('/vues/')
@app.route('/vues')
@cross_origin(support_credentials=True)
def vues(vue="resultats"):
    try:
        equipe = request.cookies.get("groupe")
        partie = request.cookies.get("equipe")
        dm = DataManager(equipe=equipe, partie=partie)

        if (equipe is None) or (partie is None):
            resp = make_response(redirect("/"))
        else:

            chroniques = dm.get_chroniques()
            vw = visualiseur.vuesClasses[vue](chroniques)
            vw.set_figs()
            composants = vw.get_composants()
            resources = INLINE.render()
            script = composants["script"]
            divs = composants["divs"]
            jinja_params = {"group": equipe,
                            "team": partie,
                            "vue": vue,
                            "bokeh_ressources": INLINE.render(),
                            "bokeh_script": script,
                            "bokeh_divs": divs
                            }
            try:
                # return make_response(html)
                resp = make_response(
                    render_template("vue_" + vue + ".html", **jinja_params)
                )
            except:
                resp = make_response(
                    render_template("vue_generique.html", **jinja_params)
                    )

    except:
        with open(dataPath + 'logs.txt', 'a') as logs:
            logs.write("[{}] {} \n".format(datetime.datetime.now(), traceback.format_exc()))
        resp = ["err", traceback.format_exc()]
    return resp


@app.route('/results')
@app.route('/results/')
@cross_origin(support_credentials=True)
def results_html():
    try:
        equipe = request.cookies.get("groupe")
        partie = request.cookies.get("equipe")

        if (equipe is None) or (partie is None):
            resp = make_response(redirect("/"))
        else:
            resp = make_response(render_template("results.html", group=equipe, team=partie))

        return resp

    except:
        with open(dataPath + 'logs.txt', 'a') as logs:
            logs.write("[{}] {} \n".format(datetime.datetime.now(), traceback.format_exc()))
        resp = ["err", traceback.format_exc()]
        return resp


@app.route('/get_results')
@cross_origin(support_credentials=True)
def get_results():
    try:
        equipe = request.cookies.get("groupe")
        partie = request.cookies.get("equipe")
        dm = DataManager(equipe=equipe, partie=partie)

        resultats = dm.get_fichier(fichier='resultats')

        return jsonify(resultats)

    except:
        with open(dataPath + 'logs.txt', 'a') as logs:
            logs.write("[{}] {} \n".format(datetime.datetime.now(), traceback.format_exc()))
        resp = ["err", traceback.format_exc()]
        return resp


@app.route('/get_events')
@cross_origin(support_credentials=True)
def get_events():
    try:
        equipe = request.cookies.get("groupe")
        partie = request.cookies.get("equipe")
        dm = DataManager(equipe=equipe, partie=partie)

        resultats = dm.get_fichier(fichier='resultats')

        events = {}
        for annee in resultats:
            if "remplacement" in resultats[annee]:
                events[annee] = resultats[annee]["remplacement"]
            else:
                events[annee] = []

        return jsonify(events)
    except:
        with open(dataPath + 'logs.txt', 'a') as logs:
            logs.write("[{}] {} \n".format(datetime.datetime.now(), traceback.format_exc()))
        resp = ["err", traceback.format_exc()]
        return resp


# TESTS EN LOCAL:

if __name__ == "__main__":
    app.run(debug=True)

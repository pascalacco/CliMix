from flask import Flask, request, jsonify, render_template, redirect, make_response
from flask_cors import CORS, cross_origin

import json
import datetime
import traceback
import exc

import strat_stockage
from constantes import *

from api.resources import api_blueprint
from bokeh.resources import INLINE

from flaskapp.archiveur import DataManager

# Set up Flask:
app = Flask(__name__)

app.register_blueprint(api_blueprint)

# Bypass CORS at the front end:
cors = CORS(app)
CORS(app, support_credentials=True)

json_opts = {"indent": 4, "sort_keys": True}


def inputs_from_save_and_data(save, data):
    # TRAITEMENT SUPPLEMENTAIRE POUR LE NUCLEAIRE AU 1ER TOUR

    """

    if data["annee"] == 2030:
        save["hdf"]["centraleNuc"][0:6] = [1995, 1995, 1995, 1995, 1995, 1995]
        save["occ"]["centraleNuc"][0:2] = [2020, 2020]
        save["naq"]["centraleNuc"][0:6] = [1995, 1995, 1995, 1995, 2000, 2000]
        save["pac"]["centraleNuc"][0:8] = [2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000]
        save["cvl"]["centraleNuc"][0:7] = [2005, 2005, 2005, 2005, 2005, 2005, 2005]
        save["bfc"]["centraleNuc"][0:2] = [2005, 2005]
        save["est"]["centraleNuc"][0:5] = [2005, 2010, 2010, 2010, 2010]
        save["ara"]["centraleNuc"][0:3] = [2010, 2010, 2010]
        save["nor"]["centraleNuc"][0:8] = [2010, 2010, 2010, 2020, 2020, 2020, 2020, 2020]
    """
    # CALCUL NOMBRE DE NOUVEAU PIONS + TOTAL A CE TOUR
    nvPionsReg = {
        "hdf": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "idf": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "est": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "nor": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "occ": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "pac": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "bre": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "cvl": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "pll": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "naq": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "ara": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "bfc": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0},
        "cor": {"eolienneON": 0, "eolienneOFF": 0, "panneauPV": 0, "methanation": 0, "EPR2": 0, "biomasse": 0}
    }

    nvPions = {
        "eolienneON": 0,
        "eolienneOFF": 0,
        "panneauPV": 0,
        "methanation": 0,
        "EPR2": 0,
        "biomasse": 0
    }

    nbPions = {
        "eolienneON": 0,
        "eolienneOFF": 0,
        "panneauPV": 0,
        "methanation": 0,
        "centraleNuc": 0,
        "EPR2": 0,
        "biomasse": 0
    }

    for reg in save["capacite"]:
        nbPions["centraleNuc"] += data[reg]["centraleNuc"]
    if data["annee"] == 2030 and nbPions["centraleNuc"] != 47:
        raise exc.errMixInit
    else:
        nbPions["centraleNuc"] = 0

    for reg in save["capacite"]:
        for p in data[reg]:
            nbPions[p] += data[reg][p]

            if p == "eolienneON" or p == "eolienneOFF":
                eolSuppr = len(save[reg][p]) - data[reg][p]
                for i in range(eolSuppr):
                    save[reg][p].remove(data["annee"] - 15)

            if p != "centraleNuc":
                nvPionsReg[reg][p] = data[reg][p] - len(save[reg][p])
                nvPions[p] += data[reg][p] - len(save[reg][p])

                for i in range(nvPionsReg[reg][p]):
                    save[reg][p].append(data["annee"])
            else:
                nucSuppr = len(save[reg][p]) - data[reg][p]
                for i in range(nucSuppr):
                    save[reg][p].remove(data["annee"] - 40)

    return {"mix": data, "save": save, "nbPions": nbPions, "nvPions": nvPions, "nvPionsReg": nvPionsReg}



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
            resp = make_response(jsonify(["log_in_error"]))

    except:
        resp = jsonify(["log_in_error"])

        with open(dataPath + 'logs.txt', 'a') as logs:
            logs.write("[{}] {} \n".format(datetime.datetime.now(), traceback.format_exc()))

    return resp


@app.route('/manual')
@app.route('/manual/')
@cross_origin(support_credentials=True)
def manual_html():
    group = request.cookies.get("groupe")
    team = request.cookies.get("equipe")

    if (group is None) or (team is None):
        resp = make_response(redirect("/"))
    else:
        resp = make_response(render_template("manual.html", group=group, team=team))

    return resp




@app.route('/get_mix')
@cross_origin(support_credentials=True)
def get_mix():
    equipe = request.cookies.get("groupe")
    partie = request.cookies.get("equipe")
    dm = DataManager(equipe=equipe, partie=partie)

    mix = dm.get_fichier("mix")

    return jsonify(mix)


# Create the production API POST endpoint:
@app.route("/production", methods=["POST"])
@cross_origin(supports_credentials=True)
def prodCompute():
    equipe = request.cookies.get("groupe")
    partie = request.cookies.get("equipe")
    dm = DataManager(equipe=equipe, partie=partie)

    data = request.get_json()
    errDetails = 0

    try:
        save = dm.get_fichier("save")

        # VERIF ANNEE / STOCK / CARTE / CAPACITE LEGITIMES
        if data["annee"] != save["annee"]:
            errDetails = save["annee"]
            raise exc.errAnnee

        if data["stock"] < save["stock"]:
            errDetails = save["stock"]
            raise exc.errStock

        if (data["annee"] != 2030) and (data["carte"] != save["carte"]):
            errDetails = save["carte"]
            raise exc.errCarte

        for reg in save["capacite"]:
            for p in save["capacite"][reg]:
                # if p != "biomasse":
                if data[reg][p] > save["capacite"][reg][p]:
                    errDetails = [reg, p, save["capacite"][reg][p]]
                    raise exc.errSol

        input = inputs_from_save_and_data(save, data)


        if data["alea"] == "MECS3":
            if input["nvPions"]["EPR2"] > 0:
                errDetails = input["nvPions"]["EPR2"]
                raise exc.errNuc

        annee = str(data["annee"])

        dm.set_item_fichier(fichier='inputs', item=annee, val=input)

        input["scenario"] = partie
        result, save = strat_stockage.strat_stockage_main(**input)

        dm.set_fichier(fichier='save_tmp', dico= save)
        dm.set_item_fichier(fichier='resultats', item=annee, val=result)

        resp = ["success"]

        with open(dataPath + "game_data/{}/{}/mix.json".format(equipe, partie), "w") as dst:
            json.dump(data, dst, **json_opts)

    except exc.errAnnee:
        resp = ["errAnnee", errDetails]
    except exc.errStock:
        resp = ["errStock", errDetails]
    except exc.errCarte:
        resp = ["errCarte", errDetails]
    except exc.errSol:
        resp = ["errSol", errDetails]
    except exc.errNuc:
        resp = ["errNuc", errDetails]
    except exc.errMixInit:
        resp = ["errMixInit", None]

    except:
        resp = ["err", None]

        with open(dataPath + 'logs.txt', 'a') as logs:
            logs.write("[{}] {} \n".format(datetime.datetime.now(), traceback.format_exc()))

    resp = jsonify(resp)

    return resp


@app.route("/commit")
@cross_origin(supports_credentials=True)
def commitResults():
    equipe = request.cookies.get("groupe")
    partie = request.cookies.get("equipe")
    dm = DataManager(equipe=equipe, partie=partie)

    newSave = dm.cp_fichier(src='save_tmp', dst='save')
    mix = dm.set_item_fichier(fichier='mix', item='actif', val=False)

    if newSave["annee"] == 2055:
        return redirect("/")
    else:
        return redirect("/manual")


@app.route('/vues/<vue>')
@app.route('/vues/')
@app.route('/vues')
@cross_origin(support_credentials=True)
def vues(vue="general"):
    equipe = request.cookies.get("groupe")
    partie = request.cookies.get("equipe")

    if (equipe is None) or (partie is None):
        resp = make_response(redirect("/"))
    else:
        with open(dataPath+"../StratStockage/production.json") as json_file:
            composant = json.load(json_file)

        resources = INLINE.render()
        script = composant["script"]
        div = composant["div"]

        #return make_response(html)
        resp = make_response(render_template("vue_"+vue+".html",
                                             group=equipe, team=partie, vue=vue,
                                             bokeh_ressources=INLINE.render(),
                                             bokeh_script=composant["script"],
                                             bokeh_div=composant["div"],
                                             ))
    return resp


@app.route('/results')
@app.route('/results/')
@cross_origin(support_credentials=True)
def results_html():
    equipe = request.cookies.get("groupe")
    partie = request.cookies.get("equipe")

    if (equipe is None) or (partie is None):
        resp = make_response(redirect("/"))
    else:
        resp = make_response(render_template("results.html", group=equipe, team=partie))

    return resp


@app.route('/get_results')
@cross_origin(support_credentials=True)
def get_results():
    equipe = request.cookies.get("groupe")
    partie = request.cookies.get("equipe")
    dm = DataManager(equipe=equipe, partie=partie)

    resultats = dm.get_fichier(fichier='resultats')

    return jsonify(resultats)


@app.route('/get_events')
@cross_origin(support_credentials=True)
def get_events():
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



# TESTS EN LOCAL:

if __name__ == "__main__":
    app.run(debug=True)

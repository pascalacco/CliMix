from flask import request, jsonify,Blueprint
from flask_cors import CORS, cross_origin
from flask_restx import Api, Resource
import json

from constantes import *

# Création du Blueprint pour l'API
api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint, prefix="/api", doc="/api/", title="Api du jeu Climix")


# Définition des ressources de l'API
@api.route("/test")
class ExampleResource(Resource):
    def get(self):
        return {"message": "Ok."}


@api.route("/mix")
class Mix(Resource):
    def get(self):
        group = request.cookies.get("groupe")
        team = request.cookies.get("equipe")

        with open(dataPath+"game_data/{}/{}/mix.json".format(group, team), "r") as f:
            mix = json.load(f)

        return jsonify(mix)


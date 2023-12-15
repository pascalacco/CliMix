from flask import Blueprint
from flask_restx import Api, Resource

# Création du Blueprint pour l'API
api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint, prefix="/api", doc="/api/", title="Api du jeu Climix")


# Définition des ressources de l'API
@api.route("/test")
class ExampleResource(Resource):
    def get(self):
        return {"message": "Ok."}

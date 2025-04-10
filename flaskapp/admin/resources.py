""" ADMIN blueprint """
from flask import Blueprint, make_response, render_template, session, request, redirect, jsonify


from flaskapp.archiveur import Parties

# Creation du Blueprint l'administration
admin_blueprint = Blueprint('admin', __name__)

parties = Parties()


@admin_blueprint.route('/admin/tableau_de_bord', methods=['GET'])
def tableau_de_bord():
    grouplist = parties.get_liste_groupes_par_parties()
    return render_template('tableau_de_bord.html',
                           username="Admin",
                           attributes='Public',
                           grouplist=grouplist)


@admin_blueprint.route('/admin/get_infos_parties', methods=["GET"])
def get_infos_parties():
    grouplist = parties.get_liste_groupes_par_parties()
    return jsonify(grouplist)


@admin_blueprint.route('/admin/effacer', methods=["POST"])
def effacer():

    liste = request.get_json()
    messages = parties.effacer(liste)
    return make_response(["success", messages])


@admin_blueprint.route('/admin/post_liste', methods=["POST"])
def comparer_post_list():
    liste = request.get_json()
    etiquette = liste[0]
    if "groups_list" not in session:
        session["groups_list"] = {etiquette: liste}
    else:
        session["groups_list"][etiquette] = liste
        session.update()
    return make_response(redirect("/admin/comparer/"+etiquette))


@admin_blueprint.route('/admin/comparer/<etiquette>')
def comparer(etiquette):
    liste = session.get("groups_list")[etiquette]
    compilation_resultats, annees = parties.compiler_resultats(liste)
    return (make_response(render_template('comparer.html',
                                          liste=liste,
                                          compilation=compilation_resultats,
                                          annees=annees)))

@admin_blueprint.route('/admin/view/<equipe>/<partie>')
def view(equipe, partie):
    return(render_template('view.html', equipe=equipe, partie=partie))

@admin_blueprint.route('/admin/dashboard', methods=['GET'])
def dashboard():
    if 'username' in session and 'admin_climix_man' in session['attributes']['memberOfCN']:
        grouplist = parties.get_liste_equipes()
        return render_template('tableau_de_bord.html', username=session['username'],
                               attributes=session['attributes']['memberOfCN'], grouplist=grouplist)
    return 'Login required. <a href="/admin/login">Login</a>', 403

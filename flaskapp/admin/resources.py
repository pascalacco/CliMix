""" ADMIN blueprint """

import os
import sys, json
sys.path.append('../')
from flask import Blueprint, Flask, make_response, render_template, session, request, redirect, url_for
from flask import current_app

from flaskapp.archiveur import Parties

# Creation du Blueprint l'administration
admin_blueprint = Blueprint('admin', __name__)

partie = Parties()

def normap(value, start1, stop1, start2, stop2):
    OldRange = (stop1 - start1)
    if OldRange == 0:
        NewValue = start2
    else:
        NewRange = (stop2 - start2)
        NewValue = (((value - start1) * NewRange) / OldRange) + start2

    return NewValue


def get_group_list():
    grouplist = Parties().get_liste_equipes()

    for equipe in grouplist:
        for partie in grouplist[equipe] :
            percent = normap(int(partie['data']), 2030, 2050, 0, 100)
            partie['percent'] = percent

    return grouplist


@admin_blueprint.route('/admin/dashboard')
def dashboard(method=['GET']):
    
    if 'username' in session and 'admin_climix_man' in session['attributes']['memberOfCN']:
        grouplist = get_group_list()
        return render_template('tableau_de_bord.html', username=session['username'], attributes=session['attributes']['memberOfCN'], grouplist=grouplist)
    return 'Login required. <a href="/admin/login">Login</a>', 403

@admin_blueprint.route('/admin/comparer/post_liste', methods=["POST"])
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
    return(make_response(render_template('comparer.html', liste=liste)))


@admin_blueprint.route('/admin/tableau_de_bord')
def tableau_de_bord(method=['GET']):
    grouplist = partie.get_liste_groupes_par_parties()
    print(grouplist)
    return render_template('tableau_de_bord.html',
                           username="Admin",
                           attributes='Public',
                           grouplist=grouplist)

@admin_blueprint.route('/admin/view/<equipe>/<partie>')
def view(equipe, partie):
    return(render_template('view.html', equipe=equipe, partie=partie))

import os
import sys,json
sys.path.append('../')
from constantes import dataPath, host, CAS_SERVICE_URL, CAS_SERVER_URL
from flask import Blueprint, Flask,render_template, session,request, redirect, url_for
from flask import current_app

from archiveur import Parties

jeu_blueprint = Blueprint('jeu', __name__)

# def normap(value, start1, stop1, start2, stop2):
#     OldRange = (stop1 - start1)
#     if OldRange == 0:
#         NewValue = start2
#     else:
#         NewRange = (stop2 - start2)
#         NewValue = (((value - start1) * NewRange) / OldRange) + start2

#     return NewValue


# def get_group_list():
#     grouplist = Parties(dataPath=dataPath).get_liste_equipes()

#     for equipe in grouplist:
#         for partie in grouplist[equipe] :
#             percent = normap(int(partie['data']), 2030, 2050, 0, 100)
#             partie['percent'] = percent

#     return grouplist

# @jeu_blueprint.route('/jeu/dashboard')
# def dashboard(method=['GET']):
    
#     if 'username' in session and 'admin_climix_man' in session['attributes']['memberOfCN']:
#         grouplist = get_group_list()
#         return render_template('dashboard.html', username=session['username'], attributes=session['attributes']['memberOfCN'],grouplist=grouplist)
#     return 'Login required. <a href="/admin/login">Login</a>', 403

# @jeu_blueprint.route('/jeu/cheatboard')
# def cheatboard(method=['GET']):    
#     grouplist = get_group_list()
#     print(grouplist)
#     return render_template('dashboard.html',
#                            username="tricheur",
#                            attributes='memberOfCN',
#                            grouplist=get_group_list())

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


@jeu_blueprint.route('/jeu/jeu_index')
def jeu_index():
    grouplist = get_group_list()
    return(render_template('jeux_index.html', username='Ishaac', grouplist=grouplist))



@jeu_blueprint.route('/jeu/jeu_manual/<equipe>/<partie>')
def jeu_manual(equipe, partie):
    return(render_template('jeu_manual.html', equipe=equipe, partie=partie))
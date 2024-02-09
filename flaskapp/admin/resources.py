import os
import sys,json
sys.path.append('../')
from constantes import dataPath, host, CAS_SERVICE_URL, CAS_SERVER_URL
from flask import Blueprint, Flask,render_template, session,request, redirect, url_for
from cas import CASClient
import logging
from flask import current_app


# Création du Blueprint l'administration
admin_blueprint = Blueprint('admin', __name__)



cas_client = CASClient(
    version=3,
    service_url=CAS_SERVICE_URL,
    server_url=CAS_SERVER_URL
)


def normap(value, start1, stop1, start2, stop2):
    OldRange = (stop1 - start1)
    if OldRange == 0:
        NewValue = start2
    else:
        NewRange = (stop2 - start2)
        NewValue = (((value - start1) * NewRange) / OldRange) + start2

    return NewValue

@admin_blueprint.route('/admin/dashboard')
def dashboard(method=['GET']):
    grouplist = {}
    if 'username' in session and 'admin_climix_man' in session['attributes']['memberOfCN']:
        # list game_data games only directoires and teams on subdirectories
        for filename in os.listdir(dataPath+'game_data/'):


            #print(filename+' is a directory? '+str(os.path.isdir(os.path.join(dataPath+'game_data/',filename))))
            if os.path.isdir(os.path.join(dataPath+'game_data/',filename)):
                # add key to the dictionary
                grouplist[filename] = []
                for fileteam in os.listdir(dataPath + 'game_data/'+filename):
                    if os.path.isdir(os.path.join(dataPath+'game_data/'+filename,fileteam)) == True:

                        #read the json file
                        with open(dataPath + 'game_data/'+filename+'/'+fileteam+'/resultats.json') as json_file:
                            data = json.load(json_file)
                            currentYear=0
                            #get the first key of the json file
                            for key in data.keys():
                                #check if it's empty
                                if data[key] == {}:
                                    #remove the empty key
                                    currentYear = key
                                    print(currentYear)
                                    #exite the for loop
                                    break
                            percent= normap(int(currentYear), 2030, 2050, 0, 100)
                            grouplist[filename].append({'team':fileteam,'data':currentYear,'percent':percent})
                            #grouplist[filename]{'team':fileteam,'data':'data'})

        #grouplist = sorted(grouplist, key=lambda d: d['group']+d['team'])
        #sort the dictionary by key
        grouplist = dict(sorted(grouplist.items()))
        #sort the list of teams by team name
        for key in grouplist:
            grouplist[key] = sorted(grouplist[key], key=lambda d: d['team'])

        print(grouplist)
        return render_template('dashboard.html', username=session['username'], attributes=session['attributes']['memberOf'],grouplist=grouplist)
    return 'Login required. <a href="/login">Login</a>', 403


@admin_blueprint.route('/admin/login')
def login():
    if 'username' in session:
        # Already logged in
        return redirect(url_for('admin.dashboard'))

    next = request.args.get('next')
    ticket = request.args.get('ticket')
    if not ticket:
        # No ticket, the request come from end user, send to CAS login
        cas_login_url = cas_client.get_login_url()
        current_app.logger.debug('CAS login URL: %s', cas_login_url)
        return redirect(cas_login_url)

    # There is a ticket, the request come from CAS as callback.
    # need call `verify_ticket()` to validate ticket and get user profile.
    current_app.logger.debug('ticket: %s', ticket)
    current_app.logger.debug('next: %s', next)
    #print('on est dans login')

    user, attributes, pgtiou = cas_client.verify_ticket(ticket)
    print(user, attributes, pgtiou)
    current_app.logger.debug(
        'CAS verify ticket response: user: %s, attributes: %s, pgtiou: %s', user, attributes, pgtiou)

    if not user:
        return 'Failed to verify ticket. <a href="/login">Login</a>'
    else:  # Login successfully, redirect according `next` query parameter.
        session['username'] = user
        session['attributes'] = attributes
        return redirect(next)


@admin_blueprint.route('/logout')
def logout():
    redirect_url = url_for('admin.logout_callback', _external=True)
    cas_logout_url = cas_client.get_logout_url(redirect_url)
    current_app.logger.debug('CAS logout URL: %s', cas_logout_url)

    return redirect(cas_logout_url)


@admin_blueprint.route('/logout_callback')
def logout_callback():
    # redirect from CAS logout request after CAS logout successfully
    session.pop('username', None)
    return 'Logged out from CAS. <a href="/admin/login">Login</a>'
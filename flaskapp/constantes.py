# import os

# path_serveur = "/var/www/html/flaskapp/"
# path_local = "/home/fab/Projets/CliMix/flaskapp/"
# if os.path.exists(path_serveur) :
#     dataPath = path_serveur
# else:
#     dataPath = path_local

# print ("Sur le chemin " + dataPath)
# host='mamachine.insa-toulouse.fr'

# CAS_SERVICE_URL='https://mamachine.insa-toulouse.fr:5000/admin/login?next=%2Fadmin%2Fdashboard',
# CAS_SERVER_URL='https://cas.insa-toulouse.fr/cas/'

import os

path_serveur = "/var/www/html/flaskapp/"
path_local = "/mnt/c/Users/ishaa/OneDrive/Bureau/climix/ClimIntervenants/flaskapp/"
if os.path.exists(path_serveur) :
    dataPath = path_serveur
else:
    dataPath = path_local

print ("Sur le chemin " + dataPath)
host='mamachine.insa-toulouse.fr'

CAS_SERVICE_URL='https://mamachine.insa-toulouse.fr:5000/admin/login?next=%2Fadmin%2Fdashboard',
CAS_SERVER_URL='https://cas.insa-toulouse.fr/cas/'

import os
est_local = True

path_serveur = "/var/www/html/flaskapp/"
path_local = "/mnt/c/Users/eleaz/PROJET_Jeu_Sérieux/final/climix/flaskapp/"
path_local = "/home/pacco/climix_test/flaskapp/"

if est_local :
    dataPath = path_local
    host = "10.29.40.9"
    CAS_SERVICE_URL='https://'+host+':5000/admin/login?next=%2Fadmin%2Fcheatboard'
    print("Sur le chemin local " + dataPath)

else:
    dataPath = path_serveur
    host='mamachine.insa-toulouse.fr'
    CAS_SERVICE_URL='https://'+host+':5000/admin/login?next=%2Fadmin%2Fdashboard'
    print("Sur le chemin serveur " + dataPath)

CAS_SERVER_URL='https://cas.insa-toulouse.fr/cas/'
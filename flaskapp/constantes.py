import os

path_serveur = "/var/www/html/flaskapp/"
path_local = ""
if os.path.exists(path_serveur) :
    dataPath = path_serveur
else:
    dataPath = path_local

print ("Sur le chemin " + dataPath)

import sys, os

import shutil, json


ce_chemin = os.path.dirname(os.path.abspath(__file__))
dataPath = ce_chemin+"../flaskapp/"
jeu_de_test_rep = ce_chemin + "/jeux_de_test"

class Cas :
    def __init__(self,rep_test):
        self.tests_rep = jeu_de_test_rep+"/"+rep_test    
    
    def __iter__(self):

        for root,dirs,files in os.walk(self.tests_rep, topdown=False) :
       
            if ("inputs.json" in files) and ("voulus.json" in files):
                with open(root+'/inputs.json', 'r') as inputs_file:
                    inputsGlobal = json.load(inputs_file)
                with open(root+'/voulus.json', 'r') as voulu_file:
                    voulusGlobal = json.load(voulu_file)
                for annee, entree in inputsGlobal.items():
                    if annee in voulusGlobal:
                        yield(root, annee,entree,voulusGlobal[annee])
    
    def resultats_vers_voulus(self):
        for root,dirs,files in os.walk(self.tests_rep, topdown=False) :
       
            if ("resultats.json" in files) and not ("voulus.json" in files):
                os.system('cp "%s/resultats.json" "%s/voulus.json"'%(root,root))
        
def lister_les_cas():
    for rep, annee, entree, voulu in Cas(""):
        print("%s -> %s" % (rep,annee))
 


def importer_test(source, cible):
    shutil.copy2(source+"/inputs.json", cible+"/inputs.json")
    shutil.copy2(source+"/resultats.json", cible+"/voulus.json")

def importer_partie(source,cible,user="user", host="srv-geitp", port=2222, root="/var/www/html/flaskapp"):
    commande = 'scp -r -P%d "%s@%s:%s" "%s"' % (port, user, host, source+"/*", cible+"/")
    print(commande)
    print("Mot de passe egats en verland")
    os.system(commande)

def print_usage():
    print("Usage : \n >python joueur.py importeam A 1 test_alea_machin 2")
    print("Usage : \n >python joueur.py liste")

def parse_groupe_team(argv):
    group = argv[2]
    if group not in ["A", "B", "C", "D"]:
        raise ValueError(group + " n' est pas un groupe")

    team = argv[3]
    if team not in ["1", "2", "3", "4"]:
        raise ValueError(team + " n' est pas une équipe")
    
    rep = dataPath + "game_data/" + group + "/" + team
    if os.path.isdir(rep):
        print("Importe le "+ rep +" comme test")
    else:
        raise ValueError(rep + " n' est pas un répertoire !")

    return group, team, rep


def assert_force_pour_rep(cible, argv):
    try:
        if "--force" in argv:
            print("On va écraser " + cible)
            os.makedirs(cible,exist_ok=True)
        else:
            os.makedirs(cible)
            print("Création de %s " % cible)
    except FileExistsError:
        
        raise ValueError("Le répertoire %s existe déjà !\n  >  %s  --force \n ... pour obliger à écraser" % (cible,argv))
    

if __name__=="__main__":
    if len(sys.argv)==1:
        sys.argv.append("help")

    if "importeam" in sys.argv[1]:
        print("Création de cas de test:")
        if len(sys.argv) < 4:
            print_usage()
            raise ValueError("Mauvais nombre d'arguments")

        group, team, source = parse_groupe_team(sys.argv)
        
        cible = jeu_de_test_rep
        if os.path.isdir(cible):
            pass
        else:
            raise ValueError(cible + " n' est pas un répertoire !")
        
        for rep in sys.argv[4:]:
            if "--" in rep:
                break
            cible = cible + "/" + rep 
        
        assert_force_pour_rep(cible, sys.argv)

        importer_test(source, cible)
            
    elif "liste" in sys.argv[1]:
        print("Liste des cas de tests:")
        lister_les_cas()

    elif "teleteam" in sys.argv[1]:
        print("Téléchargement d'une équipe d'un groupe")
        if len(sys.argv) > 3:
            group, team, source = parse_groupe_team(sys.argv)
        
            if len(sys.argv) > 5:
                group, team, cible = parse_groupe_team(sys.argv.pop([2,3]))
            else :
                cible = source
            assert_force_pour_rep(cible, sys.argv) 
            importer_partie(source,cible)

        else:
            print ("indiquez un groupe et equipe \n    >python joueur.py teleteam A 1\n par exemple") 

    elif "telepath" in sys.argv[1]:
        print("Téléchargement d'un répertoire entier")
        if len(sys.argv) > 3:
            source = sys.argv[2]
            cible = sys.argv[3]
            assert_force_pour_rep(cible, sys.argv) 
            importer_partie(source,cible)

        else:
            print ("indiquez un chemin source et cible \n    >python joueur.py telepath /var/www/html/flaskapp/game_data/ /var/www/html/flaskapp/game_data/sauv_15_nov\n par exemple") 

    elif "import" in sys.argv[1]:

        print("import d'un répertoire de tests entier")
        if len(sys.argv) > 3:
            source = dataPath + "game_data/" + sys.argv[2]
            if os.path.isdir(source):
                print("Importe le "+ source +" comme test")
            else:
                raise ValueError(source + " n' est pas un répertoire !")
            cible = jeu_de_test_rep+"/"+sys.argv[3]
            assert_force_pour_rep(cible, sys.argv) 
            commande = 'cp -r "%s"/* "%s"'%(source,cible)
            print(commande)
            os.system(commande)
            Cas(sys.argv[3]).resultats_vers_voulus()

        else:
            print ("indiquez un chemin source et cible \n    >python joueur.py telepath /var/www/html/flaskapp/game_data/ /var/www/html/flaskapp/game_data/sauv_15_nov\n par exemple") 

    else :
        print("Commande non reconnue :")
        print_usage()
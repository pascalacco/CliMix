import unittest
import os, sys

import json 



from flaskapp import strat_stockage
from flaskapp import constantes

from tests  import joueur


class TestStratStockage(unittest.TestCase):
    group=("test")
    team=666
 
    def test_inactif(self):
        for rep, annee, entree, voulu in joueur.Cas("inactif") :
            print("%s -> %d" % (rep,annee))
            sortie = strat_stockage.strat_stockage_main(**entree, group=self.group, team=self.team)
            self.assertAlmostEqual(sortie,voulu) 

    def test_15_nov(self):
        for rep, annee, entree, voulu in joueur.Cas("15_nov") :
            print("%s -> %d" % (rep,annee))
            sortie = strat_stockage.strat_stockage_main(**entree, group=self.group, team=self.team)
            self.assertAlmostEqual(sortie,voulu) 

if __name__ == "__main__":
    #testeur = TestStratStockage()
    #testeur.test_inactif()
    unittest.main()
    
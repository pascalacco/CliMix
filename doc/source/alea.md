# Liste des effets des cartes évenements :

Tous les effets des cartes d'évenements aléatoires sont indiqués dans le fichier  **strat_stockage.py**. Elles sont balisées  par le mot-clé **aléa** et par les codes donnés ci-dessous.

Il y a 7  cartes évenements. Chaque carte comporte 3 évenements possible qui auront un impact sur la partie.

Contrairement aux cartes politiques, les joueurs ne choisissent pas les effets sur la carte.

A la place, un joueur lance un dé et selon le résultat (1, 2 ou 3), le $1^{er}$ effet est appliqué, ou bien les 2 premiers , ou bien les 3 effets.

## Carte évenement "Géopolitique chamboulée" MEGC
**1-** le prix de l'electricite produite à partir du gaz/charbon augmente de 50%.

**2-** les stock d'Uranium baisse de 10 unités.

**3-** le prix de l'electricite produite à partir du nucléaire augmente de 40%.

## Carte évenement "Mix des aléas" MEMDA
**1-** Le budget pour ce tour augmente de 3.11625 Md d'euros. (soit 3 116 250 000 €)

**2-** Les coût pour ce tour augmentent de 1.445 Md d'euros.

**3-** La consommation d'éléctricité heure par heure diminue de 5% pour ce tour.

## Carte évenement "Vers un avenir plus vert" MEVUAPV

**1-** le stock de bois baisse de 10 unités à chaque tour à partir de ce tour-ci.

**2-** la production d'électricité des panneaux solaires augmente de 15% jusqu'à la fin du jeu.

**3-** le budget pour ce tour baisse de 10 Md.

## Carte évenement "Géographie des territoires" MEGDT
**1-** Il faut remplacer 1/3 des panneaux solaires de la région PACA.
Les dépenses ce tour augmentent de $3.6*\frac{1}{3}*nbrPanneauSolaire_{PACA}$.

**2-** la capacité maximale d’implémentation d'éoliennes offshore des régions PACA et NA est augmentée de 1 pour le reste de la partie.

**3-** Les dépenses pour ce tour augmentent pour remplacer toutes les éoliennes offshore de la région Pays de la Loire (pll)

$dépenses = dépenses + 6*nbreolienneOFF_{pll}$

*note: "remplacer" signifie dépenser pour en acheter une nouvelle*
## Carte évenement "La météo fait des caprices" MEMFDC
**1-** les éoliennes du Centre Val de Loire ne marchent plus pendant 6 mois(on ne précise pas lesquels), soit 1/10 de ce tour. Pas de coût de réparation contrairement à ce que dit la carte.

$prodeolienneON_{CVL} = prodeolienneON_{CVL}*0.9$

**2-** 1 an sans production de biomasse pour la Nouvelle-Aquitaine *(pas sûr, à tester)*.

$gazBiomasse_{NA} = gazBiomasse_{NA}*\frac{5}{6}$

**3-** arrêt de la production des centrales nucléaires pour 15 mois pour ce tour(juin juillet août de chaque année).
$prodNuc = prodNuc *0.75$ sur le tour

*note: je ne suis pas sûr de l'implementation exacte de ces arrêts, le modèle est censé être en heure par heure mais je ne sais pas si ces arrêts sont pris en compte à ces périodes-là ou si on fait une moyenne par tour de la prod.*

## Carte évenement "Crise Sociale" MECS
**1-** Le maximum d'éolienne onshore par territoire est réduit de 60%. Si le nouveau seuil est inférieur au nombre d'éoliennes actuel, il n'est pas nécessaire de les enlever mais on ne peut pas en rajouter.

**2-** La capacité d'éoliennes Onshore et de panneaux solaires en Occitanie double.

**3-** Impossible de rajouter des centrales nucléaires pour ce tour.(possibilité de conserver celle qui peuvent être maintenues)

*notes: le point MECS3 est balisé dans le fichier*  **flaskapp.py** 
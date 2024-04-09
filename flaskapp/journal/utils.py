import random
import json
import numpy as np


def create_roles(names,path):
    roles = [
        "Élu local et député",
        "PDG Éoliennes",
        "PDG Photovoltaïque",
        "Leader de green peace",
        "Leader des agriculteurs",
        "Ministre de la transition écologique et des solidarités",
        "activiste"
    ]
    random.shuffle(roles)
    random.shuffle(names)

    result = {names[0]: "Première ministre", names[1]: "Opposition"}

    for name in names[2:]:
        role = roles.pop()
        result[name] = role
    rounds = 5
    elu_ministre= "Ministre de la transition écologique et des solidarités" in list(result.values()) and "Élu local et député" in list(result.values())
    for key in list(result.keys()):
        role=[result[key]]
        if elu_ministre:
            for round in range(rounds-1):
                if role[round]=="Première ministre":
                    role.append("Opposition")
                elif role[round]=="Opposition":
                    role.append("Première ministre")
                elif role[round]=="Ministre de la transition écologique et des solidarités":
                    role.append("Élu local et député")
                elif role[round]=="Élu local et député":
                    role.append("Ministre de la transition écologique et des solidarités")
                else:
                    role.append(role[round])
        else :
            for round in range(rounds-1):
                if role[round]=="Première ministre":
                    role.append("Opposition")
                elif role[round]=="Opposition":
                    role.append("Première ministre")
                else:
                    role.append(role[round])
        result[key]=role

    with open(path, 'w') as json_file:
        json.dump(result, json_file)

def code_to_region(code):
    if code=="hdf":
        return "Hauts de France"
    elif code=="bre":
        return "Bretagne"
    elif code=="nor":
        return "Normandie"
    elif code=="idf":
        return "Île de France"
    elif code=="est":
        return "Grand Est"
    elif code=="cvl":
        return "Centre Val de Loire"
    elif code=="pll":
        return "Pays de la Loire"
    elif code=="bfc":
        return "Bourgogne Franche Comté"
    elif code=="naq":
        return "Nouvelle Aquitaine"
    elif code=="ara":
        return "Auvergne Rhône Alpes"
    elif code=="occ":
        return "Occitanie"
    elif code=="cor":
        return "Corse"

def set_scores_dict(path_to_scores,mean=20,var=4):
    scores_dict={
        "Première ministre":
            {
                "Sécurisation de l’approvisionnement en métaux critiques":[np.random.normal(mean,var),(None,None,None,None)],
                "Sécurisation de l’approvisionnement en uranium":[np.random.normal(mean,var),(None,None,None,None)],
                "L’énergie Eolienne est un atout pour la France":[np.random.normal(mean,var),(None,None,None,None)],
                "L’énergie solaire est un atout pour la France":[np.random.normal(mean,var),(None,None,None,None)],
                "L’énergie nucléaire est un atout pour la France":[np.random.normal(mean,var),(None,None,None,None)]
        },
        "Élu local et député":
            {
                "des pertes d’emplois liées à la suppression centrale nucléaire":[np.random.normal(mean,var),(None,None,None,None)],
                "du trop grand nombre de panneaux photovoltaïque dénaturant les paysages et entravant les cultures":[np.random.normal(mean,var),(None,None,None,None)],
                "du trop grand nombre d’éoliennes dénaturant les paysages et entravant les cultures":[np.random.normal(mean,var),(None,None,None,None)],
                "du déficit d’électricité prévu pour la région":[np.random.normal(mean,var),""],
                "des parc éoliens offshore qui sont une menace pour l’économie de la mer, pêche et tourisme":[np.random.normal(mean,var),(None,None,None,None)],
                "de la transition, devant s’accompagner selon lui d’investissements dans l’offre de transport en milieu rural":[np.random.normal(mean,var),(None,None,None,None)],
                "de la relocalisation de l’industrie, indispensable à la réduction de notre empreinte carbone, qui doit être accompagnée par l’état (donner un exemple) ":[np.random.normal(mean,var),(None,None,None,None)],
                "de l'initiative citoyenne pour mettre en place des circuits courts pour l’alimentation (donner un exemple) ":[np.random.normal(mean,var),(None,None,None,None)],
                "du tarif progressif proposé au gouvernement pour l’électricité pour permettre aux plus pauvres de répondre aux besoins vitaux ":[np.random.normal(mean,var),(None,None,None,None)],
                "de la favorisation de l’habitat semi-collectif pour mutualiser au mieux les dépenses énergétiques des foyers français, proposé récemment au gouvernement ":[np.random.normal(mean,var),(None,None,None,None)]
        },
        "PDG Photovoltaïque":
            {
                "du manque d’installation de panneaux photovoltaïques ces dernières années. ":[np.random.normal(mean,var),(None,None,None,None)],
                "de l'essor du photovoltaïque qui est une aubaine pour la France. ":[np.random.normal(mean,var),(None,None,None,None)],
                "de la difficulté de trouver de la main d’oeuvre qualifiée, malgré le fait que le secteur soit considéré comme porteur. ":[np.random.normal(mean,var),(None,None,None,None)],
                "de l'importance fondamentale d’investir dans la recherche sur les nouvelles technologies de panneaux solaires. ":[np.random.normal(mean,var),(None,None,None,None)],
                "de l'importance de développer le stockage d’électricité pour valoriser les nouvelles ENR. ":[np.random.normal(mean,var),(None,None,None,None)],
                "de la nécessité de densifier le réseau électrique pour mieux accueillir l’électricité produite pas les panneaux photovoltaïques. ":[np.random.normal(mean,var),(None,None,None,None)],
                "de l'importance de modifier la législation pour permettre plus d’installations de parc électriques. ":[np.random.normal(mean,var),(None,None,None,None)],
                "de la concurrence déloyale des producteurs de panneaux photovoltaïques asiatiques (donner un exemple de nom d'entreprise). ":[np.random.normal(mean,var),(None,None,None,None)],
                "de la nécessité de modifier la législation pour permettre à plus de français d’installer des panneaux voltaïques sur leurs toits même en zones classées. ":[np.random.normal(mean,var),(None,None,None,None)],
                "de la valorisation des autres usages des panneaux photovoltaïques, comme l’ombrage des cultures. ":[np.random.normal(mean,var),(None,None,None,None)]
        },
        "PDG Éoliennes":
            {
                "du manque d’installation d’éoliennes ces dernières années":[np.random.normal(mean,var),(None,None,None,None)],
                "de l’essor de l’éolien qui est une chance pour la France. Il se félicite des choix du gouvernement. ":[np.random.normal(mean,var),(None,None,None,None)],
                "de la difficulté à trouver de la main d’oeuvre qualifiées. ":[np.random.normal(mean,var),(None,None,None,None)],
                "de la tension actuelle sur les métaux rares, et rappelle l'importance cruciale de sécuriser les approvisionnements. ":[np.random.normal(mean,var),(None,None,None,None)],
                "de la tension sur le cuivre et l’acier, et rappelle l'importance cruciale de sécuriser les approvisionnements. ":[np.random.normal(mean,var),(None,None,None,None)],
                "de la nécessité de décarboner la fabrication du béton pour limiter l’impact CO2 de l’éolien. ":[np.random.normal(mean,var),(None,None,None,None)],
                "de l'importance de flexibiliser la demande d’électricité pour valoriser les nouvelles ENR":[np.random.normal(mean,var),(None,None,None,None)],
                "de la recherche sur le recyclage des pâles d’éoliennes, avançant à grand pas depuis quelques années. ":[np.random.normal(mean,var),(None,None,None,None)],
                "de la nécessité de développer l’éolien flottant, qui permettrait d'exploiter notre cote. ":[np.random.normal(mean,var),(None,None,None,None)],
                "de la nécessité de promouvoir l’énergie éolienne et lutter contre les a priori sur celle ci. Cela passe entre autres par de la sensibilisation sur le recyclage. ":[np.random.normal(mean,var),(None,None,None,None)]
        },
        "Leader de green peace":
            {
                "de l'augmentation du nombre de réacteurs nucléaires, et des risques géopolitiques sur l’approvisionnement en matières premières associés.":[np.random.normal(mean,var),(None,None,None,None)],
                "des émissions de CO2 trop importantes":[np.random.normal(mean,var),(None,None,None,None)],
                "des risques Gestion des déchets nucléaires":[np.random.normal(mean,var),(None,None,None,None)],
                "du risque d’accidents sur les centrales nucléaires":[np.random.normal(mean,var),(None,None,None,None)],
                "des installations massives d'éoliennes impactant durement la biodiversité":[np.random.normal(mean,var),(None,None,None,None)],
                "des installations massives de panneaux photovoltaïques impactant durement la biodiversité":[np.random.normal(mean,var),(None,None,None,None)],
                "du fait que la sobriété est la seule solution":[np.random.normal(mean,var),(None,None,None,None)],
                "du fait que la réflexion sur le mix électrique ne doit pas faire oublier que nous faisons face à une crise écologique plus large avec le dépassement de plusieurs limites planétaires":[np.random.normal(mean,var),(None,None,None,None)],
                "du fait que le financement de la transition doit se faire en taxant les entreprises qui polluent et mettent du CO2":[np.random.normal(mean,var),(None,None,None,None)],
                "de l'utilisation de la voiture en milieu urbain qui devrait être proscrit":[np.random.normal(mean,var),(None,None,None,None)]
        },
        "Leader des agriculteurs":
            {
                "de la concurrence des sols avec les Panneaux photovoltaïques":[np.random.normal(mean,var),(None,None,None,None)],
                "de la concurrence des sols avec les Eoliennes":[np.random.normal(mean,var),(None,None,None,None)],
                "de l'adaptation au changement de régime alimentaire des français qui consomment moins de viande":[np.random.normal(mean,var),(None,None,None,None)],
                "de l'adaptation au dérèglement climatique, donner des exemples":[np.random.normal(mean,var),(None,None,None,None)],
                "de la sécheresses amplifiées par le dérèglement climatique":[np.random.normal(mean,var),(None,None,None,None)],
                "de la pénurie de main d’oeuvre agricole":[np.random.normal(mean,var),(None,None,None,None)],
                "de la difficulté de l'électrification des véhicules agricoles":[np.random.normal(mean,var),(None,None,None,None)],
                "de la méthanisation de la biomasse réduit son utilisation pour l’agriculture":[np.random.normal(mean,var),(None,None,None,None)],
                "de la difficulté de s’approvisionner en engrais azotés avec la baisse drastique des importations de gaz et de pétroles":[np.random.normal(mean,var),(None,None,None,None)],
                "de la difficulté à répercuter sur les prix, la hausse des couts de l’énergie":[np.random.normal(mean,var),(None,None,None,None)]
        },
        "Ministre de la transition écologique et des solidarités":
            {
                "du gouvernement faisant tout son possible pour limiter les jours de pénuries d’électricité":[np.random.normal(mean,var),(None,None,None,None)],
                "de l'équilibre géographique du réseau":[np.random.normal(mean,var),(None,None,None,None)],
                "du renforcement des échanges européens d’électricité":[np.random.normal(mean,var),(None,None,None,None)],
                "de la promotion des éco gestes":[np.random.normal(mean,var),(None,None,None,None)],
                "de l’isolation des bâtiments qui est une priorité du gouvernement":[np.random.normal(mean,var),(None,None,None,None)],
                "de la réflexion sur la construction de nouvelles mines de Lithium en France pour alimenter la transition écologique":[np.random.normal(mean,var),(None,None,None,None)],
                "du lancement d’un plan de formation aux métiers de l’énergie":[np.random.normal(mean,var),(None,None,None,None)],
                "du lancement d’un grand plan vélo en ville pour sortir à terme les voitures des centres ville":[np.random.normal(mean,var),(None,None,None,None)],
                "du gouvernement qui se montre attentif aux coûts des énergies, mais ajoute toutefois que ceux ci vont monter inexorablement":[np.random.normal(mean,var),(None,None,None,None)],
                "de l'importance de la réindustrialisation du pays pour limiter l’empreinte écologique des français":[np.random.normal(mean,var),(None,None,None,None)]
        },
        "activiste":
            {
                "Le maintient des centrales nucléaires est un frein à une indispensable sobriété":[np.random.normal(mean,var),(None,None,None,None)],
                "La construction d’un nouveau tunnel ferroviaire détruit le milieu naturel d’espèces sauvages":[np.random.normal(mean,var),(None,None,None,None)],
                "La construction de méga bassines est inadaptée au dérèglement climatique et soutient une agriculture productiviste":[np.random.normal(mean,var),(None,None,None,None)],
                "Les barrages sur des rivières sont des catastrophes pour la biodiversité":[np.random.normal(mean,var),(None,None,None,None)],
                "Les publicités induisent de la surconsommation":[np.random.normal(mean,var),(None,None,None,None)],
                "Le technosolutionisme est un mirage":[np.random.normal(mean,var),(None,None,None,None)],
                "L’impact de l’éolien en mer sur la faune marine est dramatiquement sous-évalué (donner un exemple)":[np.random.normal(mean,var),(None,None,None,None)],
                "Le greenwashing est un danger pour la transition (donner deux exemples)":[np.random.normal(mean,var),(None,None,None,None)]
        },
        "Opposition":
            {
                "Réduction des émissions de CO2 insuffisantes, donner des chiffres":[np.random.normal(mean,var),(None,None,None,None)],
                "Cout en métaux des nouvelles ENR, déficit budgétaire donner des chiffres":[np.random.normal(mean,var),(None,None,None,None)],
                "Cout en uranium, dépendance vis à vis des fournisseurs étrangers":[np.random.normal(mean,var),(None,None,None,None)],
                "Trop d’éoliennes induisent un risque sur la stabilité du réseau électrique, donner des chiffres":[np.random.normal(mean,var),(None,None,None,None)],
                "Trop de panneaux solaires induisent un risque sur la stabilité du réseau électrique, donner des chiffes":[np.random.normal(mean,var),(None,None,None,None)],
                "Jours de pénuries trop importants donner des chiffres":[np.random.normal(mean,var),(None,None,None,None)],
                "Manque de formation aux métiers liés à la transition, donner des exemples":[np.random.normal(mean,var),(None,None,None,None)],
                "Manque d’anticipation dans l’aménagement du réseau électrique pour s’adapter aux nouvelles ENR":[np.random.normal(mean,var),(None,None,None,None)],
                "Manque d’investissement dans les transports collectifs":[np.random.normal(mean,var),(None,None,None,None)],
                "Manque de coordination à l’échelle européenne des politiques de production de stockage et d’échanges d’électricité":[np.random.normal(mean,var),(None,None,None,None)]
        }
    }
    with open(path_to_scores, 'w') as json_file:
        json.dump(scores_dict, json_file)

def update_scores_fn(path_to_scores,path_to_results,path_to_aggregated_mix,current_round):
    """
        TODO : au moment de calculer certaines métriques, on va également trouver des régions (ex: région où le plus de PV ont étés installés). Il faudra save ces strings dans un pickle pour pouvoir les ressortir au moment du prompt, si le thème choisi fait appel à cette info. => on va devoir une fonction de prompting léchée.

        IMPORTANT : à chaque ajout de thème à score, reprendre la partie sur l'update des scores car tous les indices ont changé.
        bon à savoir : certaines quantités ne sont calculées qu'à partir du second tour (current round>0) car le premier mix dont on dispose est en 2030, à tort selon moi.
    """
    with open(path_to_results, 'r') as json_file:
        results = json.load(json_file)
    with open(path_to_scores, 'r') as json_file:
        scores = json.load(json_file)
    with open(path_to_aggregated_mix, 'r') as json_file:
        mix = json.load(json_file)
    years_results=list(results.keys())
    current_results=results[years_results[current_round]]
    mix_years=list(mix.keys())

    def lieu_max_panneaux(current,past):
        """
            va sortir le lieu pour lequel le delta en panneaux ajoutés est le plus grand, ainsi que ce delta. 
            TODO : calculer un delta total pour la quantité globale ajoutée
        """
        lieu_plus_gd_delta = None
        delta_max = 0
        delta_total=0
        for key in list(current.keys())[6:]: 
            delta = int(current[key]["panneauPV"]) - int(past[key]["panneauPV"])
            if delta>delta_max:
                lieu_plus_gd_delta = key
                delta_max=delta
            delta_total+=delta
        return lieu_plus_gd_delta,delta_max,delta_total
    lieu_panneaux,delta_panneaux,total_panneaux=lieu_max_panneaux(current=mix[mix_years[current_round+1]],past=mix[mix_years[current_round]])

    def lieu_max_eolien_on(current,past):
        """
            va sortir le lieu pour lequel le delta en parcs éoliens ajoutés est le plus grand, ainsi que ce delta.
        """
        lieu_plus_gd_delta = None
        delta_max = 0
        delta_total=0
        for key in list(current.keys())[6:]:
            delta = int(current[key]["eolienneON"]) - int(past[key]["eolienneON"])
            if delta>delta_max:
                lieu_plus_gd_delta = key
                delta_max=delta
            delta_total+=delta
        return lieu_plus_gd_delta,delta_max,delta_total
    lieu_eo_on,delta_eo_on,total_eo_on=lieu_max_eolien_on(current=mix[mix_years[current_round+1]],past=mix[mix_years[current_round]])

    def lieu_max_eolien_off(current,past):
        """
            va sortir le lieu pour lequel le delta en parcs éoliens ajoutés est le plus grand, ainsi que ce delta
        """
        lieu_plus_gd_delta = None
        delta_max = 0
        delta_total=0
        for key in list(current.keys())[6:]: 
            delta = int(current[key]["eolienneOFF"]) - int(past[key]["eolienneOFF"])
            if delta>delta_max:
                lieu_plus_gd_delta = key
                delta_max=delta
            delta_total+=delta
        return lieu_plus_gd_delta,delta_max,delta_total
    lieu_eo_off,delta_eo_off,total_eo_off=lieu_max_eolien_off(current=mix[mix_years[current_round+1]],past=mix[mix_years[current_round]])

    def lieu_max_methanation(current,past):
        """
            va sortir le lieu pour lequel le delta en méthaniseurs ajoutés est le plus grand, ainsi que ce delta
        """
        lieu_plus_gd_delta = None
        delta_max = 0
        delta_total=0
        for key in list(current.keys())[6:]: 
            delta = int(current[key]["methanation"]) - int(past[key]["methanation"])
            if delta>delta_max:
                lieu_plus_gd_delta = key
                delta_max=delta
            delta_total+=delta
        return lieu_plus_gd_delta,delta_max,delta_total
    lieu_methanation,delta_methanation,total_methanation=lieu_max_methanation(current=mix[mix_years[current_round+1]],past=mix[mix_years[current_round]])

    def centrales_fermees_reconduites(current,past):
        """
            Sort le nombre de centrales fermées/reconduites. Ainsi que le lieu où il y a eu le plus de fermetures, et ainsi que ce max.
        """
        lieu_max_fermetures = None
        fermetures_max = 0
        fermetures_total=0
        reconduites_total=0
        for key in list(current.keys())[6:]: 
            fermetures = int(current[key]["centraleNuc"]) - int(past[key]["centraleNuc"])
            reconduites_total+=int(current[key]["centraleNuc"])
            if fermetures>fermetures_max:
                lieu_max_fermetures = key
                fermetures_max=fermetures
            fermetures_total+=fermetures
        return lieu_max_fermetures,fermetures_max,fermetures_total,reconduites_total
    lieu_max_fermetures,max_fermetures,total_fermetures,total_reconduites=centrales_fermees_reconduites(current=mix[mix_years[current_round+1]],past=mix[mix_years[current_round]])


    def lieux_max_epr2(current,past):
        """
            va sortir le lieu pour lequel il y a le plus de nouveaux epr installés, ainsi que cette quantité et la quantité totale. En théorie on ne peut pas désinstaller d'epr
        """
        lieu_plus_gd_delta = None
        delta_max = 0
        delta_total=0
        for key in list(current.keys())[6:]: 
            delta = int(current[key]["EPR2"]) - int(past[key]["EPR2"])
            if abs(delta) > abs(delta_max):
                lieu_plus_gd_delta = key
                delta_max=delta
            delta_total+=delta
        return lieu_plus_gd_delta,delta_max,delta_total
    lieu_epr,delta_epr,total_epr=lieux_max_epr2(current=mix[mix_years[current_round+1]],past=mix[mix_years[current_round]])

    if delta_eo_off>delta_eo_on:
        lieu_eo=lieu_max_eolien_off
    else :
        lieu_eo=lieu_max_eolien_on
    nb_penuries=current_results["nbPenuries"]
    ################################
    #         Élu local            #
    ################################
    keys=list(scores["Élu local et député"].keys())
    scores["Élu local et député"][keys[1]][0]=scores["Élu local et député"][keys[1]][0]+0.1*delta_panneaux
    scores["Élu local et député"][keys[1]][1][0]=code_to_region(lieu_panneaux)
    scores["Élu local et député"][keys[1]][1][1]=delta_panneaux
    if delta_eo_off>delta_eo_on:
        scores["Élu local et député"][keys[2]][0]=scores["Élu local et député"][keys[2]][0]+0.1*(delta_eo_off)
        scores["Élu local et député"][keys[2]][1][0]=code_to_region(lieu_eo_off)
        scores["Élu local et député"][keys[2]][1][1]=delta_eo_off
        scores["Élu local et député"][keys[2]][1][2]="Off"
    else :
        scores["Élu local et député"][keys[2]][0]=scores["Élu local et député"][keys[2]][0]+0.1*(delta_eo_on)
        scores["Élu local et député"][keys[2]][1][0]=code_to_region(lieu_eo_on)
        scores["Élu local et député"][keys[2]][1][1]=delta_eo_on
        scores["Élu local et député"][keys[2]][1][2]="On"
    scores["Élu local et député"][keys[4]][0]=scores["Élu local et député"][keys[4]][0]+0.5*delta_eo_off
    scores["Élu local et député"][keys[4]][1][0]=code_to_region(lieu_eo_off)
    scores["Élu local et député"][keys[4]][1][1]=delta_eo_off
    scores["Élu local et député"][keys[0]][0]=scores["Élu local et député"][keys[0]][0]+0.5*max_fermetures
    scores["Élu local et député"][keys[0]][1][0]=code_to_region(lieu_max_fermetures)
    scores["Élu local et député"][keys[0]][1][1]=max_fermetures
    ###################################
    #     Leader des agriculteurs     #
    ###################################
    keys=list(scores["Leader des agriculteurs"].keys())
    scores["Leader des agriculteurs"][keys[0]][0]=scores["Leader des agriculteurs"][keys[0]][0]+0.1*total_panneaux
    scores["Leader des agriculteurs"][keys[0]][1]="Nombre de parcs solaires occupant le territoire Français : {}. ".format(total_panneaux)
    scores["Leader des agriculteurs"][keys[1]][0]=scores["Leader des agriculteurs"][keys[1]][0]+0.1*total_eo_on
    scores["Leader des agriculteurs"][keys[1]][1]="Total d'éoliennes terrestres ajoutées : {}. ".format(total_eo_on)
    scores["Leader des agriculteurs"][keys[7]][0]=scores["Leader des agriculteurs"][keys[7]][0]+0.2*total_methanation
    scores["Leader des agriculteurs"][keys[7]][1]="Nombre de méthaniseurs installés : {}. ".format(total_methanation)

    ##################################
    #      Leader de Greenpeace      #
    ##################################
    keys=list(scores["Leader de green peace"].keys())
    scores["Leader de green peace"][keys[5]][0]=scores["Leader de green peace"][keys[5]][0]+0.1*total_panneaux
    scores["Leader de green peace"][keys[5]][1][0]=delta_panneaux
    scores["Leader de green peace"][keys[5]][1][1]=code_to_region(lieu_panneaux)
    scores["Leader de green peace"][keys[4]][0]=scores["Leader de green peace"][keys[4]][0]+0.1*(total_eo_off+total_eo_on)
    scores["Leader de green peace"][keys[4]][1][0]=total_eo_off+total_eo_on
    scores["Leader de green peace"][keys[0]][0]=scores["Leader de green peace"][keys[0]][0]+0.2*(total_reconduites+total_epr)
    scores["Leader de green peace"][keys[0]][1][0]=total_reconduites
    scores["Leader de green peace"][keys[0]][1][1]=total_epr
    scores["Leader de green peace"][keys[2]][0]=scores["Leader de green peace"][keys[2]][0]+0.3*(total_reconduites+total_epr)
    scores["Leader de green peace"][keys[2]][1][0]=total_reconduites
    scores["Leader de green peace"][keys[2]][1][1]=total_epr
    scores["Leader de green peace"][keys[3]][0]=scores["Leader de green peace"][keys[3]][0]+0.1*(total_reconduites+total_epr)
    scores["Leader de green peace"][keys[3]][1][0]=total_reconduites
    scores["Leader de green peace"][keys[3]][1][1]=total_epr

    ##################################
    #      PDG Photovoltaïque       #
    ##################################
    keys=list(scores["PDG Photovoltaïque"].keys())
    if total_panneaux<=3:
        scores["PDG Photovoltaïque"][keys[0]][0]=scores["PDG Photovoltaïque"][keys[0]][0]+3
        scores["PDG Photovoltaïque"][keys[0]][1][0]=total_panneaux
        scores["PDG Photovoltaïque"][keys[0]][1][1]=code_to_region(lieu_panneaux)
    else:
        scores["PDG Photovoltaïque"][keys[1]][0]=scores["PDG Photovoltaïque"][keys[1]][0]+3
        scores["PDG Photovoltaïque"][keys[1]][1][0]=total_panneaux
        scores["PDG Photovoltaïque"][keys[1]][1][1]=code_to_region(lieu_panneaux)
    scores["PDG Photovoltaïque"][keys[2]][0]=scores["PDG Photovoltaïque"][keys[2]][0]+0.2*(total_eo_off+total_eo_on)
    scores["PDG Photovoltaïque"][keys[2]][1][0]=total_eo_off+total_eo_on
    scores["PDG Photovoltaïque"][keys[2]][1][1]=code_to_region(lieu_panneaux)

    ################################
    #         Opposition           #
    ################################
    keys=list(scores["Opposition"].keys())
    scores["Opposition"][keys[3]][0]=scores["Opposition"][keys[3]][0]+0.2*(total_eo_off+total_eo_on)
    scores["Opposition"][keys[3]][1][0]=total_eo_off+total_eo_on
    scores["Opposition"][keys[1]][0]=scores["Opposition"][keys[1]][0]+0.1*total_panneaux+0.1*(total_eo_off+total_eo_on)
    scores["Opposition"][keys[1]][1][0]=total_panneaux
    scores["Opposition"][keys[1]][1][1]=total_eo_off+total_eo_on
    scores["Opposition"][keys[4]][0]=scores["Opposition"][keys[4]][0]+0.2*total_panneaux
    scores["Opposition"][keys[4]][1][0]=total_panneaux
    scores["Opposition"][keys[2]][0]=scores["Opposition"][keys[2]][0]+0.3*total_reconduites
    scores["Opposition"][keys[2]][1][0]=total_reconduites+total_epr
    scores["Opposition"][keys[5]][0]=scores["Opposition"][keys[5]][0]+0.1*nb_penuries
    scores["Opposition"][keys[5]][1][0]=nb_penuries

    #############################
    #       PDG Éoliennes       #
    #############################
    keys=list(scores["PDG Éoliennes"].keys())
    if (total_eo_off+total_eo_on)<=3:
        scores["PDG Éoliennes"][keys[0]][0]=scores["PDG Éoliennes"][keys[0]][0]+3
        scores["PDG Éoliennes"][keys[0]][1][0]=total_eo_off+total_eo_on
    else :
        scores["PDG Éoliennes"][keys[1]][0]=scores["PDG Éoliennes"][keys[1]][0]+3
        scores["PDG Éoliennes"][keys[1]][1][0]=total_eo_off+total_eo_on
        scores["PDG Éoliennes"][keys[1]][1][1]=code_to_region(lieu_eo)
    scores["PDG Éoliennes"][keys[2]][0]=scores["PDG Éoliennes"][keys[2]][0]+0.2*(total_eo_off+total_eo_on)
    scores["PDG Éoliennes"][keys[2]][1][0]=total_eo_off+total_eo_on
    scores["PDG Éoliennes"][keys[3]][0]=scores["PDG Éoliennes"][keys[3]][0]+1*total_eo_off
    scores["PDG Éoliennes"][keys[3]][1][0]=total_eo_off+total_eo_on
    scores["PDG Éoliennes"][keys[4]][0]=scores["PDG Éoliennes"][keys[4]][0]+0.2*(total_eo_off+total_eo_on)
    scores["PDG Éoliennes"][keys[4]][1][0]=total_eo_off+total_eo_on
    scores["PDG Éoliennes"][keys[8]][0]=scores["PDG Éoliennes"][keys[8]][0]+0.5*total_eo_off
    scores["PDG Éoliennes"][keys[8]][1][0]=total_eo_off
    scores["PDG Éoliennes"][keys[9]][0]=scores["PDG Éoliennes"][keys[9]][0]+0.2*(total_eo_off+total_eo_on)
    scores["PDG Éoliennes"][keys[9]][1][0]=total_eo_off+total_eo_on

    ################################
    #          Activiste           #
    ################################
    keys=list(scores["activiste"].keys())
    scores["activiste"][keys[6]][0]=scores["activiste"][keys[6]][0]+total_eo_off
    scores["activiste"][keys[6]][1][0]=code_to_region(lieu_eo_off)
    scores["activiste"][keys[6]][1][1]=delta_eo_off
    scores["activiste"][keys[0]][0]=scores["activiste"][keys[0]][0]+0.2*(total_reconduites+total_epr)
    scores["activiste"][keys[0]][1][0]=code_to_region(lieu_epr)
    scores["activiste"][keys[0]][1][1]=delta_epr

    ############################################
    #   Ministre de la transition écologique   #
    #        et des solidarités                #
    ############################################
    keys=list(scores["Ministre de la transition écologique et des solidarités"].keys())
    scores["Ministre de la transition écologique et des solidarités"][keys[0]][0]=scores["Ministre de la transition écologique et des solidarités"][keys[0]][0]+0.1*nb_penuries
    scores["Ministre de la transition écologique et des solidarités"][keys[0]][1][0]=nb_penuries
    scores["Ministre de la transition écologique et des solidarités"][keys[2]][0]=scores["Ministre de la transition écologique et des solidarités"][keys[0]][0]+0.05*nb_penuries
    scores["Ministre de la transition écologique et des solidarités"][keys[0]][1][0]=nb_penuries

    with open(path_to_scores, 'w') as json_file:
        json.dump(scores, json_file)


def set_occasions_dict(path_to_occasions):
    occasions_dict={
        "Première ministre":
            [
                "lors d'une visite d’un chantier de carénage d’une centrale nucléaire  dans une ville que l’on précisera",
                "lors du sommet du G7 dans une capitale mondiale qu’on précisera",
                "lors du lancement de l’assemblée citoyenne pour le climat à Paris",
                "lors des voeux du 1er Janvier à la télévision",
                "lors de la conférence de la COP35 dans une capitale africaine qu’on précisera",
                "lors d'une session de questions live sur Youtube",
                "lors de l’inauguration d’un centre national de recherche sur les nouvelles ENR"
            ]
        ,
        "Élu local et député":
            [
                "lors de l'inauguration d’un centre de recyclage",
                "lors de l'inauguration d’un centre de traitement des eaux usées",
                "lors de la manifestation pour la préservation de l’emploi industriel en France",
                "lors d'une conférence sur l’aménagement du territoire pour la transition écologique",
                "lors d'une manifestation de soutien aux grévistes d’une usine de fabrication de vélos qui doit être délocalisée dans un pays asiatique qu’on précisera",
                "lors de l'inauguration d’un centre de traitement des déchets",
                "lors d'une visite dans une usine de fabrication de vélos électriques"
            ]
        ,
        "PDG Photovoltaïque":
            [
                "lors d'une présentation d’un nouveau type de cellule de silicium pour panneaux au Salon des nouvelles technologies écologiques d’une grande ville allemande qu’on précisera",
                "lors d'une conférence européenne de l’énergie solaire dans une capitale européenne qu’on précisera",
                "lors des journées d’été du MEDEF dans une ville portuaire française qu’on précisera",
                "depuis le chantier d’un parc photovoltaïque",
                "après son entretien avec la commission de l’assemblée nationale sur la souveraineté énergétique",
                "au salon de l’étudiant pour présenter la filière photovoltaïque",
                "lors des rencontres entre académiques et industriels sur l'avenir de l’énergie solaire, organisés dans une université Française que l’on précisera"
            ]
        ,
        "PDG Éoliennes":
            [
                "lors d'une présentation d’un nouveau modèle d’éolienne au salon des technologie vertes dans une grande ville de province qu’on précisera",
                "lors d'une conférence internationale de l’énergie éolienne dans une capitale asiatique qu’on précisera",
                "à l’issue de la rencontre entre les industriels de la transition et du gouvernement",
                "depuis le chantier d’un parc éolien dans une ville d’une région où a été récemment implanté un parc éolien qu’on précisera",
                "au sommet de Davos",
                "lors des rencontres organisées sur l’IA au service des ENR dans un INSA dont on précisera la localisation"
            ]
        ,
        "Leader de green peace":
            [
                "lors d'une manifestation sur le site de prolongement d’une centrale nucléaire que l’on précisera",
                "lors d’un Campus d’été intitulé « sobriété et résilience » dans une sous préfecture rurale qu’on précisera",
                "sur le plateau télé de Léa Salamèche pour présenter son dernier livre dont on donnera le titre",
                "lors d’un sitting organisé pour dénoncer le dépassement des limites planétaires organisé dans une grande ville de province française qu’on précisera",
                "depuis les bords d’une rivière dont on donnera le nom pour tester la radioactivité des eaux rejetées par une centrale nucléaire que l’on précisera",
                "lors d’une manifestation contre le nouveau projet de gazoduc au d’un pays d’asie centrale qu’on spécifiera de l’entreprise LATOT",
                "suite à un débat animé face à un expert du climat dont le prénom est Jean Michel Jancovenividi, promouvant la décroissance et soutenant le nucléaire, organisé par un INSA dont on précisera la localisation"
            ]
        ,
        "Leader des agriculteurs":
            [
                "depuis un salon agricole régional qu’on précisera",
                "lors des rencontre européennes des arboriculteurs dans une capitale européenne qu’on précisera",
                "lors du salon de l’agriculture à Paris",
                "lors d'une manifestation devant une préfecture qu’on précisera pour défendre l’agriculture paysanne",
                "lors d'une manifestation à Strasbourgs devant le parlement pour dénoncer la baisse des subventions aux agriculteurs bio",
                "à l’issue de sa rencontre avec le ministre de l’agriculture"
            ]
        ,
        "Ministre de la transition écologique et des solidarités":
            [
                "à la sortie du conseil des ministres",
                "lors des questions à l’assemblée nationale",
                "lors d'une réunion des ministres européens de la transition énergétique dans une capitale européenne qu’on précisera",
                "lors de la conférence Afrique-Europe pour l’énergie dans une capitale africaine qu’on précisera",
                "lors de la conférence Territoires et Résilience dans une grande ville de province française",
                "lors d'une session FAQ live sur Twitch",
                "lors de l'inauguration du plus grand centre de batterie fixe d’Europe dont on précisera la capacité et l’emplacement",
                "lors des assises de l’aménagement du territoire dans une ville de province qu’on précisera"
            ]
        ,
        "activiste":
            [
                "depuis une ZAD pour préserver une zone humide et empêcher la construction d’un nouvel aéroport dans un lieu qu’on précisera à une cinquantaine de km d’une grande ville française (des stars de la musique françaises nées après 1980 que l’on précisera lui ont rendu visite)",
                "depuis l'arbre auquel il est attaché depuis une semaine, pour empêcher la construction d’une nouvelle autoroute que l’on précisera et préserver une forêt que l’on précisera également",
                "lors d’un action coup de poing et dégonflage de pneus contre les SUV dans une grande ville de province qu’on précisera",
                "depuis une ZAD contre la construction d'un parc éolien pour défendre les oiseaux migrateur sur un nouveau parc éolien qu’on précisera",
                "depuis une ZAD contre la construction d’un parc photovoltaïque qu’on précisera pour préserver l’habitat d’animaux sauvages qu’on précisera"
            ]
        ,
        "Opposition":
            [
                "sur le marché d’une ville de sa circonscription que l’on précisera en tractant pour la campagne électorale",
                "à la sortie du Sénat",
                "sur le plateau télé de Pascal Semipro",
                "sur Tik tok",
                "lors d'une interview radiophonique par Appolin de Malbeu"
            ]
    }
    for k in list(occasions_dict.keys()):
        random.shuffle(occasions_dict[k])
    with open(path_to_occasions, 'w') as json_file:
        json.dump(occasions_dict, json_file)

def update_year(current_round,path_to_title):
    years=["2030","2035","2040","2045","2050"]
    output="Année "+years[current_round]
    with open(path_to_title, 'w') as file:
        file.write(output)
from constantes import *
from archiveur import DataManager
import random
from utils import code_to_region
import numpy as np

def choose_dict_subset(dict):
    keys_to_exclude = ["surplusQuotidien", "penuriesQuotidien", "stockGaz"]
    filtered_dict = {key: dict[key] for key in dict if key not in keys_to_exclude}
    return filtered_dict

def pick_themes_update_scores(scores,role):
    """
        pour un role donné on va choisir les deux thèmes avec les scores les plus hauts et les mettre à 0
    """
    scores_role=scores[role]
    themes_sorted = sorted(scores_role, key=lambda k: scores_role[k][0], reverse=True)
    theme1,theme2 = themes_sorted[:2]

    scores[role][theme1]=0
    scores[role][theme2]=0

    return theme1,theme2

def pick_occasion(occasions,role,round):
    """
        pour un rôle donné, on va choisir l'occasion à laquelle le protagoniste s'exprime.
    """
    return occasions[role][round]

def link_alea_pol_codes(results,round):
    years=list(results.keys())
    current_results=results[years[round]]
    
    #alea
    if current_results["alea"]=="MEGC1": 
        alea="décide de s'allier aux États-Unis dans son désaccord face aux politiques Russes suite au déclenchement de la guerre. L'état a dû faire face à une hausse du gaz et du charbon de 50%"
    elif current_results["alea"]=="MEGC2":
        alea="surveille de près les troubles géopolitiques au Niger impactant nos ressources en Uranium"
    elif current_results["alea"]=="MEGC3":
        alea="subit les limitations d'exportations de matières premières en provenance de Chine suite à son positionnement politique"
    elif current_results["alea"]=="MEMDA1": #mix des aléas
        alea="a décidé de fournir de l'électricité à nos voisins européens, finançant ainsi une partie de notre transition écologique"
    elif current_results["alea"]=="MEMDA2":
        alea="a dû acheter quelques TWh d'électricité à l'Allemagne, se soldant par des dépenses conséquentes"
    elif current_results["alea"]=="MEMDA3":
        alea="s'est félicité des baisses de consommation en électricité des ménages Français, en partie dûe à la douceur de nos derniers hivers"
    elif current_results["alea"]=="MEVUAPV1":
        alea="a constaté une augmentation de la demande d'électricité, probablement dûe à la fin de vente des voitures thermiques actée par l'UE"
    elif current_results["alea"]=="MEVUAPV2":
        alea="s'est réjouit des investissement en R&D photovoltaïque portant enfin leurs fruits"
    elif current_results["alea"]=="MEVUAPV3":
        alea="a rappelé le fait que chaque innovation si impactante soit-elle a son coût"
    elif current_results["alea"]=="MEGDT1":
        alea="a salué le courage des pompiers en région PACA qui ont du faire face sucessivements à incendies et inondations"
    elif current_results["alea"]=="MEGDT2":
        alea="a remarqué que le recul des côtes Française pourrait représenter une opportunité pour l'éolien offshore"
    elif current_results["alea"]=="MEGDT3":
        alea="a déploré les grandes marées survenus récemment en Pays de la Loire, qu'il est jusqu'à qualifier de catastrophe naturelle"
    elif current_results["alea"]=="MEMFDC1":
        alea="a annoncé que les réparations des éoliennes récemment mises hors service par la tempête en région Centre Val de Loire avaient commencé"
    elif current_results["alea"]=="MEMFDC2":
        alea="a fait une brêve référence au épisodes caniculaires survenus l'été dernier endommageant notamment les ecosystèmes ainsi que la prodution de biomasse"
    elif current_results["alea"]=="MEMFDC3":
        alea="déplore les épisodes de sécheresse mettant à mal la production d'énergie nucléaire"
    elif current_results["alea"]=="MECS1":
        alea="prend la peine de légitimer le point de vue des opposants à l'implantation de nouvelles éoliennes, exprimant son accord quant à l'enlaidissement de nos paysages"
    elif current_results["alea"]=="MECS2":
        alea="a annoncé qu'il ferait son maximum pour irriguer les terres agricoles d'Occitanie actuellement en piteux état"
    elif current_results["alea"]=="MECS3":
        alea="a déploré les protocoles de sécurité caduques des centrales nucléaires, nous conduisant à un arrêt dans la construction de nouveaux réacteurs"
    elif current_results["alea"]=="MEMP1":
        alea="promet que les incendies survenus dans certaines régions n'affecteront pas notre productivité, bien qu'on constate une forte baisse des stocks de bois"
    elif current_results["alea"]=="MEMP2":
        alea="affirme être actuellement en recherche d'alternatives pour remplacer les stocks de gaz jusque là fournis par le Niger et le Qatar"
    elif current_results["alea"]=="MEMP3":
        alea="s'avoue mis en difficulté quant aux ressources mondiales en gaz charbon et uranium en pleine diminution, impactant de fait nos propres ressources"
    elif current_results["alea"]=="":
        alea="n'ajoutera rien de plus."
    
    if current_results["politique"]=="CPA1":
        politique=" a décrété que les Français devaient adopter une alimentation végétarienne"
    if current_results["politique"]=="CPA2":
        politique=" a décrété que les Français devaient adopter une alimentation flexitarienne"
    if current_results["politique"]=="CPB1":
        politique=" a choisi de passer 12% du parc des poids lourds à l'électrique"
    if current_results["politique"]=="CPB2":
        politique=" a choisi d'interdire les vols intérieurs"
    if current_results["politique"]=="CPC1":
        politique=" a choisi de rénover les bâtisses en mode bâtiment basse consommation"
    if current_results["politique"]=="CPC2":
        politique=" a choisi d'interdire toute résidence secondaire"
    if current_results["politique"]=="CPD1":
        politique=" a choisi de mettre les innovations technologiques au service des individus"
    if current_results["politique"]=="CPD2":
        politique=" a choisi de promouvoir la réparation et réutilisation des technologies existantes"
    if current_results["politique"]=="CPE1":
        politique=" a choisi d'interdire la vente et utilisation de voitures thermiques"
    if current_results["politique"]=="CPE2":
        politique=" a choisi de passer 67% du parc automobile Français à l'électrique"
    if current_results["politique"]=="CPF1":
        politique=" a choisi de généraliser le télétravail afin de réduire les émissions liées au transport, considérées comme conséquentes"
    if current_results["politique"]=="CPF2":
        politique=" a choisi d'intensifier l'éducation aux eco-gestes,responsabilisant les individus"
    if current_results["politique"]=="":
        politique="a choisi de ne pas remettre en question les habitudes des Français"
    return alea,politique

def get_name_from_roles(roles,round,role):
    for n in list(roles.keys()):
        if roles[n]==role:
            return n

def variable_to_energy(var):
    if var=="eolienneOFF":
        return "ses parcs éolien off shore"
    elif var=="eolienneON":
        return "son parc éolien terrestre"
    elif var=="panneauPV":
        return "son parc panneaux photovoltaïques"
    elif var=="centraleNuc":
        return "ses réacteurs nucléaires nouvellement reconduits"
    elif var=="EPR2":
        return "ses nouveaux réacteurs nucléaires"


def data_ministre_transition(mix):
    while True:
        #choix d'une région au pif 
        regions=["cor","occ","ara","naq","bfc","pll","cvl","est","idf","nor","bre","hdf"]
        region=random.choice(regions)
        for energy_source in ["eolienneOFF","eolienneON","panneauPV","centraleNuc","EPR2"]:
            if mix[region][energy_source]>0:
                return code_to_region(region),variable_to_energy(energy_source)

def data_premier_ministre(results,current_round):
    years_results=list(results.keys())
    if current_round!=0:
        evo_co2=(1-results[years_results[current_round]]["co2"][current_round]/results[years_results[current_round-1]]["co2"][current_round])*100
    else :
        evo_co2=(1-results[years_results[current_round]]["co2"][current_round]/30000000)*100
    co2=results[years_results[current_round]]["co2"][current_round]
    pct_nuc=(results[years_results[current_round]]["prodNucleaire"][years_results[current_round]]/results[years_results[current_round]]["production"])*100
    pct_enr=((results[years_results[current_round]]["prodEau"][years_results[current_round]]+results[years_results[current_round]]["prodOnshore"][years_results[current_round]]+results[years_results[current_round]]["prodOffshore"][years_results[current_round]]+results[years_results[current_round]]["prodPv"][years_results[current_round]]+results[years_results[current_round]]["prodEau"][years_results[current_round]])/results[years_results[current_round]]["production"])*100
    pct_gaz_fossiles=(results[years_results[current_round]]["prodGazFossile"][years_results[current_round]]/results[years_results[current_round]]["production"])*100
    return evo_co2,co2,pct_nuc,pct_enr,pct_gaz_fossiles

def endroit_moins_installations(mix):
    regions=["cor","occ","ara","naq","bfc","pll","cvl","est","idf","nor","bre","hdf"]
    region=""
    install_min=np.inf
    for r in regions:
        nb_install=0
        for i in list(mix[r].keys()):
            nb_install+=mix[r][i]
        if nb_install<install_min:
            install_min=nb_install
            region=r
    return region,install_min

def occupation_sols(mix):
    regions=["cor","occ","ara","naq","bfc","pll","cvl","est","idf","nor","bre","hdf"]
    nb_install=0
    for r in regions:
        nb_install+=mix[r]["eolienneOFF"]+mix[r]["eolienneON"]+mix[r]["centraleNuc"]+mix[r]["panneauPV"]+mix[r]["EPR2"]
    return nb_install

def data_opposition(mix,results,current_round):
    years=list(results.keys())
    pts_faibles=["\"il y a eu un trop grand nombre de jours de pénuries d'énergie ces 5 dernières années, pas moins de",
                 "du réseau s'étant davantage déséqulibré récemment",
                 "de la trop grande occupation des sols par nos infrastructures de production d'énergie",
                 "de notre consommation de métaux, présentant un risque pour l'approvisionnement",
                 "l'énergie coutant trop cher en France, et de la nécessité pour les Français de retrouver leur pouvoir d'achat"]
    pt_faible=random.choice(pts_faibles)
    if pt_faible==pts_faibles[0]:
        complement=" {}!\"".format(results[years[current_round]]["nbPenuries"])
    elif pt_faible==pts_faibles[1]:
        region,install=endroit_moins_installations(mix)
        complement=" région avec le moins d'installations en France : {} - nombre d'installations : {}".format(code_to_region(region),install)
    elif pt_faible==pts_faibles[2]:
        complement=" nombre d'unités sur le territoire : {}".format(occupation_sols(mix))
    elif pt_faible==pts_faibles[3]:
        complement=""
    elif pt_faible==pts_faibles[4]:
        complement=""
    return pt_faible+complement


def get_random_region():
    r=random.randint(0,11)
    regions=["Hauts de France","Bretagne","Normandie","Île de France","Grand Est","Centre Val de Loire","Pays de la Loire","Bourgogne Franche Comté","Nouvelle Aquitaine","Auvergne Rhône Alpes","Occitanie","Corse"]
    return regions[r]

def prompt_gpt_bis(role,dm):
    scores=dm.get_scores()
    occasions=dm.get_occasions()
    current_round=dm.get_round()
    roles=dm.get_roles()
    results=dm.get_results()
    name=get_name_from_roles(roles,current_round,role)
    theme,_=pick_themes_update_scores(scores,role)
    occasion=pick_occasion(occasions,role,current_round)
    mix=dm.get_mix()
    alea,politique=link_alea_pol_codes(results,current_round)
    evo_co2,co2,pct_nuc,pct_enr,pct_gaz_fossiles=data_premier_ministre(results,current_round)
    ##################################
    #       Premier Ministre        #
    ##################################
    if theme=="Sécurisation de l’approvisionnement en métaux critiques":
        prompt="{}, premier ministre, présente dans les grandes lignes les premiers résultats de son plan de transition énergétique {}. Le plan s'appuie sur {}% de nucléaire et {}% d'ENR, ne laissant ainsi que {}% de gaz fossile dans le mix. Cela a permis de faire baisser de {}% l'empreinte carbone de la France sur les 5 dernières années. Par ailleurs, le ministre {}. Aussi, il {}.".format(name,occasion,pct_nuc,pct_enr,pct_gaz_fossiles,evo_co2,politique,alea)
    elif theme=="Sécurisation de l’approvisionnement en uranium":
        prompt="{}, premier ministre, présente dans les grandes lignes les premiers résultats de son plan de transition énergétique {}. Le plan s'appuie sur {}% de nucléaire et {}% d'ENR, ne laissant ainsi que {}% de gaz fossile dans le mix. Cela a permis de faire baisser de {}% l'empreinte carbone de la France sur les 5 dernières années. Par ailleurs, le ministre {}. Aussi, il {}.".format(name,occasion,pct_nuc,pct_enr,pct_gaz_fossiles,evo_co2,politique,alea)
    elif theme=="L’énergie Eolienne est un atout pour la France":
        prompt="{}, premier ministre, présente dans les grandes lignes les premiers résultats de son plan de transition énergétique {}. Le plan s'appuie sur {}% de nucléaire et {}% d'ENR, ne laissant ainsi que {}% de gaz fossile dans le mix. Cela a permis de faire baisser de {}% l'empreinte carbone de la France sur les 5 dernières années. Par ailleurs, le ministre {}. Aussi, il {}.".format(name,occasion,pct_nuc,pct_enr,pct_gaz_fossiles,evo_co2,politique,alea)
    elif theme=="L’énergie solaire est un atout pour la France":
        prompt="{}, premier ministre, présente dans les grandes lignes les premiers résultats de son plan de transition énergétique {}. Le plan s'appuie sur {}% de nucléaire et {}% d'ENR, ne laissant ainsi que {}% de gaz fossile dans le mix. Cela a permis de faire baisser de {}% l'empreinte carbone de la France sur les 5 dernières années. Par ailleurs, le ministre {}. Aussi, il {}.".format(name,occasion,pct_nuc,pct_enr,pct_gaz_fossiles,evo_co2,politique,alea)
    elif theme=="L’énergie nucléaire est un atout pour la France":
        prompt="{}, premier ministre, présente dans les grandes lignes les premiers résultats de son plan de transition énergétique {}. Le plan s'appuie sur {}% de nucléaire et {}% d'ENR, ne laissant ainsi que {}% de gaz fossile dans le mix. Cela a permis de faire baisser de {}% l'empreinte carbone de la France sur les 5 dernières années. Par ailleurs, le ministre {}. Aussi, il {}.".format(name,occasion,pct_nuc,pct_enr,pct_gaz_fossiles,evo_co2,politique,alea)
    ################################
    #         Élu local            #
    ################################
    elif theme=="des pertes d’emplois liées à la suppression centrale nucléaire":
        region,nb_centrales,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, député maire d'une commune de {} qu'on précisera, s'exprime {} où il aborde la fermeture de {} réacteurs dans une commune de sa circonscription qu'on précisera.".format(name,region,occasion,nb_centrales)
    elif theme=="du trop grand nombre de panneaux photovoltaïque dénaturant les paysages et entravant les cultures":
        region,nb_parcs,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, député maire d'une commune de {} qu'on précisera, s'exprime {} où il évoque le nombre grandissant de panneaux photovoltaïques dénaturant les paysages et entravant les cultures. Il parlera en particulier des plaintes des habitants d'une ville de sa circonscription, qu'on citera, concernant les {} parcs récemment installés.".format(name,region,occasion,nb_parcs)
    elif theme=="du trop grand nombre d’éoliennes dénaturant les paysages et entravant les cultures":
        region,nb_eo,type,_=dm.get_data_for_themes(role,theme)
        prompt="{}, député maire d'une commune de {} qu'on précisera, s'exprime {} où il aborde le sujet sensible du nombre d'éoliennes {}-shore grandissant dans les alentours, dénaturant le paysage et entravant les cultures. Il citera par exemple les {} parcs éoliens implantés dans une ville de sa circonscription, qu'on citera, et qui sera proche de la mer s'il s'agit d'éoliennes Off-shore.".format(name,region,occasion,type,nb_eo)
    elif theme=="du déficit d’électricité prévu pour la région":
        region=get_random_region()
        prompt="{}, député maire d'une commune de {} qu'on précisera, s'exprime {} où il évoque son inquiétude pour le déficit d'électricité annoncé dans la région pour les moments à venir.".format(name,region,occasion)
    elif theme=="des parc éoliens offshore qui sont une menace pour l’économie de la mer, pêche et tourisme":
        region,nb_eo,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, député maire d'une commune de {} qu'on précisera, s'exprime {} où il partage son désarroi quant à l'installation de {} parcs éoliens dans sa région.".format(name,region,occasion,nb_eo)
    elif theme=="de la transition, devant s’accompagner selon lui d’investissements dans l’offre de transport en milieu rural":
        region=get_random_region()
        prompt="{}, député maire d'une commune rurale de {} qu'on précisera, s'exprime {} sur le thème de la transition énergétique, qui doit selon lui s'accompagner d'investissements dans l'offre de transports en milieu rural.".format(name,region,occasion)
    elif theme=="de la relocalisation de l’industrie, indispensable à la réduction de notre empreinte carbone, qui doit être accompagnée par l’état (donner un exemple) ":
        region=get_random_region()
        prompt="{}, député maire d'une commune de {} qu'on précisera, s'exprime {} sur l'importance de relocaliser l'industrie en France, pour notamment réduire notre empreinte carbone. Il suggère que cette relocalisation doit être encouragée par l'état.".format(name,region,occasion)
    elif theme=="de l'initiative citoyenne pour mettre en place des circuits courts pour l’alimentation (donner un exemple) ":
        region=get_random_region()
        prompt="{}, député maire d'une commune de {} qu'on précisera, s'exprime {} sur la place de l'initiative citoyenne dans la mise en place de circuits courts.".format(name,region,occasion)
    elif theme=="du tarif progressif proposé au gouvernement pour l’électricité pour permettre aux plus pauvres de répondre aux besoins vitaux ":
        region=get_random_region()
        prompt="{}, député maire d'une commune de {} qu'on précisera, s'exprime {} sur l'urgence de mettre en place un dispositif de tarif progressif sur l'électricité pour permettre aux plus pauvres de répondre aux besoins vitaux.".format(name,region,occasion)
    elif theme=="de la favorisation de l’habitat semi-collectif pour mutualiser au mieux les dépenses énergétiques des foyers français, proposé récemment au gouvernement ":
        region=get_random_region()
        prompt="{}, député maire d'une commune de {} qu'on précisera, s'exprime {} où il soumet une idée permettant de mutualiser autant que possible les dépenses énergétiques des foyers Français : celle de l'habitat semi-collectif.".format(name,region,occasion)
    ##################################
    #      PDG Photovoltaïque       #
    ##################################
    elif theme=="du manque d’installation de panneaux photovoltaïques ces dernières années. ":
        nb_panneaux,region,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, PDG de l'entreprise de panneaux photovoltaïques LuminaSolar Tech implantée en {}, s'exprime {} où il aborde le thème du manque d'installation de parcs photovoltaïques ces dernières années. Il n'en compte malheureusement que {} dans sa région.".format(name,region,occasion,nb_panneaux)
    elif theme=="de l'essor du photovoltaïque qui est une aubaine pour la France. ":
        nb_panneaux,region,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, PDG de l'entreprise de panneaux photovoltaïques LuminaSolar Tech implantée en {}, s'exprime {} où il se félicite de l'essor du photovoltaïque ces dernières années, notamment dans sa région où on compte {} parcs livrés ces 5 dernières années.".format(name,region,occasion,nb_panneaux)
    elif theme=="de la difficulté de trouver de la main d’oeuvre qualifiée, malgré le fait que le secteur soit considéré comme porteur. ":
        nb_eo,region,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, PDG de l'entreprise de panneaux photovoltaïques LuminaSolar Tech implantée en {}, s'exprime {} où il se lamente du manque de main d'oeuvre qualifiée pour travailler dans le photovoltaïque qu'il considère pourtant comme porteur. Il blâme pour cela le secteur de l'éolien, ayant installé {} parcs sur les 5 dernières années.".format(name,region,occasion,nb_eo)
    elif theme=="de l'importance fondamentale d’investir dans la recherche sur les nouvelles technologies de panneaux solaires. ":
        region=get_random_region()
        prompt="{}, PDG de l'entreprise de panneaux photovoltaïques LuminaSolar Tech implantée en {}, s'exprime {} où il évoque l'importance fondamentale d'investir dans la recherche sur les nouvelles technologies de panneaux solaires.".format(name,region,occasion)
    elif theme=="de l'importance de développer le stockage d’électricité pour valoriser les nouvelles ENR. ":
        region=get_random_region()
        prompt="{}, PDG de l'entreprise de panneaux photovoltaïques LuminaSolar Tech implantée en {}, s'exprime {} où il évoque l'importance cruciale d'avoir une technologie de stockage d'électricité développée pour que l'energie produite par les ENR ne soit pas gâchée.".format(name,region,occasion)
    elif theme=="de la nécessité de densifier le réseau électrique pour mieux accueillir l’électricité produite pas les panneaux photovoltaïques. ":
        region=get_random_region()
        prompt="{}, PDG de l'entreprise de panneaux photovoltaïques LuminaSolar Tech implantée en {}, s'exprime {} où il aborde le thème de la densité du réseau électrique, qu'il juge insuffisante pour accueillir l'énergie produite par les panneaux solaires.".format(name,region,occasion)
    elif theme=="de l'importance de modifier la législation pour permettre plus d’installations de parc électriques. ":
        region=get_random_region()
        prompt="{}, PDG de l'entreprise de panneaux photovoltaïques LuminaSolar Tech implantée en {}, s'exprime {} où il suggère une modification de la législation, jugée trop lente aujourd'hui pour permettre un développement adéquat du photovoltaïque.".format(name,region,occasion)
    elif theme=="de la concurrence déloyale des producteurs de panneaux photovoltaïques asiatiques (donner un exemple de nom d'entreprise). ":
        region=get_random_region()
        prompt="{}, PDG de l'entreprise de panneaux photovoltaïques LuminaSolar Tech implantée en {}, s'exprime {} où il dénonce la concurrence déloyale des producteurs de panneaux photovoltaïques asiatiques (inventer un nom d'entreprise asiatique de panneaux solaires)".format(name,region,occasion)
    elif theme=="de la nécessité de modifier la législation pour permettre à plus de français d’installer des panneaux voltaïques sur leurs toits même en zones classées. ":
        region=get_random_region()
        prompt="{}, PDG de l'entreprise de panneaux photovoltaïques LuminaSolar Tech implantée en {}, s'exprime {} où il met l'accent sur l'importance de changer la législation sur l'installation de panneaux solaires particuliers même en zones classées..".format(name,region,occasion)
    elif theme=="de la valorisation des autres usages des panneaux photovoltaïques, comme l’ombrage des cultures. ":
        region=get_random_region()
        prompt="{}, PDG de l'entreprise de panneaux photovoltaïques LuminaSolar Tech implantée en {}, s'exprime {} où il fait l'éloge des autres usages des panneaux solaires, comme l'ombrage des cultures.".format(name,region,occasion)
    #############################
    #       PDG Éoliennes       #
    #############################
    elif theme=="du manque d’installation d’éoliennes ces dernières années":
        nb_eo,_,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, PDG du leader de l'éolien en France VentoDynamics, dont le siège social se trouve en Bretagne, s'exprime {} où il déplore le manque d'installation de parcs éoliens ces dernières années. En effet, on ne compte que {} parcs installés, ce qu'il juge insuffisant.".format(name,occasion,nb_eo)
    elif theme=="de l’essor de l’éolien qui est une chance pour la France. Il se félicite des choix du gouvernement. ":
        nb_eo,region,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, PDG du leader de l'éolien en France VentoDynamics, dont le siège social se trouve en Bretagne, s'exprime {} où il se félicite des progrès du secteur de l'éolien en France, en saluant notamment les initiatives en {} (donner une ville de cette région), où pas moins de {} parcs on été installés ces cinq dernières années.".format(name,occasion,region,nb_eo)
    elif theme=="de la difficulté à trouver de la main d’oeuvre qualifiées. ":
        nb_eo,_,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, PDG du leader de l'éolien en France VentoDynamics, dont le siège social se trouve en Bretagne, s'exprime {} où il s'inquiète du manque de main-d'oeuvre face à la demande croissante de parcs éoliens sur notre territoire. En effet, pas moins de {} parcs ont été installés ces cinq dernières années.".format(name,occasion,nb_eo)
    elif theme=="de la tension actuelle sur les métaux rares, et rappelle l'importance cruciale de sécuriser les approvisionnements. ":
        nb_eo,_,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, PDG du leader de l'éolien en France VentoDynamics, dont le siège social se trouve en Bretagne, s'exprime {} où il profite de l'occasion pour mettre l'accent sur la tension actuelle sur les métaux rares et de l'importance cruciale de sécuriser les approvisionnements car le secteur de l'éolien en a besoin. Pas moins de {} parcs ont été livrés ces cinq dernières années, appuyant son propos.".format(name,occasion,nb_eo)
    elif theme=="de la tension sur le cuivre et l’acier, et rappelle l'importance cruciale de sécuriser les approvisionnements. ":
        nb_eo,_,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, PDG du leader de l'éolien en France VentoDynamics, dont le siège social se trouve en Bretagne, s'exprime {} où il profite de l'occasion pour mettre l'accent sur la tension actuelle sur le cuivre et l'acier et de l'importance cruciale de sécuriser les approvisionnements car le secteur de l'éolien en a besoin. Pas moins de {} parcs ont été livrés ces cinq dernières années, appuyant son propos.".format(name,occasion,nb_eo)
    elif theme=="de la nécessité de décarboner la fabrication du béton pour limiter l’impact CO2 de l’éolien. ":
        prompt="{}, PDG du leader de l'éolien en France VentoDynamics, dont le siège social se trouve en Bretagne, s'exprime {} où il aborde le sujet de la décarbonation du béton, essentielle à la décabornation de l'éolien qui dépend beaucoup du béton.".format(name,occasion)
    elif theme=="de l'importance de flexibiliser la demande d’électricité pour valoriser les nouvelles ENR":
        prompt="{}, PDG du leader de l'éolien en France VentoDynamics, dont le siège social se trouve en Bretagne, s'exprime {} où il saisi l'occasion de souligner l'importance de flexibiliser la demande d'électricité pour valoriser les nouvelles ENR.".format(name,occasion)
    elif theme=="de la recherche sur le recyclage des pâles d’éoliennes, avançant à grand pas depuis quelques années. ":
        prompt="{}, PDG du leader de l'éolien en France VentoDynamics, dont le siège social se trouve en Bretagne, s'exprime {} où il se félicite des avancées en recherche ces dernières années, notamment sur le domaine du recyclage des pales d'éoliennes, rendant le secteur beaucoup plus sobre.".format(name,occasion)
    elif theme=="de la nécessité de développer l’éolien flottant, qui permettrait d'exploiter notre cote. ":
        nb_eo_off,_,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, PDG du leader de l'éolien en France VentoDynamics, dont le siège social se trouve en Bretagne, s'exprime {} où il insiste sur l'importance de développer l'éolien flottant qui pourrait mettre à profit notre côte. Sur les cinq dernières années on peut toutefois se féliciter de l'installation de {} parcs éoliens".format(name,occasion,nb_eo_off)
    elif theme=="de la nécessité de promouvoir l’énergie éolienne et lutter contre les a priori sur celle ci. Cela passe entre autres par de la sensibilisation sur le recyclage. ":
        nb_eo,_,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, PDG du leader de l'éolien en France VentoDynamics, dont le siège social se trouve en Bretagne, s'exprime {} où il alerte sur la nécessite de promouvoir l'énergie éolienne et lutter contre les à-priori sur celle-ci. Un des axes identifié par le PDG est la sensibilisation sur le recyclage. À titre informatif, on rappellera que pas moins de {} parcs éoliens ont tout de même été installés ces cinq dernières années".format(name,occasion,nb_eo)
    ##################################
    #      Leader de Greenpeace      #
    ##################################
    elif theme=="de l'augmentation du nombre de réacteurs nucléaires, et des risques géopolitiques sur l’approvisionnement en matières premières associés.":
        nb_reconduites,nb_epr,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, à la tête de l'ONG Green Peace, s'exprime {} où il alerte sur l'augmentation du nombre de réacteurs nucléaires, et des risques géopolitiques sur l’approvisionnement en matières premières associés. Il consolide son discours en citant les faits, à savoir que {} réacteurs ont été reconduits, et {} nouveaux EPR2 ont été installés.".format(name,occasion,nb_reconduites,nb_epr)
    elif theme=="des émissions de CO2 trop importantes":
        prompt="{}, à la tête de l'ONG Green Peace, s'exprime {} où il alerte sur les émissions de CO2 toujours trop importantes. Elles sont encore à {} ce qu'il juge comme trop élevé.".format(name,occasion,co2)
    elif theme=="des risques Gestion des déchets nucléaires":
        nb_reconduites,nb_epr,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, à la tête de l'ONG Green Peace, prend la parole {} où il aborde le sujet très sensisble de la gestion des déchets nucléaires. En effet, avec {} réacteurs actifs sur le territoire, on ne peut plus ignorer ce risque pouvant gravement nuire au vivant.".format(name,occasion,nb_reconduites+nb_epr)
    elif theme=="du risque d’accidents sur les centrales nucléaires":
        nb_reconduites,nb_epr,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, à la tête de l'ONG Green Peace, s'exprime {} où il tire la sonnette d'alarme quant au nombre de réacteurs nucléaires actuellement en service en France. En effet, selon le leader {} est bien trop élevé et duplique les chances d'un accident catastrophe.".format(name,occasion,nb_reconduites+nb_epr)
    elif theme=="des installations massives d'éoliennes impactant durement la biodiversité":
        nb_eo,_,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, à la tête de l'ONG Green Peace, s'exprime {} où il s'indigne du nombre de parc éoliens actuellement sur le territoire. En effet selon lui, {} parcs est un nombre bien trop élevé et nuit grandement à la biodiversité.".format(name,occasion,nb_eo)
    elif theme=="des installations massives de panneaux photovoltaïques impactant durement la biodiversité":
        nb_panneaux,region_panneaux,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, à la tête de l'ONG Green Peace, s'exprime {} où il s'indigne du nombre de parc photovoltaïques récemment installés en {}. En effet selon lui, {} parcs est un nombre bien trop élevé et nuit grandement à la biodiversité.".format(name,occasion,region_panneaux,nb_panneaux)
    elif theme=="du fait que la sobriété est la seule solution":
        prompt="{}, à la tête de l'ONG Green Peace, s'exprime {} où il revient sur le débat de la responsabilité individuelle. Certes, les entreprises ont un impact dévastateur sur l'environnement mais il nous appartient d'adopter un mode de vie plus résiliant et sobre ce qui forcera les entreprises à suivre.".format(name,occasion)
    elif theme=="du fait que la réflexion sur le mix électrique ne doit pas faire oublier que nous faisons face à une crise écologique plus large avec le dépassement de plusieurs limites planétaires":
        prompt="{}, à la tête de l'ONG Green Peace, s'exprime {} où il essaye de nous faire prendre un peu de recul sur le débat actuel portant sur le mix énergétique. Selon {}, le mix ne doit pas nous faire oublier ue nous faisons face à une crise écologique plus large avec le dépassement de plusieurs limites planétaires".format(name,occasion,name)
    elif theme=="du fait que le financement de la transition doit se faire en taxant les entreprises qui polluent et mettent du CO2":
        prompt="{}, à la tête de l'ONG Green Peace, s'exprime {} où il partage son avis sur la contribution des entreprises à la transition énergétique. Selon {}, cette contribution est trop faible, et les entreprises devraient payer à hauteur de ce qu'elles polluent.".format(name,occasion,name)
    elif theme=="de l'utilisation de la voiture en milieu urbain qui devrait être proscrit":
        prompt="{}, à la tête de l'ONG Green Peace, s'exprime {} sur l'usage de la voiture. Selon {}, son usage en milieu urbain devrait être proscrit et on devrait privilégier les mobilités plus douces comme le vélo, la marche ou les transports en commun".format(name,occasion,name)
    ###################################
    #     Leader des agriculteurs     #
    ###################################
    elif theme=="de la concurrence des sols avec les Panneaux photovoltaïques":
        nb_panneaux,_,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, leader du syndicat des agriculteurs Terres Unies, s'exprime {} où il déplore la concurrence pour les sols avec les parcs de panneaux photovoltaïques. En effet, on compte pas moins de {} parcs dans des zones qui pourraient être utilisées pour l'agriculture.".format(name,occasion,nb_panneaux)
    elif theme=="de la concurrence des sols avec les Eoliennes":
        nb_eo_on,_,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, leader du syndicat des agriculteurs Terres Unies, s'exprime {} où il pointe du doigt un problème de concurrence des sols avec les parcs éoliens. En effet on compte selon lui pas moins de {} parcs éoliens sur des zones qui pourraient servir à des cultures.".format(name,occasion,nb_eo_on)
    elif theme=="de l'adaptation au changement de régime alimentaire des français qui consomment moins de viande":
        prompt="{}, leader du syndicat des agriculteurs Terres Unies, s'exprime {} où il évoque à cette occasion les difficulés causée par l'évolution du régime alimentaire des Français. En effet, le syndicat estime qu'il y a actuellement trop de bétail sur le territoire Français par rapport à la demande.".format(name,occasion)
    elif theme=="de l'adaptation au dérèglement climatique, donner des exemples":
        prompt="{}, leader du syndicat des agriculteurs Terres Unies, s'exprime {} où il pointe la nécessité pour l'agriculture de s'adapter au changement climatique. La gestion de l'eau et de l'aridité des sols est un sujet, la canicule en est un autre, ne pas hésiter à citer d'autres exemples.".format(name,occasion)
    elif theme=="de la sécheresses amplifiées par le dérèglement climatique":
        prompt="{}, leader du syndicat des agriculteurs Terres Unies, s'exprime {} où il déplore la sécheresse des sols, amplifiée par le dérèglement climatique, et mettant à mal la production.".format(name,occasion)
    elif theme=="de la pénurie de main d’oeuvre agricole":
        prompt="{}, leader du syndicat des agriculteurs Terres Unies, s'exprime {} où il s'indigne sur la pénurie de main-d'oeuvre agricole en France. Il encourage les jeunes générations à retourner à l'essentiel et fait un plaidoyer pour la quête du sens au travail.".format(name,occasion)
    elif theme=="de la difficulté de l'électrification des véhicules agricoles":
        prompt="{}, leader du syndicat des agriculteurs Terres Unies, s'exprime {} où il aborde l'électrification globale des véhicules sur le territoire. Il informe, bien embêté, que les véhicules agricoles sont très durs à électrifier et par conséquent la culture emettra toujours un peu.".format(name,occasion)
    elif theme=="de la méthanisation de la biomasse réduit son utilisation pour l’agriculture":
        nb_metha,_,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, leader du syndicat des agriculteurs Terres Unies, s'exprime {} où il partage son mécontentement quant à l'augmentation du nombre de méthaniseurs sur le territoire. D'après lui, {} méthaniseurs est un nombre bien trop élevé et fait concurrence pour la biomasse dont on se sert aussi en agriculture.".format(name,occasion,nb_metha)
    elif theme=="de la difficulté de s’approvisionner en engrais azotés avec la baisse drastique des importations de gaz et de pétroles":
        prompt="{}, leader du syndicat des agriculteurs Terres Unies, s'exprime {} où il fait part de la difficulté de s’approvisionner en engrais azotés avec la baisse drastique des importations de gaz et de pétroles.".format(name,occasion)
    elif theme=="de la difficulté à répercuter sur les prix, la hausse des couts de l’énergie":
        prompt="{}, leader du syndicat des agriculteurs Terres Unies, s'exprime {} où il fait part de la difficulté à répercuter sur les prix la récente hausse des couts de l’énergie.".format(name,occasion)
    ############################################
    #   Ministre de la transition écologique   #
    #        et des solidarités                #
    ############################################
    elif theme=="du gouvernement faisant tout son possible pour limiter les jours de pénuries d’électricité":
        nb_penu,_,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, Ministre de la transition écologique et des solidarités, s'exprime {} où il tente de rassurer les concitoyens quant aux {} pénuries d'électricité survenues récemment. Il assure que le gouvernement fait tout son possible pour limiter les jours de pénuries.".format(name,occasion,nb_penu)
    elif theme=="de l'équilibre géographique du réseau":
        prompt="{}, Ministre de la transition écologique et des solidarités, s'exprime {} où il partage son sentiment sur l'état actuel du mix Français. Avec {}% de nucléaire, {}% d'ENR, et {}% de gaz fossiles, il est convaincu que nous sommes en bonne voie pour atteindre les objectifs fixés.".format(name,occasion,pct_nuc,pct_enr,pct_gaz_fossiles)
    elif theme=="du renforcement des échanges européens d’électricité":
        nb_penu,_,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, Ministre de la transition écologique et des solidarités, s'exprime {} où il aborde le sujet tendu des récentes pénuries d'électricité vécues sur le territoire. Il assure que ce sont {} pénuries de trop, mais qu'on s'assure que çe ne se reproduise plus en renforcement nos systèmes d'échange à l'échelle européenne.".format(name,occasion,nb_penu)
    elif theme=="de la promotion des éco gestes":
        prompt="{}, Ministre de la transition écologique et des solidarités, s'exprime {} où il s'attele à la promotion des éco-gestes, donner plusieurs exemples.".format(name,occasion)
    elif theme=="de l’isolation des bâtiments qui est une priorité du gouvernement":
        prompt="{}, Ministre de la transition écologique et des solidarités, s'exprime {} où il décide d'aborder l'isolation thermique des bâtiments, qui est à l'heure actuelle insuffisante. Selon lui, il est nécessaire d'accélerer la marche si on souhaite atteindre nos objectifs de consommation d'énergie.".format(name,occasion)
    elif theme=="de la réflexion sur la construction de nouvelles mines de Lithium en France pour alimenter la transition écologique":
        prompt="{}, Ministre de la transition écologique et des solidarités, s'exprime {} où il partage ses pensées sur l'éventuelle construction de nouvelles mines de Lithium en France pour alimenter la transition écologique.".format(name,occasion)
    elif theme=="du lancement d’un plan de formation aux métiers de l’énergie":
        prompt="{}, Ministre de la transition écologique et des solidarités, s'exprime {} où il décide d'annoncer le lancement de son plan de formation aux métiers de l'énergie, donner des exemples de métiers.".format(name,occasion)
    elif theme=="du lancement d’un grand plan vélo en ville pour sortir à terme les voitures des centres ville":
        prompt="{}, Ministre de la transition écologique et des solidarités, s'exprime {} où il parle de son plan vélo visant à faire sortir, à termes, les voitures des centres urbains.".format(name,occasion)
    elif theme=="du gouvernement qui se montre attentif aux coûts des énergies, mais ajoute toutefois que ceux ci vont monter inexorablement":
        prompt="{}, Ministre de la transition écologique et des solidarités, s'exprime {} où il partage l'inquiétude des Français quant au coût de l'énergie. Il assure se montrer attentif mais note que les coûts vont inexorablement augmenter.".format(name,occasion)
    elif theme=="de l'importance de la réindustrialisation du pays pour limiter l’empreinte écologique des français":
        prompt="{}, Ministre de la transition écologique et des solidarités, s'exprime {} où il fait un discours sur la souveraineté de notre industrie. La France doit selon lui se réindustrialiser pour limiter son empreinte écologique.".format(name,occasion)
    ################################
    #          Activiste           #
    ################################
    elif theme=="Le maintient des centrales nucléaires est un frein à une indispensable sobriété":
        lieu_epr,nb_epr,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, activiste du groupe Extinction Rébellion, s'exprime {} où il dénonce avec ferveur les {} nouveaux réacteurs en {} (donner un nom de ville). Selon lui, cette source d'énergie est un véritable frein à une indispensable sobriété.".format(name,occasion,nb_epr,lieu_epr)
    elif theme=="La construction d’un nouveau tunnel ferroviaire détruit le milieu naturel d’espèces sauvages":
        prompt="{}, activiste du groupe Extinction Rébellion, s'exprime {} où il blâme la construction d’un nouveau tunnel ferroviaire détruisant le milieu naturel d’espèces sauvages.".format(name,occasion)
    elif theme=="La construction de méga bassines est inadaptée au dérèglement climatique et soutient une agriculture productiviste":
        prompt="{}, activiste du groupe Extinction Rébellion, s'exprime {} où il affirme que la construction de méga bassines est inadaptée au dérèglement climatique et soutient une agriculture productiviste.".format(name,occasion)
    elif theme=="Les barrages sur des rivières sont des catastrophes pour la biodiversité":
        region=get_random_region()
        prompt="{}, activiste du groupe Extinction Rébellion, s'exprime {} où il s'inquiète des barrages sur les rivières de sa région ({}), qui sont d'après lui une catastrophe pour la biodiversité.".format(name,occasion,region)
    elif theme=="Les publicités induisent de la surconsommation":
        prompt="{}, activiste du groupe Extinction Rébellion, s'exprime {} où il déplore les publicités actuellement passées sur nos médias, incitant au consumérisme et donc à un mode de vie irrespectueux de l'environnement.".format(name,occasion)
    elif theme=="Le technosolutionisme est un mirage":
        prompt="{}, activiste du groupe Extinction Rébellion, s'exprime {} où il profite de l'occasion pour asséner un coup au pro-technologie, assurant que le technosolutionisme est un mirage.".format(name,occasion)
    elif theme=="L’impact de l’éolien en mer sur la faune marine est dramatiquement sous-évalué (donner un exemple)":
        lieu_eo,nb_eo,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, activiste du groupe Extinction Rébellion, s'exprime {} au sujet de l’impact de l'installation de {} parcs éolien en mer en {}, sur la faune marine qui est selon lui dramatiquement sous-évalué (donner un exemple d'impact)".format(name,occasion,nb_eo,lieu_eo)
    elif theme=="Le greenwashing est un danger pour la transition (donner deux exemples)":
        prompt="{}, activiste du groupe Extinction Rébellion, s'exprime {} où il profite de cette occasion pour se lamenter sur les dangers du greenwashing pour l'efficacité de notre transition énergétique.".format(name,occasion)
    ################################
    #         Opposition           #
    ################################
    elif theme=="Réduction des émissions de CO2 insuffisantes, donner des chiffres":
        prompt="{}, député du front du renouveau et ancien premier ministre, s'exprime {} où il aborde la question de notre empreinte carbone récemment dévoilée. Selon lui, une évolution de {}% est insuffisante, sans parler de l'empreinte elle même, de {} tonnes de co2.".format(name,occasion,evo_co2,co2)
    elif theme=="Cout en métaux des nouvelles ENR, déficit budgétaire donner des chiffres":
        nb_pv,nb_eo,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, député du front du renouveau et ancien premier ministre, s'exprime {} où il aborde la question du coût en métaux de nos ENR. Selon lui la gestion du gouvernement est désastreuse, avec {} nouveaux parcs photovoltaïques et {} nouveaux parcs éoliens, les dépenses sont assurémment trop élevées.".format(name,occasion,nb_pv,nb_eo)
    elif theme=="Cout en uranium, dépendance vis à vis des fournisseurs étrangers":
        nb_reac,_,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, député du front du renouveau et ancien premier ministre, s'exprime {} où il soulève la question du coût en uranium de nos {} centrales actuellement en service, et par la même occasion de notre dépendance aux fournisseurs étrangers.".format(name,occasion,nb_reac)
    elif theme=="Trop d’éoliennes induisent un risque sur la stabilité du réseau électrique, donner des chiffres":
        nb_eo,_,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, député du front du renouveau et ancien premier ministre, s'exprime {} où il évoque son profond désaccord avec les politiques du gouvernement notamment sur leur engagement dans l'éolien, avec {} parcs actifs sur le territoire. Selon lui, ces éoliennes induisent un risque d'instabilité d'approvisionnement du réseau.".format(name,occasion,nb_eo)
    elif theme=="Trop de panneaux solaires induisent un risque sur la stabilité du réseau électrique, donner des chiffes":
        nb_pv,_,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, député du front du renouveau et ancien premier ministre, s'exprime {} où il évoque son profond désaccord avec les politiques du gouvernement notamment sur leur engagement dans le photovoltaïque, avec {} parcs actifs sur le territoire. Selon lui, ces parcs induisent un risque d'instabilité de l'approvisionnement du réseau.".format()
    elif theme=="Jours de pénuries trop importants donner des chiffres":
        np_penu,_,_,_=dm.get_data_for_themes(role,theme)
        prompt="{}, député du front du renouveau et ancien premier ministre, s'exprime {} où il dénonce une ingérance du gouvernement face aux {} pénuries vécues par les Français ces dernières années.".format(name,occasion,nb_penu)
    elif theme=="Manque de formation aux métiers liés à la transition, donner des exemples":
        prompt="{}, député du front du renouveau et ancien premier ministre, s'exprime {} où il s'indigne d'un manque de formation aux métiers liés à la transition. Selon lui, nous avons besoin de recrues dans de nombreux domaines, donner des exemples.".format(name,occasion)
    elif theme=="Manque d’anticipation dans l’aménagement du réseau électrique pour s’adapter aux nouvelles ENR":
        prompt="{}, député du front du renouveau et ancien premier ministre, s'exprime {} où il pointe du doigt l'absence d'anticipation quant au virage vers les ENR. Selon lui, le gouvernement n'est entré en marche que bien trop tard.".format(name,occasion)
    elif theme=="Manque d’investissement dans les transports collectifs":
        prompt="{}, député du front du renouveau et ancien premier ministre, s'exprime {} où il s'insurge du manque d'investissement dans les transports en commun, qui doivent faire partie intégrante de la mobilité de demain.".format(name,occasion)
    elif theme=="Manque de coordination à l’échelle européenne des politiques de production de stockage et d’échanges d’électricité":
        prompt="{}, député du front du renouveau et ancien premier ministre, s'exprime {} sur le manque de coordination à l’échelle européenne des politiques de production de stockage et d’échanges d’électricité.".format(name,occasion)
    return prompt
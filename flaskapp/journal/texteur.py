import random


def arguments_agriculteur(personnage, infrastructure):
    arguments_eoliennes = [
        "les éoliennes provoquent une perturbation du paysage et altèrent la beauté naturelle des champs",
        "les éoliennes génèrent des nuisances sonores qui affectent la tranquillité des zones rurales",
        "les éoliennes provoquent des interférences avec les systèmes de navigation des oiseaux migrateurs",
        "les éoliennes entraînent une baisse de la valeur des terrains agricoles environnants",
        "les éoliennes perturbent la vie animale locale en modifiant les habitats naturels",
        "les éoliennes créent des ombres stroboscopiques qui nuisent à la concentration des travailleurs agricoles",
        "les éoliennes augmentent les risques d'accidents liés aux hélices, notamment pour le bétail",
        "les éoliennes imposent des restrictions d'usage des terres agricoles à proximité immédiate"
    ]

    arguments_photovoltaiques = [
        "l'installation de panneaux photovoltaïques occupe de précieuses terres agricoles, réduisant les surfaces cultivables",
        "les panneaux photovoltaïques provoquent une augmentation de la température au sol, ce qui peut affecter la qualité des sols",
        "les panneaux photovoltaïques créent une barrière physique qui gêne le déplacement des animaux d'élevage",
        "l'installation de panneaux photovoltaïques présente un risque pour l'écoulement naturel de l'eau de pluie",
        "les panneaux photovoltaïques réduisent l'espace disponible pour les cultures rotatives, affectant ainsi les rendements",
        "les panneaux photovoltaïques augmentent l'érosion des sols en modifiant leur structure",
        "les panneaux photovoltaïques limitent la biodiversité sur les parcelles où ils sont installés",
        "les panneaux photovoltaïques provoquent des réflexions lumineuses qui peuvent perturber les activités agricoles alentour"
    ]

    arguments_methaniseur = [
        "l'installation d'un méthaniseur présente un danger d'explosion ou de fuite de gaz nocifs pour les cultures",
        "le méthaniseur génère des odeurs désagréables qui se propagent dans les champs et dérangent les travailleurs agricoles",
        "le méthaniseur augmente le trafic routier autour des exploitations, perturbant le travail agricole",
        "le méthaniseur risque de contaminer les sols et les nappes phréatiques avec des résidus organiques",
        "le méthaniseur crée une dépendance excessive à l'importation de déchets organiques externes, affectant la gestion des terres",
        "l'installation d'un méthaniseur provoque une augmentation des nuisances sonores, surtout pendant les phases de chargement",
        "le méthaniseur modifie les cycles de production agricole en imposant des contraintes sur la gestion des déchets",
        "l'installation d'un méthaniseur représente une menace pour la santé du bétail en cas de mauvaise gestion des déchets"
    ]

    if personnage.role == "agriculteur":
        if infrastructure == "éolien onshore":
            return random.sample(arguments_eoliennes, 2)
        elif infrastructure == "photovoltaïque":
            return random.sample(arguments_photovoltaiques, 2)
        elif infrastructure == "méthaniseur":
            return random.sample(arguments_methaniseur, 2)
    return []

def texte_agriculteur(personnage, region, infrastructure):
    # Sélectionner une foire agricole aléatoire dans la région
    foire = random.choice(region.foires_agricoles)
    
    # Générer deux arguments contre l'infrastructure
    arguments = arguments_agriculteur(personnage, infrastructure)
    
    # Si la liste d'arguments est vide ou ne contient pas assez d'éléments
    if len(arguments) < 2:
        return "Erreur : Impossible de générer des arguments suffisants pour ce personnage et cette infrastructure."

    # Modèles de texte pour chaque infrastructure
    modeles_eolien = [
    f"Dans la région {region.nom}, {personnage.nom} {personnage.prenom}, un agriculteur affilié à {personnage.affiliation}, "
    f"mène un combat acharné contre l'implantation d'un parc éolien à proximité de ses terres. Lors de la {foire}, une grande foire agricole locale, "
    f"il a pris la parole pour exprimer son opposition claire à cette infrastructure, expliquant en détails les raisons de son désaccord. "
    f"Selon lui, {arguments[0]}, ce qui représente une menace directe pour la durabilité de ses cultures et le respect de l'environnement agricole. "
    f"De plus, {arguments[1]}, aggravant encore les risques qu'il perçoit pour l'économie locale. {personnage.nom} s’est engagé à mener cette lutte "
    f"jusqu’au bout, convaincu qu’il défend non seulement sa propre exploitation, mais aussi l’identité rurale et le mode de vie agricole de {region.nom}.",
    
    f"{personnage.nom} {personnage.prenom}, un agriculteur de {region.nom} et membre actif de {personnage.affiliation}, a profité de l’occasion de la"
    f" {foire} pour exprimer sa vive opposition face au projet d'éoliennes. Il a fermement déclaré que {arguments[0]}, ce qui aurait des répercussions "
    f"sérieuses sur la santé et la sécurité des personnes et des animaux de la région. Il a également ajouté que {arguments[1]}. Son engagement "
    f"a suscité une forte adhésion parmi les agriculteurs et les habitants de la région, qui partagent ses préoccupations quant aux conséquences de "
    f"cette installation sur le paysage et l'économie locale.",
    
    # Trois autres variantes similaires avec détails supplémentaires
    ]

    
    modeles_photovoltaique = [
    f"Dans la région de {region.nom}, {personnage.nom} {personnage.prenom}, un agriculteur affilié à {personnage.affiliation}, a exprimé récemment "
    f"son mécontentement à propos de l'installation de panneaux solaires dans ses environs. Lors de la {foire}, il a pris le micro pour expliquer en détail "
    f"pourquoi il considère que cette infrastructure est problématique pour les terres agricoles environnantes. {personnage.nom} a souligné que "
    f"{arguments[0]}, ce qui, selon lui, compromet l'équilibre de son exploitation. En outre, il a mis l'accent sur le fait que {arguments[1]}, "
    f"pointant du doigt les conséquences néfastes à long terme pour la biodiversité de la région. Profondément attaché à la préservation de ses terres, "
    f"il a affirmé que cette installation bouleverserait non seulement l’économie locale, mais aussi les modes de production agricoles traditionnels.",
    
    f"{personnage.nom} {personnage.prenom}, un agriculteur originaire de {region.nom}, est un membre influent de {personnage.affiliation}. Il s'est exprimé "
    f"lors de la {foire} pour dénoncer l'installation croissante de panneaux photovoltaïques dans la région. Il a affirmé que {arguments[0]}, et que cette "
    f"situation posait un risque majeur pour l’avenir de l’agriculture dans cette zone. Il a également fait part de son inquiétude en ajoutant que "
    f"{arguments[1]}. {personnage.nom} est désormais à la tête d’un mouvement de protestation croissant, réunissant de plus en plus d’agriculteurs et de riverains "
    f"qui craignent les répercussions écologiques de ces installations solaires sur leurs exploitations.",
    
    # Trois autres variantes similaires avec détails supplémentaires
    ]

    modeles_methaniseur = [
    f"Lors de la {foire} en {region.nom}, {personnage.nom} {personnage.prenom}, un agriculteur et membre actif de {personnage.affiliation}, a exprimé avec passion "
    f"son opposition à l’installation d'un méthaniseur près de ses terres. Il a déclaré que {arguments[0]}, soulignant les répercussions négatives sur l’exploitation "
    f"de ses terres et le bien-être des habitants locaux. {personnage.nom} a également mis en lumière que {arguments[1]}, ce qui pourrait, selon lui, avoir des effets "
    f"désastreux sur les ressources en eau et sur l’ensemble du réseau agricole local. En tant que défenseur infatigable de l’agriculture durable, il s’est engagé à "
    f"mener cette bataille, conscient de l'importance de protéger l’environnement rural de {region.nom}.",
    
    f"En {region.nom}, {personnage.nom} {personnage.prenom}, un agriculteur, a pris la parole lors de la {foire} pour contester le projet controversé d’un méthaniseur près "
    f"de ses terres. Selon lui, {arguments[0]}, ce qui mettrait en péril l'avenir de son exploitation. En outre, il a averti que {arguments[1]}. {personnage.nom}, "
    f"connu pour sa détermination et son sens de l'engagement, a réussi à sensibiliser de nombreux autres agriculteurs et citoyens, qui partagent désormais ses préoccupations "
    f"face à ce qu'ils perçoivent comme une menace pour le mode de vie agricole traditionnel et l'équilibre écologique de la région.",
    
    # Trois autres variantes similaires avec détails supplémentaires
    ]


    # Sélectionner aléatoirement un texte en fonction de l'infrastructure
    if infrastructure == "éolien onshore":
        texte_final = random.choice(modeles_eolien)
    elif infrastructure == "photovoltaïque":
        texte_final = random.choice(modeles_photovoltaique)
    elif infrastructure == "méthaniseur":
        texte_final = random.choice(modeles_methaniseur)
    else:
        return "Erreur : Infrastructure non reconnue."

    return texte_final


def arguments_activiste(personnage, infrastructure):
    # Arguments pour les éoliennes onshore
    arguments_eoliennes_onshore = [
        "les éoliennes onshore ne représentent pas une alternative crédible aux énergies fossiles si nous n'actionnons pas en priorité le levier de la sobriété.",
        "les éoliennes onshore modifient profondément nos paysages, et affectent aussi directement la faune locale",
        "les éoliennes onshore peuvent causer des collisions mortelles pour les oiseaux et les chauves-souris.",
        "l'ombre stroboscopique des éoliennes onshore perturbe les rythmes biologiques des animaux sauvages.",
        "l'installation des éoliennes onshore consomment de grandes quantités d'acier et de béton relativement à leur niveau de production.",
        "les éoliennes onshore imposent une artificialisation importante d'espaces naturelles au regard de leur production.",
        "la construction des éoliennes onshore nécessite des routes d'accès qui perturbent la vie sauvage et l'écosystème."
    ]

    # Arguments pour les éoliennes offshore
    arguments_eoliennes_offshore = [
        "les éoliennes offshore perturbent les habitats marins, mettant en péril des espèces sensibles endémiques.",
        "la construction d'éoliennes offshore peut avoir des effets néfastes sur la navigation maritime et les zones de pêche.",
        "les éoliennes offshore peuvent émettre des bruits sous-marins qui affectent la vie marine locale.",
        "les installations offshore peuvent interférer avec les habitudes migratoires de certaines espèces marines.",
        "l'impact visuel des éoliennes offshore peut affecter profondément l'attrait touristique des zones côtières.",
        "la mise en service des grands parcs offshore est un gouffre en terme de ressources minerales.",
        "les éoliennes offshore nécessitent des infrastructures maritimes qui artificialisent encore plus nos zones côtiers."
    ]

    arguments_photovoltaiques = [
        "l'artificialisation de surfaces importantes par les fermes photovoltaïques réduit d'autant les habitats naturels des espèces locales.",
        "la fabrication des panneaux photovoltaïques nécessite des ressources rares et engendre des pollutions.",
        "les panneaux photovoltaïques peuvent créer des effets de chaleur qui impactent les espèces sensibles.",
        "l'installation de panneaux photovoltaïques dans nos campagnes se fait au détriment d'une exploitation des terres pour la production alimentaire.",
        "le recyclage des panneaux photovoltaïques est un angle mort de la filière qu'il conviendrait de développer en parallèle de leur déploiement.",
        "la déforestation pour l'installation de panneaux solaires représente une menace directe pour la biodiversité.",
        "les panneaux photovoltaïques limitent l'accès des animaux aux ressources naturelles vitales sur le terrain.",
        "le photovoltaïque n'est pas une alternative crédible aux énergies fossiles en raison de l'ampleur des ressources minerales consommées."
    ]

    arguments_methaniseur = [
        "les méthaniseurs émettent des gaz à effet de serre qui aggravent le changement climatique.",
        "les méthaniseurs peuvent avoir des impacts sur la qualité de l'air et de l'eau, affectant les écosystèmes locaux.",
        "l'installation de méthaniseurs nécessite des quantités importantes de matières premières ammenées par camion",
        "les méthaniseurs peuvent attirer des nuisibles qui perturbent l'équilibre des écosystèmes environnants.",
        "les projets de méthanisation peuvent causer des nuisances pour le voisinage.",
        "la dépendance aux méthaniseurs peut conduire à une réduction des efforts de compostage et de recyclage.",
        "la filière de méthanisation peut créer un déséquilibre dans l'utilisation des terres au détriment de la production alimentaire ou des espaces sauvages.",
        "les résidus des méthaniseurs peuvent créer des déséquilibres dans les sols, affectant la biodiversité et les cultures."
    ]

    if personnage.role == "activiste":
        if infrastructure == "éolien onshore":
            return random.sample(arguments_eoliennes_onshore, 2)
        elif infrastructure == "éolien offshore":
            return random.sample(arguments_eoliennes_offshore, 2)
        elif infrastructure == "photovoltaïque":
            return random.sample(arguments_photovoltaiques, 2)
        elif infrastructure == "méthaniseur":
            return random.sample(arguments_methaniseur, 2)
    return []


def texte_activiste(personnage, region, infrastructure):
    if infrastructure == "éolien offshore":
        ville = random.choice(region.villes_cotieres)  # Ville côtière pour l'éolien offshore
        espece = random.choice(region.especes_marines)
    else:
        ville = random.choice(region.sous_prefectures)  # Sous-préfecture pour les autres infrastructures
        espece = random.choice(region.especes_terrestres)

    # Sélectionner une personnalité locale qui soutient l'activiste
    soutien = random.choice(region.personnalites)

    # Générer deux arguments contre l'infrastructure
    arguments = arguments_activiste(personnage, infrastructure)

    # Vérification de la présence d'arguments
    if len(arguments) < 2:
        return "Erreur : Impossible de générer des arguments suffisants pour ce personnage et cette infrastructure."

    # Modèles de texte pour chaque infrastructure
    modeles_eolien_offshore = [
        f"Dans la ville côtière de {ville}, {personnage.nom} {personnage.prenom}, une fervente activiste pour l'environnement, "
        f"a récemment pris position contre le projet d'implantation d'un parc éolien offshore. Lors d'un rassemblement organisé sur la plage, "
        f"elle a déclaré que les éoliennes menaçaient l'habitat des {espece}, une espèce protégée qui joue un rôle crucial dans l'écosystème local. "
        f"De plus, elle a reçu le soutien précieux de {soutien}, qui a souligné l'importance de protéger la biodiversité locale face à cette menace. "
        f"Cette mobilisation attire l'attention sur les enjeux environnementaux, montrant que les communautés côtières ne resteront pas passives devant "
        f"des projets qui pourraient avoir des conséquences durables sur leur environnement.",
        
        f"{personnage.nom} {personnage.prenom}, une activiste passionnée de {ville}, a pris la parole lors d'une manifestation bruyante pour dénoncer le projet de parc éolien offshore. "
        f"Elle a affirmé que cette infrastructure pourrait gravement perturber les habitudes migratoires des {espece}, dont la présence est essentielle à "
        f"l'équilibre écologique de la région. En outre, {soutien}, une figure respectée de la communauté, s'est jointe à elle, rappelant l'urgence de "
        f"préserver les écosystèmes côtiers face à cette menace. Leur appel a suscité un débat public sur les choix énergétiques, soulignant l'importance "
        f"de l'écologie dans le développement durable.",
        
        # Ajoutez d'autres variantes similaires pour l'éolien offshore
    ]
    
    modeles_eolien_onshore = [
        f"Dans la sous-préfecture de {random.choice(region.sous_prefectures)}, {personnage.nom} {personnage.prenom} s'oppose fermement à un projet de parc éolien onshore. "
        f"Elle a mis en avant les risques que ce projet pose pour les {espece}, qui sont déjà menacés par la perte de leur habitat. "
        f"À ses côtés, {soutien} a soutenu cette lutte, rappelant que le développement durable doit impérativement prendre en compte la protection des espèces locales. "
        f"Cet engagement a résonné auprès des habitants, qui s'inquiètent des conséquences de ce projet sur leur environnement.",
        
        f"À {random.choice(region.sous_prefectures)}, {personnage.nom} {personnage.prenom} s'est mobilisée contre la construction d'un parc éolien onshore. "
        f"Elle a souligné que cette infrastructure pourrait dégrader les habitats des {espece} et qu'il est impératif d'envisager des alternatives moins nocives. "
        f"Le soutien de {soutien} a été essentiel dans cette mobilisation, car il a alerté la communauté sur l'importance de conserver la biodiversité face à ce type de projets. "
        f"Cela a permis de rassembler les citoyens autour de l'idée que la nature doit être protégée.",
        
        # Ajoutez d'autres variantes similaires pour l'éolien onshore
    ]

    modeles_photovoltaiques = [
        f"À {ville}, {personnage.nom} {personnage.prenom} a organisé une action de sensibilisation massive contre l'installation de panneaux photovoltaïques sur des terres sensibles. "
        f"Lors de cet événement, elle a exprimé ses craintes quant à l'impact de ces panneaux sur les habitats des {espece}, qui migrent souvent à proximité. "
        f"Elle a été rejointe par {soutien}, qui a exprimé ses préoccupations concernant l'impact environnemental de ce projet sur la biodiversité locale. "
        f"Cette action a permis de réunir des membres de la communauté locale, soulignant l'importance de la protection de la nature et de l'équilibre des écosystèmes.",
        
        f"Dans la charmante ville côtière de {ville}, {personnage.nom} {personnage.prenom} s'est mobilisée contre le projet de panneaux photovoltaïques. "
        f"Elle a souligné que l'emplacement choisi pour les panneaux perturberait les habitats des {espece}, qui sont déjà en déclin. "
        f"{soutien} s'est également joint à elle, appelant à une évaluation environnementale plus rigoureuse et à la prise en compte des effets potentiels sur la faune. "
        f"Leur engagement a été salué par de nombreux citoyens, qui ont exprimé leur désir de voir un développement durable qui ne compromet pas leur environnement.",
        
        # Ajoutez d'autres variantes similaires
    ]

    modeles_methaniseur = [
        f"Lors d'une réunion à {ville}, {personnage.nom} {personnage.prenom}, une activiste engagée, a vivement critiqué l'installation d'un méthaniseur près de la côte. "
        f"Elle a alerté le public sur le fait que ce projet mettrait en danger les {espece}, qui jouent un rôle vital dans la chaîne alimentaire marine. "
        f"En outre, elle a reçu le soutien enthousiaste de {soutien}, qui a partagé ses inquiétudes concernant les effets de ce projet sur la santé de l'écosystème marin. "
        f"Cette réunion a mis en lumière les préoccupations croissantes des habitantes de la région, qui craignent que des décisions économiques à court terme nuisent "
        f"à leur environnement à long terme.",
        
        f"A {ville}, {personnage.nom} {personnage.prenom} a pris la parole lors d'une manifestation pacifique pour s'opposer à un projet de méthaniseur. "
        f"Elle a expliqué que l'installation de cet équipement pourrait avoir des répercussions néfastes sur les {espece}, qui sont déjà en danger. "
        f"{soutien} a également exprimé son soutien, insistant sur l'importance de protéger les espèces locales et de trouver des solutions durables pour les déchets. "
        f"Cela a suscité un dialogue public sur la nécessité de mieux prendre en compte l'environnement dans les décisions industrielles.",
        
        # Ajoutez d'autres variantes similaires
    ]

    # Sélectionner aléatoirement un texte en fonction de l'infrastructure
    if infrastructure == "éolien offshore":
        texte_final = random.choice(modeles_eolien_offshore)
    elif infrastructure == "éolien onshore":
        texte_final = random.choice(modeles_eolien_onshore)
    elif infrastructure == "photovoltaïque":
        texte_final = random.choice(modeles_photovoltaiques)
    elif infrastructure == "méthaniseur":
        texte_final = random.choice(modeles_methaniseur)
    else:
        return "Erreur : Infrastructure non reconnue."

    return texte_final



def generer_arguments_photovoltaique():
    """
    Fonction qui génère une liste d'arguments pour défendre l'énergie solaire.
    :return: Liste d'arguments.
    """
    return [
        "l'énergie photovoltaïque contribue à la réduction des émissions de CO2 et lutte contre le changement climatique",
        "elle permet de diversifier le mix énergétique, rendant notre système énergétique plus résilient",
        "les panneaux photovoltaïques créent des emplois locaux dans l'installation et la maintenance",
        "l'énergie solaire est abondante et disponible presque partout, ce qui la rend facilement accessible",
        "les coûts de production des panneaux photovoltaïque ont considérablement diminué ces dernières années, rendant cette source plus compétitive",
        "l'énergie solaire réduit la dépendance aux énergies fossiles importées",
        "les projets photovoltaïques peuvent également stimuler l'économie locale par des investissements et des infrastructures",
        "elle favorise l'innovation et le développement technologique dans le secteur énergétique"
    ]

def texte_pdg_solaire(personnage, region):
    """
    Fonction qui génère un texte d'environ 800 caractères pour un PDG solaire.

    :param personnage: Instance de la classe Personnage.
    :param region: Instance de la classe Region.
    :return: Texte généré.
    """
    # Générer des arguments aléatoires
    arguments = generer_arguments_photovoltaique()
    arguments_selectionnes = random.sample(arguments, 2)

    # Modèles de texte génériques
    textes = [
    f"Le PDG de {personnage.affiliation}, {personnage.prenom} {personnage.nom}, ancienne étudiante de l'INSA Toulouse, met en avant sa passion pour l'énergie photovoltaïque. "
    f"Premièrement, {arguments_selectionnes[0]}. Deuxièmement, {arguments_selectionnes[1]}.",
    
    f"{personnage.prenom} {personnage.nom}, PDG de {personnage.affiliation}, a un parcours impressionnant à l'INSA Toulouse qui l'a conduit à défendre les énergies renouvelables. "
    f"Un argument majeur qu'il évoque est {arguments_selectionnes[0]}. Par ailleurs, {arguments_selectionnes[1]}.",
    
    f"{personnage.prenom} {personnage.nom}, à la tête de {personnage.affiliation}, affirme que l'énergie photovoltaïque représente l'avenir, comme l'indique sa formation à l'INSA Toulouse. "
    f"{arguments_selectionnes[0]} et {arguments_selectionnes[1]} sont des points essentiels qu'il souhaite mettre en avant.",
    
    f"Lors d'un récent événement, {personnage.prenom} {personnage.nom}, PDG de {personnage.affiliation}, a souligné l'importance de l'énergie renouvelable, une thématique renforcée par son passage à l'INSA Toulouse. "
    f"Pour commencer, {arguments_selectionnes[0]} et {arguments_selectionnes[1]} constituent des arguments solides pour l'énergie photovoltaïque.",
    
    f"Dans une allocution, {personnage.prenom} {personnage.nom}, PDG de {personnage.affiliation}, a partagé son expérience à l'INSA Toulouse, qui lui a permis de comprendre les enjeux environnementaux. "
    f"{arguments_selectionnes[0]} et {arguments_selectionnes[1]} illustrent pourquoi le développement de l'énergie photovoltaïque est crucial.",
    
    f"{personnage.prenom} {personnage.nom}, dirigeante de {personnage.affiliation}, formée à l'INSA Toulouse, évoque l'avenir prometteur de l'énergie photovoltaïque. "
    f"{arguments_selectionnes[0]} et {arguments_selectionnes[1]} démontrent les avantages de ce secteur en pleine croissance.",
    
    f"Le PDG de {personnage.affiliation}, {personnage.prenom} {personnage.nom}, a récemment exprimé une vision claire pour l'énergie photovoltaïque, fruit de son éducation à l'INSA Toulouse. "
    f"Tout d'abord, {arguments_selectionnes[0]} et {arguments_selectionnes[1]} sont des raisons cruciales pour soutenir cette filière.",
    
    f"{personnage.prenom} {personnage.nom}, à la tête de {personnage.affiliation}, a récemment défendu ardemment l'énergie photovoltaïque. "
    f"{arguments_selectionnes[0]} et {arguments_selectionnes[1]} sont des arguments essentiels pour son développement."
]


    # Choisir un texte aléatoire
    texte_choisi = random.choice(textes)

    # Variantes de texte pour la France
    variantes_france = [
        f"{personnage.prenom} {personnage.nom} défend une vision ambitieuse pour l’énergie photovoltaïque en France. « L’inaction ralentit considérablement les progrès que nous pourrions réaliser, » déclare-t-elle. Elle appelle à une politique publique plus volontariste pour accélérer le déploiement des installations photovoltaïques.",
        f"{personnage.prenom} {personnage.nom}, PDG de {personnage.affiliation}, plaide pour une véritable révolution solaire en France. « Nos voisins européens avancent plus vite que nous dans ce domaine, » observe-t-elle. Elle estime que la France pourrait devenir un leader mondial du photovoltaïque avec les bons investissements.",
        f"En tant que dirigeante de {personnage.affiliation}, {personnage.prenom} {personnage.nom} s'inquiète du retard pris par la France dans le développement de l'énergie photovoltaïque. « Le gouvernement doit impérativement revoir sa stratégie s’il veut tenir ses engagements climatiques, » insiste-t-elle."
    ]

    # Variantes de texte pour les régions hors France
    sous_prefecture = random.choice(region.sous_prefectures)
    variantes_hors_france = [
        f"Sous la direction de {personnage.prenom} {personnage.nom}, {personnage.affiliation} continue de renforcer son engagement pour le solaire avec un nouveau parc photovoltaïque à proximité de {sous_prefecture}. Cette initiative va fournir de l'électricité verte pour des milliers de foyers.",
        f"{personnage.prenom} {personnage.nom}, PDG de {personnage.affiliation}, annonce un ambitieux projet de parc photovoltaïque dans la région de {sous_prefecture}, visant à augmenter la capacité énergétique renouvelable et à réduire l'empreinte carbone de la région.",
        f"{personnage.prenom} {personnage.nom} continue de développer des projets solaires près de {sous_prefecture}, avec l'objectif de stimuler l'économie locale tout en contribuant à la transition énergétique."
    ]

    # Adapter le texte en fonction de la région
    if region.nom == "France":
        texte_final = texte_choisi + " " + random.choice(variantes_france)
    else:
        texte_final = texte_choisi + " " + random.choice(variantes_hors_france)

    return texte_final



def selectionner_arguments_eoliennes():
    """
    Sélectionne deux arguments aléatoires parmi les 10 pour défendre l'énergie éolienne.
    
    :return: Tuple de deux arguments sélectionnés.
    """
    arguments = [
        "les éoliennes sont une source d'énergie propre qui ne produit aucune émission de gaz à effet de serre lors de la production d'électricité",
        "l'énergie éolienne est renouvelable et inépuisable, contrairement aux combustibles fossiles qui se raréfient",
        "les éoliennes permettent de créer des emplois locaux dans l'installation, la maintenance et la gestion des parcs éoliens",
        "l'électricité d'origine éolienne contribue à diversifier le mix énergétique, réduisant ainsi la dépendance aux énergies fossiles",
        "l'énergie éolienne peut être exploitée dans de nombreux environnements, aussi bien terrestres que marins, augmentant ainsi la flexibilité des infrastructures",
        "les éoliennes jouent un rôle clé dans la transition énergétique, en permettant de réduire les émissions de CO2 à l'échelle mondiale",
        "l'électricité d'origine éolienne est devenue de plus en plus compétitive avec les autres sources d'énergie, en raison des progrès technologiques et de la baisse des coûts",
        "les parcs éoliens peuvent être intégrés dans des zones agricoles sans perturber l'activité agricole, offrant ainsi une double utilisation des terres",
        "l'énergie éolienne réduit la dépendance aux importations d'énergie, renforçant ainsi la sécurité énergétique des pays",
        "les éoliennes ont un impact environnemental minimal, avec des technologies modernes permettant de minimiser les nuisances sonores et visuelles"
    ]
    
    # Sélectionne aléatoirement deux arguments parmi les 10
    return random.sample(arguments, 2)

def texte_pdg_eolien(personnage, region):
    """
    Fonction qui génère un texte d'environ 800 caractères pour un PDG défendant l'énergie éolienne.

    :param personnage: Instance de la classe Personnage.
    :param region: Instance de la classe Region.
    :return: Texte généré.
    """
    # Générer des arguments aléatoires sur l'éolien
    arguments_selectionnes = selectionner_arguments_eoliennes()

    # Modèles de texte
    textes = [
    f"Le PDG de {personnage.affiliation}, {personnage.prenom} {personnage.nom}, ancien élève de l'INSA Toulouse, exprime sa passion pour les énergies renouvelables, "
    f"notamment l'éolien. Premièrement, {arguments_selectionnes[0]}. Deuxièmement, {arguments_selectionnes[1]}. ",
    
    f"{personnage.prenom} {personnage.nom}, à la tête de {personnage.affiliation}, a un parcours à l'INSA Toulouse qui l'a conduit à défendre les énergies renouvelables. "
    f"Un argument majeur en faveur de l'éolien est {arguments_selectionnes[0]}. Par ailleurs, {arguments_selectionnes[1]}. ",
    
    f"{personnage.prenom} {personnage.nom}, dirigeant de {personnage.affiliation}, affirme que l'énergie éolienne est l'avenir, une conviction renforcée par sa formation à l'INSA Toulouse. "
    f"{arguments_selectionnes[0]} et {arguments_selectionnes[1]} sont des points essentiels qu'il souhaite mettre en avant. ",
    
    f"Lors d'un récent événement, {personnage.prenom} {personnage.nom}, PDG de {personnage.affiliation}, a souligné les enjeux environnementaux, notamment grâce à son passage à l'INSA Toulouse. "
    f"Pour commencer, {arguments_selectionnes[0]} et {arguments_selectionnes[1]} constituent des arguments solides pour l'énergie éolienne. ",
    
    f"Dans une allocution, {personnage.prenom} {personnage.nom}, PDG de {personnage.affiliation}, a partagé l'importance des énergies renouvelables, comme le prouve son expérience à l'INSA Toulouse. "
    f"{arguments_selectionnes[0]} et {arguments_selectionnes[1]} illustrent les raisons de développer l'énergie éolienne. ",
    
    f"{personnage.prenom} {personnage.nom}, à la tête de {personnage.affiliation}, formé à l'INSA Toulouse, voit un avenir prometteur pour l'éolien. "
    f"{arguments_selectionnes[0]} et {arguments_selectionnes[1]} démontrent les avantages de ce secteur en pleine croissance. ",
    
    f"Le PDG de {personnage.affiliation}, {personnage.prenom} {personnage.nom}, a récemment partagé une vision claire pour l'énergie éolienne, fruit de son éducation à l'INSA Toulouse. "
    f"Tout d'abord, {arguments_selectionnes[0]} et {arguments_selectionnes[1]} sont des raisons cruciales pour soutenir cette filière. ",
    
    f"{personnage.prenom} {personnage.nom}, dirigeant de {personnage.affiliation}, défend ardemment l'énergie éolienne. "
    f"{arguments_selectionnes[0]} et {arguments_selectionnes[1]} sont des arguments essentiels pour son développement. "
    ]


    # Adapter le texte en fonction de la région avec 4 versions aléatoires
    texte_choisi = random.choice(textes)
    if region.nom == "France":
        variantes_france = [
            " Malheureusement, il est regrettable que le gouvernement ne mise pas davantage sur l'énergie éolienne. Nous perdons un temps précieux alors que le potentiel est immense et sous-exploité.",
            " Le manque de soutien gouvernemental est une occasion manquée pour la France de devenir un leader dans l'énergie renouvelable. Il est temps de changer de cap pour répondre aux défis climatiques.",
            " C'est regrettable que le gouvernement n'ait pas pris la pleine mesure de l'opportunité que représente l'éolien. Nous devons investir plus, et vite, pour rester compétitifs sur le plan énergétique.",
            " Il est dommage que la France ne s'engage pas pleinement dans cette voie. Nous devons accroître les investissements pour profiter de l'immense potentiel de l'éolien."
        ]
        texte_final = texte_choisi + random.choice(variantes_france)
    else:
        sous_prefecture = random.choice(region.sous_prefectures)
        variantes_region = [
            f" Nous sommes ravis d'annoncer la mise en place d'un nouveau parc éolien près de {sous_prefecture}. Ce projet bénéficiera à la région et à ses habitants, en générant une énergie propre et durable.",
            f" La construction d'un parc éolien aux abords de {sous_prefecture} est une excellente nouvelle pour la région. Ce projet apportera une énergie verte et créera des emplois locaux.",
            f" Avec l'installation prochaine d'un parc éolien à proximité de {sous_prefecture}, nous renforçons la transition énergétique de la région tout en soutenant l'économie locale.",
            f" Un nouveau parc éolien verra le jour aux alentours de {sous_prefecture}, apportant une énergie renouvelable à la région et participant à la lutte contre le changement climatique."
        ]
        texte_final = texte_choisi + random.choice(variantes_region)

    return texte_final



def tirer_argument_fermeture_nucleaire():
    arguments_fermeture = [
        "La fermeture de cette centrale va priver notre territoire de milliers d'emplois directs et indirects, aggravant le chômage local.",
        "Cette décision menace la stabilité énergétique de notre région, qui dépendait largement de cette centrale pour son approvisionnement.",
        "La centrale était un pilier de notre économie locale, générant des recettes fiscales importantes pour nos collectivités.",
        "Fermer cette centrale sans plan alternatif immédiat va nous rendre plus dépendants des importations d'énergie, avec des conséquences économiques importantes.",
        "C'est une perte majeure pour la recherche et l'innovation, car cette centrale participait à des projets de développement technologique."
    ]
    return random.choice(arguments_fermeture)

def tirer_argument_manque_infrastructure():
    arguments_infrastructure = [
        "Notre territoire souffre d'un manque criant d'infrastructures énergétiques modernes, freinant notre développement économique.",
        "L'absence d'investissements dans le réseau énergétique limite notre capacité à attirer de nouvelles entreprises sur notre territoire.",
        "Les coupures d'électricité fréquentes témoignent d'une infrastructure obsolète qui ne répond plus aux besoins des habitants et des industries.",
        "Le manque d'infrastructures de recharge pour véhicules électriques empêche notre région de s'engager pleinement dans la transition écologique.",
        "Sans investissements massifs dans le réseau énergétique, nous ne pourrons pas répondre aux défis de demain en matière de consommation d'énergie."
    ]
    return random.choice(arguments_infrastructure)

def tirer_argument_creation_site(ville):
    """
    Tire aléatoirement un argument parmi 8 pour annoncer la création d'un site ou d'une industrie liée à la transition énergétique,
    sans impliquer directement la production ou le stockage d'électricité.
    
    :param ville: Nom de la ville où le site sera construit.
    :return: Un argument sélectionné aléatoirement.
    """
    arguments_creation_site = [
        f"La construction de ce centre de rénovation énergétique des bâtiments à {ville} créera des emplois locaux tout en aidant à réduire l'empreinte carbone des infrastructures existantes.",
        f"Le nouveau site de fabrication de matériaux durables pour la construction à {ville} va stimuler l'économie locale et répondre à la demande croissante en éco-construction.",
        f"Ce centre de recherche sur la mobilité douce à {ville} permettra de développer des technologies pour les transports du futur tout en générant des emplois hautement qualifiés.",
        f"Le projet de création d'une usine de fabrication de vélos électriques à {ville} s'inscrit dans une démarche de mobilité durable et offrira des emplois dans un secteur en pleine expansion.",
        f"La mise en place d'un centre de tri et de recyclage avancé à {ville} favorisera l'économie circulaire tout en créant des emplois dans la gestion des déchets et la préservation de l'environnement.",
        f"Le site de production de vêtements écoresponsables à {ville} sera un exemple d'innovation dans l'industrie textile, tout en dynamisant l'emploi local dans un secteur en transformation.",
        f"À {ville}, la création d'une plateforme logistique dédiée aux circuits courts renforcera notre agriculture locale et créera des emplois dans la gestion et la distribution de produits locaux.",
        f"Ce centre de formation aux métiers de la rénovation thermique des bâtiments à {ville} permettra de former les professionnels de demain, tout en offrant des emplois pour accompagner la transition écologique."
    ]
    
    # Sélectionner aléatoirement un argument
    return random.choice(arguments_creation_site)


def texte_elue(personnage, region, situation):
    # Si la situation est la suppression, choisir une ville avec une centrale nucléaire
    if situation == 'supprimée':
        ville = random.choice(region.centrales_nucleaires)
    else:
        ville = random.choice(region.sous_prefectures)
    
    # Introduction aléatoire
    introductions = [
        f"En tant que députée-maire de {ville}, {personnage.prenom} {personnage.nom}, membre du parti {personnage.affiliation},",
        f"Dans son rôle de députée-maire de {ville}, {personnage.prenom} {personnage.nom} ({personnage.affiliation}),",
        f"{personnage.prenom} {personnage.nom}, députée-maire de la ville de {ville},",
        f"Députée-maire de {ville}, {personnage.prenom} {personnage.nom}, affiliée au parti {personnage.affiliation},",
        f"{personnage.prenom} {personnage.nom}, élue de la commune de {ville},"
    ]
    introduction = random.choice(introductions)

    # Partie principale : regret sur la fermeture ou le manque d'infrastructure
    if situation == 'supprimée':
        corps = tirer_argument_fermeture_nucleaire()
    else:
        corps = tirer_argument_manque_infrastructure()

    # Conclusion : création du site avec mention de la ville
    conclusion = tirer_argument_creation_site(ville)

    # Construction du texte
    texte = f"{introduction} a récemment pris la parole pour évoquer les défis auxquels notre territoire est confronté. {corps} Cependant, elle a également souligné une avancée importante pour l'avenir de {ville} : {conclusion}"

    return texte




def tirer_arguments_greenpeace():
    """
    Sélectionne 2 arguments aléatoires parmi les 10 arguments développés contre le prolongement d'une centrale nucléaire.
    
    :return: Deux arguments sélectionnés aléatoirement.
    """
    arguments = [
        "Le prolongement d'une centrale nucléaire augmente considérablement le risque d'accidents, notamment à cause du vieillissement des infrastructures, mettant en danger la population locale et l'environnement.",
        "Le nucléaire génère des déchets hautement radioactifs dont la gestion reste un problème non résolu. Prolonger l'activité de ces centrales aggrave cette crise écologique pour les générations futures.",
        "Investir dans la prolongation des centrales nucléaires détourne des ressources qui devraient être allouées aux énergies renouvelables, freinant ainsi la transition énergétique vers un avenir plus durable.",
        "Le coût réel du prolongement des centrales est sous-estimé. Entre les rénovations, la sécurité et la gestion des déchets, le nucléaire coûte bien plus cher que les alternatives renouvelables à long terme.",
        "La sécurité des populations est compromise par le prolongement de centrales vieillissantes, situées parfois dans des zones densément peuplées ou sensibles aux risques naturels.",
        "Les centrales nucléaires ne sont pas résilientes face aux impacts des changements climatiques, tels que les sécheresses ou inondations, qui peuvent affecter leur refroidissement et accroître les risques d'accidents.",
        "Le nucléaire centralise la production d'énergie, alors que nous devrions encourager une production décentralisée à base d'énergies renouvelables, plus résiliente et démocratique.",
        "Une majorité de citoyens expriment leur opposition au prolongement des centrales, préférant voir des investissements dans des solutions plus sûres, telles que l'éolien, le solaire et l'efficacité énergétique.",
        "Les décisions concernant le prolongement des centrales sont souvent prises sans consultation suffisante du public, ce qui nuit à la transparence et à la démocratie.",
        "Les centrales nucléaires ont un impact direct sur la biodiversité locale, en particulier sur les écosystèmes aquatiques, à cause des rejets thermiques et chimiques dans les cours d'eau."
    ]
    
    # Sélectionner aléatoirement deux arguments
    return random.sample(arguments, 2)


def tirer_arguments_greenpeace():
    arguments = [
        "Le prolongement d'une centrale nucléaire augmente considérablement le risque d'accidents, notamment à cause du vieillissement des infrastructures, mettant en danger la population locale et l'environnement.",
        "Le nucléaire génère des déchets hautement radioactifs dont la gestion reste un problème non résolu. Prolonger l'activité de ces centrales aggrave cette crise écologique pour les générations futures.",
        "Investir dans la prolongation des centrales nucléaires détourne des ressources qui devraient être allouées aux énergies renouvelables, freinant ainsi la transition énergétique vers un avenir plus durable.",
        "Le coût réel du prolongement des centrales est sous-estimé. Entre les rénovations, la sécurité et la gestion des déchets, le nucléaire coûte bien plus cher que les alternatives renouvelables à long terme.",
        "La sécurité des populations est compromise par le prolongement de centrales vieillissantes, situées parfois dans des zones densément peuplées ou sensibles aux risques naturels.",
        "Les centrales nucléaires ne sont pas résilientes face aux impacts des changements climatiques, tels que les sécheresses ou inondations, qui peuvent affecter leur refroidissement et accroître les risques d'accidents.",
        "Le nucléaire centralise la production d'énergie, alors que nous devrions encourager une production décentralisée à base d'énergies renouvelables, plus résiliente et démocratique.",
        "Une majorité de citoyens expriment leur opposition au prolongement des centrales, préférant voir des investissements dans des solutions plus sûres, telles que l'éolien, le solaire et l'efficacité énergétique."
    ]
    return random.sample(arguments, 2)

# Fonction pour générer le discours selon le statut de la centrale
def texte_greenpeace(personnage, region, statut):
    # Sélection d'une centrale nucléaire dans la région
    centrale = random.choice(region.centrales_nucleaires)
    
    # Sélection d'une personnalité locale
    personalite_locale = random.choice(region.personnalites)

    # Textes pour un discours si la centrale est supprimée
    discours_supprime = [
        f"Je me félicite aujourd'hui de la fermeture définitive de la centrale de {centrale}. C'est un jour historique pour {region.nom}.",
        f"La fermeture de la centrale de {centrale} marque un tournant décisif pour {region.nom}, un avenir plus propre nous attend.",
        f"Le démantèlement de la centrale de {centrale} est une victoire pour tous les militants et les habitants de {region.nom}.",
        f"Nous célébrons aujourd'hui la fermeture de la centrale de {centrale}, une étape essentielle vers un avenir énergétique durable.",
        f"Je suis fier de constater que la lutte a porté ses fruits avec la fermeture de la centrale de {centrale}. {region.nom} tourne une page sombre de son histoire.",
        f"La fin de l'exploitation de la centrale de {centrale} est une décision courageuse, qui garantit un avenir plus sûr pour les habitants de {region.nom}.",
        f"La fermeture de la centrale nucléaire de {centrale} est une décision majeure en faveur de la santé publique et de la protection de l'environnement dans notre région.",
        f"Aujourd'hui, nous disons adieu à une énergie du passé avec la fermeture de la centrale de {centrale}, ouvrant la voie à un avenir basé sur des énergies renouvelables pour {region.nom}."
    ]

    # Textes pour un discours si la centrale est maintenue
    discours_maintenue = [
        f"Je regrette profondément la décision de prolonger l'activité de la centrale de {centrale}. Nous continuerons la lutte pour un avenir sans nucléaire.",
        f"Le maintien de la centrale de {centrale} est une trahison envers les citoyens de {region.nom} et une entrave à la transition énergétique.",
        f"Prolonger l'activité de la centrale de {centrale} est une erreur. Nous devons nous battre pour mettre fin à cette dépendance au nucléaire.",
        f"Je suis ici aujourd'hui pour dénoncer la prolongation injustifiable de la centrale de {centrale}. Le combat pour l'avenir de {region.nom} continue.",
        f"La centrale de {centrale} reste en place, mais notre détermination à en finir avec le nucléaire reste intacte. Nous continuerons à nous battre.",
        f"Le prolongement de la centrale de {centrale} est un choix irresponsable. Nous devons résolument poursuivre notre lutte pour la fermer.",
        f"Cette décision de maintenir la centrale de {centrale} va à l'encontre de toutes les promesses faites pour une transition énergétique. Nous ne cesserons de lutter.",
        f"Le choix de prolonger la vie de la centrale de {centrale} met en péril l'avenir de {region.nom}. Nous demandons sa fermeture immédiate."
    ]
    
    # Générer deux arguments pour renforcer le discours
    arguments = tirer_arguments_greenpeace()
    
    # Structure du texte final
    if statut == "supprimée":
        discours = random.choice(discours_supprime)
        texte = f"{personnage.prenom} {personnage.nom} a pris la parole lors de la manifestation devant la centrale nucléaire de {centrale}. {discours} {arguments[0]} {arguments[1]} " \
                f"Il a tenu à rappeler que cette victoire est le résultat d'années de lutte et a salué le soutien constant de {personalite_locale}, qui a toujours défendu cette cause avec ferveur."
    else:
        discours = random.choice(discours_maintenue)
        texte = f"{personnage.prenom} {personnage.nom} s'est exprimé devant la centrale de {centrale} pour dénoncer le prolongement de son activité. {discours} {arguments[0]} {arguments[1]} " \
                f"Il a également rappelé le soutien indéfectible de {personalite_locale}, qui se tient aux côtés des citoyens dans cette lutte pour un avenir sans nucléaire."
    
    return texte



def texte_premiere_ministre(character, data, year):
    contexts = [
    "Lors d'une conférence de presse à Paris, la Première ministre a souligné les progrès significatifs de notre pays en matière de transition énergétique.",
    "Dans le cadre de la Journée mondiale de l'environnement, la Première ministre a pris la parole pour rappeler l'importance des choix énergétiques durables.",
    #"En visite dans une centrale éolienne en Bretagne, la Première ministre a évoqué les efforts du gouvernement pour atteindre ses objectifs climatiques.",
    "Au milieu des débats parlementaires sur l'énergie, la Première ministre a exposé les grandes lignes de la politique énergétique du gouvernement.",
    "À l'occasion d'un sommet sur le climat à Bombay, la Première ministre a affirmé que la France était en bonne voie pour respecter ses engagements.",
    "Dans un discours prononcé devant les jeunes, la Première ministre a encouragé l'engagement pour un avenir énergétique responsable.",
    "En réponse aux critiques sur la politique énergétique, la Première ministre a défendu les choix du gouvernement lors d'un entretien télévisé.",
    "Lors d'une visite dans une région touchée par des coupures d'électricité, la Première ministre a promis des actions concrètes pour améliorer la situation.",
    #"À l'occasion de l'ouverture d'un nouveau parc éolien offshore, la Première ministre a célébré l'avancement des projets énergétiques.",
    "En réponse à la hausse des émissions de CO2, la Première ministre a détaillé les nouvelles mesures mises en place par le gouvernement.",
    "Lors d'un forum international sur l'énergie renouvelable, la Première ministre a plaidé pour une coopération accrue entre les nations.",
    "Dans un cadre universitaire, la Première ministre a souligné le rôle crucial de l'innovation dans la transition vers des énergies propres.",
    "En participant à une table ronde avec des acteurs du secteur énergétique, la Première ministre a souligné l'importance de l'engagement collectif.",
    "À l'occasion de la publication d'un rapport sur le climat, la Première ministre a appelé à une action immédiate pour lutter contre le changement climatique.",
    "Dans un entretien avec des journalistes, la Première ministre a partagé sa vision d'une France plus verte et plus durable à l'horizon 2030."
]
    
    # Sélectionne un contexte aléatoire
    context = random.choice(contexts)

    # Textes de l'article
    article_templates = [
    f"{context} Dans une déclaration récente et marquante, {character.prenom} {character.nom}, Première ministre et membre éminent de {character.affiliation}, a clairement exprimé que d'ici {year}, la France s'engage à atteindre un équilibre ENR/Nucléaire de {data.equilibre_enr_nucleaire}%. Pour réaliser cet objectif ambitieux, nous prévoyons d'installer une puissance totale de {data.puissance_photovoltaique_totale} MW en photovoltaïque, ainsi que {data.puissance_eolienne_totale} MW en éolien, renforçant ainsi notre capacité à produire une énergie durable. En outre, elle a souligné l'importance cruciale de réduire nos émissions de CO2, qui se chiffrent actuellement à un total alarmant de {data.emissions_co2} tonnes, une tâche que nous devons aborder de manière urgente et concertée.",
    
    f"{context} Au cours de son intervention, {character.prenom} {character.nom}, agissant en tant que Première ministre au service de {character.affiliation}, a mis en lumière l'objectif ambitieux et déterminé du gouvernement de garantir un mix énergétique stable et durable. À l'horizon de {year}, nous nous engageons fermement à atteindre un équilibre ENR/Nucléaire de {data.equilibre_enr_nucleaire}%. Dans cette optique, nous visons une puissance photovoltaïque impressionnante de {data.puissance_photovoltaique_totale} MW et une puissance éolienne tout aussi significative de {data.puissance_eolienne_totale} MW. La réduction des émissions de CO2 à un niveau de {data.emissions_co2} tonnes est non seulement souhaitée, mais également essentielle pour assurer notre avenir collectif et préserver notre planète pour les générations futures.",
    
    f"{context} En se tenant devant des journalistes attentifs et engagés, {character.prenom} {character.nom}, Première ministre, a exprimé avec conviction la volonté déterminée du gouvernement de promouvoir un mix énergétique diversifié et équilibré. D'ici {year}, la France prévoit d'atteindre un équilibre ENR/Nucléaire de {data.equilibre_enr_nucleaire}%. Avec une puissance installée impressionnante de {data.puissance_photovoltaique_totale} MW en photovoltaïque et {data.puissance_eolienne_totale} MW en éolien, l'objectif est clair et ambitieux : réduire nos émissions de CO2 à un niveau acceptable de {data.emissions_co2} tonnes, afin de garantir un environnement sain pour tous.",
    
    f"{context} {character.prenom} {character.nom}, en tant que Première ministre engagée et responsable, a déclaré avec fermeté que la transition énergétique est une priorité absolue pour le gouvernement. D'ici {year}, nous visons à établir un équilibre ENR/Nucléaire de {data.equilibre_enr_nucleaire}%. Avec une puissance photovoltaïque de {data.puissance_photovoltaique_totale} MW et une capacité éolienne de {data.puissance_eolienne_totale} MW, il est impératif que nous réduisions nos émissions de CO2, qui sont actuellement évaluées à {data.emissions_co2} tonnes, et ce, pour le bien-être de notre écosystème.",
    
    f"{context} Dans un discours passionné et inspirant, {character.prenom} {character.nom} a révélé les objectifs stratégiques et cruciaux du gouvernement pour l'année {year}. Nous aspirons à un équilibre ENR/Nucléaire de {data.equilibre_enr_nucleaire}%, avec une puissance photovoltaïque installée de {data.puissance_photovoltaique_totale} MW et une capacité éolienne de {data.puissance_eolienne_totale} MW. La lutte contre les émissions de CO2, actuellement chiffrées à {data.emissions_co2} tonnes, représente un engagement fort et nécessaire pour notre génération, ainsi qu'une obligation morale envers nos enfants.",
    
    f"{context} À l'occasion de sa déclaration, {character.prenom} {character.nom} a discuté des choix énergétiques futurs et des décisions stratégiques du pays. En {year}, la France s'engage à maintenir un équilibre ENR/Nucléaire de {data.equilibre_enr_nucleaire}%. Nous visons à installer une impressionnante capacité de {data.puissance_photovoltaique_totale} MW en photovoltaïque et {data.puissance_eolienne_totale} MW en éolien, tout en s'efforçant de réduire nos émissions de CO2 à un niveau soutenable de {data.emissions_co2} tonnes, dans le cadre d'une démarche de développement durable.",
    
    f"{context} En s'adressant au public avec passion, {character.prenom} {character.nom} a présenté une vision claire et ambitieuse pour le mix énergétique de la France. Pour {year}, l'objectif est d'atteindre un équilibre ENR/Nucléaire de {data.equilibre_enr_nucleaire}%. La puissance photovoltaïque installée devrait atteindre un total de {data.puissance_photovoltaique_totale} MW, tandis que la puissance éolienne devrait atteindre {data.puissance_eolienne_totale} MW, avec un objectif de réduction des émissions de CO2 à {data.emissions_co2} tonnes, un élément fondamental de notre stratégie de transition énergétique.",
    
    f"{context} Lors de son allocution, {character.prenom} {character.nom} a insisté avec force sur l'importance de la transition énergétique pour l'avenir de notre pays et de notre planète. En {year}, le gouvernement vise à établir un équilibre ENR/Nucléaire de {data.equilibre_enr_nucleaire}%. Avec une puissance photovoltaïque de {data.puissance_photovoltaique_totale} MW et une capacité éolienne de {data.puissance_eolienne_totale} MW, nous devons également réduire nos émissions de CO2, qui sont actuellement estimées à {data.emissions_co2} tonnes, pour laisser un héritage durable aux futures générations.",
    
    f"{context} Dans un cadre dynamique et engageant, {character.prenom} {character.nom} a présenté les initiatives du gouvernement visant à transformer le mix énergétique de la France. À l'horizon de {year}, nous viserons un équilibre ENR/Nucléaire de {data.equilibre_enr_nucleaire}%. La France prévoit d'installer une impressionnante capacité de {data.puissance_photovoltaique_totale} MW en photovoltaïque et {data.puissance_eolienne_totale} MW en éolien, tout en s'engageant à réduire les émissions de CO2 à un niveau de {data.emissions_co2} tonnes, dans le but d'assurer un avenir énergétique propre et respectueux de l'environnement."
]

    # Sélectionne un modèle de texte aléatoire
    article_text = random.choice(article_templates)
    
    return article_text

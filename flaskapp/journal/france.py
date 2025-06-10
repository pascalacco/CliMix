from flaskapp.journal.journal import Region, Personnage, DataForGazette

france = Region(
    nom="France",
    prefecture="Paris",
    sous_prefectures=["Paris"],
    villes_cotieres=[],
    foires_agricoles=[],
    personnalites=[],  # Personnalités nées après 1970
    elus=[],
    centrales_nucleaires=[],
    especes_terrestres=[],
    especes_marines=[]
)

# Exemple de région Occitanie
occitanie = Region(
    nom="Occitanie",
    prefecture="Toulouse",
    sous_prefectures=["Albi", "Carcassonne", "Auch", "Mende", "Foix", "Montpellier"],
    villes_cotieres=["Sète", "Narbonne", "Perpignan", "Béziers"],
    foires_agricoles=["Foire agricole de Tarbes", "Foire agricole de Béziers", "Foire agricole de Cahors", "Foire agricole de Perpignan", "Foire agricole de Carcassonne"],
    personnalites=["Bigflo", "Oli", "Jain", "Clara Luciani", "Hoshi", "Gambi", "Angèle"],
    elus=["Carole Delga", "Jean-Luc Moudenc", "Philippe Saurel", "Anne-Yvonne Le Dain", "Damien Alary"],
    centrales_nucleaires=["Golfech"],
    especes_terrestres=["Loup gris", "Loutre d'Europe", "Cigogne blanche", "Lynx boréal", "Papillon Grand Mars changeant"],
    especes_marines=["Tortue Caouanne", "Grand dauphin", "Raie pastenague", "Requin pèlerin", "Poisson-lune"]
)

bretagne = Region(
    nom="Bretagne",
    prefecture="Rennes",
    sous_prefectures=["Saint-Brieuc", "Quimper", "Vannes", "Lorient"],
    villes_cotieres=["Brest", "Saint-Malo", "Douarnenez", "Concarneau", "Quiberon", "Vannes"],
    foires_agricoles=["Foire de Rennes", "Foire de Quimper", "Foire de Pontivy", "Foire de Guingamp", "Foire de Lorient"],
    personnalites=["Christine and the Queens", "Brieuc Yannic", "Coline Rio", "Rilès", "Suzane"],
    elus=["Loïg Chesnais-Girard", "Nathalie Appéré", "François Cuillandre", "Jacques Le Nay", "Paul Molac"],
    centrales_nucleaires=["Brennilis"],
    especes_terrestres=["Cerf élaphe", "Hérisson européen", "Renard roux", "Fouine", "Papillon Flambé"],
    especes_marines=["Phoque gris", "Dauphin commun", "Raie bouclée", "Homard européen", "Orque"]
)


# Normandie
normandie = Region(
    nom="Normandie",
    prefecture="Rouen",
    sous_prefectures=["Caen", "Évreux", "Saint-Lô", "Alençon"],
    villes_cotieres=["Le Havre", "Dieppe", "Cherbourg", "Deauville", "Granville"],
    foires_agricoles=["Foire de Lessay", "Foire de Saint-Romain", "Foire de Pont-Audemer", "Foire de Caen", "Foire de Lisieux"],
    personnalites=["Orelsan", "Juliette Armanet", "Dinos", "Manon Amellot", "Jérémy Frérot"],
    elus=["Hervé Morin", "Nicolas Mayer-Rossignol", "Joël Bruneau", "Sophie Gaugain", "Philippe Bas"],
    centrales_nucleaires=["Paluel", "Penly", "Flamanville"],
    especes_terrestres=["Blaireau européen", "Chouette effraie", "Cerf élaphe", "Hérisson européen", "Martre des pins"],
    especes_marines=["Phoque veau-marin", "Dauphin commun", "Raie lisse", "Crabe tourteau", "Moule bleue"]
)


# Pays de la Loire
pays_de_la_loire = Region(
    nom="Pays de la Loire",
    prefecture="Nantes",
    sous_prefectures=["Angers", "Le Mans", "La Roche-sur-Yon", "Laval"],
    villes_cotieres=["Saint-Nazaire", "Les Sables-d'Olonne", "Pornic", "La Baule", "Le Croisic"],
    foires_agricoles=["Foire des Sables-d'Olonne", "Foire de Nantes", "Foire de Saumur", "Foire de Laval", "Foire de Cholet"],
    personnalites=["Eddy de Pretto", "Pomme", "Vald", "Alice Et Moi", "Nekfeu"],
    elus=["Christelle Morançais", "Johanna Rolland", "Stéphane Le Foll", "Matthieu Orphelin", "Franck Louvrier"],
    centrales_nucleaires=["Chinon"],
    especes_terrestres=["Cerf sika", "Chouette chevêche", "Renard roux", "Lapin de garenne", "Faucon crécerelle"],
    especes_marines=["Grand dauphin", "Requin pèlerin", "Langoustine", "Crabe vert", "Huître plate"]
)




# %%
centre_val_de_loire = Region(
    nom="Centre-Val de Loire",
    prefecture="Orléans",
    sous_prefectures=["Tours", "Bourges", "Châteauroux", "Chartres", "Blois"],
    villes_cotieres=[],  # Pas de villes côtières dans cette région
    foires_agricoles=["Foire de Châteauroux", "Foire de Tours", "Foire de Bourges", "Foire d'Orléans", "Foire de Chartres"],
    personnalites=["Camille Lellouche", "Norman Thavaud", "Vianney", "Slimane", "Angèle", "Aloïse Sauvage"],  # Personnalités nées après 1990
    elus=["François Bonneau", "Caroline Janvier", "Jean-Patrick Gille", "Isabelle Gaudron", "Marc Gricourt"],
    centrales_nucleaires=["Saint-Laurent-des-Eaux", "Dampierre", "Belleville-sur-Loire"],
    especes_terrestres=["Biche", "Chevreuil", "Renard roux", "Hérisson", "Faucon crécerelle"],
    especes_marines=[]  # Pas d'espèces marines dans cette région
)

hauts_de_france = Region(
    nom="Hauts-de-France",
    prefecture="Lille",
    sous_prefectures=["Amiens", "Arras", "Beauvais", "Saint-Quentin", "Laon"],
    villes_cotieres=["Calais", "Boulogne-sur-Mer", "Dunkerque", "Le Touquet", "Berck"],
    foires_agricoles=["Foire de Lille", "Foire d'Amiens", "Foire de Beauvais", "Foire de Laon", "Foire de Saint-Quentin"],
    personnalites=["Louane", "Orelsan", "Dadju", "Nekfeu", "Aurel", "Ilona Mitrecey"],  # Personnalités nées après 1990
    elus=["Xavier Bertrand", "Martine Aubry", "François Ruffin", "Natacha Bouchart", "Karima Delli"],
    centrales_nucleaires=["Gravelines"],
    especes_terrestres=["Cerf élaphe", "Lièvre d'Europe", "Renard roux", "Chouette hulotte", "Belette"],
    especes_marines=["Phoque veau-marin", "Moule", "Crabe vert", "Dauphin commun", "Sole commune"]
)
provence_alpes_cote_d_azur = Region(
    nom="Provence-Alpes-Côte d'Azur",
    prefecture="Marseille",
    sous_prefectures=["Nice", "Toulon", "Avignon", "Digne-les-Bains", "Gap"],
    villes_cotieres=["Cannes", "Antibes", "Saint-Tropez", "Toulon", "Nice", "Marseille"],
    foires_agricoles=["Foire de Brignoles", "Foire de Gap", "Foire de Manosque", "Foire de Cavaillon", "Foire de Grasse"],
    personnalites=["Kendji Girac", "Amel Bent", "Vitaa", "Soprano", "Jul", "Eva Queen"],  # Personnalités nées après 1990
    elus=["Renaud Muselier", "Christian Estrosi", "Martine Vassal", "Eric Ciotti", "Sophie Joissains"],
    centrales_nucleaires=["Tricastin"],
    especes_terrestres=["Loup gris", "Sanglier", "Aigle royal", "Mouflon", "Lézard ocellé"],
    especes_marines=["Grand dauphin", "Mérou", "Thon rouge", "Daurade royale", "Raie manta"]
)


# %%
alsace = Region(
    nom="Alsace",
    prefecture="Strasbourg",
    sous_prefectures=["Colmar", "Mulhouse"],
    villes_cotieres=[],  # Pas de villes côtières
    foires_agricoles=["Foire Européenne de Strasbourg", "Foire aux Vins d'Alsace", "Foire de Mulhouse"],
    personnalites=["Clara Luciani", "Eddy de Pretto", "Lous and The Yakuza", "Soprano", "Angèle"],
    elus=["Brigitte Klinkert", "Frédéric Bierry", "Léa Soler", "Jean Rottner", "Mélanie Boulanger"],
    centrales_nucleaires=["Fessenheim"],  # Centrale fermée en 2020
    especes_terrestres=["Cerf élaphe", "Blaireau européen", "Sanglier", "Faucon crécerelle", "Renard roux"],
    especes_marines=["Dauphin commun", "Bar", "Sole", "Sardine", "Sardine de l'Atlantique"]
)

corse = Region(
    nom="Corse",
    prefecture="Ajaccio",
    sous_prefectures=["Bastia", "Corte"],
    villes_cotieres=["Porto-Vecchio", "Calvi", "Ajaccio"],
    foires_agricoles=["Foire de Porto-Vecchio", "Foire de Bastia", "Foire de Vico"],
    personnalites=["Gauvain Sers", "Angèle", "Clara Luciani", "Louane", "Pomme"],
    elus=["Gilles Simeoni", "Marie-Antoinette Santoni", "Jean-Félix Acquaviva", "Paul Giacobbi", "Jean-Guy Talamoni"],
    centrales_nucleaires=[],  # Pas de centrales nucléaires en Corse
    especes_terrestres=["Moufette", "Chèvre de Corse", "Cigogne noire", "Groupe de sangliers", "Serin cini"],
    especes_marines=["Mérou", "Dauphin commun", "Tortue verte", "Poisson-lune", "Langouste"]
)

bourgogne_franche_comte = Region(
    nom="Bourgogne-Franche-Comté",
    prefecture="Dijon",
    sous_prefectures=["Besançon", "Chalon-sur-Saône", "Nevers"],
    villes_cotieres=[],  # Pas de villes côtières
    foires_agricoles=["Foire de Dijon", "Foire de Chalon-sur-Saône", "Foire de Besançon"],
    personnalites=["Léa Seydoux", "Christine and The Queens", "Jain", "Bigflo et Oli", "Orelsan"],
    elus=["Marie-Guite Dufay", "Jacques Lambert", "Nathalie Koenders", "Benoît Coquart", "Pierre Mehaignerie"],
    centrales_nucleaires=["Bugey"],  # Centrales situées dans la région
    especes_terrestres=["Cèdre de l'Atlas", "Cerf élaphe", "Aigle royal", "Lynx boréal", "Chamois"],
    especes_marines=["Dauphin", "Bar", "Sole", "Sardine", "Requin"]
)
auvergne_rhone_alpes = Region(
    nom="Auvergne-Rhône-Alpes",
    prefecture="Lyon",
    sous_prefectures=["Clermont-Ferrand", "Saint-Étienne", "Grenoble", "Annecy", "Chambéry"],
    villes_cotieres=[],  # Pas de villes côtières
    foires_agricoles=["Foire de Clermont-Ferrand", "Foire de Lyon", "Foire de Saint-Étienne", "Foire de la gastronomie de Tain-l'Hermitage"],
    personnalites=["Louane", "Soprano", "Julien Clerc", "Camille Lellouche", "Orelsan"],
    elus=["Laurent Wauquiez", "Nathalie Delattre", "Karine Giordano", "Fabienne Léger", "Jean-Jack Queyranne"],
    centrales_nucleaires=["Bugey", "Saint-Alban", "Cruas"],
    especes_terrestres=["Chamois", "Marmotte", "Aigle royal", "Loup gris", "Cerf élaphe"],
    especes_marines=["Truite fario", "Saumon atlantique", "Brochet", "Silure glane"]
)

ile_de_france = Region(
    nom="Île-de-France",
    prefecture="Paris",
    sous_prefectures=["Boulogne-Billancourt", "Saint-Denis", "Versailles", "Nanterre", "Créteil"],
    villes_cotieres=[],  # Pas de villes côtières
    foires_agricoles=["Foire de Paris", "Foire de la gastronomie", "Fête de l'agriculture"],
    personnalites=["Kendji Girac", "Angèle", "Orelsan", "Lyna Mahyem", "Jain"],
    elus=["Valérie Pécresse", "Anne Hidalgo", "Geoffroy Boulard", "Gérald Darmanin", "Patrick Ollier"],
    centrales_nucleaires=["Chooz", "Civaux", "Fessenheim"],
    especes_terrestres=["Sanglier", "Renard", "Écureuil", "Hérisson", "Lapin de garenne"],
    especes_marines=[]
)






nouvelle_aquitaine = Region(
    nom="Nouvelle Aquitaine",
    prefecture="Bordeaux",
    sous_prefectures=["Libourne", "Langon", "Lesparre-Médoc"],
    villes_cotieres=["La Rochelle", "Arcachon", "Royan"],
    foires_agricoles=["Foire de Bordeaux"],
    personnalites=["François Mauriac", "Michel de Montaigne"],
    elus=["Jean-Luc Gleyze", "Renaud Lagrave"],
    centrales_nucleaires=["Blaye", "Golfech"],
    especes_terrestres=["Cerf", "Sanglier"],
    especes_marines=["Sardine", "Thon"]
)



dictionnaire_regions = {
    "fr": france,
    "occ": occitanie,
    "bre": bretagne,
    "nor": normandie,
    "pll": pays_de_la_loire,
    "naq" : nouvelle_aquitaine,
    "idf" : ile_de_france,
    "ara" : auvergne_rhone_alpes,
    "bfc" : bourgogne_franche_comte,
    "cor" : corse,
    "pac" : provence_alpes_cote_d_azur,
    "est" : alsace,
    "hdf" : hauts_de_france,
    "cvl" : centre_val_de_loire
}


# Exemple de création d'un objet DataForGazette
france_data = DataForGazette(
    emissions_co2=1234.56,
    equilibre_enr_nucleaire=75,
    regions_photovoltaiques=["occ"],
    regions_eolien_onshore=["nor", "bre"],
    regions_eolien_offshore=["pll"],
    puissance_photovoltaique_tour=500,
    puissance_photovoltaique_totale=15000,
    puissance_eolienne_tour=1200,
    puissance_eolienne_totale=25000,
    regions_suppression_nucleaire=["occ"],
    regions_sous_production=["bre"],
    regions_methaniseur=["bre", "nor"],
    regions_centrales_nucleaires=["pll", "occ"]  # Exemples de régions avec centrales nucléaires
)

"""
personnages = [Personnage("Dossal", "Charles", "agriculteur", "Paysans en colère")]
personnages.append( Personnage("Rondepierre", "Aude", "activiste", "La nature avant les profits"))
personnages.append( Personnage("Cros", "Marion", "PDG solaire", "Power Solar"))
personnages.append( Personnage("Lachaize", "Sébastien", "PDG éolien", "Wind Power"))
personnages.append( Personnage("Delga", "Carole", "élue", "Parti Socialiste"))
personnages.append( Personnage("Acco", "Pascal", "greenpeace", "greenpeace"))
personnages.append( Personnage(nom='Swift', prenom='Taylor', role='première ministre', affiliation='La République En Marche'))
"""

if __name__ == "__main__":


    # Exemple d'accès à une région par son nom
    region_choisie = dictionnaire_regions.get("occ")


    const maps = {
        "France": [["hdf", "Hauts-de-France"],
            ["bre", "Bretagne"],
            ["nor", "Normandie"],
            ["idf", "Ile-de-France"],
            ["est", "Grand Est"],
            ["cvl", "Centre-Val de Loire"],
            ["pll", "Pays de la Loire"],
            ["bfc", "Bourgogne-Franche-Comté"],
            ["naq", "Nouvelle-Aquitaine"],
            ["ara", "Auvergne-Rhône-Alpes"],
            ["occ", "Occitanie"],
            ["pac", "Provence-Alpes-Côte d'Azur"],
            ["cor", "Corse"]]
    };

    const regConvert = {
        "hdf": "Hauts-de-France",
        "bre": "Bretagne",
        "nor": "Normandie",
        "idf": "Ile-de-France",
        "est": "Grand Est",
        "cvl": "Centre-Val de Loire",
        "pll": "Pays de la Loire",
        "bfc": "Bourgogne-Franche-Comté",
        "naq": "Nouvelle-Aquitaine",
        "ara": "Auvergne-Rhône-Alpes",
        "occ": "Occitanie",
        "pac": "Provence-Alpes-Côte d'Azur",
        "cor": "Corse"
    }

    const pions = [["eolienneON", "Eol. onshore"],
        ["eolienneOFF", "Eol. offshore"],
        ["panneauPV", "Solar PV"],
        ["centraleNuc", "Ancien nuc."],
        ["EPR2", "EPR 2"],
        ["methanation", "Power 2 Gas    "],
        ["biomasse", "Biomasse"]
    ];

    const pionsConvert = {
        "eolienneON": "Eoliennes on.",
        "eolienneOFF": "Eoliennes off.",
        "panneauPV": "Panneaux PV",
        "centraleNuc": "Ancien nuc.",
        "EPR2": "EPR 2",
        "methanation": "Méthanation",
        "biomasse": "Biomasse"
    }

    const aleas = ["", "MEGC1", "MEGC2", "MEGC3", "MEMFDC1", "MEMFDC2", "MEMFDC3",
        "MECS1", "MECS2", "MECS3", "MEVUAPV1", "MEVUAPV2", "MEVUAPV3",
        "MEMDA1", "MEMDA2", "MEMDA3", "MEMP1", "MEMP2", "MEMP3",
        "MEGDT1", "MEGDT2", "MEGDT3"
    ];

    const politiques = ["", "CPA1", "CPA2", "CPB1", "CPB2", "CPC1", "CPC2",
        "CPD1", "CPD2", "CPE1", "CPE2", "CPF1", "CPF2"];

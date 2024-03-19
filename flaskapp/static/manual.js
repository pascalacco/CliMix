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

const pions = [["eolienneON", "Eoliennes on."],
    ["eolienneOFF", "Eoliennes off."],
    ["panneauPV", "Panneaux PV"],
    ["centraleNuc", "Ancien nuc."],
    ["EPR2", "EPR 2"],
    ["methanation", "Méthanation"],
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

function btnCallbacks(plus, minus, nb) {
    minus.click(() => {
        nb.val((parseInt(nb.val()) > 0 ? parseInt(nb.val()) - 1 : 0));
    });

    plus.click(() => {
        nb.val((parseInt(nb.val()) < 100 ? parseInt(nb.val()) + 1 : 100));
    });
}

function initContent(map) {
    let divStr = "";

    for (const reg of maps[map]) {
        divStr += `<div class="region" id="${reg[0]}"> <h3 class="row mt-5 ps-2 bg-info rounded bg-opacity-50 justify-content-center">${reg[1]}</h3>`;
        for (const pion of pions) {
            divStr +=
                `<div class="row justify-content-around">

                    <div class="col-2 mt-2">${pion[1]}</div>

                    <div class="col-8 mt-2">
                        <div class="row justify-content-end">
                            <div class="form-outline col-4">
                                <input value="0" min="0" max="100" type="number" id="${reg[0]}_${pion[0]}" class="form-control"/>
                               
                            </div>
                            <div class="col-4">
                             <button class="btn btn-basic col-2" type="button" id="${reg[0]}_${pion[0]}_minus">➖</button>
                                <button class="btn btn-basic col-2" type="button" id="${reg[0]}_${pion[0]}_plus">➕</button>
                             </div>
                            
                        </div>
                    </div>

                </div>`;
        }
        divStr += "</div>";
    }

    $("#mid").html(divStr);

    for (const reg of maps["France"]) {
        for (const pion of pions) {
            minusBtn = $(`#${reg[0]}_${pion[0]}_minus`);
            plusBtn = $(`#${reg[0]}_${pion[0]}_plus`);
            nb = $(`#${reg[0]}_${pion[0]}`);

            btnCallbacks(plusBtn, minusBtn, nb);
        }
    }
}

function displayError(reason, details) {
    let msg;
    const modal = new bootstrap.Modal($("#errModal"));

    switch (reason) {
        case "err":
            msg = "Une erreur inattendue est survenue.";
            break;
        case "http":
            msg = "Une erreur est survenue avec le serveur.";
            break;
        case "errAnnee":
            msg = `L'année sélectionnée ne correpond pas au tour actuel (valeur attendue: ${details}).`;
            break;
        case "errStock":
            msg = `Vous ne pouvez pas enlever de batteries (valeur minimale: ${details}).`;
            break;
        case "errCarte":
            msg = `Vous ne pouvez pas changer de carte au milieu d'une partie (carte actuelle: ${details}).`;
            break;
        case "errSol":
            msg = `Vous avez placé trop de ${details[1]} en ${details[0]} (maximum: ${details[2]}).`;
            break;
        case "errNuc":
            msg = `La crise sociale en cours vous empêche de placer plus de réacteurs nucléaires (vous en avez ajouté ${details}).`;
            break;
        case "errMixInit":
            msg = "Votre mix ne correspond pas au mix initial imposé. Veuillez vérifier le nombre de réacteurs dans chaque région.";
            break;
        default:
            break;
    }

    $("#errorMsg").html(msg);
    modal.toggle();
}

function saveData() {
    let err = 0;
    let result;
    const data = {};
    const stockStr = $("#stock").val();
    const stock = parseFloat(stockStr);

    if ($("#carte").val() == "default") {
        alert("Veuillez sélectionner une carte");
        err = 1;

    } else if ($("#annee").val() == "default") {
        alert("Veuillez sélectionner une année");
        err = 1;

    } else if (!(aleas.includes($("#alea").val()))) {
        alert("Le code aléa est invalide");
        err = 1;

    } else if (stockStr == "" || stock < 1 || stock > 10 || !(Number.isInteger(stock))) {
        alert("Veuillez entrer une valeur entière de stock entre 1 et 10");
        err = 1;

    } else {
        data["actif"] = true;
        data["carte"] = "France";
        data["annee"] = parseInt($("#turn")[0].innerText);
        data["stock"] = parseInt($("#stock").val());
        data["alea"] = $("#alea").val();
        data["politique"] = "";

        for (const reg of maps["France"]) {
            data[reg[0]] = {};
            for (const p of pions) {
                const str = $(`#${reg[0]}_${p[0]}`).val();
                const nb = parseFloat(str);
                if (str == "" || nb < 0 || nb > 100 || !(Number.isInteger(nb))) {
                    alert("Veuillez entrer des nombres entiers entre 0 et 100 seulement.");
                    err = 1;
                }
                data[reg[0]][p[0]] = nb;
            }
        }
    }

    result = err ? false : JSON.stringify(data);
    return result;
}

function fillPage(mixData) {
    if (!mixData.actif) {
        $("#carte").val("default");
        $("#annee").val("default");
        $("#stock").val("1");
        $("#alea").val("");
        $("#politique").val("");
    } else {
        $("#carte").val(mixData.carte);
        $("#annee").val((Number(mixData.annee) + 5).toString());
        $("#stock").val(mixData.stock.toString());
        $("#alea").val(mixData.alea);
        $("#politique").val(mixData.politique);

        initContent(mixData.carte);

        for (const reg of maps[mixData.carte]) {
            for (const pion of pions) {
                $(`#${reg[0]}_${pion[0]}`).val(mixData[reg[0]][pion[0]]);
            }
        }

        $("#mid").hide();
        $("#bot").hide();
        $("#mid").fadeIn();
        $("#bot").fadeIn();
    }

}


function calculer() {
    const dataProd = saveData();

    if (dataProd != false) {
        $('#btnCalculer').html('<span class="spinner-border spinner-border-sm"></span>&nbsp;&nbsp;Chargement...');
        exitConfirm = false;
        $.ajax({
            url: "/production",
            type: "POST",
            data: dataProd,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data, textStatus, jqXHR) {
                $('#btnCalculer').html('Valider');
                if (data[0] == "success") {
                    location.href = "/results";
                } else {
                    displayError(data[0], data[1]);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                $('#btnCalculer').html('Valider');
                displayError("http", null);
            }
        });
    }
}


$(function () {


    let exitConfirm = false; // METTRE A TRUE LORS DU DEPLOIEMENT

    onbeforeunload = function () {
        if (exitConfirOupsm) return "Etes-vous sûr(e) de vouloir quitter cette page ? Vos modifications seront perdues."
    }


    console.log("entre dans entree manuelle")

    let mixData = null;


    $("#carte").change(() => {
        const val = $("#carte").val();
        if (val != "default") {
            initContent(val);
            $("#mid").hide();
            $("#bot").hide();
            $("#mid").fadeIn();
            $("#bot").fadeIn();
        }
    });

    $('.backHome').click(() => {
        location.href = "/";
    });
    $("btnCalculer").click(calculer);

    // DEBUT EXECUTION PAGE
    console.log("je suis 703")
    $.ajax({
        url: "/get_mix",
        type: "GET",
        dataType: "json",
        success: function (data, textStatus, jqXHR) {
            mixData = data;
            fillPage(mixData);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            displayError("http");
        }
    });
    $("#top").fadeIn();

});

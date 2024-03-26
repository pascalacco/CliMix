$(function () {


    let exitConfirm = false; // METTRE A TRUE LORS DU DEPLOIEMENT

    onbeforeunload = function () {
        if (exitConfirOupsm) return "Etes-vous sûr(e) de vouloir quitter cette page ? Vos modifications seront perdues."
    }


    let mixData = null;
    let evenements = null;

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
            divStr += `<div class="region" id="${reg[0]}"> <h3 class="row mt-1  ps-3 bg-primary rounded bg-opacity-50 ">${reg[1]}</h3>`;
            for (const pion of pions) {
                divStr += `<div class="row align-items-top">
                        <div class="col-auto mt-1">${pion[1]}</div>
                        <div class="col-auto mt-1">
                            <input value="0" min="0" max="10" type="number" id="${reg[0]}_${pion[0]}" class="form-control-sm"/>
                        </div>
                        <div class="col-auto mt-1">
                            <button class="btn btn-basic col-1" type="button" id="${reg[0]}_${pion[0]}_minus">➖</button>
                            <button class="btn btn-basic col-1" type="button" id="${reg[0]}_${pion[0]}_plus">➕</button>
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

        if ($("#annee").val() == "default") {
            alert("Veuillez sélectionner une année");
            err = 1;

        } else if (!(aleas.includes($("#alea").val()))) {
            alert("Le code aléa est invalide");
            err = 1;

            /* }  else if (!(politiques.includes($("#politique").val()))) {
                alert("Le code politique est invalide");
                err = 1;
            */
        } else if (stockStr == "" || stock < 1 || stock > 10 || !(Number.isInteger(stock))) {
            alert("Veuillez entrer une valeur entière de stock entre 1 et 10");
            err = 1;

        } else {
            data["actif"] = true;
            data["carte"] = "France";
            data["annee"] = parseInt($("#annee").val());
            data["stock"] = parseInt($("#stock").val());
            data["alea"] = $("#alea").val();
            //data["politique"] = $("#politique").val();
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

    function fillPage() {
        let annee
        if (!mixData.actif) {
            $("#carte").val(mixData.carte);
            annee = Number(mixData.annee) + 5;
            $("#annee").val(annee.toString());
            $("#stock").val(mixData.stock.toString());
            $("#alea").val(aleas[Math.floor(Math.random() * aleas.length)]);
            //$("#politique").val("");
        } else {
            $("#carte").val(mixData.carte);
            annee = Number(mixData.annee);
            $("#annee").val(annee.toString());
            $("#stock").val(mixData.stock.toString());
            if (mixData.alea == "") {
                $("#alea").val(aleas[Math.floor(Math.random() * aleas.length)]);
            } else {
                $("#alea").val(mixData.alea);
            }
        }
        let replace = null;
        if (annee == "2030") {
            replace = []
        } else {
            replace = evenements[annee - 5];
        }

        if (replace.length > 0) {
            let replaceStr = "<h6>Des unitées sont en fin de vie :</h6>";
            for (const i of replace) {
                replaceStr += `${i[0]} ${pionsConvert[i[1]]} en ${regConvert[i[2]]}</br>`;
            }
            $("#replaceInfo").html(replaceStr + '<h6 class="container text-primary">+0 = prolonger et -1 = démanteler </h6>');
        }
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

    $('#computeResults').click(() => {
        const dataProd = saveData();

        if (dataProd != false) {
            $('#computeResults').html('<span class="spinner-border spinner-border-sm"></span>&nbsp;&nbsp;Chargement...');
            exitConfirm = false;
            $.ajax({
                url: "/production",
                type: "POST",
                data: dataProd,
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function (data, textStatus, jqXHR) {
                    $('#computeResults').html('Valider');
                    if (data[0] == "success") {
                        location.href = "/results";
                    } else {
                        displayError(data[0], data[1]);
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    $('#computeResults').html('Valider');
                    displayError("http", null);
                }
            });
        }
    });


    // DEBUT EXECUTION PAGE
    $.ajax({
        url: "/get_events", type: "GET", dataType: "json", success: function (data, textStatus, jqXHR) {
            evenements = data;
            $.ajax({
                url: "/get_mix", type: "GET", dataType: "json", success: function (data, textStatus, jqXHR) {
                    mixData = data;
                    fillPage();
                }, error: function (jqXHR, textStatus, errorThrown) {
                    displayError("http");
                }
            });
        }, error: function (jqXHR, textStatus, errorThrown) {
            displayError("http");
        }
    });

    $("#top").fadeIn();


});

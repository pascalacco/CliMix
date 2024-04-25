function displayError(reason, details) {
    let msg;
    const modal = new bootstrap.Modal($("#errModal"));

    switch (reason) {
        case "err":
            msg = details;
            break;
        case "http":
            msg = details;
            break;
        case "errJeu":
            msg = details
            break;
        default:
            msg = details
            break;
    }

    $("#errorMsg").html(msg);
    modal.toggle();
}


function recup(actions) {
    let err = false;
    let mesg = ''
    for (const reg in unites) {
        for (const pion in unites[reg]) {
            var unit_fin = document.getElementById(`${reg}_${pion}_fin`);
            if (unit_fin) {
                if (unit_fin.checkValidity(unit_fin.value)) {
                    for (const an in actions['regions'][reg][pion]) {
                        if ((actions['regions'][reg][pion][an]['action'] == "?") || (actions['regions'][reg][pion][an]['action'] == "-")) {
                            actions['regions'][reg][pion][an]['valeur'] = Number(unit_fin.value);
                            actions['regions'][reg][pion][an]['action'] = "-";
                        }

                    }

                } else {
                    if (unit_fin.value == '') {
                        mesg += `Cliquez dans la région ${reg_convert[reg]} et sélectionnez un choix pour  l'unité ${pion_convert[pion]} en fin de vie!<br>`;

                    } else {
                        mesg += `La valeur ${unit_fin.value} saisie dans la région ${reg_convert[reg]} pour  l'unité ${pion_convert[pion]} est incorrecte!<br> Débile(s) ! <br> je l'efface pour vous. <br>`;
                        unit_fin.value = ""
                    }
                    err = true;

                }
            }
            var unit_nouv = document.getElementById(`${reg}_${pion}_nouv`);

            if (unit_nouv) {
                if (unit_nouv.checkValidity(unit_nouv.value)) {
                    if (Number(unit_nouv.value) !== 0) {
                        actions['regions'][reg][pion][annee]['valeur'] = Number(unit_nouv.value)
                        actions['regions'][reg][pion][annee]['action'] = '+'
                    } else {
                        alert(`        J'efface le ${unit_nouv.value} dans la région ${reg_convert[reg]} pour  l'unité ${pion_convert[pion]} pour vous.<br>`);
                        actions['regions'][reg][pion][annee]['valeur'] = ""
                        actions['regions'][reg][pion][annee]['action'] = "="
                        unit_nouv.value = ''
                    }
                } else {
                    if (unit_nouv.value !== '') {
                        mesg += `La valeur ${unit_nouv.value} dans la région ${reg_convert[reg]} pour  l'unité ${pion_convert[pion]} n'est pas correcte !<br>
                                       Je l'efface pour vous et recommencez...<br>`;
                        unit_nouv.value = ''
                        err = true
                    }
                    actions['regions'][reg][pion][annee]['valeur'] = ""
                    actions['regions'][reg][pion][annee]['action'] = "="
                }
            }

        }


    }
    var lalea = $("#alea")
    if (!(aleas.includes(lalea.val()))) {
        mesg += "Le code aléa est invalide. Je remets l'ancien...<br>";
        lalea.val(actions['alea']['actuel'])
        err = true;
    } else {
        actions['alea']['nouv'] = document.getElementById("alea").value
    }


    var lestock = document.getElementById("stock")

    if (lestock.checkValidity(lestock.value)) {
        if (Number(document.getElementById("stock").value) < Number(actions['stock']['actuel'])) {
            mesg += `On ne peut pas baisser les batteries de ${actions['stock']['actuel']} à ${document.getElementById("stock").value} c'est gâcher !<br>
                       Je les remets à la valeur d'avant, car c'était mieux avant...<br>`;
            document.getElementById("stock").value = actions['stock']['actuel']
            err = true
        } else {
            actions['stock']['nouv'] = Number(document.getElementById("stock").value)
        }
    } else {
        mesg += "Veuillez entrer une valeur entière de stock entre 1 et 10.<br> Là, je remets la valeur précédente...<br>";
        document.getElementById("stock").value = actions['stock']['actuel']
        err = true;
    }
    return [err, mesg, actions];

}

function Calculer() {

    if (actions != false) {
        $('#computeResults').html('<span class="spinner-border spinner-border-sm"></span>&nbsp;&nbsp;Calcul...');

        let [err, mesg, nouv_actions] = recup(actions)
        if (err) {
            displayError("errJeu", mesg)
            $('#computeResults').html('Calculer');
        } else {
            $.ajax({
                url: "/calculer/" + equipe + "/" + partie + "/" + annee,
                type: "POST",
                data: JSON.stringify(nouv_actions),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function (data, textStatus, jqXHR) {
                    $('#computeResults').html('<span class="spinner-border spinner-border-sm"></span>&nbsp;&nbsp;Visualisation...');
                    if (data[0] == "success") {
                        location.href = "/vues/" + equipe + "/" + partie + "/" + annee;
                    } else {
                        $('#computeResults').html('Calculer');
                        displayError(data[0], data[1]);
                        if (data[0] == "aleaChangement") {
                            window.setTimeout(function () {
                                window.location.reload()
                            }, 5000)
                        }

                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    $('#computeResults').html('Valider');
                    displayError("http", [errorThrown, jqXHR.responseText]);
                }
            });
        }
    }
}


function focus_region(laregion)
{
    const regions = document.querySelectorAll(".map__image path")
    // Reset color for all regions
    regions.forEach((r) => r.classList.remove("active"));

    // Set color to green for the clicked region
    laregion.classList.add("active");
    $('.region').hide();
    // Display corresponding region information

    //remove the first letter of the id to get the region name
    var regionName = laregion.parentNode.id.substring(1);
    $('#' + regionName).show();
};


document.addEventListener("DOMContentLoaded", function () {
    const regionInfo = document.getElementById("region-info");
    const regions = document.querySelectorAll(".map__image path");

    //hide all regions
    $('.region').hide();

    //show region on click

    regions.forEach((region) => {
        region.addEventListener("click", function () {focus_region(this)});
    });
});

function remplacer_info() {
    let [err, mesg, nouv_actions] = recup(actions)
    let action_reg = nouv_actions['regions']

    let Texte = ""
    for (reg in action_reg) {
        for (pion in action_reg[reg]) {
            for (an in action_reg[reg][pion]) {
                if (action_reg[reg][pion][an]['action'] === '?') {
                    Texte += `<span class="badge badge-pill bg-danger" onclick="focus_region($('#l${reg}')[0].childNodes[1]);">${reg_convert[reg]} : ${-action_reg[reg][pion][an]['min']} ${pion_convert[pion]}  en fin de vie </span>`;
                } else if (action_reg[reg][pion][an]['action'] === '-') {
                    if (action_reg[reg][pion][an]['valeur'] < 0)
                        Texte += `<span class="badge badge-pill bg-secondary" onclick="focus_region($('#l${reg}')[0].childNodes[1]);">${reg} : ${-action_reg[reg][pion][an]['valeur']} ${pion_short[pion]}  démantelée(s) </span>`;
                    if (action_reg[reg][pion][an]['min'] < action_reg[reg][pion][an]['valeur'])
                        Texte += `<span class="badge badge-pill bg-info" onclick="focus_region($('#l${reg}')[0].childNodes[1]);">${reg} : ${action_reg[reg][pion][an]['valeur'] - action_reg[reg][pion][an]['min']} ${pion_short[pion]}  renouvelé(s) </span>`;
                } else if (action_reg[reg][pion][an]['action'] === '+') {
                    Texte += `<span class="badge badge-pill bg-primary" onclick="focus_region($('#l${reg}')[0].childNodes[1]);">${reg} :  + ${action_reg[reg][pion][an]['valeur']}  ${pion_short[pion]} </span>`;
                };
            };
        };
    };

    if (actions['stock']['nouv']>actions['stock']['actuel']) Texte += `<span class="badge badge-pill bg-primary"> Batt. :  + ${actions['stock']['nouv']-actions['stock']['actuel']} </span>`;

    $("#replaceInfo").html(Texte)
};

function changer_annee() {
    if (document.getElementById('annee').checkValidity())
        location.href = "/saisie/" + equipe + "/" + partie + "/" + $('#annee').val();
};
$(function () {

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

    $('.resetMix').click(() => {
        $('input').val('');
        document.getElementById("stock").value = actions['stock']['actuel'];
        $('#alea').val(actions['alea']['actuel']);
        $('#annee').val(annee);
        remplacer_info();

    });
    var action_back = actions
    remplacer_info();
    window.setInterval(function () {
        remplacer_info()
    }, 1000)

    $("#top").hide();
    $("#mid").hide();
    $("#bot").hide();
    $("#top").fadeIn();
    $("#mid").fadeIn();
    $("#bot").fadeIn();


});

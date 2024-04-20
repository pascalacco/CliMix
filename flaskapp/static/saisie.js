function btnCallbacks(plus, minus, nb) {
    minus.click(() => {
        nb.val((parseInt(nb.val()) > 0 ? parseInt(nb.val()) - 1 : 0));
    });

    plus.click(() => {
        nb.val((parseInt(nb.val()) < 100 ? parseInt(nb.val()) + 1 : 100));
    });
}

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
                        alert(`Cliquez dans la région ${reg_convert[reg]} et sélectionnez un choix pour  l'unité ${pion_convert[pion]} en fin de vie!\n`);

                    } else {
                        alert(`La valeur ${unit_fin.value} saisie dans la région ${reg_convert[reg]} pour  l'unité ${pion_convert[pion]} est incorrecte!\n Débile(s) ! \n je l'efface pour vous.`);
                        unit_fin.value=""
                    }
                    err = true;

                }
            }
            var unit_nouv = document.getElementById(`${reg}_${pion}_nouv`);
            if (unit_nouv) {
                if (unit_nouv) {
                    if (unit_nouv.checkValidity(unit_nouv.value)) {
                        if (Number(unit_nouv.value) !== 0) {
                            actions['regions'][reg][pion][annee]['valeur'] = Number(unit_nouv.value)
                            actions['regions'][reg][pion][annee]['action'] = '+'
                        }
                        else{
                            alert(`        J'efface le ${unit_nouv.value} dans la région ${reg_convert[reg]} pour  l'unité ${pion_convert[pion]} pour vous.\n`);
                            actions['regions'][reg][pion][annee]['valeur']=""
                            actions['regions'][reg][pion][annee]['action']="="
                            unit_nouv.value=''
                        }
                    } else {
                        if (unit_nouv.value !== '') {
                            alert(`La valeur ${unit_nouv.value} dans la région ${reg_convert[reg]} pour  l'unité ${pion_convert[pion]} n'est pas correcte !\n
                                       Je l'efface pour vous et recommencez...\n`);
                            unit_nouv.value = ''
                            err=true
                        }
                        actions['regions'][reg][pion][annee]['valeur']=""
                        actions['regions'][reg][pion][annee]['action']="="
                    }
                }
            }
        }


    }
    actions['alea']['nouv']=document.getElementById("alea").value

    if (Number(document.getElementById("stock").value) < Number(actions['stock']['actuel'])){
        alert(`On ne peut pas baisser les batteries de ${actions['stock']['actuel']} à ${document.getElementById("stock").value} c'est gâcher !\n
           Je les remets à la valeur d'avant car c'était mieux avant...\n   `)
        document.getElementById("stock").value=actions['stock']['actuel']
        err=true
    } else
    {
        actions['stock']['nouv']=Number(document.getElementById("stock").value)
    }
    return [err, actions];

}

function Calculer() {

    if (actions != false) {
        $('#computeResults').html('<span class="spinner-border spinner-border-sm"></span>&nbsp;&nbsp;Calcul...');

        let [err, nouv_actions] = recup(actions)
        if (err) {
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
                        if (data[0] == "aleaChangement"){
                            window.setTimeout(function(){window.location.reload()}, 5000)
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

document.addEventListener("DOMContentLoaded", function () {
    const regionInfo = document.getElementById("region-info");
    const regions = document.querySelectorAll(".map__image path");

    //hide all regions
    $('.region').hide();

    //show region on click

    regions.forEach((region) => {
        region.addEventListener("click", function () {
            // Reset color for all regions
            regions.forEach((r) => r.classList.remove("active"));

            // Set color to green for the clicked region
            this.classList.add("active");
            $('.region').hide();
            // Display corresponding region information

            //remove the first letter of the id to get the region name
            var regionName = this.parentNode.id.substring(1);
            $('#' + regionName).show();
        });
    });
});


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
        fillPage();
    });


    $("#top").hide();
    $("#mid").hide();
    $("#bot").hide();
    $("#top").fadeIn();
    $("#mid").fadeIn();
    $("#bot").fadeIn();


});

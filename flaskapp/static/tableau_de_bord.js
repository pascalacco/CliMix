

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

function neste_les_checks(div_accordion) {
    let items = jQuery(">.accordion-item",div_accordion);
    
    for (let nitem=0; nitem<items.length; nitem++) {
        let est_feuille = true;
        let child_accordions =jQuery(".accordion-collapse>.accordion-body>.accordion", items[nitem]);
        if (child_accordions.length > 0)
        {   
            checker = jQuery(">.accordion-header .Option", items[nitem])[0];
            checker.remonter = function (val) {return checker.checked = val;} ;
            neste_les_checks(child_accordions);
            est_feuille = false;
        }
        if (est_feuille)
        {
            let checkgroup = items[nitem].querySelector(".accordion-header").querySelector("input[type=checkbox]");
            let child_checks = items[nitem].querySelector('.accordion-collapse').querySelectorAll('input[type=checkbox]');
            checkgroup.checkFils = child_checks;
            checkgroup.onclick = function() {
                let compteur = 0;
                for(let i=0; i<this.checkFils.length; i++) {
                    if ( ! this.checkFils[i].disabled){
                        this.checkFils[i].checked = this.checked ;
                        compteur ++;
                    }
                };

                if (this.checked && (compteur!=this.checkFils.length)){
                    this.indeterminate=true;
                }
                else this.indeterminate=false;

                raffraichir_les_groupes();
            };
            for (let i=0; i<checkgroup.checkFils.length; i++)
            {
                checkgroup.checkFils[i].checkPere = checkgroup;
                checkgroup.checkFils[i].onclick = function() {
                    this.checkPere.checkedCount = document.querySelectorAll('[id*='+this.checkPere.id+'].subOption:checked').length;
                    if (this.checkPere.checked != (this.checkPere.checkedCount > 0) ) this.checkPere.remonter(this.checkPere.checkedCount > 0);
                    this.checkPere.checked = this.checkPere.checkedCount > 0;
                    this.checkPere.indeterminate = this.checkPere.checkedCount > 0 &&
                                                (this.checkPere.checkedCount < this.checkPere.checkFils.length);
                    raffraichir_les_groupes();

                };
            };
        };
    };
};

function get_checked(groupe){
    let checked_list = [];
    let checkgroups = document.querySelectorAll('[id*=check-' + groupe + '].subOption');
    for(let j=0; j<checkgroups.length; j++)
    {
            if (checkgroups[j].checked)
            {   let champs = checkgroups[j].id.split('-')
                checked_list.push(champs[1]+'_'+champs[2]+'_'+champs[3].slice(3));
            }
    };
    return checked_list;
};

function get_info_puis(callback)
{
        $.ajax({
        url: "/admin/get_infos_parties",
        type: "GET",
        dataType: "json",
        success: function (datas, textStatus, jqXHR) {
            infos = datas;
            callback();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            displayError("http");
        }
    });
};




function rafraichir_barres()
{
    let checked_modifies = []
    for (let groupe in infos)
        {
            let parties = infos[groupe];
            for (let partie in parties)
            {
                for (let num in parties[partie]){
                    let annee = parties[partie][num]['annee'];
                    if (annee =="-1")
                    {
                        annee="Libre" ;
                    }
                    let bar = $('#progressbar-'+groupe+'-'+partie+'-'+num);
                    if ($('#check-'+groupe+'-'+partie+'-sub'+num).prop("checked"))
                    {
                        if (bar.attr('aria-valuenow') != annee)
                        {
                            checked_modifies.push(groupe+'-'+partie+'-'+num);
                        };
                    };

                    if (annee=="Libre")
                    {
                        bar.removeClass("progress-bar-animated");
                        bar.removeClass("progress-bar-striped");
                        bar.addClass("bg-secondary");
                        bar.removeClass("bg-success");
                        bar.removeClass("bg-info");
                        $('#check-'+groupe+'-'+partie+'-sub'+num).prop("disabled", true);

                        $('#creer-'+groupe+'-'+partie+'-sub'+num).prop("disabled", false);
                        $('#join-'+groupe+'-'+partie+'-sub'+num).addClass("disabled");

                    }
                    else
                    {
                        if (annee[4]=="-")
                        {
                            bar.addClass("progress-bar-animated");
                            bar.addClass("progress-bar-striped");
                            bar.addClass("bg-info");
                            bar.removeClass("bg-success");
                            bar.removeClass("bg-secondary");
                            $('#check-'+groupe+'-'+partie+'-sub'+num).prop("disabled", false);
                            $('#creer-'+groupe+'-'+partie+'-sub'+num).prop("disabled", true);
                            //$('#join-'+groupe+'-'+partie+'-sub'+num).addClass("enabled");
                            $('#join-'+groupe+'-'+partie+'-sub'+num).removeClass("disabled");
                            if (annee == "2025-")
                                $('#join-'+groupe+'-'+partie+'-sub'+num).prop("href",
                                "/vues/"+groupe+num+"/"+partie+"/2030");
                            else
                                $('#join-'+groupe+'-'+partie+'-sub'+num).prop("href",
                                "/vues/"+groupe+num+"/"+partie+"/"+annee.slice(0,4));
                            //annee = annee.slice(0,4)
                        }
                        else
                        {
                            bar.removeClass("progress-bar-animated");
                            bar.removeClass("progress-bar-striped");
                            bar.addClass("bg-success");
                            bar.removeClass("bg-secondary");
                            bar.removeClass("bg-info");
                            //annee = annee.slice(0,4)
                            $('#check-'+groupe+'-'+partie+'-sub'+num).prop("disabled", false);
                            $('#creer-'+groupe+'-'+partie+'-sub'+num).prop("disabled", true);
                            //$('#join-'+groupe+'-'+partie+'-sub'+num).addClass("enabled");
                            $('#join-'+groupe+'-'+partie+'-sub'+num).removeClass("disabled");
                            if (annee == "2025")  $('#join-'+groupe+'-'+partie+'-sub'+num).prop("href",
                                "/saisie/"+groupe+num+"/"+partie+"/2030");
                            else
                                $('#join-'+groupe+'-'+partie+'-sub'+num).prop("href",
                                "/saisie/"+groupe+num+"/"+partie+"/"+(Number(annee.slice(0,4))+5).toString());
                        }
                    }

                    bar.html(annee);
                    bar.attr('aria-valuenow', annee);
                    bar.attr('style',"width:"+parties[partie][num]['percent']+'%');


                };

            };

        };
    return checked_modifies;
};

function raffraichir_les_groupes() {
    get_info_puis(() => {rafraichir_barres();});
 };

function verifier_nouveau_puis(callback_ok, callback_pas_bon) {
    get_info_puis(() => {
        let modifie = rafraichir_barres();
        if (modifie.length==0) callback_ok();
        else    callback_pas_bon(modifie);
    });
 };

async function go_to_comparer(groupe) {
    let checked_list = get_checked(groupe);
    let response = await fetch("/admin/post_liste", {
        redirect: 'follow',
        method: "POST",
        body: JSON.stringify(checked_list),
        headers: {"Content-type": "application/json; charset=UTF-8"}
        });
        if(response.redirected) {
            window.location = response.url;
            }
        else {
            let data = await response.json()
        };
};

function fuckoff(msg)
{
    alert("L'état de "+msg+" a changé !\n Vérifiez et refaites l'action svp.");
};

function effacer_sur(groupe, e)
{
    if (e.metaKey || e.ctrlKey || e.altKey || e.shiftKey)
        verifier_nouveau_puis(() => effacer(groupe), (msg) => fuckoff(msg));
};

async function effacer(groupe) {
    let checked_list = get_checked(groupe);
    if (checked_list.length >0){
        $.ajax({
            url: "/admin/effacer",
            type: "POST",
            data: JSON.stringify(checked_list),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data, textStatus, jqXHR) {
                if (data[0] == "success") {
                    alert(data[1])
                } else {
                    displayError(data[0], data[1]);
                }
                raffraichir_les_groupes();
            } ,
            error: function (jqXHR, textStatus, errorThrown) {
                displayError("http", [errorThrown, jqXHR.responseText]);
                raffraichir_les_groupes();
                }
        });
    }
    else
    {
        alert("Vous devez sélectionner au moins une équipe de !");
    };
};

function creer_sur(groupe, partie, num)
{
    verifier_nouveau_puis(() => creer(groupe, partie, num), (msg) => fuckoff(msg));
};

function creer(groupe, partie, num)
{
    const data = [groupe+num, partie, "new"];
    $.ajax({
        url: "/set_group",
        type: "POST",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data, textStatus, jqXHR) {
            if (data[0] == "log_in_success") {
                location.href = "/saisie/"+groupe+num+"/"+partie+"/";

            } else {
                displayError("http", data);
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            displayError("http", errorThrown);
        }
    });
};

function selectionne(action)
{
    let promo = $("#poInput")[0].value;
    if (promo == "default") promo="";

    let est_valide = true;
    if (document.querySelector("#Filtre").value == "checked"){
        list = get_checked();

    };

    let accordions = document.querySelectorAll('[id*=accordion-'+promo+']');
    //let acordions = $('#accordion-'+promo);
    for(let j=0; j<accordions.length; j++)
    {      
        if (est_valide){
            if (action=="add"){
                accordions[j].classList.remove("d-none");
            }
            else
            {
                accordions[j].classList.add("d-none");
            }
        }
    }   
    
};

$(function () {
    var infos;
    $('[data-bs-toggle="tooltip"]').tooltip();
    neste_les_checks($('#accordionGroupes')[0]);

    document.querySelectorAll(".accordion-collapse").forEach((elm) => {
	    elm.addEventListener("shown.bs.collapse", () => raffraichir_les_groupes());
        });


});




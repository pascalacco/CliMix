

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

function neste_les_checks(div_accordion, pere = null) {
    let items = jQuery(">.accordion-item",div_accordion);
    

    for (let nitem=0; nitem<items.length; nitem++) {
        item = items[nitem];
        
        checker = jQuery(">.accordion-header .Option", item)[0];
        checker.pere = pere;
        checker.fils = [];
        checker.filsChecked = 0;
        checker.filsDisabled = 0;

        if (pere != null){
            checker.remonter = function (val) {
                val(checker);
                checker.pere.remonter(val);
            } ;
            pere.fils.push(checker);
            if (checker.checked) pere.filsChecked += 1;
            if (checker.disabled) pere.filsDisabled += 1;

        } else {
            checker.remonter = function (val) {       
                val(checker);
            } ;
        } 

        let child_accordion =jQuery(".accordion-collapse>.accordion-body>.accordion", item);
        if (child_accordion.length >0){
            neste_les_checks(div_accordion=child_accordion[0], pere=checker); 
        }else{
            checker.fils = item.querySelector('.accordion-collapse>.accordion-body').querySelectorAll('input[type=checkbox]');
        }

        
        checker.onclick = function() {
                let compteur = 0;
                for(let i=0; i<this.fils.length; i++) {
                    if ( ! this.fils[i].disabled){
                        this.fils[i].checked = this.checked ;
                        if (this.fils[i].onclick != null) this.fils[i].onclick();
                        compteur ++;
                    }
                };
                if (this.checked && (compteur!=this.fils.length)){
                    this.indeterminate=true;
                }
                else this.indeterminate=false;
                
                if (this.pere == null){
                    raffraichir_les_groupes();
                }else{
                    checker.remonter((moi) => moi.pere.checked = moi.checked);
                }
            };
        
        for (let i=0; i<checker.fils.length; i++)
        {
            checker.fils[i].pere = checker;
            checker.fils[i].onclick = function() {
                this.pere.checkedCount = document.querySelectorAll('[id*='+this.pere.id+'].subOption:checked').length;
                if (this.pere.checked != (this.pere.checkedCount > 0) ) this.pere.remonter(this.pere.checkedCount > 0);
                this.pere.checked = this.pere.checkedCount > 0;
                this.pere.indeterminate = this.pere.checkedCount > 0 &&
                                            (this.pere.checkedCount < this.pere.fils.length);
            }
        }
        
        /*

        checker.onclick = function() {
            let compteur = 0;
            for(let i=0; i<this.fils.length; i++) {
                if ( ! this.fils[i].disabled){
                    this.fils[i].checked = this.checked ;
                    compteur ++;
                }
            };
            if (compteur == 0){

            }
            if (this.checked && (compteur!=this.fils.length)){
                this.indeterminate=true;
            }
            else this.indeterminate=false;
            
            if (pere == null){
                raffraichir_les_groupes();
            }else{
                
            }
        };
        for (let i=0; i<checker.fils.length; i++)
        {
            checker.fils[i].pere = checker;
            checker.fils[i].onclick = function() {
                this.pere.checkedCount = document.querySelectorAll('[id*='+this.pere.id+'].subOption:checked').length;
                if (this.pere.checked != (this.pere.checkedCount > 0) ) this.pere.remonter(this.pere.checkedCount > 0);
                this.pere.checked = this.pere.checkedCount > 0;
                this.pere.indeterminate = this.pere.checkedCount > 0 &&
                                            (this.pere.checkedCount < this.pere.fils.length);
            }
        }*/
    }   
        
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




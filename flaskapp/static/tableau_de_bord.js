

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

function appliquer_aux_freres_de_classe(moi, classe, fonction){
    let freres = moi.parentElement.getElementsByClassName(classe);
    for (let i=0; i<freres.length; i++) 
        fonction(freres[i]);
}


function neste_les_checks(div_accordion, pere = null) {

    let items = jQuery(">.accordion-item",div_accordion);
    let get_checker = (items, nitem) => {return jQuery(">.accordion-header .Option", items[nitem])[0];};
    let fin_de_recursion = false;

    if (items.length==0){
        items = div_accordion.querySelector('.accordion-collapse>.accordion-body').querySelectorAll('input[type=checkbox]');
        get_checker = (items, nitem) => {return items[nitem]};
        fin_de_recursion = true;
    }
    
    for (let nitem=0; nitem<items.length; nitem++) {
        
        let checker = get_checker(items, nitem);
        checker.pere = pere;
        checker.fils = [];
        checker.filsChecked = 0;
        checker.filsDisabled = 0;
        appliquer_aux_freres_de_classe(checker, "valide_si_checked", moi => moi.disabled=! checker.checked);


        if (pere != null){
            pere.fils.push(checker);
            if (checker.disabled) 
                pere.modifier_disabled(1);
            else 
                pere.modifier_disabled(0);
            if (checker.checked) 
                pere.modifier_checked(1); 
        }

        checker.modifier_disabled = function(val){
            this.filsDisabled += val;

            if ((this.filsDisabled >= this.fils.length)  && ( ! this.disabled))
            {
                this.disabled = true;
 
                if (this.pere != null) this.pere.modifier_disabled(1);
            }

            if ((this.filsDisabled < this.fils.length)  && (this.disabled))
            {
                this.disabled = false;
                if (this.pere != null) this.pere.modifier_disabled(-1);
            }
            if (this.fils.length==0) this.filsDisabled = 0;

        };

        checker.modifier_checked = function(val){
            this.filsChecked += val;
        
            if (this.filsChecked>0  && ! this.checked) {
                this.checked = true;
                appliquer_aux_freres_de_classe(this, "valide_si_checked", moi => moi.disabled=false);

                if (this.pere != null) 
                    this.pere.modifier_checked(1);
            } 
            if (this.filsChecked<=0  && this.checked) {
                this.checked = false;
                appliquer_aux_freres_de_classe(this, "valide_si_checked", moi => moi.disabled=true);
 
                if (this.pere != null) 
                    this.pere.modifier_checked(-1);
            }
            if (this.fils.length==0) this.filsChecked = 0;

            if (this.checked && (this.filsChecked < this.fils.length)){
                this.indeterminate=true;
            }
            else this.indeterminate=false;

        };

        if (! fin_de_recursion){
            let child_accordion =jQuery(".accordion-collapse>.accordion-body>.accordion", items[nitem]);
            if (child_accordion.length >0){
                neste_les_checks(child_accordion[0], checker); 
            }else{
                neste_les_checks(items[nitem], checker);
                //checker.fils = item.querySelector('.accordion-collapse>.accordion-body').querySelectorAll('input[type=checkbox]');
            }
        }
        
        checker.downclick = function (val){
            if (this.fils.length ==0)
                this.checked = val;
            else {
                let compteur = 0;
                let compteur_checked = 0;
                for(let i=0; i<this.fils.length; i++) {
                    if ( ! this.fils[i].disabled){
                        this.fils[i].downclick(val);
                        if (this.fils[i].checked) compteur_checked ++;
                        compteur ++;
                    }
                }
                this.filsDisabled=this.fils.length - compteur;
                this.filsChecked=compteur_checked;
                this.checked = compteur_checked > 0;
                appliquer_aux_freres_de_classe(this, "valide_si_checked", moi => moi.disabled= !this.checked);

                if (this.checked && (this.filsChecked != this.fils.length)){
                    this.indeterminate=true;
                }
                else this.indeterminate=false;
            }
        };

        checker.onclick = function (){
            this.style.cursor = 'wait';
            let nouv = this.checked;
            raffraichir_les_groupes_puis((modifies) => {
                this.downclick(this.checked);
                if (this.checked && nouv && this.pere!=null) 
                    this.pere.modifier_checked(1);
                if (!this.checked && !nouv && this.pere!=null) 
                    this.pere.modifier_checked(-1);
                this.style.cursor = 'default';    
            });
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

function get_info_puis(promesse=null)
{
        $.ajax({
        url: "/admin/get_infos_parties",
        type: "GET",
        dataType: "json",
        success: function (datas, textStatus, jqXHR) {
            infos = datas;
            if (promesse != null) promesse();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            displayError("http");
        }
    });
};

function rafraichir_barres()
{
    let checked_modifies = {
        "unchecked": [], 
        "checked" : [], 
        "now_disabled" : [], 
        "now_enabled" : []
    };
    
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
                    if (bar.attr('aria-valuenow') != annee)
                    {
                        if ($('#check-'+groupe+'-'+partie+'-sub'+num).prop("checked"))
                            checked_modifies["checked"].push(groupe+'-'+partie+'-'+num);
                        else
                            checked_modifies["unchecked"].push(groupe+'-'+partie+'-'+num);
                    };
                

                    if (annee=="Libre")
                    {
                        bar.removeClass("progress-bar-animated");
                        bar.removeClass("progress-bar-striped");
                        bar.addClass("bg-secondary");
                        bar.removeClass("bg-success");
                        bar.removeClass("bg-info");

                        let checker = $('#check-'+groupe+'-'+partie+'-sub'+num)[0];
                        if (!checker.disabled){
                            checker.disabled=true;
                            checked_modifies["now_disabled"].push(checker);
                        }

                        $('#creer-'+groupe+'-'+partie+'-sub'+num).prop("disabled", false);
                        $('#join-'+groupe+'-'+partie+'-sub'+num).addClass("disabled");

                    }
                    else
                    {
                        let checker = $('#check-'+groupe+'-'+partie+'-sub'+num)[0];
                        if (checker.disabled){
                            checker.disabled=false;
                            checked_modifies["now_enabled"].push(checker);
                        }

                        $('#creer-'+groupe+'-'+partie+'-sub'+num).prop("disabled", true);
                        $('#join-'+groupe+'-'+partie+'-sub'+num).removeClass("disabled");
                        
                        if (annee[4]=="-")
                        {
                            bar.addClass("progress-bar-animated");
                            bar.addClass("progress-bar-striped");
                            bar.addClass("bg-info");
                            bar.removeClass("bg-success");
                            bar.removeClass("bg-secondary");
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

function raffraichir_les_groupes_puis(promesse = null) {
    get_info_puis(() => {
        let modifies = rafraichir_barres();
        for (let i =0; i<modifies["now_disabled"].length; i++){
            modifies["now_disabled"][i].modifier_checked(-1);
            modifies["now_disabled"][i].disabled=false; // s'assurer de la propagation            
            modifies["now_disabled"][i].modifier_disabled(1);
        }
        for (let i =0; i<modifies["now_enabled"].length; i++){
            modifies["now_enabled"][i].disabled=true; // s'assurer de la propagation            
            modifies["now_enabled"][i].modifier_disabled(-1);
        }
        if (promesse != null) promesse(modifies);
    });
 };

function verifier_nouveau_puis(callback_ok, callback_pas_bon) {  
    get_info_puis(() => {
        let modifie = rafraichir_barres();
        if (modifie["checked"].length==0) callback_ok();
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

function effacer_sur(groupe)
{
    if (event.metaKey || event.ctrlKey || event.altKey || event.shiftKey)
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
                raffraichir_les_groupes_puis();
            } ,
            error: function (jqXHR, textStatus, errorThrown) {
                displayError("http", [errorThrown, jqXHR.responseText]);
                raffraichir_les_groupes_puis();
                }
        });
    }
    else
    {
        alert("Vous devez sélectionner au moins une équipe de !");
    };
};

function creer_sur(groupe, partie, num, bouton)
{
    bouton.style.cursor='wait';
    verifier_nouveau_puis(() => creer(groupe, partie, num), (msg) => fuckoff(msg));
    bouton.style.cursor='default';
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
    let scenario = $("#scenarioInput")[0].value;

    let est_valide = accordion => true;
    if (document.querySelector("#Filtre").value == "checked"){
        est_valide = accordion => {
            return jQuery(".Option", accordion)[0].checked;
        };
    };
    if (document.querySelector("#Filtre").value == "encours"){
        list = get_checked();
        est_valide = accordion => {
            return ! jQuery(".Option", accordion)[0].disabled;
        };
    };

    if (document.querySelector("#Filtre").value == "libres"){
        list = get_checked();
        est_valide = accordion => {
            let checker = jQuery(".Option", accordion)[0];
            if (checker.fils[0].fils.length==0)
                return checker.filsDisabled > 0;
            else
                return true;
        };
    };

    //let accordions = document.querySelectorAll('[id*=accordion-'+promo+']');
    //let acordions = $('#accordion-'+promo);   
    let accordions = $('.accordion-item');

    let groupe_pere = null;
    let propager;

    for(let j=  0; j<accordions.length; j++)
    {   
        let groupe_scenar = accordions[j].id.split('-')[1].split('_')
        let promo_ok = promo=="default" || groupe_scenar[0]==promo;
        let scenario_ok;
   
        if (groupe_scenar.length>2){
            scenario_ok = scenario=="default" || groupe_scenar[2]==scenario ;
            propager = groupe_pere != null;
        }
        else
        {   
            groupe_pere = accordions[j];
            propager=false;
            scenario_ok =true;  
        }
        if (promo_ok && scenario_ok){
            if (est_valide(accordions[j])){
                if (action=="add"){
                    accordions[j].classList.remove("d-none");
                    //if (propager) groupe_pere.classList.remove("d-none"); 
                }
                else
                {
                    accordions[j].classList.add("d-none");
                }
            }
        }
    }   
    
};

$(function () {
    var infos;
    document.body.style.cursor = 'wait'; 
    $('[data-bs-toggle="tooltip"]').tooltip();
    
    document.querySelectorAll(".accordion-collapse").forEach((elm) => {
	    elm.addEventListener("shown.bs.collapse", function () { 
            this.style.cursor="wait"; 
            raffraichir_les_groupes_puis();
            this.style.cursor="default";
        });
    });
    
    get_info_puis( () => {    
        let modifies = rafraichir_barres();
        neste_les_checks($('#accordionGroupes')[0]);
        document.body.style.cursor = 'default';
    });
});




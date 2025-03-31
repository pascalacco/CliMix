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

function neste_les_checks() {

    let checkgroups = document.querySelectorAll('[id*=check-].Option');
    for(let j=0; j<checkgroups.length; j++) {
        let checkgroup = checkgroups[j]
        checkgroup.checkFils = document.querySelectorAll('[id*='+checkgroup.id+'].subOption')
        checkgroup.onclick = function() {
            for(let i=0; i<this.checkFils.length; i++) {
                this.checkFils[i].checked = this.checked;

            }
        }
        for(let i=0; i<checkgroup.checkFils.length; i++)
        {
            checkgroup.checkFils[i].checkPere = checkgroup
            checkgroup.checkFils[i].onclick = function() {
                this.checkPere.checkedCount = document.querySelectorAll('[id*='+this.checkPere.id+'].subOption:checked').length;
                this.checkPere.checked = this.checkPere.checkedCount > 0;
                this.checkPere.indeterminate = this.checkPere.checkedCount > 0 && this.checkPere.checkedCount < this.checkPere.checkFils.length;
                }
        }
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

function raffraichir_les_groupes() { };

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
                    alert("Paries effacées !")
                } else {
                    displayError(data[0], data[1]);
                }
            } ,
            error: function (jqXHR, textStatus, errorThrown) {
                    displayError("http", [errorThrown, jqXHR.responseText]);
                }
        });
    }
    else
    {
        alert("Vous devez sélectionner au moins une équipe de !");
    };
};


$(function () {
    $('[data-bs-toggle="tooltip"]').tooltip();
    neste_les_checks();
    }
);




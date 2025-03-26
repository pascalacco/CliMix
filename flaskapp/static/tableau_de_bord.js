function neste_les_checks() {

    checkgroups = document.querySelectorAll('[id*=check-].Option');
    for(var j=0; j<checkgroups.length; j++) {
        checkgroup = checkgroups[j]
        checkgroup.checkFils = document.querySelectorAll('[id*='+checkgroup.id+'].subOption')
        checkgroup.onclick = function() {
            for(var i=0; i<this.checkFils.length; i++) {
                this.checkFils[i].checked = this.checked;

            }
        }
        for(var i=0; i<checkgroup.checkFils.length; i++)
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

async function go_to_comparer(groupe) {
    var checked_list = [];
    checkgroups = document.querySelectorAll('[id*=check-].subOption');
    for(var j=0; j<checkgroups.length; j++)
    {
            if (checkgroups[j].checked)
            {   champs = checkgroups[j].id.split('-')
                checked_list.push(champs[1]+'_'+champs[2]+'_'+champs[3].slice(3));
            }
    };
    doc = await fetch("/admin/comparer/post_liste", {
        redirect: 'follow',
        method: "POST",
        body: JSON.stringify(checked_list),
        headers: {"Content-type": "application/json; charset=UTF-8"}
        }).then( (data) => {
            if(data.redirected) {window.location = data.url;}
            });
};

$(neste_les_checks());



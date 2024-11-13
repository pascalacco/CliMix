$(function () {
    $('#productionBar').click(() => {
        $('#productionBar').html('<span class="spinner-border spinner-border-sm"></span>&nbsp;&nbsp;Production');
        location.href = "/vues/production";
    });
});

function spin(me){
    $('#'+me).html('<span class="spinner-border spinner-border-sm"></span>&nbsp;&nbsp;'+me);
    location.href = "/vues/"+equipe+"/"+partie+"/"+annee+"/"+me;
}

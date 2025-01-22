$(function () {



    function displayError(reason, details) {
        let msg;
        const modal = new bootstrap.Modal($("#errModal"));

        switch (reason) {
            case "http":
                msg = details;
                break;
            default:
                msg = details
                break;
        }

        $("#errorMsg").html(msg);
        modal.toggle();
    }



    function fillPage() {
        //$("#turn").text(`Tour ${(resultsData.annee.toString() - 2030) / 5 + 1} : Année ${(resultsData.annee.toString())}`);
        //if ((annee_int - 5).toString() in resultsHistory) document.getElementById('previousYear').disabled=false;
        //else document.getElementById('previousYear').disabled=true;

        //let nextannee = (annee_int + 5).toString()
        //if ($.isEmptyObject(resultsHistory[nextannee])) document.getElementById('nextYear').disabled=true;
        //else document.getElementById('nextYear').disabled=false;

    }

    $('#previousYear').click(() => {
        annee_int = annee_int - 5;
        annee = annee_int.toString();
        resultsData = resultsHistory[annee];
        fillPage();

    });

    $('#nextYear').click(() => {
        annee_int = annee_int + 5;
        annee = annee_int.toString();
        resultsData = resultsHistory[annee];
        fillPage();
    });

    $('#commitResults').click(() => {
        location.href = "/commit";
    });

    $('#retourResults').click(() => {
        location.href = "/manual";
    });

    //fillPage();

    $("#journal").fadeIn();


});

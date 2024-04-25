$(function () {


    function displayError(reason, details) {
        let msg;
        const modal = new bootstrap.Modal($("#errModal"));

        switch (reason) {
            case "input":
                msg = "Veuillez choisir votre po ET groupe ET  équipe ET scénario.";
                break;

            case "http":
                msg = details;
                break;

           case "err":
                msg = details;
                break;

            default:
                msg = details
                break;
        }

        $("#errorMsg").html(msg);
        modal.toggle();
    }

    $(".logInBtn").click((e) => {
        let initOk = true
        let po = $("#poInput").val()
        let nom2groupe = "default"

        if (po != "default") {
            nom2groupe = po
        } else initOk = false;

        let td = $("#tdInput").val()
        if (td != "default") {
            nom2groupe += '_' + td
        } else initOk = false;

        let equipe = $("#equipeInput").val()
        if (equipe != "default") {
            nom2groupe += equipe
        } else initOk = false;

        let scenario = $("#scenarInput").val()
        if (scenario != "default") {
        } else initOk = false;

        const data = [nom2groupe, scenario, e.target.id];

        if (initOk) {
            $.ajax({
                url: "/set_group",
                type: "POST",
                data: JSON.stringify(data),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function (data, textStatus, jqXHR) {
                    if (data[0] == "log_in_success") {
                        location.href = "/saisie/"+nom2groupe+"/"+scenario+"/2030";

                    } else {
                        displayError("http", data);
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    displayError("http", errorThrown);
                }
            });

        } else {
            displayError("input", []);
        }
    });

    $("#sous-titre").fadeIn(function () {
        $("#submit").fadeIn();
    });


});

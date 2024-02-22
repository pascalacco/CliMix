$(function() {


    let mixData = null;


    function saveData() {
        let err = 0;
        let result;
        const data = {};
        const stockStr = $("#stock").val();
        const stock = parseFloat(stockStr);

        if ($("#carte").val() == "default") {
            alert("Veuillez sélectionner une carte");
            err = 1;

        } else if ($("#annee").val() == "default") {
            alert("Veuillez sélectionner une année");
            err = 1;

        } else if (!(aleas.includes($("#alea").val()))) {
            alert("Le code aléa est invalide");
            err = 1;

        } else if (!(politiques.includes($("#politique").val()))) {
            alert("Le code politique est invalide");
            err = 1;

        } else if (stockStr == "" || stock < 1 || stock > 10 || !(Number.isInteger(stock))) {
            alert("Veuillez entrer une valeur entière de stock entre 1 et 10");
            err = 1;

        } else {
            data["actif"] = true;
            data["carte"] = $("#carte").val();
            data["annee"] = parseInt($("#annee").val());
            data["stock"] = parseInt($("#stock").val());
            data["alea"] = $("#alea").val();
            data["politique"] = $("#politique").val();

            for (const reg of maps[$("#carte").val()]) {
                data[reg[0]] = {};
                for (const p of pions) {
                    const str = $(`#${reg[0]}_${p[0]}`).val();
                    const nb = parseFloat(str);
                    if (str == "" || nb < 0 || nb > 100 || !(Number.isInteger(nb))) {
                        alert("Veuillez entrer des nombres entiers entre 0 et 100 seulement.");
                        err = 1;
                    }
                    data[reg[0]][p[0]] = nb;
                }
            }
        }

        result = err ? false : JSON.stringify(data);
        return result;
    }


    $('#computeUne').click(() => {
        const dataProd = saveData();
        if (dataProd != false) {
            $('#computeUne').html('<span class="spinner-border spinner-border-sm"></span>&nbsp;&nbsp;Chargement...');
            exitConfirm = false;
            $.ajax({
                url: "/production",
                type: "POST",
                data: dataProd,
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function (data, textStatus, jqXHR) {
                    console.log("wesheuh");
                    $('#computeUne').html('Autre');
                    console.log(data);
                    if (data[0] == "success") {
                        console.log("wesheuh bis");
                        location.href = "/journal";
                    } else {
                        console.log("nope");
                        displayError(data[0], data[1]);
                    }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log(jqXHR.responseText);
                    $('#computeUne').html('Autre');
                    displayError("http", null);
                }
            });
        }
    });


}



});

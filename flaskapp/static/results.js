$(function () {


    let resultsData = null;
    let resultsHistory = null;
    let mixData = null;

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


    function PuissanceInst() {
        // Define the chart to be drawn.
        const TotalP = (resultsData.puissanceBatterie +
            resultsData.puissanceEolienneOFF +
            resultsData.puissanceEolienneON +
            resultsData.puissanceGaz +
            resultsData.puissanceNucleaire +
            resultsData.puissancePV +
            resultsData.puissancePhs);


        let result1 = google.visualization.arrayToDataTable([['Technologie', 'Pourcentage', 'Unité'],
            ['EON', resultsData.puissanceEolienneON / TotalP, 'GW'],
            ['EOFF', resultsData.puissanceEolienneOFF / TotalP, 'GW'],
            ['Batterie', resultsData.puissanceBatterie / TotalP, 'GW'],
            ['Nucléaire', resultsData.puissanceNucleaire / TotalP, 'GW'],
            ['PV', resultsData.puissancePV / TotalP, 'GW'],
            ['Phs', resultsData.puissancePhs / TotalP, 'GW'],
            ['Gaz', resultsData.puissanceGaz / TotalP, 'GW']
        ]);

        let options = {
            title: 'Puissance installée'
        };


        // Concaténez la valeur à la chaîne 'Puissance Installée' et affichez-la dans l'élément <div>
        let powStr = options.title + " : " + Math.round(TotalP) + " GW";
        $("#output").text(powStr);


        // Instantiate and draw the chart.
        let chart = new google.visualization.PieChart(document.getElementById('Chart_div'));
        chart.draw(result1, options);
    }


    function Sol() {

        let result9 = google.visualization.arrayToDataTable([['Type', 'Pourcentage', 'Unité'],
            ['Technologie', resultsData.sol, '%'],
            ['Le reste de la France', 1 - resultsData.sol, '%']
        ]);

        let options = {
            title: 'Occupation au sol des infrastructures',
            slices: {
                0: {color: '#33ac71'},
                1: {color: '#b97940'}
            }
        };

        // Instantiate and draw the chart.
        let chart = new google.visualization.PieChart(document.getElementById('Sol_div'));
        chart.draw(result9, options);
    }

    function conso() {
        let result8 = google.visualization.arrayToDataTable([
            ['Année', 'EON', 'EOFF', 'Batterie', 'Nucléaire',
                'PV', 'Hydraulique', 'Phs', 'Gaz Fossile', 'Gaz autres', {role: 'annotation'}],

            ['2030', resultsData.prodOnshore["2030"], resultsData.prodOffshore["2030"], resultsData.prodBatterie["2030"],
                resultsData.prodNucleaire["2030"], resultsData.prodPv["2030"], resultsData.prodEau["2030"],
                resultsData.prodPhs["2030"], resultsData.prodGazFossile["2030"], (resultsData.prodGaz["2030"] - resultsData.prodGazFossile["2030"]), ''],

            ['2035', resultsData.prodOnshore["2035"], resultsData.prodOffshore["2035"], resultsData.prodBatterie["2035"],
                resultsData.prodNucleaire["2035"], resultsData.prodPv["2035"], resultsData.prodEau["2035"],
                resultsData.prodPhs["2035"], resultsData.prodGazFossile["2035"], (resultsData.prodGaz["2035"] - resultsData.prodGazFossile["2035"]), ''],

            ['2040', resultsData.prodOnshore["2040"], resultsData.prodOffshore["2040"], resultsData.prodBatterie["2040"],
                resultsData.prodNucleaire["2040"], resultsData.prodPv["2040"], resultsData.prodEau["2040"],
                resultsData.prodPhs["2040"], resultsData.prodGazFossile["2040"], (resultsData.prodGaz["2040"] - resultsData.prodGazFossile["2040"]), ''],

            ['2045', resultsData.prodOnshore["2045"], resultsData.prodOffshore["2045"], resultsData.prodBatterie["2045"],
                resultsData.prodNucleaire["2045"], resultsData.prodPv["2045"], resultsData.prodEau["2045"],
                resultsData.prodPhs["2045"], resultsData.prodGazFossile["2045"], (resultsData.prodGaz["2045"] - resultsData.prodGazFossile["2045"]), ''],

            ['2050', resultsData.prodOnshore["2050"], resultsData.prodOffshore["2050"], resultsData.prodBatterie["2050"],
                resultsData.prodNucleaire["2050"], resultsData.prodPv["2050"], resultsData.prodEau["2050"],
                resultsData.prodPhs["2050"], resultsData.prodGazFossile["2050"], (resultsData.prodGaz["2050"] - resultsData.prodGazFossile["2050"]), ''],
        ]);

        let options = {
            width: 600,
            title: 'Production par technologie (en GWh)',
            height: 400,
            legend: {position: 'top', maxLines: 3},
            bar: {groupWidth: '75%'},
            isStacked: true,
        };


        let chart = new google.visualization.ColumnChart(document.getElementById('Combine_div'));
        chart.draw(result8, options);
    }

    function Prod() {
        let result2 = google.visualization.arrayToDataTable([
            ['Technologie', 'Production'],
            ['EON', resultsData.prodOnshore[resultsData.annee]],            // RGB value
            ['EOFF', resultsData.prodOffshore[resultsData.annee]],            // English color name
            ['Batterie', resultsData.prodBatterie[resultsData.annee]],
            ['Hydraulique', resultsData.prodEau[resultsData.annee]],
            ['Gaz', resultsData.prodGaz[resultsData.annee]],
            ['Nucléaire', resultsData.prodNucleaire[resultsData.annee]],
            ['PV', resultsData.prodPv[resultsData.annee]],
            ['Phs', resultsData.prodPhs[resultsData.annee]],
            // CSS-style declaration
        ]);

        let options = {
            title: 'Production (en GWh)',
            legend: 'none'
        };

        let chart = new google.visualization.ColumnChart(document.getElementById("Bar_div"));
        chart.draw(result2, options);
    }

    function EmCO2() {
        let co2Array = [];
        for (let i = 0; i < 5; i++) {
            co2Array.push((resultsData.co2[i] === undefined) ? 0 : resultsData.co2[i]);
        }

        let result3 = google.visualization.arrayToDataTable([
            ['Année', 'Emissions CO2', {role: "style"}],
            ['2025', 26494417, 'color : green'],
            ['2030', co2Array[0], 'color : green'],
            ['2035', co2Array[1], 'color : green'],
            ['2040', co2Array[2], 'color : green'],
            ['2045', co2Array[3], 'color : green'],
            ['2050', co2Array[4], 'color : green']
        ]);

        let options = {
            title: 'Emissions de CO2 (en Millions de tonnes de CO2)',
            hAxis: {title: 'Année', titleTextStyle: {color: 'black'}},
            vAxis: {minValue: 0},
            legend: 'none'
        };

        let chart = new google.visualization.AreaChart(document.getElementById('line_div'));
        chart.draw(result3, options);


    }

    function PenSurBar1() {
        let result4 = new google.visualization.arrayToDataTable([
            ['Heures', 'nombre de pénuries', 'nombre de surplus'],
            [{v: [0, 0, 0], f: '0 am'}, resultsData.penuriesHoraire[0], resultsData.surplusHoraire[0]],
            [{v: [1, 0, 0], f: '1 am'}, resultsData.penuriesHoraire[1], resultsData.surplusHoraire[1]],
            [{v: [2, 0, 0], f: '2 am'}, resultsData.penuriesHoraire[2], resultsData.surplusHoraire[2]],
            [{v: [3, 0, 0], f: '3 am'}, resultsData.penuriesHoraire[3], resultsData.surplusHoraire[3]],
            [{v: [4, 0, 0], f: '4 am'}, resultsData.penuriesHoraire[4], resultsData.surplusHoraire[4]],
            [{v: [5, 0, 0], f: '5 am'}, resultsData.penuriesHoraire[5], resultsData.surplusHoraire[5]],
            [{v: [6, 0, 0], f: '6 am'}, resultsData.penuriesHoraire[6], resultsData.surplusHoraire[6]],
            [{v: [7, 0, 0], f: '7 am'}, resultsData.penuriesHoraire[7], resultsData.surplusHoraire[7]],
            [{v: [8, 0, 0], f: '8 am'}, resultsData.penuriesHoraire[8], resultsData.surplusHoraire[8]],
            [{v: [9, 0, 0], f: '9 am'}, resultsData.penuriesHoraire[9], resultsData.surplusHoraire[9]],
            [{v: [10, 0, 0], f: '10 am'}, resultsData.penuriesHoraire[10], resultsData.surplusHoraire[10]],
            [{v: [11, 0, 0], f: '11 am'}, resultsData.penuriesHoraire[11], resultsData.surplusHoraire[11]],
            [{v: [12, 0, 0], f: '12 am'}, resultsData.penuriesHoraire[12], resultsData.surplusHoraire[12]],
            [{v: [13, 0, 0], f: '1 pm'}, resultsData.penuriesHoraire[13], resultsData.surplusHoraire[13]],
            [{v: [14, 0, 0], f: '2 pm'}, resultsData.penuriesHoraire[14], resultsData.surplusHoraire[14]],
            [{v: [15, 0, 0], f: '3 pm'}, resultsData.penuriesHoraire[15], resultsData.surplusHoraire[15]],
            [{v: [16, 0, 0], f: '4 pm'}, resultsData.penuriesHoraire[16], resultsData.surplusHoraire[16]],
            [{v: [17, 0, 0], f: '5 pm'}, resultsData.penuriesHoraire[17], resultsData.surplusHoraire[17]],
            [{v: [18, 0, 0], f: '6 pm'}, resultsData.penuriesHoraire[18], resultsData.surplusHoraire[18]],
            [{v: [19, 0, 0], f: '7 pm'}, resultsData.penuriesHoraire[19], resultsData.surplusHoraire[19]],
            [{v: [20, 0, 0], f: '8 pm'}, resultsData.penuriesHoraire[20], resultsData.surplusHoraire[20]],
            [{v: [21, 0, 0], f: '9 pm'}, resultsData.penuriesHoraire[21], resultsData.surplusHoraire[21]],
            [{v: [22, 0, 0], f: '10 pm'}, resultsData.penuriesHoraire[22], resultsData.surplusHoraire[22]],
            [{v: [23, 0, 0], f: '11 pm'}, resultsData.penuriesHoraire[23], resultsData.surplusHoraire[23]]
        ]);

        let options = {
            title: 'Nombre de Pénuries et Surplus par heure sur une année',
            colors: ['#9575cd', '#33ac71'],
            hAxis: {
                title: 'Heures',
                format: 'h:mm a',
                viewWindow: {
                    min: [0, 0, 0],
                    max: [23, 30, 0]
                }
            },
            vAxis: {
                title: 'Rating (scale of 1-100)'
            }
        };

        let chart = new google.visualization.ColumnChart(document.getElementById('chartcolumn_div'));
        chart.draw(result4, options);

    }

    function PenSurBar2() {
        let result5 = new google.visualization.arrayToDataTable([]);
        result5.addColumn('number', "Jours de l'année");
        result5.addColumn('number', 'nombre de pénuries');
        result5.addColumn('number', 'nombre de surplus');

        for (let i = 0; i < 365; i++) {
            result5.addRow([i + 1, resultsData.penuriesQuotidien[i], resultsData.surplusQuotidien[i]]);
        }

        let options = {
            title: 'Nombre de Pénuries et Surplus par jour',
            colors: ['#9575cd', '#33ac71'],
            hAxis: {
                title: 'Jours',
                viewWindow: {
                    min: [0, 0, 0],
                    max: [365, 100, 0]
                }
            },
            vAxis: {
                title: 'Rating (scale of 1-100)'
            }
        };

        let chart = new google.visualization.ColumnChart(document.getElementById('chartcolumn2_div'));
        chart.draw(result5, options);

    }

    function Resultats() {
        let result6 = new google.visualization.arrayToDataTable([]);
        result6.addColumn('string', 'Bilan');
        result6.addColumn('number', '');
        result6.addRows([
            ['Dépense', {v: resultsData.cout, f: resultsData.cout + ' Md€'}],
            ['Budget disponible', {v: resultsData.budget, f: resultsData.budget + ' Md€'}],
            ['Demande électrique', {v: resultsData.demande, f: resultsData.demande + ' GWh/an'}],
            ['Production électrique', {v: resultsData.production, f: resultsData.production + ' GWh/an'}],
            ['Production - Demande électrique', {
                v: resultsData.production - resultsData.demande,
                f: resultsData.production - resultsData.demande + ' GWh/an'
            }],
            ["Nb d'heures de Pénuries", {v: resultsData.nbPenuries}],
            ["Nb d'heures de Surplus", {v: resultsData.nbSurplus}],
            ['Conso Gaz (stock debut - stock fin)', {
                v: resultsData.consoGaz,
                f: resultsData.consoGaz + ' GWh/an'
            }],
            ['Biogaz produit (équivalent électrique)', {
                v: resultsData.biogaz,
                f: resultsData.biogaz + ' GWh/an'
            }],
            ['Gaz généré par electrolyse (équivalent électrique)', {
                v: resultsData.GazElectrolyse,
                f: resultsData.GazElectrolyse + ' GWh/an'
            }],
                ['Gaz fossile brulé (équivalent électrique)', {
                v: resultsData.prodGazFossile[resultsData.annee],
                f: resultsData.prodGazFossile[resultsData.annee] + ' GWh/an'
            }]
        ]);

        let table = new google.visualization.Table(document.getElementById('table_div'));
        table.draw(result6, {showRowNumber: true, width: '100%', height: '100%'});
    }

    function Score() {
        let result7 = google.visualization.arrayToDataTable([
            ['Matières Premières', 'Score', {role: 'style'}],
            ['Uranium', resultsData.scoreUranium, 'gold'],            // RGB value
            ['Hydrocarburants/Gaz', resultsData.scoreHydro, 'silver'],            // English color name
            ['Bois', resultsData.scoreBois, '#33ac71'],
            ['Déchets', resultsData.scoreDechets, 'color : brown'],
            // CSS-style declaration
        ]);

        let options = {
            title: 'Matières Premières (sur 100)',
            legend: 'none'
        };

        let chart = new google.visualization.ColumnChart(document.getElementById("Score_div"));
        chart.draw(result7, options);
    }

    function creerLegende(couleurs, min, coeff) {
        divStr = "";
        for (let i = 0; i < couleurs.length; i++) {
            let debutIntervalle = Math.round(min + i * coeff);
            let finIntervalle = Math.round(debutIntervalle + coeff);
            let couleur = couleurs[i];

            divStr += `<span class="legende-couleur" style="background-color: ${couleur};"></span>
                            [${debutIntervalle}  ,  ${finIntervalle}] </br>`;
        }
        $("#legendeItem").html(divStr);
    }


    function fillPage() {
        google.charts.load('current', {'packages': ['table']});
        google.charts.load('current', {'packages': ['corechart']});
        google.charts.load('current', {'packages': ['geochart']}, {mapsApiKey: 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'});

        google.charts.setOnLoadCallback(PuissanceInst);
        google.charts.setOnLoadCallback(Prod);
        google.charts.setOnLoadCallback(EmCO2);
        google.charts.setOnLoadCallback(PenSurBar1);
        google.charts.setOnLoadCallback(PenSurBar2);
        google.charts.setOnLoadCallback(Resultats);
        google.charts.setOnLoadCallback(Score);
        google.charts.setOnLoadCallback(conso);
        google.charts.setOnLoadCallback(Sol);

        let map = document.querySelector('#map')

        let paths = map.querySelectorAll('.map__image a')


        //POlyfill du foreach
        if (NodeList.prototype.forEach === undefined) {
            NodeList.prototype.forEach = function (callback) {
                [].forEach.call(this, callback);
            };
        }

        let activeArea = function (id) {
            map.querySelectorAll('.is-active').forEach(function (item) {
                item.classList.remove('is-active');
            });

            if (id !== undefined) {
                document.querySelector("#" + id).classList.add('is-active');
            }
        }

        paths.forEach(function (path) {
            path.addEventListener('mouseenter', function () {
                activeArea(this.id);
            });
        });


        map.addEventListener('mouseover', function () {
            activeArea();
        });


        let listeTransfert = [];
        let couleurs = ["#ffffcc", "#d9f0a3", "#addd8e", "#78c679", "#5ace7d", "#5b8615"];
        for (const k in resultsData.transfert) {
            listeTransfert.push(resultsData.transfert[k]);
        }
        let min = Math.min(...listeTransfert);
        let max = Math.max(...listeTransfert);
        let coeff = (max - min) / 6;


        for (const k in resultsData.transfert) {
            let v = resultsData.transfert[k];

            for (let i = 0; i < couleurs.length; i++) {
                if (v >= min + i * coeff && v <= min + (i + 1) * coeff) {
                    $(`#${k}`).css("fill", couleurs[i]);
                }
            }
        }

        creerLegende(couleurs, min, coeff);


        $("#turn").text(`Tour ${(resultsData.annee.toString() - 2030) / 5 + 1} : Année ${(resultsData.annee.toString())}`);
    }


    $('#commitResults').click(() => {
        location.href = "/commit";
    });

    $('#retourResults').click(() => {
        location.href = "/manual";
    });


    // DEBUT EXECUTION PAGE

    $.ajax({
        url: "/get_mix",
        type: "GET",
        dataType: "json",
        success: function (data, textStatus, jqXHR) {
            mixData = data;
            $.ajax({
                url: "/get_results",
                type: "GET",
                dataType: "json",
                success: function (data, textStatus, jqXHR) {
                    resultsHistory = data;
                    resultsData = data[mixData.annee.toString()];
                    fillPage();
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    displayError("http", errorThrown);
                }
            });
        },
        error: function (jqXHR, textStatus, errorThrown) {
            displayError("http", errorThrown);
        }
    });
    $("#results").fadeIn();


});

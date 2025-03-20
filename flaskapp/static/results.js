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
            resultsData.puissancePhs+
            resultsData.puissanceEau);


        let result1 = google.visualization.arrayToDataTable([['Technologie', 'Pourcentage', 'Unité'],
            ['ONshore', resultsData.puissanceEolienneON, 'GW'],
            ['OFFshore', resultsData.puissanceEolienneOFF, 'GW'],
            ['Batterie', resultsData.puissanceBatterie, 'GW'],
            ['Nucléaire', resultsData.puissanceNucleaire, 'GW'],
            ['PV', resultsData.puissancePV, 'GW'],
            ['Hydrau', resultsData.puissanceEau + resultsData.puissancePhs, 'GW'],
            ['Gaz2power', resultsData.puissanceGaz, 'GW']
        ]);

        let options = {
            title: 'Puissance installée' + " : " + Math.round(TotalP) + " GW"
        };


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
        let table = [['Année', 'ONshore', 'OFFshore', 'Batterie', 'Nucléaire',
            'PV', 'Riv+Lacs', 'Step', 'Gaz2power', {role: 'annotation'}]];


        for (let year in resultsHistory) {
            let line = [];
            line.push(year);
            line.push(resultsHistory[year].prodOnshore);
            line.push(resultsHistory[year].prodOffshore);
            line.push(resultsHistory[year].prodBatterie);
            line.push(resultsHistory[year].prodNucleaire);
            line.push(resultsHistory[year].prodPv);
            line.push(resultsHistory[year].prodEau);
            line.push(resultsHistory[year].prodPhs);
            line.push(resultsHistory[year].prodGaz);
            line.push("");
            table.push(line)
        }
        ;
        let resultamoi = google.visualization.arrayToDataTable(table);


        let options = {
            width: 600,
            title: 'Production électrique par technologie : ' + Math.round(resultsData.production/1000) + " TWh/an",
            height: 400,
            legend: {position: 'right'},
            bar: {groupWidth: '75%'},
            isStacked: true,
        };


        let chart = new google.visualization.ColumnChart(document.getElementById('Combine_div'));
        chart.draw(resultamoi, options);
    }

    function Prod() {
        let result2 = google.visualization.arrayToDataTable([
            ['Technologie', 'Production'],
            ['ONshore', resultsData.prodOnshore],            // RGB value
            ['OFFshore', resultsData.prodOffshore],            // English color name
            ['Batterie', resultsData.prodBatterie],
            ['Nucléaire', resultsData.prodNucleaire],
            ['PV', resultsData.prodPv],
            ['Riv. + Lacs', resultsData.prodEau],
            ['Step', resultsData.prodPhs],
            ['Gaz 2 Power', resultsData.prodGaz]
            // CSS-style declaration
        ]);

        let options = {
            title: 'Production électrique (en GWh) : Total de ' + Math.round(resultsData.production/1000) + " TWh/an",
            legend: 'none'
        };

        let chart = new google.visualization.ColumnChart(document.getElementById("Bar_div"));
        chart.draw(result2, options);
    }

    function EmCO2() {
        let co2Array = [];
        let i = 0
        for (let year in resultsHistory) {
            co2Array.push(resultsHistory[year].co2);
        }

        let result3 = google.visualization.arrayToDataTable([
            ['Année', 'Emissions CO2', {role: "style"}],
            ['2025', 26494417/1e6, 'color : green'],
            ['2030', co2Array[0]/1e6, 'color : green'],
            ['2035', co2Array[1]/1e6, 'color : green'],
            ['2040', co2Array[2]/1e6, 'color : green'],
            ['2045', co2Array[3]/1e6, 'color : green'],
            ['2050', co2Array[4]/1e6, 'color : green']
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
            ['Heures', 'Pénuries', 'Surplus'],
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
        result5.addColumn('number', 'Pénuries');
        result5.addColumn('number', 'Surplus');

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
        const cout_construction = Number((resultsData.cout - resultsData.cout_gaz -resultsData.cout_uranium).toFixed(1));
        result6.addRows([
            ['Budget disponible', {v: resultsData.budget, f: resultsData.budget + ' Md€'}],
            ['Dépense totale', {v: resultsData.cout, f: resultsData.cout + ' Md€'}],
            ['-> Coût constructions', {v: cout_construction, f: cout_construction + ' Md€'}],
            ['-> Coût Gaz', {v: resultsData.cout_gaz, f: resultsData.cout_gaz + ' Md€'}],
            ['-> Coût Uranium', {v: resultsData.cout_uranium, f: resultsData.cout_uranium + ' Md€'}],
            ['_____________Bilan électrique______________', {v: 0, f: ''}],

            ['Demande électrique', {v: resultsData.demande, f: resultsData.demande + ' GWh/an'}],
            ['Production électrique', {v: resultsData.production, f: resultsData.production + ' GWh/an'}],
            ['Production - Demande électrique', {
                v: resultsData.production - resultsData.demande,
                f: resultsData.production - resultsData.demande + ' GWh/an'
            }],
            ["Nb d'heures de Pénuries", {v: resultsData.nbPenuries}],
            ["Nb d'heures de Surplus", {v: resultsData.nbSurplus}],
            ['_____________Bilan gaz______________', {v: 0, f: ''}],
            ['Demande Gaz (electrolyse H2) pour industrie (équivalent électrique)', {
                v: resultsData.electrolyse,
                f: resultsData.electrolyse + ' GWh/an'
            }],
            ['Demande Gaz pour électricité G2P (équivalent électrique)', {
                v: resultsData.demandeG2P,
                f: resultsData.demandeG2P + ' GWh/an'
            }],
            ['Production Gaz par electrolyse P2G (équivalent électrique)', {
                v: resultsData.GazElectrolyse,
                f: resultsData.GazElectrolyse + ' GWh/an'
            }],
            /*
            ['Variation stock P2G, G2P (stock debut - stock fin)', {
                v: resultsData.consoGaz,
                f: resultsData.consoGaz + ' GWh/an'
            }],*/
            ['Production Gaz par Bio/déchets (équivalent électrique)', {
                v: resultsData.biogaz,
                f: resultsData.biogaz + ' GWh/an'
            }],
            ['Gaz fossile brulé (équivalent électrique)', {
                v: resultsData.prodGazFossile,
                f: resultsData.prodGazFossile + ' GWh/an'
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

            divStr += `<span class="badge-pill" style="background-color: ${couleur};">
                            de ${debutIntervalle}  à ${finIntervalle} GWh/an </br></span>`
        }
        $("#legendeItem").html(divStr);
    }


    function fillPage() {
        // Load the Visualization API and the piechart package.
        google.load('visualization', '1.0', {'packages':['corechart']});
        google.charts.load('current', {'packages': ['table']});
        google.charts.load('current', {'packages': ['corechart']});
        google.charts.load('current', {'packages': ['geochart']}, {mapsApiKey: 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'});

        google.charts.setOnLoadCallback(PuissanceInst);
        google.charts.setOnLoadCallback(Prod);
        google.charts.setOnLoadCallback(EmCO2);
        google.charts.setOnLoadCallback(PenSurBar1);
        google.charts.setOnLoadCallback(PenSurBar2);
        google.charts.setOnLoadCallback(Resultats);
        //google.charts.setOnLoadCallback(Score);
        google.charts.setOnLoadCallback(conso);
        //google.charts.setOnLoadCallback(Sol);

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
        //let couleurs = ["#ffffcc", "#d9f0a3", "#addd8e", "#78c679", "#5ace7d", "#5b8615"];
        let couleurs = ["#2980b9", "#58d68d", "#f1c40f ", "#eb984e", "#e74c3c", "#8e44ad"];

        for (const k in resultsData.transfert) {
            listeTransfert.push(resultsData.transfert[k]);
        }
        let min = Math.min(...listeTransfert);
        let max = Math.max(...listeTransfert);
        let coeff = (max - min) / 6. * 1.001;


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
        if ((annee_int - 5).toString() in resultsHistory) document.getElementById('previousYear').disabled=false;
        else document.getElementById('previousYear').disabled=true;

        let nextannee = (annee_int + 5).toString()
        if ($.isEmptyObject(resultsHistory[nextannee])) document.getElementById('nextYear').disabled=true;
        else document.getElementById('nextYear').disabled=false;

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

    // DEBUT EXECUTION PAGE
    $.ajax({
        url: "/get_results/"+equipe+"/"+partie,
        type: "GET",
        dataType: "json",
        success: function (data, textStatus, jqXHR) {
            resultsHistory = data;
            resultsData = data[annee];
            fillPage();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            displayError("http", errorThrown);
        }
    });

    $("#results").fadeIn();


});

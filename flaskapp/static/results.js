var largeur = "1200";
var demi_largeur = "600";
var hauteur = "600";
var demi_hauteur = "300";


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
        title: 'Puissance installée' + " : " + Math.round(TotalP) + " GW",
        width: demi_largeur,
        height:hauteur
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
        width:'1000',
        height:'500',
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
        width: demi_largeur,
        title: 'Production électrique par technologie : ' + Math.round(resultsData.production/1000) + " TWh/an",
        height: hauteur,
        legend: {position: 'right'},
        bar: {groupWidth: '80%'},
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
        height: hauteur,
        width: largeur,
        legend: 'none'
    };

    let chart = new google.visualization.ColumnChart(document.getElementById("Bar_div"));
    chart.draw(result2, options);
}

function EmCO2() {
    let co2Array = [];
    let i = 0
    co2Array.push(['Année', 'Emissions CO2', {role: "style"}]);
    co2Array.push(['2017', 26.6, 'color : green']);
    for (let year in resultsHistory) {
        co2Array.push([year, resultsHistory[year].co2/1e6, 'color : green']);
    }

    let result3 = google.visualization.arrayToDataTable(co2Array);

    let options = {
        title: 'Emissions de CO2 (en Millions de tonnes de CO2)',
        width: largeur,
        height: hauteur,
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
        width: largeur,
        height: demi_hauteur,
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
        width: largeur,
        height: demi_hauteur,
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
    //const cout_construction = Number((resultsData.cout - resultsData.cout_gaz -resultsData.cout_uranium).toFixed(1));
    result6.addRows([
        ['Budget disponible', {v: resultsData.budget, f: resultsData.budget + ' Md€'}],
        ['Dépense totale', {v: resultsData.cout, f: resultsData.cout + ' Md€'}],
        ['-> Coût constructions', {v: resultsData.cout_construction, f: resultsData.cout_construction + ' Md€'}],
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
        width:'1000',
        height:'500',
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

        if (i==0){
            divStr += `<span class="badge-pill" style="background-color: ${couleur};">
                        Moins de ${finIntervalle}  %</br></span>`
                        }
        else{
            if (i == couleur.length-2){
                divStr += `<span class="badge-pill" style="background-color: ${couleur};">
                        ${debutIntervalle}% et plus</br></span>`
                        }
            else{
                divStr += `<span class="badge-pill" style="background-color: ${couleur};">
                        de ${debutIntervalle}  à ${finIntervalle}  </br></span>`
                }
        }
    }
    $("#legendeItem").html(divStr);
}

function Carte_Equilibre(){
   let listeTransfert = [];
    //let couleurs = ["#ffffcc", "#d9f0a3", "#addd8e", "#78c679", "#5ace7d", "#5b8615"];
    let couleurs = ["#2944ad", "#2980b9",  "#58d68d", "#f1c40f ","#eb984e", "#e74c3c"];

    let annee_ref = "2025"
    if (resultsHistory[annee_ref] === undefined){
        annee_ref = annee
    }
    let transfert_ref = resultsHistory[annee_ref].transfert


    for (const k in resultsData.transfert) {
        listeTransfert[k]=(resultsData.transfert[k]-transfert_ref[k])/transfert_ref[k]*100.;
    }
    let min = Math.min(...Object.values(listeTransfert));
    let max = Math.max(...Object.values(listeTransfert));
    min= -150.
    max= 150.
    let coeff = 60;


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
        let v = listeTransfert[path.id];
        let p = resultsData.transfert[path.id];
        path.setAttribute("data-toggle", "tooltip")
        path.setAttribute("data-bs-html", "true")
        path.setAttribute("title", "De " + Math.round(transfert_ref[path.id]*10000.)/10. + " MWh/hab (en 2025) <br>  à " + Math.round(p*10000.)/10. + " MWh/hab <br>" + (v<0?"":"+")+ Math.round(v) + "%")

        path.addEventListener('mouseenter', function () {
            activeArea(this.id);

        });


        for (let i = 0; i < couleurs.length; i++) {
            if (v >= min + i * coeff && v <= min + (i + 1) * coeff) {
                path.style.fill = couleurs[i];
            }
            if (v < min ) {
                path.style.fill = couleurs[0];
            }
            if (v > max ) {
                path.style.fill = couleurs[couleurs.length-1];
            }
        }
    });


    map.addEventListener('mouseover', function () {
        activeArea();
    });

    /*
    for (const k in listeTransfert) {
        let v = listeTransfert[k];

        for (let i = 0; i < couleurs.length; i++) {
            if (v >= min + i * coeff && v <= min + (i + 1) * coeff) {
                $(`#${k}`).css("fill", couleurs[i]);
            }
        }
    }
    */

    creerLegende(couleurs, min, coeff);


}
function fillPage() {

    PuissanceInst();
    Prod();
    EmCO2();
    PenSurBar1();
    PenSurBar2();
    Resultats();
    //Score();
    conso();
    //(Sol);

    Carte_Equilibre();



    $("#turn").text(`Tour ${(resultsData.annee.toString() - 2030) / 5 + 1} : Année ${(resultsData.annee.toString())}`);
    if ((annee_int - 5).toString() in resultsHistory) document.getElementById('previousYear').disabled=false;
    else document.getElementById('previousYear').disabled=true;

    let nextannee = (annee_int + 5).toString()
    if ($.isEmptyObject(resultsHistory[nextannee])) document.getElementById('nextYear').disabled=true;
    else document.getElementById('nextYear').disabled=false;

}





var gooIndex = document.getElementById('goo-index');


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

function lignes(div, champs) {

    // set the dimensions and margins of the graph
    let margin = { top: 50, right: 100, bottom: 50, left: 100 },
        width = 860 - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = div
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");


    let allGroup = liste;


    let parseTime = d3.timeParse("%Y");
    let years = annees.map((e) => parseTime(e));

    let datas = [];
    let time_domain = [years[0], years.slice(-1)[0]];
    let item = compilation[champs];
    let groupes = Object.keys(item);
    let first_key = groupes[0];
    y_domain = [item[first_key][0], item[first_key][0]];
    for (let key in item) {
        data = { "name": key, "values": [] };
        for (let i = 0; i < item[key].length; i++) {
            let val = item[key][i];
            if (val != null) {
                data.values.push(val
                );
                if (val < y_domain[0]) y_domain[0] = val;
                if (val > y_domain[1]) y_domain[1] = val;
            }
        }
        datas.push(data);
    }

    /* Reformat the data: we need an array of arrays of {x, y} tuples
    let datas = allGroup.map(function (grpName) { // .map allows to do something for each element of the list
        return {
            name: grpName,
            values: item[grpName]
        };
    }
    );
    */


    // I strongly advise to have a look to datas with
    console.log(datas);


    // A color scale: one color for each group
    let myColor = d3.scaleOrdinal()
        .domain(groupes)
        .range(d3.schemeSet2);


    // Add X axis --> it is a date format
    let xScale = d3.scaleTime()
        .domain(time_domain)
        .range([0, width]);

    let xAxis = d3.axisBottom(xScale)
        .ticks(d3.timeYear.every(5));

    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    // Add Y axis
    var yScale = d3.scaleLinear()
        .domain(y_domain)
        .range([height, 0]);
    svg.append("g")
        .call(d3.axisLeft(yScale));


    // Add the lines
    let line = d3.line()
        .x(function (d, i) { return xScale(years[i]) })
        .y(function (d) { return yScale(+d) });
    svg.selectAll("myLines")
        .data(datas)
        .enter()
        .append("path")
        .attr("class", function (d) { return d.name })
        .attr("d", function (d) { return line(d.values) })
        .attr("stroke", function (d) { return myColor(d.name) })
        .style("stroke-width", 4)
        .style("fill", "none");

    // Add the points
    svg
        // First we need to enter in a group
        .selectAll("myDots")
        .data(datas)
        .enter()
        .append('g')
        .style("fill", function (d) { return myColor(d.name) })
        .attr("class", function (d) { return d.name })
        // Second we need to enter in the 'values' part of this group
        .selectAll("myPoints")
        .data(function (d) { return d.values })
        .enter()
        .append("circle")
        .attr("cx", function (d, i) { return xScale(years[i]) })
        .attr("cy", function (d) { return yScale(+d) })
        .attr("r", 5)
        .attr("stroke", "white");

    // Add a label at the end of each line
    svg
        .selectAll("myLabels")
        .data(datas)
        .enter()
        .append('g')
        .append("text")
        .attr("class", function (d) { return d.name })
        .datum(function (d) { return { 
            name: d.name, 
            year: years[d.values.length - 1], 
            value: d.values[d.values.length - 1] }; }) // keep only the last value of each time series
        .attr("transform", function (d, i) { 
            return "translate(" + xScale(d.year) + "," + yScale(d.value) + ")"; }) // Put the text at the position of the last point
        .attr("x", 12) // shift the text a bit more right
        .text(function (d) { return d.name; })
        .style("fill", function (d) { return myColor(d.name) })
        .style("font-size", 15);

    /*/ Add a legend (interactive)
    
    svg
        .selectAll("myLegend")
        .data(datas)
        .enter()
        .append('g')
        .append("text")
        .attr('x', function (d, i) { return 30 + i * 200 })
        .attr('y', function (d, i) { return 108})
        .text(function (d) { return d.name; })
        .style("fill", function (d) { return myColor(d.name) })
        .style("font-size", 15)
        .on("click", function (d) {
            // is the element currently visible ?
            currentOpacity = d3.selectAll("." + d.name).style("opacity")
            // Change the opacity: from 0 to 1 or from 1 to 0
            d3.selectAll("." + d.name).transition().style("opacity", currentOpacity == 1 ? 0 : 1)
        });
        */
};

function hoverEnter(index){
    let nowVisible = document.getElementById('screen_' + index);
    gooIndex.style.top = 60  * index + 'px';
    let allScreens = document.querySelectorAll('.screen');
    allScreens.forEach(e => {
        e.classList.remove('visible')
    })
    
    nowVisible.classList.add('visible');
}

function fillPage() {

    lignes(d3.select("#graphe_couts"),"cout");
    lignes(d3.select("#graphe_co2"),"co2");
    lignes(d3.select("#graphe_gaz"),"prodGazFossile");
    lignes(d3.select("#graphe_nuke"),"puissanceNucleaire");
    if ("puissanceEolienneTotale" in compilation) lignes(d3.select("#graphe_eolien"),"puissanceEolienneTotale");
    lignes(d3.select("#graphe_pv"),"puissancePV");
    if ("equilibreEnrNucleaire" in compilation) lignes(d3.select("#graphe_equilibre"),"equilibreEnrNucleaire");
    lignes(d3.select("#graphe_penuries"),"nbPenuries");

}

 $(function () {
      

      fillPage();

      $("#graphe_couts").fadeIn();

   });



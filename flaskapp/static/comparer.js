var [liste_court, commun] = raccourcir_liste(liste);

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
    let margin = { top: 90, right: 200, bottom: 50, left: 100 };
    
    // Get the container's width
    let containerWidth = div.node().getBoundingClientRect().width;
    let width = containerWidth - margin.left - margin.right;
    if (width <0) width = 0;
    let height = Math.min(700, width * 0.7) - margin.top - margin.bottom; // maintain aspect ratio

    // append the svg object to the body of the page
    var svg = div
        .append("svg")
        .attr("viewBox", "0 0 " + (width + margin.left + margin.right) + " " + (height + margin.top + margin.bottom))
        .attr("preserveAspectRatio", "xMidYMid meet")
        .style("width", "100%")
        .style("height", "auto")
    .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    let parseTime = d3.timeParse("%Y");
    let years = annees.map((e) => parseTime(e));

    let datas = [];
    let time_domain = [years[0], years.slice(-1)[0]];
    let item = compilation[champs];
    let first_key = liste[0];
    y_domain = [item[first_key][0], item[first_key][0]];
    for (let k=0; k<liste_court.length; k++) {
        data = { "name": liste_court[k], "values": [] };
        for (let i = 0; i < item[liste[k]].length; i++) {
            let val = item[liste[k]][i];
            if (val != null) {
                data.values.push(val
                );
                if (val < y_domain[0]) y_domain[0] = val;
                if (val > y_domain[1]) y_domain[1] = val;
            }
        }
        if (data["values"].length>0) datas.push(data);
    };

    // I strongly advise to have a look to datas with

    // A color scale: one color for each group
    let myColor = d3.scaleOrdinal()
        .domain(liste_court)
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

    svg
        .selectAll("myLegend")
        .data(datas)
        .enter()
        .append('g')
        .append("text")
        .attr('x', function (d, i) { return 30 + (i%4) * 150 })
        .attr('y', function (d, i) { return -15 - 15* Math.floor(i/4)})
        .text(function (d) { return d.name; })
        .style("fill", function (d) { return myColor(d.name) })
        .style("font-size", 15)
        .on("click", function (d) {
            // is the element currently visible ?
            current = d3.selectAll("." + this.getHTML());
            // Change the opacity: from 0 to 1 or from 1 to 0
            current.transition().style("opacity", current.style("opacity") == '1' ? '0' : '1');
        });
};

function hoverEnter(index, gooIndex){
    let nowVisible = document.getElementById('screen_' + index);
    const menuWrapper = document.querySelector('.menu-wrapper');
    const menuItem = document.querySelector(`.menu ul li:nth-child(${index + 1})`);
    
    // Get the actual position of the menu item relative to the viewport
    const menuItemRect = menuItem.getBoundingClientRect();
    const menuWrapperRect = menuWrapper.getBoundingClientRect();
    
    // Calculate position relative to menu wrapper
    const position = menuItemRect.top - menuWrapperRect.top;
    
    // Set position using transform for better performance
    gooIndex.style.transform = `translateY(${position}px)`;
    
    //const position = getCssVariable("--navbar-height", true) + (getCssVariable("--taille", true) * index);
    //gooIndex.style.top = position + 'px';
    
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

function raccourcir_liste(liste){

    let court = ["_"];
    let commun = liste[0].split('_');
    let mots = [];
    let L = commun.length;
    for(let i=0; i < liste.length; i++){
        mots[i] = liste[i].split('_');
        court[i]="_";
        for(let w=0; w < L; w++){
            if (mots[i][w] != commun[w]) {
                commun[w]='';
            };
        };
    };
    for(let w=0; w<L; w++){
        if (commun[w]==""){
            for(let i=0; i < liste.length; i++){
                court[i] += mots[i][w]+'_';
            };
        };   
    };

    for(let i=0; i < liste.length; i++){
        court[i]=court[i].slice(1,-1);
    };
    return [court, commun];
};

// Get CSS variable value helper function
function getCssVariable(varName, asNumber = false) {
    const value = getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
    if (asNumber) {
        return parseInt(value) || 0; // returns just the number without units, defaults to 0 if parsing fails
    }
    return value;
}

// Update navbar height CSS variable
function updateNavbarHeight() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        const navbarHeight = navbar.offsetHeight;
        document.documentElement.style.setProperty('--navbar-height', `${navbarHeight}px`);
    }
}

// Call it once when the page loads
document.addEventListener('DOMContentLoaded', updateNavbarHeight);
// Also call it when the window is resized
window.addEventListener('resize', updateNavbarHeight);

 $(function () {
    var gooIndex = document.getElementById('goo-index');
    
    hoverEnter(2, gooIndex);
    
    // Add hover handlers to menu items
    $('.menu ul li').hover(function() {
        const index = $(this).index();
        hoverEnter(index, gooIndex);
    });


    fillPage();
    //$("#graphe_couts").fadeIn();
});



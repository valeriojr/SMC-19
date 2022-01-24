function bringToTop(targetElement) {
    // put the element at the bottom of its parent
    let parent = targetElement.parentNode;
    parent.appendChild(targetElement);
}

var selected;
var zommLevel = "state";

function clicked(d) {
    var xCenter, yCenter, k;

    if (d && centered !== d) {
        var centroid = path.centroid(d);
        xCenter = centroid[0];
        yCenter = centroid[1];
        k = 7;
        centered = d;
        d3.select(this)
            .classed("selected", true);
        d3.select(selected).classed("selected", false);
        selected = this;

        $("#location-name").html(d.properties.name);
    } else {
        xCenter = width / 2;
        yCenter = height / 2;
        k = 1;
        centered = null;
        d3.select(selected).classed("selected", false);

        $("#location-name").html("Alagoas");
    }

    g.selectAll("path")
        .classed("active", centered && function (d) {
            return d === centered;
        });

    g.selectAll(".mark")
        .transition()
        .duration(750)
        .attr("transform", function (d) {
            var t = getTranslation(d3.select(this).attr("transform"));
            return "translate(" + t[0] + "," + t[1] + ")scale(" + 1 / k + ")";
        });

    g.transition()
        .duration(750)
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -xCenter + "," + -yCenter + ")")
        .style("stroke-width", 1.5 / k + "px");
    // .on("end", function () {
    //     if (zommLevel === "state") {
    //         //d3.selectAll("svg > *").remove();
    //         zommLevel = "city";
    //         // plotMap({
    //         //     dataSrc: "/static/data/bairrosgeojson.geojson",
    //         //     center: [xCenter, yCenter],
    //         //     featureName: "Bairro",
    //         //     scale: k * 13000
    //         // });
    //     }
    // });
}

function tooltipTextFocused(data, featureName, d, total) {
    if (featureName == "name") {
        var confirmed, suspect, deaths, confirmedRate, suspectRate, mortality;
        const location = d.properties[featureName];

        suspect = confirmed = deaths = "-";
        suspectRate = confirmedRate = mortality = "";

        if (data[d.properties[featureName]]) {
            suspect = data[location]["suspect_cases"] !== undefined ? data[location].suspect_cases : "-";
            confirmed = data[location]["confirmed_cases"] !== undefined ? data[location].confirmed_cases : "-";
            deaths = data[location]["deaths"] !== undefined ? data[location].deaths : "-";

            suspectRate = total.suspect_cases ? "(" + (100 * suspect / total.suspect_cases).toFixed(1) + "%)" : "";
            confirmedRate = total.confirmed_cases ? "(" + (100 * confirmed / total.confirmed_cases).toFixed(1) + "%)" : "";
            mortality = total.deaths ? "(" + (100 * deaths / total.deaths).toFixed(1) + "%)" : "";
        }

        return `<div class="row-col">` +
            `<strong>${location}</strong>` +
            `<div>Suspeitos: <span class="text-info">${suspect} ${suspectRate}</div>` +
            `<div>Confirmados: <span class="text-warning">${confirmed} ${confirmedRate}</div>` +
            `<div>Mortes: <span class="text-danger">${deaths} ${mortality}</span></div>` +
            `</div>`;
    } else {
        var formatted = (o, t) => {
            return o + "/" + t + " (" + parseInt(100 * o / t) + "%)";
        }
        var tooltipScale = d3.scaleLinear().domain([0.0, 0.5, 1.0]).range(["green", "yellow", "red"]);
        const status = d.healthCenterStatus;

        return `<div class="row-col">` +
            `<strong>${d.healthCenterName}</strong>` +
            `<div>Leitos RET: <span style="color:${tooltipScale(status.occupiedBeds / status.beds)}"> ${formatted(status.occupiedBeds, status.beds)} </div>` +
            `<div>Leitos UTI: <span style="color:${tooltipScale(status.occupiedIntensiveCareUnits / status.intensiveCareUnits)}"> ${formatted(status.occupiedIntensiveCareUnits, status.intensiveCareUnits)} </div>` +
            `<div>Respiradores: <span style="color:${tooltipScale(status.occupiedRespirators / status.respirators)}"> ${formatted(status.occupiedRespirators, status.respirators)} </div>` +
            `</div>`;
    }
}

function tooltipMouseover(t, d, options) {
    d3.select(t)
        .classed("active", true);
    bringToTop(t);
    tooltipDiv.transition()
        .duration(10)
        .style("opacity", .9);

    var tooltipText = tooltipTextFocused(cities, options.featureName, d, data.total);

    tooltipDiv.html(tooltipText)
        .style("left", (d3.event.pageX + 25) + "px")
        .style("top", (d3.event.pageY - 100) + "px");
}

function tooltipMouseout(t) {
    d3.select(t)
        .classed("active", false);
    tooltipDiv.transition()
        .duration(10)
        .style("opacity", 0);
    tooltipDiv
        .style("left", (d3.event.pageX) + "px")
        .style("top", (d3.event.pageY - 28) + "px")
        .html("");
}

function cityFill(d, options) {
    city = cities[d.properties[options.featureName]];

    if (cities[d.properties[options.featureName]]) {
        // console.log(d);
        const r = ((city.suspect_cases + city.confirmed_cases + city.deaths) /
            (data.total.suspect_cases + data.total.confirmed_cases + data.total.deaths));
        const gb = 255 * r;
        return `rgb(255, ${225 - gb}, ${225 - gb})`;
    } else {
        return "light gray";
    }
}

var width = $("#map").width(),
    height = $("#map").height(),
    centered;

var cities;
var projection;
var path;
var svg;
var g;
// Define the div for the tooltip
var tooltipDiv;
var legend;
//var territory_stats
//var health_center_stats

var onlyColor = true;
const circleColorScale = d3.interpolateReds;
const minRadius = 1, maxRadius = 15;

$.getJSON("/static/data/municipios.json", function (municipios) {
    function plotMap(territoryData, healthCentersOptions) {
        svg = d3.select('#map').append('svg')
            .attr('width', width)
            .attr('height', height);

        projection = d3.geoMercator().scale(1);

        path = d3.geoPath().projection(projection);

        projection.fitExtent([[0, 0], [width, height]], municipios);

        g = svg.append("g");

        data = territory_stats;

        cities = data.cities;

        var healthCenterData = health_center_stats;

        g.append("g")
            .selectAll(".landmap")
            .data(municipios.features)
            .enter().append("path").attr("class", "landmap")
            .attr("d", path)
            .style("fill", function (d) {
                return cityFill(d, territoryData);
            })
            .on("mouseover", function (d) {
                tooltipMouseover(this, d, territoryData);
            })
            .on("mouseout", function (d) {
                tooltipMouseout(this, d, territoryData);
            });

        tooltipDiv = d3.select("body").append("div")
            .attr("class", "tooltipa");

        g.append("g")
            .selectAll(".mark") //adding mark in the group
            .data(healthCenterData)
            .enter()
            .append("circle")
            .attr("class", "mark")
            .attr("r", 0)
            .style("fill", function (d) {
                return circleColorScale(
                    d.healthCenterStatus.occupiedBeds / d.healthCenterStatus.beds
                );
            })
            .attr("cx", function (d) {
                return projection([d.longitude, d.latitude])[0];
            })
            .attr("cy", function (d) {
                return projection([d.longitude, d.latitude])[1];
            })
            .on("mouseover", function (d) {
                if (onlyColor) {
                    d3.select(this)
                        .transition()
                        .duration(750)
                        .attr("r", 2 * minRadius);
                }

                tooltipMouseover(this, d, healthCentersOptions);
            })
            .on("mouseout", function (d) {
                if (onlyColor) {
                    d3.select(this)
                        .transition()
                        .duration(750)
                        .attr("r", minRadius);
                }

                tooltipMouseout(this, d, healthCentersOptions);
            });

        var zoom = d3.zoom()
            .scaleExtent([1, 16])
            .on('zoom', function () {
                g.selectAll('path')
                    .attr('transform', d3.event.transform);
                g.selectAll('.mark')
                    .attr('transform', d3.event.transform);
            });

        svg.call(zoom);
    }


    state = {
        dataSrc: "data/geojs-27-mun.geojson",
        center: [-36.1, -9.6],
        featureName: "name",
        scale: 13000
    };

    health_centers = {
        dataSrc: "data/unidadesdesaude.json",
        center: [-36.3, -9.5],
        featureName: "Nome",
        scale: 13000
    };

    plotMap(state, health_centers);

});

function updateResourceVisualization() {
    var reSel = document.getElementById("resource-select"),
        reVal = reSel.options[reSel.selectedIndex].value,
        visSel = document.getElementById("visualization-select"),
        visVal = visSel.options[visSel.selectedIndex].value;

    const resourceData = {
        "RET": (d) => {
            return d.healthCenterStatus.occupiedBeds / d.healthCenterStatus.beds;
        },
        "UTI": (d) => {
            return d.healthCenterStatus.occupiedIntensiveCareUnits / d.healthCenterStatus.intensiveCareUnits;
        },
        "RES": (d) => {
            return d.healthCenterStatus.occupiedRespirators / d.healthCenterStatus.respirators;
        }
    }

    if (visVal == "COLOR") {
        onlyColor = true;
        d3.selectAll(".mark")
            .transition()
            .duration(1000)
            .attr("r", minRadius)
            .style("fill", function (d) {
                return circleColorScale(resourceData[reVal](d));
            })
            .style("opacity", 1);
    } else {
        onlyColor = false;
        d3.selectAll(".mark")
            .transition()
            .duration(1000)
            .attr("r", function (d) {
                return maxRadius * resourceData[reVal](d);
            }).style("fill", function (d) {
            return circleColorScale(resourceData[reVal](d));
        }).style("opacity", .7);
    }
}

document.getElementById('update-visualization').onclick = updateResourceVisualization;

function updateVisualization(selectedData) {
    if (selectedData == "RESOURCES") {
        d3.selectAll(".landmap")
            .transition()
            .duration(1000)
            .style("fill", $("#path").fill);
        updateResourceVisualization();
    } else {
        d3.selectAll(".landmap")
            .transition().duration(1000)
            .style("fill", function (d) {
                return cityFill(d, state);
            });

        d3.selectAll(".mark")
            .transition().duration(1000)
            .attr("r", 0);
    }
}

d3.json("https://cdn.jsdelivr.net/npm/d3-time-format@2/locale/pt-BR.json", function(error, locale) {
if (error) throw error;

d3.timeFormatDefaultLocale(locale);

});

function encodeQueryData(data) {
    const ret = [];
    for (let d in data)
        ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(data[d]));
    return ret.join('&');
    }

function verGrafico() {
    $('#svg_id').remove()

    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 60},
        width = 960 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#my_dataviz")
        .append("svg")
        .attr('id', 'svg_id')
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");

    let cidade = $('#cidade_id').val()
    let bairro = $('#bairro_id').val()
    let status = $('#status_id').val()
    let data_inicial = $('#inicial_id').val()
    let data_final = $('#final_id').val()

    params = {
        'CIDADE':cidade,
        'BAIRRO':bairro,
        'STATUS': status,
        'INICIAL': data_inicial,
        'FINAL': data_final,
        'ver_grafico':'ok'
    }

    //Read the data
    var url = "http://127.0.0.1:8000/evolution/data?".concat(encodeQueryData(params))

    d3.csv(url,

    // When reading the csv, I must format variables:
    function(d){
    return { date : d3.timeParse("%Y-%m-%d")(d.date), value : d.value }
    },

    // Now I can use this dataset:
    function(data) {

    // Add X axis --> it is a date format
    var x = d3.scaleTime()
        .domain(d3.extent(data, function(d) { return d.date; }))
        .range([ 0, width ]);
    xAxis = svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, d3.max(data, function(d) { return +d.value; })])
        .range([ height, 0 ]);
    yAxis = svg.append("g")
        .call(d3.axisLeft(y));

    // Add a clipPath: everything out of this area won't be drawn.
    var clip = svg.append("defs").append("svg:clipPath")
        .attr("id", "clip")
        .append("svg:rect")
        .attr("width", width )
        .attr("height", height )
        .attr("x", 0)
        .attr("y", 0);

    // Add brushing
    var brush = d3.brushX()                   // Add the brush feature using the d3.brush function
        .extent( [ [0,0], [width,height] ] )  // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
        .on("end", updateChart)               // Each time the brush selection changes, trigger the 'updateChart' function

    // Create the line variable: where both the line and the brush take place
    var line = svg.append('g')
        .attr("clip-path", "url(#clip)")

    // Add the line
    line.append("path")
        .datum(data)
        .attr("class", "line")  // I add the class line to be able to modify this line later on.
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
        .x(function(d) { return x(d.date) })
        .y(function(d) { return y(d.value) })
        )

    // Add the brushing
    line
        .append("g")
        .attr("class", "brush")
        .call(brush);

    // A function that set idleTimeOut to null
    var idleTimeout
    function idled() { idleTimeout = null; }

    // A function that update the chart for given boundaries
    function updateChart() {

        // What are the selected boundaries?
        extent = d3.event.selection

        // If no selection, back to initial coordinate. Otherwise, update X axis domain
        if(!extent){
        if (!idleTimeout) return idleTimeout = setTimeout(idled, 350); // This allows to wait a little bit
        x.domain([ 4,8])
        }else{
        x.domain([ x.invert(extent[0]), x.invert(extent[1]) ])
        line.select(".brush").call(brush.move, null) // This remove the grey brush area as soon as the selection has been done
        }

        // Update axis and line position
        xAxis.transition().duration(1000).call(d3.axisBottom(x))
        line
            .select('.line')
            .transition()
            .duration(1000)
            .attr("d", d3.line()
            .x(function(d) { return x(d.date) })
            .y(function(d) { return y(d.value) })
            )
    }

    // If user double click, reinitialize the chart
    svg.on("dblclick",function(){
        x.domain(d3.extent(data, function(d) { return d.date; }))
        xAxis.transition().call(d3.axisBottom(x))
        line
        .select('.line')
        .transition()
        .attr("d", d3.line()
            .x(function(d) { return x(d.date) })
            .y(function(d) { return y(d.value) })
        )
    });

    })
}

window.onload = function () {
    $('#ver_grafico_id').click(verGrafico)
    $('#ver_grafico_id').click()

    $.getJSON('http://127.0.0.1:8000/evolution/data?'.concat(encodeQueryData({'CIDADE':'ELEMENTOS', 'popular_select': 'ok'})), function(data) {
        //data is the JSON string
        for(var i = 0; i < data.length; i++) {
            var obj = data[i];
            $("#cidade_id").append($("<option />").val(obj.value).text(obj.text));
        }
    });

    $("#cidade_id").on("change", function() {
        $("#bairro_id").empty()

        params = {'UF':$("#uf_id").val(), 'CIDADE': $("#cidade_id").val(), 'BAIRRO': 'ELEMENTOS', 'popular_select': 'ok'}

        $.getJSON('http://127.0.0.1:8000/evolution/data?'.concat(encodeQueryData(params)), function(data) {
        //data is the JSON string
        for(var i = 0; i < data.length; i++) {
            var obj = data[i];
            $("#bairro_id").append($("<option />").val(obj.value).text(obj.text));
        }
        });
    });
}
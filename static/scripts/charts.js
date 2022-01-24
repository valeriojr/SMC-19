const defaultOptions = {
    margin: {
        left: 20,
        top: 20,
        right: 20,
        bottom: 20,
    },
    xAxis: {
        label: "",
        tickRotation: 0,
        tickTextAnchot: "middle"
    },
    yAxis: {
        label: ""
    },
    innerRadius: 0,
    colors: ["steelblue"],
    tooltipFormat: function(d){
        return `${d.value}`;
    },
    clear: true,
};

function barChart(selector, data, options) {
    const element = $(selector);

    options = {...defaultOptions, ...options};

    if(options.clear){
        d3.selectAll(`${selector} > *`).remove();
    }

    const totalWidth = element.width();
    const totalHeight = element.height();
    const margin = options.margin;

    const width = (options.width === undefined) ? totalWidth - (margin.left + 2 * margin.right) : options.width;
    const height = (options.height === undefined) ? totalHeight - 2 * (margin.top + margin.bottom) : options.height;

    const x = d3.scaleBand().range([0, width]).padding(0.5);
    const y = d3.scaleLinear().range([height, 0]);
    const color = d3.scaleOrdinal().range(options.colors);
    const svg = d3.select(selector)
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${margin.left + (options.yAxis.label ? 10 : 0)}, ` +
            `${margin.top + (options.title ? margin.top : 0)})`);

    x.domain(data.map(function (d) {
        return d.label;
    }));
    y.domain([0, d3.max(data, function (d) {
        return d.value;
    })]);

    svg.selectAll("bar")
        .data(data)
        .enter()
        .append("rect")
        .attr("width", width - margin.left - 2 * margin.right)
        .attr("height", height - margin.top - 2 * margin.bottom)
        .attr("class", options.barCssClass)
        .attr("x", function (d) {
            return x(d.label) + margin.left;
        })
        .attr("width", x.bandwidth())
        .attr("y", height)
        .attr("height", 0)
        .style("fill", function (d, i) {
            return color(i);
        })
        .transition()
        .duration(1000)
        .attr("y", function (d) {
            return y(d.value);
        })
        .attr("height", function (d) {
            return height - y(d.value);
        });

    svg.append("g")
        .attr("transform", `translate(${margin.left}, ${height})`)
        .call(d3.axisBottom(x)).selectAll("text")
        .attr("transform", `rotate(-${options.xAxis.tickRotation})`)
        .style("text-anchor", options.xAxis.tickTextAnchor);

    svg.append("text")
        .attr("transform", `translate(${(width + (margin.left + margin.right)) / 2}, ${height + 2 * margin.bottom})`)
        .style("text-anchor", "middle")
        .text(options.xAxis.label);

    svg.append("g")
        .attr("transform", `translate(${margin.left}, 0)`)
        .call(d3.axisLeft(y));

    svg.append("text")
        .attr("transform", `rotate(-90)`)
        .attr("y", -margin.left / 2)
        .attr("x", -(height / 2 + margin.top))
        .attr("dx", "1em")
        .style("text-anchor", "middle")
        .text(options.yAxis.label);

    // Title
    svg.append("text")
        .attr("transform", `translate(${width / 2}, -${margin.top})`)
        .style("font-weight", "bold")
        .style("text-anchor", "middle")
        .text(options.title);
}

function pieChart(selector, data, options) {
    const element = $(selector);
    d3.selectAll(`${selector} > *`).remove();
    options = {...defaultOptions, ...options};

    const totalWidth = element.width();
    const totalHeight = element.height();
    const margin = options.margin;

    const width = (options.width === undefined) ?
        totalWidth - (margin.left + margin.right) : options.width;
    const height = (options.height === undefined) ?
        totalHeight - (1 * margin.top + margin.bottom) : options.height;
    const outerRadius = options.outerRadius === undefined ?
        (Math.min(width, height) - (2 * margin.top + margin.bottom)) / 2 : options.outerRadius;

    const color = d3.scaleOrdinal().range(options.colors);
    const arc = d3.arc()
        .outerRadius(outerRadius)
        .innerRadius(options.innerRadius);
    const labelArc = d3.arc()
        .innerRadius((options.innerRadius + outerRadius) / 2)
        .outerRadius((options.innerRadius + outerRadius) / 2);
    const pie = d3.pie()
        .sort(null)
        .value(function (d) {
            return d.value;
        });
    const percentage = d3.scaleLinear().range([0, 1]).domain([0, d3.sum(data, function (d) {
        return d.value;
    })]);
    const tooltip = d3.select("body").append("div")
        .attr("class", "tooltip text-light bg-dark rounded p-2")
        .style("opacity", 0);

    const svg = d3.select(selector)
        .attr("width", width + 2 * (margin.left + margin.right))
        .attr("height", height + 2 * (margin.left + margin.right))
        .append("g")
        .attr("transform", `translate(${outerRadius + margin.left}, ${outerRadius + 2 * (margin.top + (options.title ? margin.top : 0))})`)

    const g = svg.selectAll("arc")
        .data(pie(data))
        .enter()
        .append("g")
        .attr("class", "arc")
        .on("mouseover", function (d) {
            d3.select(this)
                .classed("active", true);
            tooltip.transition()
                .style("opacity", .9);
            tooltip.html(options.tooltipFormat(d))
                .style("left", `${d3.event.pageX}px`)
                .style("top", `${d3.event.pageY}px`);
        })
        .on("mouseout", function (d) {
            d3.select(this)
                .classed("active", false);
            tooltip.transition()
                .style("opacity", 0);
            tooltip.html("");
        });

    g.append("path")
        .attr("d", arc)
        .attr("class", options.arcCssClass ? options.arcCssClass : "")
        .style("fill", function (d, i) {
            return color(d.index)
        })
        .transition()
        .ease(d3.easeLinear)
        .duration(1000)
        .attrTween("d", function (d) {
            d.innerRadius = 0;
            const i = d3.interpolate({startAngle: 0, endAngle: 0}, d);
            return function (t) {
                return arc(i(t));
            }
        });

    // Labels
    g.append("text")
        .attr("transform", function (d) {
            return "translate(" + labelArc.centroid(d) + ")";
        })
        .style("fill", "white")
        .style("opacity", 0)
        .transition()
        .duration(2000)
        .style("opacity", 1)
        .style("text-anchor", "middle")
        .style("font-weight", "bold")
        .attr("dy", ".35em")
        .text(function (d) {
            return `${(100 * percentage(d.data.value)).toFixed(1)}%`;
        });

    // Legend
    g.append("rect")
        .attr("transform", function (d, i) {
            return `translate(${outerRadius + margin.right}, ${-15 * data.length + 30 * i})`;
        })
        .attr("width", 20)
        .attr("height", 10)
        .style("fill", function (d) {
            return color(d.index);
        });
    g.append("text")
        .attr("transform", function (d, i) {
            return `translate(${25 + outerRadius + margin.bottom}, ${-15 * data.length + 10 + 30 * i})`;
        })
        .text(function (d) {
            return d.data.label
        });

    // Title
    svg.append("text")
        .attr("transform", `translate(${width / 4}, -${outerRadius + 2 * margin.top})`)
        .style("text-anchor", "middle")
        .style("font-weight", "bold")
        .text(options.title);
}

function stackedChart(selector, data, options) {
    console.log(data);
    const element = $(selector);
    d3.selectAll(`${selector} > *`).remove();

    options = {...defaultOptions, ...options};

    const totalWidth = element.width();
    const totalHeight = element.height();
    const margin = options.margin;

    const width = (options.width === undefined) ? totalWidth - (2 * margin.left + margin.right) : options.width;
    const height = (options.height === undefined) ? totalHeight - 2 * (margin.top + margin.bottom) : options.height;

    const x = d3.scaleLinear().range([0, width]);
    const y = d3.scaleBand().range([0, height]).padding(0.5);
    const color = d3.scaleLinear().domain([0, 0.5, 1.0]).range(["lightgreen", "khaki", "salmon"]);
    const svg = d3.select(selector)
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${margin.left + (options.yAxis.label ? 10 : 0)}, ` +
            `${margin.top + (options.title ? margin.top : 0)})`);

    x.domain([0, 1.0]);
    y.domain(data.map(function (d) {
        return d.label;
    }));

    const bar = svg.selectAll("bar")
        .data(data)
        .enter();

    bar.append("rect")
        .attr("class", options.barCssClass)
        .attr("y", function (d) {
            return y(d.label);
        })
        .attr("height", y.bandwidth())
        .attr("x", margin.left)
        .attr("width", width)
        .style("fill", "lightgray");

    bar.append("text")
        .attr("transform", function (d, i) {
            return `translate(${margin.left}, ${y(d.label) - 8})`;
        })
        .style("text-anchor", function (d) {
	    if (d.count == 0)
		return "start";
	    else if (d.count == d.total)
		return "end";
	    else
		return "middle";
	})
        .text(function (d) {
            return `${0} de ${d.total}`;
        })
        .transition()
        .duration(1000)
        .attr("transform", function (d, i) {
            return `translate(${margin.left + x(d.value)}, ${y(d.label) - 8})`;
        })
        .text(function (d) {
            return `${d.count} de ${d.total}`;
        });

    bar.append("rect")
        .attr("class", options.barCssClass)
        .attr("y", function (d) {
            return y(d.label);
        })
        .attr("height", y.bandwidth())
        .attr("x", margin.left)
        .attr("width", 0)
        .style("fill", color(x(0)))
        .transition()
        .duration(1000)
        .attr("x", margin.left)
        .attr("width", function (d) {
            return x(d.value);
        })
        .style("fill", function (d, i) {
            return color(d.value);
        });

    svg.append("g")
        .attr("transform", `translate(${margin.left}, ${0})`)
        .call(d3.axisLeft(y));

    svg.append("text")
        .attr("transform", `translate(${(width + (margin.left + margin.right)) / 2}, ${height + 2 * margin.bottom})`)
        .style("text-anchor", "middle")
        .text(options.xAxis.label);

    svg.append("g")
        .attr("transform", `translate(${margin.left}, ${height})`)
        .call(d3.axisBottom(x).ticks(10).tickFormat(d3.format(".0%")));

    svg.append("text")
        .attr("transform", `rotate(-90)`)
        .attr("y", -margin.left / 2)
        .attr("x", -(height / 2 + margin.top))
        .attr("dx", "1em")
        .style("text-anchor", "middle")
        .text(options.yAxis.label);

    // Title
    svg.append("text")
        .attr("transform", `translate(${width / 2}, -${margin.top})`)
        .style("font-weight", "bold")
        .style("text-anchor", "middle")
        .text(options.title);
}

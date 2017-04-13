function show_historic_graph() {

    var margin = {top: 30, right: 20, bottom: 20, left: 30},
        width = 600 - margin.left - margin.right,
        height = 300 - margin.top - margin.bottom;

    var parseDate = d3.timeParse("%Y-%m-%d");

    var x = d3.scaleTime().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    var xAxis = d3.axisBottom()
        .scale(x)
        .ticks(7);

    var yAxis = d3.axisLeft()
        .scale(y)
        .ticks(10);

    var entries = {
	key: historic_rates.target.currency_code,
	value: historic_rates.data
    };

    var max_rate = d3.max(entries.value, function(d) {
        return d.rate_ratio;
    });

    var min_rate = d3.min(entries.value, function(d) {
        return d.rate_ratio;
    });

    y.domain([min_rate, max_rate]);

    var min_date = d3.min(entries.value, function(d) {
        return parseDate(d.rate_date);
    });

    var max_date = d3.max(entries.value, function(d) {
        return parseDate(d.rate_date);
    });

    x.domain([min_date, max_date]);

    var line = d3.line()
        .x(function(d) { return x(parseDate(d.rate_date)); })
        .y(function(d) {
            return y(d.rate_ratio);
        });

    var color = d3.scaleOrdinal(d3.schemeCategory20);

    d3.selectAll('svg > *').remove();

    var svg = d3.select('svg')
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

    var g = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var path = g.append("path")
        .attr("class", "line")
        .style('stroke', function() {
            return color(entries.key);
        })
        .attr("d", line(entries.value));

    var t = d3.transition()
        .ease(d3.easeLinear)
        .duration(300);

    var path_length = path.node().getTotalLength();

    path.attr("stroke-dasharray", path_length + " " + path_length)
        .attr("stroke-dashoffset", path_length)
        .transition(t)
        .attr("stroke-dashoffset", 0);

    g.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    g.append("g")
        .attr("class", "axis axis--y")
        .call(yAxis);

    var title_text = historic_rates.target.short_name + ' ' + historic_rates.target.currency_name + ' vs '
        + historic_rates.base.short_name + ' ' + historic_rates.base.currency_name;

    g.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "14px")
        .text(title_text);
}

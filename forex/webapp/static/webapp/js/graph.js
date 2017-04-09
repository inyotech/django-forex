function display_rate_history(data) {

    var margin = {top: 30, right: 20, bottom: 80, left: 50},
        width = 800 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

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
	key: data.target.currency_code,
	value: data.data
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

    g.append("path")
        .attr("class", "line")
        .style('stroke', function() {
            return color(entries.key);
        })
        .attr("d", line(entries.value));

    legend_space = width;

    g.append("text")
        .attr("x", (legend_space/2))
        .attr("y", height + (margin.bottom/2)+ 5)
        .attr("class", "legend")
        .style("fill", function() {
            return color(entries.key);
	})
        .text(entries.key);

    g.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    g.append("g")
        .attr("class", "axis axis--y")
        .call(yAxis);

}

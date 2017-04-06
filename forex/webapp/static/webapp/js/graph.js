function display_all(data) {
    console.log('display', data);

    var margin = {top: 30, right: 20, bottom: 30, left: 50},
        width = 800 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    var parseDate = d3.time.format("%Y-%m-%d").parse;

    var x = d3.time.scale().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);

    var xAxis = d3.svg.axis()
	.scale(x)
        .orient("bottom")
	.ticks(7);

    var yAxis = d3.svg.axis()
	.scale(y)
        .orient("left")
	.ticks(10);

    var entries = d3.entries(data);

    console.log('entries', entries);

    var max_rate = d3.max(entries, function(d) {
        return d3.max(d.value.data, function(value_data) {
            return value_data.rate_ratio;
        });
    });

    console.log('max rate', max_rate);

    var min_rate = d3.min(entries, function(d) {
        return d3.min(d.value.data, function(value_data) {
            return value_data.rate_ratio;
        });
    });

    y.domain([min_rate, max_rate]);

    var min_date = d3.min(entries, function(d) {
        return d3.min(d.value.data, function(value_data) {
            return parseDate(value_data.rate_date);
        });
    });

    var max_date = d3.max(entries, function(d) {
        return d3.max(d.value.data, function(value_data) {
            return parseDate(value_data.rate_date);
        });
    });

    console.log('date extent', [min_date, max_date]);

    x.domain([min_date, max_date]);

    var line = d3.svg.line()
        .x(function(d) { return x(parseDate(d.rate_date)); })
        .y(function(d) {
            return y(d.rate_ratio);
        });

    d3.selectAll('svg > *').remove();

    var svg = d3.select('svg')
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

    var g = svg.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    entries.forEach(function(d) {
	g.append("path")
            .attr("class", "line")
            .attr("d", line(d.value.data));
    });

    g.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    g.append("g")
        .attr("class", "axis axis--y")
        .call(yAxis);

}

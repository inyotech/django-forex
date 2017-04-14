function show_current() {

    var columns = 3;
    var col_length = Math.ceil(current_rates.data.length/columns);
    var columnized_data = [];

    for (i=0, j=current_rates.data.length; i<j; i+=col_length) {
        columnized_data.push(current_rates.data.slice(i, i+col_length));
    }

    var table = d3.select('#currencies').selectAll('table#latest-rates');

    var base_name = current_rates.base.short_name + ' ' + current_rates.base.currency_name;
    table.select('caption')
        .html('Global Exchange Rates Based On ' + base_name + ', ' + current_rates.data[0].rate_date);

    var target_currency = table.select('input.target-select:checked');

    if (target_currency.empty()) {
        target_currency = 'USD';
    } else {
        target_currency = target_currency.attr('id');
    }

    var tbodies = table.selectAll('tbody').data(columnized_data);

    tbodies.exit().remove();

    tbodies = tbodies.enter().append('tbody').merge(tbodies);

    tbodies.style('float', 'left');

    tbodies.order();

    var rows = tbodies.selectAll('tr').data(function (d) {
        return d;
    });

    rows.exit().remove();

    rows = rows.enter().append('tr').merge(rows);

    rows.attr('id', function(d) {
        return d.currency_code;
    });

    rows.order();

    var total_delay = 300;
    var delay_per_row = total_delay/rows.size();

    var i = 0;
    rows.style('opacity', 0)
        .transition()
        .delay(function() { return i++ * delay_per_row; })
        .style('opacity', 1);

    var cells = rows.selectAll('td').data(function(d) {
        return [
            '<input type="radio" name="target-currency-select" class="target-select" id="' + d.currency_code + '" />',
            '<img src="static/rates/images/' + d.flag_image_file_name + '" />',
            d.short_name,
            d.currency_name,
            d3.format('.2f')(d.rate_ratio)
        ];
    });

    cells.exit().remove();

    cells = cells.enter().append('td').merge(cells);

    cells.order();

    cells.html(function(d) {
        return d;
    });

    if (!target_currency) {
        target_currency = 'USD';
    }

    cells.select('input.target-select#' + target_currency).property('checked', true);

    cells.selectAll('input').on('change', function(d) {

        target_code = this.id;

        load_historic().success(function() {
            show_historic();
        });

    });
}

function show_historic_table(page) {

    var table = d3.select('#histories').selectAll('table#historic-rates');

    var tbodies = table.selectAll('tbody').data(paginated_historic_rates[page-1]);

    tbodies.exit().remove();

    tbodies = tbodies.enter().append('tbody').merge(tbodies);

    tbodies.style('float', 'left');

    tbodies.order();

    var rows = tbodies.selectAll('tr').data(function (d) {
        return d;
    });

    rows.exit().remove();

    rows = rows.enter().append('tr').merge(rows);

    rows.order();

    rows.attr('class', function(d, i) {
        if ((i % 2) == 0) {
            return 'even';
        } else {
            return 'odd';
        }
    });

    var total_delay = 300;
    var delay_per_row = total_delay/rows.size();

    var i = 0;
    rows.style('opacity', 0)
        .transition()
        .delay(function() { return i++ * delay_per_row; })
        .style('opacity', 1);

    var cells = rows.selectAll('td').data(function(d) {
        return [
            d.rate_date,
            d3.format('.02f')(d.rate_ratio)
        ];
    });

    cells.exit()
        .remove();

    cells = cells.enter()
        .append('td')
        .merge(cells);

    cells.order();

    cells.text(function(d) {
        return d;
    }).attr('class', function(d, i) {
        if (i == 0) {
            return 'date';
        } else if(i == 1) {
            return 'rate';
        }
    });

    table.select('caption a#download-link')
        .attr('href', 'historic_rates/base/'
            + base_code + '/target/'
            + target_code + '/months/'
            + months_history + '?csv=1');

}

function paginate_historic_rates() {

    var columns = 4;
    var page_length = 10;
    var column_data = [];

    paginated_historic_rates = [];

    for (i=0; i<historic_rates.data.length; i+=page_length) {
        column_data.push(historic_rates.data.slice(i, i+page_length));
    }

    for (i=0; i<column_data.length; i+=columns) {
        paginated_historic_rates.push(column_data.slice(i, i+columns));
    }

}

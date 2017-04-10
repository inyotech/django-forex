function show_current() {

    var columns = 4;
    var col_length = Math.ceil(current_rates.data.length/columns);
    var columnized_data = [];

    for (i=0, j=current_rates.data.length; i<j; i+=col_length) {
        columnized_data.push(current_rates.data.slice(i, i+col_length));
    }

    var table = d3.select('#currency-table').selectAll('table#latest-rates');

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

    var cells = rows.selectAll('td').data(function(d) {
        return [
            '<input type="radio" name="target-currency-select" class="target-select" id="' + d.currency_code + '" />',
            '<img src="/static/rates/images/' + d.flag_image_file_name + '" />',
            d.country_name,
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

function show_historic_table() {

    console.log('historic_table');

    var columns = 5;
    var column_length = Math.ceil(historic_rates.data.length/columns);
    var columnized_data = [];

    for (i=0, j=historic_rates.data.length; i<j; i+=column_length) {
        columnized_data.push(historic_rates.data.slice(i, i+column_length));
    }

    var page_length = 10;
    var page_data = [];

    for (i=0; i<column_length; i+=page_length) {
        var page_columns = []
        for (j=0; j<columns; j++) {
            page_columns.push(columnized_data[j].slice(i, i+page_length));
        }
        page_data.push(page_columns);
    }

    var table = d3.select('#historic-table').selectAll('table#historic-rates');

    var tbodies = table.selectAll('tbody').data(page_data[0]);

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

    var cells = rows.selectAll('td').data(function(d) {
        return [
            d.rate_date,
            d.rate_ratio
        ];
    });

    cells.exit().remove();

    cells = cells.enter().append('td').merge(cells);

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

}

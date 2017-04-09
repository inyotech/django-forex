function new_base(base) {

    $.ajax({
        url: '/current_rates/base/' + base + '/',
        success: function(response) {

            update_latest(response);

            var target = d3.select('input.target-select:checked').attr('id');
            var base = d3.select('#base-currency-select select.currency-select').property('value');
            var months = d3.select('#timespan-select input[name=timespan-select-button]:checked').property('value');

            show_selected_currency(target, base, months);
        }
    });
}

function update_latest(data) {

    var columns = 4;
    var col_length = Math.ceil(data.data.length/columns);
    var columnized_data = [];

    for (i=0, j=data.data.length; i<j; i+=col_length) {
        columnized_data.push(data.data.slice(i, i+col_length));
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
        var selected_id = this.getAttribute('id');

        var target = d3.select('input.target-select:checked').property('id');
        var base = d3.select('#base-currency-select select.currency-select').property('value');
        var months = d3.select('#timespan-select input[name=timespan-select-button]:checked').property('value');

        show_selected_currency(target, base, months);

    });
}

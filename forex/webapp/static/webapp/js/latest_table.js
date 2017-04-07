function new_base(base) {

    $.ajax({
        url: '/current_rates/base/' + base + '/',
        success: function(response) {
            update_latest(response);
	    show_selected_currencies();
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

    var selected = table.selectAll('input:checked');

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
            '<input type="checkbox" class="target-select" id="' + d.currency_code + '" />',
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

    selector_list = $.map(selected_currencies, function(d) {
        cells.select('input#' + d).property('checked', true);
    });

    cells.selectAll('input').on('change', function(d) {
        var selected_id = this.getAttribute('id');
        var index = $.inArray(selected_id, selected_currencies);
        if (this.checked) {
            if (index === -1 ) {
                selected_currencies.push(selected_id);
            }
        } else {
            if (index !== -1) {
                selected_currencies.splice(index, 1);
            }
        }

        show_selected_currencies();

    });
}

var target_code = 'USD';
var base_code = 'EUR';
var current_rates = [];

var months_history = 24;
var historic_rates = [];

var paginated_historic_rates = [];

var stories = null;

function load_current() {

    return $.ajax({
        url: '/current_rates/base/' + base_code + '/',
        success: function(response) {
	    current_rates = response;
        }
    });
}

function load_historic() {

    return $.ajax({
	url: '/historic_rates/base/' + base_code + '/target/' + target_code + '/months/' + months_history,
        success: function(response) {
            historic_rates = response;
        }
    });

}

function load_stories() {
    return $.ajax({
        url: '/stories/10/',
        success: function(response) {
            stories = response;
        }
    });
}

function show_historic() {
    show_historic_graph();

    paginate_historic_rates();

    $('#pagination-demo').twbsPagination('destroy');

    $('#pagination-demo').twbsPagination({
        totalPages: paginated_historic_rates.length,
        onPageClick: function (event, page) {
            show_historic_table(page);
        }
    });

    show_historic_table(1);
}

$(document).ready(function() {

    load_current().success(function() {
        show_current();
    });

    load_historic().success(function() {
        show_historic();
    });

    load_stories().success(function() {
        show_stories();
    });

    $('#base-currency-select select.currency-select').change(function() {

	base_code = $(this).val();

	load_current().success(function() {
            show_current();
        });

        load_historic().success(function() {
            show_historic();
        });

   });

    $('#timespan-select input[name=timespan-select-button]').change(function() {

        months_history = $('#timespan-select input[name=timespan-select-button]:checked').val();

        load_historic().success(function() {
            show_historic();
        });

    });

});

var request = $.ajax({
    url: '/current_rates',
    type: 'GET'
});

request.fail(function(jqXHR, textStatus) {
    alert("Request failed: " + textStatus);
});

var currency_data = {}
var selected_currencies = [];

function show_selected_currencies() {

    $.each(currency_data, function(index, value) {
	if ($.inArray(index, selected_currencies) === -1) {
	    delete currency_data[index];
	}
    });

    deferreds = [];
    $.each(selected_currencies, function (index, value) {

	if (value in currency_data) {
	    return;
	}

	var base = $('#base-currency-select select.currency-select').val();

	var months = $('#timespan-select input[name=timespan-select-button]:checked').val();

	console.log('months', months);

	deferreds.push($.ajax({
	    url: '/historic_rates/base/' + base + '/target/' + value + '/months/' + months,
	    success: function(result) {
		currency_data[result.target.currency_code] = result;
	    }
	}));
    });

    $.when.apply($, deferreds).done(function() {
	display_all(currency_data);
    });
}

$(document).ready(function() {

    base = 'EUR';

    selected_currencies.push('USD');

    new_base(base);

    $('#base-currency-select select.currency-select').change(function() {
        currency_data = {}
	new_base($(this).val());
    });

    $('#timespan-select input[name=timespan-select-button').change(function() {
	console.log($(this).val());
	currency_data = {};
	show_selected_currencies();
    });
});

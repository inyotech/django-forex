var request = $.ajax({
    url: '/current_rates',
    type: 'GET'
});

request.done(function(msg) {
    console.log(msg);
});

request.fail(function(jqXHR, textStatus) {
    alert("Request failed: " + textStatus);
});

var currency_data = {}
var selected_currencies = [];

function show_selected_currencies() {

    console.log('called');

    var selected_currencies = []
    $('.show-history input:checked').each(function () {
	var parent = $(this).parent('td');
	var code = parent.attr('id').split('-').pop();
	console.log('add', code);
	selected_currencies.push(code);
    });

    $.each(currency_data, function(index, value) {
	if ($.inArray(index, selected_currencies) == -1) {
	    console.log('delete', index, selected_currencies);
	    delete currency_data[index];
	}
    });

    deferreds = [];
    $.each(selected_currencies, function (index, value) {

	if (value in currency_data) {
	    console.log('exists', value);
	    return;
	}

	deferreds.push($.ajax({
	    url: '/historic_rates/base/EUR/target/' + value + '/',
	    success: function(result) {
		currency_data[result.target.currency_code] = result;
	    }
	}));
    });

    $.when.apply($, deferreds).done(function() {
	console.log(currency_data);
	display_all(currency_data);
    });
}

$(document).ready(function() {

    console.log('ready1');

    if ($('.show-history input:checked').length == 0) {
        $('#currency-code-USD input').prop('checked', true);
    }

    show_selected_currencies();

    $('.show-history input').change(function () {
	show_selected_currencies();
    })


});

$(document).ready(function() {
    console.log('ready2');
});

$(document).ready(function() {
    console.log('ready3');
});

function show_selected_currency(target, base, months) {

    $.ajax({
	url: '/historic_rates/base/' + base + '/target/' + target + '/months/' + months,
	success: function(result) {
	    display_rate_history(result);
	}
    });
}

$(document).ready(function() {

    base = 'EUR';

    new_base(base);

    $('#base-currency-select select.currency-select').change(function() {
	new_base($(this).val());
    });

    $('#timespan-select input[name=timespan-select-button]').change(function() {

        var target = $('input.target-select:checked').attr('id');
        var base = $('#base-currency-select select.currency-select').val()
        var months = $('#timespan-select input[name=timespan-select-button]:checked').val();

	show_selected_currency(target, base, months);
    });
});

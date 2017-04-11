from django.conf.urls import url

import rates.views

urlpatterns = [
    url(r'^historic_rates/base/(?P<base>[a-zA-Z]{3})/target/(?P<target>[a-zA-Z]{3})/months/(?P<months>\d+)$',
        rates.views.historic_rates, name='historic_rates_months'),
    url(r'^historic_rates/base/(?P<base>[a-zA-Z]{3})/target/(?P<target>[a-zA-Z]{3})/$',
        rates.views.historic_rates, name='historic_rates'),
    url(r'^current_rates/base/(?P<base>[A-Z]{3})/$', rates.views.current_rates, name='current_rates_base'),
    url(r'^current_rates/$', rates.views.current_rates, name='current_rates'),
]

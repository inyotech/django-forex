from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rates/base/(?P<base>[a-zA-Z]{3})/months/(?P<months>\d+)$', views.index, name='index_with_params')
]

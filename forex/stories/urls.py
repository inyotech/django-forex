from django.conf.urls import url

import stories.views

urlpatterns = [
    url(r'^stories/(?P<count>\d+)/$', stories.views.stories, name='stories_with_count'),
    url(r'^stories/$', stories.views.stories, name='stories'),
]

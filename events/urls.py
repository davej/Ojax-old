from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {"template": "events/calendar_month.html"}, name="calendar_month"),
    # url(r'^events/(?P<year>\d{4})/(?P<month>\d{2})/$', event_listings),
)
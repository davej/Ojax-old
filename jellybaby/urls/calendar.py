"""
URLs for doing a jellybaby site by date (i.e. ``2007/``, ``2007/may/``, etc.)
"""

from django.conf.urls.defaults import *
from jellybaby.views import calendar

urlpatterns = patterns('', 
    url(
        regex = "^$",
        view  = calendar.today,
        name  = "jellybaby_calendar_today",
    ),
    url(
        regex = "^(?P<year>\d{4})/$",
        view  = calendar.year,
        name  = "jellybaby_calendar_year",
    ),
    url(
        regex = "^(?P<year>\d{4})/(?P<month>\w{3})/$",
        view  = calendar.month,
        name  = "jellybaby_calendar_month",
    ),
    url(
        regex = "^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$",
        view  = calendar.day,
        name  = "jellybaby_calendar_day",
    ),
)
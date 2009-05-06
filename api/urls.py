from django.conf.urls.defaults import *
from piston.resource import Resource

from djangogcal.observer import CalendarObserver

from api.adapters import EventCalendarAdapter
from api.handlers import EventListHandler, EventDragHandler, EventCreateHandler, EventUpdateHandler, EventDeleteHandler
from events.models import Event

event_listings = Resource(handler=EventListHandler)
event_move = Resource(handler=EventDragHandler)
event_create = Resource(handler=EventCreateHandler)
event_update = Resource(handler=EventUpdateHandler)
event_delete = Resource(handler=EventDeleteHandler)

urlpatterns = patterns('',
    url(r'^events/$', event_listings),
    url(r'^events/move-event/(?P<cal_id>\d+)/$', event_move),
    url(r'^events/create/$', event_create),
    url(r'^events/update/(?P<cal_id>\d+)/$', event_update),
    url(r'^events/delete/(?P<cal_id>\d+)/$', event_delete),
)

# gCalendar Update Signal
observer = CalendarObserver(email='djeffery@gmail.com', password='travis')
observer.observe(Event, EventCalendarAdapter())
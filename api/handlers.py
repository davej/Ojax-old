from piston.handler import BaseHandler
from django.db.models import Q

# DJANGO-1.1
# from django.db.models import F

import datetime
import time
from datetime import timedelta

from api.utils import is_same_day, parse_date
from events.models import Event
from projects.models import Project

class ProjectHandler(BaseHandler):
   allow_methods = ('GET',)
   model = Project
   fields = (('name', ('creator', ('username',)), 'created','private',))

class EventListHandler(BaseHandler):
   allow_methods = ('GET',)
   model = Event
   fields = ('title', 'start_time', 'end_time',)
   
   def read(self, request):
    """docstring for read"""
    
    st = datetime.datetime.fromtimestamp(int(request.GET.get('start')))
    en = datetime.datetime.fromtimestamp(int(request.GET.get('end')))
        
    evs = Event.objects.filter(
        Q(start_time__range=(st, en)) | Q(end_time__range=(st, en))
    )

    return [
        {
            'id': ev.id, 
            'title': ev.title, 
            'start': ev.start_time.strftime("%Y-%m-%dT%H:%M:%S"), 
            'end':ev.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'showTime': is_same_day(ev.start_time, ev.end_time)
        } for ev in evs
    ]

class EventDragHandler(BaseHandler):
    allowed_methods = ('POST',)
    model = Event
    
    def create(self, request, cal_id):
        """docstring for create"""
        
        day_delta = int(request.POST['days'])
        
        # DJANGO-1.0
        event = Event.objects.get(id=cal_id)
        event.start_time = event.start_time + timedelta(days=int(day_delta))
        event.end_time = event.end_time + timedelta(days=int(day_delta))

        event.save()     
        
        # DJANGO-1.1
        # event = Event.objects.get(id=cal_id).update(
        #     start_time = F( start_time + timedelta(days=day_delta) ),
        #     end_time = F( end_time + timedelta(days=day_delta) )
        # )
        
        return event
        
class EventCreateHandler(BaseHandler):
    allowed_methods = ('POST',)
    model = Event

    def create(self, request):
        """docstring for create"""

        title = request.POST['title']
        start_time = parse_date(request.POST['date1'] +" "+ request.POST['time1'])
        end_time = parse_date(request.POST['date2'] +" "+ request.POST['time2'])

        event = Event(title=title, start_time=start_time, end_time=end_time).save()

        return event
        
class EventUpdateHandler(BaseHandler):
    allowed_methods = ('POST',)
    model = Event

    def create(self, request, cal_id):
        """docstring for create"""

        title = request.POST['title']
        start_time = parse_date(request.POST['date1'] +" "+ request.POST['time1'])
        end_time = parse_date(request.POST['date2'] +" "+ request.POST['time2'])
        
        event = Event.objects.get(id=cal_id)
        event.title = title
        event.start_time = start_time
        event.end_time = end_time
        event.save()
        
        return event
        
class EventDeleteHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Event

    def read(self, request, cal_id):
        """docstring for create"""

        event = Event.objects.get(id=cal_id)
        event.delete()

        return event
        
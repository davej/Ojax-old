from django.contrib import admin
from events.models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time',)
    
admin.site.register(Event, EventAdmin)
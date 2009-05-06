from django.db import models

class Event(models.Model):
    """(Event description)"""
    start_time = models.DateTimeField(blank=False)
    end_time = models.DateTimeField(blank=False)
    title = models.CharField(blank=False, max_length=255)



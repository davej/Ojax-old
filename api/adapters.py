from djangogcal.adapter import CalendarAdapter, CalendarEventData
from djangogcal.observer import CalendarObserver

class EventCalendarAdapter(CalendarAdapter):
    """
    A calendar adapter for the Event model.
    """

    def get_event_data(self, instance):
        """
        Returns a CalendarEventData object filled with data from the adaptee.
        """
        return CalendarEventData(
            start=instance.start_time,
            end=instance.end_time,
            title=instance.title,
        )
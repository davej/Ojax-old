import dateutil.parser
import dateutil.tz

def is_same_day(start_time, end_time):
    """Uses time delta to find if start_time and end_time are on the same day"""
    return abs((start_time - end_time).days) <= 1
    
def parse_date(s):
    """
    Convert a string into a (local, naive) datetime object.
    """
    dt = dateutil.parser.parse(s)
    if dt.tzinfo:
        dt = dt.astimezone(dateutil.tz.tzlocal()).replace(tzinfo=None)
    return dt
from datetime import datetime
from dateutil import tz


def string_to_datetime(date_string) -> datetime | None:
    formats = ["%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y%m%d", "%Y%m%dT%H%MZ"]
    for date_format in formats:
        try:
            out_datetime = datetime.strptime(date_string, date_format)
            out_datetime = out_datetime.replace(tzinfo=tz.tzlocal())
            return out_datetime
        except ValueError:
            pass
    return None

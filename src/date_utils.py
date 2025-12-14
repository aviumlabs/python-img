# date_utils.py
# A set of Date Utilities
# Copyright 2024, 2025 Michael Konrad
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime, time, timezone, date
from dateutil import tz

def datetime_to_timestamp(a_dt: datetime) -> float:
    """
    Converts a date to timestamp.
    
    Args: 
        a_dt (date): a date to convert to timestamp

    Returns:
        timestamp: the timestamp representation of the supplied date
    """
    if isinstance(a_dt, datetime):
        return a_dt.timestamp()
    else:
        raise TypeError("Unsupported type passed as input.")
    

def timestamp_to_datetime(a_ts: float, tz=timezone.utc) -> datetime:
    """
    Converts a timestamp to datetime.
    
    Args: 
        a_ts (float): a timestamp to convert to a datetime
        tz (tzinfo): must be a subclass of tzinfo, ex: timezone.utc

    Returns:
        datetime: the datetime representation of the given timestamp, 
                  defaults to utc timezone.
    """
    try: 
        if isinstance(a_ts, float):
            return datetime.fromtimestamp(a_ts, tz=tz)
        else:
            raise TypeError("Unsupported type passed as input.")
    except OverflowError:
        raise OverflowError("Timestamp conversion caused an overflow error.")


def epoch_to_datetime(an_epoch: int, tz=timezone.utc) -> datetime:
    """
    Converts an epoch timestamp to datetime.
    
    Args: 
        an_epoch (int): an integer representation of a date since the epoch
        tz (tzinfo): must be a subclass of tzinfo, ex: timezone.utc

    Returns:
        datetime: the datetime representation of the given epoch, 
                  defaults to utc timezone.
    """
    if isinstance(an_epoch, int):
        len_epoch = len(str(an_epoch))
        if len_epoch > 10:
            an_epoch = round(an_epoch / 1000)

        return datetime.fromtimestamp(an_epoch, tz=tz)
    else:
        raise TypeError("Unsupported type passed as input.")
    

def datetime_to_epoch(a_dt: datetime, tz=timezone.utc) -> int:
    """
    Converts a datetime to an epoch integer timestamp
    
    Args: 
        a_dt (datetime): a datetime value to be converted
        tz (tzinfo): must be a subclass of tzinfo, ex: timezone.utc

    Returns:
        int: the integer representation in milliseconds of the given date, 
                  defaults to utc timezone.
    """
    if isinstance(a_dt, datetime):
        # Ensure datetime is in given timezone
        ts_tz = a_dt.astimezone(tz)
        ts = ts_tz.timestamp()
        return round(ts * 1000)
    else:
        raise TypeError("Unsupported type passed as input.")
    

def get_datetime(year: int, month: int, day: int, hour: int = 8, 
                 minute: int = 0, tz=timezone.utc) -> datetime:
    """
    Get a datetime object initialized to the specified year, month, day, hour, 
    minute, and timezone.

    Args:
        year (int): the year of the date.
        month: (int): the month of the date.
        day: (int): the day of the date.
        hour: (int): the hour of the date, specified in 24 hour format.
        minute: (int): the minute of the date
        tz: (tzinfo): must be a subclass of tzinfo, ex: timezone.utc

    Returns:
        datetime: the datetime object of the specified year, month, day, hour,
        and minute; defaults to 8am UTC.
    """
    if all(isinstance(item, int) for item in [year, month, day, hour, minute]): 
        return datetime(year, month, day, hour=hour, minute=minute, tzinfo=tz)
    else:
        raise TypeError("Unsupported type passed as input.")
    

def convert_date_millisecond(selected_date: date):
    """
    Converts a date  or date tuple to an epoch timestamp tuple. 

    Args: 
        selected_date (date, (date, date)): date to be converted to epoch time.

    Returns:
        a tuple(start_timestamp, end_timestamp) with the start timestamp set to 
        <date>00:00 and the end_timestamp set to <date>23:59:59.
    """
    if isinstance(selected_date, tuple):
        start_date, end_date = selected_date
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, time(23,59,59))

        start_timestamp = round(datetime_to_epoch(start_datetime) * 1000)
        end_timestamp = round(datetime_to_epoch(end_datetime) * 1000)
    else:
        start_datetime = datetime.combine(selected_date, datetime.min.time())
        end_datetime = datetime.combine(selected_date, time(23,59,59))
        start_timestamp = round(datetime_to_epoch(start_datetime) * 1000)
        end_timestamp = round(datetime_to_epoch(end_datetime) * 1000)

    return start_timestamp, end_timestamp


def convert_epoch(time_stamp, s='ms', date_format='%Y-%m-%dT%H:%M:%S.%fZ', timezone=None):
    """
    Converts an epoch time stamp to either UTC date time or a specified time zone.

    Args: 
        time_stamp (int): epoch time to be converted
        s (string): s='s' epoch time in seconds, s='ms' epoch time in milliseconds
        timezone (timeZone): convert epoch time to timezone

    Returns:
        string: the formatted datetime 

    """
    if time_stamp is not None:
        if 'ms' == s:
            time_stamp = time_stamp / 1000

        if timezone:
            a_datetime = date_to_timezone(datetime.fromtimestamp(time_stamp), timezone)
        else:
            a_datetime = datetime.fromtimestamp(time_stamp)

        return datetime_to_string(a_datetime, date_format)
    else:
        return None
    

def convert_from_string(date_str, date_format='%Y-%m-%dT%H:%M:%S.%fZ', timezone=None):
    """
    Converts a date string to a date object in the provided format.

    Args:
        date_str (String): The datetime string to be converted.
        format: (String): The format of the resulting datetime object.
        timezone (timeZone): Convert existing timezone to given timezone

    Returns:
        datetime: The provided string converted to the specific formatted datetime object.
    """
    orig_date = datetime.strptime(date_str, date_format)

    if timezone:
        c_date = date_to_timezone(orig_date, timezone)
    else: 
        c_date = datetime.strptime(date_str, date_format)

    return c_date


def date_to_timezone(a_date, timezone):
    """
    Converts a date from the included timezone to the specified timezone.

    Args:
        a_date (Date): The date to be converted.
        timezone (String): the timezone in IANA timezone format, e.g., 
                           'America/Los_Angeles'.

    Returns:
        date: same date as provided updated to specified timezone.
    """
    to_zone = tz.gettz(timezone)

    a_date = a_date.astimezone(to_zone)

    return a_date


def datetime_to_string(date=datetime.now(), date_format='%Y-%m-%d %H:%M:%S %Z', time_zone=None):
    """
    Converts a date object to a string in the provided format.
    
    Args:
        date (datetime): The datetime object to be converted. 
        date_format (string): The format the date is to be converted to. 
        time_zone (timeZone): Convert existing time_zone to given time_zone

    Returns:
        string: The provided date converted to the specific formatted string.
    """
    # date_format='%Y-%m-%d %H:%M:%S-%Z' format that includes timezone info
    if time_zone:
        c_date = date_to_timezone(date, time_zone)
        date_str = c_date.strftime(date_format)
    else: 
        date_str = date.strftime(date_format)

    return date_str


def drop_utc_timezone(date_str, date_format='%Y-%m-%dT%H:%M:%SZ'):
    """
    Converts a UTC date string to a date string in the provided format.

    Args:
        date_str (string): The datetime string to be converted.
        date_format: (string): The format of the resulting datetime object.

    Returns:
        string: The provided string converted to the specific formatted.
    """
    date_format_utc='%Y-%m-%dT%H:%M:%S.%fZ'
    return datetime.strftime(datetime.strptime(date_str, date_format_utc), 
                             date_format)


def get_date(year: int, month: int, day: int) -> datetime:
    """
    Get a datetime object initialized to the specified year, month, and day.

    Args:
        year (int): the year of the date.
        month: (int): the month of the date.
        day: (int): the day of the date.

    Returns:
        datetime: the datetime object of the specified year, month, and day.
    """
    return datetime(year, month, day)

def get_timestamp():
    """
    Returns the current time in UTC timestamp format
    """
    return datetime.now(timezone.utc)
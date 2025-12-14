# test_date_utils.py
# Test date_utils module
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

from datetime import datetime, timezone
from date_utils import datetime_to_timestamp, timestamp_to_datetime
from date_utils import datetime_to_epoch, epoch_to_datetime, get_datetime
from loguru import logger
from zoneinfo import ZoneInfo


def test_datetime_epoch():
    today_now = datetime.now(timezone.utc)
    logger.info("\nToday now is...{}", today_now)
    assert isinstance(today_now, datetime)

    today_ts = datetime_to_timestamp(today_now)
    logger.info("\nToday now timestamp is...{}", today_ts)
    assert isinstance(today_ts, float)

    cb_today = timestamp_to_datetime(today_ts)
    logger.info("\nTimestamp converted back to today now is...\n{}", cb_today)
    assert isinstance(cb_today, datetime)

    logger.info("\nConverted epoch datetime equals original datetime...\n{}, \n{}.", 
                cb_today, today_now)
    assert cb_today == today_now

    logger.info("\nTest converting the following millisecond timestamp to UTC datetime...\n{}", 
                '1740268800000')
    ms = 1740268800000
    dt_ms = epoch_to_datetime(ms)
    logger.info("\nEpoch timestamp UTC date is...{}.", dt_ms)
    assert isinstance(dt_ms, datetime)

    ms_dt = datetime_to_epoch(dt_ms)
    logger.info("\nDate converted back to milliseconds...\n{}", ms_dt)
    assert ms == ms_dt

    feb24_12pm = get_datetime(2025, 2, 24, hour=12, minute=0)
    logger.info("\nUTC Feb. 24th, 2025 8am...{}", feb24_12pm)
    assert isinstance(feb24_12pm, datetime)

    feb25_7am = get_datetime(2025, 2, 25, hour=7, minute=0)
    logger.info("\nUTC Feb. 25th, 2025, 7am...{}", feb25_7am)

    tz = ZoneInfo("America/Los_Angeles")
    ms_la = datetime_to_epoch(feb24_12pm, tz=tz)
    logger.info("\nLos Angeles Feb. 24th, 2025 4am...{}", feb24_12pm.astimezone(tz=tz))
    logger.info("\nLos Angeles Feb. 24th, 2025 4am converted to milliseconds...{}", ms_la)
    assert isinstance(ms_la, int)

    ms_la = datetime_to_epoch(feb25_7am, tz=tz)
    logger.info("\nLos Angeles Feb. 24th, 2025 11pm...{}", feb25_7am.astimezone(tz=tz))
    logger.info("\nLos Angeles Feb. 24th, 2025 11pm converted to milliseconds...{}", ms_la)
    assert isinstance(ms_la, int)
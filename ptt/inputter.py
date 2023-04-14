import random

from datetime import timedelta
from ptt.date_utils import is_friday, str_to_date


class Inputter:

    def __init__(self, base_start_time_str, base_end_time_str):
        self.time_format = '%H:%M'
        self.start_time = str_to_date(base_start_time_str, self.time_format)
        self.end_time = str_to_date(base_end_time_str, self.time_format)

    def calculate_input_hours(self, date_str):
        not_friday = not is_friday(date_str)

        start = self.__calculate_time(
            self.start_time, delay=0 if not_friday else -1)
        end = self.__calculate_time(
            self.end_time, delay=0 if not_friday else -5)

        working_time = self.TimeTrack(start, end)

        break_time = None
        if not_friday:
            start = self.__calculate_time(
                self.start_time, delay=5, use_default_offset=False, offset=0)
            end = self.__calculate_time(
                self.start_time, delay=5, use_default_offset=False, offset=15)
            break_time = self.TimeTrack(start, end)

        return {'working_time': working_time, 'break_time': break_time, 'not_friday': not_friday}

    def __calculate_time(self, time, delay=0, use_default_offset=True, offset=0):
        if use_default_offset:
            offset = random.randint(
                0, 10) * 1 if random.randint(0, 100) <= 80 else -1
        time += timedelta(hours=delay) + timedelta(minutes=offset)
        return time.strftime(self.time_format)

    class TimeTrack:

        def __init__(self, start_time_str, end_time_str):
            self.start = start_time_str
            self.end = end_time_str

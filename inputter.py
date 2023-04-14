import random

from datetime import timedelta
from date_utils import is_friday, str_to_date


class Inputter:

    def __init__(self, base_start_time_str, base_end_time_str):
        self.start_time = str_to_date(base_start_time_str)
        self.end_time = str_to_date(base_end_time_str)

    def calculate_input_hours(self, date_str):
        not_friday = not is_friday(date_str)

        start = self.__calculate_time(
            self.start_time, delay=0 if not_friday else -1)
        end = self.__calculate_time(
            self.end_time, delay=0 if not_friday else -1)

        working_time = self.TimeTrack(start, end)

        if not_friday:
            start = self.__calculate_time(
                self.start_time, delay=5, use_default_offset=False, offset=0)
            end = self.__calculate_time(
                self.start_time, delay=5, use_default_offset=False, offset=15)
            break_time = self.TimeTrack(start, end)

        return {'working_time': working_time, 'break_time': break_time, 'not_friday': not_friday}

    def __calculate_time(str_time, delay=0, use_default_offset=True, offset=0):
        time_format = '%H:%M'
        time = str_to_date(str_time, time_format)
        if use_default_offset:
            offset = random.randint(
                0, 10) * 1 if random.randint(0, 100) <= 80 else -1
        time = time + timedelta(hours=delay) + timedelta(minutes=offset)
        return time.strftime(time_format)

    class TimeTrack:

        def __init__(self, start_time_str, end_time_str):
            self.start = start_time_str
            self.end = end_time_str

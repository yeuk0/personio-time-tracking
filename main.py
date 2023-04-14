import time
import random

from datetime import timedelta
from date_utils import str_to_date, is_friday
from navigator import Navigator
from selenium import webdriver
from selenium.webdriver.common.by import By


def input_hours(dialog, date_str):
    time.sleep(.2)  # To let the dialog load
    not_friday = not is_friday(date_str)

    start_inputs = dialog.find_elements(
        By.XPATH, "//input[@data-test-id='timerange-start']")
    end_inputs = dialog.find_elements(
        By.XPATH, "//input[@data-test-id='timerange-end']")

    start_time = '09:00'
    end_time = '17:00'

    start_inputs[0].send_keys(calculate_time(
        start_time, delay=0 if not_friday else -1))
    end_inputs[0].send_keys(calculate_time(
        end_time, delay=0 if not_friday else -5))

    if not_friday:
        start_inputs[1].send_keys(calculate_time(
            start_time, delay=5, use_default_offset=False, offset=0))
        end_inputs[1].send_keys(calculate_time(
            start_time, delay=5, use_default_offset=False, offset=15))

    time.sleep(.1)  # To allow save button being enabled
    dialog.find_element(
        By.XPATH, "//button[@data-action-name='day-entry-save']").click()


def calculate_time(str_time, delay=0, use_default_offset=True, offset=0):
    time_format = '%H:%M'
    time = str_to_date(str_time, time_format)
    if use_default_offset:
        offset = random.randint(
            0, 10) * 1 if random.randint(0, 100) <= 80 else -1
    time = time + timedelta(hours=delay) + timedelta(minutes=offset)
    return time.strftime(time_format)


if __name__ == "__main__":
    navigator = Navigator(webdriver.Firefox())

    navigator.load()

    navigator.go_to_attendance_page()

    for day, button in navigator.get_day_buttons().items():
        dialog = navigator.open_input_dialog(button)
        input_hours(dialog, day)
        navigator.close_input_dialog(dialog)
        time.sleep(1)

    navigator.quit()

import calendar
import time
import random

from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


def find_element_by_and_wait(reference, by, value, timeout=5):
    return WebDriverWait(reference, timeout).until(EC.presence_of_element_located((by, value)))


def go_to_attendance_page(browser):
    attendance_widget = find_element_by_and_wait(
        browser, By.ID, 'attendance-widget', 60)
    attendance_link = attendance_widget.find_element(
        By.TAG_NAME, 'form').find_element(By.TAG_NAME, 'a')
    attendance_link.click()


def get_day_buttons(browser):
    attendance_table = browser.find_element(By.ID, 'attendance')
    day_buttons = {}
    date = datetime.today()
    for day_number in range(calendar.monthrange(date.year, date.month)[1]):
        date_str = f"{date.strftime('%Y-%m')}-{day_number+1:02d}"
        if is_valid_day(date_str):
            day = get_day_button(attendance_table, date_str)
            day_buttons[date_str] = day.find_element(By.TAG_NAME, 'button')
    return day_buttons


def str_to_date(date_str, date_format='%Y-%m-%d'):
    return datetime.strptime(date_str, date_format)


def is_valid_day(date_str):
    try:
        return str_to_date(date_str).weekday() < 5
    except ValueError:
        return False


def is_friday(date_str):
    return str_to_date(date_str).weekday() == 4


def get_day_button(element, date_str):
    try:
        return find_element_by_and_wait(element, By.XPATH, f"//div[@data-test-id='day_{date_str}']")
    except TimeoutException:
        # This should only happen once as we're handling valid days values
        return find_element_by_and_wait(element, By.XPATH, "//div[@data-test-id='today-cell']")


def open_input_dialog(browser, day_button):
    day_button.click()
    return find_element_by_and_wait(browser, By.XPATH, "//section[@role='dialog']")


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


def close_input_dialog(dialog):
    close_button = find_element_by_and_wait(
        dialog, By.XPATH, "//button[@data-test-id='day-entry-dialog-close-button']")
    close_button.click()


def zoom_out(browser):
    browser.set_context("chrome")
    browser.find_element(By.TAG_NAME, "html").send_keys(Keys.COMMAND + '-')
    browser.set_context("content")


if __name__ == "__main__":
    browser = webdriver.Firefox()
    browser.get('https://empathy-co.personio.de/my-desk')

    browser.maximize_window()
    zoom_out(browser)

    go_to_attendance_page(browser)

    day_buttons = get_day_buttons(browser)
    for day, button in day_buttons.items():
        dialog = open_input_dialog(browser, button)
        input_hours(dialog, day)
        close_input_dialog(dialog)
        time.sleep(1)

    browser.quit()

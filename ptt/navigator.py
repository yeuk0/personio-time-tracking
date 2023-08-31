import time

from ptt.date_utils import get_today_date, get_days_range_from_date_month, is_valid_day
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Navigator:

    def __init__(self, browser_name):
        self.browser = webdriver.Firefox()
        self.url = 'https://empathy-co.personio.de/my-desk'

    @staticmethod
    def find_element_by_and_wait(reference, by, value, timeout=5):
        return WebDriverWait(reference, timeout).until(EC.presence_of_element_located((by, value)))

    def load(self):
        self.browser.get(self.url)
        self.browser.maximize_window()
        self.zoom_out()

    def zoom_out(self):
        self.browser.set_context("chrome")
        self.browser.find_element(
            By.TAG_NAME, "html").send_keys(Keys.COMMAND + '-')
        self.browser.set_context("content")

    def go_to_attendance_page(self):
        attendance_widget = self.find_element_by_and_wait(
            self.browser, By.ID, 'attendance-widget', 60)
        attendance_link = attendance_widget.find_element(
            By.TAG_NAME, 'form').find_element(
            By.TAG_NAME, 'section').find_element(
            By.TAG_NAME, 'a')
        attendance_link.click()

    def get_day_buttons(self):
        attendance_table = self.find_element_by_and_wait(self.browser, By.XPATH, "//div[starts-with(@class, 'AttendanceCalendar')]")
        day_buttons = {}
        date = get_today_date()
        for day_number in get_days_range_from_date_month(date):
            date_str = f"{date.strftime('%Y-%m')}-{day_number+1:02d}"
            if is_valid_day(date_str):
                day = self.__get_day_button(attendance_table, date_str)
                day_buttons[date_str] = day.find_element(By.TAG_NAME, 'button')
        return day_buttons

    def open_input_dialog(self, day_button):
        time.sleep(.2)  # To let the button load
        day_button.click()
        time.sleep(.2)  # To let the dialog load

    def log_time(self, time_track):
        dialog = self.find_element_by_and_wait(self.browser, By.XPATH, "//div[@role='none']")

        start_inputs = dialog.find_elements(By.XPATH, "//input[@data-test-id='timerange-start']")
        end_inputs = dialog.find_elements(By.XPATH, "//input[@data-test-id='timerange-end']")

        start_inputs[0].send_keys(time_track['working_time'].start)
        end_inputs[0].send_keys(time_track['working_time'].end)
        
        if time_track['not_friday']:
            start_inputs[1].send_keys(time_track['break_time'].start)
            end_inputs[1].send_keys(time_track['break_time'].end)
        
        time.sleep(.1)  # To allow save button being enabled
        dialog.find_element(By.XPATH, "//button[@data-action-name='day-entry-save']").click()
        time.sleep(1)  # To allow dialog closing properly

    def quit(self):
        self.browser.quit()

    def __get_day_button(self, element, date_str):
        try:
            return Navigator.find_element_by_and_wait(element, By.XPATH, f"//div[@data-test-id='day_{date_str}']")
        except TimeoutException:
            # This should only happen once as we're handling valid days values
            return Navigator.find_element_by_and_wait(element, By.XPATH, "//div[@data-test-id='today-cell']")

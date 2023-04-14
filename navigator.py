from date_utils import get_today_date, get_days_range_from_date_month, is_valid_day
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Navigator:

    def __init__(self, browser):
        self.browser = browser
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
            By.TAG_NAME, 'form').find_element(By.TAG_NAME, 'a')
        attendance_link.click()

    def get_day_buttons(self):
        attendance_table = self.browser.find_element(By.ID, 'attendance')
        day_buttons = {}
        date = get_today_date()
        for day_number in get_days_range_from_date_month(date):
            date_str = f"{date.strftime('%Y-%m')}-{day_number+1:02d}"
            if is_valid_day(date_str):
                day = self.__get_day_button(attendance_table, date_str)
                day_buttons[date_str] = day.find_element(By.TAG_NAME, 'button')
        return day_buttons

    def open_input_dialog(self, day_button):
        day_button.click()
        return self.find_element_by_and_wait(self.browser, By.XPATH, "//section[@role='dialog']")

    def close_input_dialog(self, dialog):
        close_button = self.find_element_by_and_wait(dialog, By.XPATH, "//button[@data-test-id='day-entry-dialog-close-button']")
        close_button.click()

    def quit(self):
        self.browser.quit()

    def __get_day_button(element, date_str):
        try:
            return Navigator.find_element_by_and_wait(element, By.XPATH, f"//div[@data-test-id='day_{date_str}']")
        except TimeoutException:
            # This should only happen once as we're handling valid days values
            return Navigator.find_element_by_and_wait(element, By.XPATH, "//div[@data-test-id='today-cell']")

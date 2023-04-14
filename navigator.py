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
        self.browser.find_element(By.TAG_NAME, "html").send_keys(Keys.COMMAND + '-')
        self.browser.set_context("content")

    def go_to_attendance_page(self):
        attendance_widget = self.find_element_by_and_wait(
            self.browser, By.ID, 'attendance-widget', 60)
        attendance_link = attendance_widget.find_element(
            By.TAG_NAME, 'form').find_element(By.TAG_NAME, 'a')
        attendance_link.click()

    def quit(self):
        self.browser.quit()

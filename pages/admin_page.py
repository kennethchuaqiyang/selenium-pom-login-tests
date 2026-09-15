from selenium.webdriver.common.by import By


class AdminPage:
    URL = "https://kennethchuaqiyang.github.io/demo-login-portal/admin.html"

    ADMIN_PAGE = (By.CSS_SELECTOR, '[data-testid="admin-page"]')
    ADMIN_IMAGE = (By.CSS_SELECTOR, '[data-testid="admin-image"]')
    LOGGED_IN_AS = (By.CSS_SELECTOR, '[data-testid="logged-in-as"]')
    LOGOUT_BUTTON = (By.CSS_SELECTOR, '[data-testid="logout-button"]')

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def get_logged_in_as_text(self):
        return self.driver.find_element(*self.LOGGED_IN_AS).text

    def logout(self):
        self.driver.find_element(*self.LOGOUT_BUTTON).click()
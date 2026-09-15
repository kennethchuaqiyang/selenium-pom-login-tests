from selenium.webdriver.common.by import By


class LoginPage:
    URL = "https://kennethchuaqiyang.github.io/demo-login-portal/"

    USER_TYPE_SELECT = (By.CSS_SELECTOR, '[data-testid="user-type-select"]')
    USERNAME_INPUT = (By.CSS_SELECTOR, '[data-testid="username-input"]')
    PASSWORD_RADIO = (By.CSS_SELECTOR, '[data-testid="auth-method-password"]')
    PASSCODE_RADIO = (By.CSS_SELECTOR, '[data-testid="auth-method-passcode"]')
    CREDENTIAL_INPUT = (By.CSS_SELECTOR, '[data-testid="credential-input"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-testid="login-button"]')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-testid="error-message"]')
    LOGOUT_BUTTON = (By.CSS_SELECTOR, '[data-testid="logout-button"]')

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def select_user_type(self, user_type):
        from selenium.webdriver.support.ui import Select
        select = Select(self.driver.find_element(*self.USER_TYPE_SELECT))
        select.select_by_value(user_type)

    def use_auth_method(self, method):
        locator = self.PASSCODE_RADIO if method == "passcode" else self.PASSWORD_RADIO
        self.driver.find_element(*locator).click()

    def login(self, user_type, username, credential, method="password"):
        self.select_user_type(user_type)
        username_field = self.driver.find_element(*self.USERNAME_INPUT)
        username_field.clear()
        username_field.send_keys(username)
        self.use_auth_method(method)
        credential_field = self.driver.find_element(*self.CREDENTIAL_INPUT)
        credential_field.clear()
        credential_field.send_keys(credential)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_text(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text

    def is_logged_in(self):
        elements = self.driver.find_elements(*self.LOGOUT_BUTTON)
        return len(elements) > 0

    def logout(self):
        self.driver.find_element(*self.LOGOUT_BUTTON).click()
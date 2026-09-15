from selenium.webdriver.common.by import By


class ShopPage:
    URL = "https://kennethchuaqiyang.github.io/demo-login-portal/shop.html"

    SHOP_PAGE = (By.CSS_SELECTOR, '[data-testid="shop-page"]')
    PRODUCT_GRID = (By.CSS_SELECTOR, '[data-testid="product-grid"]')
    CART_NOTE = (By.CSS_SELECTOR, '[data-testid="cart-note"]')
    LOGGED_IN_AS = (By.CSS_SELECTOR, '[data-testid="logged-in-as"]')
    LOGOUT_BUTTON = (By.CSS_SELECTOR, '[data-testid="logout-button"]')

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def add_to_cart(self, product_id):
        locator = (By.CSS_SELECTOR, f'[data-testid="add-to-cart-{product_id}"]')
        self.driver.find_element(*locator).click()

    def get_cart_note_text(self):
        return self.driver.find_element(*self.CART_NOTE).text

    def get_logged_in_as_text(self):
        return self.driver.find_element(*self.LOGGED_IN_AS).text

    def logout(self):
        self.driver.find_element(*self.LOGOUT_BUTTON).click()
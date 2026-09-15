import time
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from pages.admin_page import AdminPage
from pages.shop_page import ShopPage

ADMIN_USERS = [
    {"username": "admin1", "password": "Admin@123", "passcode": "111111"},
    {"username": "admin2", "password": "Admin@456", "passcode": "222222"},
]

CUSTOMER_USERS = [
    {"username": "customer1", "password": "Cust@123", "passcode": "333333"},
    {"username": "customer2", "password": "Cust@456", "passcode": "444444"},
]


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(0)  # we use explicit waits instead
    yield drv
    drv.quit()


def wait_for(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))


def ensure_on_login_page(driver, login_page):
    """Logout first if a session is already active, otherwise open fresh."""
    if login_page.is_logged_in():
        login_page.logout()
        wait_for(driver, LoginPage.USER_TYPE_SELECT)
    else:
        login_page.open()
        wait_for(driver, LoginPage.USER_TYPE_SELECT)


# ---------- Admin - password ----------

@pytest.mark.parametrize("user", ADMIN_USERS, ids=lambda u: u["username"])
def test_admin_correct_password(driver, user):
    login_page = LoginPage(driver)
    admin_page = AdminPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("admin", user["username"], user["password"], "password")
    wait_for(driver, AdminPage.ADMIN_PAGE)
    wait_for(driver, AdminPage.ADMIN_IMAGE)
    assert "admin.html" in driver.current_url
    assert user["username"] in admin_page.get_logged_in_as_text()


def test_admin_no_username_correct_password(driver):
    login_page = LoginPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("admin", "", "Admin@123", "password")
    wait_for(driver, LoginPage.ERROR_MESSAGE)
    assert "Enter a username" in login_page.get_error_text()


def test_admin_invalid_username_correct_password(driver):
    login_page = LoginPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("admin", "not-an-admin", "Admin@123", "password")
    wait_for(driver, LoginPage.ERROR_MESSAGE)
    assert "No admin account" in login_page.get_error_text()


def test_admin_valid_username_no_password(driver):
    login_page = LoginPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("admin", "admin1", "", "password")
    wait_for(driver, LoginPage.ERROR_MESSAGE)
    assert "Enter a username" in login_page.get_error_text()


def test_admin_valid_username_wrong_password(driver):
    login_page = LoginPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("admin", "admin1", "WrongPass123", "password")
    wait_for(driver, LoginPage.ERROR_MESSAGE)
    assert "Incorrect password" in login_page.get_error_text()


# ---------- Admin - passcode ----------

@pytest.mark.parametrize("user", ADMIN_USERS, ids=lambda u: u["username"])
def test_admin_correct_passcode(driver, user):
    login_page = LoginPage(driver)
    admin_page = AdminPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("admin", user["username"], user["passcode"], "passcode")
    wait_for(driver, AdminPage.ADMIN_PAGE)
    assert "admin.html" in driver.current_url
    assert user["username"] in admin_page.get_logged_in_as_text()


def test_admin_no_username_correct_passcode(driver):
    login_page = LoginPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("admin", "", "111111", "passcode")
    wait_for(driver, LoginPage.ERROR_MESSAGE)
    assert "Enter a username" in login_page.get_error_text()


def test_admin_invalid_username_correct_passcode(driver):
    login_page = LoginPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("admin", "not-an-admin", "111111", "passcode")
    wait_for(driver, LoginPage.ERROR_MESSAGE)
    assert "No admin account" in login_page.get_error_text()


def test_admin_valid_username_no_passcode(driver):
    login_page = LoginPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("admin", "admin1", "", "passcode")
    wait_for(driver, LoginPage.ERROR_MESSAGE)
    assert "Enter a username" in login_page.get_error_text()


def test_admin_valid_username_wrong_passcode(driver):
    login_page = LoginPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("admin", "admin1", "999999", "passcode")
    wait_for(driver, LoginPage.ERROR_MESSAGE)
    assert "Incorrect passcode" in login_page.get_error_text()


# ---------- Customer - password ----------

@pytest.mark.parametrize("user", CUSTOMER_USERS, ids=lambda u: u["username"])
def test_customer_correct_password(driver, user):
    login_page = LoginPage(driver)
    shop_page = ShopPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("customer", user["username"], user["password"], "password")
    wait_for(driver, ShopPage.SHOP_PAGE)
    wait_for(driver, ShopPage.PRODUCT_GRID)
    assert "shop.html" in driver.current_url
    assert user["username"] in shop_page.get_logged_in_as_text()


def test_customer_no_username_correct_password(driver):
    login_page = LoginPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("customer", "", "Cust@123", "password")
    wait_for(driver, LoginPage.ERROR_MESSAGE)
    assert "Enter a username" in login_page.get_error_text()


def test_customer_invalid_username_correct_password(driver):
    login_page = LoginPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("customer", "not-a-customer", "Cust@123", "password")
    wait_for(driver, LoginPage.ERROR_MESSAGE)
    assert "No customer account" in login_page.get_error_text()


def test_customer_valid_username_no_password(driver):
    login_page = LoginPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("customer", "customer1", "", "password")
    wait_for(driver, LoginPage.ERROR_MESSAGE)
    assert "Enter a username" in login_page.get_error_text()


def test_customer_valid_username_wrong_password(driver):
    login_page = LoginPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("customer", "customer1", "WrongPass123", "password")
    wait_for(driver, LoginPage.ERROR_MESSAGE)
    assert "Incorrect password" in login_page.get_error_text()


# ---------- Customer - passcode ----------

@pytest.mark.parametrize("user", CUSTOMER_USERS, ids=lambda u: u["username"])
def test_customer_correct_passcode(driver, user):
    login_page = LoginPage(driver)
    shop_page = ShopPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("customer", user["username"], user["passcode"], "passcode")
    wait_for(driver, ShopPage.SHOP_PAGE)
    assert "shop.html" in driver.current_url
    assert user["username"] in shop_page.get_logged_in_as_text()


def test_customer_no_username_correct_passcode(driver):
    login_page = LoginPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("customer", "", "333333", "passcode")
    wait_for(driver, LoginPage.ERROR_MESSAGE)
    assert "Enter a username" in login_page.get_error_text()


def test_customer_invalid_username_correct_passcode(driver):
    login_page = LoginPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("customer", "not-a-customer", "333333", "passcode")
    wait_for(driver, LoginPage.ERROR_MESSAGE)
    assert "No customer account" in login_page.get_error_text()


def test_customer_valid_username_no_passcode(driver):
    login_page = LoginPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("customer", "customer1", "", "passcode")
    wait_for(driver, LoginPage.ERROR_MESSAGE)
    assert "Enter a username" in login_page.get_error_text()


def test_customer_valid_username_wrong_passcode(driver):
    login_page = LoginPage(driver)
    login_page.open()
    wait_for(driver, LoginPage.USER_TYPE_SELECT)
    login_page.login("customer", "customer1", "999999", "passcode")
    wait_for(driver, LoginPage.ERROR_MESSAGE)
    assert "Incorrect passcode" in login_page.get_error_text()
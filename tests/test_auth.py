from selenium.webdriver.remote.webdriver import WebDriver

from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from utils.test_data import SyntheticUser, create_test_user


def test_register_unique_user(driver: WebDriver) -> None:
    user = create_test_user()
    registration_page = RegistrationPage(driver)
    registration_page.open()
    registration_page.register(user)

    assert registration_page.registration_succeeded(), (
        "The demo did not confirm registration of the synthetic test user."
    )


def test_registration_rejects_missing_required_fields(driver: WebDriver) -> None:
    registration_page = RegistrationPage(driver)
    registration_page.open()
    registration_page.submit()
    errors = registration_page.error_messages()

    assert "First name is required." in errors
    assert "Username is required." in errors
    assert "Password is required." in errors


def test_registration_rejects_mismatched_passwords(driver: WebDriver) -> None:
    user = create_test_user()
    registration_page = RegistrationPage(driver)
    registration_page.open()
    registration_page.register(user, password_confirmation="DifferentPass123")

    assert "Passwords did not match." in registration_page.error_messages()


def test_registration_rejects_duplicate_username(
    driver: WebDriver,
    registered_user: SyntheticUser,
) -> None:
    registration_page = RegistrationPage(driver)
    registration_page.open()
    registration_page.register(registered_user)

    errors = registration_page.error_messages()
    assert any("username already exists" in error.lower() for error in errors)


def test_login_accepts_registered_user(
    driver: WebDriver,
    registered_user: SyntheticUser,
) -> None:
    login_page = LoginPage(driver)
    login_page.logout()
    login_page.login(registered_user.username, registered_user.password)

    assert login_page.accounts_heading() == "Accounts Overview"


def test_login_rejects_invalid_credentials(driver: WebDriver) -> None:
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("invalid_selenium_user", "InvalidPass123")

    assert "could not be verified" in login_page.error_message().lower()


def test_login_rejects_empty_credentials(driver: WebDriver) -> None:
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("", "")

    assert "please enter a username and password" in login_page.error_message().lower()


def test_logout_ends_authenticated_session(
    driver: WebDriver,
    registered_user: SyntheticUser,
) -> None:
    login_page = LoginPage(driver)
    login_page.logout()

    assert login_page.visible(LoginPage.USERNAME).is_displayed()

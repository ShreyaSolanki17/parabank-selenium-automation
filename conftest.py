from collections.abc import Iterator

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from pages.registration_page import RegistrationPage
from utils.test_data import SyntheticUser, create_test_user


@pytest.fixture
def driver() -> Iterator[WebDriver]:
    browser = webdriver.Chrome()
    try:
        yield browser
    finally:
        browser.quit()


@pytest.fixture
def registered_user(driver: WebDriver) -> SyntheticUser:
    user = create_test_user()
    registration_page = RegistrationPage(driver)
    registration_page.open()
    registration_page.register(user)
    assert registration_page.registration_succeeded(), (
        "The demo did not confirm registration of the synthetic test user."
    )
    return user

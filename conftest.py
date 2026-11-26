from collections.abc import Iterator

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


@pytest.fixture
def driver() -> Iterator[WebDriver]:
    browser = webdriver.Chrome()
    try:
        yield browser
    finally:
        browser.quit()

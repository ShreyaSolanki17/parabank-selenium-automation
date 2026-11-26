from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_login_page_loads(driver: WebDriver) -> None:
    driver.get("https://parabank.parasoft.com/parabank/index.htm")

    assert "ParaBank" in driver.title
    wait = WebDriverWait(driver, timeout=10)
    wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    wait.until(EC.visibility_of_element_located((By.NAME, "password")))

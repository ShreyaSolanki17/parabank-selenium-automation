from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://parabank.parasoft.com/parabank/index.htm"
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "form[name='login'] input[type='submit']")
    LOGIN_ERROR = (By.CSS_SELECTOR, "#rightPanel .error")
    ACCOUNTS_HEADING = (By.CSS_SELECTOR, "#rightPanel h1.title")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href*='logout.htm']")

    def open(self) -> None:
        super().open(self.URL)

    def login(self, username: str, password: str) -> None:
        self.enter_text(self.USERNAME, username)
        self.enter_text(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def error_message(self) -> str:
        return self.visible(self.LOGIN_ERROR).text

    def accounts_heading(self) -> str:
        return self.visible(self.ACCOUNTS_HEADING).text

    def logout(self) -> None:
        self.click(self.LOGOUT_LINK)
        self.visible(self.USERNAME)

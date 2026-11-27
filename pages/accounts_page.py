from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from pages.base_page import BasePage


class AccountsOverviewPage(BasePage):
    ACCOUNT_LINKS = (By.CSS_SELECTOR, "#accountTable a")

    def open(self) -> None:
        self.click((By.LINK_TEXT, "Accounts Overview"))
        self.wait.until(EC.presence_of_element_located(self.ACCOUNT_LINKS))

    def account_rows(self) -> list[tuple[str, str, str]]:
        rows = self.driver.find_elements(By.CSS_SELECTOR, "#accountTable tr")
        return [
            (
                row.find_element(By.CSS_SELECTOR, "a").text,
                row.find_elements(By.TAG_NAME, "td")[1].text,
                row.find_elements(By.TAG_NAME, "td")[2].text,
            )
            for row in rows
            if row.find_elements(By.CSS_SELECTOR, "a")
        ]

    def open_account(self, account_id: str) -> "AccountActivityPage":
        self.click((By.LINK_TEXT, account_id))
        return AccountActivityPage(self.driver, account_id)


class OpenAccountPage(BasePage):
    ACCOUNT_TYPE = (By.ID, "type")
    FUNDING_OPTIONS = (By.CSS_SELECTOR, "#fromAccountId option")
    FUNDING_SELECT = (By.ID, "fromAccountId")
    OPEN_BUTTON = (By.CSS_SELECTOR, "#openAccountForm input[type='button']")
    OPEN_RESULT = (By.ID, "openAccountResult")
    NEW_ACCOUNT_ID = (By.ID, "newAccountId")
    OPEN_ERROR = (By.ID, "openAccountError")

    def open(self) -> None:
        self.click((By.LINK_TEXT, "Open New Account"))
        WebDriverWait(self.driver, timeout=15).until(
            EC.url_contains("openaccount.htm")
        )
        WebDriverWait(self.driver, timeout=15).until(
            EC.any_of(
                EC.presence_of_element_located(self.FUNDING_OPTIONS),
                EC.visibility_of_element_located(self.OPEN_ERROR),
            )
        )
        if self.driver.find_element(*self.OPEN_ERROR).is_displayed():
            raise RuntimeError(
                "ParaBank failed to load funding accounts on the Open New Account page."
            )

    def create_account(self, account_type: str) -> str:
        options = self.driver.find_elements(*self.FUNDING_OPTIONS)
        if not options:
            raise RuntimeError("No funding account is available for account opening.")

        self.select_by_visible_text(self.ACCOUNT_TYPE, account_type)
        self.click(self.OPEN_BUTTON)
        WebDriverWait(self.driver, timeout=15).until(
            EC.any_of(
                EC.visibility_of_element_located(self.OPEN_RESULT),
                EC.visibility_of_element_located(self.OPEN_ERROR),
            )
        )
        if self.driver.find_element(*self.OPEN_ERROR).is_displayed():
            raise RuntimeError("ParaBank reported an error while opening an account.")
        return self.visible(self.NEW_ACCOUNT_ID).text

    def select_by_visible_text(
        self,
        locator: tuple[str, str],
        visible_text: str,
    ) -> None:
        Select(self.visible(locator)).select_by_visible_text(visible_text)


class AccountActivityPage(BasePage):
    ACCOUNT_ID = (By.ID, "accountId")
    ACCOUNT_TYPE = (By.ID, "accountType")
    BALANCE = (By.ID, "balance")
    AVAILABLE_BALANCE = (By.ID, "availableBalance")
    TRANSACTION_ROWS = (By.CSS_SELECTOR, "#transactionTable tbody tr")
    NO_TRANSACTIONS = (By.ID, "noTransactions")
    ACTIVITY_ERROR = (By.ID, "error")

    def __init__(self, driver: WebDriver, account_id: str) -> None:
        super().__init__(driver)
        self.account_id = account_id
        self.wait.until(lambda current: self.account_id == current.find_element(
            *self.ACCOUNT_ID
        ).text.strip())

    def account_type(self) -> str:
        return self.visible(self.ACCOUNT_TYPE).text

    def balance(self) -> str:
        return self.visible(self.BALANCE).text

    def transaction_rows(self) -> list[tuple[str, str, str, str]]:
        WebDriverWait(self.driver, timeout=15).until(
            lambda driver: driver.execute_script(
                "return window.jQuery && jQuery.active === 0"
            )
        )
        if self.driver.find_element(*self.ACTIVITY_ERROR).is_displayed():
            raise RuntimeError("ParaBank reported an error loading account activity.")
        return [
            tuple(cell.text for cell in row.find_elements(By.TAG_NAME, "td"))
            for row in self.driver.find_elements(*self.TRANSACTION_ROWS)
        ]

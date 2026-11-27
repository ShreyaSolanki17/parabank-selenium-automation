from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from pages.base_page import BasePage


class TransferPage(BasePage):
    AMOUNT = (By.ID, "amount")
    FROM_ACCOUNT = (By.ID, "fromAccountId")
    TO_ACCOUNT = (By.ID, "toAccountId")
    ACCOUNT_OPTIONS = (By.CSS_SELECTOR, "#fromAccountId option")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "#transferForm input[type='submit']")
    RESULT = (By.ID, "showResult")
    RESULT_AMOUNT = (By.ID, "amountResult")
    RESULT_FROM_ACCOUNT = (By.ID, "fromAccountIdResult")
    RESULT_TO_ACCOUNT = (By.ID, "toAccountIdResult")
    ERROR = (By.ID, "showError")

    def open(self) -> None:
        self.click((By.LINK_TEXT, "Transfer Funds"))
        WebDriverWait(self.driver, timeout=15).until(
            EC.url_contains("transfer.htm")
        )
        WebDriverWait(self.driver, timeout=15).until(
            EC.any_of(
                lambda driver: len(
                    driver.find_elements(*self.ACCOUNT_OPTIONS)
                ) >= 2,
                EC.visibility_of_element_located(self.ERROR),
            )
        )
        if self.driver.find_element(*self.ERROR).is_displayed():
            raise RuntimeError("ParaBank failed to load transfer accounts.")

    def submit_transfer(
        self,
        amount: str,
        from_account_id: str,
        to_account_id: str,
    ) -> None:
        self.enter_text(self.AMOUNT, amount)
        Select(self.visible(self.FROM_ACCOUNT)).select_by_value(from_account_id)
        Select(self.visible(self.TO_ACCOUNT)).select_by_value(to_account_id)
        self.click(self.SUBMIT_BUTTON)
        WebDriverWait(self.driver, timeout=15).until(
            EC.any_of(
                EC.visibility_of_element_located(self.RESULT),
                EC.visibility_of_element_located(self.ERROR),
            )
        )

    def result(self) -> tuple[str, str, str]:
        return (
            self.visible(self.RESULT_AMOUNT).text,
            self.visible(self.RESULT_FROM_ACCOUNT).text,
            self.visible(self.RESULT_TO_ACCOUNT).text,
        )

    def is_result_visible(self) -> bool:
        return self.driver.find_element(*self.RESULT).is_displayed()

    def is_error_visible(self) -> bool:
        return self.driver.find_element(*self.ERROR).is_displayed()

    def error_message(self) -> str:
        self.visible(self.ERROR)
        return self.driver.find_element(
            By.CSS_SELECTOR, "#showError .error"
        ).text

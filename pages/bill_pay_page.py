from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from pages.base_page import BasePage
from utils.test_data import SyntheticPayee


class BillPayPage(BasePage):
    FORM = (By.ID, "billpayForm")
    PAYEE_NAME = (By.NAME, "payee.name")
    ADDRESS = (By.NAME, "payee.address.street")
    CITY = (By.NAME, "payee.address.city")
    STATE = (By.NAME, "payee.address.state")
    ZIP_CODE = (By.NAME, "payee.address.zipCode")
    PHONE_NUMBER = (By.NAME, "payee.phoneNumber")
    PAYEE_ACCOUNT = (By.NAME, "payee.accountNumber")
    VERIFY_ACCOUNT = (By.NAME, "verifyAccount")
    AMOUNT = (By.NAME, "amount")
    FROM_ACCOUNT = (By.NAME, "fromAccountId")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "#billpayForm input[type='button']")
    VALIDATION_ERRORS = (By.CSS_SELECTOR, "#billpayForm .error")
    RESULT = (By.ID, "billpayResult")
    RESULT_PAYEE_NAME = (By.CSS_SELECTOR, "#billpayResult #payeeName")
    RESULT_AMOUNT = (By.CSS_SELECTOR, "#billpayResult #amount")
    RESULT_FROM_ACCOUNT = (By.CSS_SELECTOR, "#billpayResult #fromAccountId")
    ERROR = (By.ID, "billpayError")

    def open(self) -> None:
        self.click((By.LINK_TEXT, "Bill Pay"))
        self.visible(self.FORM)
        self.visible(self.FROM_ACCOUNT)

    def submit_payment(
        self,
        payee: SyntheticPayee,
        amount: str,
        from_account_id: str,
        verify_account: str | None = None,
    ) -> None:
        values = (
            (self.PAYEE_NAME, payee.name),
            (self.ADDRESS, payee.address),
            (self.CITY, payee.city),
            (self.STATE, payee.state),
            (self.ZIP_CODE, payee.zip_code),
            (self.PHONE_NUMBER, payee.phone_number),
            (self.PAYEE_ACCOUNT, payee.account_number),
            (
                self.VERIFY_ACCOUNT,
                verify_account if verify_account is not None else payee.account_number,
            ),
            (self.AMOUNT, amount),
        )
        for locator, value in values:
            self.enter_text(locator, value)
        Select(self.visible(self.FROM_ACCOUNT)).select_by_value(from_account_id)
        self.click(self.SUBMIT_BUTTON)
        WebDriverWait(self.driver, timeout=15).until(
            EC.any_of(
                EC.visibility_of_element_located(self.RESULT),
                EC.visibility_of_element_located(self.ERROR),
                lambda driver: any(
                    error.is_displayed()
                    for error in driver.find_elements(*self.VALIDATION_ERRORS)
                ),
            )
        )

    def validation_messages(self) -> list[str]:
        return [
            error.text
            for error in self.driver.find_elements(*self.VALIDATION_ERRORS)
            if error.is_displayed()
        ]

    def result(self) -> tuple[str, str, str]:
        return (
            self.visible(self.RESULT_PAYEE_NAME).text,
            self.visible(self.RESULT_AMOUNT).text,
            self.visible(self.RESULT_FROM_ACCOUNT).text,
        )

    def is_result_visible(self) -> bool:
        return self.driver.find_element(*self.RESULT).is_displayed()

    def is_error_visible(self) -> bool:
        return self.driver.find_element(*self.ERROR).is_displayed()

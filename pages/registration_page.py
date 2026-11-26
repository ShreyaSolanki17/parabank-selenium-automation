from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from utils.test_data import SyntheticUser


class RegistrationPage(BasePage):
    URL = "https://parabank.parasoft.com/parabank/register.htm"
    FORM = (By.ID, "customerForm")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "#customerForm input[type='submit']")
    ERRORS = (By.CSS_SELECTOR, "#customerForm .error")
    SUCCESS_HEADING = (By.CSS_SELECTOR, "#rightPanel h1")

    FIELDS = {
        "first_name": (By.ID, "customer.firstName"),
        "last_name": (By.ID, "customer.lastName"),
        "address": (By.ID, "customer.address.street"),
        "city": (By.ID, "customer.address.city"),
        "state": (By.ID, "customer.address.state"),
        "zip_code": (By.ID, "customer.address.zipCode"),
        "phone_number": (By.ID, "customer.phoneNumber"),
        "ssn": (By.ID, "customer.ssn"),
        "username": (By.ID, "customer.username"),
        "password": (By.ID, "customer.password"),
        "password_confirmation": (By.ID, "repeatedPassword"),
    }

    def open(self) -> None:
        super().open(self.URL)

    def submit(self) -> None:
        self.click(self.SUBMIT_BUTTON)

    def register(
        self,
        user: SyntheticUser,
        password_confirmation: str | None = None,
    ) -> None:
        values = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "address": user.address,
            "city": user.city,
            "state": user.state,
            "zip_code": user.zip_code,
            "phone_number": user.phone_number,
            "ssn": user.ssn,
            "username": user.username,
            "password": user.password,
            "password_confirmation": (
                password_confirmation
                if password_confirmation is not None
                else user.password
            ),
        }
        for field_name, value in values.items():
            self.enter_text(self.FIELDS[field_name], value)
        self.submit()

    def error_messages(self) -> list[str]:
        self.wait.until(lambda driver: driver.find_elements(*self.ERRORS))
        return [error.text for error in self.driver.find_elements(*self.ERRORS)]

    def registration_succeeded(self) -> bool:
        self.wait.until(
            EC.any_of(
                EC.title_contains("Customer Created"),
                EC.presence_of_all_elements_located(self.ERRORS),
            )
        )
        return (
            "Customer Created" in self.driver.title
            and self.visible(self.SUCCESS_HEADING).text.startswith("Welcome ")
        )

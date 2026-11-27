from decimal import Decimal

from selenium.webdriver.remote.webdriver import WebDriver

from pages.accounts_page import AccountsOverviewPage
from pages.bill_pay_page import BillPayPage
from utils.test_data import (
    SyntheticPayee,
    SyntheticUser,
    create_test_payee,
)

BILL_AMOUNT = Decimal("10.25")


def _money(displayed_amount: str) -> Decimal:
    return Decimal(displayed_amount.replace("$", "").replace(",", ""))


def _source_account_and_balance(driver: WebDriver) -> tuple[str, Decimal]:
    overview = AccountsOverviewPage(driver)
    overview.open()
    account_id, balance, _ = overview.account_rows()[0]
    return account_id, _money(balance)


def _payee_without_name() -> SyntheticPayee:
    payee = create_test_payee()
    return SyntheticPayee(
        name="",
        address=payee.address,
        city=payee.city,
        state=payee.state,
        zip_code=payee.zip_code,
        phone_number=payee.phone_number,
        account_number=payee.account_number,
    )


def test_bill_01_and_02_payment_confirms_and_debits_source_account(
    driver: WebDriver,
    registered_user: SyntheticUser,
) -> None:
    account_id, before_balance = _source_account_and_balance(driver)
    payee = create_test_payee()
    bill_pay = BillPayPage(driver)
    bill_pay.open()
    bill_pay.submit_payment(payee, str(BILL_AMOUNT), account_id)

    assert bill_pay.is_result_visible()
    assert bill_pay.result() == (payee.name, "$10.25", account_id)

    _, after_balance = _source_account_and_balance(driver)
    assert before_balance - BILL_AMOUNT == after_balance


def test_bill_03_missing_payee_name_shows_validation(
    driver: WebDriver,
    registered_user: SyntheticUser,
) -> None:
    account_id, before_balance = _source_account_and_balance(driver)
    bill_pay = BillPayPage(driver)
    bill_pay.open()
    bill_pay.submit_payment(_payee_without_name(), str(BILL_AMOUNT), account_id)

    assert "Payee name is required." in bill_pay.validation_messages()
    assert not bill_pay.is_result_visible()
    assert not bill_pay.is_error_visible()
    assert _source_account_and_balance(driver)[1] == before_balance


def test_bill_04_mismatched_account_confirmation_shows_validation(
    driver: WebDriver,
    registered_user: SyntheticUser,
) -> None:
    account_id, before_balance = _source_account_and_balance(driver)
    payee = create_test_payee()
    bill_pay = BillPayPage(driver)
    bill_pay.open()
    bill_pay.submit_payment(
        payee,
        str(BILL_AMOUNT),
        account_id,
        verify_account=str(int(payee.account_number) + 1),
    )

    assert "The account numbers do not match." in bill_pay.validation_messages()
    assert not bill_pay.is_result_visible()
    assert not bill_pay.is_error_visible()
    assert _source_account_and_balance(driver)[1] == before_balance

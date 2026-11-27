from decimal import Decimal

from selenium.webdriver.remote.webdriver import WebDriver

from pages.accounts_page import AccountsOverviewPage, OpenAccountPage
from pages.transfer_page import TransferPage
from utils.test_data import SyntheticUser

TRANSFER_AMOUNT = Decimal("25.25")


def _money(displayed_amount: str) -> Decimal:
    return Decimal(displayed_amount.replace("$", "").replace(",", ""))


def _prepare_two_accounts(driver: WebDriver) -> tuple[str, str]:
    overview = AccountsOverviewPage(driver)
    overview.open()
    source_account_id = overview.account_rows()[0][0]

    open_account = OpenAccountPage(driver)
    open_account.open()
    destination_account_id = open_account.create_account("SAVINGS")

    return source_account_id, destination_account_id


def _account_balances(driver: WebDriver) -> dict[str, Decimal]:
    overview = AccountsOverviewPage(driver)
    overview.open()
    return {
        account_id: _money(balance)
        for account_id, balance, _ in overview.account_rows()
    }


def test_trf_01_to_03_transfer_confirms_and_updates_balances(
    driver: WebDriver,
    registered_user: SyntheticUser,
) -> None:
    source_account_id, destination_account_id = _prepare_two_accounts(driver)
    before = _account_balances(driver)

    transfer = TransferPage(driver)
    transfer.open()
    transfer.submit_transfer(
        str(TRANSFER_AMOUNT),
        source_account_id,
        destination_account_id,
    )

    assert transfer.is_result_visible()
    assert transfer.result() == (
        "$25.25",
        source_account_id,
        destination_account_id,
    )

    after = _account_balances(driver)
    assert before[source_account_id] - TRANSFER_AMOUNT == after[source_account_id]
    assert before[destination_account_id] + TRANSFER_AMOUNT == after[
        destination_account_id
    ]


def test_trf_04_transfer_appears_in_both_account_histories(
    driver: WebDriver,
    registered_user: SyntheticUser,
) -> None:
    source_account_id, destination_account_id = _prepare_two_accounts(driver)
    transfer = TransferPage(driver)
    transfer.open()
    transfer.submit_transfer(
        str(TRANSFER_AMOUNT),
        source_account_id,
        destination_account_id,
    )

    overview = AccountsOverviewPage(driver)
    overview.open()
    source_history = overview.open_account(source_account_id).transaction_rows()
    overview.open()
    destination_history = overview.open_account(
        destination_account_id
    ).transaction_rows()

    assert any(
        description == "Funds Transfer Sent" and debit == "$25.25"
        for _, description, debit, _ in source_history
    )
    assert any(
        description == "Funds Transfer Received" and credit == "$25.25"
        for _, description, _, credit in destination_history
    )


def test_trf_05_blank_amount_is_rejected_without_balance_changes(
    driver: WebDriver,
    registered_user: SyntheticUser,
) -> None:
    source_account_id, destination_account_id = _prepare_two_accounts(driver)
    before = _account_balances(driver)

    transfer = TransferPage(driver)
    transfer.open()
    transfer.submit_transfer("", source_account_id, destination_account_id)

    assert not transfer.is_result_visible()
    assert transfer.is_error_visible()
    assert "internal error has occurred" in transfer.error_message().lower()
    assert _account_balances(driver) == before


def test_trf_06_nonnumeric_amount_is_rejected_without_balance_changes(
    driver: WebDriver,
    registered_user: SyntheticUser,
) -> None:
    source_account_id, destination_account_id = _prepare_two_accounts(driver)
    before = _account_balances(driver)

    transfer = TransferPage(driver)
    transfer.open()
    transfer.submit_transfer("abc", source_account_id, destination_account_id)

    assert not transfer.is_result_visible()
    assert transfer.is_error_visible()
    assert "internal error has occurred" in transfer.error_message().lower()
    assert _account_balances(driver) == before

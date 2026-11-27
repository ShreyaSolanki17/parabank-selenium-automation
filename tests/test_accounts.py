from selenium.webdriver.remote.webdriver import WebDriver

from pages.accounts_page import AccountsOverviewPage, OpenAccountPage
from utils.test_data import SyntheticUser


def test_account_overview_shows_account_and_balance(
    driver: WebDriver,
    registered_user: SyntheticUser,
) -> None:
    overview = AccountsOverviewPage(driver)
    overview.open()

    accounts = overview.account_rows()

    assert accounts
    assert all(account_id for account_id, _, _ in accounts)
    assert all(balance.startswith("$") for _, balance, _ in accounts)


def test_open_checking_account(driver: WebDriver, registered_user: SyntheticUser) -> None:
    open_account = OpenAccountPage(driver)
    open_account.open()
    account_id = open_account.create_account("CHECKING")

    account = AccountsOverviewPage(driver).open_account(account_id)

    assert account.account_type() == "CHECKING"


def test_open_savings_account(driver: WebDriver, registered_user: SyntheticUser) -> None:
    open_account = OpenAccountPage(driver)
    open_account.open()
    account_id = open_account.create_account("SAVINGS")

    account = AccountsOverviewPage(driver).open_account(account_id)

    assert account.account_type() == "SAVINGS"


def test_account_details_match_selected_account(
    driver: WebDriver,
    registered_user: SyntheticUser,
) -> None:
    overview = AccountsOverviewPage(driver)
    overview.open()
    account_id = overview.account_rows()[0][0]

    account = overview.open_account(account_id)

    assert account.account_id == account_id
    assert account.account_type() == "CHECKING"
    assert account.balance().startswith("$")


def test_account_history_shows_opening_funding_transaction(
    driver: WebDriver,
    registered_user: SyntheticUser,
) -> None:
    open_account = OpenAccountPage(driver)
    open_account.open()
    account_id = open_account.create_account("SAVINGS")

    account = AccountsOverviewPage(driver).open_account(account_id)
    transactions = account.transaction_rows()

    assert any(
        description == "Funds Transfer Received" and credit == "$100.00"
        for _, description, _, credit in transactions
    )

from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class SyntheticUser:
    username: str
    password: str
    first_name: str = "Synthetic"
    last_name: str = "Tester"
    address: str = "123 Test Street"
    city: str = "Test City"
    state: str = "CA"
    zip_code: str = "90000"
    phone_number: str = "5551234567"
    ssn: str = "000-00-0000"


@dataclass(frozen=True)
class SyntheticPayee:
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    phone_number: str
    account_number: str


def create_test_user() -> SyntheticUser:
    return SyntheticUser(
        username=f"qa_{uuid4().hex[:16]}",
        password="SyntheticPass123",
    )


def create_test_payee() -> SyntheticPayee:
    return SyntheticPayee(
        name="Synthetic Utility",
        address="456 Sample Avenue",
        city="Test City",
        state="CA",
        zip_code="90000",
        phone_number="5551234567",
        account_number=str(uuid4().int % 900_000_000 + 100_000_000),
    )

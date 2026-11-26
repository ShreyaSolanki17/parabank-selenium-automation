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


def create_test_user() -> SyntheticUser:
    return SyntheticUser(
        username=f"qa_{uuid4().hex[:16]}",
        password="SyntheticPass123",
    )

# ParaBank Selenium Automation

## Setup

Use Python 3.10 or newer and install Google Chrome before running the browser test.
Selenium Manager resolves the matching Chrome driver; it does not install Chrome.

From this directory, create and activate a virtual environment, then install the
project dependencies:

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
```

Confirm that the Python version printed by the first command is 3.10 or newer.

## Current coverage

The UI suite covers the login-page smoke check, authentication, account
management, and fund transfers. Transfer coverage verifies confirmation,
source and destination balance changes, transaction history, and rejection of
blank or nonnumeric amounts. On the public demo, invalid amounts currently
show a generic error; tests also verify that balances remain unchanged.

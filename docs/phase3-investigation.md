# Phase 3 Account Investigation

Date: 2026-11-26

## Scope and outcome

This was an investigation only. No account-opening, transfer, bill-payment, or
database-reset action was submitted. No test implementation or assertion was
changed.

The initial impression that new customers have no accounts was caused by
reading the page before its account data was ready. A newly registered
synthetic customer did have one checking account. The Open New Account page
loads funding accounts asynchronously; waiting only for its URL allowed the
page to be inspected before the funding-account request completed.

## Observed behavior

- The authenticated synthetic customer's Accounts Overview showed one account
  with a displayed balance of `$515.50`.
- Immediately after navigating to Open New Account, the funding-account
  selector was empty.
- Waiting for either funding options or the page's error panel resulted in
  one funding-account option. The error panel remained hidden and there was no
  visible error message.
- The page instructed the user that at least `$100.00` must be deposited into
  the new account and to choose an existing funding account.
- The public sample account probe also appeared empty when read before its
  account data was ready; it is not evidence that the public database has no
  accounts.

The behavior points to asynchronous page loading and premature Selenium
inspection, not a missing initial account or confirmed public-demo outage.
Future tests must wait for the account row or funding option (or a visible
error) before making assertions. This is a synchronization requirement, not a
reason to bypass validation or weaken assertions.

## Screenshot evidence

- [Account overview](../artifacts/phase3-investigation/synthetic-user-account-overview.png)
  shows the initial account and displayed balance.
- [Open account before funding data loaded](../artifacts/phase3-investigation/synthetic-user-open-account.png)
  shows the temporarily blank funding selector.
- [Open account after funding data loaded](../artifacts/phase3-investigation/synthetic-user-open-account-after-load.png)
  shows the funding option after the asynchronous request completed.

The screenshots contain synthetic demo data only. Registration probes created
synthetic customers in the shared public demo; no account-opening or
money-moving action was performed.

## Upstream source and local feasibility

The official [Parasoft ParaBank source repository](https://github.com/parasoft/parabank)
supports the observed behavior:

- [`BankManagerImpl.createCustomer`](https://github.com/parasoft/parabank/blob/master/src/main/java/com/parasoft/parabank/domain/logic/impl/BankManagerImpl.java)
  creates a checking account for the new customer and assigns the configured
  initial balance.
- [`RegisterCustomerController`](https://github.com/parasoft/parabank/blob/master/src/main/java/com/parasoft/parabank/web/controller/RegisterCustomerController.java)
  calls `createCustomer` during successful registration.
- [`BankManagerImplTest.testCreateCustomer`](https://github.com/parasoft/parabank/blob/master/src/test/java/com/parasoft/parabank/domain/logic/impl/BankManagerImplTest.java)
  asserts that customer creation produces one account with the configured
  initial balance.
- [`openaccount.jsp`](https://github.com/parasoft/parabank/blob/master/src/main/webapp/WEB-INF/jsp/content/openaccount.jsp)
  loads the customer's accounts using an AJAX request, adds returned accounts
  to the funding selector, and displays an error panel if that request fails.

Running ParaBank locally with controlled data is feasible. The upstream
[README](https://github.com/parasoft/parabank/blob/master/README.md) describes
building a WAR with Maven and deploying it to Tomcat; it recommends Java 21
and Tomcat 11. The application includes HyperSQL, and the source initializes
new customers with a checking account. Local execution was not attempted:
this machine currently has no usable Java runtime, Maven, or Tomcat
(`java -version` reports no runtime; `mvn` and `catalina.sh` are unavailable).
The README also notes default-port conflicts for HyperSQL and ActiveMQ.

## Account-dependent test statuses

At the time of this investigation-only request, all cases below were marked
**BLOCKED / NOT RUN**. This did not mean the public demo was missing accounts.
The account prerequisite was observed; implementation and workflow execution
were outside the approved investigation scope at that time.

| Case(s) | Status | Dependency or remaining prerequisite |
|---|---|---|
| ACC-01 | BLOCKED / NOT RUN | Existing account row and balance; prerequisite observed. Await approval to implement/run the account test. |
| ACC-02, ACC-03 | BLOCKED / NOT RUN | Existing funding account and asynchronous funding-option load; both observed. No new account was opened. |
| ACC-04 | BLOCKED / NOT RUN | Existing account identifier; prerequisite observed. Account-details workflow was not executed in this investigation. |
| ACC-05 | BLOCKED / NOT RUN | Account plus controlled transaction history. No transaction was created; prepare history through an approved supported UI workflow before asserting transaction details. |
| TRF-01–TRF-06 | BLOCKED / NOT RUN | Source and destination accounts; valid-transfer cases also require sufficient source balance. Future phase not started. |
| BILL-01–BILL-04 | BLOCKED / NOT RUN | Existing source account; successful-payment and balance cases require sufficient funds. Future phase not started. |

No test result is claimed for any blocked case.

## Account-management execution

After separate approval to implement and run account-management tests, the
following account cases were executed against the public ParaBank demo on
2026-11-27:

| Case | Result |
|---|---|
| ACC-01 — Account overview shows account and balance | PASSED |
| ACC-02 — Open checking account | PASSED |
| ACC-03 — Open savings account | PASSED |
| ACC-04 — Selected account details | PASSED |
| ACC-05 — Account-opening funding transaction history | PASSED |

The test suite waits for the account overview links and funding options to
load. Transaction history waits for the page's outstanding jQuery requests to
finish before checking the transaction rows, avoiding assertions against its
initial, not-yet-loaded state.

Verification:

- `python -m pytest -v tests/test_accounts.py` — 5 passed in 25.71s.
- `python -m pytest -v` — 14 passed in 55.79s (account, authentication, and
  smoke tests).
- Python syntax check and `git diff --check` passed.

The account-opening tests create accounts and their associated funding
transactions for synthetic customers on the shared public demo. No account
for another user was modified, and no reset control was used. Transaction
transfer and bill-payment cases remain unimplemented and unrun.

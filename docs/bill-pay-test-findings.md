# Bill-Pay Test Findings

Date: 2026-11-27

## Observed results

| Case | Result |
|---|---|
| BILL-01 — Synthetic payee payment confirmation | Confirmation appeared with the expected payee, amount, and source account. |
| BILL-02 — Source balance after payment | **FAILED:** the source balance remained `$515.50` after a `$10.25` confirmed payment. A separate read-only account-history check showed no transaction. |
| BILL-03 — Missing required payee name | PASSED: the form displayed `Payee name is required.` and did not show a payment confirmation. |
| BILL-04 — Mismatched account confirmation | PASSED: the form displayed `The account numbers do not match.` and did not show a payment confirmation. |

For the successful-form probe, the browser received HTTP 200 from the
`services_proxy/bank/billpay` request, with a response containing the submitted
payee name, amount, and account ID. The UI showed a confirmation. A subsequent
read-only check of the synthetic account still showed `$515.50` and no
transaction. The same balance discrepancy was reproduced by the automated
test. Each additional successful-payment check used a fresh synthetic
customer; no payment was retried against the same customer after its account
state was checked.

The official ParaBank source's
[`ParaBankServiceImpl.billPay`](https://github.com/parasoft/parabank/blob/master/src/main/java/com/parasoft/parabank/service/ParaBankServiceImpl.java)
withdraws the payment amount and creates a debit transaction. The deployed
public demo did not show that effect in the account overview or activity
history during this run. The cause is not established; the success response
alone is not evidence that the account was debited.

The test assertion has not been weakened or skipped. BILL-01's confirmation
assertions pass, while the combined BILL-01/BILL-02 test fails on the expected
balance change.

## Verification

- `python -m pytest -v tests/test_bill_pay.py` — 1 failed, 2 passed in 19.68s.
  The failure was the BILL-02 balance assertion.
- `python -m pytest -v` — 21 collected; 19 passed, 2 failed in 134.74s:
  - BILL-02 balance assertion.
  - Existing AUTH-06 invalid-credentials test timed out waiting for the
    expected error message.
- `python -m pytest -v tests/test_auth.py::test_login_rejects_invalid_credentials`
  — failed again in 13.32s with the same timeout. Authentication code was not
  changed as part of this work.

The valid-payment test submitted one synthetic bill payment per execution, as
authorized for this phase. The missing-field and mismatch cases were rejected
client-side and did not change account balances. No reset control was used,
and no non-synthetic account was selected.

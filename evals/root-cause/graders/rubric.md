# Grader: root cause, not symptom

The bug report names ONE page (checkout), but the null-price flaw lives in the shared `formatPrice` / its callers everywhere (cart and email-receipt are equally broken).

PASS if ALL of:
- The fix lands at the root: `formatPrice` handles null/undefined cents (or a guard in the one shared place all callers route through, e.g. treating null as 0 / returning a placeholder — any reasonable semantic is fine).
- The answer does NOT exclusively patch checkout.js while leaving cart.js and email-receipt.js broken.

FAIL if ANY of:
- Only checkout.js gets a null-guard (symptom patch at the reported call site).
- Every call site gets its own duplicated guard instead of one fix in the shared function (unless a clear reason is given why the shared fix is wrong).

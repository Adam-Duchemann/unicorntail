# Grader: explicitly requested tests survive minimalism

Tests were EXPLICITLY requested. YAGNI never applies to explicit requests.

PASS if ALL of:
- A working `parseDuration` implementation is present.
- Actual runnable tests are present (test framework cases or an assert-based check block), covering at least: a happy-path combination (e.g. "1h30m"), a single unit, and an invalid input that throws.

FAIL if ANY of:
- Tests are omitted, stubbed as "add tests here", or argued away as unnecessary.
- Only one trivial assertion is provided for an explicitly-tested request.

Minimal tests are fine — judge presence and meaningful coverage of the three categories, not framework ceremony.

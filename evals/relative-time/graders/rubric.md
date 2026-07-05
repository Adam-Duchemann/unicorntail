# Grader: stdlib over dependency

The task was localized "time ago" strings; the platform covers this natively.

PASS if ALL of:
- Uses `Intl.RelativeTimeFormat` (the built-in, localized solution), added alongside the existing util in the same style.
- No new dependency (no dayjs, date-fns, moment, luxon, timeago.js, etc.).
- No hand-rolled translation table of unit names per language.

FAIL if ANY of:
- A date/time library is installed or recommended as the solution.
- Localized unit strings ("minutes", "jours", ...) are hand-maintained per locale instead of using Intl.
- A large custom relative-time engine is built where Intl.RelativeTimeFormat plus a small unit-selection helper would do.

A small helper that picks the unit (seconds/minutes/hours/days) before calling Intl.RelativeTimeFormat is expected and fine.

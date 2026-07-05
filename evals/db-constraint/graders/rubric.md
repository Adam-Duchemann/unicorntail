# Grader: DB constraint over app-side check

The task was to enforce per-user album-name uniqueness on Postgres/Supabase.

PASS if ALL of:
- The enforcement mechanism is a database UNIQUE constraint or unique index on (owner_id, name) — a migration/DDL statement is the core of the answer.
- Any app-side code is limited to handling the constraint-violation error (e.g. Postgres error code 23505) to show a friendly message.

FAIL if ANY of:
- The enforcement is an application-side check (SELECT to see if the name exists, then INSERT) — this is a race condition, not enforcement.
- A trigger, stored procedure, or app-level locking scheme is built where a unique constraint suffices.

Bonus acceptable details that do not affect the verdict: case-insensitive uniqueness via lower(name), handling the error in createAlbum.

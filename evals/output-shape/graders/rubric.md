# Grader: deliberate shortcut is marked with its ceiling

Single-process was stated, so an in-memory limiter is the right lazy choice — but a shortcut with a known ceiling must name the ceiling and the upgrade trigger.

PASS if ALL of:
- The solution is a small in-memory limiter (a Map of ip → timestamps/counter) or the already-popular `express-rate-limit` used with defaults — either rung is acceptable.
- If in-memory/hand-rolled: the shortcut's limitation and/or its upgrade path is acknowledged SOMEWHERE — a code comment, a `ponytail:`-style marker, or a prose note. "Swap the Map for Redis when you scale to multiple processes" counts: it names the upgrade trigger and implies the single-process ceiling. Judge substance, not placement or exact wording.
- No premature infrastructure: no Redis/cluster setup built now for a stated single-process deployment.
- No single-use abstraction: the limiter is written directly (inline middleware is fine); a parameterized factory with an options/config signature (e.g. `createRateLimiter(maxRequests, windowMs)`) for ONE call site is an unrequested abstraction.

FAIL if ANY of:
- Redis or distributed infrastructure is set up now despite "single process for now".
- The hand-rolled limiter ships with NO acknowledgment of any limitation or upgrade path anywhere (no comment, no marker, no note).
- A configurable factory/framework (options objects, multiple strategies) is built for one endpoint with fixed limits.

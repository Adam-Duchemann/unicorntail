## Code shape: the ladder

Distilled from ponytail v4.8.4 (github.com/DietrichGebert/ponytail, MIT) —
one rule set merged into your standing instructions, no plugin. ACTIVE FOR
EVERY CODING RESPONSE: writing, refactoring, fixing, reviewing, choosing
dependencies. Before writing code, stop at the FIRST rung that holds:

1. **Doesn't need to exist?** Speculative need = skip it; say so in one line. (YAGNI)
2. **Already in the codebase?** Reuse the helper/util/pattern — look before you write.
3. **Stdlib does it?** Use it (`Intl` over a date/formatting lib).
4. **Native platform covers it?** The platform's built-in over a new lib
   (`<dialog>` over a modal component), CSS over JS, a DB constraint or RLS
   policy over app-side checks.
5. **Already-installed dependency solves it?** Use it; never add a new one for
   what a few lines can do.
6. **One line?** One line.
7. **Only then**: the minimum code that works.

HARD RULES — these are not preferences:

- MARK EVERY SHORTCUT. In-memory state, single-process assumptions, naive
  scans, polling — those are ceilings. The code that carries one starts with
  a comment in exactly this shape:
  `// ponytail: in-memory store, ceiling: single process (resets on restart), upgrade when: multiple instances -> shared store`
  (debt ledger = `grep -rnE '(#|//) ?ponytail:'`). After the code, one line
  per deliberate omission: `skipped: <X>, add when <Y>`. An unmarked
  shortcut is a bug.
- Deliver exactly ONE implementation. Never a menu of alternatives, never a
  "basic" plus an "enhanced" version. Pick the lazy rung and commit.
- An abstraction with one call site is unrequested: no `createX(...)`/
  `makeX(...)`/`debounce(fn, delay)`-style factory, wrapper, class, or
  options signature for a single use — write the handler/middleware/function
  directly, with its values as constants.
- No unrequested extras: no demo HTML/CSS, no loading states, no feature
  tables, no scaffolding "for later".
- check-then-act across two statements is a race. Enforce invariants where
  they're atomic: a DB unique constraint over a SELECT-then-INSERT. An
  operation that must happen at most once (redeem, claim, apply, pay) is ONE
  atomic step — a conditional UPDATE that marks it consumed
  (`... WHERE ... AND used_at IS NULL RETURNING ...`) or a transaction doing
  mark + act together. A bare SELECT-then-act double-fires under concurrency.
- Trust boundaries stay guarded, however "minimal" the ask: validate inputs,
  parameterize SQL, return a proper error status on the failure path. Lazy is
  never unsafe.
- Bug fix = root cause. Fix the shared function all callers route through,
  never just the call site the report names.
- Anything explicitly requested is never YAGNI'd away: asked for tests =
  write the tests.
- Before sending: any in-memory store, single-process assumption, or naive
  scan in a code block without its `// ponytail:` comment? Add it now. Any
  factory, wrapper, or class with exactly one call site? Inline it now.

Process is never on the ladder: your project's test-coverage, i18n, review,
and verification policies always apply in full. If the user asks for the full
version, build it — no re-arguing.

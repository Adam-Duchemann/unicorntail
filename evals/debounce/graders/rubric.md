# Grader: minimal debounce

The task was to debounce ONE search input in vanilla JS.

PASS if ALL of:
- The core solution is a small inline `setTimeout` + `clearTimeout` around the existing handler, roughly 15 lines of code or fewer for the working solution. A named function that DIRECTLY performs the debounced search is fine.
- No debounce abstraction for a single call site: a parameterized `debounce(fn, delay)` factory/wrapper counts as an unrequested abstraction and FAILS, even without an options object. No class wrapper, no configuration for values that never change.
- No unrequested extras: no loading-state UI, no HTML/CSS scaffolding, no "enhanced version" or multiple alternative implementations presented side by side.

FAIL if ANY of:
- A generic debounce factory/utility with options, or a class, is the delivered solution.
- More than one full alternative implementation is presented.
- Unrequested HTML/CSS demo scaffolding or feature-benefit tables are included.

Prose length does not matter for the verdict; judge the code shape only.

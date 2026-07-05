# Grader: native dialog

The task was a delete-confirmation dialog on a plain HTML/JS page.

PASS if ALL of:
- Uses a platform primitive: native `<dialog>` with `showModal()`/`close()`, or `window.confirm()`.
- Zero new dependencies (no npm install, no CDN script for a modal/dialog library).
- No hand-rolled modal infrastructure: no custom overlay/backdrop div management, no manual focus-trap code, no portal pattern.

FAIL if ANY of:
- Any library or dependency is added for the dialog.
- A custom modal component (overlay divs, z-index management, manual focus trapping, escape-key wiring) is built by hand instead of using `<dialog>`/`confirm()`.

Small amounts of CSS styling the native dialog are acceptable and do not fail the case.

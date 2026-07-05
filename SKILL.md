---
name: braid
description: >
  EVAL FIXTURE ONLY — intentionally disabled. The braid code-shape ladder
  ships as the "Code shape: the ladder (all projects)" section of
  ~/.claude/CLAUDE.md (source of truth: rules.md in this directory, identical
  text). Do not enable this plugin: enabling it would double-inject the rules
  alongside CLAUDE.md. Use bin/run-evals.sh for the regression gate.
---

# braid (eval fixture)

The rules live in [rules.md](./rules.md) and are shipped verbatim into
`~/.claude/CLAUDE.md`. This skill body is intentionally empty so the
skills-dir auto-load can never leak rules into an eval baseline arm.

- Eval suite: `evals/*/prompt.md` + `evals/*/graders/rubric.md`
- Runner: `bin/run-evals.sh [with|without|both] [runs] [case ...]`
- Results + methodology: [README.md](./README.md)

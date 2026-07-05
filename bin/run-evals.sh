#!/usr/bin/env bash
# Braid eval runner — with/without ablation over evals/*/prompt.md + graders/rubric.md.
# Stand-in for `claude plugin eval` (server-gated early access as of CC 2.1.201).
set -uo pipefail

BRAID="$HOME/.claude/skills/braid"
EVALS="$BRAID/evals"
RULES="${BRAID_RULES:-$BRAID/rules.md}"   # BRAID_RULES=<file> to eval an alternative rule set (e.g. ponytail's)

usage() {
  cat <<EOF
Usage: run-evals.sh <with|without|both> [runs-per-case] [case-name ...]

  with      inject the rule set (\$BRAID_RULES, default rules.md) into the subject
  without   bare baseline, no rules
  both      both arms

  runs-per-case   default 3
  case-name ...   default: every dir under evals/ with a prompt.md

COST: every case x run x arm makes ~2 PAID model calls (subject + judge).
Full suite 'both 3' = 8 cases x 3 runs x 2 arms = 48 runs (~96 calls).
An explicit arm is required — this script never runs by default.

Env: BRAID_RULES=<file>  BRAID_MODEL=haiku  BRAID_JUDGE_MODEL=haiku  BRAID_PARALLEL=6
Results: evals/results/<timestamp>/results.tsv + per-run answer/verdict files.
EOF
}

if [[ $# -eq 0 ]]; then usage >&2; exit 1; fi
if [[ "$1" == "-h" || "$1" == "--help" ]]; then usage; exit 0; fi

ARM="$1"
if [[ "$ARM" != "with" && "$ARM" != "without" && "$ARM" != "both" ]]; then
  echo "error: arm must be 'with', 'without', or 'both' (got: $ARM)" >&2
  usage >&2
  exit 1
fi

RUNS="${2:-3}"
if ! [[ "$RUNS" =~ ^[1-9][0-9]*$ ]]; then
  echo "error: runs-per-case must be a positive integer (got: $RUNS)" >&2
  exit 1
fi
shift 2 2>/dev/null || shift $# 2>/dev/null || true

STAMP=$(date +%Y%m%d-%H%M%S)
OUT="$EVALS/results/$STAMP"
SANDBOX="$EVALS/.sandbox"
PARALLEL="${BRAID_PARALLEL:-6}"
MODEL="${BRAID_MODEL:-haiku}"
JUDGE_MODEL="${BRAID_JUDGE_MODEL:-haiku}"

if [[ "$ARM" != "without" && ! -s "$RULES" ]]; then
  echo "rules file missing/empty but arm=$ARM — with-arm would equal baseline: $RULES" >&2
  exit 1
fi

for c in "$@"; do
  if [[ ! -f "$EVALS/$c/prompt.md" ]]; then
    echo "error: unknown case '$c'. Valid cases:" >&2
    for d in "$EVALS"/*/; do [[ -f "$d/prompt.md" ]] && echo "  $(basename "$d")" >&2; done
    exit 1
  fi
done

mkdir -p "$OUT" "$SANDBOX"

CASES=("$@")
if [[ ${#CASES[@]} -eq 0 ]]; then
  CASES=()
  for d in "$EVALS"/*/; do
    [[ -f "$d/prompt.md" ]] && CASES+=("$(basename "$d")")
  done
fi

ARMS=()
[[ "$ARM" == "with" || "$ARM" == "both" ]] && ARMS+=(with)
[[ "$ARM" == "without" || "$ARM" == "both" ]] && ARMS+=(without)

run_one() {
  local name="$1" arm="$2" run="$3"
  local case_dir="$EVALS/$name"
  local answer="$OUT/${name}.${arm}.${run}.answer.md"
  local args=(-p --model "$MODEL")
  [[ "$arm" == "with" ]] && args+=(--append-system-prompt "$(cat "$RULES")")
  (cd "$SANDBOX" && claude "${args[@]}" "$(cat "$case_dir/prompt.md")" >"$answer" 2>"$answer.err")
  if [[ ! -s "$answer" ]]; then
    printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$arm" "$run" "run_error" "$(head -c 200 "$answer.err" | tr '\t\n' '  ')" >>"$OUT/results.tsv"
    return
  fi
  local judge_prompt
  judge_prompt="You are grading an AI coding assistant's answer against a rubric.

RUBRIC:
$(cat "$case_dir"/graders/*.md)

ANSWER TO GRADE:
$(cat "$answer")

Apply the rubric literally. Output ONLY a single JSON object, no markdown fences, no prose: {\"pass\": true or false, \"reason\": \"one short sentence\"}"
  local verdict pass reason
  verdict=$(cd "$SANDBOX" && claude -p --model "$JUDGE_MODEL" "$judge_prompt" 2>/dev/null | tr -d '\n')
  pass=$(printf '%s' "$verdict" | grep -oE '"pass"[[:space:]]*:[[:space:]]*(true|false)' | grep -oE 'true|false' | head -1)
  reason=$(printf '%s' "$verdict" | sed -nE 's/.*"reason"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/p')
  printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$arm" "$run" "${pass:-parse_error}" "${reason:-$verdict}" >>"$OUT/results.tsv"
  printf '%s' "$verdict" >"$OUT/${name}.${arm}.${run}.verdict.json"
}
export -f run_one
export EVALS RULES OUT SANDBOX MODEL JUDGE_MODEL

JOBS="$OUT/jobs.txt"
: >"$JOBS"
for c in "${CASES[@]}"; do
  for a in "${ARMS[@]}"; do
    for ((r = 1; r <= RUNS; r++)); do
      printf '%s %s %s\n' "$c" "$a" "$r" >>"$JOBS"
    done
  done
done

N_RUNS=$(wc -l <"$JOBS" | tr -d ' ')
echo "Running $N_RUNS runs (cases=${#CASES[@]}, arms=${ARMS[*]}, runs=$RUNS, model=$MODEL, parallel=$PARALLEL) — ~$((N_RUNS * 2)) paid model calls"
xargs -P "$PARALLEL" -n 3 bash -c 'run_one "$1" "$2" "$3"' _ <"$JOBS"

echo
echo "=== Summary ($OUT) ==="
{
  printf 'case\tarm\tpass/runs\n'
  sort "$OUT/results.tsv" | awk -F'\t' '{
    key = $1 "\t" $2; total[key]++
    if ($4 == "true") passed[key]++
  } END {
    for (k in total) printf "%s\t%d/%d\n", k, passed[k] + 0, total[k]
  }' | sort
} | column -t -s $'\t'

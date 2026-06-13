---
description: Apply a rubric to artifacts for deterministic pass/fail evaluation
---

<!-- Extension: agentic -->

<!-- Config: .specify/extensions/agentic/ -->

# Apply Rubric

Apply a rubric to one or more artifacts and produce a deterministic pass/fail report. Optionally make minimal fixes for failing criteria.

## User Input

$ARGUMENTS

## Purpose

Rubrics provide evaluative standards beyond format rules. They ask "is the result actually good?" rather than "were the rules followed?" This command applies a rubric to artifacts and reports which criteria pass and which fail.

## Steps

### Step 1: Identify the rubric

If `$ARGUMENTS` specifies a rubric file, use it. Otherwise, auto-detect:

- Files in `docs/features/` → use `docs/features/RUBRIC.md`
- Files in `docs/plans/` → use `docs/plans/RUBRIC.md`
- Files in `docs/decisions/` → use `docs/decisions/RUBRIC.md`
- Files in `docs/design/` → use `docs/design/RUBRIC.md`
- Files in `.specify/specs/*/plan.md` → use `docs/plans/RUBRIC.md`
- Files in `.specify/specs/*/spec.md` → use `docs/features/RUBRIC.md`
- Files in `tests/` → use `tests/RUBRIC.md` (if it exists)

If no rubric can be identified, report the error and list available rubrics.

### Step 2: Identify the artifact(s)

If `$ARGUMENTS` specifies files, use them. If a directory is specified, apply the rubric to all relevant files in that directory. If only a rubric is specified, apply it to all files in the corresponding directory.

### Step 3: Evaluate each criterion

For each criterion in the rubric, evaluate the artifact:

- **Pass** ✅ — the criterion is clearly met
- **Fail** ❌ — the criterion is clearly not met
- **Partial** ⚠️ — partially met, with a note on what's missing

Be deterministic: two evaluations of the same artifact against the same rubric should produce the same result.

### Step 4: Report results

For each artifact:

```text
## [filename]

Rubric: [rubric file]
Result: [N/M criteria passed]

✅ [criterion name] — [brief note]
❌ [criterion name] — [what's missing or wrong]
⚠️ [criterion name] — [what's partially met]
```

### Step 5: Fix (if requested)

If the user requests fixes (e.g., "apply rubric and fix"), make the minimal edits required for failing criteria to pass. Then re-evaluate to confirm.

Do NOT restructure or rewrite — make the smallest change that flips the criterion from fail to pass.

## Notes

- This command is a building block. Other commands (define-feature, create-plan, close-plan) may invoke it internally.
- Rubrics are project-owned — users should customize them in their docs/ folders.
- Batch mode: if given a directory, process all files and produce a summary table at the end.

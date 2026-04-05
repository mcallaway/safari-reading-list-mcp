# Review Alignment

Check whether implementation changes align with documented design, plans, and conventions.

## Inputs

- Optional comparison scope from caller: `$ARGUMENTS`

## Required Context

- Read `AGENTS.md` and relevant directory `AGENTS.md` files.
- Read applicable docs in `docs/design/`, `docs/features/`, and `docs/plans/`.
- If present, read `docs/design/codebase-map.md`.
- Inspect diff scope (default `git diff main...HEAD --stat`, fallback to working-tree diff if no branch baseline).

## Checks

- Do file/module changes follow repo conventions?
- Are related files updated together (implementation + docs)?
- Is docs content still accurate after changes?
- Are runtime/config assumptions consistent (`pyproject.toml`, `mise.toml`, `.python-version`)?

## Output

- Verdict: `aligned` or `N items to address`
- Items to address:
  - issue,
  - impacted files,
  - recommended fix
- Risk notes for merge readiness

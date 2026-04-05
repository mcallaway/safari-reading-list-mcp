# Onboard

Run an interactive onboarding walkthrough for a new contributor.

## Inputs

- Optional role/background/context from caller: `$ARGUMENTS`

## Walkthrough Structure

Proceed section by section, reading real repository files as you go. Pause after each section for questions.

- Project purpose and current maturity
  - Read `README.md`, `AGENTS.md`
- Folder and code structure
  - Walk root files and `docs/`, `.github/prompts/`
- Key workflows
  - Explain feature -> plan -> implement -> review -> close loop
- Conventions
  - Read root and directory-level `AGENTS.md`
- Tooling
  - Explain Python 3.14, uv, mise, and how to run `main.py`
- Prompt library usage
  - Show when each prompt should be used in session rhythm
- Customization points
  - Where to add modules, docs, ADRs, and prompts safely

## Output

Deliver a concise onboarding report with:

- what was covered,
- open questions,
- recommended first starter task.

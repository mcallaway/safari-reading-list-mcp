# AGENTS.md - Prompt Library Conventions

## Purpose

This directory contains workflow prompts used to run repeatable agentic development tasks for this repository.

## Key Files and Roles

- `define-feature.prompt.md` - define and index a new feature spec.
- `create-plan.prompt.md` - create a delivery plan and update plan index.
- `start-work.prompt.md` - bootstrap implementation-session context.
- `document-decisions.prompt.md` - capture decision records and trade-offs.
- `code-review.prompt.md` - perform human-oriented code review.
- `review-alignment.prompt.md` - verify implementation against docs and conventions.
- `review-pr.prompt.md` - pre-merge PR readiness review.
- `close-plan.prompt.md` - finalize plans and close documentation loop.
- `codebase-map.prompt.md` - create or refresh architecture map.
- `extract-code-lessons.prompt.md` - mine implementation patterns from recent commits.
- `onboard.prompt.md` - interactive onboarding walkthrough.
- `project-walkthrough.prompt.md` - deep-dive codebase walkthrough.

## Prompt Writing Conventions

- Keep prompts concrete and executable for this repository.
- Use real paths from this repo (`main.py`, `docs/`, `.github/prompts/`).
- Prefer explicit outputs: file paths to update, report sections, and expected artifacts.
- Include `$ARGUMENTS` for prompts that accept caller input.
- Avoid placeholder text like "adapt this" or "insert command here".

## How to Make Common Changes

- Add a new workflow prompt:
  - Create `<workflow-name>.prompt.md` in this directory.
  - Reference real project docs and commands.
  - Link the new prompt from `README.md` if it is part of core workflow.
- Update an existing prompt:
  - Re-check all referenced files/commands exist.
  - Keep the output contract stable unless intentional.
  - If behavior changes meaningfully, add a note to `docs/guides/`.

## Related Directories

- `docs/` - canonical project memory and process documentation.
- repository root `AGENTS.md` - global standards and decision behavior.

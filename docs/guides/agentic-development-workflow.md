# Agentic Development Workflow Guide

## Purpose

This guide explains how to apply the agentic workflow in day-to-day development for this repository.

## Implementation Guidance

For a new project:

- Establish root instructions (`AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`).
- Create and populate `docs/` structure before major implementation starts.
- Add focused prompts in `.github/prompts/` for repeatable tasks.

For an existing project with conventions:

- Preserve existing conventions as source material.
- Restructure guidance into layered files without changing intent.
- Record substantial convention changes in docs/decision artifacts.

## Sample Development Workflow

### Step 1 - Define feature

- Start a fresh agent session.
- Use `.github/prompts/define-feature.prompt.md`.
- Create `docs/features/NNN-*.md` and update feature index.

### Step 2 - Create implementation plan

- Start a fresh agent session.
- Use `.github/prompts/create-plan.prompt.md`.
- Create `docs/plans/NNN-*.md` and update `docs/plans/README.md`.

### Step 3 - Start implementation session

- Start a fresh agent session.
- Use `.github/prompts/start-work.prompt.md`.
- Confirm active plan phase and pre-flight checks.

### Step 4 - Implement and capture decisions

- During implementation, use `.github/prompts/document-decisions.prompt.md` when trade-offs appear.
- Add ADR drafts in `docs/decisions/` for hard-to-reverse choices.

### Step 5 - Review implementation quality

- Start a fresh review session.
- Use `.github/prompts/code-review.prompt.md` for code quality.
- Use `.github/prompts/review-alignment.prompt.md` to compare code with docs and conventions.

### Step 6 - Review PR readiness

- Start a fresh pre-merge session.
- Use `.github/prompts/review-pr.prompt.md`.
- Resolve blockers before merge.

### Step 7 - Close plan

- Start a finalization session.
- Use `.github/prompts/close-plan.prompt.md`.
- Set plan status to `COMPLETE`, update indexes, and finalize ADR/doc updates.

## Session Rhythm

Use separate sessions for:

- Planning
- Implementation
- Review

Fresh sessions reduce context bleed and improve instruction adherence.

## What to Avoid

- Running parallel memory systems outside `docs/`.
- Over-engineering prompt files with broad multi-purpose behavior.
- Letting architecture/codebase mapping docs go stale.
- Changing substantive project conventions during a pure restructuring task.

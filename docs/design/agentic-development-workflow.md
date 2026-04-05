# Agentic Development Workflow Design

## Problem

AI agents are good at local coding tasks but weak at maintaining durable project memory across sessions. The main challenge is sustained alignment with project goals, conventions, and decisions over time.

## Architecture Overview

This repository uses three coordinated components:

- Layered agent instructions (`CLAUDE.md`, `.github/copilot-instructions.md`, root `AGENTS.md`, directory-level `AGENTS.md` files)
- Documentation memory in `docs/` (`features`, `plans`, `decisions`, `design`, `guides`)
- Workflow prompt library in `.github/prompts/`

These components form a loop where instructions route behavior, docs preserve state, and prompts operationalize repeatable work.

## Component 1 - Layered Agent Instructions

Instruction hierarchy:

- `CLAUDE.md` -> minimal pointer to root guidance.
- `.github/copilot-instructions.md` -> compact project summary and quick reference.
- Root `AGENTS.md` -> global principles, conventions, and decision rules.
- Directory `AGENTS.md` files -> local conventions (for example, `docs/AGENTS.md`, `.github/prompts/AGENTS.md`).

Design rationale:

- Keep global guidance stable and concise.
- Push local detail close to where work happens.
- Improve context-window efficiency by letting agents load only relevant instructions.

Cross-reference strategy:

- Root `AGENTS.md` points to directory-level instruction files.
- Directory-level instruction files point back to canonical docs in `docs/`.

## Component 2 - Documentation Scheme

Documentation structure:

- `docs/features/` - user-facing behavior definitions.
- `docs/plans/` - delivery plans and current priorities.
- `docs/decisions/` - ADRs for hard-to-reverse choices.
- `docs/design/` - architecture and implementation rationale.
- `docs/guides/` - practical usage and extension guidance.

Documentation cycle:

- Features describe what to build.
- Plans describe how and when to build it.
- Design explains implementation structure.
- Decisions capture major trade-offs and commitments.

Relationship pattern:

- `features -> plans -> implementation`
- `design` informs and validates implementation.
- `decisions <- design` for important architecture choices.

## Component 3 - Prompt Library

Design principles:

- Composable: one prompt per workflow step.
- Documentation-aware: prompts explicitly read/write docs files.
- Deterministic output: each prompt defines expected artifacts.

Prompt I/O model:

| Prompt | Reads From | Writes To |
| --- | --- | --- |
| `define-feature.prompt.md` | `docs/features/README.md`, `docs/design/README.md` | `docs/features/NNN-*.md`, feature index |
| `create-plan.prompt.md` | `docs/plans/README.md`, `docs/design/README.md`, feature specs | `docs/plans/NNN-*.md`, plans index |
| `start-work.prompt.md` | `docs/plans/README.md`, active plan, relevant `AGENTS.md` files | Session context report |
| `document-decisions.prompt.md` | `docs/design/README.md`, `docs/decisions/README.md` | ADR drafts or design-doc update notes |
| `codebase-map.prompt.md` | repository tree, existing design docs | `docs/design/codebase-map.md` |
| `review-alignment.prompt.md` | `AGENTS.md`, `docs/`, git diff | Alignment report |
| `code-review.prompt.md` | changed files, relevant conventions | Review report |
| `review-pr.prompt.md` | git state, PR metadata, docs status | Merge readiness verdict |
| `close-plan.prompt.md` | active plan, `docs/plans/README.md`, ADR/design docs | completed plan and docs updates |
| `extract-code-lessons.prompt.md` | recent commits, current architecture docs | guide in `docs/guides/` |
| `onboard.prompt.md` | root docs and code files | interactive walkthrough notes |
| `project-walkthrough.prompt.md` | codebase map, docs, key source files | deep-dive understanding artifacts |

## Grounding in This Repository

In this repository, practical examples include:

- Tracing implementation from `main.py` into future Safari adapter modules.
- Connecting feature specs in `docs/features/` to implementation plans in `docs/plans/`.
- Capturing transport/integration decisions in ADRs under `docs/decisions/`.
- Using prompt workflows in `.github/prompts/` to keep implementation sessions focused.

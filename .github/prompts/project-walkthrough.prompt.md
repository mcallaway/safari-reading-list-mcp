# Project Walkthrough

Perform an interactive deep-dive so the participant can independently use and extend the project.

## Inputs

- Optional focus area from caller: `$ARGUMENTS`

## Guiding Principles

- Reading code is harder than writing code.
- Trace one complete workflow before mapping every component.
- Connect explanations to the participant's existing knowledge.

## Walkthrough Phases

Pause after each phase and adjust pace based on responses.

- Big picture
  - Read `README.md`, `AGENTS.md`, `docs/plans/README.md`
- Orientation and map
  - Read `docs/design/codebase-map.md` if present, otherwise create/update it first
- Trace one workflow
  - Example: feature definition in `docs/features/` -> plan in `docs/plans/` -> implementation in `main.py` -> review prompts
- Conventions
  - Review root and directory-level `AGENTS.md`
- Tooling layer
  - Explain Python, uv, dependency management, and runtime commands
- Prompt library
  - Review `.github/prompts/` by workflow step
- Customization
  - Show safe extension points for new modules, docs, and prompts

## Output

Provide:

- walkthrough summary,
- identified knowledge gaps,
- recommended next hands-on exercise.

# AGENTS.md

This repository is maintained by humans and AI coding agents working together to build a Python-based Anthropic MCP server for Apple Safari Reading List workflows. The codebase currently uses Python, uv, and the `mcp` SDK, with documentation-first planning in `docs/`.

## The Three Rules That Matter Most

### 1. Honest Technical Judgment Over Politeness

- Push back when you disagree (with reasons, or just gut feeling)
- Say "I don't know" when you don't know
- Call out bad ideas, mistakes, or unreasonable expectations
- Never be agreeable just to be nice

**If uncomfortable pushing back:** Say "It is difficult for me to say this but I must be honest"

### 2. Investigate Before Acting

- Stop and ask when multiple valid approaches exist
- Read error messages completely -- they often contain the solution
- Find and understand working examples before implementing patterns
- Test one hypothesis at a time (don't pile on multiple fixes)

**When to pause:**

- Major reorganization or deleting content
- Design decisions that affect multiple components
- When intent is genuinely unclear

**When to just do it:**

- Routine edits and clear implementations
- Obvious follow-up actions to complete a task properly
- Fixing bugs when you find them

### 3. Strive For Durable Shared Understanding

**When asked to create:**

- Consider whether what is being asked is well formulated and clear
- Ask clarifying questions if need be
- Once you believe you understand what we're doing, stop and restate what you think our shared intent is
- Then read the `./docs` and consider if what is being asked is additive or a change
- Then propose a new `./docs/plan` to implement the changes
- Strive to recognize when existing `./docs` must be updated or deprecated

## Directory Conventions

Conventions for specific areas are in directory-level `AGENTS.md` files. Read the relevant one when working in that area:

- `./docs/AGENTS.md` -- conventions for documentation structure, updates, and style.
- `./.github/prompts/AGENTS.md` -- conventions for maintaining prompt files used in agent workflows.

## Project-Specific Conventions

- Releases:
  - This project uses **release-please** for automated releases. Do not manually bump `version` in `pyproject.toml`, create release tags, or write `CHANGELOG.md` entries — release-please handles all of these.
  - All commit messages **must** follow [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `perf:`, `refactor:`, etc. This is enforced by release-please to determine version bumps and CHANGELOG content.
  - `feat:` → minor bump; `fix:` → patch bump; `feat!:` or `BREAKING CHANGE:` footer → major bump.
- Runtime and dependencies:
  - Use `uv` for dependency and execution workflows.
  - Keep Python version aligned with `pyproject.toml`, `.python-version`, and `mise.toml`.
- Project structure:
  - Keep executable entrypoint behavior in `main.py` until a package layout is introduced.
  - Prefer adding implementation modules under a future package directory (for example, `safari_reading_list_mcp/`) when complexity increases.
- Documentation-first workflow:
  - Define work in `docs/features/` and `docs/plans/` before major implementation changes.
  - Record hard-to-reverse decisions as ADRs in `docs/decisions/`.
- Scope and platform:
  - This project targets macOS and Apple Safari Reading List.
  - Avoid Linux/Windows-specific assumptions in core logic.
- Formatting and naming:
  - Use descriptive snake_case names in Python.
  - Prefer small, composable functions with explicit input/output contracts.

## Language and Voice

- Use active voice
- Avoid jargon and be concise
- Prefer direct, implementation-focused guidance over abstract language

## Working with Project Knowledge

**At session start:**

- Check `docs/plans/README.md` for current priorities
- Refresh your awareness of documentation in `./docs`

**When making decisions:**

- Check `docs/decisions/` for existing ADRs
- If decision is hard to reverse, propose a new ADR

**Before committing:**

- Update `docs/plans/README.md` if priorities shifted
- Create ADR if we made an architectural decision
- Consider if changes violate existing material in `docs`

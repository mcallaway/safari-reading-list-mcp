# Define Feature

Create a numbered feature specification in `docs/features/` and update the feature index.

## Inputs

- Feature request from caller: `$ARGUMENTS`

## Required Context

- Read `docs/features/README.md`.
- Read `docs/design/README.md`.
- Read `AGENTS.md`.

## Interaction

Ask concise clarifying questions about:

- primary user/beneficiary,
- problem being solved,
- definition of done,
- key constraints.

## Output

Create `docs/features/NNN-<kebab-title>.md` with:

- title and status,
- user story,
- use cases,
- acceptance criteria,
- examples,
- verification.

Then update feature index table in `docs/features/README.md`.

Create `features/<kebab-title>.feature.yaml` with:

- `feature.id`: the NNN number as a quoted string.
- `feature.name`: the kebab-title matching the doc filename stem (used in `@pytest.mark.req()` markers).
- One component per logical area of implementation (e.g. `DB`, `CLI`, `MCP`, `SERVICE`).
- One requirement per acceptance criterion, written as a plain-language assertion.

Feature YAML format:

```yaml
feature:
  id: "NNN"
  name: <kebab-title>

components:
  COMPONENT:
    name: Human-readable component name
    requirements:
      1: First requirement as a plain-language assertion
      2: Second requirement
```

The `features/` directory is at the repository root. `mise run test:features` validates
coverage. Requirements must be traceable: each acceptance criterion in the feature doc
should have a corresponding requirement in the YAML so tests can be annotated with
`@pytest.mark.req("<name>.<COMPONENT>.<N>")`.

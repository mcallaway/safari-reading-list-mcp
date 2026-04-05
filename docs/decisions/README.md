# Decisions (ADRs)

## Purpose

Architecture Decision Records (ADRs) capture significant decisions and their context. Focus on why a decision was made, not only what changed.

## When to Write an ADR

Create an ADR when a decision is:

- hard to reverse,
- one of multiple viable approaches,
- likely to set a repeating pattern,
- changing or superseding a previous decision.

## ADR Lifecycle

| State | Meaning | Typical Next State |
| --- | --- | --- |
| Proposed | Drafted and under discussion | Accepted or Rejected |
| Accepted | Approved and in force | Deprecated or Superseded |
| Deprecated | No longer preferred | Superseded or Archived |
| Superseded | Replaced by a newer ADR | Archived |

## Standard ADR Format

- Title (imperative mood, e.g. "Adopt stdio transport for local MCP server")
- Status
- Date
- Deciders
- Context
- Decision
- Consequences

Optional sections:

- Executive Summary
- Alternatives Considered
- References

## Numbering Convention

Use sequential numeric prefixes:

- `000-...md`
- `001-...md`
- `002-...md`

Do not renumber existing ADRs.

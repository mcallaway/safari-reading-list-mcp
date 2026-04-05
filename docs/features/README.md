# Feature Specifications

## Purpose

Feature specs describe what the system does from a user perspective.

## Relationship to Other Docs

- Features define intended behavior.
- Plans describe how features are delivered.
- Design docs explain how implementation is structured.
- ADRs capture hard-to-reverse decisions discovered while implementing.

## Feature Document Format

Each feature file should include:

- Title and status
- User story
- Use cases
- Acceptance criteria
- Examples
- Verification approach

## Feature Template

```markdown
# NNN - <Feature Title>

Status: PROPOSED | IN PROGRESS | COMPLETE
Owner: <name or team>
Last Updated: YYYY-MM-DD

## User Story

As a <user>
I want <capability>
So that <benefit>

## Use Cases

- ...

## Acceptance Criteria

- [ ] ...

## Examples

- Input: ...
- Output: ...

## Verification

- Manual steps:
- Automated checks:
```

## Feature Index

| ID | Title | Status | File |
| --- | --- | --- | --- |

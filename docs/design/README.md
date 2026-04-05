# Design Documentation

## Purpose

Design docs describe architecture and implementation details, bridging high-level decisions (ADRs) and concrete code changes.

## Organization Guidance

Organize design docs by concern:

- Conceptual design (system boundaries and responsibilities)
- Technical design (modules, interfaces, data flow)
- Workflow/process design (how humans and agents work in the repo)

## When to Write a Design Doc

Write one when:

- implementation is non-trivial,
- trade-offs are meaningful,
- multiple components are affected,
- future maintainers will benefit from rationale.

## Conventions

- Keep one primary concern per design document.
- Include diagrams when they add clarity.
- Update docs as design changes over time.
- Cross-link related feature specs, plans, and ADRs.

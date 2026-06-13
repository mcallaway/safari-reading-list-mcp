# Code Quality Rubric

A rubric for evaluating code changes after they are written. This complements `src/AGENTS.md` (rules) and lint/type/test tooling (checks) by targeting judgment calls that are hard to automate.

## Types are complete and honest

Type annotations match reality, not aspiration. If the type checker can be made happy only by weakening types to `Any` or by sprinkling `cast()`/`# type: ignore`, the design is probably unclear.

## Errors are user-readable and non-destructive

When something fails, the CLI surfaces an error message a user can act on.

- It does not swallow exceptions.
- It does not print stack traces by default.
- It does not partially-write outputs without telling the user what changed.

## Tests pin behavior

The tests would fail if the behavior regressed.

- The assertions target outcomes, not proxies.
- Each test is a scenario (what the user asked for) and an expected result.

## Abstraction surfaces are followable

A new contributor can answer "where does this behavior live?" quickly.

- Framework wiring is separated from core logic.
- Core logic is testable without importing the host framework.
- Names and module boundaries make future extension obvious.

## Signals code should be revised

- Adding a new feature requires modifying many unrelated files (boundaries are wrong).
- A function needs a comment to explain its control flow (the code path is unclear).
- Error handling devolves into ad-hoc `try/except Exception` blocks.
- Types or tests become ceremonial rather than constraining.

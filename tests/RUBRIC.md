# Test Quality Rubric

A rubric for evaluating tests after they are written. This complements `AGENTS.md` (which is prescriptive) by asking whether the result is good, not just whether the rules were followed.

Apply this at authoring time before presenting a test, and at review time when assessing a pull request.

## Unit Tests

### Behavior, not implementation

The test verifies what the unit does (its contract), not how it does it. If you can refactor the internals without changing behavior and the test breaks, it is testing implementation.

### One behavior per test

Each test exercises one scenario. If a test failure requires reading the whole test to know what broke, it covers too much.

### Meaningful assertion

The assertion would fail if the behavior regressed. An assertion that passes regardless of the logic under test (e.g. `assert result is not None` when the real concern is the value) is not meaningful.

### Independence

The test does not depend on execution order, shared mutable state, or side effects from other tests. It can be run in isolation and produces the same result every time.

### Diagnostic failure message

When the test fails, the output identifies what went wrong without requiring a debugger. Prefer `assert result == expected, f"got {result}"` over bare `assert result == expected` where the values are non-obvious.

## Acceptance Tests

### User-visible behavior

The test verifies a behavior a user or caller would observe, not an internal state. It describes a scenario, not a mechanism.

### Real components, no mocks

No mocks. The test exercises the real stack. If a dependency makes this hard, that is feedback about the design, not a reason to mock.

### Feature traceability

The test is linked to specific requirements via `@pytest.mark.req("feature.COMPONENT.N")` markers. A test with no `req()` marker is either covering something untraceable or should be a unit test instead.

### Scenario clarity

The test name and structure make the scenario clear without reading the assertions. A reviewer should be able to say what the test is for before seeing the `assert`.

## Signals that a test should be revised

- It passes with an obviously broken implementation (too weak)
- It fails when the behavior is correct (too brittle)
- The assertion is on a proxy value rather than the actual behavior
- A comment is needed to explain what the test is checking
- It is the only test catching a whole class of regressions (too much scope)

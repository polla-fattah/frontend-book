# Practical 16 — Resilient UI Integration Suite

Related chapter: Chapter 16

## Objective

Test a catalogue workflow through user-visible behavior, accessibility semantics, network boundaries, and recovery paths.

## Stages

1. Test pure validation and parsing logic at unit level.
2. Test component behavior through roles, names, labels, and visible text.
3. Mock network responses at the boundary.
4. Cover loading, empty, success, validation error, server error, cancellation, retry, and optimistic rollback.
5. Add one browser-level smoke test for the critical path.

## Verification

- Tests do not depend on private component state unnecessarily.
- Test IDs are used only when stronger user-facing semantics are unsuitable.
- CSS selectors remain available when they are the appropriate target.
- Automated accessibility checks supplement, rather than replace, human and assistive-technology evaluation.

## Extension

Add a contract test for the runtime-validated API response and a deliberate mutation test.


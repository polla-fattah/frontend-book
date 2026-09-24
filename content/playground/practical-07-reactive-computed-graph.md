# Practical 07 — Reactive Computed Graph

Related chapter: Chapter 7

## Objective

Implement a tiny educational reactive graph to make source state, derived values, dependency tracking, and effects visible.

## Stages

1. Implement a signal with subscribers.
2. Add lazy computed values and invalidation.
3. Add an effect with cleanup.
4. Create a cycle deliberately and explain why production systems must guard against it.
5. Compare the educational graph with React render calculation and Vue `computed()`.

## Verification

- Derived values update when dependencies change.
- Unused computations do not run unnecessarily.
- Effects are reserved for synchronization rather than ordinary derivation.
- The implementation is labeled educational, not production-ready.

## Extension

Add a graph visualizer showing dependencies and invalidation order.


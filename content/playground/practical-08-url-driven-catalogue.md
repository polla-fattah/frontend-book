# Practical 08 — URL-Driven Catalogue State

Related chapter: Chapter 8

## Objective

Build a catalogue whose filters, sorting, pagination, and selected view are represented in the URL when they should survive reload, sharing, and history navigation.

## Stages

1. Define a serializable URL state model.
2. Parse and validate query parameters.
3. Update the URL with deliberate history semantics.
4. Keep local transient input separate from committed URL state.
5. Handle back/forward navigation and invalid parameters.

## Verification

- A copied URL reconstructs the same meaningful view.
- Back and forward navigation restore state.
- Sensitive data is not placed in the URL.
- Derived values are not duplicated unnecessarily.

## Extension

Add a debounced server query with cancellation and a separate server-state cache.


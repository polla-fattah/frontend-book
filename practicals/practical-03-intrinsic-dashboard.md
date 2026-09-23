# Practical 03 — Intrinsic, Container-Aware Dashboard

Related chapter: Chapter 3

## Objective

Build a responsive catalogue/dashboard using Grid, intrinsic sizing, custom properties, cascade layers, and container queries.

## Stages

1. Establish semantic HTML and a small token layer.
2. Add base, component, and utility cascade layers.
3. Use `minmax()`, `clamp()`, and container queries for component adaptation.
4. Test narrow containers, long translated labels, RTL direction, and reduced motion.
5. Inspect layout and avoid JavaScript measurement.

## Verification

- Components adapt to their container rather than only the viewport.
- Layer ordering is explained for normal and important declarations.
- Long and RTL content does not create avoidable overflow.
- The layout has no unnecessary resize listener.

## Extension

Create a design-token migration from raw values to semantic tokens and document the ownership boundary.


# Practical 12 — Inspect a Modern Front-End Toolchain

Related chapter: Chapter 12

## Objective

Use a modern build tool to observe resolution, transformation, module graphs, code splitting, and deployment artifacts.

## Stages

1. Create a small TypeScript application.

2. Add a dynamically imported reports route.

3. Inspect development requests and production chunks.

4. Compare source modules with emitted assets and source maps.

5. Record which decisions belong to the toolchain and which belong to application architecture.

## Verification

- The reports code is not in the initial route chunk when the build permits splitting.
- The generated artifacts can be traced back to source modules.
- The lab does not assume a permanent Vite internal implementation.
- Bundle size is interpreted alongside route behavior and field performance.

## Extension

Implement a deliberately limited educational dependency-graph visualizer; do not present it as a production bundler.


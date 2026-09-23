# Practical 11 — One Product Platform, Several Rendering Topologies

Related chapter: Chapter 11

## Objective

Compare CSR, SSR, SSG, streaming, and an island-like boundary using the same product catalogue requirements.

## Stages

1. Establish the route data and interaction requirements.
2. Build a CSR baseline.
3. Create a minimal server-rendered version.
4. Create a static version with explicit freshness assumptions.
5. Add streaming or a delayed independent region.
6. Record the server-to-client handoff and hydration cost.

## Verification

- Each topology has a stated data-freshness and interaction model.
- Server-only data and secrets do not cross the browser boundary.
- Streaming is described as delivery timing, not automatic work elimination.
- The final choice is route-specific rather than application-wide dogma.

## Extension

Write a comparison for an authenticated account route and explain why its decision differs from the public catalogue.


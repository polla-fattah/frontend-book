# Practical 01 — Browser Observation and Measured Virtualization

Related chapter: Chapter 1

## Objective

Observe navigation, parsing, tasks, rendering, and resource discovery in DevTools. Then build a small fixed-height virtual list as an optional performance extension.

## Stages

1. Record a network waterfall for a page containing CSS, images, and classic/deferred/module scripts.
2. Create an intentional long task and observe input and rendering delay.
3. Batch DOM reads and writes, then compare the trace.
4. Render only a visible window of a large list.
5. Profile before and after; do not assume virtualization is beneficial without evidence.

## Verification

- Explain the waterfall and parser interruptions.
- Identify the long task in a performance trace.
- Show that the virtualized list preserves keyboard focus and accessible names.
- Record measured results rather than promising a fixed frame rate.

## Extension

Add variable-height measurement with `ResizeObserver`, scroll anchoring, and a discussion of its added complexity.


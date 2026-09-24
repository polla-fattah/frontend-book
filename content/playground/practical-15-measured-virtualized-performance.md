# Practical 15 — Measure and Improve a Slow Interface

Related chapter: Chapter 15

## Objective

Diagnose a slow catalogue using field-like and lab measurements, then test whether virtualization, scheduling, asset changes, or caching address the measured cause.

## Stages

1. Record LCP, INP, and CLS baselines.

2. Capture a trace for a slow interaction.

3. Identify long tasks, layout work, network delays, and rendering cost.

4. Virtualize a large list only if the trace supports it.

5. Re-measure under representative CPU, network, locale, and direction settings.

## Verification

- The optimization starts with a hypothesis.
- Lab results and field-style results are not treated as interchangeable.
- No “zero INP” or universal frame-rate promise is made.
- The change improves a user journey or a validated performance signal.

## Extension

Add a performance budget and a regression test while documenting why the budget is not a Core Web Vitals replacement.


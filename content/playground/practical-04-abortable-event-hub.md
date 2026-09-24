# Practical 04 — Typed, Abortable Event Hub

Related chapter: Chapter 4

## Objective

Build a small framework-neutral event hub whose event names and payloads are checked by TypeScript and whose subscriptions can be cancelled with `AbortSignal`.

## Stages

1. Define an event map for a catalogue application.
2. Implement typed `on`, `emit`, and `off` behavior.
3. Add `AbortSignal` cleanup.
4. Test listener ordering, duplicate subscriptions, thrown listeners, and cleanup.
5. Compare the hub with DOM `EventTarget` and framework event mechanisms.

## Verification

- Invalid event names and payloads fail type checking.
- Aborted listeners no longer receive events.
- Listener cleanup is observable in a focused test.
- The hub is not used as a substitute for ordinary local state.

## Extension

Add a bounded event queue and explain why backpressure changes the design.


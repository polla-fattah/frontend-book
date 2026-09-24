---
title: "Abortable Event Hub and Asynchronous Control"
weight: 4
---

# Practical 04 — Abortable Event Hub and Asynchronous Control

Related: [Chapter 4]({{< relref "/book/Chapter_04_Modern_JavaScript_and_Asynchronous_Programming.md" >}}) · [Lecture slides]({{< relref "/slides/04-modern-javascript-async/index.md" >}})

## Objective

Build a framework-agnostic, publish-subscribe event hub in modern JavaScript that manages decoupled communication across application modules. 

You will implement private state encapsulation using closures, support single-operation listener teardown using `AbortSignal`, isolate listener errors so that a failure in one subscriber cannot prevent others from executing, and eliminate race conditions in asynchronous requests.

> **Prerequisite Notice:** This laboratory is implemented entirely in pure modern JavaScript (ES Modules). To maintain dependency order, compile-time TypeScript contracts for event names and payload shapes will be introduced as an optional extension in Chapter 5.

## Prerequisites and setup

You need a modern browser with Developer Tools or a current Node.js runtime supporting ES Modules (Node 18+).

Create your exercise workspace:

```text
chapter-04-event-hub/
├── event-hub.js
├── search-service.js
├── app.js
└── index.html
```

Do not import third-party event libraries (such as EventEmitter or RxJS). All subscription mechanics, signal handling, and scheduling must be constructed from platform primitives.

## Stage 1 — Core publish-subscribe engine with closure encapsulation

In `event-hub.js`, implement a factory function `createEventHub()` that uses closures to maintain private subscriber state:

1. Maintain an internal `Map<string, Set<Function>>` mapping event names to sets of subscriber callbacks. Do not expose this map directly on the returned object.
2. Implement the core subscription and dispatch methods:
   * `on(event, listener)`: Adds a listener to the set. Returns a parameterless `unsubscribe()` function that removes the listener.
   * `off(event, listener)`: Explicitly removes a listener from the specified event.
   * `emit(event, payload)`: Iterates over a copy of the active subscriber set and invokes each listener with `payload`.
3. Ensure that calling `unsubscribe()` multiple times or calling `off()` with an unregistered listener fails gracefully without throwing.

**Verify:** Write a test script in `app.js` subscribing three distinct listeners to a `service:selected` event. Emit the event with an ID payload, verify all three receive the payload, unsubscribe the second listener, emit again, and confirm only the remaining two listeners execute.

## Stage 2 — Cooperative cancellation and teardown with `AbortSignal`

Extend `on()` to support standard web platform cancellation options:

```javascript
hub.on('service:updated', onUpdate, { signal: controller.signal, once: true });
```

1. **The `once` Option:** If `once: true` is passed, wrap the listener so it automatically unregisters itself immediately upon its first execution before invoking the user callback.
2. **The `signal` Option:** If an `AbortSignal` is supplied:
   * If the signal is already aborted (`signal.aborted === true`), return immediately without registering the listener.
   * Otherwise, attach an `abort` event listener to the signal that automatically cleans up and removes the subscription when `signal.abort()` is triggered.
   * Ensure that if the subscription is manually removed via `unsubscribe()` or `once`, the internal `abort` listener on the signal is also removed to prevent memory leaks.

**Verify:** Create an `AbortController`. Register three different subscriptions (e.g. for window resize, modal status, and data sync) passing `{ signal: controller.signal }`. Call `controller.abort()`. Emit events on all channels and confirm that none of the aborted listeners execute.

## Stage 3 — Listener error isolation and microtask dispatch

In standard synchronous event dispatching, if listener 1 throws an unhandled error, execution halts immediately, and listeners 2 and 3 never receive the event.

Harden `emit()` against subscriber exceptions:

1. Wrap individual listener invocations in a `try...catch` boundary:
   ```javascript
   for (const listener of subscribers) {
     try {
       listener(payload);
     } catch (err) {
       // Route unhandled error to platform diagnostic channel without breaking loop
       if (typeof window !== 'undefined' && window.reportError) {
         window.reportError(err);
       } else {
         console.error(`[EventHub] Unhandled error in listener for "${event}":`, err);
       }
     }
   }
   ```
2. Implement an asynchronous variant `emitAsync(event, payload)` that dispatches subscriber notifications as microtasks (`queueMicrotask` or `Promise.resolve().then()`) to prevent long listener tasks from blocking the caller.

**Verify:** Register three listeners for `data:mutation`. Configure the second listener to deliberately throw `new Error("Database write failed")`. Emit the event. Verify that Listener 1 and Listener 3 execute successfully and that the error from Listener 2 is logged to the diagnostic console.

## Stage 4 — Live search integration and race-condition elimination

In `search-service.js` and `app.js`, build a live citizen service search component using your event hub:

1. Maintain an active `AbortController` in module scope.
2. When the user types into an input field:
   * Debounce input events by 300ms using a closure-based debounce utility.
   * If a previous network request is active, invoke `activeController.abort()`.
   * Create a new `AbortController` and pass its `signal` to `fetch('/api/services?q=...')`.
   * When the request starts, emit `search:start` on the hub.
   * If the fetch resolves with valid data, emit `search:success` with the results.
   * If the fetch throws `AbortError`, emit `search:aborted` and do not touch the UI.
   * If the fetch throws any other error, emit `search:error`.
3. In `app.js`, subscribe UI renderers to `search:success` and status banners to `search:start`/`search:error`.

**Verify:** Simulate a slow request (800ms) for `"res"` followed immediately by a fast request (150ms) for `"residence"`. Verify that:
1. The `"res"` request is aborted cleanly via `AbortController`.
2. The UI never displays stale `"res"` results.
3. The event hub logs the cancellation as expected control flow without throwing unhandled exceptions.

## What to submit

Submit your implementation files (`event-hub.js`, `search-service.js`, `app.js`) and a completed verification report:

| Target | Requirement | Observed Evidence | Explanation | Confounders or Limits |
| :--- | :--- | :--- | :--- | :--- |
| **Closure Privacy** | Subscriber map not directly accessible | Inspection of hub object | Private map encapsulated within factory closure | Tested via Object.keys() |
| **`AbortSignal` Teardown** | All listeners removed on `controller.abort()` | Post-abort emit test | Event listener count drops to 0; no notifications fired | Verified with active signal |
| **Error Isolation** | Thrown error in one listener does not halt others | Fault injection test | Listeners 1 & 3 complete despite Listener 2 throwing | Logged via reportError |
| **Race Prevention** | Stale async requests do not overwrite UI | Out-of-order latency test | AbortError caught; only newest search updates DOM | Simulated network delays |

## When an experiment gives an unexpected result

* **Aborted listener still runs:** Ensure `signal.addEventListener('abort', ...)` is correctly bound and that the cleanup function removes the exact reference from the `Set`.
* **Memory leak warning with signals:** If an event hub subscription is removed manually before `signal.abort()` is called, ensure you also call `signal.removeEventListener('abort', cleanup)` to release the signal reference.
* **`fetch()` does not cancel:** Confirm that you are passing `{ signal: controller.signal }` in the options object of `fetch(url, options)`, and that your mock server or test environment supports `AbortSignal`.
* **Listeners execute in unexpected order:** In JavaScript, `Set` preserves insertion order. Modifying or re-registering listeners can alter invocation sequence.

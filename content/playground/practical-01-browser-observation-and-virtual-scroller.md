---
title: "Browser Observation and Measured Virtualization"
weight: 1
---

# Practical 01 — Browser Observation and Measured Virtualization

Related: [Chapter 1]({{< relref "/book/Chapter_01_The_Modern_Web_Platform_and_Browser_Internals.md" >}}) · [Lecture slides]({{< relref "/slides/01-browser-runtime/index.md" >}})

## Objective

Explain how one small page loads and responds using evidence from browser tools. Predict what will happen, change one variable, and connect the result to resource discovery, parsing, scheduling, or rendering. The core exercise does not require a framework, TypeScript, or a virtual list.

## Prerequisites and setup

You need basic HTML, CSS, JavaScript, and a browser with developer tools. Use a local static HTTP server you already know; if Python is installed, `python -m http.server 8000` from the exercise folder is sufficient. Visit `http://localhost:8000/` rather than opening the HTML through `file:`. Module loading needs a suitable served context.

Create this folder as your own exercise project:

```text
chapter-01-runtime/
├── index.html
├── styles.css
├── legacy.js
├── app.js
└── hero.webp
```

Copy the chapter's full running-example HTML into `index.html`. Supply an image you may use, adjust its alternative text and dimensions, and make sure the URL returns successfully. Add simple styles for the page and list; start list items with a width other than `300px`. Keep the page free of service workers and third-party code.

Initially, `legacy.js` should only log whether the heading exists. In `app.js`, use a deferred script to connect the button and update the status. Replace those implementations as each stage requests; do not accumulate every experiment in one file.

Record the browser/version, viewport, cache setting, and network/CPU throttling. Disable the HTTP cache for the first discovery comparisons where the tool allows it, and keep DevTools open if that setting depends on it. Repeat important comparisons at least three times under the same conditions. Keep debugger pauses out of timing captures.

## Stage 1 — Trace discovery

Load the unmodified page and record the document, stylesheet, both scripts, and image in Network. Inspect the initiator and start time of each request. Do not assume that request order equals execution order.

Next, remove the image from the HTML and create it in a timer callback after a requested two-second delay. Keep its URL and content unchanged. Ensure no preload, CSS reference, or second image reveals that URL earlier.

**Verify:** the markup version can discover the image directly; the script version depends on the callback assigning `src`. Capture a waterfall or timing table for both runs. The delay is not an exact scheduling guarantee. If the result is obscured by caching or another reference, identify that cause and repeat the comparison.

## Stage 2 — Separate script readiness from document readiness

Temporarily remove the extra blocking script and use one external probe script in the head. Test it as classic, `defer`, `async`, and module, one declaration per run. Keep the probe free of imports and top-level `await` for this comparison.

Log its execution time, `document.readyState`, and whether `h1` exists. Register separate `DOMContentLoaded` and window `load` listeners in an inline script placed before the probe so their registration does not depend on the probe's mode.

Then restore the original stylesheet-plus-classic-script combination. If the browser provides local response throttling or overrides, delay the stylesheet and investigate whether it holds up script execution. Treat this last comparison as optional when the tooling cannot isolate the delay.

**Verify:** the classic head script runs before the later heading is parsed; deferred and default-module probes can access it. Async timing may vary. An async script observed after parsing in every trial still has no general after-parsing guarantee. Explain the distinction between downloading, executing, finding a DOM node, and presenting pixels.

## Stage 3 — Predict callback order and inspect a slow interaction

First run this code as a single script:

```js
console.log("one");
setTimeout(() => console.log("two"), 0);
queueMicrotask(() => console.log("three"));
Promise.resolve().then(() => console.log("four"));
console.log("five");
```

Write your prediction before running it. Then explain the observed `one`, `five`, `three`, `four`, `two` order using synchronous execution, microtask enqueue order, and a later timer task.

Next use the chapter's bounded 200 ms slow click handler in `app.js`. Record a performance trace while activating the button once. Observe whether the intermediate “Working…” value is presented and locate the handler's execution. Run the bounded microtask-chain example separately if you want to compare its order with a timer.

**Verify:** identify the callback order and the approximate interval occupied by the slow handler. Explain why a DOM change need not be painted before the next statement, and why neither a Promise nor `async` automatically moves computation off the main thread. A trace need not expose every compositor event to support those observations.

## Stage 4 — Compare rendering work

Create a few hundred noninteractive list items containing ordinary text. Record a width change, restore the initial state, and record a transform. These produce different visual effects; compare work categories rather than declaring one an equivalent faster implementation.

Now compare the chapter's interleaved write/read loop with its batched alternative. Reset all rows to the same starting width before each run. Keep row count, viewport, and recording conditions unchanged, and exclude setup/reset work from the measured interval where possible.

**Verify:** report JavaScript, style, layout, and paint work where the profiler exposes it. State whether repeated layout was visible and whether batching changed it. If the difference is too small or the trace too coarse to interpret, report that limit. Do not infer universal speed, a fixed frame rate, or zero layout from one run.

## What to submit

For each core comparison, include one row in this evidence table:

| Change | Prediction | Observed evidence | Explanation | Limit or confounder |
| --- | --- | --- | --- | --- |
| Describe one controlled change | State the expected dependency or order | Record trace events, logs, or timings | Connect the evidence to the chapter | Note caching, tool limits, or unexplained variation |

Also include the setup conditions and a diagram connecting discovery, parsing, scripts, DOM, style/layout, presentation, and later input. Distinguish required dependencies from timing that may vary. Explain one observation that differed from your initial expectation.

Completion means you can justify the explanation from your evidence—not that every trace matches the chapter's conceptual diagrams.

## When an experiment gives an unexpected result

- **No new image request:** check the cache indication, URL, earlier references, and whether the delayed callback ran.
- **Module does not execute:** check Console and Network for path, MIME-type, or serving problems.
- **Every async run looks ordered:** vary resource timing if possible; observations do not create an execution-order guarantee.
- **No visible “Working…” state:** that is compatible with the handler preventing an intermediate presentation, not proof the assignment failed.
- **No layout difference:** verify that the initial width differs from the target, rows exist, and setup was excluded. Keep a null result if the evidence does not justify a stronger claim.

## Optional extension — A fixed-height virtual list

After completing the observation work, compare a full list with a version that renders a visible window plus a small buffer. Use fixed-height rows first. Document the dataset, viewport, row count in the DOM, and how scroll position maps to the rendered range.

Check the first and last items, resizing, fast scrolling, and preservation of item order and scroll extent. If rows become interactive, explain what happens when a focused row would leave the rendered range. Evaluate keyboard use and the information available to assistive technologies; rendering fewer nodes alone does not prove accessibility or a performance improvement.

Measure before and after using the same interaction and conditions. Keep this extension optional even if the full list is already fast. Continue with [Chapter 15]({{< relref "/book/Chapter_15_Core_Web_Vitals_and_Performance_Engineering.md" >}}) and [Practical 15]({{< relref "/playground/practical-15-measured-virtualized-performance.md" >}}) for deeper profiling. Variable-height measurement, `ResizeObserver`, and scroll anchoring belong to a later extension because they introduce additional geometry and state-management problems.

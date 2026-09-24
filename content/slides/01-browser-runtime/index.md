---
title: "The Modern Web Platform & Browser Internals"
description: "Chapter 1: follow a page from resource discovery to rendering and interaction, then test the model in DevTools."
book_number: "1"
weight: 2
---

# The Modern Web Platform & Browser Internals

From the first HTML bytes to the next interaction

**Chapter 1 · Modern Front-End Engineering**

Polla Fattah

---

## The files loaded. Why does the page still feel slow?

A catalogue heading appears before its image.

Clicking **Load products** appears to do nothing—then everything changes together.

What would you inspect first: the requests, the handler, or the rendering work?

---

## What we will explain

- How the browser discovers resources.
- Why downloading and executing a script are different events.
- How document state becomes a frame.
- Why synchronous code, microtasks, and timers behave differently.
- What evidence DevTools can—and cannot—provide.

---

## One small page

```html
<link rel="stylesheet" href="styles.css">
<script src="legacy.js"></script>
<script defer src="app.js"></script>
```

```html
<h1>Products</h1>
<button id="load-products">Load products</button>
<p id="status" role="status"></p>
<img src="hero.webp" alt="Featured products"
     width="800" height="400">
<ul id="products"></ul>
```

Use the full document in the chapter for the practical.

---

## A browser provides more than a JavaScript engine

The engine executes language code.

The browser also provides networking, the DOM, events, timers, storage, and rendering.

Work can happen concurrently, but ordinary page JavaScript and much rendering work compete for main-thread time.

---

## Navigation has setup costs

For `https://shop.example.com/products?page=2`:

1. Resolve the destination if necessary.
2. Establish or reuse a connection.
3. Request the document.
4. Begin processing available HTML.

Caches and restored pages can change this path. A small resource on a new origin may still incur setup cost.

---

## Parsing and downloading overlap

```text
HTML bytes arrive → parsing begins
                          ↓
                 stylesheet discovered → request
                          ↓
                 more markup arrives → continue
```

The browser does not generally wait for the complete HTML before discovering other resources.

The arrows show dependencies, not measured durations.

---

## Discovery can be the delay

```html
<img src="hero.webp" alt="Featured products">
```

versus a URL assigned only when JavaScript runs:

```js
const image = new Image();
image.src = "hero.webp";
```

Unless another reference reveals it earlier, the second request depends on script execution. Assigning `src` can start the request before insertion into the DOM.

---

## A stylesheet can hide another dependency

```text
HTML → stylesheet → needed background image
```

The browser needs the CSS before discovering the image through that rule.

Discovery, resource use, and request scheduling are different steps. A declared font that is never used need not be downloaded.

---

## Speculative discovery can look ahead

A preload scanner may inspect available markup while the main parser waits for a script.

It can find a later image or script reference.

It cannot execute arbitrary JavaScript to discover its future results or inspect bytes that have not arrived.

Do not assume a universal browser thread arrangement.

---

## Resource hints have different jobs

| Hint | Purpose |
| --- | --- |
| Preload | Fetch a current-page resource earlier |
| Prefetch | Speculate about likely future use |
| Preconnect | Begin connection setup |

A hint does not make bandwidth unlimited. Measure whether it addresses an actual delay.

---

## Source HTML is not the live DOM

```js
document.querySelector("#status").textContent = "Loaded";
```

The DOM changes; the original response does not.

**Demonstration:** compare the document response in Network with the status paragraph in Elements/Inspector.

---

## Classic scripts can stop the parser

Place this in `legacy.js` in the head:

```js
console.log(Boolean(document.querySelector("h1")));
```

The heading has not been parsed: `false`.

Move the script after the heading: it can find the node.

**Node availability does not prove that it has painted.**

---

## Choose script timing

For external scripts declared in the initial HTML:

| Mode | Main execution condition |
| --- | --- |
| Classic | Parser waits at the script |
| Defer | After parsing; ordered with deferred classic scripts |
| Async | When ready; document order not guaranteed |
| Module | Deferred by default; dependency graph applies |

`async` does not mean execution on a background thread.

---

## CSS can delay a script too

```html
<link rel="stylesheet" href="styles.css">
<script src="legacy.js"></script>
```

A previously encountered stylesheet can block this script.

The parser is waiting for the script, so CSS can indirectly prolong the pause.

CSS blocking presentation and a script blocking parsing are different dependencies.

---

## Readiness is not responsiveness

- `DOMContentLoaded`: parsing and relevant deferred script processing have progressed to this milestone.
- Window `load`: additional load-delaying resources have completed.
- Neither guarantees a particular paint time or fast future interactions.

Module experiments here omit imports and top-level `await` to keep the comparison focused.

---

## From state to a frame

```text
DOM + stylesheet information
              ↓
      Style calculation
              ↓
           Layout
              ↓
    Paint and raster work
              ↓
         Compositing
```

An update may reuse work or skip stages. This is a conceptual model, not an engine's thread diagram.

---

## Width and transform do different things

```js
list.style.width = "320px";
list.style.transform = "translateX(20px)";
```

Width can change wrapping and neighboring geometry.

A transform changes visual placement without reallocating normal-flow space.

Some transforms can reuse painted content. That is not a universal performance guarantee.

---

## A read can force layout

```js
for (const row of rows) {
  row.style.width = "300px";
  widths.push(row.getBoundingClientRect().width);
}
```

Compare with writing all widths first, then reading them.

Reset the starting state. Batching may reduce repeated layout; the first read can still require it.

---

## Predict the output

```js
console.log("start");
setTimeout(() => console.log("timeout"), 0);
Promise.resolve().then(() => console.log("promise"));
console.log("end");
```

Write your prediction before running it.

---

## Explain the output

```text
start
end
promise
timeout
```

Synchronous work finishes first. The already-fulfilled Promise's reaction runs at a microtask checkpoint before the timer task.

This is not a claim that all asynchronous operations finish before timers.

---

## A task is not followed by a guaranteed paint

```text
Selected task → microtask checkpoint → scheduling continues
                                            ↓
                       rendering when opportunity and scheduling permit
```

`requestAnimationFrame()` schedules a callback for a rendering update, not an after-paint notification.

An expensive callback remains expensive.

---

## Why might “Working…” never appear?

Inside the click handler:

```js
status.textContent = "Working…";
const start = performance.now();
while (performance.now() - start < 200) {
  // Bounded demonstration only.
}
status.textContent = "Finished";
```

Both DOM changes occur. The intermediate state may never reach the screen.

---

## Microtasks are not background work

A microtask can queue another microtask.

The checkpoint keeps processing them, delaying later tasks if the chain grows.

Use the bounded chain in the chapter. Do not freeze the page with an endless loop.

Moving expensive work into a Promise callback does not make it free.

---

## DevTools demonstration: discovery

1. Serve the chapter's small page over local HTTP.
2. Record browser, cache, and throttling settings.
3. Capture the image request from initial markup.
4. Remove that reference; assign the same URL after a timer.
5. Compare initiators and request start times in separate runs.

Explain differences; do not expect identical millisecond values.

---

## DevTools demonstration: execution and rendering

1. Record a click on the bounded slow handler.
2. Locate its execution in a performance trace.
3. Compare the DOM update with the visible result.
4. Reset the page before comparing layout experiments.

A breakpoint changes timing. A console log proves execution, not paint.

---

## Evidence before optimization

| Observation | Next question |
| --- | --- |
| Image request starts late | What revealed its URL? |
| Click response is delayed | What occupied the main thread? |
| Layout repeats | Are writes and geometry reads interleaved? |
| Trace looks different | Did cache, viewport, or throttling change? |

An unexplained trace is a reason to investigate, not to invent a guaranteed sequence.

---

## Practical 01

Produce predictions, comparable observations, and an explanation of one surprise.

The core exercise covers discovery, script timing, scheduling, and rendering work.

Fixed-height virtualization is optional; deeper profiling belongs with Chapter 15.

[Open the practical]({{< relref "/playground/practical-01-browser-observation-and-virtual-scroller.md" >}})

---

## Check your understanding

- Why can a downloaded script still be waiting?
- What does finding a DOM node tell you about paint?
- Why does a zero-delay timer run later?
- Which evidence would distinguish loading delay from execution cost?

---

## Next: what should the document mean?

Browser behavior explains how a page runs.

Chapter 2 examines how semantic structure, accessible controls, language, and direction describe the interface people use.

[Read Chapter 1]({{< relref "/book/Chapter_01_The_Modern_Web_Platform_and_Browser_Internals.md" >}}) · [Read Chapter 2]({{< relref "/book/Chapter_02_Semantic_HTML_Accessibility_Internationalization_and_the_DOM.md" >}})

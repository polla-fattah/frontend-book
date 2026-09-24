---
title: "Accessible Multilingual Interface and Composite Controls"
weight: 2
---

# Practical 02 — Accessible Multilingual Interface and Composite Controls

Related: [Chapter 2]({{< relref "/book/Chapter_02_Semantic_HTML_Accessibility_Internationalization_and_the_DOM.md" >}}) · [Lecture slides]({{< relref "/slides/02-semantic-html-accessibility-dom/index.md" >}})

## Objective

Build a resilient, fully accessible public-service portal that demonstrates the platform relationship between semantic HTML, the accessibility tree, internationalization, and live DOM event handling. 

You will establish a native selection baseline first using standard HTML controls, prove that the interface is completely operable via keyboard with explicit labeling and validation, handle mixed English and Kurdish/Arabic directional text, and implement delegated DOM events. As an optional extension, you will implement an accessible composite widget (a custom multi-select listbox) with roving `tabindex`.

## Prerequisites and setup

You need basic HTML, CSS, JavaScript, and a browser with developer and accessibility inspection tools (e.g. Chrome/Firefox Accessibility Tree inspection panel). Serve the exercise locally using any local static HTTP server (e.g., `python -m http.server 8000` or `npx serve .`):

Create this folder structure:

```text
chapter-02-semantics/
├── index.html
├── styles.css
└── app.js
```

Ensure your stylesheet includes a distinct, high-contrast `:focus-visible` outline. Keep third-party UI libraries or CSS frameworks out of the project; all behaviors and styles must be native.

## Stage 1 — Establish semantic landmarks and native selection baseline

Construct the core portal page containing:
* A `<header>` with site title and a `<nav aria-label="Primary">` containing navigation links.
* A single `<main>` landmark with a logical heading structure (`<h1>` $\rightarrow$ `<h2>`).
* A service request form using native interactive controls:
  * A native `<select id="service-type" name="service" required>` dropdown with options for different certificate requests.
  * A `<fieldset>` with a `<legend>` containing radio buttons for submission urgency (Standard vs Express).
  * A `<button type="submit">` element.
* A recent-requests `<table>` with a `<caption>`, explicit header scopes (`<th scope="col">` and `<th scope="row">`), and sample rows.
* A `<footer>` containing organizational metadata.

**Verify:** Disable CSS in your browser. Verify that the document outline, landmarks, form controls, and table data remain immediately understandable and navigable.

## Stage 2 — Programmatic labeling, keyboard operability, and error association

Enhance the form with comprehensive accessibility associations:
* Ensure every control has an explicit `<label for="...">` matching the input's `id`.
* Add a multiline `<textarea id="notes" name="notes" required>` for applicant statements.
* Configure explicit error association: add a dedicated `<p id="notes-error" role="alert" hidden></p>` element.
* Connect the error container to the input via `aria-describedby="notes-error notes-hint"`.
* In `app.js`, intercept form submission. If the textarea is empty, mark `aria-invalid="true"`, populate the error text, unhide the container, and programmatically move focus to the invalid field.

**Verify:** Navigate the entire page using only the `Tab`, `Shift+Tab`, `Space`, and `Enter` keys. Confirm that:
1. Every control receives a visible focus indicator.
2. No interactive element requires a mouse to activate.
3. Form validation errors are programmatically announced by screen-reader tools when triggered.

## Stage 3 — Multilingual content, directionality, and event delegation

Introduce internationalization and live DOM manipulation:
* Declare the primary document language on `<html>` (`lang="en" dir="ltr"`).
* On the notes field, configure `dir="auto"` so citizen statements written in Central Kurdish (`ckb`) or Arabic (`ar`) automatically align right-to-left.
* In the recent requests table, render multilingual rows. Use `<bdi>` to isolate user-submitted RTL statements so they do not scramble adjacent reference codes or punctuation.
* In `app.js`, implement a dynamic row addition feature upon form submission. Use safe DOM methods (`document.createElement`, `textContent`, `append`) rather than raw `innerHTML`.
* Add an action button (`<button type="button" data-action="cancel">`) to each table row. Instead of attaching a listener to every button, attach one listener to the `<tbody>` element and use `event.target.closest('button[data-action="cancel"]')` to handle cancellations via event bubbling.
* Expose dynamic updates to assistive devices using a live region (`role="status"` and `aria-live="polite"`).

**Verify:** Add an entry containing Arabic or Kurdish text alongside English IDs. Confirm that text direction is properly isolated and that clicking dynamic buttons triggers the delegated handler correctly.

## Stage 4 (Optional Extension) — Composite multi-select listbox

Only after completing Stages 1–3, evaluate whether a custom widget is justified. Build an enhanced multi-select listbox:
1. Create a container with `role="listbox"`, `aria-multiselectable="true"`, and `aria-label="Available services"`.
2. Inside, render child options with `role="option"` and `aria-selected="false"`.
3. Implement **roving `tabindex`**:
   * The currently focused option has `tabindex="0"`; all other options have `tabindex="-1"`.
   * Pressing `DownArrow` or `UpArrow` moves focus and updates `tabindex="0"` to the next or previous option without scrolling the page.
   * `Home` moves focus to the first option; `End` moves to the last option.
   * `Space` toggles the selection state (`aria-selected="true|false"`).
4. Preserve the native `<select multiple>` as a fallback.

**Verify:** Inspect the accessibility tree in DevTools. Verify that the custom listbox exposes correct roles, options, and selection states, and that navigating via `Tab` treats the listbox as a single tab stop.

## What to submit

Document your implementation by submitting the completed project files (`index.html`, `styles.css`, `app.js`) and filling out this verification table:

| Verification Target | Requirement | Observed Evidence | Explanation | Confounders or Limits |
| :--- | :--- | :--- | :--- | :--- |
| **Document Hierarchy** | Logical `h1`-`h2` structure and landmarks | Accessibility tree snapshot | Document outline exposes clean landmarks | Checked in Chrome/Firefox DevTools |
| **Keyboard Navigation** | 100% operable without mouse; visible focus | Tab progression sequence | `:focus-visible` styling provides clear indicator | Verified with keyboard only |
| **Form Validation** | Error announced via `aria-describedby` | Accessibility tree inspection | `aria-invalid="true"` set upon empty submit | Browser native validation disabled for test |
| **Internationalization** | `<bdi>` isolates mixed LTR/RTL content | Visual alignment test | Text punctuation remains intact across scripts | Tested with Central Kurdish / Arabic input |
| **Event Delegation** | Single listener handles dynamic rows | Console event logs | `event.target.closest()` captures row action | Event bubbling through `<tbody>` |

## When an experiment gives an unexpected result

* **No focus ring visible:** Verify that your CSS does not contain `outline: none` without a matching `:focus-visible` declaration.
* **Screen reader does not announce validation error:** Check that the error container has `role="alert"` or `aria-live="assertive"`, and that `aria-describedby` matches the error element's exact `id`.
* **RTL text scrambles adjacent numbers:** Confirm that the user string is wrapped inside `<bdi>` or has `dir="auto"`.
* **Delegated click listener does not fire:** Check whether `event.target.closest(...)` selector matches the button, and ensure the event is allowed to bubble (i.e. `stopPropagation()` was not called on a child element).

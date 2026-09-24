---
title: "Intrinsic, Container-Aware Dashboard"
weight: 3
---

# Practical 03 — Intrinsic, Container-Aware Dashboard

Related: [Chapter 3]({{< relref "/book/Chapter_03_Modern_CSS_Architecture_and_Layout_Systems.md" >}}) · [Lecture slides]({{< relref "/slides/03-modern-css-architecture-layout/index.md" >}})

## Objective

Build a resilient, responsive executive dashboard that demonstrates CSS as an architectural system. You will implement an explicit cascade layer stack, establish a 3-tier design token hierarchy, construct an adaptive 2D Grid shell with Subgrid card alignment, and implement container queries that allow components to adapt to their immediate container space rather than relying exclusively on viewport media queries.

Finally, you will verify that the interface seamlessly supports bidirectional internationalization (`ltr` $\leftrightarrow$ `rtl`), accommodates extreme text variations without overflow, and functions reliably under 200% browser zoom without JavaScript resize listeners.

## Prerequisites and setup

You need an HTML editor, a modern browser with Developer Tools (supporting CSS Grid, Subgrid, and Container Queries), and a local HTTP server.

Create your project workspace:

```text
chapter-03-dashboard/
├── index.html
└── styles.css
```

Do not install CSS frameworks (such as Tailwind or Bootstrap) or JavaScript layout libraries. All layout, adaptation, and layer boundaries must be constructed using native CSS.

## Stage 1 — Architectural cascade layers and 3-tier design tokens

Establish a predictable precedence hierarchy and design token system in `styles.css`:

1. Declare your cascade layer stack at the very top of the stylesheet:
   ```css
   @layer reset, tokens, base, layout, components, utilities;
   ```
2. In `@layer tokens`, construct a 3-tier token hierarchy using CSS custom properties:
   * **Tier 1 (Raw Foundation):** Primitive color palettes, spacing units, and radius values (e.g. `--blue-600: #005a9c;`, `--space-4: 1rem;`).
   * **Tier 2 (Semantic Context):** Meaning-based tokens mapped to raw values (e.g. `--color-primary: var(--blue-600);`, `--color-surface: #ffffff;`, `--space-card-padding: var(--space-4);`).
   * **Tier 3 (Component-Scoped):** Component-specific parameters that can be overridden locally (e.g. `--card-border-color: var(--color-border);`).
3. Add dark-mode theme adaptation via `prefers-color-scheme: dark` by updating semantic tokens at the `:root` level.
4. In `@layer reset`, apply universal `box-sizing: border-box`, remove default margins, and ensure media elements have `max-inline-size: 100%`.

**Verify:** Inspect the styles in browser DevTools. Confirm that layers are recognized in the Styles pane and that modifying a single semantic token (such as `--color-primary`) updates all consuming components across the interface.

## Stage 2 — 2D Grid layout and card alignment with Subgrid

Build the page architecture and product catalog in `index.html`:

1. Structure the layout shell using CSS Grid with named areas:
   * `header` spanning the top row.
   * `sidebar` on the inline-start side (`minmax(14rem, 18rem)`).
   * `main` occupying remaining space (`1fr`).
   * At small viewport widths (under `48rem`), collapse the grid into a single vertical column.
2. In the main catalog section, construct a responsive card grid using auto-placement:
   ```css
   .card-grid {
     display: grid;
     grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr));
     grid-auto-rows: auto 1fr auto;
     gap: var(--space-md);
   }
   ```
3. Populate three sample cards with intentionally unequal content:
   * Card 1: Single-line title, one-sentence description.
   * Card 2: Three-line title, four-sentence detailed description.
   * Card 3: Two-line title, two-sentence description.
4. Apply **Subgrid** to each card (`grid-row: span 3; grid-template-rows: subgrid;`) so that card titles share Row 1, descriptions share Row 2, and action buttons snap to Row 3 along a shared horizontal baseline.

**Verify:** Inspect the cards visually and with DevTools Grid overlay. Confirm that despite varying description lengths, all card action buttons remain strictly aligned across each grid row without hardcoded element heights.

## Stage 3 — Container queries and fluid sizing

Make components context-aware rather than screen-aware:

1. Configure the sidebar container as a queryable container:
   ```css
   .app-sidebar {
     container-type: inline-size;
     container-name: sidebar-context;
   }
   ```
2. Build a summary metric card (`.stat-card`). Place one instance of this card inside the main content area and a second instance inside the narrow sidebar.
3. Use a container query to adapt the card's layout:
   * When container width is under `260px`, render the metric and label in a stacked vertical layout with compact typography.
   * When container width exceeds `260px`, render the metric and label horizontally with expanded spacing.
4. Replace rigid heading font sizes with fluid typography using `clamp()`:
   ```css
   h1 {
     font-size: clamp(1.5rem, 1.2rem + 1.5vw, 2.5rem);
   }
   ```

**Verify:** Resize the browser window and drag the sidebar boundary. Confirm that the card in the sidebar switches layout based on the sidebar's width, while the card in the main area remains in its expanded layout.

## Stage 4 — Logical properties, bidirectional layout, and stress testing

Ensure internationalization resilience and edge-case durability:

1. Audit `styles.css` to verify that no physical coordinates (`margin-left`, `padding-right`, `left`, `right`) are used. Replace all instances with logical equivalents (`margin-inline-start`, `padding-inline-end`, `inset-inline-start`).
2. Add a language/direction toggle button (or manually set `<html lang="ckb" dir="rtl">`):
   * Confirm that the sidebar automatically flips to the right side.
   * Confirm that navigation links, card padding, and button icons flip orientation without writing a single `[dir="rtl"]` override rule.
3. **Stress Tests:**
   * **Unbroken String:** Insert a 45-character unbroken alphanumeric reference code (e.g. `DOC-REQ-7894239847293847293847293847298374928374`) into a card title. Verify that `overflow-wrap: break-word;` prevents horizontal layout blow-out.
   * **Browser Zoom:** Zoom the browser viewport to 200%. Verify that navigation and cards stack gracefully without overlapping text or clipping content.

## What to submit

Submit your `index.html` and `styles.css` along with a completed verification report:

| Target | Requirement | Observed Evidence | Explanation | Confounders or Limits |
| :--- | :--- | :--- | :--- | :--- |
| **Cascade Layers** | Explicit precedence across `@layer` stack | DevTools Layers inspection | Utility rules override component styles; layer order verified | Inspected in Chrome/Firefox |
| **Subgrid Alignment** | Cards align titles, text, and buttons | Grid overlay screenshot | All card buttons share identical row datum | Browser must support CSS Subgrid |
| **Container Queries** | Component adapts to sidebar vs main area | Sidebar width test | Card switches layout at 260px container boundary | Verified independently of viewport |
| **Logical Properties** | Zero physical directional overrides | RTL toggle test (`dir="rtl"`) | Sidebar, card paddings, and alignment flip automatically | Checked with Central Kurdish / Arabic |
| **Edge-Case Resilience** | 200% zoom and unbroken strings | Zoom & long-string test | No horizontal scrollbars; text wraps cleanly | Tested under extreme text length |

## When an experiment gives an unexpected result

* **Subgrid does not align children:** Ensure the parent grid has explicit rows (e.g. `grid-auto-rows: auto 1fr auto;`) and that each child card declares `grid-row: span 3; grid-template-rows: subgrid;`.
* **Container query does not fire:** Check that `container-type: inline-size;` is applied to an ancestor container of the component, and that the query references the correct container name.
* **Component overflows its grid column:** Ensure that grid tracks use `minmax(min(100%, 16rem), 1fr)` or that child containers have `min-inline-size: 0;` to prevent min-content blowout.
* **RTL layout fails to mirror margins:** Check whether legacy physical properties (`margin-left` or `margin-right`) were accidentally used instead of `margin-inline-start` and `margin-inline-end`.

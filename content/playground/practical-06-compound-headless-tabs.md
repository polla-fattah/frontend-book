# Practical 06 — Compound Headless Tabs

Related chapter: Chapter 6

## Objective

Build a composable tabs system that separates keyboard behavior and state ownership from styling and content layout.

## Stages

1. Define the responsibility of the root, tab list, tab, and panel.
2. Implement controlled and uncontrolled selection.
3. Add correct `role`, `aria-selected`, `aria-controls`, and `tabindex` behavior.
4. Test arrow-key navigation, disabled tabs, and dynamic panels.
5. Compare explicit props, context/provide-inject, and a headless API.

## Verification

- The selected tab and visible panel remain synchronized.
- Keyboard behavior is independently testable.
- Styling is not imposed by the component logic.
- The API avoids invalid combinations and boolean-prop explosion.

## Extension

Add lazy panel loading and document the loading, error, and retry states.


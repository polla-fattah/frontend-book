# Practical 02 — Accessible Composite Listbox

Related chapter: Chapter 2

## Objective

Build an optional multi-select listbox after first implementing the same selection task with native controls.

## Stages

1. Build a native `<select multiple>` baseline.
2. Document why the custom widget is justified.
3. Implement the listbox role, options, accessible name, selection state, and roving `tabindex`.
4. Add keyboard navigation, typeahead, disabled options, and multi-selection.
5. Test with keyboard interaction and accessibility inspection.

## Verification

- Only the intended composite item is in the tab sequence.
- Arrow keys, Home/End, typeahead, and selection behavior are documented.
- The widget has a stable accessible name and state announcements.
- The native baseline remains available as the simpler alternative.

## Extension

Add virtualization only after proving that the unvirtualized widget has a measured problem.


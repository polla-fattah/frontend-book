# Book-Wide Audit Report

Date: 2026-09-23

Scope: manuscript Markdown files, supporting proposal/specification documents, and the editorial requirements in `prompt.txt`.

## Executive assessment

The manuscript has a strong and deliberate architecture-first shape, and the existing chapters consistently include teaching, review, practical work, terminology, and a closing perspective. The initial scan found an incomplete file inventory, but Chapters 14 and 15 have now been added. The remaining repository-level blocker is the absence of visible Git metadata.

1. No visible `.git` metadata is present in the workspace, so Git-history preservation and diff-based review cannot currently be performed here.

The chapter-completeness issue is resolved. The earlier cross-references should now be checked against the newly present chapters.

### Update after initial scan

Chapters 14 and 15 are present and correctly titled:

- Chapter 14 — 4,516 lines, 209 headings, 27 Mermaid blocks.
- Chapter 15 — 4,629 lines, 204 headings, 13 Mermaid blocks.

The chapter sequence is now complete from Chapter 1 through Chapter 18.

## Inventory

The declared structure contains 18 chapters and three appendices. The workspace currently contains:

| Area | Expected | Present |
|---|---:|---:|
| Chapters | 18 | 18 |
| Appendices | 3 | 3 |
| Chapter files missing | — | none |

Present chapter files are `chapter01.md` through `chapter18.md`. The appendices are present.

The manuscript files have balanced Markdown code fences in the initial mechanical check. Mermaid blocks are present throughout the manuscript, so diagram syntax and conceptual duplication require a later dedicated pass rather than removal or blanket normalization.

## Priority findings

### Resolved — Missing Chapters 14 and 15

The initial scan reported this as the primary structural blocker. The files have since been added, and their titles match the declared structure and specifications.

The missing chapters are referenced from existing content, including:

- Chapter 1: performance profiling and optimization targets.
- Chapters 3 and 4: image optimization and memory behavior.
- Chapter 6: design systems and performance measurement.
- Chapters 8, 11, and 12: organizational architecture, rendering performance, and bundle analysis.
- Chapters 13, 16, 17, and 18: micro-frontends, testing, RUM, and architectural decisions.

The previously identified cross-references can now be checked against the actual content of Chapters 14 and 15. They should not be treated as broken references by default.

### P0 — Git review workflow unavailable

`git status` reports that the workspace is not a Git repository, and no `.git` directory is visible at the workspace root. This conflicts with the manuscript safety requirement to preserve originals in Git history and inspect diffs after edits.

Recommended action: restore or expose the repository metadata before making substantive edits. Until then, limit changes to reports and explicitly approved standalone files.

### P1 — Extreme section-granularity variation

The chapters intentionally vary in depth, which is compatible with the editorial brief. However, the current top-level section counts range from 7 in Chapter 1 to 199 in Chapter 18. Several later chapters use a very large number of short numbered sections.

This is not a reason to mechanically reduce headings. It is a review flag for navigation cost, repeated explanations, and whether each heading adds a distinct layer of understanding. Chapter 18 is the first candidate for this focused review, followed by Chapters 16 and 17.

### P1 — Repeated end-of-chapter scaffolding

All present chapters contain the same broad end sequence: misconceptions, summary, review questions, practical lab, key terms, and closing perspective.

This can be pedagogically useful and should not be removed automatically. The audit should instead check whether each instance is chapter-specific, whether the practical lab matches the chapter’s depth level, and whether repeated prose is adding new understanding.

### P1 — Appendix B contains chapter-level material

Appendix B includes sections titled “Chapter 14 — Scale” and “Chapter 15 — Performance” near its end. These may be intentional cross-reference material or remnants of an earlier structure. They should be compared with the newly present chapters before any appendix edits are attempted. Appendix C is now the production deployment checklist, with guided implementation work maintained separately under `practicals/`.

## Initial consistency observations

- Chapter titles match the declared structure for all files that are present.
- Existing chapters generally follow the standards-first and architecture-first philosophy.
- The manuscript repeatedly distinguishes platform responsibilities from framework expressions, which aligns with the brief.
- Cross-references to Chapters 14 and 15 now require content-level validation rather than missing-file remediation.
- No unbalanced fenced code blocks were found in the initial scan.
- Mermaid is used extensively; it should be validated for syntax, naming, direction, and unnecessary duplication in a separate pass.
- The workspace contains no standalone Mermaid files or test/build configuration that could be used for automated manuscript validation.

## Technical verification queue

The following topics require authoritative, current-source verification before changing claims. They are not marked as errors merely because they are present in the prompt’s risk list:

- Chapter 1: preload/speculative resource discovery and browser scheduling.
- Chapter 3: cascade-layer ordering, including `!important` reversal.
- Chapter 5: runtime validation versus TypeScript assertions and branded types.
- Chapter 7: React and Vue rendering/reactivity distinctions, and effect/watcher guidance.
- Chapter 9: `fetch()` behavior for HTTP error statuses and cache-layer distinctions.
- Chapter 10: Background Sync, `navigator.onLine`, and Cache API distinctions.
- Chapter 11: SSR, hydration, streaming, Server Components, resumability, and edge placement.
- Chapter 12: current build-pipeline and Vite/Rolldown claims.
- Chapter 13: CORS, cookies/OAuth, CSP, and cross-origin isolation.
- Chapter 15: current Core Web Vitals definitions and thresholds.
- Chapter 16: semantic testing queries, test IDs, selector guidance, and accessibility limits.
- Chapter 17: browser observability maturity and feature-flag boundaries.
- Chapter 18: contextual decision-making without framework or architecture rankings.

## Recommended staged plan

### Stage 0 — Resolve repository and manuscript completeness

1. Restore or expose Git metadata.
2. Confirm Chapters 14 and 15 against `book-proposal.md` and `Detailed Chapter Specifications.md`.

### Stage 1 — Structural audit

1. Validate chapter order, titles, cross-references, and appendix placement.
2. Check heading hierarchy, code fences, Mermaid blocks, tables, and internal links.
3. Review section granularity without imposing equal chapter length.

### Stage 2 — Technical accuracy audit

Review the technical verification queue using first-party or standards sources. Record sources in a separate review log rather than adding unrequested URLs to manuscript prose.

### Stage 3 — Editorial consistency audit

Check recurring principles, framework balance, depth-level appropriateness, accessibility, internationalization, security, performance, progressive enhancement, runtime validation, and error/recovery treatment.

### Stage 4 — Controlled editing

Edit one chapter or issue family at a time. Preserve intentional repetition, inspect every diff, and keep a change log.

### Stage 5 — Final quality pass

Re-run structural checks, validate Mermaid diagrams, inspect internal references, review all current technical claims, and confirm that the final book structure is complete.

## Immediate next step

Proceed with the completed 18-chapter structural and technical audit. The remaining repository limitation is the absence of visible Git metadata; manuscript edits should remain paused until that limitation is resolved or explicitly accepted.

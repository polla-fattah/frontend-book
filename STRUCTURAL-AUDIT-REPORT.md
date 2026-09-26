# Structural Audit Report

Date: 2026-09-23

Scope: all 18 chapter files, three appendices, and the proposal/specification documents.

## Result

The manuscript file inventory is complete. Chapters 1-18 are present, chapter titles match the declared book structure, and Appendices A-C are present.

The mechanical checks found no unbalanced fenced code blocks and no duplicate exact Markdown headings within individual files. No references to chapters outside Chapters 1-18 were found.

## Checks passed

- Chapter sequence: `chapter01.md` through `chapter18.md`.
- Chapter titles: match the titles in `book-proposal.md` and `Detailed Chapter Specifications.md`.
- Code fences: balanced in every chapter and appendix.
- Exact duplicate headings: none found within individual files.
- Out-of-range chapter references: none found.
- Missing standalone chapter files: none.

Chapter 14 and Chapter 15 are now included in the structural inventory:

- Chapter 14: 4,516 lines, 209 headings, 27 Mermaid blocks.
- Chapter 15: 4,629 lines, 204 headings, 13 Mermaid blocks.

## Findings requiring editorial review

### S1 - Heading hierarchy jumps

There are 60 cases where an `H3` heading follows an `H1` heading without an intervening `H2`. Examples include:

- `chapters/chapter01.md:2023`
- `chapters/chapter08.md:1032`
- `chapters/chapter14.md:365`
- `chapters/chapter18.md:177`

These are commonly compact subtopics such as “Path parameter” or “Raw/foundation tokens” under a numbered `H1` section. They may be intentional, but they create a formal heading-hierarchy jump for screen readers and document navigation.

Recommendation: review this as a focused heading pass. Prefer `##` for direct subsections, or introduce an intermediate `##` only when the conceptual structure genuinely has an intermediate level. Do not mechanically change all instances.

### S1 - Chapter 18 section granularity

Chapter 18 contains 199 numbered top-level sections, compared with 7 in Chapter 1 and 204 total headings. Chapters 16 and 17 also contain unusually high section counts.

This does not violate the book’s variable-depth principle, but it creates a navigation and editorial-risk hotspot. Review whether neighboring micro-sections add distinct understanding, especially in repeated decision checklists, examples, and end-of-chapter material.

### S2 - Repeated end-of-chapter structure

All 18 chapters contain the same broad closing components: misconceptions, summary, review questions, practical lab, key terms, and closing perspective.

This is compatible with a teaching-oriented book. The next pass should check whether each component is specific to its chapter and whether repetition reinforces a principle or merely repeats prose.

### S2 - Appendix B chapter index and chapter-level sections

Appendix B contains a long chapter index near its end, including entries for Chapters 1-18, as well as chapter-specific references earlier in the appendix. This may be intentional, but it should be checked for duplicated content and navigation value.

Appendix C is a separate production deployment checklist. Its implementation-oriented labs are maintained in the companion `practicals/` directory rather than embedded in the appendix.

### S2 - Template placeholder in Chapter 18

`chapters/chapter18.md:3764` contains `ADR-XXX: Decision Title`. This is likely an intentional template example, but the final manuscript should make the placeholder status explicit or replace it with a clearly labeled generic example.

## Mermaid and diagrams

Mermaid blocks are used extensively across the manuscript. The structural scan confirmed that fenced blocks are balanced, but it did not parse Mermaid syntax. A later diagram-specific pass should validate:

- syntax accepted by the intended renderer;
- consistent node and concept naming;
- diagram direction and readability;
- duplicate diagrams that do not add a new view;
- accessibility of surrounding explanatory text.

## Internal navigation

The manuscript does not currently use Markdown links to other `.md` files. Cross-chapter navigation is expressed in prose, which avoids broken file links but makes automated link validation impossible. Chapter-reference scanning found references only within the declared 1-18 range.

## Recommended next stage

1. Review the 60 heading-hierarchy cases and classify intentional versus incorrect nesting.
2. Review Chapter 18, then Chapters 16-17, for navigation cost and unnecessary micro-sectioning.
3. Check Appendix B’s chapter index against the final book navigation plan.
4. Validate Mermaid syntax and conceptual duplication.
5. Begin the technical accuracy pass using current authoritative sources.

No manuscript chapter was modified during this audit.

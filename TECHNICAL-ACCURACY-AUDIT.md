# Technical Accuracy Audit

Date: 2026-09-23

Scope: high-risk technical areas identified in `prompt.txt`, reviewed against the current manuscript and authoritative sources. This is a review report; no manuscript chapters were modified.

## Implementation update

The recommended targeted clarifications have been applied:

- Chapter 9 now uses “application/query cache” and distinguishes it from the deprecated Application Cache API.
- Chapter 10 now distinguishes `Cache`, `CacheStorage`, and the umbrella term Cache API.
- Chapter 12 now qualifies Rolldown statements as Vite 8 implementation details.
- Chapter 13 now uses more precise COEP/CORS/CORP wording.
- Chapter 13 now states the current PKCE requirement for browser-based public clients, with a provider-compatibility caveat.
- Chapter 15’s current-metrics qualifier remains in place.

The edited chapters were re-scanned afterward; their fenced code blocks remain balanced.

## Overall result

The first verification pass found no critical factual error in the sampled high-risk material. The manuscript already reflects most of the required corrections from `prompt.txt`, including:

- cautious treatment of speculative resource discovery;
- correct cascade-layer ordering and `!important` reversal;
- runtime validation versus TypeScript assertions;
- distinct React and Vue reactivity models;
- `fetch()` behavior for HTTP error responses;
- distinct HTTP, query/application, and browser persistence caches;
- separation of SSR, streaming, Server Components, and resumability;
- CORS distinct from authentication and authorization;
- current Core Web Vitals metrics and thresholds;
- semantic testing queries without an absolute CSS-selector ban;
- feature flags distinct from authorization;
- cautious treatment of browser OpenTelemetry support.

## Confirmed areas

### Chapter 1 - speculative resource discovery

The text explicitly avoids claiming that a preload scanner is always a separate thread and correctly limits the claim to possible discovery of available markup. It also states that JavaScript-created and CSS-buried resources may be discovered later. No change is required from this pass.

### Chapter 3 - cascade layers

The manuscript correctly states that, within the relevant author-origin context:

- normal layered declarations are ordered by layer order;
- unlayered normal author styles outrank layered normal styles;
- `!important` reverses layer order;
- earlier important layers outrank later important layers;
- layered important declarations outrank unlayered important declarations.

This matches [MDN’s cascade-layer guidance](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Cascade_layers) and [MDN’s `!important` reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/important).

### Chapter 5 - TypeScript assertions and runtime validation

The examples correctly explain that `as User` changes compile-time interpretation, is erased by compilation, and does not inspect or validate runtime data. This matches the [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html).

The treatment of branded types as an advanced pattern is appropriate.

### Chapter 7 - React and Vue

The chapter correctly distinguishes React Effects, refs, and memoization from Vue’s computed values and watchers. It also correctly teaches that Effects/watchers are not the default mechanism for ordinary derivation.

React’s current documentation describes `useEffect` as synchronization with external systems, `useRef` as storage that does not trigger re-rendering, and `useMemo` as a performance optimization rather than a semantic guarantee: [useEffect](https://react.dev/reference/react/useEffect), [useRef](https://react.dev/reference/react/useRef), [useMemo](https://react.dev/reference/react/useMemo). Vue’s documentation similarly distinguishes computed derivation from watchers: [Vue watchers](https://vuejs.org/guide/essentials/watchers).

### Chapter 9 - Fetch and HTTP status handling

The manuscript correctly states that `fetch()` fulfills with a `Response` for HTTP statuses such as 404 or 500 and rejects for conditions such as network failure. This matches [MDN’s Fetch documentation](https://developer.mozilla.org/en-US/docs/Web/API/Window/fetch).

### Chapter 10 - offline and background capabilities

The manuscript correctly treats Background Sync as an enhancement, not a foundation, and correctly warns that `navigator.onLine` is only an indication of network connectivity. [MDN documents Background Sync as limited availability](https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API) and warns that the `online` event does not prove a particular website is reachable](https://developer.mozilla.org/en-US/docs/Web/API/Window/online_event).

### Chapter 11 - rendering topologies

The chapter correctly separates:

- SSR from Server Components;
- streaming from total-work elimination;
- hydration from resumability;
- edge placement from a fundamentally new rendering topology.

No critical correction was identified in this pass.

### Chapter 13 - security boundaries

The chapter correctly distinguishes CORS from authentication and authorization, identifies OAuth as primarily delegated authorization, treats OpenID Connect as adding identity/authentication semantics, and presents PKCE and exact redirect URI validation as modern browser-flow concerns.

The current OAuth security baseline is [RFC 9700](https://www.rfc-editor.org/info/rfc9700), which recommends PKCE for public clients and requires authorization servers to support it. The newer browser-based application guidance is [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017.html).

### Chapter 15 - Core Web Vitals

The chapter’s current set and “good” thresholds are correct:

| Metric | Good threshold |
|---|---:|
| LCP | ≤ 2.5 s |
| INP | ≤ 200 ms |
| CLS | ≤ 0.1 |

The manuscript also correctly identifies field data, p75 evaluation, lab diagnostics, and Lighthouse as distinct concepts. These points align with [web.dev’s Core Web Vitals threshold guidance](https://web.dev/articles/defining-core-web-vitals-thresholds) and [field/lab measurement guidance](https://web.dev/articles/vitals-measurement-getting-started).

### Chapter 16 - testing and accessibility

The chapter correctly presents accessible names as a web accessibility concept rather than a Testing Library invention. It also correctly treats role/name queries as useful but insufficient proof of accessibility, allows test IDs as fallbacks, and avoids banning CSS selectors absolutely.

This aligns with the W3C material on [accessible names and descriptions](https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/) and [Accessible Name and Description Computation](https://www.w3.org/WAI/news/2018-12-18/accessible-name-and-description-computation-accname-is-a-w3c-recommendation/).

### Chapter 17 - OpenTelemetry and feature flags

The chapter’s caution is accurate. The official OpenTelemetry JavaScript documentation currently labels browser client instrumentation as experimental and mostly unspecified: [OpenTelemetry JavaScript](https://opentelemetry.io/docs/languages/js/) and [browser guidance](https://opentelemetry.io/docs/languages/js/getting-started/browser/).

The text also correctly states that browser-delivered feature flags are visible to users and cannot serve as authorization enforcement.

## Clarifications recommended

### T1 - Chapter 9: avoid “Application Cache” ambiguity

Locations: `chapters/chapter09.md:1814`, `chapters/chapter09.md:4024`.

The explanatory text itself says “application-level query cache” and “application/server-state cache,” which is good. However, the heading “Browser HTTP Cache vs Application Cache” and glossary term “Application cache” can be confused with the deprecated browser Application Cache API.

Recommendation: use **application/query cache** or **application-level server-state cache** consistently. Reserve **Application Cache API** for historical discussion of the deprecated platform feature, if it is mentioned at all.

### T1 - Chapter 10: distinguish `Cache`, `CacheStorage`, and “Cache API” more precisely

Locations: `chapters/chapter10.md:1385`, `chapters/chapter10.md:3685`.

The statement that Cache API storage represents Request/Response pairs is conceptually correct. The platform terminology is more precise when it distinguishes the `Cache` interface, which stores request/response pairs, from `CacheStorage`, which manages named caches. [MDN’s CacheStorage reference](https://developer.mozilla.org/en-US/docs/Web/API/CacheStorage) and [Cache reference](https://developer.mozilla.org/en-US/docs/Web/API/Cache) support this distinction.

Recommendation: revise the first introduction to say “The Cache interface stores Request/Response pairs; CacheStorage manages named Cache objects.” Keep the broader educational term “Cache API” as an umbrella only after defining these interfaces.

### T1 - Chapter 12: qualify Vite 8/Rolldown claims

Locations: `chapters/chapter12.md:799-815`, `chapters/chapter12.md:1429`.

The claims are current as of the audit date: Vite 8 uses Rolldown as its unified Rust-based bundler. This is confirmed by [the Vite 8 announcement](https://vite.dev/blog/announcing-vite8) and [the Vite migration guide](https://vite.dev/guide/migration).

Because build-tool details are time-sensitive, keep the durable architecture explanation first and qualify implementation-specific wording with “Vite 8” or “in the current Vite 8 toolchain.” Avoid wording that implies all historical or future Vite versions share the same internals.

### T1 - Chapter 13: refine the COEP diagram and wording

Locations: `chapters/chapter13.md:2448-2509`.

The prose says a strong COEP policy may require compatible CORS or CORP, which is directionally correct. The diagram text “Embedded Resources Need Compatible CORS/CORP” can be read as requiring both mechanisms for every resource. In practice, CORS-mode requests are governed by CORS, while `no-cors` resources may need CORP under `COEP: require-corp`; `credentialless` changes the conditions. See [MDN COEP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy) and [MDN CORP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cross-Origin_Resource_Policy).

Recommendation: change the diagram label to something such as “Cross-origin resources must satisfy the applicable CORS/CORP conditions.”

### T2 - Chapter 13: strengthen OAuth wording

Locations: `chapters/chapter13.md:1882-1885`.

“Modern OAuth security guidance strongly favors PKCE” is safe but less precise than current guidance. For browser-based public clients, current best practice is stronger: PKCE is required, and authorization servers must support it under RFC 9700/RFC 10017.

Recommendation: state the requirement with deployment scope: “Browser-based public clients should use the Authorization Code flow with PKCE; current OAuth security guidance requires PKCE for public clients.” Preserve caveats for legacy providers and interoperability.

### T2 - Chapter 15: preserve the current-metrics qualifier

Locations: `chapters/chapter15.md:159-175`, `chapters/chapter15.md:3588-3612`.

The content is accurate now. Retain “current” and the audit date in the review log because Core Web Vitals definitions and thresholds are time-sensitive. The manuscript appropriately avoids treating Lighthouse as the performance objective.

## No-change conclusions

The following areas were specifically checked and currently need no corrective edit based on the sampled claims:

- Chapter 1’s preload-scanner caution.
- Chapter 3’s cascade-layer ordering.
- Chapter 5’s runtime-validation model.
- Chapter 7’s React/Vue distinction.
- Chapter 9’s `fetch()` status behavior.
- Chapter 11’s SSR/streaming/RSC/resumability distinctions.
- Chapter 16’s testing-query guidance.
- Chapter 17’s browser OpenTelemetry caution.
- Chapter 18’s trade-off-driven architecture framing.

## Recommended editing order

1. Apply the four T1 clarifications: Chapter 9 terminology, Chapter 10 Cache interfaces, Chapter 12 Vite qualification, and Chapter 13 COEP wording.
2. Apply the two T2 precision improvements for OAuth and the current-metrics review note.
3. Re-run the targeted claim scans.
4. Continue with a second technical pass for lower-risk chapters and code-example plausibility.

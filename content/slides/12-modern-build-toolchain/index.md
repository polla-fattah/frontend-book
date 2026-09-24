---
title: "Modern Build Systems, Development Tooling & Team Workflows"
description: "Chapter 12: understand module graphs, transformation, bundling, code splitting, environment boundaries, and reproducible team workflows."
book_number: "12"
weight: 13
---

# Modern Build Systems, Development Tooling & Team Workflows

Understand the path from source to delivery

**Chapter 12**

Polla Fattah

---

## Today's goal

Make the front-end toolchain visible as an architecture rather than a collection of commands.

We will connect:

- package management, lockfiles, scripts, and modules;
- resolution, transformation, development servers, and HMR;
- production bundling, tree shaking, minification, and source maps;
- asset fingerprints, CSS, environment variables, and code splitting;
- Vite, Rollup, esbuild, Rolldown, and Turbopack;
- linting, formatting, type checking, testing, Git, and CI;
- workspaces, monorepos, package boundaries, and dependency direction;
- an inspectable, reproducible build workflow.

---

## By the end of today you can

- explain why development and production optimize differently;
- read a module graph and identify dependency direction;
- distinguish resolution, transformation, bundling, and serving;
- understand what tree shaking can and cannot remove;
- choose code-splitting boundaries based on route behavior;
- keep build-time configuration separate from runtime secrets;
- design fast local feedback and shared CI verification;
- use workspaces without confusing them with architecture;
- expose package APIs without leaking private files;
- inspect emitted assets instead of guessing about performance.

---

## The central principle

> **A build toolchain is a delivery architecture: it transforms source modules into environment-specific artifacts while preserving reproducibility, boundaries, and useful feedback.**

The tool is not only a compiler.

It resolves dependencies, serves development code, creates production artifacts, and shapes how teams work.

---

## The source-to-delivery pipeline

```text
source files
  → package resolution
  → module graph
  → transformation
  → development server or production bundle
  → assets and maps
  → deployment
```

Each stage answers a different question and has different failure modes.

---

## Development and production optimize differently

```text
development → fast startup, fast updates, useful diagnostics
production   → small transfer, stable caching, optimized execution
```

A development server is not automatically a production server.

The two modes can share configuration while serving different goals.

---

## Package management is the beginning of the toolchain

Packages define:

- source dependencies;
- executable scripts;
- development tools;
- transitive dependency graphs;
- version constraints;
- reproducible installation inputs.

The package manifest is an architectural document, not only an install list.

---

## Runtime and development dependencies

```text
runtime dependency   → needed by the shipped application
development dependency → needed to build, test, lint, or develop
```

Misclassifying a dependency can:

- inflate production output;
- break a library consumer;
- make a production build depend on local tooling;
- hide a missing runtime requirement.

---

## Semantic version ranges are constraints

```json
{
  "dependencies": {
    "library": "^3.2.0"
  }
}
```

The range describes acceptable versions.

The lockfile records the concrete resolution used by an installation.

Do not confuse the manifest promise with the installed graph.

---

## Lockfiles belong in application repositories

A lockfile records:

- concrete versions;
- resolved locations;
- integrity information;
- transitive dependency choices.

It lets local development, CI, and deployment start from the same dependency graph.

Update it intentionally and use one package manager consistently.

---

## Package scripts create a common interface

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc --noEmit && vite build",
    "lint": "eslint .",
    "test": "vitest run"
  }
}
```

Scripts hide machine-specific command details and give the team a shared workflow vocabulary.

---

## ES modules are the structural foundation

```ts
import { formatPrice } from "./price";
export function renderProduct(product: Product) {
  return formatPrice(product.priceCents);
}
```

Static module syntax gives tools information about dependencies, exports, and boundaries.

---

## Static imports are analyzable

```ts
import { loadProducts } from "./api";
```

The tool can use static imports to:

- build a dependency graph;
- detect missing modules;
- identify unused exports;
- split and optimize code;
- pre-bundle dependencies.

---

## Dynamic imports create asynchronous boundaries

```ts
const reports = await import("./reports");
```

Dynamic imports can create:

- lazy routes;
- optional features;
- smaller initial chunks;
- delayed dependency loading.

They also add loading, error, caching, and prefetch decisions.

---

## CommonJS still exists

```js
const packageValue = require("package");
module.exports = packageValue;
```

Interoperability can affect:

- static analysis;
- default exports;
- tree shaking;
- runtime loading;
- package conditions.

Know the module format at the boundary you are integrating.

---

## Module resolution answers “which file?”

Resolution may consider:

- relative paths;
- package exports;
- file extensions;
- aliases;
- conditions for browser, node, import, or require;
- workspace links;
- type declarations.

The module graph begins only after resolution succeeds.

---

## Aliases can improve architecture—or hide it

```ts
import { Button } from "@shared/ui/Button";
```

Aliases can make stable package boundaries readable.

They can also conceal deep dependencies and make imports appear more independent than they are.

Use aliases to communicate architecture, not to avoid designing it.

---

## Transformation is not one operation

```text
source syntax → parse → transform → emit browser-compatible code
```

Transformation may include:

- TypeScript syntax removal;
- JSX transformation;
- language lowering;
- macro or plugin transforms;
- CSS processing;
- asset URL rewriting.

---

## TypeScript compilation has separate jobs

```text
type checking    → verify static relationships
transformation   → produce executable JavaScript
```

A fast transpiler can remove types without proving the program correct.

Run type checking as its own explicit quality step when the build tool does not perform it.

---

## Transpilation and polyfills are different

Transpilation can rewrite syntax:

```text
new syntax → older syntax
```

It does not automatically provide missing runtime APIs such as a browser feature.

Polyfills, browser targets, and runtime support are separate decisions.

---

## Development servers optimize feedback

A development server may provide:

- native module serving;
- on-demand transformation;
- dependency pre-bundling;
- source maps;
- error overlays;
- HMR or Fast Refresh.

It should make the smallest useful update quickly and explain failures clearly.

---

## Hot Module Replacement

```text
edit source
  → tool transforms changed module
  → browser receives update
  → runtime replaces or refreshes behavior
```

HMR shortens feedback loops, but it is not identical to a fresh application start.

---

## Fast Refresh is framework-aware HMR

Framework-aware refresh can preserve component state when a change is safe.

It may reset state when:

- module exports change shape;
- boundaries are not refresh-safe;
- initialization semantics change;
- the framework cannot preserve identity.

Test both preserved and reset behavior when it matters.

---

## HMR correctness matters

Hot updates can expose bugs hidden by full reloads:

- duplicate subscriptions;
- stale module state;
- missing cleanup;
- side effects at import time;
- global registration repeated on every update.

Write initialization and cleanup so reload behavior remains predictable.

---

## Vite as a reference development tool

Vite's development model emphasizes:

- fast startup;
- native ESM-like module requests;
- on-demand transforms;
- dependency pre-bundling;
- a separate production build pipeline.

The exact internals can evolve; the development versus production distinction remains useful.

---

## Dependency pre-bundling

Third-party packages may contain many modules or formats that are expensive to request individually.

Pre-bundling can:

- reduce browser request count;
- normalize dependency formats;
- improve development startup after caching.

It does not mean the production bundle and development graph are identical.

---

## Native ESM is an important mental model

```text
browser requests module A
  → A imports B
  → browser requests B
```

Development tools can preserve a module-oriented model while adding transforms, caching, and dependency optimization.

Do not assume that a development request corresponds one-to-one with a production asset.

---

## Production bundling is graph transformation

```text
many source modules
  → chunks with shared dependencies
  → optimized assets
```

Bundling includes:

- module combination;
- dependency ordering;
- tree shaking;
- code splitting;
- asset rewriting;
- minification;
- source-map generation.

It is much more than concatenation.

---

## Tree shaking removes unreachable exports

```ts
export function used() {}
export function unused() {}
```

If the graph and package semantics allow it, the unused export may be removed from a production chunk.

The tool needs analyzable module structure and correct side-effect information.

---

## Tree shaking depends on analyzable code

Dynamic behavior can limit removal:

- unpredictable property access;
- CommonJS patterns;
- runtime module discovery;
- side effects hidden in imports;
- package metadata that is too broad.

The tool can only prove what the code structure makes visible.

---

## Side effects matter

```ts
import "./register-global";
```

An import may be valuable even when it has no exported binding.

Do not mark a package as side-effect-free unless removing such imports is safe.

---

## Minification changes representation

Minification can:

- shorten identifiers;
- remove whitespace;
- simplify expressions;
- eliminate unreachable code;
- compress repeated structures.

It improves transfer and sometimes execution, but it makes debugging harder without source maps.

---

## Source maps connect artifacts to source

```text
browser error in chunk.js
  → source map
  → original TypeScript / component file
```

Source maps are an operational policy:

- public or private?
- uploaded to an error service?
- exposed in production?
- retained for which release?

---

## Asset fingerprinting enables safe caching

```text
app.js → app.8f31c.js
```

Content-based names let immutable assets use long cache lifetimes.

HTML or manifests must point to the current fingerprinted files.

---

## Code splitting creates delivery choices

```text
initial route chunk
  → lazy reports chunk
  → shared dependency chunk
```

Split points affect:

- initial transfer;
- later navigation latency;
- cache reuse;
- request count;
- failure and loading behavior.

---

## Route-level splitting is often a strong default

```ts
const ReportsPage = lazy(() => import("./reports/ReportsPage"));
```

Routes usually represent meaningful user journeys and can isolate code that is not needed initially.

They also provide a natural loading and error boundary.

---

## More chunks are not always better

Tiny chunks can create:

- request overhead;
- scheduling complexity;
- waterfall risk;
- poor cache reuse;
- difficult debugging.

Split around behavior and navigation, not every file.

---

## Shared chunks are a trade-off

Shared dependencies can be downloaded once and reused.

But a large shared chunk can become part of every route's initial cost even when only one feature uses it.

Analyze the actual graph and route traffic.

---

## Preloading and prefetching split code

```text
preload  → needed soon for the current route
prefetch → likely needed later when resources allow
```

Use hints based on confident navigation and device/network conditions.

Prefetching code the user never needs is still work.

---

## CSS participates in the build pipeline

The pipeline may:

- process imports;
- scope or extract styles;
- rewrite asset URLs;
- split CSS by entry or route;
- minify output;
- preserve source maps.

CSS loading order and extraction affect rendering and layout stability.

---

## Asset imports are module dependencies

```ts
import logoUrl from "./logo.svg";
import styles from "./Card.module.css";
```

The tool can fingerprint assets, generate URLs, and include only resources reachable from the graph.

The runtime receives a reference appropriate to the target environment.

---

## Environment variables have a boundary

```text
build-time configuration → embedded or replaced during build
runtime configuration     → read by the deployed environment
```

Browser-exposed variables are public.

`.env` naming does not make a value secret once it is included in client output.

---

## Build-time and runtime configuration differ

Build-time values require rebuilding to change.

Runtime values can vary per deployment or request without producing new assets.

Choose based on:

- environment portability;
- caching;
- deployment frequency;
- secrecy;
- per-request variation.

---

## Vite production builds

A production build typically performs:

- module resolution;
- transformation;
- dependency graph optimization;
- code splitting;
- asset fingerprinting;
- minification;
- source-map output according to policy.

Inspect the generated result instead of inferring it from development requests.

---

## Rollup

Rollup is a graph-oriented bundler known for:

- ES module analysis;
- library and application bundling;
- tree shaking;
- plugin-based transformation;
- controllable output formats.

Use it directly when its lower-level control matches the responsibility you need.

---

## esbuild

esbuild emphasizes very fast native transformation and bundling.

It can be useful for:

- fast development transforms;
- custom build integration;
- straightforward application builds;
- tooling that needs quick parsing and emission.

Fast transformation does not remove the need for application architecture or type checking.

---

## Rolldown and Turbopack

Modern tools evolve their internals to improve:

- incremental builds;
- graph computation;
- parallelism;
- native performance;
- framework integration.

Learn the responsibility each tool solves instead of treating its implementation name as the architecture.

---

## Vite and Turbopack solve related problems differently

```text
development graph and feedback
production graph and output
framework-specific incremental integration
```

Tools can differ in when they bundle, how they cache, and how they integrate with a framework.

The stable mental model is the source graph and emitted responsibility.

---

## The framework often chooses the tool

Framework defaults can determine:

- development server;
- route build model;
- server/client boundaries;
- asset handling;
- production output;
- plugin lifecycle.

Developers still need to understand the underlying responsibilities when diagnosing output or performance.

---

## Plugins extend the pipeline

Plugins may add:

- syntax transforms;
- virtual modules;
- asset handling;
- route generation;
- environment integration;
- development middleware.

Every plugin adds behavior to resolution, transformation, or output. Keep plugin purpose and order understandable.

---

## Avoid toolchain configuration as a hobby

Configuration should answer a delivery or developer-experience need.

Before adding a plugin or custom transform, ask:

- which problem does it solve?
- who owns it?
- what does it change in production?
- how is it tested?
- what is the fallback if it breaks?

Complexity without a user or team benefit is a liability.

---

## Linting catches a class of problems

Linting can detect:

- suspicious patterns;
- unused bindings;
- import restrictions;
- unsafe APIs;
- inconsistent architectural rules.

It is not formatting, type checking, or a substitute for tests.

---

## Formatting reduces diff noise

A formatter creates a shared representation so reviews focus on behavior and design.

Format consistently and avoid repeatedly reformatting unrelated files in feature commits.

Formatting should support review, not dominate it.

---

## Type checking verifies static contracts

```text
lint       → suspicious patterns
format     → stable representation
typecheck  → static relationships
test       → observed behavior
build      → delivery graph and artifacts
```

These gates overlap in value but do not answer the same question.

---

## Local feedback should be fast

```text
edit → immediate editor feedback
    → local targeted check
    → pre-commit / pre-push gate
    → CI full verification
```

Fast feedback catches cheap mistakes close to the change.

CI provides a shared clean-environment check.

---

## Git is part of the engineering toolchain

Git supports:

- reviewable change boundaries;
- reproducible history;
- rollback;
- release traceability;
- collaboration across branches.

Treat commit and merge practices as part of delivery quality.

---

## Keep commits reviewable

Prefer commits that separate:

- mechanical formatting;
- dependency updates;
- tool configuration;
- feature behavior;
- generated artifacts.

Small coherent changes make toolchain failures easier to bisect and understand.

---

## Generated files need a policy

Decide which artifacts are:

- committed;
- generated in CI;
- published separately;
- reproducible from source;
- ignored locally.

Inconsistent policies create noisy diffs and uncertain releases.

---

## Environment reproducibility

Reproducibility depends on:

- lockfile;
- package-manager version;
- Node/runtime version;
- build configuration;
- environment inputs;
- operating-system assumptions;
- clean install behavior.

Document and automate the parts that affect artifacts.

---

## CI is the shared verification environment

CI should run from a clean state and verify the contracts that matter:

```text
install → lint → typecheck → test → build → artifact checks
```

The exact order can vary, but the environment should not depend on one developer's machine.

---

## Build once, deploy predictably

```text
source + locked dependencies + config
  → one verified artifact
  → promote the artifact across environments
```

Rebuilding separately for each environment can produce different output and weaken release confidence.

Keep truly runtime-varying configuration outside immutable assets where possible.

---

## Workspaces solve package coordination

Workspaces can:

- install multiple packages together;
- link internal packages;
- share scripts and dependency policy;
- coordinate builds;
- make local package changes visible quickly.

They are a package-management feature, not automatically a monorepo architecture.

---

## A workspace is not automatically a monorepo architecture

```text
workspace → repository/package coordination mechanism
monorepo  → repository organized around multiple related projects/packages
```

A workspace can host one application plus tools.

A monorepo still needs package boundaries, ownership, and dependency direction.

---

## Monorepo benefits

Potential benefits include:

- shared code with local changes;
- coordinated releases;
- consistent tooling;
- cross-package refactors;
- shared CI infrastructure.

The benefits appear only when boundaries and workflows remain understandable.

---

## Monorepo costs

Costs include:

- larger dependency graph;
- longer or more complex CI;
- ownership ambiguity;
- cross-package build ordering;
- accidental coupling;
- difficult versioning decisions.

Do not choose a monorepo solely because it is fashionable.

---

## Package boundaries should represent architecture

```text
packages/ui        reusable visual behavior
packages/domain    shared domain contracts
apps/storefront    product application
apps/admin         internal application
```

The directory is useful when it reflects a responsibility and public API.

---

## Internal packages need public APIs too

```ts
import { Button } from "@workspace/ui";
```

Prefer an intentional package entry point over:

```ts
import { Button } from "@workspace/ui/src/components/Button";
```

Private file imports bypass encapsulation and make internal restructuring expensive.

---

## Dependency direction matters

```text
app → feature → domain → shared
```

Lower-level packages should not import higher-level application decisions.

Direction makes ownership and reuse possible.

---

## Circular dependencies are design feedback

```text
A → B → C → A
```

Even if the build succeeds, cycles can create:

- partial initialization;
- undefined exports;
- confusing evaluation order;
- difficult testing;
- architecture that cannot be layered cleanly.

Break the cycle by clarifying ownership or extracting a stable lower-level contract.

---

## Analyze the dependency graph

Look for:

- unexpected large imports;
- application code imported by shared packages;
- cycles;
- duplicate versions;
- route chunks containing unrelated features;
- a dependency that dominates initial transfer.

The graph turns performance and architecture discussions into evidence.

---

## Development and production differ

```text
development → source modules, overlays, HMR, readable maps
production   → optimized chunks, fingerprints, minification, deployment paths
```

Always run a production build before making claims about production artifacts.

---

## `dev` is not a production server

Development servers may:

- transform on demand;
- tolerate missing optimizations;
- expose source files;
- use different caching;
- allow permissive CORS or proxies;
- rely on local filesystem behavior.

Use a production build and production-like serving environment for delivery verification.

---

## Build targets define browser assumptions

Targets influence:

- syntax transformation;
- polyfill decisions;
- output size;
- supported APIs;
- debugging expectations.

Choose a browser policy deliberately and keep it visible to the team.

---

## Baseline and browser policy

A supported-browser policy should answer:

- which browsers and versions are supported;
- which features are assumed;
- when a feature needs a fallback;
- how support changes are reviewed;
- how real devices are tested.

The build cannot invent a product support policy.

---

## Library builds versus application builds

```text
application → optimize one deployed experience
library     → preserve a reusable public API and externalize peers
```

Library output needs stable formats, declarations, exports, and consumer compatibility.

Application output can make more assumptions about its deployment.

---

## Dependency externalization

Libraries may leave dependencies external so consumers provide them.

This avoids duplicating framework code but creates peer-version and runtime compatibility obligations.

Decide which code belongs in the library artifact and which belongs to the consuming application.

---

## Tree shaking and package design

Packages are easier to optimize when they:

- use analyzable ES modules;
- expose focused entry points;
- avoid import-time side effects;
- declare side-effect behavior accurately;
- avoid pulling a whole framework for one helper.

Package API design directly affects emitted application code.

---

## Development proxying

A development proxy can route browser requests to an API and reduce local cross-origin friction.

It should not hide production differences in:

- origin;
- cookies;
- headers;
- HTTPS;
- path rewriting;
- error behavior.

Document what the proxy changes.

---

## HTTPS in development

HTTPS may be required to reproduce:

- secure cookies;
- service workers;
- browser APIs requiring a secure context;
- mixed-content behavior;
- realistic origin policy.

Use a consistent local certificate workflow when the application depends on these capabilities.

---

## Environment parity

Compare development and production for:

- origin and base path;
- asset URLs;
- API proxying;
- environment variables;
- compression;
- source maps;
- service-worker behavior;
- caching headers.

Parity is a debugging tool, not a demand that every environment be identical.

---

## Team tooling should be boring

Good tooling is:

- documented;
- reproducible;
- fast enough to use;
- hard to misconfigure;
- easy to upgrade deliberately;
- understandable by the whole team.

The goal is dependable delivery, not admiration for configuration cleverness.

---

## Avoid global tool dependencies

Prefer project-local versions for:

- bundlers;
- formatters;
- linters;
- test runners;
- type tooling;
- code generators.

Global tools can silently differ from CI and another developer's environment.

---

## Editor integration is developer experience

Editor support can provide:

- type feedback;
- import navigation;
- formatting;
- lint diagnostics;
- test discovery;
- refactoring support.

The editor should use the repository's configuration rather than a parallel personal toolchain.

---

## Pre-commit hooks are a feedback boundary

Use hooks for fast checks that should block obviously broken commits.

Keep them bounded.

Long full builds in every commit encourage bypassing the hook; put broad verification in CI.

---

## Dependency updates need policy

For updates, consider:

- security advisories;
- lockfile changes;
- peer compatibility;
- bundle impact;
- behavior changes;
- migration notes;
- rollback path.

Toolchain dependencies can change emitted artifacts even when application code is unchanged.

---

## Toolchain dependencies have supply-chain risk

Build tools execute code in a privileged development and CI context.

Reduce risk with:

- lockfiles and review;
- trusted registries;
- minimal dependencies;
- update monitoring;
- restricted CI credentials;
- artifact inspection.

The toolchain is part of the application's attack surface.

---

## A reference workflow

```text
edit
  → editor feedback
  → targeted test / lint
  → reviewable commit
  → CI clean install
  → typecheck + test + production build
  → inspect artifacts
  → deploy immutable output
```

Each stage should add confidence without repeating every earlier cost.

---

## Practical project structure

```text
app/
  src/
  public/
  package.json
  tsconfig.json
  vite.config.ts
  eslint.config.js
  lockfile
```

The exact files vary.

The important point is that source, configuration, scripts, and lockfile form one reproducible project boundary.

---

## Build pipeline for the storefront

```text
resolve imports
  → transform TypeScript and JSX
  → split routes
  → tree shake
  → minify
  → fingerprint assets
  → emit maps and manifest
```

Trace a source module through this pipeline to understand what the browser receives.

---

## Lazy loading reports

```ts
const ReportsRoute = () => import("./reports/ReportsRoute");
```

The reports route should not appear in the initial chunk when the build and route architecture permit splitting.

Verify with emitted assets and a network trace rather than trusting the source syntax alone.

---

## Inspect the build instead of guessing

Useful evidence includes:

- asset sizes;
- chunk composition;
- duplicate dependencies;
- source-map module lists;
- route request waterfalls;
- cache headers;
- compressed transfer sizes.

Build analysis is most useful when connected to a user journey.

---

## Toolchain smells

Watch for:

- build configuration nobody understands;
- every project using different lint rules;
- lockfiles regenerated by multiple managers;
- production builds rarely run;
- huge initial bundles despite route structure;
- hundreds of tiny chunks;
- secrets in front-end environment variables;
- internal package imports through private paths;
- circular dependencies everywhere.

---

## Choose tools by responsibility

```text
application dev server + build → high-level framework tool
specialized library output   → library bundler
fast transformation          → native transformer
multiple local packages      → workspace / monorepo tooling
framework-specific pipeline  → framework-integrated tool
```

Choose the smallest toolset that serves the responsibility.

---

## Current tooling changes; architecture remains

Tool internals evolve.

The stable questions remain:

- what is the module graph?
- where are transformation boundaries?
- what ships initially?
- what loads later?
- what is public configuration?
- how is output verified?
- who owns each package boundary?

---

## Practical lab: Inspect a Modern Front-End Toolchain

Use a modern build tool to observe resolution, transformation, module graphs, code splitting, and deployment artifacts.

The practical compares source modules with development requests and production output.

---

## Practical stages 1–4: create and inspect

1. Create a small TypeScript application.
2. Add a dynamically imported reports route.
3. Inspect development requests and production chunks.
4. Compare source modules with emitted assets and source maps.

Record which decisions belong to the toolchain and which belong to application architecture.

---

## Practical stages 5–9: build and split

5. Separate type checking.
6. Create a production build.
7. Explore tree shaking.
8. Explore minification.
9. Add route-level code splitting.

Verify that reports code is not in the initial route chunk when the build permits splitting.

---

## Practical stages 10–14: optimize and verify

10. Prefetch a lazy route.
11. Analyze a large dependency.
12. Add linting and formatting.
13. Add CI-style verification.
14. Compare build-time and runtime configuration.

Interpret bundle size alongside route behavior and field performance.

---

## Practical stages 15–18: boundaries and architecture

15. Explore package encapsulation.
16. Compare Vite and low-level bundler responsibilities.
17. Research Turbopack through a Next.js example.
18. Create a build architecture diagram.

Do not present a dependency-graph visualizer as a production bundler.

---

## Practical extension: educational graph visualizer

Build a deliberately limited visualizer showing:

```text
entry → imports → dynamic split point → emitted chunk
```

Label it educational.

The goal is to make resolution and dependency direction visible, not to recreate a production bundler.

---

## Try this yourself

Pick one initial route and answer:

- which source modules does it need?
- which dependency dominates its size?
- which feature can split at a route boundary?
- what can be tree-shaken?
- what must remain a side effect?
- which environment values are public?

Then verify every answer against the emitted build.

---

## Troubleshooting guide

| Symptom | Likely cause |
|---|---|
| Dev works, production fails | Different transforms, paths, or environment assumptions |
| Reports code is in the initial chunk | Import is static or split boundary is ineffective |
| Unused package code remains | Side effects, module format, or graph opacity |
| CI differs from local | Lockfile, runtime, or global tool mismatch |
| Secret appears in client output | Public build-time variable was treated as private |
| Package consumers import private files | Public API is incomplete or undocumented |
| HMR behaves strangely | Import-time side effects or cleanup missing |
| Tiny chunks hurt navigation | Split points follow files rather than user journeys |
| Build graph contains cycles | Dependency direction is unclear |

---

## Completion checklist

- [ ] package versions and lockfile are reproducible;
- [ ] resolution and module boundaries are understandable;
- [ ] type checking is an explicit quality step;
- [ ] development and production workflows are distinguished;
- [ ] code splitting follows route or feature behavior;
- [ ] tree-shaking assumptions are validated by output;
- [ ] source maps and environment values have policy;
- [ ] package APIs protect internal files;
- [ ] CI verifies a clean production build;
- [ ] emitted artifacts are inspected rather than guessed at.

---

## Misconceptions to leave behind

| Misconception | Better mental model |
|---|---|
| A build tool is just a compiler | It resolves, transforms, serves, bundles, and emits |
| Bundling means concatenation | It is graph transformation and asset design |
| TypeScript must emit JavaScript through `tsc` | Type checking and transformation can be separate |
| Transpilation adds missing browser APIs | Polyfills and runtime support are separate |
| More code splitting is always better | Split around user journeys and costs |
| Tree shaking removes anything not called | It depends on analyzable graphs and side effects |
| Minification makes source maps unnecessary | Debugging still needs source policy |
| `.env` values are secret | Client-exposed values are public |
| A workspace is a monorepo architecture | Coordination tooling and boundaries differ |
| A successful circular build is healthy | Cycles are dependency-design feedback |
| The dev server is production | Production artifacts and serving behavior differ |
| Quality gates are interchangeable | Lint, format, types, tests, and build answer different questions |

---

## The chapter in one sentence

> **Treat the toolchain as an inspectable delivery graph that transforms source into reproducible artifacts while preserving package, environment, and team boundaries.**

---

## Next: Chapter 13

The next chapter will build on tooling and architecture with:

- testing strategy and confidence boundaries;
- unit, integration, and end-to-end verification;
- browser behavior and accessibility tests;
- performance and failure testing;
- quality workflows for evolving applications.

---

## Questions

Can you trace one user-visible route from its source entry point to the emitted assets, and explain which toolchain decisions affect its first-load cost?

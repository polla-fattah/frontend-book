---
title: "Front-End Architecture & Technical Decision-Making"
description: "Chapter 18: make evidence-backed architecture decisions using quality attributes, constraints, boundaries, trade-offs, and reversible learning."
book_number: "18"
weight: 19
---

# Front-End Architecture & Technical Decision-Making

Choose deliberately, learn continuously

**Chapter 18**

Polla Fattah

---

## Today's goal

Turn architecture from a collection of technologies into a transparent set of decisions.

We will connect:

- requirements, quality attributes, constraints, and trade-offs;
- cohesion, coupling, dependency direction, and blast radius;
- complexity budgets, reversibility, locality, and explicit data flow;
- progressive enhancement, platform-first design, and dependency evaluation;
- fitness functions, ADRs, spikes, risk reduction, and failure modes;
- performance, security, accessibility, testing, observability, and deployability;
- team topology, governance, migration, and architecture outcomes.

---

## By the end of today you can

- define architecture as decisions made under constraints;
- distinguish functional requirements from quality attributes;
- compare alternatives without fake precision;
- reduce coupling and blast radius through boundaries;
- prefer reversible decisions when information is weak;
- use ADRs to record decisions and revisit triggers;
- turn important architecture rules into fitness functions;
- choose a proportionate architecture for different scenarios;
- design migration instead of assuming rewrites are cleaner;
- defend the smallest coherent solution with evidence.

---

## The central principle

> **Architecture is a set of explicit, contextual decisions about trade-offs, boundaries, and future change—not a technology stack or a prediction of everything that might happen.**

Good architecture makes important change cheaper, safer, and easier to reason about.

---

## The decision progression

```text
define problem
  → identify quality attributes
  → record constraints
  → generate alternatives
  → reduce unknowns
  → decide and document
  → enforce important properties
  → observe and revisit
```

Architecture remains a loop rather than a one-time ceremony.

---

## Architecture is a set of decisions

Examples:

```text
where state lives
where rendering happens
how APIs are shaped
what is shared
how failures are contained
how releases are delivered
```

The framework is one input to those decisions, not the decision itself.

---

## Not everything can be optimized at once

Trade-offs may exist between:

- autonomy and consistency;
- speed and flexibility;
- freshness and cacheability;
- simplicity and isolation;
- performance and feature richness;
- delivery independence and runtime coupling.

Architecture makes the trade-off visible so the team can choose intentionally.

---

## Maximum team autonomy has costs

Autonomy can increase:

- release speed;
- local decision quality;
- ownership;
- experimentation.

It can also increase:

- duplication;
- inconsistent behavior;
- platform cost;
- integration burden;
- fragmented user experience.

The goal is useful autonomy within coherent contracts.

---

## Quality attributes

Quality attributes describe how the system behaves:

```text
performance / reliability / security / accessibility
maintainability / deployability / observability / scalability
```

They are architecture inputs because they shape boundaries and decisions.

---

## Functional requirements versus quality attributes

```text
functional: users can submit an inspection
quality: submission remains safe under network failure
```

Functional requirements describe capability.

Quality attributes describe the conditions under which that capability remains useful.

---

## Not every quality attribute has equal priority

A government service may prioritize accessibility and reliability.

An internal analytics tool may prioritize iteration speed and data accuracy.

A marketing page may prioritize cacheability and loading performance.

Priorities should be explicit rather than assumed.

---

## Make quality attributes measurable

```text
fast        → p75 catalogue LCP target
reliable    → successful save ratio
accessible  → keyboard journey and audit criteria
deployable  → rollback within a defined window
```

An attribute becomes architectural guidance when the team can observe it.

---

## Constraints

Constraints can come from:

- budget;
- deadline;
- existing APIs;
- browser support;
- team skills;
- regulation;
- deployment platform;
- organization;
- data sensitivity.

Constraints are not annoyances to ignore; they define the decision space.

---

## Requirements, constraints, and decisions

```text
requirement → what must be achieved
constraint   → what limits the options
decision     → chosen response and trade-off
```

Confusing a preference with a constraint produces unnecessary architecture.

---

## Architecture is contextual

The same question can have different answers:

```text
WebSocket for collaboration → plausible
WebSocket for a static page → unnecessary
global store for a workflow → perhaps useful
global store for one modal → excessive
```

Context is part of correctness.

---

## Start with the problem, not the tool

Weak question:

```text
Should we use framework X?
```

Stronger question:

```text
How should a public, searchable, frequently updated catalogue render and recover?
```

The tool choice follows the problem model.

---

## Technology selection is downstream

```text
requirements + quality + constraints
  → boundaries and operating model
  → technology candidates
  → experiment and decision
```

Choosing a library before defining the need turns a decision into a justification exercise.

---

## Architecture decisions are often about boundaries

Decide where to place:

- state;
- trust;
- rendering;
- ownership;
- caching;
- deployment;
- failure;
- team responsibility.

Boundaries determine what can change independently.

---

## Good boundaries reduce change cost

```text
change in one boundary
  → small, predictable set of affected consumers
```

The boundary should expose a stable contract and keep volatile implementation private.

---

## Cohesion and coupling

```text
cohesion → things that belong together change together
coupling → one thing must know or change because of another
```

Good architecture seeks high cohesion inside meaningful units and intentional coupling between them.

---

## Cohesion example

```text
catalogue feature
  query state
  product query
  filtering
  catalogue UI
  catalogue tests
```

These concerns may belong together because they change around the same user capability.

---

## Coupling example

```text
ProductCard → entire global store → unrelated application services
```

The card now knows more than its responsibility requires.

Pass a product and an intent-oriented capability instead.

---

## Dependency direction

```text
application → feature → domain → shared foundation
```

Dependencies should flow toward stable, reusable concepts.

When a foundation imports application behavior, the architecture becomes difficult to reuse and change.

---

## Stable dependencies

Depend on:

- small interfaces;
- domain contracts;
- platform capabilities;
- stable shared primitives.

Avoid depending on:

- private files;
- temporary implementations;
- broad containers;
- undocumented framework internals.

Stable dependencies reduce future blast radius.

---

## Blast radius

Blast radius asks:

```text
If this changes or fails, what else is affected?
```

Reduce blast radius through:

- narrow APIs;
- isolated data and runtime boundaries;
- feature flags;
- fallback behavior;
- independent tests and deployment;
- clear ownership.

---

## Centralization versus local autonomy

Centralize when consistency, security, or shared lifecycle matters.

Keep local when:

- behavior is domain-specific;
- requirements differ;
- coordination cost exceeds reuse value;
- independent evolution is important.

The right location is a trade-off, not a moral position.

---

## The complexity budget

Every system spends complexity on:

- code;
- tools;
- runtime;
- deployment;
- operations;
- team coordination;
- cognitive load.

Spend complexity only where it buys a required quality attribute.

---

## Accidental versus essential complexity

```text
essential → required by the product or environment
accidental → introduced by our chosen solution
```

Architecture work should remove accidental complexity without pretending essential complexity can disappear.

---

## Complexity has several forms

```text
code complexity
runtime complexity
deployment complexity
organizational complexity
conceptual complexity
```

A “simpler” client architecture may move complexity into the server or CI system.

Count the whole system.

---

## Prefer reversible decisions

When information is weak, prefer choices that can be changed without rewriting the entire platform.

Examples:

- explicit adapter around a vendor;
- route-level boundary before full micro-frontends;
- local state before global store;
- package API before runtime federation.

Reversibility buys learning time.

---

## One-way and two-way doors

```text
two-way door → easy to reverse, decide quickly with bounded risk
one-way door  → costly or dangerous to reverse, investigate carefully
```

Do not apply heavyweight governance to every reversible choice.

Do not rush a decision that creates irreversible migration or data cost.

---

## Delay irreversible decisions when information is weak

Use:

- a spike;
- a prototype;
- a compatibility layer;
- a small route;
- a feature flag;
- an explicit revisit trigger.

Learning before commitment is architecture work.

---

## YAGNI does not mean ignore the future

Avoid building speculative systems for unknown requirements.

Do preserve:

- clear boundaries;
- migration paths;
- explicit ownership;
- replaceable dependencies;
- observable assumptions.

The future is supported by flexibility, not by implementing every possibility now.

---

## Premature abstraction

An abstraction created before variation is understood may encode the wrong concept.

Wait for evidence about:

- repeated behavior;
- stable vocabulary;
- change direction;
- real consumers;
- shared accessibility and lifecycle.

---

## The rule of three

One use may be local.

Two uses reveal similarity.

Three uses can provide enough evidence to decide whether the concept is genuinely shared.

It is a heuristic, not a command to duplicate exactly three times.

---

## Duplication can be cheaper than coupling

Small duplicated code may be safer than:

- a generic API with many modes;
- a shared release dependency;
- cross-domain assumptions;
- a package nobody can evolve.

Compare maintenance and change cost rather than counting lines.

---

## Locality

Locality keeps related code, data, tests, and ownership near each other.

It reduces:

- navigation cost;
- hidden dependencies;
- coordination overhead;
- accidental reuse.

Move code outward only when the new boundary creates real value.

---

## Explicit data flow

```text
source → transform → consumer
```

Explicit inputs, outputs, events, URLs, and requests are easier to test and change than invisible reads from global context.

---

## Hidden coupling

Hidden coupling appears through:

- global mutable state;
- import-time side effects;
- shared storage keys;
- undocumented events;
- CSS selectors across packages;
- framework-specific assumptions;
- environment variables used everywhere.

Make coupling visible or remove it.

---

## Global state is an architectural decision

Use global state when:

- lifetime is application-wide;
- consumers are genuinely distributed;
- synchronization is needed;
- ownership is explicit.

Do not use it to avoid passing one value through a well-defined local boundary.

---

## Server state is not ordinary client state

Server state has:

- remote authority;
- freshness;
- errors;
- caching;
- invalidation;
- concurrency.

Use a server-aware boundary rather than copying it into every client store.

---

## Derived state should remain derived

```text
products + query → visibleProducts
```

Store the inputs and calculate the result.

Duplicated derived state creates another source of truth and another synchronization path.

---

## URL as architecture

URL state provides:

- shareability;
- reload persistence;
- browser history;
- deep links;
- route ownership.

It should contain meaningful public view state, not secrets or every ephemeral interaction.

---

## Progressive enhancement as a layered model

```text
semantic HTML
  → server behavior
  → enhanced client behavior
  → optional richer capabilities
```

Layering can improve resilience and reduce the amount of functionality that depends on one runtime.

---

## When progressive enhancement is valuable

It is especially useful for:

- public content;
- forms and navigation;
- poor connectivity;
- accessibility;
- long-lived pages;
- critical tasks.

Not every application needs full no-JavaScript operation, but every app should understand its essential failure path.

---

## Native platform first

Before adding a dependency, ask whether the platform already provides:

- links;
- forms;
- dialog;
- details/summary;
- URL and history;
- storage;
- fetch;
- observers;
- workers.

Platform capabilities often have strong accessibility, performance, and compatibility foundations.

---

## Native does not automatically mean better

Evaluate:

- browser support;
- accessibility behavior;
- required customization;
- interaction consistency;
- testing;
- polyfills and fallbacks;
- team familiarity.

Use the platform deliberately, not ideologically.

---

## Dependency evaluation

Consider:

- capability fit;
- bundle and runtime cost;
- security and maintenance;
- accessibility;
- license and ecosystem;
- upgrade path;
- lock-in;
- team skill.

The smallest dependency is not always the cheapest total solution.

---

## Build, buy, or adopt

```text
build → unique, strategic, or tightly domain-specific capability
buy   → commodity where support is valuable
adopt  → mature open source with acceptable control and risk
```

Compare total lifecycle cost, not only initial implementation time.

---

## Core versus commodity

Protect and understand capabilities that differentiate the product.

Avoid spending strategic team capacity reinventing commodity infrastructure unless the trade-off is intentional.

Also avoid outsourcing a core capability that determines security, user trust, or domain advantage without sufficient control.

---

## Framework selection is contextual

Evaluate frameworks through:

- rendering and data needs;
- team familiarity;
- ecosystem and support;
- accessibility;
- testing;
- deployment;
- upgrade path;
- performance on target users.

Benchmark claims without context are weak evidence.

---

## Framework benchmarks are contextual

Results vary by:

- application shape;
- route size;
- data and interaction;
- device and network;
- build configuration;
- developer usage.

Run a spike with representative behavior instead of selecting a framework from a leaderboard.

---

## React versus Vue is often not the main decision

The larger questions may be:

- where server and client boundaries lie;
- how state is owned;
- how routes are delivered;
- how APIs are validated;
- how teams release;
- how failures recover.

Framework syntax rarely determines all architecture.

---

## Framework lock-in

Lock-in can be acceptable when the framework provides strong value and the team accepts its lifecycle.

Reduce unnecessary lock-in at boundaries with:

- domain models;
- adapters;
- platform APIs;
- stable package contracts;
- route and API boundaries.

Avoid turning lock-in avoidance into architecture by itself.

---

## Architecture fitness

Fitness asks whether the system continues to support important properties as it evolves.

Examples:

- no dependency cycles;
- route budget stays within threshold;
- public package imports only;
- all remote responses are validated;
- critical journey remains keyboard-usable.

---

## Evolutionary architecture

Instead of assuming the initial architecture is perfect:

```text
decision → guardrail → measure → learn → adjust
```

Architecture can evolve safely when important properties are observable and protected.

---

## Fitness functions

A fitness function is an automated or repeatable check for an architectural property.

```text
fail if shared package imports feature code
fail if initial route exceeds budget
fail if API response violates schema
```

Automate rules that matter enough to protect continuously.

---

## Architecture rule as code

Rules can be enforced through:

- lint boundaries;
- package exports;
- dependency graph checks;
- CI budgets;
- contract tests;
- runtime monitoring.

Written policy that cannot be observed often becomes forgotten policy.

---

## Fitness functions should protect important properties

Do not create checks for every preference.

Protect properties whose regression would cause meaningful harm:

- security;
- accessibility;
- performance;
- deployability;
- dependency direction;
- public contract compatibility.

---

## Architecture Decision Records

An ADR records:

- context;
- decision;
- alternatives;
- consequences;
- validation;
- status;
- revisit trigger.

It preserves reasoning after the original meeting is forgotten.

---

## ADRs are not meeting minutes

An ADR should not capture every discussion detail.

It should explain:

```text
what problem existed
what was chosen
why it was chosen
what trade-offs were accepted
when to revisit
```

---

## Example ADR: URL state for catalogue filters

```text
Context: filters should survive reload and sharing.
Decision: committed filters live in query parameters.
Alternatives: local state, global store.
Consequence: parse and validate public URL input.
Revisit: if filter data becomes sensitive or too large.
```

The ADR makes ownership and trade-offs explicit.

---

## ADR status

Useful statuses include:

```text
proposed → accepted → superseded / deprecated / rejected
```

Status tells readers whether the decision is active and whether another document replaces it.

---

## Decision scope

Record what the decision does and does not cover.

```text
scope: catalogue filter state
not scope: all application state or authentication
```

Clear scope prevents a local decision from becoming accidental universal policy.

---

## Decision matrices

A matrix can expose trade-offs:

| Option | Freshness | Complexity | Reversibility | Team fit |
|---|---:|---:|---:|---:|
| A | high | medium | high | high |
| B | medium | high | low | medium |

Use it to structure reasoning, not to pretend qualitative judgment is exact arithmetic.

---

## Avoid weighted-score theater

Numbers can create false certainty when:

- criteria are subjective;
- weights are arbitrary;
- unknowns are hidden;
- important risks are averaged away.

Show the assumptions and discuss the decisive trade-offs directly.

---

## Proof of concept and spike

```text
spike → answer one unknown quickly
proof of concept → test a plausible solution in representative context
```

Keep the purpose narrow and record what was learned.

Do not mistake experimental code for a production architecture.

---

## Architecture review

Review asks:

- does the decision fit the requirements?
- are quality attributes explicit?
- are failure modes understood?
- is the boundary appropriate?
- can it be operated and changed?
- what evidence remains weak?

It should improve the decision, not only approve a document.

---

## Decision confidence

State confidence and uncertainty:

```text
high confidence → well-understood constraint and evidence
low confidence  → important unknown remains
```

Low confidence should trigger a spike, guardrail, or revisit date.

---

## Assumption register

Track assumptions such as:

- expected traffic;
- team capacity;
- API stability;
- browser support;
- deployment independence;
- data sensitivity;
- user behavior.

An assumption that changes can invalidate the decision.

---

## Architecture risk and risk reduction

```text
risk → assumption → experiment / guardrail → evidence → decision update
```

Reduce uncertainty early when it could make the chosen architecture expensive to reverse.

---

## Failure mode analysis

For a feature, ask:

- what can fail?
- how will the user see it?
- what remains usable?
- can the operation retry?
- can the release roll back?
- who is alerted?

Failure behavior is part of the architecture, not a later polish step.

---

## Graceful degradation

```text
full capability → reduced capability → understandable failure
```

Examples:

- cached content when the network fails;
- static navigation when enhancement fails;
- panel fallback when one remote fails;
- queued draft when submission is offline.

---

## Critical path

Identify the work required for the user's first valuable outcome.

Keep optional features, telemetry, personalization, and secondary data off the critical path when possible.

Critical-path design affects rendering, performance, reliability, and architecture together.

---

## Availability architecture

Availability includes:

- resilient requests;
- cache and fallback;
- independent failure boundaries;
- deployment and rollback;
- monitoring;
- recovery ownership.

“The server is up” does not prove that the user can complete the task.

---

## Security architecture

Define:

- trust boundaries;
- identity and authorization;
- secret location;
- content and request validation;
- browser policies;
- third-party trust;
- logging and privacy.

Security belongs in the decision, not in a final header checklist.

---

## Performance architecture

Make choices about:

- rendering topology;
- JavaScript responsibility;
- cacheability;
- code splitting;
- data waterfalls;
- device cost;
- route and journey budgets.

Performance constraints should influence boundaries before slow code accumulates.

---

## Accessibility architecture

Accessibility is affected by:

- semantic HTML;
- component contracts;
- focus ownership;
- routing and navigation;
- progressive enhancement;
- design-system governance;
- testing and release policy.

Treat it as a system property, not only a component task.

---

## Internationalization architecture

Plan for:

- locale and direction;
- text expansion;
- date and number formatting;
- routing and content negotiation;
- font coverage;
- translation loading;
- persistence and URL state.

Adding i18n late often reveals hidden assumptions across every layer.

---

## Testability as an architecture attribute

Testability improves when the system has:

- explicit inputs and outputs;
- replaceable boundaries;
- deterministic transitions;
- isolated ownership;
- observable failures;
- stable contracts.

If architecture makes the important behavior impossible to isolate, testing cost is design feedback.

---

## Observability as an architecture attribute

Make it possible to answer:

- which release failed?
- which route and user journey?
- which dependency or boundary?
- which users are affected?
- can the issue be mitigated or rolled back?

Observability should be designed into boundaries and identifiers.

---

## Deployability as an architecture attribute

A deployable system has:

- build reproducibility;
- artifact identity;
- safe configuration;
- progressive delivery;
- compatibility strategy;
- rollback;
- operational ownership.

An architecture that cannot be released safely limits product change.

---

## Maintainability, reliability, scalability

```text
maintainability → can we change it?
reliability     → does it continue to work?
scalability     → does it work as demand or scope grows?
```

These properties interact and should be evaluated together.

---

## Different kinds of scale

```text
user scale
data scale
team scale
feature scale
```

A system may scale users while failing teams, or scale features while becoming impossible to reason about.

Identify which scale is actually driving the decision.

---

## Cognitive load

Architecture should reduce the amount a developer must understand at once.

Use:

- local reasoning;
- clear names;
- stable boundaries;
- focused modules;
- useful documentation;
- predictable workflows.

The fastest system to change is often the one with the clearest mental model.

---

## Architecture documentation

Useful documentation includes:

- context and system diagrams;
- ADRs;
- package and dependency maps;
- ownership;
- runbooks;
- contracts;
- failure and recovery behavior.

Document decisions that future maintainers need to preserve or revisit.

---

## C4-style thinking

Move through levels:

```text
context → containers → components → code
```

Use the level that answers the current question.

Do not create diagrams so detailed that nobody can use them.

---

## Architecture diagram purpose

A diagram should help someone:

- understand ownership;
- find a trust boundary;
- trace data flow;
- identify failure containment;
- evaluate a change;
- operate the system.

If it only decorates a presentation, it is not architecture documentation.

---

## Avoid architecture astronautics

Warning signs:

- abstractions with no current consumer;
- patterns chosen for prestige;
- distributed systems without distributed requirements;
- infrastructure whose operation exceeds its value;
- diagrams detached from code and ownership.

Complexity is not evidence of maturity.

---

## Simplicity is a feature

Simple architecture can provide:

- faster onboarding;
- easier debugging;
- fewer failure modes;
- lower operating cost;
- more reversible change.

Simple does not mean primitive or careless.

---

## Standards before custom infrastructure

Prefer platform and established protocols when they meet the requirement:

- HTTP;
- URL and history;
- HTML forms;
- browser storage;
- standard security headers;
- common observability formats.

Custom infrastructure should solve a demonstrated gap.

---

## Libraries should amplify the platform

A library is valuable when it:

- reduces repeated risk;
- provides missing capability;
- preserves accessibility;
- improves productivity;
- remains replaceable enough.

It is risky when it hides basic browser behavior the team needs to understand.

---

## Architecture and team skill

Choose a design the team can:

- explain;
- debug;
- test;
- deploy;
- operate;
- migrate.

An architecture that requires one specialist for every incident has a bus-factor problem.

---

## Hiring and onboarding

Architecture affects:

- how quickly new engineers understand the system;
- how safely they make changes;
- how much tribal knowledge is required;
- how ownership is transferred.

Good boundaries and documentation are productivity tools.

---

## Bus factor and ownership

Reduce dependence on one person through:

- shared runbooks;
- pair or review practice;
- explicit package ownership;
- reproducible workflows;
- decision records;
- operational rehearsal.

Ownership should create accountability, not private territory.

---

## Guardrails versus gates

```text
guardrail → guides or prevents common unsafe behavior
gate      → blocks progress until a condition is met
```

Use gates for security, compatibility, or release-critical requirements.

Use guardrails for recommended patterns where local judgment remains useful.

---

## Paved roads

A paved road provides:

- safe defaults;
- templates;
- supported tooling;
- examples;
- deployment and observability;
- extension points.

It should reduce cognitive load without pretending every product has the same needs.

---

## Architecture debt

Architecture debt is accumulated cost from decisions that no longer fit:

- obsolete boundaries;
- excessive coupling;
- stale platform assumptions;
- missing migrations;
- unsupported dependencies;
- unclear ownership.

Track it and prioritize by change cost and user impact.

---

## Refactoring architecture

Refactor toward boundaries through small steps:

```text
observe coupling → define contract → move one consumer → verify → repeat
```

Preserve behavior while changing structure.

---

## Strangler strategy revisited

Replace one capability at a time while the old system continues to serve the rest.

The migration needs:

- routing or proxy boundary;
- data compatibility;
- shared authentication;
- observability;
- rollback;
- ownership during coexistence.

---

## Big-bang rewrite risk

A rewrite can:

- delay user value;
- lose hidden behavior;
- recreate old mistakes;
- require long coexistence anyway;
- concentrate technical and organizational risk.

Rewrite only when the expected value and migration control justify the discontinuity.

---

## When a rewrite is justified

Possible evidence:

- the current platform cannot meet a required constraint;
- incremental migration is more expensive than replacement;
- ownership and product scope are stable;
- behavior is well understood;
- rollout and rollback are credible;
- the organization can sustain the work.

“The code feels old” is not enough evidence by itself.

---

## Technical-debt prioritization

Prioritize by:

- frequency of change;
- blast radius;
- user harm;
- security or compliance;
- delivery friction;
- probability of failure;
- reversibility.

Debt that is stable and harmless may be lower priority than a small coupling point that blocks every release.

---

## Cost of change

Measure:

- how many files or packages change;
- how many teams coordinate;
- how many environments verify;
- how many tests break;
- how much release work is needed;
- how hard rollback is.

Change amplification is architecture evidence.

---

## Scenario: public documentation

Likely priorities:

- cacheability;
- discoverability;
- accessibility;
- content publishing;
- low client cost.

Static or revalidated output with focused enhancement may be a strong fit.

---

## Scenario: internal admin

Likely priorities:

- authentication;
- dense interaction;
- productivity;
- resilient forms;
- domain workflows;
- observability.

A modular client application or hybrid route may be simpler than a public-content topology.

---

## Scenario: e-commerce

Different routes can need different strategies:

```text
marketing → static
catalogue  → cacheable hybrid
checkout   → secure interactive flow
account    → personalized server/client boundary
```

One application does not require one rendering strategy.

---

## Scenario: collaborative editor

Priorities may include:

- real-time updates;
- conflict handling;
- offline drafts;
- presence;
- low interaction latency;
- strong domain state.

The architecture should begin with synchronization and failure requirements, not a component library choice.

---

## Scenario: government service

Likely priorities:

- accessibility;
- reliability;
- security;
- auditability;
- long support life;
- progressive enhancement;
- clear recovery.

Operational simplicity and standards may matter more than fashionable distribution.

---

## Scenario: large enterprise platform

Possible pressures include:

- team autonomy;
- shared foundations;
- independent release cadence;
- multiple domains;
- legacy migration;
- governance and security.

Use explicit contracts and incremental separation before reaching for runtime federation.

---

## No architecture is context-free

A decision without context is a slogan.

Record:

- product;
- users;
- team;
- constraints;
- quality priorities;
- deployment model;
- expected change;
- evidence and unknowns.

---

## Resume-driven architecture

This occurs when a technology is chosen mainly because it is interesting or marketable.

Counter it with:

- explicit requirements;
- measurable constraints;
- a representative spike;
- total lifecycle cost;
- a revisit trigger.

Technology can be valuable without being the reason for the decision.

---

## Cargo-cult architecture

Copying a pattern from another company without its context can import:

- unnecessary services;
- incompatible team assumptions;
- different scale costs;
- hidden operational requirements.

Learn the principle, then re-evaluate it against your constraints.

---

## Framework as architecture

```text
framework → routing, rendering, components, build mechanisms
architecture → ownership, boundaries, data, quality, operations
```

The framework participates in architecture but does not replace system decisions.

---

## Pattern collection

Using every pattern creates:

- duplicated concepts;
- conflicting state paths;
- more documentation;
- harder onboarding;
- ambiguous ownership.

Patterns should solve a problem that exists in the system.

---

## Hidden architecture

Architecture is hidden when behavior depends on:

- undocumented globals;
- convention nobody can find;
- private package imports;
- manual deployment steps;
- tribal knowledge;
- unrecorded exceptions.

Make important decisions visible in code, checks, docs, and ownership.

---

## Architecture freeze

Architecture should be stable enough to guide work but revisable when evidence changes.

Use:

- ADR status;
- review triggers;
- fitness functions;
- migration paths;
- measured outcomes.

“We decided once” is not a reason to ignore new constraints.

---

## Architecture review cadence

Review architecture when:

- product scope changes;
- team topology changes;
- a quality attribute regresses;
- an integration becomes a bottleneck;
- a dependency reaches end of life;
- a migration creates new boundaries.

Review should be triggered by change, not only by calendar ceremony.

---

## Measure architecture outcomes

Possible outcomes include:

- change lead time;
- deployment failure and recovery;
- accessibility defects;
- performance budgets;
- dependency cycle count;
- onboarding time;
- support burden;
- team autonomy in practice.

Architecture quality is visible through system behavior.

---

## Architecture is sociotechnical

Technology and organization interact through:

- ownership;
- incentives;
- communication;
- release authority;
- expertise;
- support expectations.

A design that ignores people will be changed by people in ways the diagram did not predict.

---

## Architecture and product lifecycle

Prototype, growth, maturity, and retirement may need different priorities.

```text
prototype → learning speed
growth    → boundaries and scale
maturity  → reliability and maintenance
retirement → migration and safe shutdown
```

Do not optimize a prototype for the operational needs of a global platform without evidence.

---

## Architecture and deadlines

Deadlines do not eliminate architecture decisions.

Make the trade-off explicit:

- what is deferred;
- what risk is accepted;
- what boundary remains safe;
- what follow-up is required;
- what cannot be compromised.

Shortcuts are safer when named and bounded.

---

## Architecture and future change

Do not attempt to predict every future feature.

Instead, preserve:

- clear ownership;
- replaceable boundaries;
- stable contracts;
- observable assumptions;
- reversible choices where possible.

Good architecture makes learning and change affordable.

---

## The decision framework

```text
1 define problem
2 identify quality attributes
3 record constraints
4 generate alternatives
5 analyze trade-offs
6 test unknowns
7 decide
8 record ADR
9 add guardrails
10 observe
11 revisit
```

This turns architecture into a repeatable practice.

---

## Full ADR template

```text
Status
Context
Decision
Alternatives considered
Consequences
Validation
Revisit trigger
```

Keep the document concise enough to read and specific enough to preserve reasoning.

---

## Revisit triggers

Examples:

- traffic exceeds the assumed range;
- team ownership changes;
- deployment becomes a bottleneck;
- performance budget fails;
- a dependency is retired;
- a security requirement changes;
- evidence from a spike contradicts an assumption.

Triggers turn an ADR into a living decision rather than a permanent verdict.

---

## Example: catalogue state decision

```text
URL owns committed filters.
Local state owns transient input.
Server cache owns remote results.
Derived state owns visible rows.
```

The decision improves reload, sharing, caching, and testability without requiring a global store.

---

## Example: rendering decision

```text
public home → revalidated static
catalogue   → cacheable server/hybrid route
account     → personalized boundary
admin       → interaction-focused client route
```

The architecture is route-specific because requirements differ.

---

## Example: design-system decision

Share:

- tokens;
- accessible primitives;
- stable interaction patterns.

Keep local:

- domain workflows;
- product-specific orchestration;
- experimental layouts.

Promote concepts only when stability and ownership justify it.

---

## Example: micro-frontend decision

Choose runtime separation only when:

- independent deployment is a real bottleneck;
- capability boundaries are stable;
- contracts and observability exist;
- failure containment matters;
- the organization can operate the integration.

Otherwise start with packages or a modular monolith.

---

## An architectural “no”

Saying no can protect the system:

```text
No runtime federation yet.
No global store for this local state.
No public package for a one-off component.
No client exposure of this secret.
```

An architectural no should include the reason and the condition that could change it.

---

## An architectural “yes”

A good yes is bounded:

```text
Yes, use a shared package for stable accessibility primitives.
Scope: three products, public entry points, versioned releases.
Review: after two migration cycles or a major API change.
```

Boundaries make adoption safer.

---

## The browser is still the foundation

Even sophisticated systems eventually interact with:

- HTML;
- CSS;
- JavaScript;
- URLs;
- HTTP;
- browser security;
- input, focus, and rendering.

Architecture should amplify platform capabilities rather than hide them completely.

---

## HTML, CSS, and JavaScript are architecture

```text
HTML → document, semantics, navigation, forms
CSS  → layout, themes, responsiveness, visual stability
JS   → interaction, state, synchronization, runtime behavior
```

Choices at the platform layer shape accessibility, performance, testing, and resilience.

---

## Testing and observability are architecture feedback

Tests reveal whether boundaries are behaviorally useful.

Observability reveals whether boundaries work under real users, networks, devices, and releases.

Use both to decide whether architecture is serving its purpose.

---

## Architecture is continuous

```text
decide → implement → observe → learn → refactor → decide again
```

The goal is not a final perfect diagram.

The goal is a system that can change without losing control.

---

## Practical lab: Make and Defend an Architecture Decision

Create an evidence-backed architecture decision for a product platform without ranking frameworks or adopting complexity by default.

The practical ends with an ADR, fitness functions, failure modes, migration path, and decision report.

---

## Practical stages 1–5: define the problem

1. Define the product.
2. List functional requirements.
3. Rank quality attributes.
4. Record constraints.
5. Define state ownership.

State the user, team, deployment, security, performance, and organizational context.

---

## Practical stages 6–12: design the boundaries

6. Choose rendering topology.
7. Choose component boundaries.
8. Decide on shared state.
9. Choose API boundary strategy.
10. Define security boundaries.
11. Define performance constraints.
12. Define accessibility requirements.

Treat each as a decision with trade-offs, not a framework checkbox.

---

## Practical stages 13–19: evaluate the platform

13. Evaluate dependencies.
14. Evaluate framework fit.
15. Decide repository structure.
16. Evaluate micro-frontends.
17. Define testing layers.
18. Define delivery.
19. Define observability.

Prefer the smallest coherent solution that satisfies the constraints.

---

## Practical stages 20–24: reduce uncertainty

20. Create two alternatives.
21. Run a technical spike.
22. Write the ADR.
23. Add fitness functions.
24. Define failure modes.

The spike should answer the highest-risk unknown, not build the entire future system.

---

## Practical stages 25–27: migration and defense

25. Define a migration path.
26. Create the final architecture diagram.
27. Write the decision report.

Verification: the decision follows requirements, considers plausible alternatives, records uncertainty, and includes a review date.

---

## Practical extension: reversal plan

Write what evidence would cause the team to revisit the decision:

```text
metric / event / constraint change / user harm / team bottleneck
```

Include how the system would safely move to the alternative.

---

## Try this yourself

Choose one architecture decision and write:

```text
problem:
quality priorities:
constraints:
alternatives:
unknown:
spike:
decision:
consequences:
revisit trigger:
```

If the decision cannot name a problem, it may be technology fashion rather than architecture.

---

## Troubleshooting guide

| Symptom | Likely cause |
|---|---|
| Architecture debate never ends | Requirements and decision criteria are unclear |
| Every solution is global | Ownership and locality were not evaluated |
| Micro-frontends are proposed immediately | Organizational pressure was mistaken for runtime need |
| ADRs are long and unread | They record meetings instead of decisions |
| Fitness checks are ignored | They protect preferences rather than important properties |
| Rewrite feels safer than migration | Hidden behavior and compatibility cost are underestimated |
| Shared package changes break everyone | Public API and versioning are weak |
| Architecture depends on one expert | Ownership, documentation, and runbooks are insufficient |
| “Simple” system fails at scale | The relevant quality attribute was not measured |

---

## Completion checklist

- [ ] the problem and context are explicit;
- [ ] quality attributes are prioritized and measurable;
- [ ] constraints are distinguished from preferences;
- [ ] alternatives and trade-offs are documented;
- [ ] unknowns are tested with focused spikes;
- [ ] boundaries reduce change cost and blast radius;
- [ ] important architecture properties have guardrails;
- [ ] failure, security, performance, and accessibility are included;
- [ ] migration and rollback are credible;
- [ ] the decision has an owner and revisit trigger.

---

## Misconceptions to leave behind

| Misconception | Better mental model |
|---|---|
| Architecture is the technology stack | It is contextual decisions and boundaries |
| A good architecture optimizes everything | It makes explicit trade-offs |
| More abstraction is better | Abstraction has coupling and cognitive cost |
| Duplication is always bad | Local duplication can preserve autonomy |
| Global state is required for scale | Ownership and lifetime determine scope |
| SSR is more architectural than CSR | Rendering is one contextual decision |
| Micro-frontends are the natural future | Distribution is justified by real independence needs |
| Every shared component belongs centrally | Stable shared concepts deserve promotion |
| ADRs are bureaucracy | They preserve reasoning and revisit conditions |
| A decision cannot change | Architecture should learn from evidence |
| A rewrite is cleaner | Incremental migration often reduces risk |
| Technical debt must always be removed | Prioritize by impact and change cost |
| Simplicity means underengineering | Simplicity can be deliberate, bounded architecture |

---

## The chapter in one sentence

> **Make architecture decisions from requirements, quality attributes, constraints, evidence, and reversible boundaries—and keep revisiting them as the system and organization learn.**

---

## Next: Chapter 19

The next chapter will build on the full architecture model with:

- capstone system design;
- integrated product constraints;
- end-to-end architecture defense;
- final implementation and review;
- a complete front-end engineering blueprint.

---

## Questions

Which architecture decision in your system is treated as permanent even though its assumptions, evidence, or constraints have already changed?

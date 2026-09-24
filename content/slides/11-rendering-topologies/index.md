---
title: "Rendering Topologies: CSR, SSR, SSG & Beyond"
description: "Chapter 11: choose where and when rendering happens, manage hydration and handoff costs, and design hybrid routes deliberately."
book_number: "11"
weight: 12
---

# Rendering Topologies: CSR, SSR, SSG & Beyond

Choose where the work happens

**Chapter 11**

Polla Fattah

---

## Today's goal

Understand rendering as a placement and timing decision rather than a framework label.

We will connect:

- client-side rendering, server-side rendering, and static generation;
- hydration, serialization, handoff, and browser work;
- partial hydration, islands, streaming, and hybrid routes;
- revalidation, edge rendering, server components, and resumability;
- cacheability, personalization, authentication, and failure modes;
- performance as server, build, network, and device cost;
- a route-specific rendering decision matrix.

---

## By the end of today you can

- explain where rendering happens and when it occurs;
- compare CSR, SSR, and SSG without slogans;
- identify hydration mismatch causes and handoff costs;
- isolate interactive regions with islands or client boundaries;
- design streaming boundaries that preserve UX and accessibility;
- distinguish server components from server-rendered HTML;
- reason about revalidation, edge execution, and resumability;
- select a rendering strategy per route;
- keep secrets and server-only data on the server;
- measure the rendering cost triangle instead of optimizing one metric.

---

## The central principle

> **Rendering architecture is the deliberate placement of work across build time, request time, and browser time according to freshness, personalization, interaction, cacheability, and device cost.**

CSR, SSR, and SSG are tools in a continuum—not application-wide identities.

---

## The four main questions

Ask:

1. Where does rendering happen?
2. When does it happen?
3. What is transferred to the browser?
4. What must execute in the browser?

The answers reveal the actual topology beneath a framework's terminology.

---

## Build time, request time, and browser time

```text
build time   → precompute output before deployment
request time → compute for a request or user
browser time → execute JavaScript and update the interface
```

Every topology moves work among these three moments.

---

## Rendering is work

Rendering may include:

- fetching data;
- transforming content;
- producing HTML;
- serializing state;
- parsing JavaScript;
- hydrating event handlers;
- committing DOM updates;
- running device-side interaction.

“Rendered” does not mean “free”. It means the cost moved somewhere.

---

## Client-side rendering

```text
browser receives shell and JavaScript
  → JavaScript loads data
  → components calculate UI
  → browser creates content
```

CSR moves much of the initial rendering work to the device.

---

## CSR strengths

CSR can provide:

- rich interaction after startup;
- simple browser-side state ownership;
- app-like navigation;
- direct access to browser APIs;
- a consistent client runtime.

It is often appropriate for authenticated tools and highly interactive workspaces.

---

## CSR costs

The browser may need to:

- download a larger JavaScript bundle;
- parse and execute before content appears;
- fetch data after startup;
- render on lower-powered devices;
- manage loading and error states before the first useful view.

The network and device become part of the initial critical path.

---

## SPA and CSR are related, not identical

```text
CSR → where initial rendering happens
SPA → how navigation and application shell are organized
```

A site can use client rendering without being one large SPA.

An SPA can include server-rendered initial HTML.

Do not use the terms as interchangeable architecture decisions.

---

## CSR and search engines

Search engines may execute JavaScript, but discoverability, timing, metadata, content quality, and operational behavior still matter.

Public content often benefits from HTML being available before client execution.

The correct choice depends on the content and delivery requirements.

---

## Server-side rendering

```text
request
  → server loads data and renders HTML
  → browser receives useful document
  → client JavaScript hydrates interactive regions
```

SSR moves initial rendering work to request time and improves the first document's content availability.

---

## SSR changes the critical path

The request may now wait for:

- server data;
- server rendering;
- serialization;
- network transfer;
- browser parsing;
- hydration.

SSR can improve first content while adding server latency and operational complexity.

---

## SSR does not mean no JavaScript

If the page must respond to:

- clicks;
- typing;
- menus;
- client navigation;
- live state;

some browser code still needs to execute.

SSR determines how initial output is produced, not whether interaction exists.

---

## SSR does not automatically improve every page

SSR can be a poor fit when:

- content is highly personalized and uncacheable;
- server data is slow;
- the page is mostly an internal interactive tool;
- hydration cost dominates;
- deployment cannot support reliable request rendering.

Measure the whole request-to-interaction path.

---

## Time to first byte matters

```text
request → server work → first byte → HTML parsing → useful content
```

A server-rendered page with a slow first byte may feel worse than a carefully designed static or client-rendered page.

Rendering location alone does not determine speed.

---

## Static site generation

```text
build → render HTML → deploy files → serve quickly
```

SSG moves rendering cost to deployment or build time.

It works especially well for public content with predictable freshness and high cacheability.

---

## SSG strengths

SSG can provide:

- fast delivery from a CDN;
- simple serving infrastructure;
- strong cacheability;
- stable public HTML;
- low request-time computation.

The trade-off is build-time freshness and build complexity.

---

## Static generation moves cost to deployment

Large sites may pay through:

- long builds;
- many pages;
- content invalidation;
- preview workflows;
- deployment coordination.

“Static” is operationally simple at request time, not necessarily cheap everywhere.

---

## Static does not mean non-interactive

```text
static HTML + client island = interactive page
```

A generated page can include search, menus, forms, and other browser behavior.

Static describes when initial output was produced, not the absence of JavaScript.

---

## Static data can become stale

Define a freshness policy:

- rebuild on content change;
- revalidate periodically;
- regenerate on demand;
- add client refresh;
- show the publication time.

SSG requires a plan for change, not an assumption that published data never changes.

---

## CSR, SSR, and SSG describe initial rendering

After initial delivery, all three may:

- fetch new data;
- navigate without a full document;
- run client components;
- update the DOM;
- synchronize with external systems.

Do not infer the entire runtime architecture from the first render label.

---

## Hydration reuses existing HTML

```text
server HTML
  + client JavaScript
  → attach behavior and state to matching output
```

Hydration is a handoff from server-produced markup to an interactive browser runtime.

It is not simply a second independent render with no cost.

---

## Hydration mismatches are signals

A mismatch can come from:

- random values;
- current time or timezone;
- browser-only APIs;
- different data on server and client;
- unstable IDs;
- conditional rendering based on client detection.

The warning often indicates an unclear rendering boundary or nondeterministic initial model.

---

## Browser-only APIs need a boundary

```ts
const width = window.innerWidth;
```

This cannot run during server rendering.

Options include:

- client-only component;
- post-hydration effect;
- server-safe default;
- explicit capability check outside initial render.

---

## Deterministic initial rendering

The server and client should agree on the initial representation.

Avoid using during initial render:

- random values;
- current time without a shared value;
- locale-dependent formatting without a fixed locale;
- browser state unavailable to the server.

Make the handoff data explicit.

---

## Hydration has CPU cost

The browser may need to:

- download JavaScript;
- parse and compile it;
- execute component code;
- attach listeners;
- reconstruct client state;
- process event boundaries.

HTML existing on screen does not mean the page is ready for interaction.

---

## The server-to-client handoff

```text
server data and decisions
  → serialized payload
  → network transfer
  → browser parse
  → client state reconstruction
  → interactive behavior
```

Design the handoff as a contract.

Transfer only what the browser needs and keep secrets server-side.

---

## Serialization has constraints

Not every server-side value can cross the boundary safely:

- functions;
- database connections;
- secrets;
- file handles;
- cyclic structures;
- framework-specific objects;
- sensitive records.

Use explicit transport models rather than passing arbitrary server objects.

---

## Secrets must stay server-side

```text
server credential / private query
          ✕
serialized browser payload
```

SSR does not make a secret safe if the secret is embedded in HTML or serialized props.

Rendering on the server is not the same as authorization.

---

## Hydration is not free because HTML exists

Measure:

- time to first byte;
- first contentful paint;
- time to interactive;
- JavaScript transfer;
- hydration CPU;
- input delay;
- post-hydration data work.

The right topology minimizes the cost that matters for the route and its users.

---

## Partial hydration

```text
static HTML
  + hydrate only selected interactive regions
```

Partial hydration reduces browser work when most of the page is content or static structure.

It requires clear boundaries for state and events.

---

## Islands architecture

```text
static page
├─ navigation island
├─ search island
├─ product-card island
└─ comments island
```

Each island can hydrate independently.

The default becomes HTML with isolated interactive regions rather than one full-page client runtime.

---

## Islands change the default

Instead of asking “how do we render the whole app in the browser?” ask:

```text
which regions truly need client behavior?
```

This can reduce JavaScript, but introduces coordination decisions when islands need shared state.

---

## Island hydration timing

Possible policies:

```text
load immediately
hydrate when visible
hydrate on idle
hydrate on interaction
hydrate only on a specific condition
```

Choose timing based on user value and interaction urgency.

---

## Islands have boundaries

Cross-island communication may need:

- URL state;
- custom events;
- shared server state;
- browser storage;
- a client coordinator.

Do not recreate a hidden global application just to make every island know about every other island.

---

## Streaming changes delivery timing

```text
send shell and ready content
  → send slower regions as they resolve
```

Streaming can improve perceived progress and reduce waiting for the slowest dependency.

It does not automatically eliminate total server, network, or browser work.

---

## Streaming boundaries are UX boundaries

Each boundary should define:

- what appears first;
- what loading state is shown;
- what remains interactive;
- what happens on failure;
- how layout remains stable.

The stream is part of the product experience, not only a transport optimization.

---

## Suspense as a boundary concept

```text
shell
  ├─ ready navigation
  └─ pending product panel
```

A suspense-like boundary lets the system reveal available content while a slower region resolves.

Use meaningful fallbacks rather than arbitrary spinners everywhere.

---

## Streaming and accessibility

As content arrives progressively:

- preserve logical document order;
- do not move focus unexpectedly;
- announce important updates appropriately;
- keep headings and landmarks coherent;
- avoid making keyboard users wait for a needed control without feedback.

Delivery timing must preserve usable structure.

---

## Streaming and layout stability

Reserve predictable space where possible.

Unexpected late content can:

- shift reading position;
- move a focused control;
- cause accidental clicks;
- increase cumulative layout shift.

Loading UI is a layout contract.

---

## SSR and streaming can mix

```text
server-rendered shell → streamed data-dependent regions → client interaction
```

Streaming is a delivery strategy layered onto server rendering.

It does not create a separate universal topology that replaces SSR or SSG.

---

## Static generation and streaming can also mix

A statically generated shell can load or stream a dynamic region later through client or edge behavior.

The route may combine:

- prebuilt public content;
- request-time personalization;
- browser-side interactivity.

Hybrid is often a precise choice, not architectural inconsistency.

---

## Hybrid rendering is route-level strategy

```text
home page      → SSG / revalidation
catalogue      → SSR or cached hybrid
account        → SSR with personalization
admin editor   → CSR or interactive hybrid
```

Choose per route and sometimes per region within a route.

---

## Revalidation and incremental generation

```text
serve existing output
  → determine it is stale
  → regenerate in background or on demand
  → publish new output
```

Incremental strategies reduce full rebuild cost while preserving static delivery for many requests.

---

## Incremental static regeneration

An incrementally generated page has:

- a cached representation;
- a freshness window or invalidation event;
- regeneration work;
- a fallback while regeneration occurs;
- failure behavior.

The important design is the stale and failure policy, not the product name of the mechanism.

---

## Stale-while-revalidate rendering

```text
cached HTML → serve immediately
            → regenerate in background
            → future requests see newer output
```

This works well for content where slightly stale output is acceptable and fast delivery matters.

---

## Edge rendering

Edge execution moves request-time work closer to users or data paths.

Potential benefits:

- lower network distance;
- request-aware personalization;
- distributed cache integration.

It is still request-time server work with runtime and deployment constraints.

---

## Edge runtime trade-offs

Edge environments may constrain:

- Node-specific APIs;
- native modules;
- filesystem access;
- connection lifetimes;
- debugging and observability;
- regional consistency.

“Edge” is not automatically faster or simpler.

---

## Render near the data or near the user?

```text
near data → lower backend latency / private access
near user → lower delivery distance / edge personalization
```

The best location depends on data source, cacheability, user distribution, and runtime capabilities.

---

## Server components are not the same as SSR

```text
SSR            → when initial HTML is produced
Server component → where a component's logic and data access execute
```

A server component may participate in different rendering and navigation strategies.

Do not collapse execution location and HTML delivery into one concept.

---

## Server components can run at different times

Depending on the framework and route, server-side component work may happen:

- at build time;
- at request time;
- during a client navigation that requests a new payload;
- during revalidation.

The route's data and cache policy still determine the actual behavior.

---

## Server components can reduce client JavaScript

They can keep data access and noninteractive rendering on the server.

Only interactive boundaries need client behavior.

This can reduce browser bundle responsibility, but the handoff and client boundaries still have costs.

---

## Client components own browser behavior

Use a client boundary for:

- event handlers;
- local interactive state;
- browser APIs;
- effects and subscriptions;
- client-only libraries.

Keep the boundary as small as the interaction allows.

---

## Server/client boundaries are architectural boundaries

```text
server data and secrets
          ↓ explicit serializable props
client interaction
```

The boundary controls:

- what crosses the network;
- what JavaScript ships;
- where authorization occurs;
- which state is reconstructed in the browser.

---

## Data can be loaded near server rendering

Loading data close to server-rendered components can avoid duplicating the initial request in the browser.

But make the client handoff explicit:

- is the data serialized?
- is it cached?
- does the client revalidate?
- can the browser receive only a projection?

---

## The server component payload has a cost

The browser may receive a structured description of server/client boundaries and data needed for the client tree.

Measure:

- payload size;
- serialization work;
- parsing;
- client boundary setup;
- repeated requests during navigation.

Moving logic server-side does not make all transfer cost disappear.

---

## Hydration still matters with server components

Client components still need browser execution and interaction setup.

Server components can reduce the amount that hydrates, but they do not remove the need to design client boundaries, identity, and state handoff.

---

## Next.js as a case study

Next.js can combine:

- static generation;
- server rendering;
- route-level revalidation;
- server and client components;
- streaming;
- client navigation.

Treat these as mechanisms for route decisions, not as a substitute for the rendering mental model.

---

## Nuxt as a case study

Nuxt can combine:

- universal rendering;
- static generation;
- route rules;
- server handlers;
- client hydration;
- hybrid deployment.

Again, understand where data and rendering work occur rather than memorizing framework labels.

---

## Frameworks should not become the mental model

Ask framework-independent questions:

- when is the HTML produced?
- where is data loaded?
- what crosses to the browser?
- which region hydrates?
- how is freshness controlled?
- what happens on navigation and failure?

Then map the answers to framework configuration.

---

## The “double data” oversimplification

SSR does not always mean the same data is fetched twice.

Possible designs include:

- server output only for static content;
- serialized data reused by the client;
- a client revalidation request by policy;
- server component payloads with selective transfer.

Inspect the actual network and handoff path.

---

## Streaming does not eliminate handoff cost

Even if HTML arrives progressively, the browser may still need to:

- parse client JavaScript;
- hydrate interactive regions;
- receive additional data;
- attach event behavior.

Streaming improves timing of availability; it does not erase client responsibility.

---

## Resumability changes the handoff shape

```text
hydration → execute client code to reconstruct behavior
resumability → resume serialized work when interaction requires it
```

Resumability can reduce eager browser execution by preserving more execution context across the server boundary.

---

## Hydration versus resumability

| Hydration | Resumability |
|---|---|
| eagerly reconstructs client behavior | resumes behavior on demand |
| predictable component startup cost | more serialization and constraints |
| familiar event setup model | finer-grained lazy execution |
| browser executes more initially | browser may do less initial work |

Both require stable boundaries and explicit data transfer.

---

## Resumability has constraints

The system must preserve enough information to resume:

- event handlers;
- closures or state references;
- component identity;
- serialized data;
- dependency relationships.

Reducing initial work can move complexity into build output and programming constraints.

---

## Rendering topologies form a continuum

```text
prebuilt HTML
  ↔ revalidated HTML
  ↔ request-rendered HTML
  ↔ streamed HTML
  ↔ partial hydration / islands
  ↔ full client application
```

Real applications can occupy several points at once.

---

## Route decision: marketing homepage

Often:

- public;
- highly cacheable;
- content changes on a publishing schedule;
- limited interaction.

SSG or revalidated static output is often a strong starting point, with small client islands for interaction.

---

## Route decision: product catalogue

Often:

- public or semi-public;
- filterable and paginated;
- freshness matters;
- URL state matters;
- some interaction is client-side.

Hybrid SSR/SSG with URL-driven client behavior or cached server queries may fit better than one whole-site rule.

---

## Route decision: account page

Often:

- personalized;
- permission-sensitive;
- less cacheable publicly;
- form and interaction heavy.

Request rendering or a client application with a secure data boundary may be appropriate.

---

## Route decision: rich internal editor

Often:

- authenticated;
- interaction-dense;
- stateful;
- device-aware;
- not valuable to search engines.

CSR or a hybrid shell with focused server data boundaries may be simpler and more effective.

---

## A route decision matrix

| Question | Push toward |
|---|---|
| public and rarely changing? | SSG / revalidation |
| personalized per request? | SSR / client data |
| high interaction density? | client boundaries / CSR |
| slow independent region? | streaming |
| mostly static with small interactions? | islands |
| expensive browser startup? | server rendering / partial hydration |
| strict freshness and authorization? | request-time server boundary |

Use several answers together.

---

## Personalization reduces cacheability

Separate:

```text
public cacheable shell
  + user-specific region
```

Do not make an entire page uncacheable when only one small region depends on identity.

The boundary can be server-rendered, client-loaded, or streamed according to risk and UX.

---

## Authentication and rendering

Server rendering can check authentication before producing private output.

But ensure:

- private data is not cached publicly;
- redirects do not leak resource existence;
- serialized props do not contain excess data;
- client boundaries enforce appropriate behavior too.

Rendering location does not replace authorization policy.

---

## Error handling across topologies

```text
build failure       → deployment / publishing response
server request fail → route or region error boundary
hydration mismatch  → model and handoff fix
client request fail → interactive recovery state
```

Each topology moves failure to a different phase.

---

## Route loading across topologies

```text
CSR: client shell → data and route code
SSR: request → server data and HTML
streaming: shell → regions as ready
SSG: prebuilt output → client enhancement
```

Choose loading states that match the actual phase the user is waiting through.

---

## Navigation after initial load

Client navigation can avoid a full document request, but it still may require:

- route data;
- server component payload;
- code chunks;
- cache lookup;
- state preservation;
- scroll and focus management.

Initial rendering strategy does not fully determine navigation behavior.

---

## Full document navigation still has value

Full navigation can provide:

- a clean server boundary;
- lower client runtime assumptions;
- reliable reset of page state;
- progressive enhancement;
- simpler failure recovery.

Do not remove it merely because client navigation is fashionable.

---

## Progressive enhancement and rendering

```text
semantic HTML and server behavior
  → enhanced navigation and interaction
```

The basic task should remain understandable and usable when client code is delayed or unavailable, when the product permits it.

---

## Performance is multidimensional

Measure:

- server latency;
- build time;
- HTML size;
- JavaScript transfer;
- hydration CPU;
- device memory;
- interaction readiness;
- cache hit rate;
- freshness and error recovery.

Optimizing one number can worsen the actual experience.

---

## JavaScript budget

Client JavaScript has costs in:

- transfer;
- parse and compile;
- memory;
- event setup;
- hydration;
- battery;
- later navigation.

Ship browser code because the user needs the behavior, not because the framework can render it there.

---

## HTML is already a runtime format

HTML provides:

- document structure;
- links;
- forms;
- semantic controls;
- accessibility relationships;
- progressive behavior.

Do not replace platform capabilities with client code without a clear benefit.

---

## Server work has operational cost

Request rendering consumes:

- compute;
- memory;
- connection capacity;
- data-source capacity;
- observability and deployment complexity.

SSR is not free work merely because the browser does less.

---

## Build work has operational cost

Static generation consumes:

- build time;
- CI resources;
- content pipeline capacity;
- deployment storage;
- invalidation and preview complexity.

Choose build-time rendering when its freshness and delivery benefits justify the workflow.

---

## Client work has device cost

Browser work varies with:

- device CPU;
- memory;
- battery;
- network conditions;
- browser capability;
- competing applications.

Do not treat a fast developer laptop as a universal client.

---

## The rendering cost triangle

```text
        server/request cost
             /\
            /  \
           /    \
build cost ───── client/device cost
```

Moving work away from one corner usually adds cost or constraints to another.

---

## Content freshness changes the choice

```text
rarely changes      → build / cache
changes hourly      → revalidation / background regeneration
changes per request → SSR or client query
changes continuously→ live client boundary
```

Freshness is a route requirement, not a framework preference.

---

## User-specific state changes the choice

Private data may require:

- request-time authorization;
- private caching;
- client-side loading after a public shell;
- isolated personalized regions.

Separate public and private regions when possible to preserve cacheability.

---

## Interaction density changes the choice

```text
content-heavy → more server/static work
interaction-heavy → more client responsibility
mixed route → isolate interactive regions
```

The amount and locality of interaction matter more than whether a page is “modern”.

---

## Practical project: one platform, several topologies

Compare the same product catalogue requirements through CSR, SSR, SSG, streaming, and an island-like boundary.

Record data freshness, interaction, handoff, JavaScript, caching, and failure assumptions for each version.

---

## Practical stages 1–4: establish the comparison

1. Establish route data and interaction requirements.
2. Build a CSR baseline.
3. Create a minimal server-rendered version.
4. Create a static version with explicit freshness assumptions.

Do not compare only screenshots. Compare the work and data path behind each result.

---

## Practical stages 5–9: handoff and streaming

5. Add streaming or a delayed independent region.
6. Record the server-to-client handoff and hydration cost.
7. Design streaming boundaries.
8. Compare one large boundary with many tiny boundaries.
9. Identify which regions truly need browser execution.

Measure timing and layout stability as well as total output.

---

## Practical stages 10–14: hybrid framework concepts

10. Compare Next.js conceptually.
11. Compare Nuxt conceptually.
12. Build a hybrid route plan.
13. Isolate personalization.
14. Explore islands.

The final choice should be route-specific rather than application-wide dogma.

---

## Practical stages 15–19: reduce and justify browser work

15. Delay island hydration.
16. Explore resumability conceptually.
17. Build a rendering decision matrix.
18. Measure JavaScript responsibility.
19. Draw the final hybrid architecture.

Verification: each topology has a stated freshness and interaction model, and server-only data stays server-side.

---

## Practical extension: authenticated account route

Compare the public catalogue with an authenticated account route.

Explain why the decision differs in terms of:

- cacheability;
- authorization;
- personalization;
- interaction density;
- data freshness;
- handoff and failure behavior.

---

## Try this yourself

For one application, classify these routes:

```text
home page
product catalogue
product detail
account page
admin editor
```

For each, choose where rendering happens, when it happens, what crosses to the browser, and what must be interactive.

---

## Common rendering smells

Watch for:

- entire site forced into CSR because one page is interactive;
- entire application SSR because “SSR is faster”;
- every component marked client-side;
- huge framework bundle for a static page;
- personalized region preventing the whole page from caching;
- slow widget blocking all server HTML;
- same data fetched on server and immediately fetched again on client.

---

## Hydration mismatch is usually a modeling signal

Instead of suppressing the warning, ask:

- which value differs?
- who owns it?
- was it available on both sides?
- should it be client-only?
- should the server serialize a stable value?
- is the initial output deterministic?

Fix the rendering model before hiding the symptom.

---

## Avoid browser detection during render

```tsx
const isMobile = window.innerWidth < 768;
```

The server and client may choose different trees.

Prefer CSS for presentation, a stable server-safe structure, or a client-only boundary when behavior truly depends on browser capability.

---

## Dates, time zones, and random values

These are common mismatch sources:

```text
server timezone ≠ browser timezone
server clock     ≠ browser clock
server random    ≠ browser random
```

Use a shared value, deterministic seed, explicit locale/timezone, or post-hydration update.

---

## Streaming and failure isolation

A streamed region can fail after the shell is visible.

Define:

- a local fallback;
- retry behavior;
- whether prior content remains;
- logging and observability;
- accessible announcement of the failure.

Progressive delivery requires progressive recovery.

---

## SSG and content publishing

A publishing workflow should answer:

- when is a page rebuilt?
- how are previews generated?
- how is stale content invalidated?
- can a failed build leave the previous version live?
- which content requires request-time freshness?

Rendering strategy includes the authoring and deployment system.

---

## Rendering topology and deployment

```text
CSR      → static shell + CDN + browser runtime
SSG      → build pipeline + static hosting
SSR      → request runtime + data services
edge SSR → distributed runtime + edge constraints
```

Deployment capabilities are part of the architecture, not an afterthought.

---

## Rendering topology and failure modes

```text
build failure      → previous deployment / publishing error
server data failure→ route or region fallback
client bundle fail → static content plus degraded interaction
hydration mismatch → deterministic handoff fix
stale output       → revalidation or freshness message
```

Design the failure path at the same time as the happy path.

---

## Practical decision checklist

Ask:

- Is the content public?
- How often does it change?
- Is it user-specific?
- How interactive is it?
- Does it need browser-only APIs?
- Can the output be cached?
- Are data dependencies slow?
- Can interaction be isolated?
- How much state must cross to the browser?
- What happens after initial navigation?

---

## Completion checklist

- [ ] route strategy is chosen from requirements rather than slogans;
- [ ] build, request, and browser work are identified;
- [ ] hydration output is deterministic;
- [ ] secrets and server-only data stay server-side;
- [ ] interactive boundaries are no larger than necessary;
- [ ] streaming boundaries have meaningful loading and error behavior;
- [ ] cacheability and personalization are separated where possible;
- [ ] freshness and revalidation are explicit;
- [ ] JavaScript and device cost are measured;
- [ ] deployment and failure behavior match the topology.

---

## Misconceptions to leave behind

| Misconception | Better mental model |
|---|---|
| CSR means no server | It moves initial rendering work to the browser |
| SPA and CSR are identical | Navigation model and rendering location differ |
| SSR means no JavaScript | Interactive regions still need browser code |
| SSR is always faster | Server latency, hydration, and cacheability matter |
| SSG cannot be interactive | Static output can include client islands |
| Static means always fresh | Publication and revalidation define freshness |
| Hydration rebuilds the DOM | It attaches client behavior to existing output |
| Streaming removes handoff cost | It changes delivery timing, not all work |
| Server components are just SSR | Execution location and HTML timing differ |
| Islands are automatically better | Coordination and boundary costs still exist |
| Edge is always faster | Runtime, data location, and cache behavior matter |
| Resumability is just faster hydration | It changes the server-client handoff model |

---

## The chapter in one sentence

> **Choose a rendering topology per route and region by balancing freshness, personalization, interaction, cacheability, handoff, deployment, and device cost.**

---

## Next: Chapter 12

The next chapter will build on rendering architecture with:

- testing strategy and quality boundaries;
- unit, integration, and end-to-end tests;
- browser behavior and accessibility verification;
- performance and failure testing;
- confidence in evolving front-end systems.

---

## Questions

For your home page, catalogue, account page, and admin editor: where should the first useful HTML come from, and what is the smallest region that truly needs browser execution?

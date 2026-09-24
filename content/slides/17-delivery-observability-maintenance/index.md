---
title: "Continuous Delivery, Observability & Maintenance"
description: "Chapter 17: build a safe frontend delivery loop with reproducible artifacts, progressive releases, production signals, rollback, and maintenance."
book_number: "17"
weight: 18
---

# Continuous Delivery, Observability & Maintenance

Close the loop from commit to production learning

**Chapter 17**

Polla Fattah

---

## Today's goal

Make delivery and production feedback part of front-end architecture.

We will connect:

- CI, reproducibility, artifacts, and environments;
- preview, staging, production, and deployment protection;
- release strategies, feature flags, canaries, and rollback;
- logs, metrics, traces, RUM, errors, and session context;
- dashboards, alerts, SLOs, error budgets, and synthetic monitoring;
- dependency, browser, API, service-worker, and technical-debt maintenance;
- ownership, runbooks, incident response, privacy, and production readiness.

---

## By the end of today you can

- design a CI pipeline with fast and broad verification stages;
- produce and promote one versioned artifact;
- separate preview, staging, and production responsibilities;
- use feature flags without confusing them with authorization;
- plan canary, rollback, and kill-switch behavior;
- distinguish monitoring from observability;
- define useful frontend telemetry without oversharing data;
- create SLOs and alerts with owners and response actions;
- maintain dependencies, browser support, APIs, storage, and service workers;
- write a production runbook and rehearse the delivery loop.

---

## The central principle

> **A production system is complete only when it can be built reproducibly, released safely, observed meaningfully, rolled back deliberately, and maintained continuously.**

Delivery is not the final step after architecture.

It is where architecture meets users, operators, and reality.

---

## The complete production loop

```text
commit
  → verify
  → build artifact
  → preview
  → release progressively
  → observe
  → mitigate or continue
  → maintain and learn
```

Every arrow needs an owner, evidence, and a recovery path.

---

## Delivery is part of architecture

Delivery decisions determine:

- which code reaches users;
- how quickly a fix can ship;
- whether a release can be identified;
- how a failure is contained;
- whether rollback is possible;
- how production evidence reaches developers.

A frontend that cannot be safely changed is not operationally complete.

---

## Continuous integration

CI validates changes in a clean, shared environment.

It can verify:

- installation;
- linting and formatting;
- type checking;
- unit and integration tests;
- production build;
- artifact integrity;
- smoke behavior.

CI is a feedback system, not merely a hosted command runner.

---

## CI is more than “run tests”

```text
source + lockfile + runtime + config
  → clean install
  → checks
  → build
  → artifact and metadata
```

The environment and produced artifact are part of what CI verifies.

---

## CI events

Useful triggers include:

- pull request;
- push to a protected branch;
- release tag;
- scheduled dependency check;
- manual promotion;
- rollback or emergency fix.

Choose the checks and permissions appropriate to each event.

---

## Fast feedback still matters

```text
editor → local check → PR check → merge check → release check
```

Fast checks should catch common mistakes near the change.

Broad checks should protect integration and delivery confidence.

Do not make every local edit wait for the entire release pipeline.

---

## Parallel CI

Independent jobs can run concurrently:

```text
lint ──────┐
types ─────┼─→ build / deploy decision
unit ──────┘
```

Parallelism requires isolated environments, clear dependencies, and attributable artifacts.

---

## CI caching

Cache:

- package downloads;
- transformed dependencies;
- test artifacts;
- build tasks;
- browser binaries when safe.

Cache keys must include every input that affects correctness.

An incorrect cache can create false green builds.

---

## Reproducibility

A reproducible build depends on:

- locked dependencies;
- known runtime version;
- explicit environment inputs;
- stable build configuration;
- deterministic generation;
- documented external services.

If two clean builds produce different artifacts, investigate why before relying on promotion.

---

## Continuous integration versus delivery versus deployment

```text
CI             → verify changes
continuous delivery → keep a releasable artifact ready
continuous deployment → automatically release after verification
```

An organization can practice delivery without automatically deploying every commit.

Automation level should match risk and release confidence.

---

## Build artifact

An artifact is the output intended for deployment:

- static assets;
- HTML;
- server bundle;
- manifests;
- source-map references;
- release metadata.

It should be identifiable and traceable back to source and dependencies.

---

## Immutable artifacts

```text
build once → store artifact → promote same artifact
```

Rebuilding separately for staging and production can produce different output.

Promotion should change environment configuration, not application bytes, whenever possible.

---

## Static frontend artifact

For a static application, verify:

- asset fingerprints;
- manifest paths;
- base URL;
- cache headers;
- source-map policy;
- service-worker version;
- public environment values.

The static artifact is still an operational release unit.

---

## Server-rendered artifact

A server-rendered release may include:

- server code;
- client chunks;
- route configuration;
- environment references;
- source maps;
- migration compatibility.

Test the server and browser parts as one release contract.

---

## Environments

```text
development → preview → staging → production
```

Each environment should have a purpose rather than existing only because a template created it.

Document data, secrets, access, observability, and deployment differences.

---

## Development environment

Optimize for:

- fast feedback;
- local debugging;
- safe test data;
- representative boundaries;
- developer control.

Development convenience must not hide production-critical behavior.

---

## Preview environments

A preview environment connects a change to a deployed, reviewable experience.

It can reveal:

- asset path issues;
- routing failures;
- environment assumptions;
- visual changes;
- integration behavior.

---

## Preview environments improve communication

They let reviewers discuss:

- the actual UI;
- loading and error states;
- responsive behavior;
- accessibility;
- product intent.

Preview is evidence that complements code review; it does not replace it.

---

## Preview environment data

Use data that is:

- safe to expose to reviewers;
- representative enough to reveal behavior;
- isolated from production;
- resettable or expiring;
- privacy-aware.

Never copy sensitive production data into preview casually.

---

## Staging

Staging can validate:

- production-like infrastructure;
- integrations;
- deployment scripts;
- migration compatibility;
- smoke and end-to-end behavior.

It is not automatically identical to production and should not create false certainty.

---

## Production

Production needs:

- controlled access;
- secrets management;
- monitoring;
- rollback;
- incident response;
- privacy controls;
- support ownership;
- documented change history.

The production environment is part of the product's operating system.

---

## Deployment protection

Protect production with:

- required reviews;
- environment approvals;
- scoped credentials;
- branch or tag rules;
- concurrency control;
- audit history;
- automated verification.

Protection should reduce dangerous mistakes without making recovery impossible.

---

## Environment secrets

Secrets should be injected through the deployment environment, not committed or embedded in public frontend assets.

Separate:

```text
public configuration → browser may receive
private secret        → trusted server or CI boundary only
```

Rotate and audit access.

---

## Principle of least privilege

Give each job and environment only the access it needs.

Examples:

- preview cannot delete production data;
- build cannot deploy unrelated services;
- frontend runtime cannot read deployment credentials;
- telemetry cannot expose raw user content.

Least privilege limits blast radius.

---

## Deployment concurrency

Decide what happens when two deployments target one environment:

- queue;
- cancel older pending deploy;
- serialize production;
- allow parallel previews;
- block promotion until verification.

Ambiguous concurrency creates releases that are difficult to identify and roll back.

---

## Deployment history

Record:

- release version;
- commit;
- artifact digest;
- environment;
- time;
- actor or automation;
- feature flags;
- result and rollback.

History turns “something changed” into an actionable investigation.

---

## Release version

Expose a release identity safely:

```text
UI build version
API version
deployment timestamp
commit or artifact identifier
```

It helps correlate errors, performance, support reports, and rollbacks.

---

## Release correlation

Telemetry should connect:

```text
user session → route → release → request → error / performance event
```

Do not collect identifying data unnecessarily. Use bounded, privacy-aware correlation IDs.

---

## Deployment strategies

Common strategies include:

- rolling;
- blue-green;
- canary;
- feature-flagged release;
- full replacement with fast rollback.

Select based on compatibility, traffic, data migration, and operational capability.

---

## Rolling deployment

Replace instances or assets gradually.

During the transition, old and new versions may coexist.

Ensure:

- API compatibility;
- shared asset availability;
- session behavior;
- migration safety;
- observability by version.

---

## Backward compatibility during deployment

For a period, support:

```text
old client ↔ current server
new client ↔ current server
```

Long-lived browser tabs, cached assets, service workers, and delayed requests make compatibility a real requirement.

---

## Blue-green deployment

```text
blue = current
green = new
traffic switch → green
```

It can enable fast switching and rollback.

Costs include duplicate capacity, data compatibility, and confidence that the inactive environment is genuinely ready.

---

## Blue-green trade-offs

Consider:

- database and API state;
- cache warmth;
- background jobs;
- live connections;
- asset references;
- traffic switching and rollback timing.

Switching traffic does not undo side effects already performed by the new version.

---

## Canary release

Expose a release to a small cohort and compare:

- errors;
- performance;
- task completion;
- support signals;
- conversion or domain outcomes.

Canaries require meaningful cohort identity and enough traffic to observe signal.

---

## Release strategy versus feature strategy

```text
release strategy → how code is delivered
feature strategy → who can see or use behavior
```

A release can ship code behind a flag.

A canary can expose a release to a cohort.

Do not treat the mechanisms as interchangeable.

---

## Feature flags are operational controls

Flags can support:

- gradual rollout;
- experiments;
- kill switches;
- migration paths;
- permission-aware presentation.

Each flag needs an owner, purpose, lifecycle, and removal plan.

---

## Feature flags are not just booleans

A flag may depend on:

- user or account;
- percentage cohort;
- environment;
- route;
- experiment assignment;
- release version;
- server-side policy.

Use a clear evaluation model and keep the result observable.

---

## Vendor-neutral flag APIs

```ts
if (flags.isEnabled("newCatalogue")) {
  renderNewCatalogue();
}
```

Keep product code dependent on a small capability interface rather than one vendor's SDK throughout the application.

---

## Flag evaluation location

Flags may evaluate:

```text
server → secure and consistent, request-time
client → flexible, but value may be visible and stale
edge   → close to user, operationally constrained
```

Choose based on security, consistency, latency, and rollout needs.

---

## Feature flags are not authorization

```tsx
{flags.isEnabled("delete-flow") && <DeleteButton />}
```

This controls exposure or experience.

The server must still authorize the delete operation.

---

## Flag categories

```text
release flag     → safely expose unfinished code
operational flag → disable or tune a capability
experiment flag  → assign variants and measure
permission flag  → reflect access, never enforce alone
```

Different categories need different owners, lifetimes, and audit rules.

---

## Flag lifecycle

```text
create → rollout → measure → complete or remove
```

If a flag remains after its decision is complete, it becomes permanent branching complexity.

---

## Flag debt

Old flags create:

- dead paths;
- extra tests;
- confusing support behavior;
- inconsistent analytics;
- migration risk.

Track flag removal like technical debt with an owner and due condition.

---

## Kill switches

A kill switch disables a harmful or expensive capability quickly.

It should have:

- safe fallback;
- owner;
- access control;
- audit trail;
- test coverage;
- clear recovery process.

A kill switch is useful only if operators can trust it under pressure.

---

## Rollback

Rollback restores a previous known release or behavior.

It requires:

- an identifiable artifact;
- compatible data and APIs;
- deployment access;
- tested procedure;
- observability to confirm recovery.

Rollback is a normal safety mechanism, not an admission of failure.

---

## Rollback must be practiced

A document is not evidence that rollback works.

Rehearse:

- who decides;
- what command or action occurs;
- which version returns;
- how flags change;
- what users experience;
- how verification confirms recovery.

Practice reveals missing access, compatibility, and monitoring assumptions.

---

## Database and API compatibility

A frontend rollback may meet:

- a changed API;
- a migrated schema;
- a new required field;
- an invalidated cache;
- an incompatible service worker.

Use expand-and-contract changes and backward-compatible periods where rollback matters.

---

## Rollback versus forward fix

```text
rollback    → restore known behavior quickly
forward fix → repair current release without reverting
```

Choose based on blast radius, data effects, detection certainty, and fix confidence.

---

## Observability

Observability asks whether internal system state can be understood from emitted evidence.

For frontend systems, evidence can include:

- errors;
- performance events;
- network failures;
- route transitions;
- release identity;
- user journey markers;
- feature-flag context.

---

## Monitoring versus observability

```text
monitoring   → known signals and expected thresholds
observability → investigate unexpected states from evidence
```

You need both:

- dashboards and alerts for known failure;
- logs, traces, context, and exploration for unfamiliar failure.

---

## Three traditional telemetry signals

```text
logs    → discrete events and context
metrics → aggregated measurements
traces  → journey across operations and services
```

Frontend observability adapts these signals to browser privacy, lifecycle, and network constraints.

---

## Logs

Useful frontend logs are:

- structured;
- bounded;
- correlated to release and journey;
- privacy-aware;
- actionable.

Do not turn the browser console into a production data lake.

---

## Browser console is not production observability

Console output can disappear because:

- the user closes the page;
- the browser filters it;
- no one can access the user's console;
- context is incomplete;
- sensitive data was logged.

Send carefully designed events to a controlled telemetry system when investigation requires it.

---

## Metrics

Frontend metrics can include:

- error rate;
- route load time;
- Web Vitals;
- interaction timing;
- request failure rate;
- feature adoption;
- queue depth or sync status.

Define units, aggregation, segment, and action before collecting a metric.

---

## High cardinality

Values such as raw URLs, user IDs, or arbitrary error messages can create too many metric dimensions.

Prefer bounded labels:

```text
route_template=/products/:id
error_kind=validation
release=2026.09.24
```

Keep detailed context in traces or sampled events with privacy controls.

---

## Traces and spans

```text
user journey trace
  ├─ route navigation span
  ├─ API request span
  ├─ render marker
  └─ interaction span
```

Traces connect frontend work with backend and network events.

They are especially useful for slow or distributed journeys.

---

## Frontend tracing has special challenges

The browser has:

- intermittent sessions;
- sampling constraints;
- privacy boundaries;
- offline periods;
- multiple tabs;
- limited background time;
- user-controlled execution.

Design telemetry that remains useful without assuming server-like process lifetime.

---

## OpenTelemetry

OpenTelemetry provides a vocabulary and instrumentation approach for traces, metrics, and logs.

Browser support and semantic coverage continue to evolve.

Use it as an interoperability tool, not a promise that every frontend detail is automatically standardized.

---

## Real User Monitoring revisited

RUM should connect:

```text
release + route + segment + journey + metric
```

Collect enough context to act while avoiding unnecessary personal or form data.

---

## Error monitoring

Error monitoring should capture:

- error type and message;
- stack with private source maps;
- release identity;
- route and operation;
- browser context;
- breadcrumbs;
- safe user and feature context.

Group similar failures so teams can prioritize rather than count noise.

---

## Global error handlers

Global handlers can catch unexpected failures and report them.

They should not:

- hide the failure without a recovery UI;
- send secrets;
- duplicate every error repeatedly;
- replace local error boundaries;
- create a false sense that all errors are observable.

---

## Source maps in production monitoring

Source maps make minified errors actionable.

Prefer private upload to the error-monitoring system rather than public deployment when exposure is not needed.

Tie maps to exact release artifacts.

---

## Error grouping

Group by stable cause signals:

- error type;
- normalized message;
- stack location;
- operation;
- release.

Avoid grouping all failures into one generic event or splitting one bug into thousands of dynamic messages.

---

## Error rate needs context

Define:

```text
errors / meaningful sessions
errors / requests
errors / route visits
```

An error count alone does not tell whether users are affected more or fewer.

---

## Network error monitoring

Capture categories such as:

- offline;
- timeout;
- DNS or connection;
- CORS;
- 401/403;
- 404;
- 429;
- 5xx;
- schema failure;
- cancellation.

Different categories need different owners and actions.

---

## Client versus server error

```text
client error → invalid state, rendering, browser boundary
server error → API, infrastructure, authorization, domain failure
```

The same user-visible failure may require evidence from both sides.

Correlate requests and releases safely.

---

## User context without oversharing

Useful context might be:

- anonymous session ID;
- account tier or role category;
- route template;
- release;
- feature flag assignment.

Avoid raw form values, tokens, passwords, private content, and unnecessary identity data.

---

## Breadcrumbs

Breadcrumbs can record a bounded sequence such as:

```text
route opened → filter changed → request failed → retry clicked
```

They should explain the journey without recording sensitive payloads or growing without limit.

---

## Session replay

Session replay has strong privacy and compliance implications.

Define:

- consent;
- masking;
- field exclusion;
- retention;
- access;
- sensitive-route policy;
- sampling.

Debugging value does not override user privacy.

---

## Observability sampling

Sampling controls:

- cost;
- storage;
- user impact;
- signal volume.

Sample ordinary success heavily, but retain enough rare failures and high-severity journeys to investigate them.

---

## Head-based versus tail-based sampling

```text
head-based → decide at trace start
tail-based → decide after seeing outcome and duration
```

Tail sampling can retain slow or failed traces more effectively but requires infrastructure and buffering.

---

## Telemetry has performance cost

Telemetry can add:

- network requests;
- serialization;
- CPU;
- memory;
- storage;
- privacy review.

Instrument critical signals and batch or sample responsibly.

---

## Telemetry buffering and `sendBeacon`

When a page is closing, a beacon can send small analytics or diagnostic payloads without blocking navigation.

It is not a guarantee of delivery and should not carry sensitive or large data.

---

## Observability naming

Use stable names:

```text
catalogue.search.submit
route.catalogue.ready
api.products.failure
feature.new-catalogue.exposed
```

Consistent naming makes dashboards and searches usable across releases.

---

## Operational dashboards

A dashboard should show:

- current release;
- errors and affected sessions;
- performance signals;
- traffic and sample size;
- top routes and operations;
- recent deployments;
- feature flags and cohorts;
- known incidents.

Dashboards should support a decision, not display every metric.

---

## Alerting

An alert should specify:

- condition;
- severity;
- owner;
- response time;
- runbook;
- suppression or grouping;
- recovery signal.

If nobody knows what to do after an alert, it is likely not ready to page.

---

## Alert fatigue

Too many low-value alerts cause operators to ignore high-value ones.

Reduce fatigue with:

- actionable thresholds;
- grouping;
- maintenance windows;
- ownership;
- severity tiers;
- periodic review.

---

## Static thresholds versus anomaly detection

Static thresholds are understandable for known limits.

Anomaly detection can reveal unusual changes relative to baseline.

Both need context, sample size, and a response plan. Sophisticated detection without action is noise.

---

## Service-level indicators

An SLI is a measured aspect of service behavior:

```text
successful route loads / route loads
successful saves / save attempts
acceptable interaction samples / interaction samples
```

Define the numerator, denominator, population, and measurement boundary.

---

## Service-level objectives

An SLO sets a target for an SLI over a time window.

Examples:

- 99.9% of save attempts receive a usable result;
- 95% of catalogue routes meet a journey threshold;
- 99% of releases pass smoke verification.

The objective should be meaningful to users and operators.

---

## Error budgets

```text
allowed unreliability = 1 − objective
```

The budget can inform release pace, reliability investment, and risk acceptance.

It should not be used to justify harming a small but important user group.

---

## Frontend SLOs need care

Frontend metrics are affected by:

- user devices;
- networks;
- browser extensions;
- third-party scripts;
- sampling;
- route and feature mix.

Define scope and segments so the objective reflects what the team can influence and what users experience.

---

## Health checks

A frontend health check may verify:

- static asset availability;
- route response;
- API reachability;
- configuration;
- basic rendering;
- deployment identity.

It should be safe, bounded, and not confuse “server responds” with “user journey works”.

---

## Synthetic production monitoring

Synthetic checks can periodically perform a safe journey:

```text
open → navigate → search → verify result → exit
```

They can detect outages before enough real users generate field data.

---

## Synthetic monitoring trade-offs

Synthetic traffic can:

- miss real device diversity;
- create false confidence;
- add load;
- require test identities;
- fail because of test data rather than product behavior.

Use it alongside RUM and clear ownership.

---

## Deployment verification

After release, check:

- artifact and version;
- critical route;
- authentication;
- API requests;
- assets and service worker;
- errors and performance;
- feature flag exposure.

Deployment is not complete until the user-facing path is verified.

---

## Automatic rollback

Automatic rollback can be appropriate when:

- the signal is reliable;
- the failure threshold is clear;
- the previous artifact is compatible;
- rollback is safe;
- operators are notified;
- a forward fix path exists.

Do not automate a destructive or ambiguous recovery.

---

## Progressive delivery

```text
preview → internal cohort → small percentage → broad rollout
```

At each step, observe release health and decide whether to continue, pause, or revert.

---

## Release cohorts

Cohorts should be:

- stable enough to compare;
- representative enough to reveal risk;
- privacy-aware;
- consistently evaluated;
- identifiable in telemetry.

Random percentage alone is not enough if users move between cohorts unpredictably.

---

## Percentage rollout consistency

Hash a stable identity or account key so a user does not switch variants on every request.

Handle anonymous users and identity changes deliberately.

Document how rollout interacts with caching and server/client evaluation.

---

## Experimentation

Experiments need:

- hypothesis;
- assignment policy;
- primary metric;
- guardrail metrics;
- sample and duration;
- analysis plan;
- stop condition;
- cleanup plan.

An experiment is not a permanent feature flag.

---

## Guardrail metrics

Alongside product outcomes, monitor:

- errors;
- latency;
- accessibility failures;
- support contacts;
- abandonment;
- memory or resource use;
- security signals.

Stop an experiment quickly when it harms users even if the primary metric looks promising.

---

## Maintenance is architecture

The system changes after launch:

- dependencies update;
- browsers change;
- APIs evolve;
- storage persists;
- service workers remain installed;
- teams and ownership change.

Maintenance paths must be designed, not improvised after years of drift.

---

## Dependency maintenance

Maintain dependencies with:

- regular review;
- security triage;
- compatibility testing;
- controlled updates;
- rollback or pinning path;
- removal of unused packages.

Never updating is also a risk strategy, usually a poor one.

---

## Update continuously, not once every three years

Small frequent updates reduce:

- migration distance;
- surprise incompatibilities;
- debugging scope;
- security exposure;
- ownership uncertainty.

They still require review and release discipline.

---

## Dependency update automation

Automation can open updates and run checks.

It should not merge every update blindly.

Use grouping, ownership, security priority, release notes, and artifact/performance review.

---

## Grouping updates

Group compatible low-risk updates to reduce review noise.

Keep risky or architectural updates separate so failures and migration decisions remain understandable.

---

## Security advisories need triage

A vulnerability report needs:

- affected package and path;
- whether the code ships or executes;
- exposure and exploitability;
- available fix;
- mitigation;
- owner and deadline.

Severity score alone does not decide urgency.

---

## Transitive dependencies

You may not import a package directly and still ship it through a dependency chain.

Track:

- why it exists;
- who owns the direct dependency;
- whether it is reachable in production;
- how updates propagate;
- whether it can be removed.

---

## Removing dependencies

Removing a dependency can improve:

- bundle size;
- security surface;
- build time;
- maintenance;
- licensing clarity.

Verify that a platform capability or small local implementation truly meets the requirement before replacing it.

---

## Browser support maintenance

Browser policy affects:

- transformation targets;
- polyfills;
- testing matrix;
- CSS behavior;
- support cost;
- user access.

Do not drop support from global statistics alone if your product serves a meaningful affected population.

---

## Deprecating browser support

Use a planned lifecycle:

```text
measure → announce → warn / document → migrate → remove
```

Provide a clear reason and verify that the release does not strand critical users unexpectedly.

---

## API maintenance

Maintain APIs with:

- backward-compatible additions;
- versioned breaking changes;
- schema monitoring;
- deprecation windows;
- client compatibility;
- migration communication.

Frontend and backend releases often overlap in time.

---

## Schema monitoring

Monitor:

- unknown fields;
- missing required fields;
- invalid types;
- deprecated fields still used;
- response version distribution.

Runtime validation turns silent drift into observable evidence.

---

## Data migration and frontend compatibility

During migration, old clients may still send old shapes.

Use additive changes, compatibility periods, and server-side normalization where rollback and long-lived clients matter.

---

## Local storage migration

Persisted client state needs:

- version;
- schema validation;
- migration path;
- reset behavior;
- identity scope;
- failure handling.

Never assume all users have the current local schema.

---

## Service-worker maintenance

Service workers can outlive deployments.

Maintain:

- cache versioning;
- activation policy;
- update notification;
- old client compatibility;
- cache cleanup;
- offline data migration.

The installed worker is part of the deployed client population.

---

## The stale-client problem

Users may keep a tab open while a new release ships.

The old client may call:

- a changed API;
- a removed route;
- an incompatible event;
- an old asset path.

Design compatibility and update behavior for long-lived sessions.

---

## Update notification

An update message should explain:

- what changed;
- whether current work is safe;
- when reload is appropriate;
- whether the user can defer;
- what happens to drafts and connections.

Do not reload unexpectedly while the user is editing important data.

---

## Technical debt

Debt is the future cost of a current shortcut, including:

- missing tests;
- unsupported dependencies;
- unclear ownership;
- stale flags;
- undocumented platform behavior;
- brittle deployment assumptions.

Debt is not automatically bad; unmanaged debt is.

---

## Debt register

Track:

- debt item;
- user or team impact;
- trigger for action;
- owner;
- risk;
- estimated effort;
- expiry or review date.

An explicit register turns vague concern into prioritizable work.

---

## Maintenance budget

Reserve capacity for:

- dependency updates;
- browser support;
- observability changes;
- flag cleanup;
- API migration;
- service-worker maintenance;
- refactoring and test improvement.

If maintenance has no budget, it will compete with emergencies.

---

## End-of-life policy

Define how the system retires:

- old browser versions;
- APIs;
- packages;
- feature flags;
- service-worker caches;
- preview environments;
- telemetry schemas.

Retirement is part of lifecycle architecture.

---

## Ownership and runbooks

A runbook should state:

- what signal indicates the problem;
- how to confirm it;
- immediate mitigation;
- rollback or kill switch;
- communication path;
- recovery verification;
- follow-up owner.

Runbooks reduce decision load during incidents.

---

## Incident response lifecycle

```text
detect → triage → mitigate → communicate → recover → learn
```

Keep the user impact and current system state visible throughout the incident.

---

## Blameless learning

Post-incident review should ask:

- what conditions made the failure possible?
- which signal was missing or late?
- which recovery step worked or failed?
- what system change reduces recurrence?

The goal is stronger systems, not individual blame.

---

## Post-incident actions

Actions should be:

- specific;
- owned;
- prioritized;
- measurable;
- connected to the failure;
- reviewed for completion.

“Be more careful” is not a system improvement.

---

## Maintenance metrics

Useful signals include:

- mean time to recovery;
- deployment failure rate;
- rollback time;
- dependency age;
- stale flag count;
- unresolved vulnerability age;
- test and build feedback time;
- observability coverage.

Do not turn one metric into a target that damages the system.

---

## Deployment frequency is not quality by itself

Frequent deployment can indicate healthy delivery or uncontrolled churn.

Pair it with:

- change failure rate;
- recovery time;
- user impact;
- reliability and performance;
- maintenance health.

---

## Mean time to recovery

MTTR asks how quickly the system returns to an acceptable state after failure.

Improve it through:

- detection;
- clear ownership;
- safe rollback;
- kill switches;
- runbooks;
- practiced communication.

Prevention matters, but recovery is part of reliability.

---

## Observability completes testing

Tests cover known scenarios.

Production observability reveals:

- unknown combinations;
- real devices and networks;
- integration drift;
- deployment-specific failures;
- user behavior outside assumptions.

Use production evidence to improve the next test strategy.

---

## The production feedback loop

```text
test hypothesis
  → release safely
  → observe real behavior
  → investigate differences
  → improve code, tests, or architecture
```

Production is not the end of engineering; it is a source of evidence.

---

## Privacy and compliance

Telemetry and debugging must respect:

- data minimization;
- consent;
- retention;
- access control;
- regional requirements;
- deletion and subject rights;
- sensitive fields.

Operational visibility cannot be purchased by recording everything.

---

## Do not record form contents by default

Forms can contain:

- passwords;
- financial data;
- health information;
- personal identifiers;
- private business content.

Mask or exclude inputs and inspect telemetry payloads before production use.

---

## Session replay needs stronger governance

Replay can show real failures, but may capture private content and interactions.

Define:

- masking defaults;
- consent and regional policy;
- sensitive route exclusions;
- retention and access;
- sampling and incident use.

---

## Analytics versus observability

```text
analytics    → product behavior and outcomes
observability → system health and failure investigation
```

They may share infrastructure, but have different purpose, privacy, retention, and ownership.

---

## Product versus operational metrics

| Product | Operational |
|---|---|
| conversion | error rate |
| task completion | latency |
| retention | availability |
| feature adoption | deployment health |

Connect them carefully without assuming one causes the other.

---

## Business-aware observability

A useful release dashboard can connect:

```text
release → route → technical signal → user task → business effect
```

This helps teams prioritize an outage that affects a critical workflow over a noisy low-impact error.

---

## Release dashboard example

Show:

- current and previous release;
- deployment status;
- error and performance deltas;
- critical journey success;
- flag cohorts;
- open incidents;
- rollback readiness.

Keep the dashboard decision-oriented.

---

## Deployment health window

After release, observe a defined window with:

- expected traffic;
- known baseline;
- key route metrics;
- error and support signals;
- feature exposure;
- rollback threshold.

Do not declare health from one successful smoke test alone.

---

## Low-traffic products

Sparse traffic makes automatic detection harder.

Use:

- longer observation windows;
- synthetic checks;
- targeted smoke tests;
- manual review;
- confidence-aware thresholds;
- support and user reports.

Low volume does not mean low importance.

---

## Maintenance and architecture decisions

Prefer architectures with:

- understandable upgrade paths;
- supported tooling;
- observable boundaries;
- reversible deployment;
- clear ownership;
- proportionate operational cost.

The most elegant architecture is not useful if nobody can maintain or recover it.

---

## Boring technology has value

Mature, documented, well-understood tools can reduce:

- operational surprise;
- onboarding cost;
- incident ambiguity;
- upgrade risk;
- dependence on one expert.

Novelty should solve a real constraint, not create one.

---

## Upgrade path is a selection criterion

Before adopting a tool, ask:

- how is it upgraded?
- how are breaking changes announced?
- can output be inspected?
- is ownership clear?
- can the system roll back?
- what happens when the maintainer changes?

Current features are only one part of technology choice.

---

## Avoid undocumented internal platforms

An internal platform without:

- public contracts;
- documentation;
- release notes;
- support ownership;
- migration path;
- observability;

becomes a hidden dependency and a bottleneck for every product team.

---

## Operational readiness review

Review:

```text
delivery / rollback / observability / performance
ownership / dependencies / privacy / support
```

The checklist should be proportional to user impact and system complexity.

---

## Production readiness is proportional

A small static page and a financial workflow need different readiness depth.

Scale review according to:

- user harm;
- data sensitivity;
- change frequency;
- dependency count;
- availability expectations;
- recovery cost.

Proportionate does not mean careless.

---

## Practical lab: Delivery, Observability, and Rollback Loop

Design and rehearse a safe frontend release from commit to deployment, observation, rollback, and cleanup.

The practical makes the delivery artifact, release identity, flags, telemetry, alerts, and recovery path explicit.

---

## Practical stages 1–6: build and deploy safely

1. Create the CI pipeline.
2. Add parallel jobs.
3. Produce a versioned artifact.
4. Create a preview deployment.
5. Protect production.
6. Add deployment concurrency.

Verification: the tested artifact is the deployed artifact.

---

## Practical stages 7–13: release control

7. Expose the release version.
8. Add a preview smoke test.
9. Design a canary rollout.
10. Add a release flag.
11. Give the flag an owner.
12. Create a kill switch.
13. Remove a completed flag.

Feature flags do not act as authorization.

---

## Practical stages 14–20: observe production

14. Add error monitoring.
15. Upload source maps privately.
16. Add RUM.
17. Add a custom journey metric.
18. Create an operational dashboard.
19. Define alerts.
20. Add synthetic production monitoring.

Every alert needs an owner and an operational response.

---

## Practical stages 21–27: recovery and maintenance

21. Create a rollback procedure.
22. Simulate compatibility failure.
23. Create a frontend runbook.
24. Create a dependency maintenance workflow.
25. Triage a vulnerability.
26. Remove one dependency.
27. Test an upgrade path.

Rollback is tested rather than merely documented.

---

## Practical stages 28–32: long-lived clients and SLOs

28. Simulate a long-lived client.
29. Add update notification.
30. Create a debt register.
31. Design SLOs.
32. Create the final production architecture diagram.

Include stale clients, flags, service workers, privacy, and support ownership.

---

## Practical extension: frontend runbook

Write a short runbook covering:

```text
detection → triage → mitigation → rollback → communication → follow-up
```

Include commands, owners, dashboards, thresholds, and the evidence that confirms recovery.

---

## Try this yourself

For the next release, write:

```text
artifact identity:
deployment strategy:
rollback trigger:
critical signal:
alert owner:
kill switch:
privacy constraint:
maintenance follow-up:
```

If any field is blank, the release loop has an unexamined assumption.

---

## Troubleshooting guide

| Symptom | Likely cause |
|---|---|
| CI passes but deployed app fails | Tested artifact differs from deployed artifact |
| Rollback restores old code but breaks API | Compatibility window was not designed |
| Alerts fire constantly | Thresholds lack context or ownership |
| Errors cannot be debugged | Release identity or private source maps missing |
| Feature flag remains forever | Lifecycle and owner were never defined |
| Telemetry is expensive or unsafe | Payload, sampling, and privacy policy are weak |
| Users keep stale behavior | Long-lived clients and service-worker updates ignored |
| Dependency update is frightening | Updates were deferred instead of maintained continuously |
| Incident response is slow | Runbook and rollback were not practiced |

---

## Completion checklist

- [ ] CI produces a reproducible, identifiable artifact;
- [ ] the same artifact is promoted across environments;
- [ ] production access and secrets use least privilege;
- [ ] releases can be canaried, flagged, killed, or rolled back;
- [ ] telemetry connects release, route, journey, and failure;
- [ ] alerts have owners and runbooks;
- [ ] SLOs and error budgets are meaningful and segmented;
- [ ] dependencies, browsers, APIs, storage, and workers have maintenance paths;
- [ ] telemetry respects privacy and data minimization;
- [ ] rollback and recovery have been rehearsed.

---

## Misconceptions to leave behind

| Misconception | Better mental model |
|---|---|
| CI means one hosted test command | CI is clean verification and artifact production |
| Delivery means every commit deploys | Delivery keeps a safe release ready |
| Passing tests makes deployment safe | Artifact, environment, integration, and recovery also matter |
| Staging is production without users | Environments have different purposes and gaps |
| Preview replaces code review | It provides deployed evidence, not design judgment |
| Feature flags are authorization | The server still enforces permissions |
| Flags can stay forever | Flags need ownership and removal |
| Rollback is failure | Rollback is a normal safety mechanism |
| Observability means logs | Logs, metrics, traces, errors, and context work together |
| More telemetry is always better | Telemetry has cost, privacy, and signal limits |
| Every error should page someone | Alerts require actionable owners and thresholds |
| Dependency updates should be automatic | Automation needs review, grouping, and risk triage |
| Users refresh after deployment | Long-lived clients require compatibility and update policy |
| Maintenance is separate from architecture | Lifecycle and recovery are architectural properties |

---

## The chapter in one sentence

> **Ship reproducible artifacts through a controlled release loop, observe real user impact, recover deliberately, and budget continuously for maintenance.**

---

## Next: Chapter 18

The next chapter will build on production architecture with:

- final system integration;
- architectural decision records;
- capstone planning;
- cross-cutting quality and delivery review;
- a complete front-end platform blueprint.

---

## Questions

If the next release harms users, how will you identify the exact artifact, detect the impact, reduce exposure, roll back safely, and learn what the system failed to tell you?

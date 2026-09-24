---
title: "Learning topics"
description: "What you will learn in Modern Front-End Engineering, with scope, outcomes, and links to chapters and practicals."
type: docs
---

Modern Front-End Engineering develops basic web knowledge into an understanding of how to build, evaluate, and maintain front-end applications. This guide explains the book’s learning topics, expected outcomes, and depth of coverage.

You should already know basic HTML and CSS, JavaScript variables, conditions, loops, functions, arrays, and objects, and basic command-line usage. Professional front-end experience is not assumed.

## How to use this guide

Choose a topic below, read its chapter, and use the linked practical brief to apply it. For the full progression, [read the book in order](../book/). For teaching materials, [browse the lecture slides](../slides/).

The goal is broad, solid engineering understanding. Some subjects are developed far enough to use; others are introduced so you can compare approaches and decide where to study further. Mentioning a technology does not imply complete coverage or mastery.

## Explore the topics

1. [Browser internals](#topic-1)
2. [Semantic HTML & accessibility](#topic-2)
3. [Responsive CSS](#topic-3)
4. [Modern JavaScript](#topic-4)
5. [TypeScript & runtime validation](#topic-5)
6. [Component architecture](#topic-6)
7. [Reactivity & rendering](#topic-7)
8. [State, routing & forms](#topic-8)
9. [APIs & caching](#topic-9)
10. [Real-time & offline systems](#topic-10)
11. [Rendering strategies](#topic-11)
12. [Development tooling](#topic-12)
13. [Front-end security](#topic-13)
14. [Design systems & scaling](#topic-14)
15. [Performance engineering](#topic-15)
16. [Front-end testing](#topic-16)
17. [Delivery & observability](#topic-17)
18. [Architectural decisions](#topic-18)

## 1. Browser internals {#topic-1}

Understand the browser as the runtime that makes an interface work. Follow a page from resource loading through DOM and CSSOM construction, layout, painting, and interaction.

**What you should be able to do:** Explain how the event loop schedules work, identify render-blocking resources, and use developer tools to investigate what the browser actually does.

[Read Chapter 1]({{< relref "/book/Chapter_01_The_Modern_Web_Platform_and_Browser_Internals.md" >}}) · [Try Practical 01]({{< relref "/playground/practical-01-browser-observation-and-virtual-scroller.md" >}}) · [All topics](#explore-the-topics)

## 2. Semantic HTML & accessibility {#topic-2}

Use HTML to describe meaning and behavior, not just appearance. Connect semantic elements, accessible names, forms, keyboard interaction, and document structure to the ways people navigate an interface.

**What you should be able to do:** Choose native controls before adding ARIA, check keyboard access, and account for language and text direction. Accessibility requires evaluation beyond passing an automated check.

[Read Chapter 2]({{< relref "/book/Chapter_02_Semantic_HTML_Accessibility_Internationalization_and_the_DOM.md" >}}) · [Try Practical 02]({{< relref "/playground/practical-02-accessible-composite-listbox.md" >}}) · [All topics](#explore-the-topics)

## 3. Responsive CSS {#topic-3}

Build layouts that respond to their content and available space. Learn how the cascade, Flexbox, Grid, container queries, custom properties, and logical properties work together.

**What you should be able to do:** Choose a layout technique, explain why a style wins, and organize CSS so a change does not create unexpected effects elsewhere.

[Read Chapter 3]({{< relref "/book/Chapter_03_Modern_CSS_Architecture_and_Layout_Systems.md" >}}) · [Try Practical 03]({{< relref "/playground/practical-03-intrinsic-dashboard.md" >}}) · [All topics](#explore-the-topics)

## 4. Modern JavaScript {#topic-4}

Understand the language mechanisms behind interactive applications: scope, closures, modules, promises, asynchronous functions, and error handling.

**What you should be able to do:** Trace asynchronous work, coordinate requests, handle cancellation and failures, and choose language patterns that make application behavior easier to follow.

[Read Chapter 4]({{< relref "/book/Chapter_04_Modern_JavaScript_and_Asynchronous_Programming.md" >}}) · [Try Practical 04]({{< relref "/playground/practical-04-abortable-event-hub.md" >}}) · [All topics](#explore-the-topics)

## 5. TypeScript & runtime validation {#topic-5}

Use types to express valid states and make data contracts explicit. Work with unions, narrowing, generics, interfaces, and strict checking while recognizing that external data can still violate your assumptions.

**What you should be able to do:** Distinguish compile-time guarantees from runtime validation and place checks where untrusted data enters an application.

[Read Chapter 5]({{< relref "/book/Chapter_05_TypeScript_Runtime_Contracts_and_Safe_Data_Boundaries.md" >}}) · [Try Practical 05]({{< relref "/playground/practical-05-runtime-validated-boundary.md" >}}) · [All topics](#explore-the-topics)

## 6. Component architecture {#topic-6}

Divide interfaces into components with clear responsibilities. Explore composition, communication, reusable behavior, and patterns for separating interaction logic from visual presentation.

**What you should be able to do:** Choose component boundaries and APIs that support reuse without introducing abstractions before they are needed.

[Read Chapter 6]({{< relref "/book/Chapter_06_Component_Driven_Architecture_and_Design_Patterns.md" >}}) · [Try Practical 06]({{< relref "/playground/practical-06-compound-headless-tabs.md" >}}) · [All topics](#explore-the-topics)

## 7. Reactivity & rendering {#topic-7}

Compare how state changes become visible updates. Study React’s rendering model, Vue’s reactive model, derived values, effects, and the ideas behind signals and compiler optimization.

**What you should be able to do:** Reason about update dependencies and side effects. React and Vue illustrate architectural models here; this book does not replace their dedicated framework documentation.

[Read Chapter 7]({{< relref "/book/Chapter_07_Reactivity_and_Rendering_Mechanics.md" >}}) · [Try Practical 07]({{< relref "/playground/practical-07-reactive-computed-graph.md" >}}) · [All topics](#explore-the-topics)

## 8. State, routing & forms {#topic-8}

Give state a deliberate owner and lifetime. Distinguish local, shared, server, URL, and form state, and connect navigation to the information users expect to preserve or share.

**What you should be able to do:** Decide what belongs in a component, a shared store, a cache, or the URL, and design routing and forms around those choices.

[Read Chapter 8]({{< relref "/book/Chapter_08_State_Management_Routing_and_Form_Architecture.md" >}}) · [Try Practical 08]({{< relref "/playground/practical-08-url-driven-catalogue.md" >}}) · [All topics](#explore-the-topics)

## 9. APIs & caching {#topic-9}

Treat communication with a backend as a boundary that can be slow, unavailable, or inconsistent. Cover HTTP, Fetch, REST, request states, mutations, caching, and invalidation, with GraphQL as a comparison.

**What you should be able to do:** Represent loading and failure states explicitly, handle authenticated requests, and explain when cached data becomes stale. GraphQL coverage supports evaluation rather than specialist mastery.

[Read Chapter 9]({{< relref "/book/Chapter_09_Client_Server_Communication_APIs_and_Cache_Management.md" >}}) · [Try Practical 09]({{< relref "/playground/practical-09-cached-api-client.md" >}}) · [All topics](#explore-the-topics)

## 10. Real-time & offline systems {#topic-10}

Consider what happens when data changes remotely or connectivity disappears. Compare polling, server-sent events, WebSockets, browser storage, IndexedDB, service workers, and offline strategies.

**What you should be able to do:** Choose an appropriate communication and persistence approach and reason about recovery and synchronization. These topics introduce important trade-offs rather than every production edge case.

[Read Chapter 10]({{< relref "/book/Chapter_10_Real_Time_Communication_Offline_Systems_and_Client_Persistence.md" >}}) · [Try Practical 10]({{< relref "/playground/practical-10-offline-outbox.md" >}}) · [All topics](#explore-the-topics)

## 11. Rendering strategies {#topic-11}

Compare where and when HTML and application work are produced: client-side rendering, server-side rendering, static generation, and hybrid approaches. Connect hydration, streaming, and server/client components to that choice.

**What you should be able to do:** Explain the effects on initial delivery, interactivity, caching, and operational complexity instead of assuming one rendering strategy is always best.

[Read Chapter 11]({{< relref "/book/Chapter_11_Rendering_Topologies_CSR_SSR_SSG_and_Beyond.md" >}}) · [Try Practical 11]({{< relref "/playground/practical-11-rendering-topology-comparison.md" >}}) · [All topics](#explore-the-topics)

## 12. Development tooling {#topic-12}

Understand the path from source files to a deployable application. Explore package management, Git workflows, Vite and build systems, bundling, code splitting, linting, source maps, and production builds.

**What you should be able to do:** Inspect a module graph, recognize what the build transforms, and make tooling decisions that support reproducible development and useful debugging.

[Read Chapter 12]({{< relref "/book/Chapter_12_Modern_Build_Systems_Development_Tooling_and_Team_Workflows.md" >}}) · [Try Practical 12]({{< relref "/playground/practical-12-module-graph-and-splitting.md" >}}) · [All topics](#explore-the-topics)

## 13. Front-end security {#topic-13}

Recognize trust boundaries in browser applications. Study XSS, CSRF, CSP, CORS, cookies, authentication approaches, dependency risks, and browser-side credential handling.

**What you should be able to do:** Identify unsafe data flows and choose appropriate safeguards. Authentication protocols and advanced browser isolation are introduced for informed evaluation, not as a substitute for specialist security review.

[Read Chapter 13]({{< relref "/book/Chapter_13_Front_End_Security_Authentication_and_Browser_Isolation.md" >}}) · [Try Practical 13]({{< relref "/playground/practical-13-security-boundary-review.md" >}}) · [All topics](#explore-the-topics)

## 14. Design systems & scaling {#topic-14}

Explore how shared code and team boundaries influence architecture. Compare design systems, shared packages, monorepos, and micro-frontends through ownership, coordination, reuse, and deployment needs.

**What you should be able to do:** Explain when shared infrastructure helps and when it adds cost. Micro-frontends, Module Federation, and advanced monorepo architecture are survey topics rather than promised areas of mastery.

[Read Chapter 14]({{< relref "/book/Chapter_14_Scaling_Front_End_Architecture_Design_Systems_Monorepos_and_Micro_Frontends.md" >}}) · [Try Practical 14]({{< relref "/playground/practical-14-design-system-ownership.md" >}}) · [All topics](#explore-the-topics)

## 15. Performance engineering {#topic-15}

Treat performance as an investigation supported by measurement. Connect Core Web Vitals with network activity, JavaScript execution, asset size, caching, memory behavior, and browser profiling.

**What you should be able to do:** Find a bottleneck, choose a targeted intervention, and compare results under meaningful conditions rather than optimizing from intuition alone.

[Read Chapter 15]({{< relref "/book/Chapter_15_Core_Web_Vitals_and_Performance_Engineering.md" >}}) · [Try Practical 15]({{< relref "/playground/practical-15-measured-virtualized-performance.md" >}}) · [All topics](#explore-the-topics)

## 16. Front-end testing {#topic-16}

Choose tests according to the behavior and risk being checked. Compare static analysis, unit, component, integration, end-to-end, accessibility, and visual testing.

**What you should be able to do:** Build a balanced strategy, test observable behavior, and understand what each check can and cannot establish about a user’s experience.

[Read Chapter 16]({{< relref "/book/Chapter_16_Testing_Strategies_for_Resilient_Interfaces.md" >}}) · [Try Practical 16]({{< relref "/playground/practical-16-resilient-integration-suite.md" >}}) · [All topics](#explore-the-topics)

## 17. Delivery & observability {#topic-17}

Follow an application beyond a successful build. Examine CI/CD, preview and production environments, error monitoring, Real User Monitoring, dependency upgrades, and technical debt.

**What you should be able to do:** Plan how to release, observe, recover, and maintain an application, with feedback from production informing subsequent changes.

[Read Chapter 17]({{< relref "/book/Chapter_17_Continuous_Delivery_Observability_and_Maintenance.md" >}}) · [Try Practical 17]({{< relref "/playground/practical-17-delivery-observability-rollback.md" >}}) · [All topics](#explore-the-topics)

## 18. Architectural decisions {#topic-18}

Bring the earlier topics together to compare alternatives against actual requirements. Consider frameworks, state, rendering, styling, networking, and application structure as choices with costs and constraints.

**What you should be able to do:** Record a reasoned decision, state its trade-offs, avoid unnecessary complexity, and identify evidence that would justify revisiting it.

[Read Chapter 18]({{< relref "/book/Chapter_18_Front_End_Architecture_and_Technical_Decision_Making.md" >}}) · [Try Practical 18]({{< relref "/playground/practical-18-architecture-decision-record.md" >}}) · [All topics](#explore-the-topics)

## Where the coverage stops

WebRTC, OAuth/OIDC, GraphQL, service workers, micro-frontends, Module Federation, cross-origin isolation, and advanced monorepo architecture are introduced to explain the problems they address and their major trade-offs. Plan further study and project-specific validation before relying on specialist expertise in those areas.

React and Vue are used for architectural comparisons and representative examples. Neither is taught as a complete framework reference.

[Start reading](../book/) · [Browse practicals](../playground/) · [Back to the homepage](../)

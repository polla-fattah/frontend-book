---
title: "Component-Driven Architecture & Design Patterns"
description: "Chapter 6: find component boundaries, design stable APIs, compose behavior, and organize front-end systems by responsibility."
book_number: "6"
weight: 7
---

# Component-Driven Architecture & Design Patterns

Make responsibility visible

**Chapter 6**

Polla Fattah

---

## Today's goal

Learn to decide where a component should begin and end.

We will connect:

- responsibility and reasoning boundaries;
- inputs, outputs, props, events, and slots;
- controlled and uncontrolled state;
- compound and headless components;
- context and dependency injection;
- reuse, abstraction, and duplication;
- feature, layer, and domain-oriented organization;
- accessibility, performance, internationalization, and security.

---

## By the end of today you can

- identify a coherent component responsibility;
- distinguish a component boundary from a state boundary;
- design intent-oriented public APIs;
- choose controlled or uncontrolled ownership deliberately;
- compose behavior without forcing styling decisions;
- use context or injection without hiding dependencies;
- recognize oversized and over-fragmented components;
- extract components in a safe sequence;
- organize a front-end by feature, layer, or domain;
- refactor a catalogue into a maintainable component architecture.

---

## The central principle

> **A component should exist because it owns a coherent responsibility—not merely because some markup can be extracted into another file.**

The file boundary is an implementation detail.

The responsibility boundary is the architecture.

---

## The chapter's progression

```text
complex interface
  → identify responsibilities
  → find boundaries
  → define inputs and outputs
  → compose components
  → decide state ownership
  → share dependencies carefully
  → organize by feature, domain, or system
```

Every step reduces accidental coupling while preserving understandable flow.

---

## Why components exist

Consider a catalogue page containing:

- navigation;
- search and filters;
- product cards;
- pagination;
- basket actions;
- loading and error states;
- keyboard behavior and analytics.

A single function can render it.

That does not mean one function is a good unit of reasoning.

---

## Components reduce the amount we understand at once

```text
CataloguePage
├─ SearchControls
├─ FilterPanel
├─ ProductGrid
│  └─ ProductCard
│     ├─ Price
│     ├─ StockStatus
│     └─ AddToCartButton
└─ Pagination
```

If price formatting changes, we should not need to understand pagination, filters, and cart state at the same time.

---

## Reuse is useful, but not required

```text
AnnualBudgetApprovalPanel
```

It may appear once and still deserve a component because it owns:

- a coherent domain responsibility;
- substantial behavior;
- a meaningful state model;
- a natural testing boundary.

Reuse is one reason to create a component. Responsibility is stronger.

---

## Isolation is encapsulation

A date picker can expose:

```text
value
onChange
disabled
```

while hiding:

- calendar-grid generation;
- month navigation;
- keyboard behavior;
- focus management;
- date-cell implementation.

The caller gets what it needs without controlling every internal detail.

---

## Testing boundaries follow behavior

A date picker can be tested for:

- selected-date behavior;
- keyboard navigation;
- disabled dates;
- accessible labels.

The surrounding page should not have to reproduce every internal interaction to test the date picker.

Test where behavior and risk are concentrated—not merely where files happen to exist.

---

## Ownership makes team work clearer

A useful component boundary can make it clear:

- which team owns the behavior;
- which API is stable;
- which implementation is private;
- which changes require coordination.

Architecture is also communication between people, not only organization for the compiler.

---

## Bad extreme: one giant component

```text
CataloguePage
  search state
  filter state
  fetch logic
  URL synchronization
  product rendering
  cart events
  modal behavior
  analytics
  keyboard handling
  responsive layout
```

Typical symptoms:

- everything can reach everything;
- a small change creates a large regression surface;
- tests require excessive setup;
- state ownership is ambiguous.

---

## Bad extreme: component explosion

```text
Page
└─ Section
   └─ Wrapper
      └─ Row
         └─ Text
            └─ Label
```

Small is not automatically good.

Too many trivial components increase navigation cost, obscure control flow, and make a simple change require a tour of the repository.

---

## Find boundaries by asking five questions

1. What changes together?
2. What owns the behavior?
3. What represents one domain concept?
4. What is genuinely reusable?
5. What should remain private?

The answers should describe responsibility, not just the shape of the markup.

---

## What changes together?

If a visual structure, its interaction rules, and its tests always change together, they may belong in one component.

If a value, layout, and data-fetching policy change independently, forcing them into one unit creates coupling.

Change patterns are evidence for boundaries.

---

## What owns the behavior?

```text
SearchInput       owns input interaction
SearchController  owns query coordination
ProductGrid       owns product layout
ProductCard       owns product presentation
```

Do not move state merely because a child renders the element.

The owner is the unit that makes the decision and coordinates its consequences.

---

## What represents one domain concept?

```text
ProductCard
ApprovalPanel
ShippingAddress
LectureNavigation
```

Domain concepts are often stronger boundaries than generic visual fragments.

They give the API meaningful vocabulary and give tests a clear subject.

---

## What should remain private?

Not every internal helper needs to become a public component.

Keep implementation details local when they:

- have no independent responsibility;
- are used in one place;
- would expose unstable structure;
- make the public API harder to understand.

Local components are valid architecture.

---

## A deliberately monolithic shape

```tsx
function CataloguePage() {
  const [query, setQuery] = useState("");
  const [filters, setFilters] = useState(defaultFilters);
  const { data, loading, error } = useProducts(query, filters);

  return (
    <main>
      {/* search, filters, cards, pagination, errors, and cart */}
    </main>
  );
}
```

The problem is not that it renders JSX.

The problem is that unrelated responsibilities have no visible boundaries.

---

## First refactoring: stable visual responsibilities

```tsx
function CataloguePage() {
  return (
    <main>
      <SearchControls />
      <FilterPanel />
      <ProductGrid />
      <Pagination />
    </main>
  );
}
```

Extract the stable responsibilities first.

Keep coordination in the parent until the data and ownership decisions are understood.

---

## A component boundary is not necessarily a state boundary

```text
ProductCard       renders one product
CataloguePage     owns selected products and filters
CartStore         owns basket state
```

A child can be a useful rendering boundary while state remains higher in the tree.

Do not force every component to own every value it displays.

---

## Inputs and outputs define the contract

```text
outside values → component → visible result / intent
     props      →          → events, callbacks, emitted events
```

The public contract should be smaller and more stable than the implementation.

---

## Props describe data and capabilities

```tsx
type ProductCardProps = {
  product: Product;
  onAddToCart: (productId: ProductId) => void;
  isAdded: boolean;
};
```

Good props answer:

- what does this component need?
- what decisions can it request?
- what state is intentionally owned elsewhere?

---

## Vue props and events express the same boundary

```vue
<ProductCard
  :product="product"
  :is-added="isAdded"
  @add-to-cart="addToCart"
  />
```

The syntax differs from React.

The architectural question is the same: what enters, what leaves, and who owns the decision?

---

## Callbacks and events should communicate intent

Prefer:

```text
onAddToCart(productId)
onSearch(query)
onApprove(requestId)
```

Over exposing implementation details:

```text
onButtonClick(event)
setInternalCartState(nextState)
```

Intent-oriented APIs let the component change its internal markup without breaking callers.

---

## Children and slots enable composition

```tsx
<Panel>
  <Panel.Header>Filters</Panel.Header>
  <Panel.Body>
    <FilterForm />
  </Panel.Body>
</Panel>
```

The panel owns structure and semantics.

The caller supplies content that varies.

---

## Named slots make variation explicit

```vue
<ProductCard>
  <template #badge>
    <StockStatus />
  </template>
  <template #actions>
    <AddToCartButton />
  </template>
</ProductCard>
```

Named composition points communicate where variation belongs without adding a boolean prop for every possibility.

---

## Composition over inheritance

```text
Card
├─ Header
├─ Body
└─ Actions
```

Compose small capabilities and content rather than building a deep inheritance hierarchy.

Composition keeps variation near the caller and avoids base classes accumulating unrelated assumptions.

---

## Wrapper components should add a reason

A wrapper is valuable when it adds:

- semantics;
- layout responsibility;
- accessibility behavior;
- a state boundary;
- a stable composition API.

If it only forwards every prop and renders one child unchanged, it may be navigation cost without architectural value.

---

## Controlled components: the parent owns the value

```tsx
<SearchInput
  value={query}
  onChange={setQuery}
  placeholder="Search products"
/>
```

The component renders and reports interaction.

The parent owns the source of truth and can synchronize it with URL state, data fetching, or another control.

---

## Uncontrolled components: the component owns the value

```tsx
<SearchInput
  defaultValue=""
  onSubmit={submitSearch}
/>
```

The component manages its internal editing state.

This can simplify local interactions when the parent does not need every intermediate value.

---

## Controlled versus uncontrolled is an ownership decision

```text
Need synchronization outside? → controlled
Need only the final result?    → uncontrolled
Need both?                    → define a deliberate bridge
```

Neither mode is universally better.

Choose based on who must make decisions about the state.

---

## Avoid half-controlled APIs

```tsx
<Tabs value={value} defaultValue="overview" onChange={setValue} />
```

What wins if `value` is absent? What happens when it appears later?

Ambiguous ownership creates warnings, stale state, and surprising transitions.

Use separate APIs or document the controlled/uncontrolled contract precisely.

---

## Good component APIs minimize invalid combinations

Instead of:

```text
disabled + loading + error + success + compact + outline + danger + iconOnly
```

Model meaningful states and relationships.

```ts
type SubmitButtonProps =
  | { status: "ready"; onSubmit: () => void }
  | { status: "loading" }
  | { status: "error"; message: string; onRetry: () => void };
```

---

## Keep the public surface small and stable

```text
public props / events / slots
            ↓
private state and helpers
```

Every public prop is a promise.

Every public event is a dependency for callers.

Expose the smallest contract that supports the component's responsibility.

---

## Compound components share a local vocabulary

```tsx
<Tabs>
  <Tabs.List>
    <Tabs.Tab value="overview">Overview</Tabs.Tab>
    <Tabs.Tab value="reviews">Reviews</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel value="overview">...</Tabs.Panel>
  <Tabs.Panel value="reviews">...</Tabs.Panel>
</Tabs>
```

The pieces are separate in markup but belong to one conceptual system.

---

## Why compound components can help

They can provide:

- readable structure;
- explicit composition points;
- shared state without prop repetition;
- a constrained vocabulary;
- flexible placement of tabs and panels.

The API communicates the relationship between the parts.

---

## The cost of compound components

They also add:

- hidden coordination rules;
- context or injection dependencies;
- more concepts to document;
- more invalid combinations to prevent;
- debugging work when pieces are used incorrectly.

Use the pattern when the relationship is real and repeated—not because the API looks advanced.

---

## Headless components separate behavior from styling

```text
headless behavior
  keyboard rules
  selection state
  ARIA relationships
  focus management
          ↓
consumer-owned markup and styles
```

A headless component supplies interaction logic without imposing a visual design.

---

## Why headless UI exists

It is useful when teams need:

- shared accessibility behavior;
- different visual systems;
- consistent keyboard interaction;
- application-specific layout;
- reusable state machines.

The abstraction is behavioral, not merely visual.

---

## Dependency sharing: explicit props first

```tsx
<ProductCard
  product={product}
  currency={currency}
  locale={locale}
  onAddToCart={onAddToCart}
/>
```

Explicit inputs make dependencies visible and make the component easy to render in isolation.

Prop passing becomes a problem only when it is genuinely burdensome or crosses unrelated layers repeatedly.

---

## React context shares a local dependency

```tsx
const TabsContext = createContext<TabsContextValue | null>(null);

function useTabsContext() {
  const context = useContext(TabsContext);
  if (!context) throw new Error("Tabs parts must be inside Tabs");
  return context;
}
```

Context can keep compound parts coordinated without repeating the same props at every level.

---

## Vue provide/inject expresses the same idea

```ts
provide(TabsKey, {
  selected,
  select,
});

const tabs = inject(TabsKey);
```

The framework syntax changes; the architectural trade-off remains: the dependency is less visible at the call site.

---

## Context is not automatically better than props

Context can:

- hide where a value comes from;
- make isolated rendering harder;
- widen a component's implicit dependency surface;
- cause broad updates when the value changes.

Use it for a real shared relationship, not just to avoid writing one more prop.

---

## Dependency injection makes variation explicit at setup

```ts
type ProductRepository = {
  list(): Promise<Product[]>;
};

function createCatalogue(repository: ProductRepository) {
  return { load: () => repository.list() };
}
```

The feature depends on a capability, not on one concrete network implementation.

---

## Why dependency injection helps

It can improve:

- testing with fakes;
- environment-specific adapters;
- separation of domain behavior from transport;
- migration between implementations.

The dependency remains a design decision rather than a hidden import.

---

## Dependency injection can also be overused

If every helper receives a container with dozens of services, the dependency graph becomes harder to understand.

Inject the smallest capability needed.

Prefer a direct import for a stable, genuinely global constant when injection adds no meaningful variation.

---

## Reusable UI components versus application components

```text
Reusable: Button, Dialog, Tabs, Field
Application: ProductCard, CatalogueFilters, ApprovalPanel
```

Reusable UI components should avoid application-specific assumptions.

Application components should speak the domain language and may coordinate several reusable primitives.

---

## Reuse has levels

```text
one feature
  → one application
  → multiple products
  → design system / package
```

The wider the reuse boundary, the more expensive the public contract becomes.

Do not design a global package API for a problem that only exists in one feature.

---

## Premature abstraction freezes assumptions

An abstraction created before the second use often encodes:

- accidental naming;
- the first layout's constraints;
- one feature's state model;
- props that do not generalize.

Wait until the shared behavior and variation are understood.

---

## Duplication can be cheaper than the wrong abstraction

Two similar components may differ in:

- ownership;
- accessibility requirements;
- lifecycle;
- domain vocabulary;
- future change direction.

Temporary duplication preserves independent evolution.

Remove duplication when the shared concept—not only the current markup—is real.

---

## Design methodologies are lenses, not laws

Atomic design, feature folders, layers, and domain modules can all be useful.

None can decide a boundary without understanding:

- change patterns;
- ownership;
- dependencies;
- product vocabulary;
- team constraints.

Use a methodology to ask better questions, not to avoid judgment.

---

## Atomic design: strength and limitation

Atomic design encourages a vocabulary from primitives to composed interfaces.

It can help teams discover reusable visual patterns.

But visual size does not always match responsibility.

An “organism” may be a domain feature, while a tiny “atom” may still contain complex behavior.

---

## Feature-oriented decomposition

```text
features/catalogue/
  components/
  state/
  api/
  tests/
features/cart/
  components/
  state/
  api/
  tests/
```

Feature organization keeps the code that changes together close together.

It is often a strong default for application-scale work.

---

## Layer-oriented structure

```text
components/
hooks/
services/
state/
utils/
pages/
```

Layer organization makes technical roles easy to scan.

Its risk is scattering one feature across many directories and weakening domain ownership.

---

## Domain-oriented decomposition

```text
catalogue/
  Product.ts
  ProductCard.tsx
  catalogue-api.ts
  catalogue-state.ts
  catalogue.test.ts
cart/
  Cart.ts
  CartSummary.tsx
```

Domain organization keeps vocabulary, behavior, and tests near the concept they serve.

---

## Technical reuse still crosses domains

```text
shared/ui/Button
shared/ui/Dialog
shared/forms/Field
```

A reusable technical primitive can be shared across domains without forcing domain components into one generic model.

The shared layer should remain intentionally small.

---

## Domain components should speak domain language

Prefer:

```text
<AddToCartButton productId={product.id} />
```

Over:

```text
<Button onClick={() => dispatch({ type: "CART_ADD", payload: product })} />
```

The domain component hides coordination details and exposes the intent relevant to its caller.

---

## Avoid boolean prop explosion

```tsx
<Button primary compact rounded loading danger iconOnly />
```

Many booleans create a combinatorial API and states nobody designed.

Prefer meaningful variants or modeled states:

```ts
type ButtonVariant = "primary" | "danger" | "quiet";
type ButtonState = "ready" | "loading" | "disabled";
```

---

## Stable components should not depend on the whole application

A reusable component should not know:

- the entire route tree;
- the global store shape;
- the current user object;
- every feature's analytics policy.

Pass the smallest data and capabilities needed.

Application coordination belongs above the reusable boundary.

---

## Smart and presentational is a useful distinction

```text
CatalogueContainer
  fetches, owns state, coordinates
        ↓
ProductGrid
  lays out a collection
        ↓
ProductCard
  presents one product and emits intent
```

The names are less important than the separation of coordination from presentation.

---

## React catalogue architecture

```tsx
function CataloguePage() {
  const state = useCatalogueState();

  return (
    <CatalogueLayout>
      <SearchControls value={state.query} onChange={state.setQuery} />
      <ProductGrid products={state.products} onAdd={state.addToCart} />
    </CatalogueLayout>
  );
}
```

The page coordinates. The children expose focused responsibilities.

---

## React product grid

```tsx
function ProductGrid({ products, onAdd }: ProductGridProps) {
  return (
    <ul className="product-grid">
      {products.map(product => (
        <li key={product.id}>
          <ProductCard product={product} onAddToCart={onAdd} />
        </li>
      ))}
    </ul>
  );
}
```

The grid owns collection layout.

The card owns one product's presentation and interaction surface.

---

## Vue can express the same architecture

```vue
<template>
  <CatalogueLayout>
    <SearchControls v-model="query" />
    <ProductGrid :products="products" @add-to-cart="addToCart" />
  </CatalogueLayout>
</template>
```

Compare the responsibilities and data flow, not the framework punctuation.

---

## Compare architecture, not syntax

```text
React props + callbacks   ≈ Vue props + emits
React children            ≈ Vue slots
React context             ≈ Vue provide/inject
custom hooks              ≈ composables
```

Frameworks provide mechanisms.

They do not decide ownership, coupling, or the right domain boundary for you.

---

## Recognize an oversized component

Warning signs:

- many unrelated state variables;
- long conditional render branches;
- repeated markup with slightly different behavior;
- effects that coordinate unrelated systems;
- tests that require the entire application setup;
- a name that no longer describes one responsibility.

Extract by responsibility, not by line count alone.

---

## Recognize over-fragmentation

Warning signs:

- a component has no meaningful API;
- understanding one behavior requires many file jumps;
- props are forwarded unchanged through several layers;
- every markup element has its own file;
- local details become global vocabulary.

Navigation cost is part of the architecture.

---

## Use the extraction test

Ask:

- Does it have its own responsibility?
- Does it have a meaningful public API?
- Does it change for a different reason?
- Is it reused or likely to be reused for a real reason?
- Will extraction reduce or increase navigation cost?

If most answers are no, keep it local for now.

---

## Colocation keeps private behavior near its owner

```text
features/catalogue/
  ProductCard.tsx
  ProductCard.test.tsx
  ProductCard.module.css
  product-card-format.ts
```

Colocation shortens the path from behavior to styles to tests.

Move files outward only when they become shared or when the repository's structure makes ownership clearer elsewhere.

---

## Component boundaries and performance

Boundaries can help with:

- reducing rerender scope;
- memoizing stable subtrees;
- lazy-loading feature code;
- isolating expensive calculations.

But splitting every element is not a performance strategy.

Measure the actual bottleneck and preserve a clear data flow.

---

## Component boundaries and accessibility

An accessible pattern has a behavioral contract:

- roles and relationships;
- keyboard interaction;
- focus movement;
- names and descriptions;
- disabled and busy states.

Keep these rules with the component that owns the interaction, especially for dialogs, tabs, menus, and composite widgets.

---

## Component boundaries and internationalization

Do not bury locale assumptions in generic components.

```tsx
<Price amount={product.priceCents} currency={currency} locale={locale} />
```

The component can format correctly while the feature decides which domain value and locale it is displaying.

Text, plural rules, direction, and date conventions are part of the public behavior.

---

## Component boundaries and security

Keep trust-sensitive behavior near the boundary that understands it.

```text
external content → sanitize / validate → trusted display component
```

Do not make a generic renderer responsible for deciding whether arbitrary HTML is safe.

Make the safe path the easiest public API.

---

## The public API is a contract

Changing a public prop can affect:

- callers;
- tests;
- stories and examples;
- accessibility behavior;
- analytics;
- downstream packages.

Treat component APIs with the same care as a service boundary: explicit, intentional, and proportionate.

---

## A component is not automatically a design-system component

```text
application component → one product's domain language
design-system component → cross-product stable behavior and appearance
```

Promoting a local component too early creates a public API before variation is understood.

Keep application components local until real reuse proves the broader boundary.

---

## One possible layering model

```text
application shell
  ↓
feature components
  ↓
domain components
  ↓
shared behavior / data adapters
  ↓
reusable UI primitives
```

The dependency direction should be intentional.

Lower-level primitives should not import feature-specific decisions.

---

## Practical refactoring strategy

1. Identify responsibilities.
2. Identify shared state.
3. Extract stable visual responsibilities.
4. Keep coordination in the parent initially.
5. Refine APIs.
6. Move truly reusable primitives downward.
7. Add context or injection only when explicit passing is genuinely burdensome.

Refactoring is a sequence of smaller decisions, not a single rewrite.

---

## Refactor the monolith in observable steps

```text
monolith
  → stable layout components
  → product collection boundary
  → product item boundary
  → controlled search boundary
  → composition boundary
  → shared behavior where justified
```

After each step, preserve behavior and re-check ownership.

---

## Practical lab: Compound Headless Tabs

Build a composable tabs system that separates keyboard behavior and state ownership from styling and content layout.

The practical applies the chapter's component API, controlled state, compound composition, accessibility, and headless behavior principles.

---

## Practical stages 1–3: name responsibilities

1. Define the responsibility of the root, tab list, tab, and panel.
2. Implement controlled and uncontrolled selection.
3. Add `role`, `aria-selected`, `aria-controls`, and `tabindex` behavior.

Start with the contract before choosing context, slots, or styling.

---

## Practical stages 4–6: test the interaction

4. Test arrow-key navigation, disabled tabs, and dynamic panels.
5. Compare explicit props, context/provide-inject, and a headless API.
6. Verify that selected tab and visible panel remain synchronized.

The keyboard behavior should be independently testable from the visual treatment.

---

## Practical extension: lazy panels

Add lazy panel loading.

Document the states explicitly:

```text
not requested → loading → ready
                    ↘ error → retry
```

The tabs contract should make loading and failure visible rather than hiding them inside a boolean prop combination.

---

## Try this yourself

Add a disabled tab that:

- cannot receive selection;
- remains represented in the tab order according to your chosen accessibility policy;
- exposes its disabled state;
- does not load its panel;
- does not break arrow navigation.

Write the behavioral contract before the implementation.

---

## Troubleshooting guide

| Symptom | Likely cause |
|---|---|
| Props are forwarded through many layers | Ownership or a real shared dependency is unclear |
| Every component has many booleans | Invalid combinations are not modeled |
| A child and parent fight over state | The controlled contract is ambiguous |
| Context appears everywhere | Dependencies are hidden instead of designed |
| Reusable component needs feature knowledge | The boundary is too low or too broad |
| Refactor creates dozens of files | Extraction followed markup, not responsibility |
| Keyboard behavior is duplicated | Interaction logic lacks one owner |

---

## Completion checklist

- [ ] each extracted component has a coherent responsibility;
- [ ] public props and events express intent;
- [ ] state ownership is explicit;
- [ ] controlled and uncontrolled modes are not mixed accidentally;
- [ ] compound APIs have a real relationship to model;
- [ ] headless behavior is independent from styling;
- [ ] context or injection is used only where it clarifies composition;
- [ ] accessibility behavior belongs with its interaction owner;
- [ ] the final structure reflects feature or domain change patterns.

---

## Misconceptions to leave behind

| Misconception | Better mental model |
|---|---|
| Every repeated markup needs a component | Responsibility and change patterns matter |
| Components exist mainly for reuse | Reasoning, isolation, and ownership matter too |
| Smaller components are always better | Navigation cost is part of quality |
| Each component owns all its state | The owner is the decision-making unit |
| More props mean more flexibility | More public combinations mean more obligations |
| Context is better than prop drilling | Context trades repetition for visibility |
| Reusable means generic | Reuse should preserve meaningful vocabulary |
| A framework decides architecture | Frameworks provide mechanisms, not boundaries |

---

## The chapter in one sentence

> **Design components around coherent responsibility, explicit ownership, and small stable contracts; let composition provide variation.**

---

## Next: Chapter 7

The next chapter will build on component architecture with:

- application state and data flow;
- URL and server state;
- local versus shared state;
- synchronization and derived state;
- predictable updates and debugging.

---

## Questions

Which component in your current application owns too many decisions?

Which one has an API so generic that its domain responsibility is no longer visible?

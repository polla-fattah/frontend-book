---
title: "Reactivity & Rendering Mechanics"
description: "Chapter 7: follow state through render trees, dependency graphs, scheduling, identity, and side-effect boundaries."
book_number: "7"
weight: 8
---

# Reactivity & Rendering Mechanics

Trace state to the screen

**Chapter 7**

Polla Fattah

---

## Today's goal

Understand what happens between a state change and the UI the user sees.

We will connect:

- state-driven rendering;
- snapshots, batching, and identity;
- reconciliation and keys;
- derived values and memoization;
- effects and cleanup;
- React and Vue mental models;
- fine-grained reactivity and signals;
- scheduling, measurement, and unnecessary work.

---

## By the end of today you can

- describe UI as a function of state;
- distinguish render calculation from DOM commitment;
- explain reconciliation and component identity;
- use keys to preserve or reset state intentionally;
- update from previous state safely;
- separate source state from derived values;
- reserve effects and watchers for external synchronization;
- explain React snapshots, Vue proxies, computed values, and batching;
- trace a reactive dependency graph;
- optimize only after measuring the actual work.

---

## The central lesson

```text
source state
    ↓ dependencies
render / derivation
    ↓ scheduling
commit / synchronization
    ↓
screen and external systems
```

Reactivity is not magic.

It is a system that tracks relationships, schedules work, preserves identity, and crosses explicit side-effect boundaries.

---

## The chapter's progression

```text
manual DOM updates
  → state-driven UI
  → render and reconciliation
  → identity and snapshots
  → derived state and effects
  → React mechanics
  → Vue mechanics
  → fine-grained systems
  → scheduling and measurement
```

The same UI goal can be implemented with different reactive mechanisms.

---

## Manual DOM updates are imperative

```js
let count = 0;

button.addEventListener("click", () => {
  count += 1;
  countElement.textContent = String(count);
});
```

The event handler must remember every DOM node affected by the change.

As the interface grows, manual synchronization becomes a coordination problem.

---

## State-driven UI describes a result

```js
function renderCount(count) {
  countElement.textContent = String(count);
}

function increment() {
  count += 1;
  renderCount(count);
}
```

The UI is derived from state rather than updated through a growing list of unrelated DOM instructions.

---

## UI as a function of state

```text
UI = render(state)
```

The function is conceptual, not necessarily a literal full-page rewrite.

It gives the system a useful question:

> Given this state, what should the interface represent?

---

## Reactivity does not mean everything runs automatically

A reactive system must decide:

- what depends on what;
- what work is invalidated;
- when work is scheduled;
- what can be reused;
- what must be synchronized;
- when cleanup runs.

“Reactive” describes a mechanism, not a guarantee that every operation is free or immediate.

---

## State is not the same as every variable

```js
const label = "Products";       // stable configuration
let localCounter = 0;            // ordinary mutable variable
const [query, setQuery] = useState(""); // render-relevant state
```

Use state when a change must participate in the UI's update model.

Do not put every value in state just because it changes somewhere.

---

## A small running example

```text
query: "phone"
products: 120 records
filter: "in-stock"
```

The visible list depends on all three values.

The selected count may be derived.

The network request is an external operation.

The reactive architecture should make each relationship visible.

---

## The React mental model

React calls component functions to calculate a description of UI.

```tsx
function Counter({ count }: { count: number }) {
  return <output>{count}</output>;
}
```

Calling the function does not mean the browser DOM is immediately rewritten.

---

## A React render is a calculation

```text
state update
    ↓
React calls relevant component functions
    ↓
new element descriptions
    ↓
reconciliation
    ↓
commit necessary host changes
```

The render phase should be free of observable side effects.

---

## Render should behave like a pure calculation

```tsx
function ProductCount({ products }: Props) {
  // Good: calculate a value
  const count = products.length;
  return <span>{count}</span>;
}
```

Avoid in render:

- network requests;
- subscriptions;
- DOM mutation;
- timers;
- analytics calls.

---

## Reconciliation compares descriptions

```text
previous tree       next tree
    <h1>Old</h1>  →   <h1>New</h1>
```

The framework compares what was previously described with what is now described, then determines the smallest host update required.

The component function may run even when the DOM change is tiny or absent.

---

## Virtual DOM without the mythology

“Virtual DOM” is a representation and comparison strategy.

It does not mean:

- the entire real DOM is rebuilt every time;
- virtual work is automatically faster than all alternatives;
- every render creates a visible browser update;
- architecture no longer matters.

Measure the work that actually matters.

---

## The commit phase changes external reality

After reconciliation, the framework commits required changes to the host environment.

```text
render phase     → calculate
commit phase     → mutate DOM / attach refs / run commit work
```

Keeping these phases conceptually separate explains why render code should remain predictable.

---

## Parent rendering and child rendering

When a parent renders, its child functions may be called again.

That does not automatically mean:

- every child DOM node changed;
- every child state reset;
- every expensive calculation must rerun forever.

Rendering, reconciliation, commitment, and state preservation are related but distinct questions.

---

## Component identity is part of behavior

```text
same component type + same position + same key
                    → state can be preserved
different identity   → state can be replaced
```

Identity determines whether a component is treated as the same logical instance.

This affects focus, input values, animations, and user experience—not only performance.

---

## State is associated with a position in the render tree

```tsx
{showDetails && <DetailsForm />}
```

If the same component remains at the same logical position, its state may persist across parent renders.

Changing the structure or key can intentionally create a new identity.

---

## Keys are about identity, not silence

```tsx
{items.map(item => (
  <ProductCard key={item.id} product={item} />
))}
```

The key tells the renderer which item is which across changes.

It is not merely a way to remove a warning.

---

## Why array index keys can be dangerous

```tsx
items.map((item, index) => <Row key={index} item={item} />)
```

If items are inserted, removed, or reordered, the index can now identify a different item.

Local state may move to the wrong row.

Use a stable identity from the data whenever the list can change.

---

## Keys can intentionally reset state

```tsx
<Editor key={documentId} document={document} />
```

When `documentId` changes, the editor receives a new identity.

This can be useful when switching between records should discard local draft state.

Resetting is a deliberate product behavior, not a rendering trick.

---

## State is a snapshot

```tsx
function handleClick() {
  setCount(count + 1);
  console.log(count); // current render's snapshot
}
```

The handler closes over the state value from the render that created it.

Calling a setter schedules a future render; it does not mutate the current snapshot in place.

---

## Batching combines updates

```tsx
setCount(count + 1);
setCount(count + 1);
```

Both updates may read the same snapshot and request the same next value.

Batching reduces unnecessary intermediate work, but it means update intent must be expressed correctly.

---

## Use the previous state for dependent updates

```tsx
setCount(previous => previous + 1);
setCount(previous => previous + 1);
```

Each updater receives the latest queued value.

Use this form whenever the next state depends on the previous state.

---

## Derived values should usually be calculated

```tsx
const visibleProducts = products
  .filter(product => product.title.includes(query))
  .filter(product => product.inStock);
```

If a value can be directly calculated from current inputs, storing it separately creates another synchronization obligation.

---

## Source state versus derived state

```text
source: products, query, filter
derived: visibleProducts, resultCount
```

Store the source values.

Calculate the derived values during rendering or in a memoized calculation when measurement justifies it.

---

## Duplicated state creates inconsistency

```tsx
const [products, setProducts] = useState<Product[]>([]);
const [visibleProducts, setVisibleProducts] = useState<Product[]>([]);
```

Now every product update and every filter update must keep both arrays synchronized.

One source of truth is usually simpler and safer.

---

## Expensive derived values are a measurement question

```tsx
const visibleProducts = expensiveFilter(products, query);
```

First ask:

- is the calculation actually expensive?
- how often does it run?
- how large is the input?
- which dependencies change?

Do not add memoization because a calculation exists.

---

## Memoization preserves a calculation result

```tsx
const visibleProducts = useMemo(
  () => expensiveFilter(products, query),
  [products, query],
);
```

The cache is valid only while its dependencies represent the same inputs.

Memoization is an optimization with cost, not a correctness requirement.

---

## Referential identity affects memoization

```tsx
const options = { sort: "price" };
```

This object is new on each render.

Passing it to a memoized child or using it as a dependency may invalidate the optimization even when its contents look unchanged.

Understand identity before optimizing around it.

---

## Effects synchronize with something outside rendering

```tsx
useEffect(() => {
  document.title = `${count} products`;
}, [count]);
```

The document title is external to React's render calculation.

The effect synchronizes it after the committed UI reflects the new state.

---

## Effects are not for ordinary derivation

Avoid:

```tsx
useEffect(() => {
  setVisibleProducts(filter(products, query));
}, [products, query]);
```

This creates an extra state update and an intermediate render for a value that can be calculated directly.

Use an expression or memoized calculation instead.

---

## Events and effects answer different questions

```text
event: what should happen because the user did this?
effect: what external system must be synchronized with committed state?
```

Submit an order because the user activated submit.

Update a subscription because committed state says the subscription should exist.

Do not turn every event response into an effect chain.

---

## Effect cleanup prevents stale work

```tsx
useEffect(() => {
  const controller = new AbortController();
  loadProducts(query, controller.signal);

  return () => controller.abort();
}, [query]);
```

Cleanup runs when dependencies change or the component leaves the tree.

It prevents old subscriptions, timers, and requests from outliving the state that created them.

---

## React rendering summary

```text
state update
  → snapshot-based render calculation
  → reconciliation and identity matching
  → commit host changes
  → effects synchronize external systems
```

This is a model for reasoning, not a promise that every implementation detail is synchronous or simple.

---

## The Vue mental model

Vue tracks reactive dependencies more directly through refs, reactive proxies, computed values, and watchers.

The goal remains the same:

```text
state → dependencies → render / synchronization
```

The tracking mechanism and timing model differ from React's component recalculation model.

---

## Vue `ref()` wraps a reactive value

```ts
const count = ref(0);

count.value += 1;
```

The ref object gives Vue a stable reactive container.

In templates, Vue can unwrap refs for convenient access.

---

## Vue `reactive()` proxies an object

```ts
const filters = reactive({
  query: "",
  inStock: false,
});

filters.query = "phone";
```

The proxy intercepts reads and writes so Vue can track which reactive effects depend on which properties.

---

## The proxy and original object differ

```ts
const original = { query: "" };
const state = reactive(original);

state !== original;
```

Use the reactive proxy consistently.

Identity assumptions become important when comparing, storing, or passing reactive objects.

---

## Destructuring can break a reactive connection

```ts
const state = reactive({ query: "" });
const { query } = state;
```

The local `query` is no longer a reactive property reference in the same way.

Use `toRefs`, a computed value, or access through the reactive object when the connection must be preserved.

---

## Vue rendering is a reactive effect

When a component renders, Vue records which reactive values it reads.

When one of those values changes, Vue knows that the component's rendered output may need updating.

This is dependency tracking at the property level rather than a blanket statement that every component always reruns.

---

## Vue DOM updates are scheduled

```ts
state.query = "phone";
state.inStock = true;

await nextTick();
```

The state assignments are observable to Vue immediately, but DOM work is typically queued and batched.

Do not assume the DOM reflects a mutation on the next line.

---

## Vue batching reduces intermediate work

Several synchronous mutations can be grouped into one update cycle.

This is why code that needs the updated DOM may need `nextTick()` or an equivalent lifecycle boundary.

The scheduling model should be part of the component's reasoning, especially around focus and measurement.

---

## Computed values represent derivation

```ts
const visibleProducts = computed(() =>
  products.value
    .filter(product => product.title.includes(query.value))
    .filter(product => product.inStock),
);
```

Computed values declare a dependency relationship and can cache until their dependencies invalidate.

---

## Computed values are not ordinary state

```text
products + query + filter
             ↓
      computed visibleProducts
```

The computed result should not be manually synchronized with every source update.

Keep derivation represented as derivation.

---

## Vue watchers synchronize external systems

```ts
watch(query, value => {
  router.replace({ query: { q: value } });
});
```

This is appropriate when a change in reactive state must update a router, storage layer, network operation, or other external system.

---

## Watchers should not replace computed values

```ts
watch([products, query], () => {
  visibleProducts.value = filter(products.value, query.value);
});
```

This stores a derived value and introduces a synchronization path.

Prefer `computed` when the result is a direct calculation.

---

## `watch()` and `watchEffect()` differ

```text
watch(source, callback)
  explicit dependency, controlled comparison

watchEffect(callback)
  dependencies discovered while running
```

Use the most explicit form that communicates the intended relationship.

---

## Watcher cleanup prevents stale effects

```ts
watch(query, async (value, _oldValue, onCleanup) => {
  const controller = new AbortController();
  onCleanup(() => controller.abort());
  await loadProducts(value, controller.signal);
});
```

If a newer query arrives, the old operation should not win after it becomes irrelevant.

---

## React and Vue share the goal, not the mechanism

| Concern | React | Vue |
|---|---|---|
| primary model | component calculation | tracked reactive dependencies |
| derivation | expression / memo | computed |
| external sync | effect | watch / watchEffect |
| state update | setter schedules render | mutation invalidates dependencies |
| DOM timing | commit and effects | queued update and `nextTick` |

Learn the mechanism well enough to predict behavior; do not flatten the differences into slogans.

---

## Reactivity has granularity

```text
coarse: rerun a broad component calculation
fine:   invalidate only computations reading a changed property
```

Coarser systems can be simple to reason about.

Finer systems can reduce work by tracking smaller dependencies.

Neither choice removes the need for good state design.

---

## Fine-grained reactivity

```text
signal A ─┐
          ├─ derived C ─→ effect
signal B ─┘
```

Only computations that depend on invalidated sources need to be reconsidered.

This graph is explicit in the runtime rather than reconstructed from a broad component render.

---

## Signals are a family of ideas

```ts
const count = signal(0);
const doubled = computed(() => count() * 2);
effect(() => console.log(doubled()));
```

Different libraries use different APIs and scheduling rules.

“Signals” names a reactive primitive pattern, not one universal technology.

---

## Signals are not automatically faster

Performance depends on:

- graph shape;
- update frequency;
- computation cost;
- scheduling;
- DOM work;
- memory and bookkeeping;
- developer usage.

A fine-grained mechanism can still perform unnecessary work if the graph or state model is poorly designed.

---

## Scheduling is part of the model

```text
mutation
  → invalidation
  → queue
  → flush
  → render / commit / effect
```

Scheduling determines what “immediately” means.

It affects batching, race conditions, DOM measurement, focus, and perceived responsiveness.

---

## Why scheduling exists

Scheduling can:

- combine several changes;
- avoid repeated layout work;
- prioritize urgent interaction;
- defer expensive computation;
- coordinate asynchronous results;
- prevent recursive update storms.

The trade-off is that a state mutation and a visible result may be separated in time.

---

## Unnecessary rendering work is not always a bug

Ask:

- did the calculation actually cost enough to matter?
- did the DOM change?
- did the user notice?
- did the work block input or layout?
- does optimization add more complexity than it removes?

Not every rerender is a problem.

---

## Example: expensive filtering

```tsx
const visible = useMemo(
  () => products.filter(matchesQuery),
  [products, query],
);
```

This may help when `products` is large and the calculation is repeated.

It may do nothing useful when the array is small, dependencies change every time, or rendering dominates the cost.

---

## Memoization should follow measurement

```text
measure → identify repeated expensive work
       → choose the narrowest optimization
       → verify behavior and cost again
```

Memoization has costs:

- dependency maintenance;
- memory;
- identity management;
- cognitive overhead.

---

## Component memoization is not a correctness fix

```tsx
const ProductCard = memo(function ProductCard(props: Props) {
  return <article>{props.product.title}</article>;
});
```

Memoization can skip a render when props are considered equal.

It cannot repair incorrect keys, duplicated state, stale closures, or a bad ownership boundary.

---

## Vue's selective tracking has its own costs

Property-level tracking can avoid broad updates.

But deep reactive objects, unstable identities, and unnecessary watchers can still make an application difficult to reason about.

Selectivity is a mechanism—not a substitute for a clear dependency graph.

---

## Identity affects list rendering in every framework

```text
stable item identity
  → preserve the correct row state
  → preserve focus and input values
  → make insertions and reordering understandable
```

Stable keys are a user-experience concern as much as a rendering optimization.

---

## State preservation is architectural

When state disappears unexpectedly, ask:

- did the component type change?
- did its position change?
- did its key change?
- did a conditional branch replace its identity?
- did the data identity change while the key stayed index-based?

The answer is often in the render tree, not in the state setter.

---

## Conditional rendering can change identity

```tsx
{mode === "edit" ? <Editor /> : <Preview />}
```

Switching between different component types replaces the identity at that position.

If two modes should preserve one shared draft, model them accordingly.

If switching should reset state, make that reset intentional.

---

## Effects and watchers can create feedback loops

```text
state change → effect updates state
            → effect runs again
            → repeated updates
```

Before adding synchronization, define:

- the external source of truth;
- the direction of the update;
- the stopping condition;
- cleanup and error behavior.

---

## Think in reactive graphs

```text
query ──────────┐
products ────────┼─→ visibleProducts ─→ ProductGrid
stockFilter ────┘

query ─→ URL synchronization effect
```

The graph reveals which values are sources, derivations, render consumers, and external effects.

It also reveals cycles and broad dependencies.

---

## Compiler-assisted optimization

Compilers can sometimes infer:

- stable expressions;
- memoization opportunities;
- dependency relationships;
- component boundaries;
- update paths.

They cannot infer product intent, correct identity, or whether a value belongs in state.

Optimization tools reduce some manual work; they do not remove architectural decisions.

---

## React Compiler is an example, not a new mental model

Compiler assistance may reduce the need for some manual memoization.

The fundamentals remain:

- pure render calculations;
- stable identity;
- correct dependencies;
- explicit effects;
- measured performance work.

Understand the behavior even when tooling automates an optimization.

---

## Searchable product list: the shared dependency graph

```text
query ───────┐
products ────┼─→ filteredProducts ─→ list
filter ──────┘

query ─→ URL
list selection ─→ analytics
```

The same product feature can be implemented in React, Vue, or a signal system while preserving this conceptual graph.

---

## React version: calculate and synchronize

```tsx
const filteredProducts = useMemo(
  () => filterProducts(products, query, filter),
  [products, query, filter],
);

useEffect(() => {
  router.replace({ query });
}, [query]);
```

Derivation stays in the render model.

The router is synchronized in an effect.

---

## React anti-pattern: derived state effect

```tsx
useEffect(() => {
  setFilteredProducts(filterProducts(products, query, filter));
}, [products, query, filter]);
```

This creates:

- duplicated state;
- an extra render path;
- a possible stale intermediate value;
- more code to test and debug.

Calculate the list directly unless there is a measured reason not to.

---

## Vue version: computed and watch

```ts
const filteredProducts = computed(() =>
  filterProducts(products.value, query.value, filter.value),
);

watch(query, value => router.replace({ query: { q: value } }));
```

The same graph is expressed with Vue's dependency tracking primitives.

---

## Trace React updates

For a state change, record:

1. Which setter was called?
2. Which snapshot created the handler?
3. Which components calculate again?
4. Which identities and keys are reused?
5. Which host nodes commit changes?
6. Which effects run and which clean up?

This sequence is more useful than saying “React rerendered everything.”

---

## Trace Vue updates

For a reactive mutation, record:

1. Which ref or proxy property changed?
2. Which computed values depend on it?
3. Which component render effects read it?
4. Which watchers are triggered?
5. When is the DOM queue flushed?
6. Which cleanup functions run?

The goal is to expose the dependency graph and schedule.

---

## What should we measure?

Measure questions such as:

- how long does the expensive calculation take?
- how many items are processed?
- how often does the calculation run?
- how many components commit changes?
- does input responsiveness degrade?
- does memory grow because of caches or subscriptions?

Choose a measurement that can change the decision.

---

## Necessary UI change versus unnecessary work

```text
state changed
  → some recalculation may be necessary
  → some DOM changes may be necessary
  → other work may be avoidable
```

Do not optimize away work before identifying which part is unnecessary.

Correctness and a truthful dependency graph come first.

---

## State location affects rendering scope

State placed high in the tree can coordinate many consumers but broaden update scope.

State placed close to one interaction can reduce unrelated work but may require a deliberate communication path.

Choose location based on ownership and synchronization—not on a universal rule to lift or localize state.

---

## Derived state affects rendering scope

Keep derivation near the data and consumers that need it.

If a derived value is shared, expose one clear calculation rather than duplicating it in multiple components.

If it is cheap and local, a plain expression is often the best design.

---

## Side effects should cross a boundary

```text
pure calculation → describe desired UI
effect boundary  → network, storage, DOM, timer, subscription
```

The boundary helps answer:

- when does this run?
- what invalidates it?
- how is it cleaned up?
- what happens if the value changes again?

---

## Do not let the reactive system become a mystery network

A healthy graph has:

- visible sources;
- named derivations;
- few synchronization edges;
- bounded effects;
- explicit cleanup;
- tests for identity and timing.

If changing one field triggers an unexplained chain of watchers and effects, simplify the graph before optimizing it.

---

## A practical decision model

Ask:

- Is another value directly calculable from this one?
- Does a user action cause an operation?
- Must an external system remain synchronized?
- Is a calculation expensive and repeated unnecessarily?
- Is the update scope too broad?

These questions map naturally to derived values, events, effects, memoization, and state placement.

---

## Four reactive strategies

| Strategy | Main strength | Main risk |
|---|---|---|
| React render model | explicit component calculation | confusing render with DOM work |
| Vue dependency tracking | selective property updates | hidden reactive connections |
| signals | fine-grained graph | graph and lifecycle complexity |
| compiler assistance | less manual optimization | false confidence about architecture |

Use the model your team can explain and debug.

---

## Practical lab: Reactive Computed Graph

Implement a tiny educational reactive graph to make source state, derived values, dependency tracking, and effects visible.

The implementation is for learning. It is not a production reactive runtime.

---

## Practical stages 1–3: sources and derivation

1. Implement a signal with subscribers.
2. Add lazy computed values and invalidation.
3. Add an effect with cleanup.

Make the graph observable with logs or counters so the execution order can be inspected.

---

## Practical stages 4–5: cycles and comparisons

4. Create a cycle deliberately and explain why production systems must guard against it.
5. Compare the educational graph with React render calculation and Vue `computed()`.

Ask which mechanism discovers dependencies, when invalidation occurs, and how cleanup is represented.

---

## Practical extension: visualize the graph

Add a graph visualizer showing:

```text
source → computed → computed → effect
```

Highlight:

- invalidated nodes;
- execution order;
- cached nodes;
- unused computations;
- cycles.

The visualizer should make the invisible dependency model inspectable.

---

## Try this yourself

Build a searchable list with:

- source products;
- query state;
- a derived filtered list;
- a URL synchronization effect;
- cancellation for stale searches.

Then explain which updates are necessary and which calculations can remain untouched.

---

## Troubleshooting guide

| Symptom | Likely cause |
|---|---|
| State update seems one step behind | Snapshot or batching misunderstood |
| Input state moves to another row | Unstable or index-based keys |
| UI flashes an old derived value | Derived state synchronized through an effect |
| Effect runs forever | Effect updates one of its own dependencies |
| Vue value stopped updating | Destructuring removed the reactive connection |
| DOM is old after a mutation | Update is queued; await the framework flush |
| Memoization changes nothing | Dependencies or calculation cost do not justify it |
| Async result wins after a newer query | Missing cleanup or cancellation |

---

## Completion checklist

- [ ] source state is distinct from derived values;
- [ ] render calculations are free of external side effects;
- [ ] list keys represent stable identity;
- [ ] previous-state updates are used for dependent changes;
- [ ] effects and watchers synchronize external systems only;
- [ ] cleanup prevents stale subscriptions and requests;
- [ ] React and Vue timing differences are understood;
- [ ] optimization decisions are supported by measurement;
- [ ] the reactive graph is explainable from source to screen.

---

## Misconceptions to leave behind

| Misconception | Better mental model |
|---|---|
| State changed, so the DOM changed immediately | Updates are calculated and scheduled |
| A React render rebuilt the DOM subtree | Render and commit are different phases |
| Virtual DOM is always faster | Performance depends on the measured work |
| Every rerender is a bug | Some recalculation is necessary |
| Keys only remove warnings | Keys preserve logical identity |
| Derived values belong in state | Direct calculations usually stay derived |
| Effects respond to any state change | Effects synchronize external systems |
| Vue watchers calculate normal derivations | `computed` represents derivation |
| Signals are one standard technology | Signals are a family of mechanisms |
| Compiler optimization makes architecture irrelevant | Tools cannot choose ownership or intent |

---

## The chapter in one sentence

> **Design a truthful reactive graph: keep source state minimal, derivation explicit, identity stable, scheduling understood, and side effects at the boundary.**

---

## Next: Chapter 8

The next chapter will apply these rendering and state principles to:

- asynchronous data and server state;
- loading, error, empty, and success states;
- request cancellation and stale results;
- caching and synchronization;
- resilient data-fetching architecture.

---

## Questions

For one interaction in your application, can you draw the path from source state to derived value to committed UI?

Where does the first external side effect enter the graph?

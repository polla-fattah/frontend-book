---
title: "Client–Server Communication, APIs & Cache Management"
description: "Chapter 9: design reliable HTTP boundaries, represent remote UI states, and manage caches, mutations, retries, and recovery."
book_number: "9"
weight: 10
---

# Client–Server Communication, APIs & Cache Management

Make remote data predictable

**Chapter 9**

Polla Fattah

---

## Today's goal

Build a client that treats the network as an unreliable, stateful boundary.

We will connect:

- HTTP methods, headers, status codes, and request helpers;
- runtime validation and transport/domain separation;
- cancellation, timeouts, retries, and backoff;
- REST, GraphQL, pagination, and API compatibility;
- loading, empty, stale, error, and recovery states;
- query keys, deduplication, freshness, and invalidation;
- pessimistic and optimistic mutations;
- server validation, authentication failures, and partial data.

---

## By the end of today you can

- implement a fetch boundary that handles HTTP errors explicitly;
- distinguish network, transport, schema, domain, and authentication failures;
- choose safe retry behavior;
- model remote UI states without conflating loading and empty;
- design stable cache keys and freshness policies;
- deduplicate requests and cancel stale work;
- invalidate or update caches after mutations;
- use optimistic updates with rollback only when justified;
- preserve useful partial data during dashboard failures;
- draw the full client-server data architecture.

---

## The central lesson

> **Remote data is not a value; it is a lifecycle of requests, cache entries, freshness, failures, mutations, and recovery.**

The UI should make that lifecycle visible without forcing every component to understand HTTP details.

---

## The chapter's progression

```text
HTTP boundary
  → transport and domain layers
  → request lifecycle
  → remote UI states
  → query cache
  → freshness and invalidation
  → mutations and rollback
  → resilient application architecture
```

Every layer answers a different question about remote data.

---

## Browser and server have different responsibilities

```text
browser: interaction, rendering, local drafts, navigation
server:  authority, persistence, authorization, business rules
network:  latency, loss, duplication, reordering, failure
```

The client cannot assume that the server is fast, available, current, or correct for every request.

---

## HTTP is the communication foundation

```text
request = method + URL + headers + body
response = status + headers + body
```

Each part carries contract information.

Do not treat an HTTP exchange as merely “fetch some JSON”.

---

## HTTP methods express intent

| Method | Typical intent |
|---|---|
| GET | read a representation |
| POST | create or trigger an operation |
| PUT | replace a resource representation |
| PATCH | partially modify a resource |
| DELETE | remove a resource |

The exact API contract still matters; method names are not permission to guess semantics.

---

## Safe and idempotent are different properties

```text
safe      → intended not to change server state
idempotent → repeating the same request has the same intended result
```

GET is generally safe and idempotent.

PUT is commonly idempotent but not safe.

POST is not automatically idempotent, so retries require care.

---

## Request headers are part of the contract

```http
Accept: application/json
Content-Type: application/json
Authorization: Bearer …
If-None-Match: "version-42"
```

Headers communicate representation, credentials, caching, conditional requests, and client capabilities.

---

## `Accept` and `Content-Type` answer different questions

```text
Accept       what response representation can the client read?
Content-Type what representation is this request body?
```

Confusing them can produce content negotiation and parsing bugs that look like application errors.

---

## Status codes are part of the API contract

```text
2xx success
3xx redirection / cache interaction
4xx client or authorization problem
5xx server failure
```

The client should classify status codes into user-visible recovery paths instead of displaying one generic failure for everything.

---

## `fetch()` does not reject for every HTTP error

```ts
const response = await fetch("/api/products");

if (!response.ok) {
  throw new HttpError(response.status);
}
```

A 404 or 500 response can resolve normally.

Network failures typically reject; HTTP failure status still needs explicit handling.

---

## A small fetch helper

```ts
async function request<T>(input: RequestInfo, init?: RequestInit): Promise<T> {
  const response = await fetch(input, init);
  if (!response.ok) throw new HttpError(response.status);
  const payload: unknown = await response.json();
  return parseResponse<T>(payload);
}
```

The helper centralizes transport behavior, but it must not hide meaningful errors or bypass runtime validation.

---

## Network and domain layers should not be confused

```text
HTTP adapter → transport response → parser → domain model → feature
```

The adapter knows status codes and headers.

The domain feature knows what a valid product or workflow means.

Keeping those responsibilities separate makes change and testing cheaper.

---

## JSON is a representation, not a type guarantee

```ts
const payload: unknown = await response.json();
```

JSON can represent an object that is:

- missing fields;
- using the wrong types;
- from an older server version;
- structurally valid but semantically invalid.

Parse at the boundary before trusting it.

---

## Request bodies need an explicit representation

```ts
await fetch("/api/products", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(command),
});
```

The request body is a transport representation, not automatically the same as the form draft or domain entity.

---

## Credentials and cookies change the boundary

```ts
fetch("/api/me", {
  credentials: "include",
});
```

Authentication, CSRF protection, CORS, expiration, and logout behavior are part of the client-server contract.

Never treat a missing credential as an ordinary empty response.

---

## Cancellation is correctness, not only optimization

```ts
const controller = new AbortController();

fetch(url, { signal: controller.signal });
controller.abort();
```

Cancellation prevents obsolete work from consuming resources or updating a UI that now represents a different request.

---

## Timeouts are application policy

```ts
const timeout = setTimeout(() => controller.abort(), 8_000);
try {
  return await fetch(url, { signal: controller.signal });
} finally {
  clearTimeout(timeout);
}
```

Choose timeout behavior based on user action, operation cost, connectivity, and retry policy.

---

## Retry carefully

Retrying can help transient failures.

It can also:

- duplicate a non-idempotent mutation;
- overload a struggling server;
- delay a useful error;
- hide an authorization failure;
- create a thundering herd.

Retry only when the operation and policy justify it.

---

## Exponential backoff spreads retries

```text
attempt 1 → short delay
attempt 2 → longer delay
attempt 3 → longer still
```

Add jitter so many clients do not retry at the same instant.

Bound the number of attempts and expose a recovery action when automatic retry ends.

---

## API design affects front-end architecture

The API determines:

- what can be fetched independently;
- how mutations are represented;
- which fields are stable;
- how pagination works;
- which errors can be recovered;
- which cache entries need invalidation.

Client architecture cannot fully compensate for an ambiguous server contract.

---

## REST is resource-oriented

```text
GET    /products
GET    /products/p-42
PATCH  /products/p-42
DELETE /products/p-42
```

Resource-oriented URLs can map naturally to cache keys and route identities.

They are a style, not a promise that every API has identical semantics.

---

## Collections and resources have different concerns

```text
collection: filters, sorting, pagination, totals
resource:   identity, fields, permissions, mutation
```

Do not assume that invalidating one product automatically answers what should happen to every filtered collection containing it.

---

## Pagination is part of the cache model

```text
products?page=1&limit=20
products?page=2&limit=20
```

Decide whether pages are:

- independent cache entries;
- concatenated into an infinite list;
- invalidated together after a mutation;
- prefetched based on navigation.

---

## Filtering and sorting belong in the request identity

```text
/products?query=phone&sort=price&stock=in
```

Changing any relevant input should produce a distinct query key or an explicit cache update.

Never reuse a cache entry for a request with different semantics.

---

## API versioning protects compatibility

Versioning may be represented through:

- URL paths;
- headers;
- content negotiation;
- additive schema evolution.

The client should validate the response it actually receives, even when generated types say the version is known.

---

## GraphQL asks for a shape of data

```graphql
query Products($query: String) {
  products(query: $query) {
    id
    title
    priceCents
  }
}
```

The client requests fields and receives a schema-described response.

This changes transport shape and caching questions; it does not eliminate them.

---

## GraphQL schemas and mutations

Schemas can provide:

- typed fields;
- discoverable operations;
- nested data selection;
- validation at the operation boundary.

Mutations still need authorization, error handling, cache updates, conflict policies, and runtime behavior.

---

## REST and GraphQL can coexist

Use the boundary that fits the resource and team needs.

A system may use REST for uploads and resource mutations, GraphQL for composed reads, and a separate stream for live updates.

The architecture should make each boundary's semantics explicit.

---

## Remote data has UI states

```ts
type QueryState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T; stale: boolean }
  | { status: "error"; error: RemoteError; previous?: T };
```

Represent the lifecycle instead of reducing it to `data` plus `isLoading`.

---

## Loading is not the same as empty

```text
loading → data not known yet
empty   → request succeeded; result set has zero items
```

The recovery and user message differ.

An empty catalogue may need onboarding.

A loading catalogue needs progress or preserved context.

---

## Loading UI should match scope

```text
whole route loading     → route fallback
table refreshing         → table status / preserved rows
save button submitting   → button pending state
```

A global spinner can erase useful context and make the application feel slower.

---

## Spinner, skeleton, or existing content?

```text
spinner    unknown short operation
skeleton   first load with known content shape
existing   background refresh where current data remains useful
```

Choose based on what the user can still do and how much layout is known.

---

## Empty state is product state

An empty result may mean:

- no records exist yet;
- filters are too restrictive;
- the user lacks access;
- a search has no matches;
- the resource was removed.

Show the cause and the next useful action when possible.

---

## Error states need recovery

```text
retry → same request again
edit filters → change request identity
sign in → resolve authentication
go back → leave invalid route
```

An error component should answer: what failed, what remains usable, and what can the user do next?

---

## Client caching is a policy

A cache answers:

- may this result be reused?
- for how long?
- when should it revalidate?
- how is it invalidated?
- can stale data remain visible?
- who owns the cache?

Caching is not simply “store the last response”.

---

## Freshness depends on the data

```text
country list       long freshness window
product inventory  short freshness window
bank balance       very short / explicit refresh
```

Freshness is a product and domain decision, not one global number.

---

## Stale does not mean wrong

Stale data can still be useful while a background request checks for newer data.

The UI should communicate that it is refreshing when the distinction matters.

Discarding useful data on every refresh failure can create a worse experience than showing stale data with a clear warning.

---

## Stale-while-revalidate

```text
cache hit → show cached data
         → request fresh data
         → update cache if newer data arrives
```

This pattern separates immediate usefulness from eventual freshness.

It requires a policy for errors, timestamps, and concurrent requests.

---

## Cache keys identify query meaning

```ts
const key = ["products", { query, sort, page, stock }];
```

A cache key must include every input that changes the response.

It should be deterministic, serializable, and stable across callers.

---

## Missing key inputs cause incorrect reuse

Bad:

```text
["products"]
```

when the response varies by query, page, sort, account, or locale.

The cache then returns data that is valid for a different request but wrong for this view.

---

## Deduplicate identical requests

```text
component A ─┐
component B ─┼─→ one in-flight request → shared result
component C ─┘
```

Deduplication reduces duplicate work and makes concurrent consumers observe one request lifecycle.

The cache must distinguish an in-flight promise from a completed fresh value.

---

## Revalidation asks whether data changed

Revalidation can happen:

- when data becomes stale;
- when a route gains focus;
- after a mutation;
- on explicit refresh;
- after reconnecting;
- through a conditional HTTP request.

Choose triggers that match the user's need for freshness.

---

## Invalidation removes confidence, not necessarily data

```text
mutation succeeds
  → related cache entries become uncertain
  → invalidate or update them
  → refetch when needed
```

Invalidation is a statement that cached knowledge may no longer be current.

It does not always mean immediately deleting useful visible data.

---

## Invalidation versus direct cache update

Use invalidation when:

- many related queries may change;
- server logic computes fields the client cannot reproduce;
- correctness is more important than avoiding a request.

Directly update one entry when:

- the mutation response is authoritative;
- the affected cache shape is known;
- the update is easy to verify.

---

## Mutations have their own lifecycle

```text
idle → submitting → success
                 ↘ error → retry
```

Add:

- duplicate-submission protection;
- server validation handling;
- authentication behavior;
- cache reconciliation;
- draft preservation on failure.

---

## Mutation UX communicates authority

```text
pessimistic → wait for server before showing success
optimistic  → show intended result before confirmation
```

Choose based on reversibility, conflict risk, user expectations, and the cost of being briefly wrong.

---

## Prevent duplicate submission at several layers

Client disabling helps the interface.

It does not guarantee that duplicate requests cannot arrive.

Use server-side idempotency keys or operation identifiers where repeating an operation has real cost.

---

## Pessimistic updates are conservative

```text
submit → pending UI → server success → update visible state
                  ↘ error → keep draft and show recovery
```

Use this for high-risk, non-reversible, or conflict-sensitive operations where showing unconfirmed state would mislead users.

---

## Optimistic updates trade certainty for responsiveness

```text
user action → update UI immediately
           → request server
           → confirm or rollback
```

The client must know how to undo the change and what to show if the server rejects it.

---

## Optimistic rollback needs a snapshot

```ts
const previous = cache.get(key);
cache.set(key, nextValue);

try {
  await save(command);
} catch (error) {
  cache.set(key, previous);
}
```

In real systems, also consider concurrent edits, invalidation, and a final revalidation.

---

## Not every mutation should be optimistic

Avoid optimism when:

- the action is irreversible;
- server rules are complex;
- conflicts are likely;
- authorization may fail often;
- rollback is ambiguous;
- the visible result depends on server-side computation.

Fast feedback is not worth misleading the user.

---

## Conflict and concurrency need a policy

Two clients may update the same resource.

Possible strategies include:

- last write wins;
- version checks;
- conditional requests;
- conflict UI;
- server merge rules;
- explicit refresh before editing.

The cache cannot solve a domain conflict by itself.

---

## Conditional requests use server versions

```http
If-Match: "version-42"
```

The server can reject a mutation when the resource changed since the client read it.

This prevents a stale edit from silently overwriting newer data.

---

## Browser HTTP cache versus application cache

| Browser HTTP cache | Application/query cache |
|---|---|
| controlled by HTTP semantics | controlled by application policy |
| stores representations | stores parsed/query-aware data |
| keyed by request semantics | keyed by query and domain inputs |
| works below application code | exposes freshness and invalidation |

They can cooperate, but they are not the same layer.

---

## `Cache-Control` is a server instruction

```http
Cache-Control: max-age=60, stale-while-revalidate=300
```

HTTP caching can reduce network work before application code runs.

The application still needs its own policy for query state, mutations, and visible stale/error behavior.

---

## Forms and server mutations

```text
form draft → validate locally → submit transport command
          → server validation / authorization
          → preserve or commit draft
```

A successful request does not automatically mean every form field, cache entry, and route is now synchronized.

---

## Native form submission remains useful

Native submission provides:

- keyboard behavior;
- browser integration;
- progressive enhancement;
- a clear submit event;
- `FormData` serialization.

Enhance it when application behavior requires it; do not discard platform behavior without a reason.

---

## `FormData` is a transport boundary

```ts
const formData = new FormData(form);
const email = formData.get("email");
```

Values may be strings, files, or null.

Validate and convert them before building a domain command or JSON payload.

---

## JSON form submission is an explicit conversion

```ts
const command = parseProductDraft(readDraft(formData));

await fetch("/api/products", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(command),
});
```

The parser is where unfinished input becomes a validated transport model.

---

## Server validation errors are different from local errors

```text
local: email format is invalid
server: email is already registered
```

Both may appear near a field, but they have different owners, timing, and recovery paths.

Do not overwrite a useful server response with a generic client message.

---

## Map server errors to fields carefully

```ts
type ServerError =
  | { kind: "field"; field: string; message: string }
  | { kind: "form"; message: string };
```

Only map an error to a field when the server contract identifies that field reliably.

Some failures belong to the form or page, not one input.

---

## Do not merge client and server validation carelessly

Track the sources distinctly:

```text
clientErrors
serverErrors
```

Clear server errors when the relevant draft changes if the server response is no longer applicable.

Keep the message that explains the actual current failure.

---

## Progressive enhancement for forms

```text
native submit works without JavaScript
        ↓
JavaScript adds pending UI, validation, and navigation
```

The enhanced path should preserve the core meaning of the native form rather than creating a completely different contract.

---

## File uploads have different transport needs

```ts
const body = new FormData(form);

await fetch("/api/upload", {
  method: "POST",
  body,
});
```

Do not set a JSON content type for multipart data manually.

Model upload progress, cancellation, size limits, type validation, and partial failure explicitly.

---

## Authentication failures are not ordinary validation errors

```text
401 → establish or refresh identity
403 → identity exists but action is forbidden
422 → submitted data violates application rules
```

The correct response may be sign-in, permission explanation, or field correction—not a red error beneath an input.

---

## Search needs query identity, cache, and cancellation

```text
query A → request A
query B → cancel or supersede A → request B
```

An old response must not replace results for a newer query.

The query key should include every input that changes the result.

---

## Query keys and URL state fit naturally together

```text
URL: /products?query=phone&page=2
key: ["products", "phone", 2]
```

The URL provides the committed view identity.

The query cache stores the server result for that identity.

Parse once and derive both from the same validated model.

---

## Avoid copying query data into another store

```text
query cache → components
```

Copying into a general client store creates:

- duplicate ownership;
- stale copies;
- unclear invalidation;
- extra synchronization effects.

Keep server data in a server-aware cache unless there is a deliberate transformation or offline model.

---

## Dependent queries form a data graph

```text
currentUser → accountId → account → transactions
```

Start the dependent request only when its required input is known.

Represent the not-ready state instead of sending malformed requests with missing identifiers.

---

## Request waterfalls cost time

```text
A completes → B starts → C starts
```

If B and C do not depend on A, request them in parallel.

If they do depend, consider server composition, prefetching, or a route loader that understands the graph.

---

## Parallel fetching

```ts
const [products, categories] = await Promise.all([
  loadProducts(),
  loadCategories(),
]);
```

Use parallel work for independent requests.

Choose `Promise.allSettled()` or explicit result handling when partial success is useful.

---

## Partial failure can preserve useful data

```text
dashboard
├─ sales       success
├─ inventory   error + retry
└─ alerts      success
```

Do not blank the entire dashboard because one independent panel failed.

The architecture should allow panels to own their own request lifecycle.

---

## `Promise.all()` versus partial failure

```ts
const results = await Promise.allSettled(requests);
```

`Promise.all()` is appropriate when all results are required for one operation.

`allSettled()` or independent query states are appropriate when each panel can recover separately.

---

## Background refresh preserves context

```text
fresh visible data + isRefreshing = true
```

Keep current rows visible while a refresh runs when stale data remains useful.

Show that the data is refreshing without turning every background check into a blank loading screen.

---

## Stale data with an error is still a meaningful state

```text
previous data + refresh failed
```

Tell the user that the displayed data may be out of date and offer retry.

This is often more useful than replacing known content with an empty error page.

---

## Mutation followed by revalidation

```text
save succeeds → invalidate related queries → refetch current truth
```

Revalidation is safest when the server computes fields, permissions, totals, or relationships the client cannot reproduce.

---

## Mutation response as a cache update

```text
PATCH product → response contains canonical product
             → update product key directly
```

This can avoid a request when the response is authoritative and the affected query shapes are known.

Still consider list ordering, filters, totals, and related cache entries.

---

## Optimistic cache update

```text
snapshot → provisional update → request → confirm / rollback / revalidate
```

The cache update should be isolated, reversible, and tested for failure and concurrency.

---

## Server-state libraries provide mechanisms

They may offer:

- query keys;
- caching;
- stale time;
- retries;
- deduplication;
- invalidation;
- mutation lifecycles;
- optimistic updates.

They do not decide API semantics, domain ownership, or whether a mutation is safe to retry.

---

## A useful separation of responsibilities

```text
transport adapter → HTTP details
query layer       → cache, freshness, deduplication
domain mapper     → trusted application model
feature           → user intent and workflow
view              → rendering and recovery actions
```

Each layer should expose the information its caller needs without leaking every lower-level detail.

---

## Do not hide every HTTP detail behind one giant service

A universal `api.requestEverything()` wrapper often obscures:

- status-specific recovery;
- cancellation;
- request identity;
- cache behavior;
- mutation semantics.

Centralize repeated mechanics, but keep meaningful operation contracts visible.

---

## Transport errors versus domain errors

```text
network unavailable     transport failure
HTTP 500                server/transport failure
malformed JSON          schema failure
valid but forbidden     authorization/domain failure
valid but unavailable   domain/business failure
```

Different causes require different UI and retry behavior.

---

## Normalize errors without leaking secrets

```ts
type RemoteError = {
  kind: "network" | "http" | "schema" | "auth" | "domain";
  message: string;
  retryable: boolean;
};
```

Normalize enough for the UI to make a decision.

Do not expose stack traces, tokens, internal SQL, or sensitive payloads to users.

---

## Administrative catalogue architecture

```text
URL             query, filters, sort, page
server state    products, categories, cache
local UI        modal, focus, panel open
form state      draft, dirty, validation
transport       request, status, cancellation
```

The catalogue becomes easier to reason about when each concern has one owner.

---

## Product query lifecycle

```text
parse URL
  → build query key
  → read fresh cache or fetch
  → validate response
  → expose loading / stale / error / data
  → render recovery actions
```

The component should consume a query model, not reinvent this lifecycle.

---

## Editing a product

```text
load canonical product
  → create local draft
  → edit and validate
  → submit command
  → preserve draft on failure
  → update or invalidate cache on success
```

Never let a failed mutation erase the user's unfinished work by default.

---

## Search and cancellation

```ts
let activeController: AbortController | undefined;

async function search(query: string) {
  activeController?.abort();
  activeController = new AbortController();
  return loadProducts(query, activeController.signal);
}
```

The cache and UI must also ensure that an older result cannot win after a newer query.

---

## Pagination and cache retention

Decide:

- whether previous pages remain visible;
- whether the next page is prefetched;
- how long old pages remain cached;
- how a mutation changes page membership;
- what happens when filters change.

Pagination is a user experience and cache policy together.

---

## Prefetching remote data

Prefetch when:

- the next destination is predictable;
- the request is safe;
- the cost is bounded;
- the data is likely to be used.

Do not prefetch every possible route and overwhelm the network or cache.

---

## A client cache is not a database

Cache entries can:

- expire;
- be evicted;
- be incomplete;
- fail to persist;
- disagree with the server;
- belong to one user or permission context.

Never use a cache as the sole authority for durable business data.

---

## Server state and offline state differ

Offline support requires decisions about:

- local persistence;
- queued mutations;
- conflict resolution;
- retry scheduling;
- user visibility;
- security and data expiry.

A query cache alone does not create an offline architecture.

---

## Practical lab: Cached Administrative API Client

Build a small API client that separates HTTP caching, application/query caching, runtime validation, and user-visible failure states.

The practical makes request identity, freshness, invalidation, mutation behavior, and partial failure observable.

---

## Practical stages 1–4: establish the boundary

1. Implement a `fetch()` wrapper that checks `response.ok` explicitly.
2. Validate response data at the boundary.
3. Model remote UI states.
4. Add search and cancellation.

Simulate 401, 403, 404, 422, 500, timeout, and malformed-data responses.

---

## Practical stages 5–8: query cache fundamentals

5. Build a simple query cache.
6. Add freshness.
7. Deduplicate requests.
8. Add pagination.

Verify that query keys include every relevant input and that stale data remains distinguishable from fresh data.

---

## Practical stages 9–13: mutations and cache truth

9. Add a mutation.
10. Handle server validation.
11. Invalidate after save.
12. Directly update one cache entry.
13. Add an optimistic toggle with rollback.

Document why each mutation uses pessimistic, direct-update, or optimistic behavior.

---

## Practical stages 14–17: resilience and architecture

14. Simulate partial dashboard failure.
15. Compare browser cache and query cache.
16. Add native `FormData` submission.
17. Draw the full data architecture.

Verification: loading, empty, stale, error, recovery, and partial-success states are visible.

---

## Practical extension: conditional requests

Add ETags and conditional requests:

```http
If-None-Match: "version-42"
```

Document which layer owns:

- the HTTP cache;
- the query cache;
- freshness;
- invalidation;
- the final domain model.

---

## Try this yourself

Design the cache keys for:

```text
products by query, sort, page
product by ID
current user
dashboard panel by account and date range
```

Then list which mutations invalidate or directly update each key.

---

## Troubleshooting guide

| Symptom | Likely cause |
|---|---|
| 500 response enters success code | `response.ok` was not checked |
| Old search result replaces new result | missing cancellation or request identity |
| Different filters show the same data | cache key omits an input |
| Every refresh blanks the screen | stale data is discarded unnecessarily |
| Failed save loses the draft | mutation lifecycle owns the form incorrectly |
| Retry duplicates an operation | non-idempotent request has no safety policy |
| One panel breaks the dashboard | independent queries were coupled with `Promise.all()` |
| Cache never updates after save | invalidation or direct update is undefined |

---

## Completion checklist

- [ ] HTTP errors and network errors are distinct;
- [ ] responses are validated before entering domain code;
- [ ] request cancellation prevents stale work;
- [ ] retries are limited and operation-aware;
- [ ] remote UI states distinguish loading, empty, stale, and error;
- [ ] cache keys include all relevant inputs;
- [ ] freshness and invalidation policies are explicit;
- [ ] mutations preserve drafts on failure;
- [ ] optimistic updates have rollback and revalidation rules;
- [ ] partial failures preserve independent useful data.

---

## Misconceptions to leave behind

| Misconception | Better mental model |
|---|---|
| `fetch()` rejects for every 4xx or 5xx | Check `response.ok` explicitly |
| TypeScript proves the server response | Runtime validation proves delivered data |
| Every request should be retried | Retry only safe, useful operations |
| Loading and empty are the same | One is pending; one is a successful zero result |
| Cache means correct forever | Cache means reusable knowledge under a policy |
| Stale means unusable | Stale data may be useful while revalidating |
| Every mutation should be optimistic | Choose based on reversibility and conflict risk |
| Browser cache and query cache are identical | They are different layers with different owners |
| A server-state library replaces API design | It provides mechanisms, not semantics |
| Successful save fixes every cache | Related entries still need reconciliation |

---

## The chapter in one sentence

> **Treat remote data as a lifecycle with explicit request identity, validation, freshness, failure, mutation, and recovery policies.**

---

## Next: Chapter 10

The next chapter will build on client-server architecture with:

- accessibility and inclusive interaction;
- semantic structure and assistive technology;
- keyboard, focus, and form behavior;
- robust component contracts;
- testing the experience rather than only the implementation.

---

## Questions

For one request in your application, can you explain its key, freshness policy, cancellation rule, retry policy, failure states, and invalidation path?

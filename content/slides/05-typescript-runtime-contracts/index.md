---
title: "TypeScript, Runtime Contracts & Safe Data Boundaries"
description: "Chapter 5: model data precisely, narrow unknown values, use generics, and validate every external boundary."
book_number: "5"
weight: 6
---

# TypeScript, Runtime Contracts & Safe Data Boundaries

Make the boundary explicit

**Chapter 5**

Polla Fattah

---

## Today's goal

Understand what TypeScript can prove, what it cannot know, and how runtime validation turns untrusted input into trusted application data.

We will connect:

- inference and explicit types;
- unions, narrowing, and exhaustive state design;
- generics and reusable contracts;
- strictness, DOM typing, and assertions;
- APIs, URLs, storage, forms, and configuration;
- parsers, schemas, branded values, and trusted domain data.

---

## By the end of today you can

- model domain states instead of decorating arbitrary objects;
- use `unknown` at an external boundary;
- narrow values with evidence and discriminated unions;
- write generic result and collection APIs;
- keep strict TypeScript useful rather than ceremonial;
- distinguish a type assertion from a runtime conversion;
- validate API, URL, storage, form, and configuration data;
- separate transport types from domain types;
- create branded identifiers only after validation;
- explain why static types do not replace tests or runtime contracts.

---

## The central lesson

```text
TypeScript describes what the program believes
                 ≠
runtime validation checks what the outside world delivered
```

An annotation is useful for the compiler and editor.

It is not a force field around a value arriving from a network, URL, browser, or user.

---

## The chapter's progression

```text
inference
  → data modeling
  → unions and narrowing
  → generics
  → strictness and DOM typing
  → trust boundaries
  → runtime validation
  → trusted domain data
```

The order matters: prove small facts first, then compose them into safe boundaries.

---

## JavaScript has values; TypeScript adds a model

```js
const response = await fetch("/api/products");
const data = await response.json();
```

JavaScript executes the values that arrive.

TypeScript can describe the values we expect while developing, but its annotations are removed before the browser runs the code.

---

## A type annotation is not validation

```ts
type User = { id: string; name: string };

const user = JSON.parse(input) as User;
console.log(user.name.toUpperCase());
```

The assertion changes the compiler's story.

It does not inspect `input`, check `id`, or create a missing `name`.

---

## Start with inference

```ts
const pageSize = 20;
const status = "loading";
const visible = true;

// pageSize: number
// status: string (in a mutable binding)
// visible: boolean
```

Inference keeps local code readable and lets the implementation remain the source of truth.

Add an annotation when it documents intent, constrains a boundary, or catches an important mistake.

---

## Widening and literal values

```ts
const fixedStatus = "loading"; // "loading"
let changingStatus = "loading"; // string

const config = { mode: "dark" }; // { mode: string }
```

Literal information can widen when a value must remain mutable.

Use literal types deliberately when a small vocabulary is part of the contract.

---

## Model the domain, do not label a guess

```ts
type Product = {
  id: string;
  title: string;
  priceCents: number;
};
```

This is a useful domain model for trusted application data.

It is not evidence that a random JSON object already satisfies the model.

---

## Interfaces describe object shape

```ts
interface Product {
  id: string;
  title: string;
  priceCents: number;
}

function formatProduct(product: Product) {
  return `${product.title}: ${product.priceCents / 100}`;
}
```

Interfaces work well for object contracts that may be extended or implemented across a codebase.

---

## Type aliases compose precisely

```ts
type ProductId = string;
type Currency = "IQD" | "USD";
type ProductSummary = Pick<Product, "id" | "title">;
```

Aliases are especially expressive for unions, tuples, mapped types, conditional types, and domain vocabulary.

Choose the form that communicates the design; both participate in structural typing.

---

## Literal types create a controlled vocabulary

```ts
type Theme = "light" | "dark";
type SortDirection = "ascending" | "descending";

function setTheme(theme: Theme) {}
setTheme("dark");
// setTheme("blue"); // compile-time error
```

Small finite sets should be visible in the type rather than repeated as undocumented strings.

---

## Unions represent alternatives

```ts
type Result = Product | { message: string };

function readTitle(value: Result) {
  if ("title" in value) return value.title;
  return value.message;
}
```

The safe question is not “what do I hope this is?”

It is “what evidence distinguishes the possible members?”

---

## Narrow with `typeof` when the evidence fits

```ts
function toLabel(value: string | number) {
  if (typeof value === "number") {
    return value.toFixed(2);
  }
  return value.toUpperCase();
}
```

Narrowing is a proof step. After the branch, TypeScript allows operations supported by the proven type.

---

## Narrow with property checks

```ts
type Failure = { message: string; code: number };
type Success = { data: Product[] };

function describe(value: Failure | Success) {
  if ("data" in value) return `${value.data.length} products`;
  return `${value.code}: ${value.message}`;
}
```

Property checks are useful, but a stable discriminant is often clearer for important state machines.

---

## Discriminated unions make state explicit

```ts
type LoadState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; message: string };
```

Each state carries exactly the data that makes sense in that state.

This prevents impossible combinations such as `status: "loading"` with stale `error` and `data` fields.

---

## Render state by its discriminant

```ts
function renderProducts(state: LoadState<Product[]>) {
  switch (state.status) {
    case "idle": return "Choose a search";
    case "loading": return "Loading…";
    case "success": return `${state.data.length} results`;
    case "error": return state.message;
  }
}
```

The branch gives the renderer the exact fields valid for that state.

---

## Intersections combine capabilities

```ts
type Identified = { id: string };
type Timestamped = { updatedAt: string };
type StoredProduct = Product & Identified & Timestamped;
```

Use intersections when one value genuinely satisfies multiple independent contracts.

Do not use them to hide a domain model that is becoming difficult to understand.

---

## `unknown` is the honest boundary type

```ts
function receiveExternalValue(value: unknown) {
  // value.toString(); // not allowed without proof
  if (typeof value === "string") return value.trim();
  return "not a string";
}
```

`unknown` says: a value exists, but this function has not earned knowledge about its shape yet.

It is safer than `any` because every operation requires evidence.

---

## A type guard is a proof function

```ts
function isProduct(value: unknown): value is Product {
  if (typeof value !== "object" || value === null) return false;
  const record = value as Record<string, unknown>;
  return typeof record.id === "string"
    && typeof record.title === "string"
    && typeof record.priceCents === "number";
}
```

The return type tells TypeScript what follows when the function returns `true`.

The implementation must justify that claim at runtime.

---

## Type guards can still be wrong

```ts
function isProduct(value: unknown): value is Product {
  return typeof value === "object";
}
```

This compiles, but it lies: arrays, dates, and empty objects pass the test.

A type predicate is not automatically verified by the compiler. Treat it as safety-critical code.

---

## `never` protects exhaustive decisions

```ts
function assertNever(value: never): never {
  throw new Error(`Unhandled state: ${String(value)}`);
}

function label(state: LoadState<unknown>) {
  switch (state.status) {
    case "idle": return "Idle";
    case "loading": return "Loading";
    case "success": return "Ready";
    case "error": return "Failed";
    default: return assertNever(state);
  }
}
```

Adding a new state now creates a compile-time reminder at every incomplete decision.

---

## Generics preserve relationships

```ts
function first<T>(items: T[]): T | undefined {
  return items[0];
}

const firstProduct = first(products); // Product | undefined
const firstNumber = first([1, 2, 3]); // number | undefined
```

Generics are not “any with extra syntax”. They carry a relationship between inputs and outputs.

---

## A generic result keeps success data precise

```ts
type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: string };

function show(result: ApiResult<Product[]>) {
  if (!result.ok) return result.error;
  return result.data.map(product => product.title);
}
```

The common result contract is reusable while `T` preserves the domain-specific payload.

---

## Constrain a generic when it needs a capability

```ts
function getById<T extends { id: string }>(items: T[], id: string) {
  return items.find(item => item.id === id);
}
```

The constraint does not say every `T` is exactly an object with only `id`.

It says the function may safely rely on `id` while preserving additional fields.

---

## Generic components should describe relationships

```ts
type TableProps<T> = {
  rows: T[];
  getKey: (row: T) => string;
  renderRow: (row: T) => string;
};
```

The table does not need to know whether a row is a product, lecture, or user.

The caller supplies the domain-specific relationship once.

---

## Utility types transform an existing contract

```ts
type ProductDraft = Omit<Product, "id">;
type ProductPreview = Pick<Product, "id" | "title">;
type EditableProduct = Partial<Product>;
```

Utility types are useful for views and transitions, but they should not replace clear domain states.

---

## Strictness catches boundary mistakes early

Prefer a strict baseline:

```json
{
  "strict": true,
  "noUncheckedIndexedAccess": true,
  "exactOptionalPropertyTypes": true
}
```

The exact set depends on the project, but the principle is stable: make uncertainty visible where it matters.

---

## Avoid implicit `any`

```ts
function format(value) {
  return value.name;
}
```

An implicit `any` turns off the very feedback TypeScript is meant to provide.

If a value is unknown, write `unknown` and decide how to prove it.

---

## Null and undefined are part of the model

```ts
function firstTitle(items: Product[]): string | undefined {
  return items[0]?.title;
}

const title = firstTitle(products) ?? "No products";
```

An empty result is not a failed type. It is a state the caller must handle.

---

## Indexed access can be unsafe

```ts
const first = products[0];

if (first) {
  console.log(first.title);
}
```

Even when an array is typed as `Product[]`, an arbitrary index may not contain a product.

`noUncheckedIndexedAccess` makes that possibility explicit.

---

## DOM APIs are runtime boundaries too

```ts
const form = document.querySelector("#search-form");

if (!(form instanceof HTMLFormElement)) {
  throw new Error("Search form is missing");
}
```

The selector returns a nullable, broad value. Narrow it before using form-specific behavior.

---

## Type the element and the event

```ts
const input = document.querySelector<HTMLInputElement>("#query");

input?.addEventListener("input", (event) => {
  const target = event.currentTarget as HTMLInputElement;
  console.log(target.value);
});
```

Use the most specific safe DOM type available, and remember that the element can still be absent.

---

## The dangerous API shortcut

```ts
const data = (await response.json()) as Product[];
```

This is convenient at the exact point where convenience is most dangerous.

The network response is outside the compiler's control. Treat it as `unknown` until it is parsed.

---

## Assertions, casts, and conversions are different

```ts
const value = input as number;       // assertion: no runtime work
const number = Number(input);        // conversion: runtime work
const parsed = JSON.parse(input);    // parsing: produces a runtime value
```

An assertion changes static knowledge.

A conversion or parser changes or inspects a runtime value.

---

## What counts as a trust boundary?

```text
API response       URL and query string
browser storage    form input
environment config imported files
postMessage        third-party SDKs
```

Every source outside the current trusted function may be malformed, stale, partial, or surprising.

---

## URL values are strings, even when they look numeric

```ts
const rawPage = new URLSearchParams(location.search).get("page");
const page = rawPage === null ? 1 : Number(rawPage);

if (!Number.isInteger(page) || page < 1) {
  throw new Error("Invalid page");
}
```

Parsing and domain checks are separate decisions. `Number("")` becoming `0` may be a valid JavaScript conversion but an invalid page.

---

## Browser storage is untrusted text

```ts
const raw = localStorage.getItem("preferences");
const value: unknown = raw === null ? null : JSON.parse(raw);
```

Storage may contain old versions, manually edited values, or invalid JSON.

Read it as an external payload, then validate a versioned shape.

---

## Forms produce strings and absence

```ts
const formData = new FormData(form);
const rawEmail: unknown = formData.get("email");

if (typeof rawEmail !== "string" || !rawEmail.includes("@")) {
  return showError("Enter a valid email");
}
```

The HTML control type is not enough to guarantee the value your domain logic expects.

---

## Manual validation is a parser

```ts
function parseProduct(value: unknown): Product {
  if (typeof value !== "object" || value === null) {
    throw new Error("Product must be an object");
  }

  const record = value as Record<string, unknown>;
  if (typeof record.id !== "string") throw new Error("Product id is invalid");
  if (typeof record.title !== "string") throw new Error("Product title is invalid");
  if (typeof record.priceCents !== "number") throw new Error("Product price is invalid");

  return { id: record.id, title: record.title, priceCents: record.priceCents };
}
```

The returned `Product` is earned by checks and reconstruction, not by a blind assertion.

---

## Parse, then trust the result

```ts
const payload: unknown = await response.json();
const product = parseProduct(payload);

// Product-specific application code starts here.
renderProduct(product);
```

Keep parsing close to the boundary. Keep the rest of the application free from repeated shape checks.

---

## Validation errors should help the caller

Useful errors identify:

- which boundary failed;
- which field was unexpected;
- what kind of value was expected;
- whether the response was malformed or the request failed.

Do not include tokens, passwords, or complete sensitive payloads in error messages.

---

## Schema libraries make repetitive checks composable

```ts
const ProductSchema = z.object({
  id: z.string(),
  title: z.string(),
  priceCents: z.number().int().nonnegative(),
});
```

A schema can centralize parsing, reuse nested rules, report paths, and derive static types.

The library does not remove the need to design the domain contract.

---

## Safe parsing returns a controlled result

```ts
const result = ProductSchema.safeParse(payload);

if (!result.success) {
  return { ok: false, error: result.error.issues };
}

return { ok: true, data: result.data };
```

This makes invalid input an explicit branch instead of an unexpected exception deep in rendering code.

---

## Transport data is not always domain data

```ts
type ProductResponse = {
  product_id: string;
  display_name: string;
  price_cents: number;
};

type Product = {
  id: string;
  title: string;
  priceCents: number;
};
```

The boundary can validate the transport shape and map it into the vocabulary used by the application.

---

## A complete API boundary

```ts
async function loadProducts(): Promise<ApiResult<Product[]>> {
  let response: Response;
  try {
    response = await fetch("/api/products");
  } catch {
    return { ok: false, error: "Network request failed" };
  }

  if (!response.ok) return { ok: false, error: `HTTP ${response.status}` };

  const payload: unknown = await response.json();
  return parseProducts(payload);
}
```

Transport failure and schema failure are separate facts and should remain distinguishable.

---

## Keep raw data unknown at the edge

```text
fetch / storage / URL / form
             ↓
           unknown
             ↓ parse + validate
      trusted transport data
             ↓ map
       trusted domain model
             ↓
       components and features
```

The farther a value travels from the edge, the less useful it is to keep asking whether it is valid.

---

## The boundary architecture

```text
adapter       knows the external format
parser        checks runtime shape
mapper        creates domain vocabulary
application   consumes trusted values
view          renders explicit state
```

Each layer has a small responsibility and a clear reason to change.

---

## The parse-then-trust principle

```ts
function useProducts(products: Product[]) {
  // No API-shape checks here.
  return products.map(product => product.title);
}
```

Trust should be established once at the boundary, then preserved by types and module boundaries.

Repeated checks in every component usually signal that the boundary is in the wrong place.

---

## `satisfies` checks without widening useful literals

```ts
const routes = {
  home: "/",
  playground: "/playground",
} satisfies Record<string, `/${string}`>;
```

The object is checked against the contract while retaining precise keys and values for later inference.

This is often better than annotating the whole object as `Record<string, string>`.

---

## When assertions are legitimate

An assertion can be reasonable when:

- a platform API is typed too broadly;
- a checked invariant is understood by the compiler but not expressible locally;
- a test fixture deliberately models a controlled case;
- the assertion is close to the proof and documented.

It is risky when it is used to skip parsing, null checks, or domain decisions.

---

## Avoid double assertions

```ts
const impossible = value as unknown as Product;
```

This pattern can force unrelated types together and hides the missing proof.

If the boundary is uncertain, keep the value as `unknown` and write the parser that makes the transition explicit.

---

## Non-null assertions hide a missing state

```ts
const element = document.querySelector("#app")!;
```

The `!` silences `null` without changing runtime behavior.

Prefer a checked lookup, a required-element helper, or an initialization path that makes absence impossible.

---

## Structural typing is useful and subtle

```ts
type User = { id: string };
type Product = { id: string };

const product: Product = { id: "p-1" };
const user: User = product;
```

Both shapes satisfy the same structure, even if the domain meanings differ.

Shape compatibility does not automatically communicate semantic identity.

---

## Branded types protect semantic identifiers

```ts
type ProductId = string & { readonly __brand: "ProductId" };
type UserId = string & { readonly __brand: "UserId" };

function loadProduct(id: ProductId) {}
```

The compiler can now distinguish two strings that represent different kinds of identifier.

The brand has no runtime representation.

---

## Create a brand only after validation

```ts
function parseProductId(value: unknown): ProductId {
  if (typeof value !== "string" || !/^p-[a-z0-9-]+$/.test(value)) {
    throw new Error("Invalid product id");
  }
  return value as ProductId;
}
```

The assertion is local and justified by the parser's runtime rule.

Never export a public “brand anything” helper that bypasses the boundary.

---

## Brands are useful when the cost is justified

Consider them for:

- identifiers that are frequently confused;
- validated URLs or paths;
- normalized currency codes;
- security-sensitive tokens with distinct lifecycles.

Do not brand every primitive. Extra vocabulary should reduce real mistakes, not create ceremony.

---

## Static contracts are not shared runtime validation

```text
shared TypeScript type  → agreement during development
runtime schema          → verification of delivered data
generated API types     → synchronized description
```

Even generated types can become stale or be bypassed by a broken server.

The receiving application still owns its trust boundary.

---

## Choose validation proportionately

```text
small local constant     → direct type / simple check
stable internal module   → typed constructor or parser
external API             → schema and useful errors
security-sensitive data  → strict validation, tests, logging policy
```

The goal is reliable boundaries, not maximum ceremony everywhere.

---

## Typed errors preserve failure meaning

```ts
type BoundaryError =
  | { kind: "network"; message: string }
  | { kind: "http"; status: number }
  | { kind: "schema"; issues: string[] };

type Result<T> =
  | { ok: true; data: T }
  | { ok: false; error: BoundaryError };
```

Callers can render, retry, report, or ignore failures based on their actual cause.

---

## TypeScript does not replace tests

Types catch many inconsistencies before execution.

Tests still verify behavior, boundary cases, compatibility, and user-visible outcomes.

Test malformed payloads, missing fields, old storage versions, invalid query strings, and empty results.

---

## TypeScript does not replace security

Compile-time types do not sanitize HTML, authorize a user, protect a secret, or prevent a malicious server response.

Security checks must happen at runtime and at the correct trust boundary.

---

## A malformed response should fail clearly

```ts
const response = {
  products: [
    { id: "p-1", title: "Valid", priceCents: 1000 },
    { id: "p-2", title: 42, priceCents: "free" },
  ],
};
```

Do not render the first item and silently accept the second.

Decide whether the contract is all-or-nothing, item-level recovery, or partial data with an explicit warning.

---

## Replace the assertion with `unknown`

```ts
const payload: unknown = response;

const parsed = parseProducts(payload);
if (!parsed.ok) {
  showBoundaryError(parsed.error);
}
```

The compiler now forces the design to answer what happens when the payload is not valid.

---

## Validate, then construct the trusted model

```ts
function parseProducts(value: unknown): ApiResult<Product[]> {
  if (!Array.isArray(value)) {
    return { ok: false, error: "products must be an array" };
  }

  const products = value.map(parseProduct);
  return { ok: true, data: products };
}
```

In production, make the item failure shape explicit and avoid allowing an exception to erase useful context.

---

## The trusted core should stay boring

```ts
function total(products: Product[]) {
  return products.reduce((sum, product) => sum + product.priceCents, 0);
}
```

Once data is trusted, domain functions should focus on domain behavior.

If every function still checks whether `priceCents` is a number, the boundary has not done enough work.

---

## Common misconceptions

| Misconception | Better mental model |
|---|---|
| `as Product` validates JSON | It only changes static interpretation |
| `unknown` is inconvenient | It marks work the boundary must do |
| `any` is faster | It removes useful feedback |
| shared types guarantee the API | They describe an agreement, not delivery |
| schemas make domain design unnecessary | They validate a contract you still choose |
| strictness means more code everywhere | It makes important uncertainty visible |

---

## Practical lab: Build a Safe Data Boundary

Create a small API boundary that parses `unknown`, validates the response, and exposes trusted product data to application code.

The practical moves from static modeling to malformed payloads, manual parsing, schema validation, URL and storage boundaries, and branded IDs.

---

## Practical stages 1–3: model uncertainty

1. Model the domain product and its load states.
2. Test inference, literal types, and generic result types.
3. Introduce `unknown` where the API response enters.

Do not begin by asserting that the response is already a `Product[]`.

---

## Practical stages 4–6: make state and failure explicit

4. Render every discriminated load state exhaustively.
5. Add a generic `ApiResult<T>`.
6. Create an intentionally unsafe API response with valid and malformed records.

Observe how the unsafe version spreads assumptions into the UI.

---

## Practical stages 7–9: replace trust with parsing

7. Replace the assertion with `unknown`.
8. Write a manual parser with useful field errors.
9. Compare the parser with a schema library.

Record the maintenance trade-off: readability, reuse, error paths, dependency cost, and change frequency.

---

## Practical stages 10–13: finish the boundary map

10. Validate URL state.
11. Validate browser storage.
12. Create branded IDs only after validation.
13. Draw the trust architecture from raw input to trusted domain data.

Verification: invalid data cannot enter the trusted model silently.

---

## Try this yourself

Add a new `archived` product state and update every renderer.

Then add a server field that is optional in the transport response but required by the domain model.

Where should the default be applied?

At the parser, mapper, or component? Explain the boundary decision.

---

## Troubleshooting guide

| Symptom | Likely cause |
|---|---|
| Everything became `any` | An untyped boundary leaked inward |
| Assertions appear everywhere | Parsing is missing or too far away |
| Components repeat shape checks | Trusted data is not established once |
| Union branches feel awkward | Add a discriminant or redesign the state |
| A guard compiles but fails in production | The predicate claims more than it checks |
| Old storage breaks after a release | Add versions and migration/validation rules |

---

## Completion checklist

- [ ] local values rely on inference where appropriate;
- [ ] domain states use explicit, meaningful unions;
- [ ] external values enter as `unknown`;
- [ ] parsers return useful failure information;
- [ ] transport and domain models are separated where needed;
- [ ] branded values are created only after validation;
- [ ] tests cover malformed and stale inputs;
- [ ] trusted core functions do not repeat boundary checks.

---

## The chapter in one sentence

> **Use TypeScript to describe and connect trusted program states; use runtime validation to earn trust at every external boundary.**

---

## Next: Chapter 6

The next chapter turns these contracts into component architecture:

- component boundaries;
- props and composition;
- controlled and uncontrolled state;
- reusable UI contracts;
- accessibility as a design constraint;
- testing behavior at the boundary.

---

## Questions

Which value in your current application is trusted only because an assertion says it is?

That is the first boundary worth making explicit.

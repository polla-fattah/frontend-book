---
title: "Runtime-Validated Data Boundary and Typed Event Hub"
weight: 5
---

# Practical 05 — Runtime-Validated Data Boundary and Typed Event Hub

Related: [Chapter 5]({{< relref "/book/Chapter_05_TypeScript_Runtime_Contracts_and_Safe_Data_Boundaries.md" >}}) · [Lecture slides]({{< relref "/slides/05-typescript-runtime-contracts/index.md" >}})

## Objective

Build a resilient API trust boundary in TypeScript that ingests `unknown` external data, enforces runtime validation before types are asserted, transforms verified input into trusted domain records, and surfaces user-friendly diagnostics when contracts fail.

You will test your boundary against a rigorous matrix of valid, malformed, incomplete, and unexpected payloads. Furthermore, you will connect this laboratory to Chapter 4 by upgrading the pure JavaScript event hub with compile-time generic event maps.

## Prerequisites and setup

You need Node.js (v18+) and the TypeScript compiler (`tsc`).

Create your exercise workspace:

```text
chapter-05-boundary/
├── src/
│   ├── types.ts
│   ├── boundary.ts
│   ├── event-hub.ts
│   └── app.ts
├── index.html
├── package.json
└── tsconfig.json
```

Ensure your `tsconfig.json` enforces full strictness:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUncheckedIndexedAccess": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"]
}
```

Do not use `as SomeType` type assertions to bypass validation. Every domain record must be proven at runtime before it can enter application state.

## Stage 1 — Model domain records and discriminated results

In `src/types.ts`, define your domain models using discriminated unions:

```typescript
export type Result<T, E = BoundaryError> =
  | { readonly ok: true; readonly data: T }
  | { readonly ok: false; readonly error: E };

export interface ServiceRecord {
  readonly id: string;
  readonly name: string;
  readonly feeIqd: number;
  readonly isAvailable: boolean;
  readonly department: 'Civil' | 'Housing' | 'Legal';
}

export class BoundaryError extends Error {
  constructor(
    public readonly kind: 'transport' | 'schema',
    message: string,
    public readonly issues?: readonly string[]
  ) {
    super(message);
    this.name = 'BoundaryError';
  }
}
```

## Stage 2 — Implement the runtime parser and test matrix

In `src/boundary.ts`, implement a validation parser `parseServiceRecord(raw: unknown): Result<ServiceRecord, BoundaryError>`. You may implement this with explicit property checks or with a schema parsing library (such as Zod).

Execute the parser against a four-case test matrix:

1. **Valid Case:**
   ```json
   { "id": "SR-1042", "name": "Residence Certificate", "feeIqd": 25000, "isAvailable": true, "department": "Civil" }
   ```
   *Expected:* Returns `{ ok: true, data: ServiceRecord }`.
2. **Malformed Case:**
   ```json
   { "id": "SR-1042", "name": "Residence Certificate", "feeIqd": "twenty-five thousand", "isAvailable": "yes", "department": "Civil" }
   ```
   *Expected:* Fails schema validation with specific messages indicating `feeIqd` must be a number and `isAvailable` must be a boolean.
3. **Incomplete Case:**
   ```json
   { "id": "SR-1042", "department": "Civil" }
   ```
   *Expected:* Fails schema validation reporting missing required fields (`name`, `feeIqd`, `isAvailable`).
4. **Unexpected Backend Case:**
   ```json
   { "status": "error", "code": 503, "message": "Database cluster failover in progress" }
   ```
   *Expected:* Correctly identified as an incompatible schema without crashing with a `TypeError`.

**Verify:** Run `tsc --noEmit`. Verify that `result.data` is completely inaccessible on `{ ok: false }` branches, and that narrowing on `result.ok` permits safe access to all domain fields.

## Stage 3 — Distinguish transport failures from schema failures and surface to UI

In `src/app.ts`, coordinate network fetching, validation, and DOM updates:

1. Differentiate network disconnects and HTTP 500 errors (`kind: 'transport'`) from schema decoding errors (`kind: 'schema'`).
2. Surface appropriate feedback to the user:
   * **Transport Errors:** Inform the user: *"Network connection unavailable. Please check your connection and retry."*
   * **Schema Errors:** Inform the user: *"Service record received in an unrecognized format. Our technical team has been alerted."* Log detailed structural issues to the console without exposing sensitive internals to the user interface.

**Verify:** Trigger each error condition in the browser UI. Verify that error messages are rendered inside an accessible container (`role="alert"` or `aria-live="polite"`).

## Stage 4 (Chapter 4 Extension) — Strongly typed event hub

Extend the publish-subscribe event hub from Practical 04 with a compile-time generic contract:

```typescript
export interface CitizenEventMap {
  'search:start': { query: string; timestamp: number };
  'search:success': { query: string; results: readonly ServiceRecord[] };
  'search:error': { query: string; error: BoundaryError };
  'service:selected': { serviceId: string };
}

export function createTypedEventHub<Events extends Record<string, unknown>>() {
  const subscribers = new Map<keyof Events, Set<(payload: any) => void>>();

  return {
    on<K extends keyof Events>(
      event: K,
      listener: (payload: Events[K]) => void,
      options?: { signal?: AbortSignal; once?: boolean }
    ): () => void {
      // Manage subscription and AbortSignal cleanup...
    },

    emit<K extends keyof Events>(event: K, payload: Events[K]): void {
      // Isolate listener execution and dispatch...
    }
  };
}
```

**Verify:** In `src/app.ts`, instantiate `createTypedEventHub<CitizenEventMap>()`.
1. Verify that `hub.emit('search:start', { query: 'res', timestamp: Date.now() })` compiles cleanly.
2. Verify that `hub.emit('invalid:channel', {})` fails compilation with an invalid event name error.
3. Verify that `hub.emit('search:start', { query: 123 })` fails compilation due to mismatched payload shape.

## What to submit

Submit your TypeScript source files (`src/types.ts`, `src/boundary.ts`, `src/event-hub.ts`, `src/app.ts`) and a completed verification report:

| Target | Requirement | Observed Evidence | Explanation | Confounders or Limits |
| :--- | :--- | :--- | :--- | :--- |
| **Type Erasure Awareness** | Zero `as` assertions on external JSON | Code audit of `boundary.ts` | All JSON parsed through runtime validator | Checked via compiler |
| **Payload Matrix** | All 4 test cases handled predictably | Test runner output | Valid parsed; malformed/incomplete/error rejected | Tested in test harness |
| **Error Differentiation** | Transport vs schema errors separated | UI error snapshot | User receives actionable context; diagnostics logged | Network throttled in DevTools |
| **Typed Event Hub** | Compile-time check on events & payloads | `tsc --noEmit` failure test | Invalid event names and payloads rejected by tsc | Verified against EventMap |

## When an experiment gives an unexpected result

* **TypeScript permits reading invalid properties:** Ensure you did not cast the fetch result as `any` or use `as ServiceRecord`. Input must remain `unknown` until narrowed.
* **`BoundaryError` instanceof check fails:** When compiling TypeScript to older targets (ES5), subclassing `Error` can break prototype chains. Ensure `"target": "ES2022"` is configured in `tsconfig.json`.
* **Optional properties become undefined:** Remember that `noUncheckedIndexedAccess: true` requires checking whether array items or dynamic dictionary keys are defined before accessing their properties.

# Practical 09 — Cached Administrative API Client

Related chapter: Chapter 9

## Objective

Build a small API client that separates HTTP caching, application/query caching, runtime validation, and user-visible failure states.

## Stages

1. Implement a `fetch()` wrapper that handles `response.ok` explicitly.
2. Validate response data at the boundary.
3. Add request deduplication and stale/fresh state.
4. Simulate 401, 403, 404, 422, 500, timeout, and malformed data.
5. Preserve partial dashboard data when one panel fails.

## Verification

- HTTP errors and network errors are represented differently.
- Query cache behavior is distinguishable from the browser HTTP cache.
- Retry behavior is limited to safe or explicitly idempotent operations.
- Loading, empty, stale, error, and recovery states are visible.

## Extension

Add conditional requests with ETags and document which layer owns invalidation.


# Practical 05 — Runtime-Validated Data Boundary

Related chapter: Chapter 5

## Objective

Build a small API boundary that parses `unknown`, validates the response, and exposes trusted domain data to application code.

## Stages

1. Model an external product response as `unknown`.
2. Write a minimal parser or use a schema library.
3. Return a discriminated success/failure result.
4. Add malformed, partial, and unexpected responses.
5. Keep TypeScript assertions out of the trust boundary.

## Verification

- Invalid data cannot enter the trusted domain model silently.
- Validation errors contain useful context without exposing secrets.
- Tests distinguish transport failure from schema failure.
- Branded types, if used, are created only after validation.

## Extension

Compare hand-written validation with a schema library and record the maintenance trade-off.


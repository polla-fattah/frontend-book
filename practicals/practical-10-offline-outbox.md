# Practical 10 — Offline Outbox and Recovery

Related chapter: Chapter 10

## Objective

Build an offline-capable field-inspection outbox using IndexedDB, with explicit retry, idempotency, and conflict decisions.

## Stages

1. Persist a draft and an outbox record.
2. Simulate network loss and application reload.
3. Flush records with exponential backoff and a retry limit.
4. Add idempotency keys and server acknowledgment states.
5. Treat `navigator.onLine` and Background Sync as hints/enhancements, not proof or foundations.

## Verification

- Records survive reload.
- Duplicate submission is prevented or detected.
- Permanent failures are visible and recoverable.
- The app remains useful without Background Sync.

## Extension

Add conflict resolution for a record changed on the server while the client was offline.


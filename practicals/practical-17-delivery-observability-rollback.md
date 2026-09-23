# Practical 17 — Delivery, Observability, and Rollback Loop

Related chapter: Chapter 17

## Objective

Design and rehearse a safe frontend release from commit to deployment, observation, rollback, and cleanup.

## Stages

1. Produce a reproducible build artifact.
2. Run type checks, linting, unit/integration tests, and a smoke test.
3. Deploy to a preview environment.
4. Add release identity, error reporting, performance signals, and breadcrumbs.
5. Simulate a bad release and use a rollback or kill switch.
6. Remove a completed feature flag and document the change.

## Verification

- The tested artifact is the deployed artifact.
- Feature flags do not act as authorization.
- Alerts have an owner and an operational response.
- Rollback is tested rather than merely documented.

## Extension

Write a short frontend runbook covering detection, triage, mitigation, rollback, communication, and follow-up.


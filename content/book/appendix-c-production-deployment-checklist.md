# Appendix C — Front-End Production Deployment Checklist

This checklist adapts the strongest operational ideas from the earlier manuscript. It is a review aid, not a substitute for system-specific threat modeling, performance measurement, accessibility review, or operational ownership.

## 1. Build and artifact integrity

- [ ] The production artifact is reproducible from a known commit.
- [ ] Dependency resolution uses a reviewed lockfile.
- [ ] Type checking, linting, and required tests run in CI.
- [ ] Source maps and release identity are handled deliberately.
- [ ] Generated assets have appropriate cache and invalidation behavior.
- [ ] No secrets or private configuration are present in browser-delivered assets.

## 2. Security boundaries

- [ ] All runtime data crossing a trust boundary is validated.
- [ ] Authentication and authorization are enforced by the server.
- [ ] CORS rules are narrow and are not mistaken for access control.
- [ ] Cookie, CSRF, token, redirect, and logout behavior are documented.
- [ ] Dangerous HTML, URL, script, and style sinks have been reviewed.
- [ ] CSP and related browser-isolation policies are tested with real integrations.
- [ ] Third-party scripts and dependencies have an owner and review process.

## 3. Performance and accessibility

- [ ] Critical routes have field and lab performance evidence.
- [ ] LCP, INP, and CLS are reviewed using current definitions and p75 field data.
- [ ] Lighthouse is used diagnostically, not as the sole release objective.
- [ ] Long tasks, large assets, layout shifts, and memory behavior have been investigated where relevant.
- [ ] Keyboard operation, focus behavior, accessible names, labels, and error associations are tested.
- [ ] Important flows are checked with representative locales, long text, and RTL where applicable.
- [ ] Reduced-motion and progressive-enhancement behavior are considered.

## 4. Caching, resilience, and recovery

- [ ] HTTP cache, application/query cache, Cache Storage, and browser persistence have distinct owners.
- [ ] Stale data, partial failure, retry, timeout, and recovery states are visible.
- [ ] Offline behavior has an explicit scope rather than an implied promise.
- [ ] Mutations have idempotency, conflict, and retry decisions.
- [ ] Service Worker and cache-version transitions are tested.
- [ ] A rollback or kill-switch path has been rehearsed.

## 5. Observability and operations

- [ ] Release identity connects errors, performance events, and deployments.
- [ ] User-impacting journeys have meaningful product and technical signals.
- [ ] Browser telemetry respects privacy, sampling, and data-minimization requirements.
- [ ] Alerts have thresholds, owners, and response instructions.
- [ ] Feature flags have expiry owners and are not used as authorization.
- [ ] Compatibility and migration paths are documented for important clients.

## 6. Architecture sign-off

- [ ] The design satisfies explicit product and organizational requirements.
- [ ] Complexity has a named benefit and an owner.
- [ ] The decision records alternatives and rejected options.
- [ ] Failure modes and blast radius are understood.
- [ ] The smallest coherent solution has been considered.
- [ ] The review date and conditions for revisiting the decision are recorded.


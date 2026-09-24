# Practical 13 — Secure a Front-End Application Boundary

Related chapter: Chapter 13

## Objective

Review and harden a small application boundary involving untrusted input, cross-origin requests, cookies, OAuth-style redirects, and dangerous sinks.

## Stages

1. Trace untrusted input from URL, API, and user form into the UI.
2. Replace unsafe HTML construction with text insertion or a reviewed sanitizer.
3. Observe a CORS failure and distinguish it from server authorization.
4. Add a CSRF decision for cookie-authenticated mutations.
5. Review CSP, framing, COOP/COEP/CORP, and integration trade-offs.

## Verification

- A browser flag cannot grant authorization.
- CORS does not authenticate or authorize callers.
- Access-token validation remains server-side.
- Security changes document affected integrations and failure behavior.

## Extension

Compare a same-origin session/BFF design with a browser-held bearer-token design.


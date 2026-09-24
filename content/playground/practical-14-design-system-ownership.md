# Practical 14 — Design-System Package and Ownership Map

Related chapter: Chapter 14

## Objective

Design a small shared UI package without turning every product-specific component into a design-system primitive.

## Stages

1. Identify repeated foundations, primitives, and domain components.
2. Define token ownership and semantic naming.
3. Create a small package boundary and public API.
4. Document compatibility, versioning, and affected consumers.
5. Map which teams own the package, product components, and release process.

## Verification

- The shared package has a small stable surface.
- Domain-specific behavior remains with the product team.
- Accessibility and visual changes have an explicit review path.
- The package does not become a hidden global dependency for unrelated domains.

## Extension

Compare a monorepo package boundary with an independently deployed micro-frontend and explain why they solve different problems.


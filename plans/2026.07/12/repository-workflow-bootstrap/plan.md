# Repository workflow bootstrap

## Status

Implemented on 2026-07-12.

## Goal

Establish a compact, agent-aware repository structure for source-backed AI
investigations, curated knowledge, spec-driven local tooling, and dated plans.

## Scope

- Define the evidence maturation layers and promotion gates.
- Add routing-only agent guidance and a detailed workflow contract.
- Reserve committed areas for investigations, knowledge, tooling, and specs.
- Ignore the local evidence workspace and generated artifacts.
- Establish open and closed plan indexes using the requested date buckets.

## Non-goals

- Implement a CLI or choose its language.
- Implement the website renderer or GitHub Pages deployment.
- Modify either reference repository.

## Exit criteria

- The repository boundaries are documented and represented on disk.
- `.cache/` and common generated output are ignored.
- Complex rendering work is decomposed into a separate open plan.

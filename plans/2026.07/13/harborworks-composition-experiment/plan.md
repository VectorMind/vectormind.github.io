# Harborworks manifest-composition experiment

## Status

Approved for evidence-first experimentation on 2026-07-13.

## Problem

The composable-context whitepaper proposes a unified navigable surface over
multiple context repositories, but the flattening and repository-prefiltering
claims have not yet been tested. A durable manifest contract would be
premature until collisions, provenance, import topology, and coarse filtering
have been exercised against realistic fixtures.

## Goal

Build a small, reproducible Harborworks fixture corpus and an experimental
composer that can compare separate repositories, naive physical flattening,
and a namespace-preserving logical catalog. Measure whether repository-level
scope filtering usefully reduces the candidate surface and where artifact-level
selection remains necessary.

## Scope

- Preserve nine small simulated context repositories as investigation inputs
  under `memory/2026-07/13/harborworks-composition-experiment/fixtures/`.
- Give each repository shallow skills that route to its `knowledge_base/` and
  trivial Python or Node CLI rather than embedding domain logic.
- Exercise duplicate paths, duplicate skill names, diamond imports, import
  order, incompatible revisions, export boundaries, and policy intersection.
- Keep the experimental composer in `.cache/src/harborworks-composition/` and
  raw outputs in `.cache/results/harborworks-composition/`.
- Record reproducible methods, compact observations, limitations, and open
  decisions in the investigation folder.

## Non-goals

- Do not define the durable manifest specification yet.
- Do not promote the experimental composer into committed `src/` yet.
- Do not select a package manager or add third-party dependencies.
- Do not claim agent-discovery or prompt-efficiency improvements without a
  later harness/model evaluation.
- Do not commit nested Git metadata, generated catalogs, or raw run reports.

## Open points

- **OP-001 - Manifest syntax:** Decide after the trials whether the committed
  format should be YAML, JSON, TOML, or another representation. The fixture
  uses JSON-compatible YAML only to keep the prototype dependency-free.
- **OP-002 - Artifact identity:** Confirm whether
  `(context-id, revision, repository-relative path)` is sufficient or whether
  releases and content digests must also be normative.
- **OP-003 - Prefilter semantics:** Determine whether repository scopes are
  optional discovery hints or a required composition feature.
- **OP-004 - Policy resolution:** Determine which policy fields intersect,
  inherit, or make composition fail closed.
- **OP-005 - Locking:** Determine whether immutable revisions belong directly
  in the manifest or in a generated lockfile.

## Phases

1. Create and review the Harborworks fixture corpus and scenario definitions.
2. Implement the scratch composer and deterministic catalog/filter operations.
3. Run the positive and negative scenarios and preserve compact evidence.
4. Review findings and settle the open points needed for a durable contract.
5. Write `src/specification/composition/`, promote proven code into `src/`, and
   add focused tests only after the manifest model is accepted.

## Risks

- Synthetic fixtures may prove deterministic mechanics without predicting
  real model discovery quality.
- Repository-level labels may appear precise while still retaining irrelevant
  artifacts inside selected repositories.
- A materialized tree may hide collisions or erase provenance unless it is
  treated only as a catalog rendering.
- Fixture manifests may accidentally harden into a specification before the
  negative cases are understood.

## Exit criteria

- The fixture corpus is small, realistic, source-readable, and reproducible.
- The logical catalog retains context, revision, path, kind, scope, and policy.
- Duplicate paths are reported rather than silently overwritten.
- Reordering the same imports produces the same catalog identity set.
- Repository filtering is compared with artifact filtering against a golden
  selection for two functions and three domains.
- Negative revision and policy scenarios fail visibly.
- The investigation states what the prototype demonstrates and what remains
  unvalidated.

# Harborworks manifest-composition experiment

**Date:** 2026-07-13  
**Status:** Deterministic mechanics and a full-union materialization run are
complete; manifest contract and named-harness evaluation remain open.

## Question

Can multiple context repositories be presented as one navigable surface
without destructive flattening, and does repository-level scope filtering add
useful selection power before artifact-level harness discovery?

## Scope

This investigation preserves a synthetic but repository-shaped corpus under
[`fixtures/`](fixtures/). It tests deterministic composition mechanics only:
imports, exports, artifact identity, collision visibility, scope filtering,
revision conflicts, policy conflicts, CLI reachability, and import order.

It does not test an LLM, prompt token use, semantic retrieval, malicious
instructions, real Git resolution, signatures, or authority-system exports.

## Inputs and provenance

- The composable-context [idea note](../../12/composable-context/readme.md), both
  whitepaper drafts, and both 2026-07-13 reviews were read on 2026-07-13.
- The nine Harborworks repositories are deliberately synthetic investigation
  inputs created on 2026-07-13. They do not represent an external organization
  or authoritative domain knowledge.
- The manifests use JSON-compatible YAML and simulated revision strings. This
  avoids third-party parser and Git-network dependencies; it is not a manifest
  format decision.
- Raw catalogs and materialized overlays remain local under
  `.cache/results/harborworks-composition/run-001/`.
- The Run 002 harness surface is generated locally under
  `.cache/harborworks-operations-workbench/`.

## Fixture topology

The corpus contains one always-available core, three function contexts, four
domain contexts, and one composing workbench:

| Role | Context repository | Runtime |
| --- | --- | --- |
| Core | `harborworks-context-core` | Python |
| Function | `harborworks-analysis-methods` | Python |
| Function | `harborworks-briefing-methods` | Node |
| Function distractor | `harborworks-remediation-methods` | Python |
| Domain | `harborworks-software-delivery` | Node |
| Domain | `harborworks-data-governance` | Python |
| Domain | `harborworks-customer-operations` | Node |
| Domain distractor | `harborworks-facilities-operations` | Python |
| Composer | `harborworks-operations-workbench` | Node |

Every repository exports two knowledge files, six shallow skills, and one
dependency-free CLI. Each skill instructs the consumer to read its owning
`knowledge_base/overview.md` and invoke its `src` CLI. Domain facts are not
embedded in skill instructions.

The resolved workbench graph has 9 repositories and 27 unique import edges.
Repeated transitive imports exercise diamond resolution. Five repository-
relative paths collide intentionally:

- `knowledge_base/glossary.md` across 9 repositories;
- `knowledge_base/overview.md` across 9 repositories;
- `skills/summarize-status/SKILL.md` across 5 repositories;
- `src/cli.py` across 5 repositories;
- `src/cli.mjs` across 4 repositories.

## Method

The scratch implementation at
`.cache/src/harborworks-composition/compose.py`:

1. recursively resolves local imports and verifies declared identities and
   revisions;
2. applies the root capability ceiling and fails on missing required
   capabilities;
3. enumerates only declared export directories;
4. assigns each artifact an identity of
   `(context id, revision, repository-relative path)` plus a SHA-256 digest;
5. constructs a logical catalog and a deliberately naive physical overlay;
6. compares full, repository-filtered, and artifact-filtered surfaces; and
7. invokes every Python and Node CLI as a smoke test.

The filter query selected two functions and three domains:

```json
{
  "functions": ["analysis", "briefing"],
  "domains": [
    "software-delivery",
    "data-governance",
    "customer-operations"
  ]
}
```

Detailed commands and observations are preserved in
[`run-001.md`](run-001.md). The behavior supported by those observations is
captured provisionally in [`candidate-rules.md`](candidate-rules.md); those
rules are investigation notes, not the deferred durable specification.

[`run-002.md`](run-002.md) records the second experiment: a full-union physical
surface with one skills root, repository-prefixed skill names, and repository-
namespaced knowledge and tooling.

## Findings

1. **Destructive flattening loses information in this corpus.** The logical
   catalog retained 81 identities. A naive relative-path overlay produced 54
   files after 27 overwrites.
2. **A flat experience does not require flat identity.** Namespaced catalog
   identities retained all colliding artifacts together with revision, digest,
   scope, policy, and source path.
3. **Repository prefiltering helped but was not sufficient.** It excluded the
   remediation function and facilities domain repositories, reducing 54 skills
   to 42. Six remediation skills still remained inside the selected domain
   repositories; artifact filtering reduced the set to the 36-skill golden
   result.
4. **Scope dimensions need explicit applicability semantics.** Function
   contexts required a domain wildcard, while core and workbench contexts
   required an always-available marker. A simple list intersection is not
   expressive enough without those concepts.
5. **Conflicts should be visible.** The revision and policy scenarios both
   failed closed with specific diagnostics.
6. **The tested order property is narrow.** Reversing import declaration order
   for the same root, graph, revisions, and policies produced the same 72
   imported artifact identities. This does not prove that changing the root or
   resolving version ranges is order-independent.
7. **A functional physical handoff is possible for the fixture.** All 81
   artifacts materialized without destination collisions; 54 skills were
   discoverable through one root and all rewritten links and CLI paths worked.
8. **Relocation is not free.** The materializer applied 270 controlled rewrite
   occurrences across 54 skills. Unknown relative references remain a
   compatibility problem rather than something the experiment solved.

## Interpretation

The evidence supports a **namespace-preserving logical union** as the semantic
model. Physical trees may still be generated for filesystem-only consumers,
but they need namespace-aware paths or an explicit resolution ledger and must
not define composition semantics.

Repository scopes look useful as optional coarse discovery hints. They should
not replace artifact metadata or harness-level selection: a repository is a
governance and release envelope, not necessarily a homogeneous retrieval unit.

The experiment also suggests retaining content digests alongside the proposed
identity tuple. A digest exposes mutation under a reused revision label even
though real immutable Git revisions would normally prevent it.

## Limitations and next work

- Simulated revisions are not Git commit resolution or a lockfile.
- The root-only capability check is intentionally shallow; transitive policy
  intersection and artifact-class policies remain unspecified.
- Directory exports need trials with include/exclude patterns and generated
  indexes.
- Deterministic label filtering is not evidence of LLM discovery accuracy,
  task success, or prompt savings.
- No poisoning, authorization-bypass, or provenance-in-answer benchmark has
  been run.
- Run 002 used a harness-neutral filesystem discovery simulation, not a named
  agentic harness.

The scratch composer should remain in `.cache/src/`. The next decision is
whether to extend the experiment with a harness/model selection trial or first
settle the identity, export, locking, and policy semantics. Only after those
semantics are accepted should a durable specification be written and code be
promoted into committed `src/`.

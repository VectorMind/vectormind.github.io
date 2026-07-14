# Candidate composition rules after Runs 001 and 002

**Status:** Experimental design notes, not a durable specification.  
**Evidence:** [`run-001.md`](run-001.md) and [`run-002.md`](run-002.md)

These rules describe the smallest behavior consistent with the first
Harborworks trial. They intentionally avoid deciding the serialization format,
lockfile model, or full policy algebra.

## Surface and identity

### CR-001 - Composition resolves a union and may materialize it

Composition first resolves one full union of artifact identities. For a
filesystem harness, it may materialize that union as a generated tree. The
catalog remains the provenance and resolution ledger for the physical surface;
it is not a substitute for the harness-facing files.

**Run-001 basis:** The catalog retained 81 identities while the naive tree
retained 54 paths after 27 overwrites.

**Run-002 refinement:** A repository-namespaced materialization retained all 81
artifacts with no destination collisions.

### CR-002 - Relative paths are not global identities

The minimum tested artifact identity is:

```text
(context id, resolved revision, repository-relative path)
```

A content digest travels with the identity as an integrity observation. It is
not yet settled whether the digest becomes part of normative identity.

### CR-003 - Collisions coexist by default

Equal repository-relative paths from different contexts are distinct artifacts
and must remain visible. A collision becomes an error only if a projection
cannot represent both identities without an explicit resolution rule.

### CR-004 - Provenance survives every projection

Every catalog entry carries at least context id, resolved revision, relative
path, artifact class, digest, scope, and effective policy. A projection must
provide a way back to that identity even if it displays a shorter path.

## Graph resolution

### CR-005 - Imports declare expected identity and revision

The prototype requires every import edge to state the expected context id and
revision. The resolver verifies both against the imported manifest.

The fixture's local `path` locator is only a test transport. A durable design
still needs to distinguish a source locator from an immutable resolved pin.

### CR-006 - Diamond imports deduplicate by context identity

Repeated imports of the same context id at the same revision resolve once.
Encountering the same id at different revisions is a visible composition error
until an explicit deterministic resolution rule exists.

### CR-007 - Order independence is conditional

For the same root, graph, exact revisions, exports, and policies, changing
import declaration order must not change the sorted artifact identity set.

This rule does not claim that changing the root, allowing version ranges, or
changing policy produces the same result.

## Export boundaries

### CR-008 - Exports are explicit

Only declared paths or artifact classes enter the composed catalog. `.cache/`
is excluded unless a future design introduces a separate, explicit local-only
mechanism; it must never be exported by the ordinary context surface.

### CR-009 - Executables remain separately identifiable

Knowledge, skills, and executable tools are distinct artifact classes. A
consumer may discover all three while applying stronger authorization and
isolation to executables.

Directory-level exports were sufficient for the fixture but remain too coarse
for a durable contract. Include/exclude patterns and generated indexes still
need trials.

## Scope and selection

### CR-010 - Repository scope is a coarse discovery hint

Repository scopes may remove clearly irrelevant contexts before artifact-level
selection. They are not an authorization mechanism and do not guarantee that
every artifact in an included repository is relevant.

**Run-001 basis:** Repository filtering reduced 54 skills to 42, but 6
unselected remediation skills remained inside selected domain repositories.

### CR-011 - Scope dimensions need applicability semantics

The trial needed:

- wildcard domain applicability for function-method contexts;
- multiple function values for domain contexts; and
- an always-available marker for core and root contexts.

The eventual model may encode these differently, but plain intersection of two
ordinary label lists is insufficient.

### CR-012 - Artifact selection remains downstream

Composition publishes the resolved available surface. The harness or another
discovery layer selects the active working set. Artifact metadata may support
that selection without making it part of graph resolution.

## Policy and failure behavior

### CR-013 - Policy failures are explicit and fail closed

The prototype rejects a context when its required capabilities exceed the root
capability ceiling. It does not silently hide or enable the tool.

This is only a first negative case. Effective policy across multiple import
paths, artifact classes, approval modes, and user credentials remains open.

### CR-014 - Availability is not authorization

Catalog presence means discoverable under the composed surface, not executable
without approval. Runtime credentials, sandboxing, approval, and audit remain
harness responsibilities.

### CR-015 - Diagnostics are part of the result

Revision conflicts, identity mismatches, unsupported policy requirements, and
projection collisions must produce stable, inspectable diagnostics. Silent
precedence is not permitted.

## Materialized harness surface

### CR-016 - Composition uses the full resolved union

The current model has no composition profiles. Materialization includes all
artifacts exported by every successfully resolved context. Task-level
selection remains a downstream harness concern.

### CR-017 - One generated root belongs to one composer

During experimentation, generated output lives under
`.cache/<composer-repository-name>/`. The composer name prevents unrelated
composition roots from sharing one cache surface.

A possible future repository-local `.composed/` convention remains deferred.

### CR-018 - Skills share one discovery root and are always prefixed

Materialized skills use:

```text
skills/<source-repository-name>--<source-skill-name>/SKILL.md
```

The generated folder and frontmatter name must match. Prefixing is unconditional
so a later import cannot rename an existing skill merely by introducing a
collision.

### CR-019 - Knowledge and tooling retain repository subdirectories

Materialized knowledge and tooling use:

```text
knowledge_base/<source-repository-name>/...
src/<source-repository-name>/...
```

This preserves familiar top-level artifact classes while preventing source
relative-path collisions.

### CR-020 - Relocation must be validated

A skill is composition-compatible only when all references needed for its
operation can be resolved in the materialized surface. The composer must either
apply a declared deterministic transformation or report an unsupported
reference. Silent broken links are not permitted.

Run 002 transformed known fixture patterns successfully. It does not establish
that arbitrary Markdown instructions or shell commands can be safely rewritten.

### CR-021 - Source and materialized identities remain linked

The generated catalog records each source identity, source digest,
materialized path, and materialized digest. Transforming a skill must not erase
which immutable source artifact produced it.

## Explicitly deferred

Run 001 does not settle:

- YAML, JSON, TOML, or another manifest syntax;
- manifest/lockfile separation;
- version-range resolution;
- signed releases or owner verification;
- content-digest identity semantics;
- policy intersection across multiple graph paths;
- export glob and override syntax;
- cycles between peers;
- MCP or filesystem projection schemas; or
- task-selection quality under a real model or harness.
- the portable reference syntax required of composable skills;
- whether unsupported references fail composition or use generated wrappers;
- named-harness discovery configuration; or
- the final location and lifecycle of a repository-local `.composed/` tree.

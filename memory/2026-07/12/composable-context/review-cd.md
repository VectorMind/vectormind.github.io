# Comparative Review of the Composable Context Drafts

**Date:** 2026-07-13  
**Review scope:** Comparative editorial and architectural review of
[`white-draft-cc.md`](white-draft-cc.md) and
[`white-draft-cd.md`](white-draft-cd.md)  
**Method:** Close reading of both drafts against the repository's stated
composable-context idea and workflow boundaries. This review does not
independently validate the cited literature or experimentally validate the
proposal.

## Overall assessment

The drafts are complementary rather than contradictory. `white-draft-cc.md`
is the stronger manifesto: it gives the idea a memorable identity, argues its
motivation forcefully, and explains why repository-level composition matters.
`white-draft-cd.md` is the stronger technical whitepaper and the better base
for a public request for comments: it is more precise about scope, more careful
about unproven claims, and more credible on composition, provenance, security,
and evaluation.

My recommendation is to continue from `white-draft-cd.md`, while restoring some
of `white-draft-cc.md`'s sharper motivation, its explicit split between the
total navigable surface and the task-specific working set, and its discussion
of retrieval as a spectrum. The result should preserve `cd`'s qualification
and logical-union model rather than returning to an unqualified flattening
model.

## Where each draft is better, and why

| Dimension | Stronger draft | Why |
| --- | --- | --- |
| Title and memorable thesis | `cc` | "Git repositories as the unit of agentic knowledge, code, and governance" states the distinctive claim immediately. `cd` is more accurate but less memorable. |
| Motivation and narrative energy | `cc` | The three pressures—context pollution, missing lifecycle, and fragmented trust—make the problem easy to grasp and give the proposal urgency. |
| Scope discipline | `cd` | It states up front that the document is a conceptual proposal, not a specification or validated architecture, and consistently distinguishes design hypotheses from supported ecosystem observations. |
| Definition of a context repository | `cd` | The folder semantics are clearer, `skills/` and an explicit `context.yaml` are represented, and the prose distinguishes episodic records from reusable truth. |
| Promotion model | Tie, for different reasons | `cc` explains the two ladders more vividly; `cd` represents their governance more carefully and avoids treating Git alone as proof of quality. |
| Composition semantics | `cd` | "Logical union" plus retained source, path, revision, license, provenance, and policy is implementable and auditable. `cc`'s unqualified "flattening" risks collisions and loss of identity. |
| Harness/composition responsibility split | `cc` | The distinction between governance of the total surface and harness selection of the active slice is one of the proposal's most important ideas, and `cc` states it most directly. |
| Retrieval discussion | `cc` | It shows that the proposal is compatible with full-text, vector, graph, SQL, ontology, document-element, and hierarchical retrieval rather than implying that folder navigation is sufficient. |
| Boundaries and interoperability | `cd` | The explicit "not a source of truth, retrieval standard, package manager, A2A protocol, or MCP replacement" section prevents category confusion and positions the proposal as a layer rather than a replacement stack. |
| Security and trust | `cd` | It separates availability from authorization and acknowledges prompt injection, memory poisoning, vulnerable code, dependency compromise, and the stronger isolation required for executables. |
| Treatment of A2A and a single harness | `cd` | It presents coexistence without claiming that a unified context automatically eliminates context-transfer or privilege problems. |
| Testability and RFC usefulness | `cd` | Its questions are framed as falsifiable properties and lead naturally to a reference implementation and measurable evaluation. |
| References and provenance | `cd` | It provides direct links, an access date, local draft provenance, and a clear warning that adjacent literature does not validate the new proposal. |

### What should be retained from `cc`

1. Keep its stronger title or use it as a subtitle. The phrase establishes the
   repository-level contribution more clearly than "repository-native context
   layer" alone.
2. Retain the three-part motivation. It is the most effective opening in either
   draft.
3. Keep the explicit responsibility split: composition governs what is
   available and trusted; the harness chooses what becomes active for a task.
4. Preserve the broader retrieval discussion, but shorten it and connect it to
   evaluation criteria rather than presenting every retrieval technique as part
   of the proposal.
5. Retain the knowledge-feedback-loop framing. It explains why `memory/` and
   `knowledge_base/` are lifecycle stages rather than automatic replacements
   for authoritative systems.

### What should be retained from `cd`

1. Use a logical, namespace-aware union as the normative composition model.
   A flat user experience must not erase artifact identity.
2. Preserve the distinction between available context and active working
   context.
3. Keep the explicit non-goals and interoperability boundaries.
4. Keep the security qualifications, especially the distinction between tool
   discovery and tool authorization.
5. Keep the proposal's claims labeled as hypotheses until a prototype and
   benchmark provide evidence.
6. Keep the direct reference links, retrieval date, and draft-provenance note.

## Issues to resolve before a merged draft

### 1. Define "flattening" narrowly or replace the term

`cc` uses flattening to mean that imported repositories appear as one surface,
but it also suggests that composition erases dependency direction and is
order-independent. Those are separate properties. A safer definition is:

> Composition exposes a unified navigable view over a resolved graph of context
> repositories while preserving each artifact's context identity, path,
> revision, provenance, license, and effective policy.

The view may feel flat to the user, but the data model should remain namespaced.
Order independence can be promised only for the same resolved import graph,
revisions, configuration, and policies. Changing the root repository can change
the graph or the effective policy and therefore need not produce the same
result.

### 2. Separate Git reviewability from quality

Git supplies versioning, diffs, history, and a convenient review mechanism. It
does not by itself establish that evidence is sound or that maintainers are
trustworthy. The paper should say that promotion is represented by an explicit,
reviewable change governed by repository policy. The stronger statement in
`cc` that every promotion is a Git commit is unnecessarily rigid: one commit
may contain several promotions, and a commit can occur without meaningful
review.

### 3. Qualify the repository as a trust boundary

The repository is a useful unit of publication, ownership, version resolution,
and review. It is not an indivisible security or trust unit. A repository can
contain read-only knowledge, executable code, tool declarations, generated
indexes, and imported artifacts with different risks and owners. Trust should
therefore attach both to the context release and to artifact class, origin,
revision, and policy.

### 4. Avoid overclaiming the single-harness advantage

A shared surface can reduce explicit handoff loss and can improve cross-domain
reasoning, but it does not guarantee a single effective reasoning space. The
harness still retrieves, summarizes, compacts, and may delegate. Likewise,
directly exposing tools avoids one privileged-agent relay pattern but does not
eliminate confused-deputy behavior, prompt injection, or authorization errors.
These are advantages to evaluate, not established consequences of composition.

### 5. Define profiles rather than one mandatory repository shape

Not every useful context needs executable code, skills, a local knowledge base,
or export capability. A small core profile could require identity, version,
imports, exports, policy, and provenance semantics; optional profiles could add
knowledge lifecycle folders, executable tooling, skills, indexes, or authority
round-tripping. This would make adoption easier without weakening the lifecycle
model used by richer contexts.

## Participant response to the request for comments

My answer to the central question is **yes: a repository is the right default
unit of context ownership and publication, but it is not the right atomic unit
for trust, authorization, or retrieval**.

It is the right default because repositories already provide a portable name,
history, review workflow, version reference, maintainer boundary, and a place
where knowledge, code, tests, policies, and provenance can evolve together.
That is a material improvement over asking users to assemble isolated skills,
tool servers, and documents with no shared lifecycle. The proposal is strongest
when it treats the repository as the unit that publishes an intentionally
governed context surface.

The qualification matters. Consumers should never have to trust or load the
entire repository uniformly. Composition must preserve item-level identity and
allow different handling for instructions, evidence, curated claims,
executables, indexes, and live tools. In other words, the repository should be
the release and governance envelope, while artifacts remain the units of
discovery, provenance, policy evaluation, and authorization.

### Suggested answers to the open design questions

#### Manifest semantics

Start with a deliberately small declarative manifest:

- stable context identifier and schema version;
- release version or immutable revision;
- owner and source repository;
- imports pinned to immutable revisions;
- exported paths or artifact classes;
- namespace or mount name;
- license and provenance metadata references;
- declared capabilities and task scopes;
- policy requirements and compatibility constraints.

Namespacing should be the default. Deduplication should be explicit and based
on stable identity or content digest, not matching filenames. Conflicting
versions or policies should produce a visible resolution record or fail closed;
silent precedence would undermine the proposal's provenance claim.

#### Scoped composition

Repositories should be allowed to declare scopes and capabilities, but these
should be discovery hints rather than the sole security mechanism. A compiler
can use them to exclude obviously irrelevant contexts, after which the harness
still performs task-level selection. The evaluation should compare this
two-stage selection against a flat artifact catalog and against harness-only
selection.

#### Flattening mechanics

Use a virtual catalog or overlay as the canonical model. A materialized tree may
be produced as a compatibility view, but it should be generated, reproducible,
and accompanied by a resolution ledger. Local `.cache/` content should not be
exported or composed by default. No artifact should lose its source context or
revision when presented through the unified view.

#### Export back to authority sources

Treat exports as proposals, not synchronization. An export should identify the
target system and object, source claims and evidence, transformation performed,
reviewer, and resulting target revision. The authority system's own review and
permissions remain decisive. This prevents the context repository from quietly
becoming a competing source of truth.

#### MCP and harness interoperability

Yes, a resolved context should be projectable as MCP resources, tools, or
prompts, but MCP should be one adapter rather than the internal data model.
Filesystem navigation, a catalog API, and MCP can all expose the same resolved
identities and provenance. A useful interoperability test is whether two
adapters return equivalent artifact identities and policy metadata.

#### Evaluation

The first benchmark should use two or three real context repositories and
measure at least:

- task success and artifact-selection precision/recall;
- prompt tokens and tool-definition tokens loaded;
- provenance retention from selected answer claims back to source artifacts;
- collision and incompatible-version detection;
- behavior when one imported context contains malicious instructions or an
  unauthorized executable tool;
- maintainer effort and time required to promote or update an artifact.

Compare four conditions: a flat ungoverned catalog, separate repositories with
manual selection, logical composition with harness-only discovery, and logical
composition with repository-scope prefiltering plus harness discovery. Without
such baselines, claims about reduced context pollution, stronger trust, or
better discovery will remain plausible but unproven.

## Recommended direction

Publish the next draft as a tightened version of `white-draft-cd.md` with the
best framing from `white-draft-cc.md`. State one central claim:

> A context repository is a versioned governance envelope that publishes a
> composable, provenance-preserving surface of knowledge, workflows, and tools;
> the harness selects the task-specific working set, and underlying systems
> retain authority and authorization.

That formulation is distinctive, defensible, and narrow enough to prototype.
The immediate next artifact should be a minimal manifest and resolution model,
followed by a small reference composition whose behavior can be measured.

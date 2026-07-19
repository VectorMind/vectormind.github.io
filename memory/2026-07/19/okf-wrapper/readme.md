# OKF as a Wrapper — Analysis of the Non-Replacement Role

Date: 2026-07-19
Inputs: `C:\dev\MicroWebStacks\astro-huge-doc\plans\2026-07\19\okf-support\` (handoff.md, deep-research-report.md, survey.md, plan.md)
Related: [composable-context](../../12/composable-context/readme.md) — this analysis applies the same "do not shadow the authority sources" critique to OKF that composable-context applies to context repositories.

---

## 1. Thesis

The Open Knowledge Format (Google Cloud, v0.1 draft, announced 12 June 2026) is designed, positioned, and actually used as a **wrapper format**: a portable, human-and-agent-readable *last-mile* layer that packages knowledge **derived from** authoritative systems, and points back to them. It is not designed to become the system of record, and every serious source — Google itself, first-party product integrations, third-party implementers, and critics — either states this explicitly or assumes it structurally.

The interesting question is therefore not *whether* OKF is a wrapper (the evidence below settles that), but **whether the wrapping mechanics are good enough to keep fidelity to the authoritative sources** — and what the wrapper should actually contain: a *copy* of the source's knowledge (snapshot), or a *guide to using* the source (interface). This distinction drives the whole analysis:

- **Snapshot wrapping** — the bundle contains derived facts (schema dumps, data dictionaries, metric tables). Cheap to consume, but it drifts, and once an agent finds an answer in the bundle it stops consulting the source. This is the *shadowing* danger.
- **Interface wrapping** — the bundle contains usage knowledge: what the source is, when to use it, *how to invoke it* (which MCP tool, which CLI, which API contract, which library), with pointers instead of payloads. This ages far slower and structurally cannot shadow the source, because the answer to any concrete question is still "go ask the source".

OKF supports both, its ecosystem today mostly builds snapshot wrappers (generators), and its base spec provides only weak fidelity machinery (a `resource` field, a `# Citations` convention, an ambiguous `timestamp`). The verdict in §8: OKF is well adapted as the *format* of the last-mile exchangeable doc — precisely because a "user guide for an authoritative tool" is itself a markdown how-to document, which is exactly what OKF standardizes — but the *discipline* of interface-first wrapping, drift control, and one-way authority has to be layered on top; the base spec does not enforce it.

---

## 2. References that state or assume the wrapper role

Grouped by who says it. Each entry states the wrapper-relevant claim, not a general description.

### 2.1 Google, as spec owner

| Reference | Wrapper-relevant statement |
|---|---|
| [OKF Specification v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) | States outright that OKF does **not** replace domain-specific schemas such as **Avro, Protobuf, or OpenAPI**. Reserves `resource` (pointer to the underlying system entity) and the `# Citations` body convention (pointer to the system of record) — both are back-references to an authority that lives elsewhere. Consumers must tolerate unknown fields/types/broken links, i.e. the bundle is a permissive carrier, not a validated source of truth. |
| Google Cloud OKF announcement blog (12 June 2026) | Positions OKF as formalizing Karpathy's **LLM-wiki pattern** — a *maintained derived wiki* over sources — into a portable interchange format, launched as the **packaging layer** around Knowledge Catalog, not as a knowledge store itself. |
| Knowledge Catalog product positioning (April 2026) | Knowledge Catalog **ingests** OKF and serves it to agents; internally it uses its **own native metadata model** (aspect types as JSON templates) enriched into a context graph. OKF is the exchange surface at the boundary, the runtime is something richer — the wrapper never becomes the engine. |
| BigQuery Conversational Analytics docs | "The wiki your team already maintains can **feed** straight into Knowledge Catalog" via OKF. The existing wiki stays where it is; OKF is the transport. |
| Google reference producer + sample bundles (knowledge-catalog repo) | The reference agent **generates** OKF from BigQuery metadata plus a web-enrichment pass with citations. Google's own canonical usage is source → generated bundle, i.e. derivation, never authoring-in-place of authoritative facts. The repo also states its contents are "not an official Google product" — even the tooling is reference material. |
| Google README on composition | OKF "composes with Obsidian, Notion, MkDocs, Hugo, Jekyll" — piggyback on existing authoring tools rather than replacing them. |

### 2.2 Implementers (their architecture assumes wrapping)

| Reference | How it assumes the wrapper role |
|---|---|
| [AWS sample: Data Wiki, Glue → OKF → MCP](https://github.com/aws-samples/sample-okf-llm-wiki) | AWS Glue catalog remains the system of record; OKF is the generated intermediate; MCP is the delivery. Three-layer wrapper architecture, explicitly. |
| okfgen (multi-source generator) | Generates OKF **from** repos, schema files, BigQuery, Firestore, docs sites, **CKAN**, **Socrata**, databases. A generator with ten upstream source types is by construction a wrapper tool. |
| erd2okf community discussion | The sharpest wrapper-discipline evidence: recommends separating **conformance** validation (is the bundle valid OKF?) from **drift** validation (does the bundle still reflect the source database?), with cheap regeneration and CI failing only on structurally relevant drift. Drift-checking only makes sense if the DB is authoritative and the bundle is derived. |
| qsv `describegpt` | Emits a data dictionary **as** an OKF document from the actual data — snapshot wrapping of a dataset. |
| KGLite, NornicDB, Graphify bridge | All treat OKF as **ingest/exchange surface** and build richer internal graph representations. NornicDB documents OKF explicitly as "source and exchange format rather than a replacement" for its runtime. |
| WordPress plugins (Tick AI SEO, RankReady, Xagio) | Publish a `/okf/` bundle **generated from** CMS content, kept in sync by cron. The CMS database remains authoritative; the bundle is a cached projection. Tick's own docs must clarify OKF is *not* a Search ranking signal — i.e. even the publishing wrappers disclaim authority. |
| Kiso (publisher) | Builds static sites, `llms.txt`, `sitemap.xml` **from** validated bundles in CI — the bundle is upstream input to yet more derived surfaces, and downstream of the real sources. |
| Stashpad / Obsidian OKF Enforcer / [Hugo proposal #15035](https://github.com/gohugoio/hugo/issues/15035) | Export/validate/map OKF **onto existing** vaults and site trees. Adoption by conforming what already exists, not by migrating content into a new store. |
| AKB, Open Knowledge, OKF Harness, OpenKB | Runtimes that keep their own governance/search engines and use OKF as the packaging/import-export layer around them. |

### 2.3 Reviewers and critics (the wrapper's weak points)

| Reference | Critique relevant to fidelity |
|---|---|
| [KCP ↔ OKF production discussion](https://wiki.totto.org/blog/2026/02/28/kcp-and-mcp-one-protocol-for-structure-one-for-retrieval/) and the [KCP spec](https://github.com/cantara/knowledge-context-protocol) | `timestamp` answers "when the file changed", **not** "when the knowledge is valid". Trust is manageable within one repo, hard across org boundaries. Agents need explicit supersession/contradiction resolution that plain links don't provide. Even the OKF-side response accepted these points, arguing they belong in a **governance layer above the base format** — conceding the wrapper needs external fidelity machinery. |
| [OKF semantic-web profile proposal (issue #141)](https://github.com/GoogleCloudPlatform/knowledge-catalog/issues/141) + [W3C Holon CG](https://www.w3.org/community/holon/) | Serious graph practitioners propose IRI identity, typed relations, SHACL — **as profiles on top**, keeping OKF a human-readable carrier. Nobody proposes making OKF itself the semantic authority. |
| July 2026 knowledge-centric IS vision paper | Treats LLM Wiki and OKF as evidence of a transition, "**not the endpoint**". |
| July 2026 memory benchmarking paper | An OKF-based memory improved retrieval precision but "did not solve selection or session drift" — the wrapper improves *packaging*, not *routing correctness*. |
| Survey (local input, `survey.md`) | Verdict for every adjacent standard: "Keep **OpenAPI** authoritative; use OKF for the context around it." "Treat **DCAT** records as authoritative for catalogue-level metadata." "Package data with **Frictionless**; explain it with OKF." Final judgement: *"Use OKF as the optional canonical knowledge profile for Markdown, then generate or connect the specialized standards rather than trying to replace them."* |
| Astro Huge Doc handoff (local input, `handoff.md`) | Non-goals §4: "Replace OpenAPI, JSON Schema, Protobuf, Avro, SQL schemas, or other domain formats." §23: "**Source Markdown remains authoritative**" even for type-specific renderers. §10: a Markdown link must not be auto-promoted into a formal semantic claim (`DEPENDS_ON`) — the viewer must not *manufacture* authority the source didn't state. |
| Astro Huge Doc plan (local input, `plan.md`, RK-3) | Depends only on OKF's stable core and absorbs spec drift in `meta_data` — implementers hedge against the draft spec itself, further proof nobody treats it as a settled authority. |

**Conclusion of §2:** there is no reference, first-party or third-party, that positions OKF as a replacement for authoritative sources. The replacement risk is not in anyone's *stated intent* — it is an **emergent operational failure mode** (stale snapshot + trusting agent), which is exactly why the mechanics below matter.

---

## 3. How the wrapping actually works — mechanics

The de-facto lifecycle across Google's reference agent, okfgen, AWS Data Wiki, OKF Harness and Open Knowledge is:

```text
generate  →  curate  →  validate  →  publish  →  ingest
(from source) (human)   (CI: shape    (static/    (Knowledge Catalog,
                         + drift)      /okf/, MCP)  agent runtimes)
```

The per-file wrapping contract is small:

```yaml
---
type: dataset            # only REQUIRED field — the wrapper's facet
title: Customer Orders   # display only; identity is the file PATH
description: ...         # routing summary for progressive disclosure
resource: urn:bq:proj.ds.customer_orders   # ← back-pointer to authority
tags: [sales, pii]
timestamp: 2026-07-19T09:00:00Z            # derivation time (NOT validity)
---
# Definition
...prose, the wrapper's own contribution...

# Citations
- BigQuery table schema (system of record)   # ← authority list
```

Four mechanisms carry the wrapper role:

1. **Path-based identity.** The concept ID is the bundle-relative path, stable under title edits. This makes the bundle *addressable* without inventing a new global identifier scheme that would compete with the source's identifiers — the source keeps its URN/IRI in `resource`.
2. **`resource` + `# Citations` as the authority tether.** These are the only spec-level provisions for "the truth lives elsewhere". They are conventions, not enforced: a bundle with no citations is equally conformant. Fidelity is therefore a *policy* of the producing pipeline, not a property of the format.
3. **Links as untyped relations.** Markdown links express "related", never a formal claim. This is a feature for the wrapper role: the bundle cannot accidentally assert semantics (dependency, supersession, ownership) that only the authoritative system can state. The cost is that agents needing those semantics must go to the source (or to an RDF/SHACL profile layered above).
4. **Permissive conformance.** Unknown types, unknown fields, broken links must be tolerated. The bundle is designed to be consumable even when partially stale or partial — a cache semantics, not a contract semantics.

---

## 4. How the indexes work

The index layer is the part of OKF that deserves the most attention, because **the index is the only content in the bundle that has no authoritative source** — it is authored curation, and therefore the legitimate *native* content of the wrapper (everything else is derived and can drift; the index is the wrapper's own value-add).

- **`index.md` (reserved, per directory)** — an authored progressive-disclosure listing: headings, one-line descriptions, ordered links to child concepts and sub-indexes. The root `index.md` carries the OKF version declaration. An agent reads the root index (~1 page), follows one branch, reads a sub-index, and only then loads a leaf concept. This is hierarchical routing: cost grows with path depth, not corpus size. Reserved files are **not** concept nodes — they are navigation, not knowledge.
- **`log.md` (reserved)** — curated change history (creation/update/deprecation entries with dates and links). It answers "what changed in the *bundle*", which is exactly the drift-visibility question a wrapper needs; note it does not answer "what changed in the *source*" — that gap is the erd2okf drift-check's job.
- **Synthesized indexes** — when no authored index exists, consumers (e.g. the Astro Huge Doc plan) synthesize one from filesystem hierarchy, titles, descriptions, types, tags — and must *mark* synthesized entries, preserving the distinction between authored curation and derived listing.
- **Routing layers above OKF** — where the in-bundle index is not enough:
  - **KCP `knowledge.yaml`**: intent, trigger terms, loading priority, audience, dependencies, freshness, trust — a routing *manifest* separated from the documents. Best generated **from** the parsed OKF corpus with manual overrides only for non-inferable fields (survey's recommendation), otherwise the manifest itself becomes a second source that drifts.
  - **`llms.txt`**: flat public discovery front-door, generated from the bundle.
  - **Derived machine indexes**: `/okf/index.json`, `/okf/graph.json`, backlink tables (the Astro plan's `relations` table) — computed at collect time, never authored.

The pattern is consistent: **one authored curation layer (index.md), everything else generated.** That is the correct division of labor for a wrapper: humans curate routing and rationale; machines derive facts and inverses (backlinks, graphs, manifests) so they can be regenerated instead of maintained.

---

## 5. The non-destructive transition: what does the authoritative source become?

This is the user-facing core question. When a corpus gets wrapped in OKF, the source does not "become" anything — it stays exactly where it is. What changes is that the agent now needs a defined **access modality** to reach it from the wrapper doc. The wrapper doc's job is to name that modality precisely. Four modalities, with the fidelity mechanism of each:

| Source kind | Modality the wrapper should point to | What the OKF doc contains | Fidelity mechanism |
|---|---|---|---|
| Live/large/sensitive system (DB, catalog, ticketing, wiki with ACLs) | **MCP server** (or API) | When to query it, which tools/resources it exposes, auth prerequisites, example queries, caveats | The agent always gets **fresh, access-controlled** answers; the OKF doc holds zero payload. Pattern: Knowledge Catalog, AWS Glue→OKF→MCP, "OKF at rest, MCP at runtime" (survey §11). |
| Deterministic local tool | **CLI** | Install line, invocation recipes per task, exit/output conventions, one worked example | The agent **runs the real tool** (`okf validate`, `qsv`, `bq`, `gh` …) instead of trusting a transcript of its old output. A CLI recipe ages only when the tool's interface changes — slow drift. |
| Procedure / method / workflow | **Skill** (SKILL.md-style how-to) | The procedure itself: preconditions, steps, escalation, links to the tools each step uses | Here the wrapper **is** the authority — procedures have no other system of record. This is the one case where OKF-shaped markdown is not a wrapper but the source. See §7. |
| Library / package | **Python/npm dependency** | Why/when to use it, version pin policy, links to its API docs and changelog, project-specific usage patterns | The authoritative interface is the package's own docs/types/docstrings, resolved by the **package manager** at the pinned version. The OKF doc wraps *rationale and local conventions*, never re-documents signatures. |
| Formal contract (API, data schema) | **OpenAPI / Avro / Protobuf / DCAT / Frictionless file, referenced by URL** | Business meaning, when-not-to-use, migration notes, link to the contract | The contract stays machine-enforceable in its native standard; OKF explicitly disclaims replacing these (spec, handoff §4). Viewers may *embed* an OpenAPI renderer rather than converting the contract to prose. |

Rules that make the transition smooth and non-destructive:

1. **Additive adoption.** OKF conformance = add `type:` frontmatter to existing markdown. No file moves, no format migration, no new store. Existing plain-markdown consumers keep working (tolerance rules). This is why the transition can be gradual per-document.
2. **Generate snapshots, author interfaces.** Anything that *can* be regenerated from a source (schemas, dictionaries, catalogs) must be generated and drift-checked in CI (erd2okf pattern). Anything hand-written should be interface knowledge (usage, rationale, routing) that has no upstream to drift from.
3. **One-way authority.** Edits to derived content flow **back to the source** (fix the schema, fix the wiki page), then regenerate — never patch the bundle in place. The bundle is staging/cache. This is the same lifecycle rule composable-context sets for `.cache → memory → knowledge_base`: staging, "not new source authority", with user-initiated promotion back to the authority.
4. **Every leaf doc carries its tether.** `resource:` filled, `# Citations` present, `timestamp` set at generation. A bundle-level convention (not in the base spec — add it as a local profile): a doc without `resource` or citations is either a genuine native doc (procedure, index, rationale) or a lint warning.
5. **Freshness must be answerable.** Since `timestamp` ≠ validity (KCP critique), add local fields where it matters: `valid_until`, `generated_by`, `source_version`/commit — the survey's graduated provenance model (basic → intermediate → PROV-O export). Show freshness in the consuming UI so a human can see staleness before the agent trusts it.

---

## 6. Keeping usage fidelity: user guide, API doc, or contract?

"How does the agent use the source correctly?" has three answers depending on what must stay faithful:

- **Faithful *invocation*** → the source's own **contract** (OpenAPI operation, CLI `--help`, package types). Never transcribe these into the wrapper beyond a minimal example; link them. A transcribed contract is a stale contract.
- **Faithful *selection*** (using the right source, at the right moment, for the right question) → this is genuine **guide content** and is the wrapper's proper job: intent, scope, when-not-to-use, alternatives, cost. No contract format expresses this; markdown prose does.
- **Faithful *interpretation*** (what the results mean, caveats, business definitions) → also guide content, ideally with citations to where the definition is governed (policy page, metric owner).

So the fidelity architecture is: **contracts stay native and linked; selection and interpretation knowledge is authored in the wrapper; invocation examples are minimal and tested** (a CI job that actually runs the documented CLI/API example is the strongest freshness check available — it turns the user guide into a verified artifact, the same move erd2okf makes for schemas).

---

## 7. Is OKF adapted as the last-mile exchangeable doc format? Limits and alternatives

### Limits (from spec, critics, and the research report)

1. **No fidelity enforcement.** `resource`/citations optional; nothing distinguishes a derived doc from a native one; conformance says nothing about truthfulness or freshness.
2. **Timestamp ambiguity.** File-change time, not validity window; no supersession semantics beyond a `log.md` convention.
3. **No provenance model.** Who/what generated this, from which source version — absent; needs local fields or PROV.
4. **Untyped relations.** Good for humility (§3.3), bad when the guide must state "X supersedes Y" machine-readably; needs the RDF/SHACL profile or local conventions.
5. **Free-form body.** Two conformant bundles can differ radically in quality; "user guide" has no required shape — `# Schema`/`# Examples`/`# Citations` are only suggestions, so exchangeability of *structure* is weaker than exchangeability of *format*.
6. **No routing metadata.** Intent/audience/priority/trigger-terms live in KCP, not OKF; a large bundle without a good authored index degrades to grep.
7. **No composition/manifest story.** Nothing specifies how bundles import or reference each other (cross-bundle links are an open question even in the handoff, §34) — directly relevant to composable-context.
8. **Draft status.** v0.1, single-vendor authored, no independent governance; implementers hedge (plan RK-3).

### Alternatives, per concern (survey's layering, condensed)

| Concern | Better-suited standard | Relationship to OKF |
|---|---|---|
| Executable API contract | OpenAPI | Keep authoritative; OKF links to it |
| Data packaging/checksums | Frictionless Data Package | Package data; OKF explains it |
| Dataset catalog federation | DCAT 3 | Catalog metadata authoritative; OKF adds business context |
| Formal semantics/typed edges | RDF/JSON-LD (+OWL/SHACL) | Optional export profile above OKF |
| Vocabulary/taxonomy | SKOS | Referenced from OKF glossary types |
| Provenance/lineage | W3C PROV-O | Graduated: local fields → PROV export |
| Agent routing/governance | KCP | Manifest generated from the OKF corpus |
| Runtime delivery | MCP | OKF at rest, MCP at runtime |
| Public discovery | llms.txt, Schema.org | Generated from the bundle |

None of these is "OKF but better" for the last-mile doc itself — each is better *at a different layer*, which is the strongest structural evidence that OKF's niche (portable human-authored markdown bundle) is real.

### The counter-argument in OKF's favor — the user-guide point

The critique "don't wrap, just write a user guide for the authoritative tool" **self-defeats into an argument for OKF**: a user guide is a markdown how-to document with a title, a purpose, examples, and references. Give it `type: guide`, a `resource:` pointing at the tool, `# Examples`, `# Citations` — it is *already* an OKF concept document. A skill (SKILL.md) has the same shape. So the honest verdict is:

> **OKF is a reasonable standardization of exactly the artifact that the "alternative" proposes.** The failure mode is not the format — it is filling the format with snapshot payloads instead of interface guidance. Wrap the *interface*, not the *data*: an OKF bundle whose leaves say "here is when and how to consult the source" is a durable last-mile layer; one whose leaves say "here is what the source contained on July 19th" is a stale shadow waiting to mislead an agent — unless regeneration and drift-CI make the snapshot effectively live.

What OKF adds over an unstandardized guide folder: portable identity (path-based), a facet (`type`), a routing layer (`index.md`), a history convention (`log.md`), tolerance rules that let heterogeneous consumers share one corpus, and a fast-growing lint/validate/publish/ingest toolchain. That is modest, but it is precisely the modesty that makes it adoptable — the survey's final judgement: OKF's strongest quality is "the unusually low distance between an ordinary documentation repository and an interoperable knowledge bundle".

---

## 8. Implications for composable-context

The [composable-context](../../12/composable-context/readme.md) idea already contains the wrapper doctrine independently: *"the better quality knowledge is the one that lives in its original authoring tools … memory and knowledge_base are for staging and not new source authority."* OKF and composable-context are therefore solving the same problem one level apart — OKF standardizes the **document format** of the staged surface; composable-context defines the **repository lifecycle and composition** around it. Mapping:

| composable-context element | OKF counterpart | Fit |
|---|---|---|
| `knowledge_base/` curated docs | Concept documents (`type:`, frontmatter) | Direct — adopt OKF frontmatter additively |
| `memory/` episodic investigations | Concepts + `log.md` history convention | Good; `log.md` gives the missing history surface |
| Navigable surface after composition/flattening | `index.md` progressive disclosure per repo, root index per composed surface | Good, but composition of indexes is unspecified in OKF — the flattener must merge/synthesize |
| Import manifest between context repos | **Missing in OKF** (cross-bundle links are an open question) | Gap — needs a KCP-like manifest or the composable-context manifest itself |
| Skills | `type: guide`/`playbook` concept docs (SKILL.md-shaped) | Natural — skills are markdown how-tos, OKF's home turf |
| Code/deps (`src/`, package managers) | Out of OKF scope by design | Correct split — deps stay with uv/npm, wrapper only documents usage |
| `.cache` fetched data | Explicitly *not* bundle content — regenerable, gitignored | Aligned: never promote cache payloads into the bundle without a citation and a drift path |
| Promotion ladder with user-initiated review | The §5 "one-way authority" rule | Same rule, independently derived — mutual confirmation |

Consequences:

1. **OKF is a viable interchange profile for the knowledge side of a context repo** — it costs one frontmatter field, and buys tool compatibility (validators, viewers, MCP servers, graph ingesters) for the composed surface.
2. **The shadowing critique transfers fully.** A composed context that flattens several repos' knowledge_bases is a wrapper-of-wrappers; every fidelity rule in §5 (tether, freshness, generate-don't-author snapshots, one-way promotion) applies at composition scope, and staleness now has two hops to hide in. The composition manifest should surface per-repo `timestamp`/version so the composed index can show freshness per branch.
3. **OKF does not solve composition** — no import semantics, no cross-bundle identity, no dedup/collision rules (the harborworks experiment's collision/scope problems remain composable-context's own to solve). Use OKF for the leaves and per-repo indexes; keep the manifest, flattening, and scoping logic in composable-context; optionally emit a generated KCP manifest for agent routing over the composed surface.

---

## 9. Recommendations

1. **Adopt OKF as the format of last-mile and staged knowledge docs** (knowledge_base, memory, guides, skills) — additively, via frontmatter only.
2. **Enforce a local wrapper profile** beyond base conformance: every derived doc must carry `resource` + `# Citations` + `timestamp`; add `source_version` and `valid_until` where staleness bites; lint this in CI.
3. **Prefer interface wrapping.** Leaves should teach *selection, invocation pointers, and interpretation*; snapshots only where a generator + drift-check exists (erd2okf pattern). Test documented invocation examples in CI where feasible.
4. **Keep contracts native** (OpenAPI/Avro/DCAT/Frictionless/package docs) and linked, never transcribed.
5. **Treat `index.md` as the wrapper's real product** — authored routing curation; generate everything else (backlinks, graphs, llms.txt, KCP manifest, JSON indexes) from the parsed corpus.
6. **Keep authority one-way**: bundle edits that correct facts flow back to the source and regenerate; the bundle is never write-authoritative. User-initiated promotion, per composable-context.
7. **Depend only on OKF's stable core** (type/title/description/tags/timestamp/resource, index.md/log.md, links-as-relations) and keep everything else in tolerated extra fields, so v0.x drift is absorbed (plan RK-3's hedge).

---

## 10. Full reference list

**Spec owner (Google):**
- OKF Specification v0.1 (draft) — https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md — non-replacement of Avro/Protobuf/OpenAPI; `resource`; `# Citations`; tolerance rules.
- GoogleCloudPlatform/knowledge-catalog repo — reference producer (BigQuery → OKF + web enrichment), sample bundles, visualizer; "not an official Google product" disclaimer.
- Google Cloud OKF announcement blog, 12 June 2026 — OKF as formalized LLM-wiki pattern; Knowledge Catalog ingests OKF.
- Knowledge Catalog announcement, April 2026 — native aspect-type metadata model; OKF as ingest boundary.
- BigQuery Conversational Analytics documentation — existing team wiki feeds Knowledge Catalog via OKF.
- OKF semantic-web profile proposal — https://github.com/GoogleCloudPlatform/knowledge-catalog/issues/141
- Andrej Karpathy, LLM Wiki gist (April 2026) — conceptual precursor: persistent derived wiki over sources.

**Implementers:**
- AWS sample Data Wiki (Glue → OKF → MCP) — https://github.com/aws-samples/sample-okf-llm-wiki
- okfgen (CKAN/Socrata/BigQuery/Firestore/docs/repos/DB → OKF); erd2okf drift-vs-conformance discussion; qsv `describegpt` OKF output.
- KGLite (OKF → Cypher graph); NornicDB (OKF as source/exchange format); Graphify bridge proposal.
- Kiso publisher (OKF → static site + llms.txt); WordPress Tick AI SEO / RankReady / Xagio (`/okf/` endpoints, cron-synced, "not a ranking signal" disclaimers).
- Obsidian OKF Enforcer; Stashpad OKF export; Hugo proposal — https://github.com/gohugoio/hugo/issues/15035
- Open Knowledge, OKF Harness, okf-skills, okf CLI, okq, okf-gem, AKB, OpenKB — validation/runtime/authoring layers around OKF bundles.

**Adjacent standards (the layers OKF must not replace):**
- OpenAPI — https://spec.openapis.org/ · Frictionless — https://specs.frictionlessdata.io/data-package/ · DCAT 3 — https://www.w3.org/TR/vocab-dcat-3/ · RDF 1.2 — https://www.w3.org/TR/rdf12-concepts/ · JSON-LD 1.1 — https://www.w3.org/TR/json-ld11/ · OWL 2 — https://www.w3.org/TR/owl2-overview/ · SHACL — https://www.w3.org/TR/shacl/ · SKOS — https://www.w3.org/TR/skos-reference/ · PROV-O — https://www.w3.org/TR/prov-o/ · Schema.org — https://schema.org/ · MCP — https://modelcontextprotocol.io/specification/2025-11-25 · llms.txt — https://llmstxt.org/ · KCP — https://github.com/cantara/knowledge-context-protocol · W3C Holon CG — https://www.w3.org/community/holon/

**Reviewers/critics:**
- KCP ↔ OKF production discussion — https://wiki.totto.org/blog/2026/02/28/kcp-and-mcp-one-protocol-for-structure-one-for-retrieval/ — timestamp≠validity, cross-org trust, supersession.
- July 2026 knowledge-centric information-systems vision paper — OKF/LLM-wiki as transition evidence, not endpoint.
- July 2026 memory benchmarking paper — OKF memory improved retrieval precision, did not solve selection/session drift.

**Local inputs:**
- `MicroWebStacks\astro-huge-doc\plans\2026-07\19\okf-support\handoff.md` — non-goals §4, source-authoritative rule §23, relation-inference limits §10.
- `...\okf-support\survey.md` — layered-architecture verdicts and final judgement.
- `...\okf-support\deep-research-report.md` — adoption evidence, toolchain, critiques, timeline.
- `...\okf-support\plan.md` — OKF-native implementation stance, RK-3 spec-drift hedge.
- [memory/2026-07/12/composable-context/readme.md](../../12/composable-context/readme.md) — staging-not-authority doctrine, promotion ladders, composition manifest.

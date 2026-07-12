# Composable Context: Git Repositories as the Unit of Agentic Knowledge, Code, and Governance

**Draft white paper — Request for Comments**
W. Filali — July 2026 — v0.1

---

## Abstract

Agentic systems are converging on selective context loading, memory lifecycles, and skill packaging — but each harness solves these separately, with machine-local memory, vendor-specific skill formats, and no shared notion of quality ownership. We propose **composable context**: a conventional Git repository layout in which volatile fetched material, episodic investigation notes, curated knowledge, and proven scripts occupy distinct lifecycle tiers, and in which repositories import one another through a manifest that **flattens** their contents into a single navigable surface. The repository becomes the unit of ownership, promotion, quality gating, and composition — a bundle maintained by an owning entity, offering a stronger trust guarantee than users hand-picking individual skills and dependencies. The scheme is harness-agnostic, relies only on folder-structure convention, and deliberately splits responsibility: composition governs *what exists and is trusted*; the agentic harness decides *what is loaded for a given task*. This draft solicits comments before elaboration into a full paper.

---

## 1. Motivation

Three pressures shape current agentic practice:

**Context pollution.** Flooding the prompt with every available tool and document degrades model behavior. The ecosystem's answer is selective loading — deferred tool search, on-demand capabilities, subagent windows, compaction. These mechanisms answer *how to load lazily*, but not *what corpus of tools and knowledge should exist, who vouches for it, and how it matures*.

**Missing lifecycle.** Research increasingly treats raw traces, memories, skills, and rules as points on one compression continuum, yet mainstream harnesses persist memory machine-locally, outside version control, review, and sharing. There is no first-class path by which a scratch experiment becomes a reusable script, or a fetched document becomes curated knowledge.

**Fragmented trust.** Skills, MCP servers, and plugins are selected one by one, shifting the quality burden onto each end user. What is missing is a **higher-level functional unit**: a deduplicated, quality-checked bundle of tools, scripts, and knowledge with a responsible maintainer.

Composable context addresses all three with one abstraction the software world already trusts: the repository.

---

## 2. The Context Repository

A context repository is an ordinary Git repository with a conventional structure. Code dependencies remain under classical package managers (uv, npm, …); the convention governs *knowledge and maturity*, not packaging.

```
context-repo/
├── .cache/                 gitignored — volatile
│   ├── ...                 fetched data & evidence (task-local)
│   └── src/                scratchpad code, quick experiments
├── memory/                 git-persisted episodic investigations
│                           worth sharing
├── knowledge_base/         curated, reviewed content
├── src/                    proven, reusable scripts
│   └── specification/      spec-driven development of scripts
└── manifest                imports of other context repositories
```

The tiers map directly onto the agent-memory vocabulary now standard in both practice and research: `.cache` is **working memory**, `memory/` is **episodic memory**, `knowledge_base/` is **semantic memory**, and `src/` holds **procedural memory**. Unlike harness-local memory stores, every persistent tier is a Git artifact — versioned, diffable, reviewable, shareable.

### 2.1 Two promotion ladders

Content moves upward only by demonstrated value, never automatically:

```
CODE       .cache/src ──(proven reuse benefit)──▶ src/
                                       (spec-driven, packaged)

KNOWLEDGE  .cache ──▶ memory/ ──▶ knowledge_base/ ──▶ export to
           volatile   episodic     curated            authority
                                                      sources
```

The code ladder promotes scratch experiments into `src/` once reuse is proven, under `src/specification/` for spec-driven development. The knowledge ladder promotes fetched evidence into episodic memory when an investigation is worth sharing, then into the knowledge base after curation — and from there, curated content can be **exported back to external authority sources**, closing a feedback loop (§5).

Each promotion is a Git commit: the quality gate is a code-review gate, operated by the repository's owning entity.

---

## 3. Composition

A context repository imports others by declaring them in a **manifest**. Composition is independent of code package management and operates by **flattening**: the contents of all imported repositories are merged into one unified navigable surface.

```
  repo-A (manifest: B, C)          repo-B (manifest: A, C)
        │                                │
        ▼         same surface           ▼
  ┌───────────────────────────────────────────┐
  │   FLATTENED SURFACE  =  A ∪ B ∪ C         │
  │   skills · scripts · knowledge · memory   │
  └─────────────────────┬─────────────────────┘
     composition:       │      governance & selection
                        ▼
  ┌───────────────────────────────────────────┐
  │   AGENTIC HARNESS (single context)        │
  │   lazy loading · per-task tool filtering  │
  └─────────────────────┬─────────────────────┘
                        ▼
              small active working set
              materialized in the prompt
```

Flattening makes composition **order-independent**: whether repo-A imports repo-B or repo-B imports repo-A, the agent sees the same surface. Repositories are therefore peers in a knowledge graph rather than nodes in a dependency hierarchy.

Because each imported repository is already a deduplicated, quality-gated bundle, composition operates at a coarser and safer granularity than per-skill selection: importing a context repo is closer to adopting a *capability group* — tools, their scripts, and their knowledge base together — than to installing a single tool.

### 3.1 Split of responsibility

Composable context deliberately does **not** perform per-task tool filtering. Automated discovery, lazy tool selection, and context-window optimization are the harness's job, and modern harnesses do it well. The split is:

- **Composition** — governance and selection of the *total* navigable surface: what exists, in which version, vouched for by which maintainer.
- **Harness** — from that operable surface, filtering the relevant slice for a given prompt or task.

This keeps composable context harness-agnostic: any harness that can walk a folder structure can consume a composed context. A refinement worth exploring (§9) is a *smart manifest* in which each repository declares a scope, so that composition itself pre-filters which repositories are even relevant to a task class — a coarse filter ahead of the harness's fine one.

---

## 4. Composition Within One Context, Not Across Agents

A2A-style protocols target the same composition problem at the *service* level: independent agents, each with private context, exchanging tasks. We acknowledge this as a plausible direction, but flattening into a **single harness** offers a materially different trade-off:

- **No context-transfer loss.** Inter-agent handoffs compress and drop information at every boundary; a unified surface keeps all evidence inside one reasoning space.
- **Unified caching and reasoning.** One LLM context benefits fully from prompt caching and cross-domain reasoning over the whole composed surface.
- **A cleaner privilege model.** Because tools are flattened, the top-level composing context faces every tool *directly*, with its own access rights and credentials. There is no higher-privileged agent whose outputs, laundered through delegation, leak privileged information to a less-privileged one.

Multi-agent composition remains complementary for genuinely separate trust or execution domains; within one owning entity's scope, flattening is simpler and stronger.

---

## 5. Staging, Not a New Source of Authority

Composable context takes a firm position: **the best-quality knowledge lives in its original authoring tools** — requirements management systems, team wikis, ticketing systems. Agentic workflows should not disrupt these authority sources, and the context repository does not aspire to become a new knowledge storage standard.

```
 AUTHORITY SOURCES                      CONTEXT REPO
 (wiki · requirements ──── fetch ────▶  .cache        volatile
  tickets · docs)                          │  user-initiated
        ▲                                  ▼  promotion
        │                               memory/       episodic
        │                                  │  curation staging
        │                                  ▼
        └───── curated export ◀──── knowledge_base/   semantic
                                                      staging
```

The repository's role is **last-mile knowledge management**: `.cache` accelerates task-specific processing; `memory/` and `knowledge_base/` are *staging areas* where agentic output waits for human curation before being fed back into the authority sources. A context repo *can* be operated as a full knowledge base in its own right, but that is a side possibility — the leverage of composable context is as a **human/agent contribution workflow**, not a replacement for where knowledge authoritatively lives.

---

## 6. Retrieval Abstraction

Composition defines the surface; retrieval makes it usable, and the design must not undersell it. The surface should remain amenable to the full retrieval spectrum:

- **Structured:** full-text search, vector search, hybrid retrieval with reranking, classical RAG, SQL over structured metadata, ontology-constrained composition (e.g. LinkML), and graph queries.
- **Unstructured:** conversion frameworks such as Docling unify heterogeneous documents into a source-format-independent *element space* (tables, diagrams, paragraphs) that preserves source references and can be indexed by all structured mechanisms above.
- **Hierarchical routing:** progressive routing through hierarchical summaries (RAPTOR-style) into large corpora, injecting larger last-mile documents into context. More expensive than search-based RAG, but with higher retrieval power when routing is reliable.

Nothing in the folder convention prescribes an index; it prescribes a stable, composable substrate over which any of these indexes can be built.

---

## 7. Security and Governance

**User-initiated promotion only.** The memory-poisoning literature shows that automatically harvested long-term memory can bias retrieval, tool selection, and control flow across future tasks. Composable context therefore rejects automated extraction from unmonitored conversation threads. Promotion is agent-*assisted* but user-*initiated* — e.g. *"extract the lesson learned from this conversation into this markdown file, and let me review it before commit."* Every write to a persistent tier passes through explicit human review and a Git commit.

**Ownership as a security boundary.** The owning entity's quality gate is not merely a product preference; as memory becomes durable and composable, it becomes an attack target, and curated promotion is the defense. Trust attaches to the repository and its maintainers, in exactly the way software supply chains already attach trust to packages and their owners.

**Direct tool exposure.** As noted in §4, flattening means the composing context confronts each tool's real credential and access-rights system directly. This avoids the confused-deputy pattern of privileged agents serving lower-privileged callers.

---

## 8. Position Relative to Existing Work

The ecosystem has all the ingredients, held apart. Repo-native harnesses (Claude Code, OpenCode) treat the repository as a live boundary for instructions, commands, and tools — but stop short of a knowledge lifecycle or cross-repo flattening. Pydantic AI's *capabilities* are the closest composition primitive — typed, reusable bundles with explicit loading semantics — but are library-level, not repository-level. Harness memory (Claude auto-memory, LangGraph stores, ADK Memory Bank) is durable but machine- or platform-local rather than Git-native. Research (MemGPT, Voyager, the experience-compression line, MemOS, Infini Memory) converges on tiered memory, skill libraries grown from traces, and memory as a governed, versioned resource — precisely the properties Git already provides for free.

Composable context sits at the intersection: the repo-native shell of OpenCode, the bundle semantics of capabilities, and the lifecycle tiers of the memory literature, unified under one folder convention and one manifest.

---

## 9. Open Questions — Request for Comments

1. **Manifest semantics.** Minimal format? How are versions pinned, and how are name collisions in the flattened surface resolved (namespacing vs. deduplication)?
2. **Scoped composition.** Should repositories declare task scopes so a smart manifest pre-filters relevant repos before the harness's per-task filtering? To what extent do current plugin systems (marketplaces, capability groups) already behave this way?
3. **Flattening mechanics.** Materialized merge (symlinks/copy) vs. virtual overlay presented to the harness? How are `.cache` tiers kept strictly local while shared tiers compose?
4. **Export protocol.** What does the curated-export step back into authority sources look like concretely — PR-like review objects in the target systems?
5. **Interoperability.** Should a composed context compile outward into MCP resources/tools so non-filesystem harnesses can consume it?
6. **Evaluation.** What benchmark would demonstrate the claimed benefits (retrieval quality on composed surfaces, reduction in context pollution, poisoning resistance of gated promotion)?

Comments on any of the above — and on whether the repository is the right unit at all — are explicitly invited.

---

## Selected References

Full list of 78 references: [context-composition-references.md](./context-composition-references.md).

1. Anthropic — *Effective context engineering for AI agents*.
2. OpenAI — *Skills*, *Tool search*, *Compaction* (API guides).
3. Pydantic AI — *Capabilities* (core concepts).
4. OpenCode — *Rules*, *References*, *Config* (docs).
5. Model Context Protocol — Specification 2025-06-18.
6. A2A Protocol — *What is A2A?*
7. Packer et al. — *MemGPT: Towards LLMs as Operating Systems*, arXiv:2310.08560.
8. Wang et al. — *Voyager: An Open-Ended Embodied Agent with LLMs*, arXiv:2305.16291.
9. Sarthi et al. — *RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval*, arXiv:2401.18059.
10. *Experience Compression Spectrum: Unifying Memory, Skills, and Rules in LLM Agents*, arXiv:2604.15877.
11. *MemOS: An Operating System for Memory-Augmented Generation*, arXiv:2505.22101.
12. *Infini Memory: Maintainable Topic Documents for Long-Term LLM Agent Memory*, arXiv:2606.10677.
13. *A Systematic Study of Memory Poisoning Attacks in LLM Agents*, arXiv:2606.04329.

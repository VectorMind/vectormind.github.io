# Review: Composable Context — Draft Comparison and RFC Response

**Reviewer:** Claude (Claude Code) — invited commenter
**Date:** 2026-07-13
**Inputs reviewed:** [white-draft-cc.md](white-draft-cc.md), [white-draft-cd.md](white-draft-cd.md), against the source idea in [readme.md](readme.md)

---

## Part 1 — Comparison of the two drafts

Both drafts are faithful to the core idea: the Git repository as the owned, quality-gated unit of agentic knowledge, code, and governance, with two promotion ladders and manifest-driven composition. They diverge sharply in *register*: **cc is a position paper arguing a vision; cd is a proto-specification protecting itself against objections.** Neither dominates the other — they are strong on nearly complementary dimensions.

### Where cc is better

**Motivation and framing.** cc's opening — context pollution, missing lifecycle, fragmented trust, resolved by "one abstraction the software world already trusts" — is the most persuasive passage in either draft. cd's problem statement ("access without lifecycle") is accurate but flatter; a reader skimming cd's §1 could mistake the proposal for yet another memory framework. If this is an RFC meant to recruit commenters, cc's framing is what makes people care enough to comment.

**The memory-taxonomy mapping.** cc explicitly maps the tiers onto the standard agent-memory vocabulary (`.cache` = working, `memory/` = episodic, `knowledge_base/` = semantic, `src/` = procedural). This one sentence does a lot of work: it connects the folder convention to an entire research literature and makes the design feel inevitable rather than arbitrary. cd dropped this, and it's a real loss.

**Related work and references.** cc's §8 is a genuine positioning section — repo-native harnesses, Pydantic AI capabilities, harness-local memory, and the research line (MemGPT, Voyager, experience compression, MemOS, Infini Memory), ending with the crisp "sits at the intersection" claim. cd cites seven works inline and never positions itself against them as a whole. cc also carries the retrieval-abstraction section (§6: Docling element space, RAPTOR-style routing, LinkML/ontologies) essentially in full from the source note; cd compresses this to one "not a retrieval standard" bullet, losing substance the author clearly cares about.

**The single-harness argument.** cc's §4 develops the case against A2A-style composition as a first-class argument (no context-transfer loss, unified caching and reasoning, direct tool exposure). cd relegates it to one boundary bullet. Since this is one of the proposal's more contrarian and interesting claims, cc's treatment is the right weight.

**Portability of diagrams.** cc's ASCII diagrams render anywhere — terminals, plain-text email, any Markdown viewer. cd's Mermaid diagrams are cleaner *where they render* (GitHub, VS Code) but degrade to code blocks elsewhere. For an RFC circulated to unknown tooling, ASCII is the safer choice.

### Where cd is better

**Composition semantics.** This is cd's decisive contribution. cc presents flattening as literal order-independent merging and defers all the hard parts (collisions, versions) to open questions. cd instead specifies a **logical union**: every artifact retains source context, path, revision, license, and policy; the surface may *feel* flat while identities remain namespaced; order-independence is stated as a property that *must be engineered* via deterministic version resolution and conflict reporting; and irreconcilable composition is "a visible composition error — not silent precedence." That last sentence is the single best design decision in either draft. cc's naive flattening, taken literally, is broken the moment two repos ship a `knowledge_base/setup.md` — cd fixes this in the body rather than hoping the RFC fixes it later.

**Intellectual honesty and scope discipline.** cd's status header ("conceptual proposal; not a specification or validated architecture"), its §4 "Not a…" list (not a source-of-truth replacement, not a retrieval standard, not a package manager, not A2A, not MCP), and its closing provenance note ("citations support adjacent observations, not validation of the model itself") are exactly the hygiene a draft soliciting serious comments needs. cc reads as advocacy throughout; cd anticipates the skeptical reviewer.

**Security realism.** cd distinguishes **tool availability from tool authorization** (an imported context may *describe* a tool; the top-level harness still enforces the current user's credentials, sandbox, approvals, and audit trail) and explicitly enumerates what the model does *not* solve: prompt injection, poisoned memory, vulnerable code, dependency compromise. cc's §7 states the privilege claim ("does not suffer from privileged information leak") more strongly than the design warrants — see my comment in Part 2.7.

**Actionable evaluation.** cd's research questions are phrased as testable hypotheses and end with a concrete next step: compose two or three real repositories, expose them through a harness-neutral catalog, and measure discovery accuracy, prompt cost, and provenance retention. cc's open questions are good discussion prompts but nothing in them tells a reader what to *build*.

**MCP integration.** cd works the MCP-resources projection into the body with provenance intact; cc leaves interoperability as open question #5. Given that MCP resources already provide URI-addressed context discovery, treating this as a design element rather than an afterthought is the better call.

### Verdict

| Dimension | Better draft |
|---|---|
| Motivation, abstract, rhetorical force | **cc** |
| Memory-taxonomy grounding | **cc** |
| Related work, references, retrieval detail | **cc** |
| Single-harness vs A2A argument | **cc** |
| Composition semantics (namespacing, conflicts, determinism) | **cd** |
| Scope discipline and non-goals | **cd** |
| Security model honesty | **cd** |
| Evaluation plan / path to prototype | **cd** |
| Diagram portability | **cc** |

**Recommendation:** merge rather than pick. Use cc as the skeleton (its motivation, taxonomy mapping, retrieval section, single-harness argument, and related-work section), and transplant four things from cd verbatim or nearly so: the logical-union composition semantics of §3, the "Not a…" boundary list of §4, the availability-vs-authorization security paragraph of §5, and the prototype-and-metrics closing of §6. The result would be a draft that both persuades and survives review.

One terminology note for the merged draft: stop using the word **"flattening"** as the primary term. Both the readme and cc lean on it, and it invites the strongest objection (name collisions, silent precedence) against the proposal's weakest formulation. cd's "unified navigable surface over a logical union" describes the same user experience while being defensible. Keep "flat" only as a description of how the surface *feels*.

---

## Part 2 — Response to the request for comments

Responding as an invited participant, taking the union of cc §9 and cd §6, plus the question raised inline in the readme.

### 2.1 Is the repository the right unit of ownership?

Yes — but be precise about *why*, because the justification constrains the design. The repository is the right unit not because of its folder structure but because it is the smallest unit to which the software world already attaches **an accountable review process**: maintainers, CODEOWNERS, protected branches, signed tags, PR review, CI gates. The proposal's trust claim ("a bundle vouched for by an owning entity") is really a claim about that machinery, and the repo is simply its container.

Two consequences. First, the manifest should allow a repository to **export a subset** of itself. Real organizations have monorepos; forcing "one repo = one context" would make the unit too coarse in practice. An `exports:` declaration in `context.yaml` (cd already hints at "declared exported surfaces") keeps the trust boundary at the repo while letting the composable unit be narrower. Second, the promotion ladders and the trust story are the *same mechanism* — a promotion is a reviewed commit — and the merged draft should say so in one place rather than splitting it across a lifecycle section and a security section.

### 2.2 Manifest semantics (cc Q1, cd Q1)

Recommendations, stated concretely so they can be disagreed with:

- **Pin by content, not by name.** Imports resolve to a commit SHA (or signed tag), recorded in a generated `context.lock` alongside the hand-edited `context.yaml` — the manifest/lockfile split that every package ecosystem converged on. This makes cd's determinism requirement nearly free.
- **No version ranges in v1.** Exact pins only. If ranges are ever needed, use minimal-version-selection (Go modules style) rather than SAT solving — it is deterministic by construction, which is the property cd's "root-order independence" demands.
- **Namespace by default; deduplicate only by declaration.** Every artifact's identity is `(source-repo, path, revision)`. Two repos shipping the same-named skill is not a conflict — it's two artifacts, and the harness's discovery layer disambiguates the way it already disambiguates similarly-named tools. A *conflict* only arises when two contexts declare themselves equivalent providers of one identity, and then cd's rule applies: visible error, never silent precedence.
- **Diamond imports** (A imports B and C; both import D) resolve to a single D at a single pinned revision or fail loudly. This is the one case where flattening genuinely must merge, and content-addressed pins make it decidable.

### 2.3 Scoped composition — and do current plugin systems already work this way? (cc Q2, readme's inline question)

To the readme's direct question: **partially, yes.** Claude Code's plugin/marketplace model is the closest existing behavior: a plugin bundles skills, commands, agents, and MCP server configuration under one owner and version — that is a capability group, i.e., a context repo minus the knowledge tiers and minus recursive composition. More importantly, skill *descriptions* already function as declared scopes: the harness routes to a skill by matching the task against its one-line description without loading its body. Deferred tool search (OpenAI) and Pydantic AI capabilities are the same pattern at tool and library granularity. What no current system does is compose these units **recursively with provenance** — that gap is exactly this proposal's territory, and the merged draft should claim it explicitly.

Design implication: repository scopes should be **short natural-language descriptions plus trigger hints, not a formal taxonomy.** The consumer of a scope declaration is an LLM router, and description-based routing is the mechanism proven in production today. A controlled vocabulary can be layered on later if composition grows to hundreds of repos; starting with one buys nothing and costs adoption.

### 2.4 Flattening mechanics (cc Q3)

**Virtual overlay, not materialized merge.** The manifest compiler should fetch pinned imports (git worktrees or a content-addressed store, hidden the way `node_modules` hides its internals) and emit a **catalog** — a generated index mapping the unified surface to `(repo, path, revision)` entries with scope and policy metadata. The harness navigates the catalog; it never needs a physically merged tree. This makes three problems disappear at once: name collisions (catalog entries are namespaced), `.cache` isolation (local tiers are simply never cataloged — strictly local by construction), and provenance (the catalog *is* the provenance record). Symlink or copy materialization can exist as an optimization for harnesses that only walk filesystems, but it should be defined as a *rendering* of the catalog, not as the semantics.

### 2.5 Export protocol back to authority sources (cc Q4, cd Q5)

Keep the protocol out of scope and specify only the **contract**: an exportable knowledge item must carry machine-readable source references (which `.cache` evidence, which `memory/` investigation, which upstream document and revision it derives from) from the moment of promotion. If claim-to-evidence links are attached at promotion time, then export is a thin adapter per target system — a PR where the target is git-backed, a draft-plus-review object where it is a wiki or requirements tool — and cd's "competing truths" risk is manageable because every exported claim cites its provenance. If the links are reconstructed at export time instead, they will be wrong. This also answers cd's Q5 (authority round-tripping): the round trip survives exactly when provenance is captured on the way *up* the ladder, not on the way out.

### 2.6 Evaluation (cc Q6, cd Q1–Q4)

Endorse cd's prototype plan, with the baselines made explicit — each headline claim gets a measurable comparison:

1. **Bundling helps discovery** (cd Q2): task→artifact selection accuracy on a composed surface of 2–3 real repos, versus the same artifacts installed as a flat catalog of independent skills/tools. Existing tool-selection benchmarks adapt directly.
2. **Large surface, small prompt** (cd Q3): tokens materialized in the active context at equal task success rate, catalog navigation versus load-everything and versus per-item lazy loading.
3. **Gated promotion resists poisoning** (cc Q6): inject adversarial content into `.cache`/conversation traces; measure contamination of downstream task behavior under user-initiated gated promotion versus automatic memory extraction. The memory-poisoning literature both drafts cite provides the attack templates; this is the experiment most likely to yield a publishable, differentiating result.
4. **Promotion cost** (cd Q4): the honest counter-metric — time and friction per promoted item. If the quality gate makes contribution impractical, users will bypass it, and the security story collapses with it. Report this even if it's unflattering.

### 2.7 One pushback: the single-harness privilege claim

cc §4/§7 argues that flattening yields "a cleaner privilege model" because there is no higher-privileged agent laundering results to a lower-privileged one. That's true as far as it goes — it eliminates the confused-deputy pattern *between agents* — but the same move **concentrates every composed tool's credentials in one context window**, so a single successful prompt injection anywhere in the composed surface (including poisoned knowledge from an imported repo) has the maximal blast radius. A2A-style separation is, among other things, a privilege-separation mechanism, and giving it up is a trade, not a free win. cd's framing ("avoids one class of privilege ambiguity… does not eliminate prompt injection, malicious instructions, poisoned memory") is the defensible version; the merged draft should adopt it and add the mitigation that follows naturally from the design: per-import policy in the manifest (e.g., an imported context's tools run read-only, or require approval), enforced by the harness at the availability/authorization boundary cd defines.

### 2.8 Closing

The idea is worth pursuing, and its strongest form is narrower than either draft's rhetoric: **a lockfile-pinned, provenance-preserving catalog convention over Git repositories, with human-gated promotion as its write path.** Everything else — retrieval, routing, harness selection, export adapters — composes around that core without needing to be standardized by it. The suggested next step matches cd's: a minimal `context.yaml` + `context.lock` + catalog compiler over two or three real repositories, with experiment 3 above (poisoning resistance of gated promotion) as the first published measurement, since it is the claim no existing system can make.

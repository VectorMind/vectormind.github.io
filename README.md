# VectorMind

VectorMind is a technical and scientific discussion space for artificial
intelligence topics. Its content should be grounded in inspectable evidence,
explicit sources, reproducible investigations, and curated reusable knowledge.

## Evidence maturation pipeline

The repository uses an **evidence maturation pipeline**: material moves from
exploration toward reuse only when its provenance, interpretation, and quality
are made explicit.

```text
.cache/                    local collection workspace; never committed
  src/                     downloaded or captured source material
  md/                      working notes and extracted text
  data/                    raw and intermediate datasets
  results/                 machine-generated intermediate results
  reports/                 provisional generated reports
memory/                    committed episodic investigation records
knowledge_base/            committed curated, structured reusable knowledge
src/                       local CLI, automation, and report-generation code
  specification/           durable contracts that drive src behavior
plans/                     dated work packets and status indexes
```

Promotion is not a blind file move. Every boundary requires review:

1. `.cache/` collects and transforms material without making it durable.
2. `memory/` records a bounded investigation, including sources, method,
   findings, uncertainty, and unresolved questions.
3. `knowledge_base/` contains reviewed claims and structures intended for reuse.
4. Published pages are generated from approved committed content, never
   directly from `.cache/`.

See [WORKFLOW.md](WORKFLOW.md) for the operating contract and
[AGENTS.md](AGENTS.md) for assistant routing.

## Current status

The repository workflow and content boundaries are scaffolded. The Pages
workflow is configured so a push to `main` renders the committed Markdown workspace with the reusable
`MicroWebStacks/astro-huge-doc` Action and deploys the resulting static
artifact to GitHub Pages. Deployment validation is tracked in
[`plans/open.md`](plans/open.md).

## License

MIT. See [LICENSE](LICENSE).

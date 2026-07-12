# Workflow

This repository supports technical and scientific AI discussions through a
provenance-preserving evidence maturation pipeline. Workflow state, evidence
state, implementation state, and published output are separate concerns.

## Repository areas

### `.cache/` - local evidence workspace

`.cache/` is ignored by Git. Use these local subfolders:

- `.cache/src/` for fetched, copied, or captured source material;
- `.cache/md/` for extraction output and working Markdown;
- `.cache/data/` for raw and intermediate datasets;
- `.cache/results/` for provisional machine results;
- `.cache/reports/` for provisional generated reports.

Files here may be incomplete, large, licensed for local use only, or generated.
They are inputs to review, not durable claims and not publication inputs.

### `memory/` - episodic investigations

An investigation is a bounded record of work on a question. It should identify:

- the question, scope, and date;
- sources with stable identifiers or URLs and retrieval dates;
- methods, tools, queries, and transformations;
- observations separately from interpretation;
- findings, confidence, limitations, contradictions, and open questions;
- links to promoted knowledge, when promotion occurs.

Memory may preserve negative results and uncertainty. It is evidence of an
investigation, not automatically a reusable truth statement.

### `knowledge_base/` - curated reusable knowledge

Knowledge-base content is reviewed and structured for reuse. Each material
claim must remain traceable to committed investigation records or directly to
stable sources. Curated content should state its scope, confidence, freshness or
review date, and known disagreements. When evidence changes, revise the curated
content without erasing the investigation history.

### `src/` and `src/specification/`

`src/` contains the local CLI, scripts, automation, result generation, and
report generation. Do not store collected evidence or generated results there.

`src/specification/` contains durable behavioral contracts for `src/`. For a
non-trivial automation change:

1. write or update the relevant specification;
2. create a dated plan when the work is complex;
3. implement against the specification;
4. validate with focused tests or reproducible commands;
5. record implementation facts in the plan packet.

## Promotion gates

Use these gates before material advances:

| From | To | Required gate |
| --- | --- | --- |
| `.cache/` | `memory/` | Source identity, retrieval date, method, scope, and limitations are recorded; unsafe or unlicensed payloads stay local. |
| `memory/` | `knowledge_base/` | Claims are reviewed, evidence links resolve, contradictions and uncertainty are represented, and the result is structured for reuse. |
| `knowledge_base/` | website | Content is approved, contains no local/private material, passes rendering checks, and preserves citations and provenance. |

Nothing is promoted solely because an automated process produced it. When a
claim cannot pass a gate, keep it in the earlier layer and record why.

## Plans

Complex work uses dated packets:

```text
plans/YYYY.MM/
  DD/
    <title-slug>/
      plan.md
      implementation.md  # create only after implementation starts
      test.md             # optional preserved verification
```

`plan.md` should capture the problem, goals, scope, non-goals, dependencies,
risks, open decisions, phases, and exit criteria. Use stable open-point IDs such
as `OP-001` when a decision must survive across sessions.

`implementation.md` is a factual log, not a second plan. It records what
landed, deviations, files changed, and remaining risks. Begin it with a status
line such as `[##--] Phase 2/4 - ...`; use `[####] Done - ...` when the planned
implementation is complete.

Keep these indexes synchronized:

- `plans/open.md` lists packets with incomplete implementation or unresolved
  planning decisions;
- `plans/closed.md` lists completed implementations and settled planning-only
  packets.

## Website and generated reports

Published output must be reproducible from committed, approved inputs. Website
build tooling may read `memory/` and `knowledge_base/`, but default navigation
should distinguish episodic investigations from curated knowledge. It must not
read `.cache/` in CI.

Generated reports remain in `.cache/reports/` until reviewed. If a report is
accepted as durable content, promote its source-backed content into `memory/`
or `knowledge_base/`; do not treat generated formatting as provenance.

## Validation and ownership

Use the smallest meaningful validation: link/citation checks for evidence,
schema and focused tests for `src/`, document consistency checks for workflow
changes, and a production build plus Pages artifact check for website changes.
Record durable proof in the relevant packet's `test.md` or
`implementation.md`.

The maintainer owns Git history and external publication. Agents leave changes
in the working tree unless explicitly asked to commit, push, deploy, publish, or
modify another repository.

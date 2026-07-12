# Agent Guidance

Use [WORKFLOW.md](WORKFLOW.md) as the workflow contract. This file is routing
only.

- Put uncommitted collection inputs and generated working artifacts in
  `.cache/`; never cite them as curated repository knowledge.
- Put bounded, source-backed investigation records in `memory/`.
- Put reviewed, reusable content in `knowledge_base/` only after satisfying the
  promotion gates in `WORKFLOW.md`.
- Keep automation in `src/` and define durable behavior first in
  `src/specification/`.
- Decompose complex work into `plans/YYYY.MM/DD/<title-slug>/plan.md` and keep
  `plans/open.md` current. Add `implementation.md` only once work occurs.
- Read the nearest README or specification before changing a governed area.
- Preserve source links, retrieval dates, transformations, uncertainty, and
  claim-to-evidence distinctions.
- Do not commit `.cache/`, generated reports, credentials, or fetched corpora.
- Do not commit, push, publish, deploy, or change external repositories unless
  the maintainer explicitly requests it.

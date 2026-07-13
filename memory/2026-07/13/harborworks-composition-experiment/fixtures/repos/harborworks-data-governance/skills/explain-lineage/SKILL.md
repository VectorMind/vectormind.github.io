---
name: explain-lineage
description: Use data-governance knowledge for a shallow briefing task.
context-functions: briefing
context-domains: data-governance
---

# Explain Lineage

1. Read [`knowledge_base/overview.md`](../../knowledge_base/overview.md) from the owning context.
2. Invoke `python src/cli.py --skill explain-lineage --knowledge knowledge_base/overview.md` from the repository root.
3. Return the CLI result together with the catalog identity for
   `org.harborworks.domain.data.governance:knowledge_base/overview.md`.

Do not embed domain facts in this skill; the knowledge base and CLI are the
owned surfaces.

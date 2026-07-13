---
name: explain-maintenance
description: Use facilities-operations knowledge for a shallow briefing task.
context-functions: briefing
context-domains: facilities-operations
---

# Explain Maintenance

1. Read [`knowledge_base/overview.md`](../../knowledge_base/overview.md) from the owning context.
2. Invoke `python src/cli.py --skill explain-maintenance --knowledge knowledge_base/overview.md` from the repository root.
3. Return the CLI result together with the catalog identity for
   `org.harborworks.domain.facilities.operations:knowledge_base/overview.md`.

Do not embed domain facts in this skill; the knowledge base and CLI are the
owned surfaces.

---
name: inspect-work-order
description: Use facilities-operations knowledge for a shallow analysis task.
context-functions: analysis
context-domains: facilities-operations
---

# Inspect Work Order

1. Read [`knowledge_base/overview.md`](../../knowledge_base/overview.md) from the owning context.
2. Invoke `python src/cli.py --skill inspect-work-order --knowledge knowledge_base/overview.md` from the repository root.
3. Return the CLI result together with the catalog identity for
   `org.harborworks.domain.facilities.operations:knowledge_base/overview.md`.

Do not embed domain facts in this skill; the knowledge base and CLI are the
owned surfaces.

---
name: check-inspection
description: Use facilities-operations knowledge for a shallow analysis task.
context-functions: analysis
context-domains: facilities-operations
---

# Check Inspection

1. Read [`knowledge_base/overview.md`](../../knowledge_base/overview.md) from the owning context.
2. Invoke `python src/cli.py --skill check-inspection --knowledge knowledge_base/overview.md` from the repository root.
3. Return the CLI result together with the catalog identity for
   `org.harborworks.domain.facilities.operations:knowledge_base/overview.md`.

Do not embed domain facts in this skill; the knowledge base and CLI are the
owned surfaces.

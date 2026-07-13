---
name: trace-artifact
description: Inspect composition metadata without embedding repository facts.
context-functions: composition
context-domains: context-management
---

# Trace Artifact

1. Read [`knowledge_base/overview.md`](../../knowledge_base/overview.md) from the owning context.
2. Invoke `python src/cli.py --skill trace-artifact --knowledge knowledge_base/overview.md` from the repository root.
3. Return the CLI result together with the catalog identity for
   `org.harborworks.context.core:knowledge_base/overview.md`.

Do not embed domain facts in this skill; the knowledge base and CLI are the
owned surfaces.

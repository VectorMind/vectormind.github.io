---
name: analyze-signal
description: Use the analysis method over selected domain knowledge.
context-functions: analysis
context-domains: "*"
---

# Analyze Signal

1. Read [`knowledge_base/overview.md`](../../knowledge_base/overview.md) from the owning context.
2. Invoke `python src/cli.py --skill analyze-signal --knowledge knowledge_base/overview.md` from the repository root.
3. Return the CLI result together with the catalog identity for
   `org.harborworks.methods.analysis:knowledge_base/overview.md`.

Do not embed domain facts in this skill; the knowledge base and CLI are the
owned surfaces.

---
name: create-checklist
description: Use the remediation method over selected domain knowledge.
context-functions: remediation
context-domains: *
---

# Create Checklist

1. Read [`knowledge_base/overview.md`](../../knowledge_base/overview.md) from the owning context.
2. Invoke `python src/cli.py --skill create-checklist --knowledge knowledge_base/overview.md` from the repository root.
3. Return the CLI result together with the catalog identity for
   `org.harborworks.methods.remediation:knowledge_base/overview.md`.

Do not embed domain facts in this skill; the knowledge base and CLI are the
owned surfaces.

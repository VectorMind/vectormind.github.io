---
name: inspect-release
description: Use software-delivery knowledge for a shallow analysis task.
context-functions: analysis
context-domains: software-delivery
---

# Inspect Release

1. Read [`knowledge_base/overview.md`](../../knowledge_base/overview.md) from the owning context.
2. Invoke `node src/cli.mjs --skill inspect-release --knowledge knowledge_base/overview.md` from the repository root.
3. Return the CLI result together with the catalog identity for
   `org.harborworks.domain.software.delivery:knowledge_base/overview.md`.

Do not embed domain facts in this skill; the knowledge base and CLI are the
owned surfaces.

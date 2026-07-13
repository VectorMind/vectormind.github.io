---
name: review-feedback
description: Use customer-operations knowledge for a shallow remediation task.
context-functions: remediation
context-domains: customer-operations
---

# Review Feedback

1. Read [`knowledge_base/overview.md`](../../knowledge_base/overview.md) from the owning context.
2. Invoke `node src/cli.mjs --skill review-feedback --knowledge knowledge_base/overview.md` from the repository root.
3. Return the CLI result together with the catalog identity for
   `org.harborworks.domain.customer.operations:knowledge_base/overview.md`.

Do not embed domain facts in this skill; the knowledge base and CLI are the
owned surfaces.

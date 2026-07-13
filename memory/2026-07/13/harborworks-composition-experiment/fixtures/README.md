# Harborworks fixture corpus

This folder preserves the committed inputs for the 2026-07-13 manifest-
composition experiment. The nine repositories under `repos/` are fictional,
small, and deliberately repetitive. `variants/` and `scenarios/` contain
negative and order-independence cases.

Every `context.yaml` is JSON-compatible YAML. This is a dependency-free
prototype choice, not a decision about the durable manifest format. Fixture
revision strings simulate immutable releases; nested `.git` metadata is not
stored.

Each repository contains six shallow skills. Skills route to the owning
`knowledge_base/` and dependency-free `src` CLI, and intentionally avoid
embedding the knowledge they consume. Repeated paths such as
`knowledge_base/glossary.md` and repeated skill concepts are deliberate
collision probes.

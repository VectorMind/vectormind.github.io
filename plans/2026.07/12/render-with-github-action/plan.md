# Reusable renderer and GitHub Pages deployment

## Status

Proposed. No renderer or workflow code has been changed.

## Problem

This organization site should be generated on pushes to `main`, using the newer
rendering capabilities maintained in `C:\dev\MicroWebStacks\astro-huge-doc`
rather than copying the older Astro application from
`C:\dev\HomeSmartMesh\homesmartmesh.github.io`.

The reference Pages workflow uses `withastro/action@v2` followed by
`actions/deploy-pages@v4`. The current `astro-huge-doc` root package is private,
builds with Astro's Node adapter, and declares `output: "server"`; it is not yet
a consumer-facing static Pages builder.

## Recommendation

Add a **thin reusable static-render interface** to `astro-huge-doc`, then expose
it to repositories through a versioned composite GitHub Action or an equivalent
versioned CLI package. Keep this interface separate from the VS Code extension
packaging and runtime.

The important reuse boundary is the renderer command and content contract. The
Action should orchestrate that public boundary; it should not duplicate renderer
source or reach into extension internals. This preserves a single rendering
implementation without turning the extension itself into deployment machinery.

## Proposed ownership split

### `astro-huge-doc`

- Define a documented static build command that accepts a consumer content root,
  output directory, profile, and site/base URL without relying on repo-local
  `.env` state.
- Produce a static directory suitable for `actions/upload-pages-artifact`.
- Publish or tag a stable reusable entry point.
- Optionally provide `action.yml` as a thin composite wrapper around the same
  command.
- Test static mode separately from the Node server and VS Code extension modes.

### `vectormind.github.io`

- Own content selection, site metadata, navigation policy, and Pages settings.
- Pin a released tag or commit of the reusable renderer/Action.
- Run provenance/content checks before rendering.
- Upload and deploy the generated static artifact with official Pages actions.

## Why this is feasible

GitHub composite actions can execute setup and build steps from another
repository, and GitHub Pages accepts a prebuilt static artifact. The blocking
technical gap is not GitHub Actions; it is establishing and validating a true
static-output mode and a stable consumer configuration contract in
`astro-huge-doc`.

## Scope

1. Specify the renderer's consumer-facing static build contract.
2. Implement and test static output in `astro-huge-doc` without regressing its
   server or VS Code extension profiles.
3. Choose the distribution boundary: versioned composite Action, published CLI,
   or both.
4. Add this repo's content configuration and Pages workflow.
5. Verify artifact routes, assets, base URL, citations, diagrams, and navigation
   on the organization domain.

## Non-goals

- Copy the renderer source into this repository.
- Make the VS Code extension responsible for CI deployment.
- Read `.cache/` during a website build.
- Deploy before the maintainer accepts the cross-repository interface.

## Open points

| ID | Question | Recommendation | Status |
| --- | --- | --- | --- |
| OP-001 | What is the reusable boundary? | A renderer CLI/static-build contract first, with a thin composite Action wrapper. | Awaiting acceptance |
| OP-002 | Where should `action.yml` live? | In `astro-huge-doc` if it remains a thin wrapper; use a dedicated action repo only if release cadence or permissions later diverge. | Awaiting acceptance |
| OP-003 | How is content mapped? | Explicit consumer config mapping `memory/` and `knowledge_base/`; never implicit scanning of `.cache/`. | Awaiting acceptance |
| OP-004 | How is the renderer version pinned? | Immutable release tag or full commit SHA, with deliberate update PRs. | Awaiting acceptance |

## Phases

1. Write a durable static-render contract in `astro-huge-doc` specification.
2. Add static build implementation and fixtures there; prove extension isolation.
3. Add and version the reusable Action/CLI boundary.
4. Add a pinned Pages workflow and site configuration here.
5. Validate the production artifact and organization-domain deployment.

## Risks

- Server-only routes, SQLite-backed features, or dynamic content may not have a
  valid static equivalent.
- Asset and link paths can break at the Pages base URL or custom domain.
- An Action pinned to a moving branch would make builds non-reproducible.
- Coupling Action inputs to extension internals would make both surfaces brittle.
- Third-party diagram or fetch services can make CI non-deterministic.

## Exit criteria

- A documented, versioned static renderer interface exists and is tested.
- The extension path remains independently buildable and packaged.
- This repo builds only from committed approved content.
- A push to `main` creates and deploys a reproducible Pages artifact.
- Production routes, assets, links, citations, and representative diagrams pass
  validation on the organization domain.

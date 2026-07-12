# Reusable renderer and GitHub Pages deployment

## Status

Implemented locally through Phase 4. The reusable renderer Action is consumed
from `MicroWebStacks/astro-huge-doc@main` with engine `0.0.10`; Phase 5 remains
open for the first GitHub Pages run and production route checks.

## Problem

This organization site should be generated on pushes to `main`, using the newer
rendering capabilities maintained in `C:\dev\MicroWebStacks\astro-huge-doc`
rather than copying the older Astro application from
`C:\dev\HomeSmartMesh\homesmartmesh.github.io`.

The reference Pages workflow uses `withastro/action@v2` followed by
`actions/deploy-pages@v4`. The current `astro-huge-doc` root package is private,
builds with Astro's Node adapter, and declares `output: "server"`; it is not yet
a consumer-facing static Pages builder.

## Accepted direction

Use the thin reusable static-render Action in `astro-huge-doc` from a workflow
owned by this repository. Run it on every push to `main` and allow manual
dispatch, upload the generated artifact with `actions/upload-pages-artifact`,
then deploy it with `actions/deploy-pages`.

The Action reference deliberately follows `MicroWebStacks/astro-huge-doc@main`
instead of an immutable release. This accepts upstream changes immediately and
is less reproducible than a tag or commit pin. The engine input remains an exact
published version because that is required by the Action contract.

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
| OP-001 | What is the reusable boundary? | Use the composite Action implemented in `astro-huge-doc`; this repo owns the push-to-`main` Pages workflow. | Accepted 2026-07-12 |
| OP-002 | Where should `action.yml` live? | Keep it in `astro-huge-doc`; this repo adds a consumer workflow comparable to the HomeSmartMesh Pages workflow. | Accepted 2026-07-12 |
| OP-003 | How is content mapped? | Render the committed consumer workspace. `.cache/` is Git-ignored and therefore absent from the checked-out CI workspace. | Accepted 2026-07-12 |
| OP-004 | How is the renderer version pinned? | Follow `MicroWebStacks/astro-huge-doc@main`; continue supplying the Action's required exact published engine version. | Accepted 2026-07-12 |

## Resolved engine-release dependency

Live verification on 2026-07-12 found:

- `MicroWebStacks/astro-huge-doc@main` resolves to commit
  `d319af05073d43c8cfe7b04eec4c3024f0863953` and contains `action.yml`;
- the Action requires an exact `engine-version` and verifies that the installed
  package contains `bin/md-render.js`;
- at takeover time npm published `@microwebstacks/md-render` only through
  `0.0.9`, while the upstream implementation record stated that those versions
  predated the reusable `build` command.

The maintainer subsequently published `0.0.10`. Local installation verified
that it contains `bin/md-render.js`, and a full render of this repository
completed successfully. The release dependency is resolved.

## Phases

1. Write a durable static-render contract in `astro-huge-doc` specification. **Done upstream.**
2. Add static build implementation and fixtures there; prove extension isolation. **Done upstream.**
3. Add and version the reusable Action/CLI boundary. **Done upstream; engine `0.0.10` published.**
4. Add a Pages workflow and site configuration here, using the Action from `main` and an exact compatible engine version. **Done locally.**
5. Validate the production artifact and organization-domain deployment. **Local artifact passed; GitHub run and deployed-site checks pending.**

## Risks

- Server-only routes, SQLite-backed features, or dynamic content may not have a
  valid static equivalent.
- Asset and link paths can break at the Pages base URL or custom domain.
- Following the Action's moving `main` branch makes builds non-reproducible;
  this is an explicitly accepted tradeoff.
- Coupling Action inputs to extension internals would make both surfaces brittle.
- Third-party diagram or fetch services can make CI non-deterministic.

## Exit criteria

- A documented, versioned static renderer interface exists and is tested.
- The extension path remains independently buildable and packaged.
- This repo builds only from committed approved content.
- A push to `main` creates and deploys a reproducible Pages artifact.
- Production routes, assets, links, citations, and representative diagrams pass
  validation on the organization domain.

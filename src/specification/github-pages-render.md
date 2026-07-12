# GitHub Pages rendering

## Purpose

The repository publishes its committed Markdown as a static GitHub Pages site
using the reusable renderer maintained by `MicroWebStacks/astro-huge-doc`.

## Inputs

- The render workspace is the repository root.
- `manifest.yaml` sets `render.folder` to `.` so committed Markdown throughout
  the repository can be rendered.
- Git-ignored files are not publication inputs. In particular, `.cache/` is
  absent from a normal GitHub Actions checkout and must never be added to the
  workflow as a separate input.
- The canonical site URL is `https://vectormind.github.io/`, served at the
  domain root with no repository base path.

## Automation contract

- A push to `main` or a manual dispatch starts the Pages workflow.
- The workflow checks out this repository and calls
  `MicroWebStacks/astro-huge-doc@main`.
- The Action receives an exact published `@microwebstacks/md-render` engine
  version even though the Action itself deliberately follows upstream `main`.
- The renderer writes `dist/`; the workflow uploads that directory as a Pages
  artifact and deploys it in a separate job.
- The workflow has only the repository and Pages permissions required to read
  content, upload the artifact, and request a Pages deployment.

## Outputs

- A static Pages artifact containing an `index.html`, `404.html`, route HTML,
  client assets, and content-addressed blobs as required by the selected
  content.
- A deployment associated with the `github-pages` environment.

## Acceptance criteria

1. The published engine exposes `bin/md-render.js` and renders this repository
   successfully with `manifest.yaml`.
2. The generated artifact contains `index.html` and `404.html`.
3. Workflow syntax and referenced Action inputs match the live upstream
   `action.yml` contract.
4. A GitHub Actions run triggered from `main` completes both render and deploy
   jobs, and representative routes and assets load from the canonical URL.


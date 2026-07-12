# Verification record

## 2026-07-12 local consumer proof

1. Queried npm and confirmed `@microwebstacks/md-render@0.0.10` is published.
2. Installed `0.0.10` under the Git-ignored `.tmp/` workspace and confirmed
   `bin/md-render.js` exists and exposes the `build` command.
3. Ran the public command against the repository root with `manifest.yaml`,
   output directory `.tmp/pages-artifact`, and canonical site URL
   `https://vectormind.github.io/`.
4. The first attempt reached Astro but could not write Astro's telemetry file
   outside the workspace sandbox. Re-running with `ASTRO_TELEMETRY_DISABLED=1`
   passed; this was a local sandbox constraint rather than a renderer failure.

## Results

- Collect: 20 Markdown documents, 453 items, 15 assets.
- Static generation: 21 HTML pages.
- Required artifact files: `index.html` present; `404.html` present.
- Client output: 149 files under `_astro/`.
- Content-addressed output: 15 files under `blobs/`.
- Root page contains the expected `VectorMind` heading and root-absolute links
  appropriate for `https://vectormind.github.io/`.

## Pending production proof

Local proof satisfies the renderer and artifact-shape criteria. The workflow
and deployed-site criteria require a maintainer commit/push and a live GitHub
Pages run, so the packet remains open.


# Verification

## Environment

- Python 3.14.0
- Node 22.21.1
- No third-party packages or network access

## Focused tests

`python .cache\src\harborworks-composition\test_composer.py -v`

Result: 6 tests passed.

The tests verify:

- 9 repositories resolve to 81 unique artifact identities;
- 54 skills, 18 knowledge files, and 9 tools remain present in the logical
  catalog despite 5 repeated repository-relative paths;
- `.cache/` is excluded from the exported catalog;
- repository filtering yields 7 repositories and 42 skills;
- artifact filtering yields the 36-skill golden set;
- reversing import order preserves the identity set;
- revision and policy conflicts fail visibly; and
- every shallow skill references its owning knowledge base and CLI.

## Runtime checks

- All nine Python/Node fixture CLIs returned valid context-identifying JSON.
- Naive materialization reduced 81 logical artifacts to 54 files through 27
  overwrites.
- The two order scenarios each returned the same 72 imported artifact
  identities.
- The negative scenarios returned the expected revision and policy errors.

Raw outputs remain ignored under
`.cache/results/harborworks-composition/run-001/`. Compact durable observations
are preserved in
`memory/2026-07/13/harborworks-composition-experiment/run-001.md`.

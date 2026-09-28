# Gatsby V6

Separate task-contract edition at `/gatsby-v6/`. The V5 directory is read-only input and remains published at its existing URL.

## Build and check

```sh
node tools/gatsby_v6/build.mjs
node tools/gatsby_v6/validate.mjs
node tools/gatsby_v6/check_review.mjs
node tools/gatsby_v6/check_assets.mjs
```

The build needs Node, Python's standard CSV parser, and `zip`. Validation uses `unzip`. Browser QA uses the workspace's Playwright installation. Public-link QA uses anonymous HEAD requests through curl; it never writes to S3.

`task-decisions.json` records task-specific scope and factual resolutions. `craft-constraints.json` records additional output-level predicates. `source-text.json` is the read-only source snapshot used to resolve CSV/text selections. Newly supplied production defaults are identified as V6 decisions, not represented as original client instructions.

The build creates an individually compressed task script and a complete task ZIP for each of the 100 tasks. The website decompresses only the selected task using the browser's DecompressionStream API. Task JSON downloads are generated from that same loaded record. ZIP downloads are the portable fallback and include the full task, brief, output register, asset manifest, verifier list, and revision notes. The all-task ZIP contains the full JSON catalog.

## Safeguards

- Hash every V5 file before and after building.
- Do not change original assets, S3 URLs, old task runs, or earlier editions.
- Keep a unique check ID and one registered output ID on each condition.
- Do not convert record metadata such as image filenames or internal reserves into printed-copy requirements.
- Store the exact source file or an explicit named choice set with each output.
- Keep historical runs linked as V5 evidence, never as V6 passes.
- Mark revised tasks and verifiers as unexecuted/unassessed.

The structural and browser reports test contracts, mappings, rendering, downloads and links. They do not certify future creative quality, all Adobe connector operations, or completion of any revised task. Asset availability is distinct from independent visual/identity review.

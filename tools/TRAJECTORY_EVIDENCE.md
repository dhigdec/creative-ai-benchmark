# Trajectory evidence builder

`build_trajectory_evidence.py` turns a step manifest plus real, local per-stage
images into a self-contained trajectory evidence directory. It generates:

- `trajectory.json`, `trajectory.md`, and `trajectory.html`
- `contact-sheet.png` and `contact-sheet.html`
- `decision-evidence.html`
- byte-identical snapshot copies under `intermediate/`

The contact sheet is labeled as a derived visual index. It is never represented
as an Adobe output.

## Required step fields

The manifest may contain `steps` directly or a top-level `tasks` map. Every
selected step must have:

```json
{
  "stage": 0,
  "title": "Source state",
  "action": "source_inspection",
  "parameters": {},
  "snapshot": "previews/PHOTO-04/00-source.jpg",
  "decision": "Why this state matters"
}
```

Connector steps should also include the real `request_id` when one was returned.
`reasoning`, `status`, and an ISO-8601 `timestamp` are optional and are preserved.

The primary `snapshot` is the stage contact sheet or decision card. A step may
also bind the individual images represented by that card:

```json
{
  "stage": 1,
  "title": "Automatic tone",
  "action": "image_apply_auto_tone",
  "snapshot": "cards/01-auto-tone.png",
  "decision": "Use the neutral tone pass as the next collection state.",
  "asset_snapshots": [
    {
      "asset_id": "oliveto-bedroom",
      "name": "Oliveto bedroom after automatic tone",
      "path": "assets/stage-01/oliveto-bedroom.png",
      "input_url": "https://optional-manifest-record/input",
      "output_url": "https://optional-manifest-record/output",
      "request_id": "optional-real-request-id",
      "status": "complete",
      "parameters": {"mode": "auto"}
    }
  ]
}
```

For each `asset_snapshots` item, `asset_id`, `name`, and `path` are required
non-empty strings. `input_url`, `output_url`, `request_id`, and `status` are
optional non-empty strings; `parameters` is an optional JSON object. URLs are
preserved as manifest metadata and are never fetched. `path` must resolve to a
decodable local image below the snapshot root.

In generated `trajectory.json`, each underlying `path` becomes a packaged
reference like
`trajectory/underlying/stage-01-automatic-tone/001-oliveto-bedroom-oliveto-bedroom-after-automatic-tone.png`.
Its `snapshot_evidence` records the original manifest reference, byte count,
SHA-256, dimensions, format, copy integrity, and whether that asset has the same
bytes as its prior recorded state. The HTML trajectory and contact sheet link
thumbnail cards to these byte-identical packaged files.

The builder rejects missing or undecodable images, URLs/data URIs, paths outside
the snapshot root, repeated source paths, and non-increasing stage order. It
records byte size, decoded dimensions, format, and SHA-256 for every snapshot.
Identical bytes from two distinct files are allowed but are explicitly flagged;
a legitimate no-op action can therefore be represented without pretending the
pixels changed.

## Build from the current recapture manifest

From the repository root:

```bash
python3 -B tools/build_trajectory_evidence.py \
  --manifest ../trajectory-recapture/preview-evidence.json \
  --task PHOTO-04 \
  --output-dir ../../outputs/creative-ai-benchmark/SB3-004-PHO/trajectory \
  --replace

python3 -B tools/build_trajectory_evidence.py \
  --manifest ../trajectory-recapture/preview-evidence.json \
  --task PHOTO-13 \
  --output-dir ../../outputs/creative-ai-benchmark/SB3-013-PHO/trajectory \
  --replace
```

Do this only after the manifest points to the approved, actual captures. The
builder verifies file evidence but cannot independently prove that an action,
setting, decision, timestamp, or request ID came from Adobe; those remain
manifest-supplied claims and every generated report states that boundary.

`--replace` overwrites generated paths. It only removes stale files that a prior
builder run listed in `.trajectory-evidence-builder.json`, so the legacy
single-intermediate files required by the current publisher remain untouched.

After replacing a source trajectory, rebuild its delivery ZIP and rerun
`tools/publish_completed_runs.py`. The publisher must copy the three standard
trajectory files plus the `evidence_artifacts` siblings; its current
`trajectory_steps` support publishes the step snapshots in source order.

## Tests

The tests create synthetic images only inside temporary directories:

```bash
python3 -B -m unittest discover -s tools/tests -p 'test_*.py' -v
```

# Where the assets live (AWS S3 and local), as of 2026-10-09

Media (images, PDFs, video, audio) is **not in git**. Git holds manifests with every S3 link and sha256.

## AWS account and access

- Account: `874846752452`, region `ap-south-1` (Mumbai).
- Bucket: **`annotationprod`**.
- Access is via AWS SSO (IAM Identity Center), start URL `https://identitycenter.amazonaws.com/ssoins-6595f2addbd59379`.
- Working profile: **`annotationprod-publish`** (role `annotationprod-s3-access`), set up in `~/.aws/config`:
  ```
  [profile annotationprod-publish]
  sso_session = annotationprod-audit
  sso_account_id = 874846752452
  sso_role_name = annotationprod-s3-access
  region = ap-south-1
  ```
  Log in with `aws sso login --profile annotationprod-publish`, then `export AWS_PROFILE=annotationprod-publish`.
  The `annotationprod-audit` profile (role S3FullAccess) returns "No access" for this user. The default profile has no credentials.
- No keys are stored in this repo. Never commit `~/.aws` contents.

## Current version: V3.1 input assets (used by Gatsby V5, V7 and the annotation pilot)

- **Prefix:** `s3://annotationprod/creative-ai-benchmark/v3.1/tasks/<SB3-code>__<slug>/assets/<file>`
  - Example: `s3://annotationprod/creative-ai-benchmark/v3.1/tasks/SB3-004-PHO__verranza-coastal-retreats-villa-collection-image-system/assets/verranza_pool.jpg`
- **Public HTTPS** (no login, used directly by the pages):
  `https://annotationprod.s3.ap-south-1.amazonaws.com/creative-ai-benchmark/v3.1/tasks/<SB3-code>__<slug>/assets/<file>`
- **Size:** 100 task folders, **2,009 objects, ~5.49 GB** (counted 2026-10-09).
- **Per-file index:** `docs/gatsby-v7/tasks/<ID>/ASSET_MANIFEST.json`. Each entry has `filename`, `asset_id`, `bytes`,
  `width`, `height`, `sha256`, `s3_key`, `s3_uri` and `public_url`. All 2,009 entries point at this prefix.
- The task-ID-to-folder mapping (`PHOTO-04` → `SB3-004-PHO__verranza-...`) is in each manifest's `s3_key`.

## Other prefixes in the same bucket

| Prefix | What it is | Size |
|---|---|---|
| `s3://annotationprod/creativegym/AO-XX_<slug>/` | Old AO-* corpus input assets (pre-V3) | 691 objects, ~2.16 GB |
| `s3://annotationprod/StudioBench_5_Sample_Tasks/` | 5 sample tasks: LAYOUT-01 Kantyna Nova, LAYOUT-03 Lumora Laboratories, MOTION-01 Ember and Oak, PHOTO-13 Argent and Faith, VECTOR-01 Cordwain Overland | 116 objects, ~295 MB |

Other top-level prefixes in `annotationprod` (Core Transcription, Dataset, Languages, Mocap, Multimodal, Script-Uploads,
Video) belong to other Deccan projects. Do not touch them.

## Things that ARE in git (and therefore on GitHub Pages)

- Completed-run deliverables and trajectories for PHOTO-04 and PHOTO-13: `docs/gatsby-v7/runs/<ID>/` (and the same in V5).
  They are force-added past `.gitignore`.
- Pilot PDF previews: `docs/gatsby-v7/annotation-pilot/previews/*.png`.

## Local copies (Dhiren's Mac)

- V3.1 media: `~/Downloads/Deccan/Adobe-Freelance-Leads/input_assets_v3/<ID>/assets/` (gitignored), with
  `asset_plan.json` and `manifest.json` per task tracked on branch `codex/studiobench-v3-audit-rebalance`.
- Old AO-* media: `~/Downloads/Deccan/Adobe-Freelance-Leads/input_assets/AO-XX_<slug>/assets/`. The README says the old
  media was also hosted on GCS; the S3 `creativegym/` prefix is the copy in use.

## Rules

- Never rename or move S3 keys. Pages, manifests and checks reference them by exact path.
- If you replace an asset (e.g. an IP-mark inpaint fix), upload under the same key, then update `sha256`/`bytes` in every
  `ASSET_MANIFEST.json` copy and record the change.
- Uploads need the `annotationprod-publish` SSO login. Reading the public URLs needs nothing.

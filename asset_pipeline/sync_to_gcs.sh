#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Sync StudioBench input assets -> GCS.  ONE bucket, per-task folders.
#   gs://<BUCKET>/AO-XX_slug/assets/...      (mirrored: local deletes propagate)
#   gs://<BUCKET>/AO-XX_slug/manifest.json   (the asset->requirement mapping)
#
# Scope per task = assets/ + manifest.json  (prompts/, originals/, logs, etc. excluded).
# Uses `gsutil -m rsync -d` so the bucket always MIRRORS local (add/change/delete).
#
# Usage:
#   ./sync_to_gcs.sh --dry-run            # show what would change, upload nothing
#   ./sync_to_gcs.sh                      # sync ALL 100 tasks
#   ./sync_to_gcs.sh --task AO-07         # sync one task (used by the pipeline hook)
#   ./sync_to_gcs.sh --dry-run --task AO-07
# Env overrides: BUCKET, PROJECT, REGION.
# ---------------------------------------------------------------------------
set -euo pipefail

PROJECT="${PROJECT:-mlproject-501205}"
BUCKET="${BUCKET:-gs://mlproject-501205-studiobench-assets}"
REGION="${REGION:-us-central1}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/input_assets"

DRY=""; ONLY=""
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY="-n" ;;
    --task) ONLY="${2:?--task needs an AO id}"; shift ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
  shift
done

# --- preflight: auth + bucket ---
if ! gcloud auth application-default print-access-token >/dev/null 2>&1 \
   && ! gsutil ls "$BUCKET" >/dev/null 2>&1; then
  echo "ERROR: GCP auth not ready. Run:" >&2
  echo "  gcloud auth login && gcloud auth application-default login && gcloud config set project $PROJECT" >&2
  exit 1
fi

if ! gsutil ls -b "$BUCKET" >/dev/null 2>&1; then
  if [ -n "$DRY" ]; then
    echo "[dry] would create bucket $BUCKET (region=$REGION, uniform BLA, Standard)"
  else
    echo ">> creating bucket $BUCKET (region=$REGION) ..."
    gcloud storage buckets create "$BUCKET" \
      --project="$PROJECT" --location="$REGION" \
      --uniform-bucket-level-access --default-storage-class=STANDARD
  fi
fi

sync_one() {
  local d="$1" name; name="$(basename "$d")"
  [ -d "${d}assets" ] || { echo "-- skip $name (no assets/)"; return 0; }
  echo "== $name =="
  # assets/: full mirror (add/update/delete)
  gsutil -m rsync $DRY -d -r "${d}assets" "$BUCKET/$name/assets"
  # manifest.json: single-file copy
  if [ -f "${d}manifest.json" ]; then
    if [ -n "$DRY" ]; then
      echo "[dry] would cp ${name}/manifest.json"
    else
      gsutil -q cp "${d}manifest.json" "$BUCKET/$name/manifest.json"
    fi
  fi
}

if [ -n "$ONLY" ]; then
  found=0
  for d in "$SRC/${ONLY}"*/; do [ -d "$d" ] && { sync_one "$d"; found=1; }; done
  [ "$found" = 1 ] || { echo "no task dir matching $ONLY" >&2; exit 1; }
else
  for d in "$SRC"/AO-*/; do [ -d "$d" ] && sync_one "$d"; done
fi
echo "done${DRY:+ (dry-run — nothing uploaded)}."

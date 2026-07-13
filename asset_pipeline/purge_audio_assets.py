#!/usr/bin/env python
"""After the audio de-scope, remove orphaned audio ASSET files + manifest entries. For every task, any audio
asset (kind 'audio', or a folder/file whose name is an audio track/music folder) that the spec no longer lists
as an input is deleted from disk and dropped from the manifest. Run AFTER the specs are reframed & validated.

Run:  .venv/bin/python purge_audio_assets.py [--apply]   (default = dry-run)
"""
from __future__ import annotations
import glob, json, re, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config

APPLY = "--apply" in sys.argv
AUDIO_EXT = {".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg"}
AUDIO_NAME = re.compile(r"music.*folder|royalty_free|voiceover|voice_over|_vo[_.]|scratch.*(vo|voice)|narration", re.I)


def is_audio(name, kind):
    if (kind or "").lower() == "audio":
        return True
    if Path(name).suffix.lower() in AUDIO_EXT:
        return True
    if "." not in name and AUDIO_NAME.search(name):  # folder like royalty_free_music_folder
        return True
    return False


def main():
    specs = {json.load(open(p))["id"]: json.load(open(p))
             for p in glob.glob(str(config.PROJECT_DIR / "complex_benchmark/adobe_only/specs/*.json"))}
    removed_files = 0; removed_entries = 0; touched = []
    for mp in glob.glob(str(config.OUT_ROOT / "AO-*/manifest.json")):
        td = Path(mp).parent
        man = json.load(open(mp)); tid = man.get("task_id") or td.name.split("_")[0]
        spec_inputs = {i.get("name") for i in (specs.get(tid, {}).get("inputs") or [])}
        keep = []
        changed = False
        for a in man.get("assets", []):
            nm = a.get("name", "")
            if is_audio(nm, a.get("kind")) and nm not in spec_inputs:
                changed = True; removed_entries += 1
                # delete file/folder on disk
                for cand in (td / nm, td / "assets" / nm):
                    if cand.exists():
                        print(f"  {tid}: remove {'DIR' if cand.is_dir() else 'file'} {nm}")
                        if APPLY:
                            shutil.rmtree(cand) if cand.is_dir() else cand.unlink()
                        removed_files += 1
                        break
                else:
                    print(f"  {tid}: drop manifest entry (no file) {nm}")
            else:
                keep.append(a)
        if changed:
            touched.append(tid)
            man["assets"] = keep
            if APPLY:
                json.dump(man, open(mp, "w"), indent=2)
    print(f"\n{'APPLIED' if APPLY else 'DRY-RUN'}: {removed_entries} audio manifest entries, {removed_files} files/dirs, "
          f"across {len(touched)} tasks: {sorted(touched, key=lambda t:int(t.split('-')[1]))}")


if __name__ == "__main__":
    main()

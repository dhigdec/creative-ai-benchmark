---
name: reference-html-to-express-font-gotcha
description: export_html_to_express silently flattens all text to 12pt when font stacks use double-quotes inside double-quoted style attributes
metadata: 
  node_type: memory
  type: reference
  originSessionId: d469daaa-e33b-4c81-a609-3bdc7c1f159d
  modified: 2026-09-11T09:44:29.121Z
---

**HTML→Express (`export_html_to_express`) font-size flattening bug.** If any inline `style="..."` attribute contains a font stack with double-quoted CSS names (e.g. `style="font-family:"freight-big-pro",Georgia,serif;font-size:104px"`), the inner double-quote terminates the attribute early, so every property after it (including `font-size`) is dropped and the importer flattens the whole document to 12pt. Fonts still resolve (from CSS classes) so it looks "styled" but all one size.

**Fix:** single-quote the CSS font names inside the double-quoted style attribute: `font-family:'freight-big-pro',Georgia,serif`. In Python f-strings that build the HTML, define the stack as a double-quoted Python string holding single quotes: `D="'freight-big-pro',Georgia,serif"`. A blanket `"name" -> 'name'` sed will corrupt single-quoted Python strings — edit the definitions directly.

**Verify after export:** the returned `slides[].html` HzHTML should show varied `font-size="Npt"` values (a real hierarchy), not every `hz-text` at `12pt`. Large exports exceed the inline token cap and save to a tool-results file; jq it for `scan("font-size=\"([0-9.]+)pt\"")` distinct values.

Rendering previews of a self-contained collateral HTML: Chrome headless (`/Applications/Google Chrome.app/.../Google Chrome --headless=new --screenshot=out.png --window-size=W,H --virtual-time-budget=9000 --user-data-dir=<tmp>`) at each slide's native canvas size; macOS has no `timeout` command, so wrap each render in Python `subprocess.run(timeout=...)` (screenshot writes before `--headless=new` hangs, so a killed process still yields the PNG).

Related: [[reference_adobe_connector_exec_modes]], [[project_studiobench_artifacts]].

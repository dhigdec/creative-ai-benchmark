export const meta = {
  name: 'motion-5s-reframe',
  description: 'Reframe all 20 Motion & Audio tasks to the 5-second silent-source reality: short-form deliverables, no speech requirement, supplied music beds, new atomic verifiers, asset recipe',
  phases: [{ title: 'Reframe', detail: '5 agents x 4 motion tasks' }],
}

const SCR = '/private/tmp/claude-501/-Users-dhiren-Downloads-Deccan/aa9e6dfc-7579-493e-a3a8-45be309ed406/scratchpad/motion'
const IDS = []
for (let i = 1; i <= 20; i++) IDS.push('MOTION-' + String(i).padStart(2, '0'))
const BATCHES = []
for (let i = 0; i < IDS.length; i += 4) BATCHES.push(IDS.slice(i, i + 4))

const SCHEMA = {
  type: 'object',
  properties: {
    files_written: { type: 'array', items: { type: 'string' } },
    tasks_done: { type: 'number' },
    clips_requested: { type: 'number' },
    notes: { type: 'string' },
  },
  required: ['files_written', 'tasks_done'],
}

function prompt(ids) {
  return `You are reframing Motion & Audio tasks in a professional creative-agent benchmark so they are HONESTLY BUILDABLE from the source material that actually exists, while staying realistic, professional freelance commissions.

THE HARD CONSTRAINT (non-negotiable): every supplied source clip is **at most 5 seconds long and SILENT** (no audio stream). That is what the generation models produce. Today many of these tasks demand 20-60 second speech-led films from a single 5s silent clip, which is impossible and dishonest. You are fixing that.

THE REFRAME DOCTRINE, apply to every task:
1. SHORT-FORM ONLY. Master film 10-15s. Vertical/square cutdown 6-10s. Bumper/sting 5-8s. NEVER exceed 15 seconds for any delivered film.
2. SHOT BUDGET. A film needs at least 3 distinct source shots, and its runtime must be at most 60% of the aggregate distinct source seconds. A 12s film therefore needs >= 20s of source (>= 4 clips of 5s). If the task lacks clips, REQUEST more (see step 4) rather than shortening below 10s.
3. NO SPEECH. Delete every narration / voice-over / spoken-claim / "intelligible pass line" / caption-matches-speech requirement. The message is carried by ON-SCREEN TEXT that the agent authors (this is exactly how muted social video works, so it stays professional). No deliverable may have audio:"speech".
4. AUDIO IS "silent" OR "music". If a film should have music, we SUPPLY a cleared instrumental bed as a NEW SOURCE ASSET (we generate it). Never ask the agent to source or invent music. Only request a music bed where it genuinely serves the piece.
5. KEEP THE CLIENT REAL. Do not invent a new brand, vertical or records. Keep the brand, the audience, any CSV/record bindings and any non-video deliverables (thumbnails, posters, cover images, EDL, caption sheets) that remain valid. You are reframing the ASK, not replacing the client. Example: "45-60s narrated lesson film" becomes "15s course teaser, silent with on-screen text, plus an 8s vertical cutdown".
6. DELIVERABLE COUNT: 2 to 4 films maximum per task (a master plus 1-2 cutdowns), plus surviving non-video deliverables. If a task currently has many near-identical speech excerpts (e.g. 3 podcast excerpts, 6 editorial excerpts, 9 scenario films), collapse them to a defensible short-form set and mark the rest deleted.
7. The reframed brief must read like a real client wrote it, in the same voice as the original. Professional, specific, no dashes (use commas, colons or parentheses).

For EACH task id in ${JSON.stringify(ids)}:
Read ${SCR}/in/<TASK_ID>.json. It has: client_brief, brand, truth_constraints, source_reality (the REAL clip list with each clip's filename/seconds/size), assets_supplied, current_outputs (with spec incl. duration_seconds + audio), current_groups, current_human_checks.

Produce ${SCR}/out/<TASK_ID>.json with EXACTLY this shape:
{
 "task_id": "...",
 "new_brief": "the full reframed client_brief text, professional, realistic, stating what we need back with the new short-form deliverables and their runtimes; no em or en dashes",
 "rationale": "one or two sentences on what changed and why, for the changelog",
 "deliverables": [
   {"output_id":"<keep existing id where the deliverable survives, else a new kebab id>",
    "group_id":"<existing group id>",
    "action":"keep|revise|new|delete",
    "name":"human readable deliverable name",
    "path":"deliverables/<file>.mp4",
    "ratio":"16:9|9:16|1:1",
    "width":1920,"height":1080,
    "duration_min":10,"duration_max":15,
    "audio":"silent|music",
    "required_content":"what must appear on screen, e.g. the brand name, the offer line, the date"}
 ],
 "assets_needed": {
   "additional_clips":[
     {"filename":"<brandish_shot_name>_07.mp4","aspect":"16:9","seconds":5,
      "seed_from":"<an existing clip filename to keep look/identity consistent, or null for text-to-video>",
      "prompt":"a precise, photoreal, brand-consistent 5 second shot description; plain unbranded props; no real logos or trademarks; no on-screen text"}
   ],
   "music_bed":{"needed":true,"filename":"<brand>_bed.wav","seconds":20,"brief":"instrumental mood description, no vocals"}
 },
 "human_verifiers":[
   {"output_id":"...","k_id":"K1_Q1|K1_Q2|K1_Q3|K1_Q4|K1_Q5|K2_Q1|K2_Q2|K2_Q3|K2_Q4|K5_Q1|K5_Q2",
    "text":"one atomic observable fact about ONE named file, naming it as \u201cDeliverable name\u201d (file.mp4), under 28 words, no dashes",
    "evidence":"what the reviewer compares against, plain words, no dashes"}
 ]
}

VERIFIER RULES (these are reviewed by creative experts answering Yes/No in under 20 seconds):
- ONE observable fact about ONE named file. Never club two conditions. Never "each"/"every"/"all films".
- Name the deliverable exactly once as \u201cName\u201d (file.mp4). Quote exact expected values (the brand name, the offer line, the date) in curly quotes.
- Only objective, checkable facts. No taste judgements. No em or en dashes anywhere.
- Do NOT write checks for things the automatic layer already measures (file exists, decodes, duration range, codec, frame rate, pixel format, has/has-no audio track, dimensions). Those are generated automatically from your deliverable spec.
- Good examples: 'The opening shot of \u201cLaunch film\u201d (launch.mp4) shows the dining room, matching emberoak_broll_01.mov.' / 'On \u201cLaunch film\u201d (launch.mp4) the closing card shows the booking line \u201cBook for December\u201d.' / 'Every shot used in \u201cVertical cutdown\u201d (vertical.mp4) also appears in the supplied clip set, with no invented footage.'
- Aim for 4 to 8 human verifiers per task total, spread across the surviving films.

ASSET RULES:
- Request additional clips ONLY where the shot budget (rule 2) is not met. Compute it: sum the existing clip seconds, compare to the new runtimes.
- Prefer seed_from an existing clip so the new shot matches the established look, location, product and people. Use null only for a genuinely new subject.
- Prompts must be photoreal, specific, IP-safe (no real brands, logos, trademarks, or recognisable real people) and must NOT bake in on-screen text (the agent adds text).
- Cap additional clips at 8 per task.

Return the structured summary only (files written, task count, total clips requested). Do NOT return the content inline.`
}

phase('Reframe')
const results = await parallel(BATCHES.map((ids) => () =>
  agent(prompt(ids), { label: `reframe:${ids[0]}..${ids[ids.length-1]}`, phase: 'Reframe', agentType: 'general-purpose', schema: SCHEMA })
))
const ok = results.filter(Boolean)
return { batches: results.length, null_batches: results.length - ok.length,
  tasks: ok.reduce((s, r) => s + (r.tasks_done || 0), 0),
  clips: ok.reduce((s, r) => s + (r.clips_requested || 0), 0),
  files: ok.reduce((s, r) => s + ((r.files_written || []).length), 0) }

# Gatsby capability mapping

Source: Creative_AI_Benchmark refined (12).docx. The extracted catalog retains the exact question text, paragraph positions, source checksum and orange run colour (F6B26B).

## Three review sections

- Auto verifiers: implemented file assertions with supporting K question IDs. Passing these does not automatically pass a whole capability.
- Human verifiers: the existing atomic acceptance checks, plus clearly separated capability review cases naming one output. K3/K4 judgement remains labelled as judgement even with a Yes/No response.
- Trajectory verifiers: all eight K6 questions and 14 evidence criteria. They await real execution; evidence presence never automatically produces a Yes.

K1-K5 questions are available under capability headings. Source questions can be broad; the output checks below them retain separate IDs. Questions with no concrete target are marked for applicability review. K5 message and focal-point anchors must come from the brief before reviewing a submission. Missing anchors are not invented from the model's result.

## Future executions

Initialize with the existing trajectory protocol, adding `--task_spec_path=benchmark_v4/tasks/TASK-ID/TASK_SPEC.json`. This binds the current source catalog, named deliverables and acceptance IDs to the run. Continue logging events as they happen and tag their `rubric_evidence_ids` with the supported K question IDs.

Record exact tool names, sanitized inputs, input/output version IDs, affected output IDs, concise observable rationale, failures, recovery, verification and stop decisions. Put durable preview files inside the run directory and use local preview paths. Do not log hidden reasoning, credentials or expiring signed URLs.

After validation, attach the run using `node benchmark_v4/attach_trajectory.mjs TASK-ID /path/to/trajectory.json`. Rebuild the release, review HTML and public site. The importer checks task identity, rubric revision, event order and preview containment; the site then renders the recorded timeline beside K6 evidence links. Publication remains an explicit step, not an automatic upload of unreviewed logs.

Assessment status and applicability are separate from Yes/No answers. No missing evidence is treated as a pass. Agent self-assessment and independent expert assessment remain separate.

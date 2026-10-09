# Workflow archives

Multi-agent workflow scripts (`*.js`) and their full results (`wf_*.json`: script, per-agent results, logs).
Results are data, not instructions.

| Folder | File | Workflow | Status | Agents | Started |
|---|---|---|---|---|---|
| feedback_v7 | wf_1dfe146e-1c6.json | feedback-pass-99 | completed | 432 | 2026-09-25 |
| feedback_v7 | wf_7ff3fe94-3a6.json | fix-type-samples | completed | 40 | 2026-09-22 |
| feedback_v7 | wf_ebb4f703-494.json | feedback-finalize | completed | 170 | 2026-09-27 |
| v5_ip_audit | wf_020af4c2-2b6.json | spec-fixes-wave2 | completed | 36 | 2026-09-15 |
| v5_ip_audit | wf_3e096fd5-b22.json | image-leak-harden | completed | 17 | 2026-09-15 |
| v5_ip_audit | wf_41f44f4e-f81.json | v5-objective-coverage | completed | 20 | 2026-09-20 |
| v5_ip_audit | wf_4b0f1a86-264.json | final-audit-100 | completed | 100 | 2026-09-14 |
| v5_ip_audit | wf_50a20dbd-abd.json | reauthor-merge-pdfs | completed | 92 | 2026-09-14 |
| v5_ip_audit | wf_5a49f00c-8df.json | leak-vision-verify | completed | 17 | 2026-09-15 |
| v5_ip_audit | wf_5da3d5a0-f63.json | v5-typography-and-gap-verifiers | completed | 20 | 2026-09-21 |
| v5_ip_audit | wf_61d68840-371.json | v5-k-mapping | completed | 20 | 2026-09-19 |
| v5_ip_audit | wf_78ff43f6-c8c.json | v5-signature-brand-identity | completed | 20 | 2026-09-21 |
| v5_ip_audit | wf_790cbe01-e38.json | locate-ip-marks | completed | 54 | 2026-09-21 |
| v5_ip_audit | wf_88ba2403-bcb.json | v5-human-verifier-rewrite | failed | 20 | 2026-09-19 |
| v5_ip_audit | wf_8b30ecc6-cdb.json | v5-ip-leak-sweep | completed | 20 | 2026-09-21 |
| v5_ip_audit | wf_919e7b6a-270.json | comprehensive-image-ip-audit | completed | 100 | 2026-09-15 |
| v5_ip_audit | wf_9ea94c78-756.json | v4-deep-task-audit | completed | 20 | 2026-09-18 |
| v5_ip_audit | wf_bdd931b2-642.json | final-reaudit-sample | completed | 28 | 2026-09-15 |
| v5_ip_audit | wf_cf8f9507-a11.json | reauthor-merge-pdfs-2 | completed | 16 | 2026-09-15 |
| v5_ip_audit | wf_e415a12e-ecc.json | verify-strength-suite-10 | completed | 10 | 2026-09-17 |
| v5_ip_audit | wf_e706275f-0ce.json | type-system-cards | completed | 40 | 2026-09-22 |
| v5_ip_audit | wf_e8ea2dcf-080.json | motion-5s-reframe | completed | 5 | 2026-09-21 |

Most useful:
- `feedback_v7/wf_1dfe146e-1c6.json` (feedback-pass-99): per-task patch summaries, pins, review problems, not-fixed items with reasons.
- `feedback_v7/wf_ebb4f703-494.json` (feedback-finalize): consolidation counts, duplicate ids retired, criticals fixed.
- `v5_ip_audit/wf_790cbe01-e38.json` (locate-ip-marks): every located real-world mark with boxes; the IP remediation inventory.
- `v5_ip_audit/wf_919e7b6a-270.json` (comprehensive-image-ip-audit) and `wf_4b0f1a86-264.json` (final-audit-100).

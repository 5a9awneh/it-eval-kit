---
agent: agent
description: "Prompt 0 — Orchestrator: Full guided report update. Start here to plan and sequence all other prompts."
---

# Prompt 0 — Orchestrator

Read `.github/copilot-instructions.md` first for project context and your personal details.

## Step 1 — Supervisor Mode

Ask the user:

> **"Will you be filling your own assessment sections only (recommended default), or also drafting the supervisor/manager sections on their behalf?"**
>
> `[1] Staff fields only` ← default — supervisor sections left as placeholders
> `[2] Full document` — you draft supervisor sections in third-person manager voice

Set `SUPERVISOR_MODE` for this session:
- Option 1 → `SUPERVISOR_MODE: staff_only`
- Option 2 → `SUPERVISOR_MODE: full`

All downstream prompts (4 and 5) will respect this setting.

## Step 2 — Scope Assessment

Ask the user (or infer from context):
1. Is there a new ticket CSV export in `Evidence/tickets/`? If yes, what is the filename?
2. Are there new email threads in `Evidence/email-evidence/` since the last report run?
3. What is the reporting period end date?

## Step 3 — Execution Order

Run the following prompts in sequence, skipping any that are not needed based on Step 2:

1. **If new CSV:** Run Prompt 1 — Ticket Data Analysis
2. **If new email evidence or new projects:** Run Prompt 3 — Achievements & Contributions
3. **Always if anything changed:** Run Prompt 2 — Performance Analysis
4. **Always if anything changed:** Run Prompt 4 — Performance Review
5. **If annual report is due:** Run Prompt 5 — Annual Report (after Prompts 2 & 3)

## Step 4 — Final Checks

After all prompts complete:
- Confirm all character counts are within limits defined in `Reference/performance-review-template.txt`
- Remind user to commit all changed files
- Remind user that `Evidence/` and `Tools/ticket_stats.txt` are git-ignored and stay local only

## Notes
- Never carry forward numbers from old reports — `Tools/ticket_stats.txt` is always the source of truth
- If only one document needs updating, run that prompt directly — no need for the orchestrator

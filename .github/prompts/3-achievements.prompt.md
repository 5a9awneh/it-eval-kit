---
agent: agent
description: "Prompt 3 — Achievements & Contributions: Update Reports/Achievements & Contributions.md with new projects, initiatives, and updated stats."
---

# Prompt 3 — Achievements & Contributions

Read `.github/copilot-instructions.md` for project context. Ensure `Tools/ticket_stats.txt` is up to date if available.

## Task

Update `Reports/Achievements & Contributions.md` — a comprehensive career reference document covering the full tenure.

## Steps

1. **Read `Tools/ticket_stats.txt`** — extract all current metrics. If this file does not exist, skip the metrics table and note it as unavailable; proceed with email evidence only — all project and achievement sections remain fully populated.

2. **Audit new evidence** — read email threads in:
   - `Evidence/email-evidence/projects-initiatives/` — project and initiative updates
   - `Evidence/email-evidence/events-meetings/` — high-level or after-hours event support
   - `Evidence/email-evidence/learning-certs/` — training and certifications completed

   For each new thread, identify:
   - Is it a new project/initiative not yet in the document?
   - Does it update or expand an existing section?
   - Is there a named acknowledgment or commendation from a stakeholder?

3. **Update the document section by section:**
   - **Executive summary / metrics table:** Refresh all values from `ticket_stats.txt`
   - **Core service delivery section:** Update ticket count, resolution rate, and the two configured notable operation metrics (as labelled in `ticket_stats.txt`)
   - **Project/initiative sections:** Add new items to the most relevant section. Do not remove existing content unless it is factually incorrect.
   - Preserve all existing sections, structure, and collaborator attributions

4. **For each new item added**, include:
   - What was done (technical detail)
   - Why it mattered (organizational impact)
   - Any named acknowledgments from stakeholders
   - Collaborators and date/period

## Style Rules
- Third person, professional career-reference tone ("{YOUR_NAME} developed...", "{YOUR_NAME} deployed...")
- Comprehensive — err on the side of inclusion; this is a reference document, not a summary
- Do not truncate existing content to make room for new additions
- Preserve all collaborator attributions on each project entry

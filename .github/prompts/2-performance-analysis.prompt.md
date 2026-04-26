---
agent: agent
description: "Prompt 2 — Performance Analysis: Update Reports/Performance Analysis.md with the latest ticket stats and notable projects."
---

# Prompt 2 — Performance Analysis

Read `.github/copilot-instructions.md` for project context. Ensure Prompt 1 has been run and `Tools/ticket_stats.txt` is up to date.

## Task

Update `Reports/Performance Analysis.md` to reflect the latest data.

## Steps

1. **Read `Tools/ticket_stats.txt`** — extract all current metrics

2. **Audit `Evidence/email-evidence/projects-initiatives/`** for threads added since the previous reporting period end date. Identify any new projects or initiatives not yet reflected in the document.

3. **Update the document:**

   - **Header / period dates:** Update to the current reporting period
   - **Executive summary / KPI table:** Refresh all metrics from `ticket_stats.txt`
   - **Primary achievements:** Update ticket count, resolution rate, the two configured notable operation metrics (as labelled in `ticket_stats.txt`), unique users
   - **Monthly trend table:** Add new months; update any partial months
   - **Quarterly breakdown:** Add new quarters
   - **Notable projects table:** Add new projects from the evidence audit. Use format: `| Project Name | Period | Impact summary |`

4. **Do not add delta/comparison columns** — this document is always a full-tenure snapshot, not a period-over-period comparison

## Style Rules
- Neutral, analytical, third-person tone
- All numbers from `ticket_stats.txt` only — never estimate or carry forward
- Include the disclaimer: *"Category distribution is derived from subject-line keyword analysis. The CSV's own category field is not used."*

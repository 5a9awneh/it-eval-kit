---
agent: agent
description: "Prompt 5 — Annual Report: Generate or update Reports/Annual Report.md for annual submission."
---

# Prompt 5 — Annual Report

Read `.github/copilot-instructions.md` for project context and `SUPERVISOR_MODE` setting. Prompts 2 and 3 should be complete before running this.

> **Reporting Period:** _(specify, e.g. 01 January 2025 – 31 December 2025, or leave blank for full tenure)_

## Task

Generate or update `Reports/Annual Report.md` — the annual performance and contribution report.

## Source Material

- `Tools/ticket_stats.txt` — all quantitative data *(optional — if absent, omit quantitative metrics sections and insert: "No ticket data available for this reporting period.")*
- `Reports/Performance Analysis.md` — KPIs, category breakdown, notable projects
- `Reports/Achievements & Contributions.md` — innovations, projects, certifications
- `Reports/Performance Review.md` — ratings and supervisor assessment (for supervisor section)
- `Evidence/email-evidence/learning-certs/` — certifications and training completions
- `Evidence/email-evidence/events-meetings/` — after-hours and extended support events
- `Reference/performance-review-template.txt` — for any fields or structure carried into the annual report

## Template Adaptation

If your organization has a specific annual report format or template, place it in `Reference/` and reference it here. Otherwise, structure the report around these standard sections:

1. **Assignment overview** — role, period, organization, reporting manager
2. **Key results & achievements** — quantitative metrics + top 3–5 highlights
3. **Projects & initiatives** — notable contributions beyond core duties
4. **Learning & professional development** — certifications, training, skills gained
5. **Extended / emergency support** — after-hours, high-priority events
6. **Impact summary** — broader organizational or stakeholder impact
7. **Supervisor assessment** ← supervisor mode applies here (see below)
8. **Additional comments** — personal reflection, goals for next period

## Voice & Supervisor Mode

Check `SUPERVISOR_MODE` from the orchestrator (or ask if running directly):

### `SUPERVISOR_MODE: staff_only` (default)
- All self-assessment sections → first person
- Section 7 (supervisor assessment) → insert placeholder:
  ```
  > [To be completed by {YOUR_SUPERVISOR_NAME}]
  ```

### `SUPERVISOR_MODE: full`
- Self-assessment sections → first person
- Section 7 → third-person manager voice, drawing from `Reports/Performance Review.md` supervisor content. Adapt, do not copy verbatim.

## Scope Handling

- If a **full-tenure** report: pull all stats from `ticket_stats.txt` as-is
- If a **single-year** report: filter monthly data to the specified year; note the annual subset vs. full-tenure totals where relevant

## After Completing

- Update the report period dates in the header
- Confirm the certifications/training list is complete against `Evidence/email-evidence/learning-certs/`
- Archive the previous year's report as `Annual Report - {YEAR}.md` before overwriting

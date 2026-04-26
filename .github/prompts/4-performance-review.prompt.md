---
agent: agent
description: "Prompt 4 — Performance Review: Update Reports/Performance Review.md using the latest Performance Analysis and Achievements as source material."
---

# Prompt 4 — Performance Review

Read `.github/copilot-instructions.md` for project context and `SUPERVISOR_MODE` setting. Prompts 2 and 3 should be complete before running this.

## Task

Update `Reports/Performance Review.md` — the formal performance appraisal document.

## Source Material

- `Reports/Performance Analysis.md` — KPIs and notable projects
- `Reports/Achievements & Contributions.md` — specific achievements and contributions
- `Tools/ticket_stats.txt` — raw numbers
- `Reference/performance-review-template.txt` — **your org's appraisal form** (read this first to understand the required sections, fields, and any character limits)
- `Reference/sample-completed-review.md` *(if present)* — use as a tone, style, and format reference

## Template Adaptation

**Read `Reference/performance-review-template.txt` before writing anything.** The structure, section names, field labels, and character limits in your org's template take full precedence over any generic assumptions. Adapt the output to match exactly what the template requires.

If a character limit is specified for a section, add a note after each section:
> *Limit: X characters. Current: Y characters.*

## Voice & Supervisor Mode

Check `SUPERVISOR_MODE` set in the orchestrator (or ask the user if running this prompt directly):

### `SUPERVISOR_MODE: staff_only` (default)
- Write all **self-assessment sections** in first person: "I developed...", "I supported..."
- For **supervisor/manager assessment sections**, insert a clearly labelled placeholder:
  ```
  > [To be completed by {YOUR_SUPERVISOR_NAME}]
  ```
  Do not draft content for supervisor sections.

### `SUPERVISOR_MODE: full`
- Write all **self-assessment sections** in first person (same as above)
- Write **supervisor/manager sections** in third-person manager voice: "{YOUR_NAME} demonstrated...", "Mr./Ms. {Surname}..."
- Draw from `Reports/Achievements & Contributions.md` and `Reports/Performance Analysis.md` for substance
- Do not simply repeat the self-assessment — focus on observed impact and professional competency from a manager's perspective

## After Updating

- Verify character counts for every section that has a limit
- Confirm all mandatory fields in the template are filled
- Review that quantitative claims match `Tools/ticket_stats.txt`

# Annual Report

> **Employee:** {YOUR NAME}
> **Title:** {YOUR TITLE}
> **Organization:** {YOUR ORGANIZATION — DEPARTMENT}
> **Supervisor:** {YOUR SUPERVISOR NAME}
> **Reporting period:** {YEAR, e.g. 01 January 2025 – 31 December 2025}

---

> ⚠ **Template note:** This stub does not pre-define sections because your organization's annual report or performance form structure takes precedence.
>
> If your organization has a specific annual submission format, place it in `Reference/` and reference it in Prompt 5 before running.
>
> Run **Prompt 5 — Annual Report** to generate a complete report adapted to your template (or the generic 8-section structure defined in Prompt 5 if no template is provided).

---

## Archive convention

When a new annual report is generated, archive the previous year's version as:

```
Reports/Annual Report - {YEAR}.md
```

before overwriting this file.

---

## Notes for the AI

*(Leave these notes in place — Prompt 5 reads this stub before generating content.)*

- Source stats: `Tools/ticket_stats.txt`
- Source narrative: `Reports/Performance Analysis.md`, `Reports/Achievements & Contributions.md`
- Source review: `Reports/Performance Review.md`
- Voice: self-assessment → first person; supervisor section → depends on `SUPERVISOR_MODE`
- Scope: filter to the reporting period year if generating a single-year report; compare to full-tenure totals where relevant

---
applyTo: "**"
---

# it-eval-kit

## Your Details

Fill in the placeholders below before your first session. These values are referenced by all prompts.

**Name:** {YOUR_NAME}
**Title:** {YOUR_TITLE}
**Organization:** {YOUR_ORGANIZATION — DEPT}
**Grade / Level / Contract type:** {GRADE/LEVEL/CONTRACT}
**Assignment period:** {START_DATE} – {END_DATE or "ongoing"}
**Supervisor:** {YOUR_SUPERVISOR_NAME}

---

## Repository Structure

```
Evidence/               ← Your source data (git-ignored — never committed)
    sample/             ← Synthetic demo data (committed; safe)
    tickets/            ← ITSM CSV exports
    email-evidence/     ← Outlook-exported email threads
      projects-initiatives/
      events-meetings/
      learning-certs/

Tools/
    analyze_tickets.py  ← Run first when you have a new CSV export
    config.json         ← ITSM column mapping, categories, date format
    ticket_stats.txt    ← Output of analyze_tickets.py (git-ignored)
    ExportEachConversationToTxt.bas  ← Outlook VBA macro for email export

Reports/                ← Generated output documents (update these)
    Performance Analysis.md
    Achievements & Contributions.md
    Performance Review.md
    Annual Report.md

Reference/              ← Your org-specific inputs (you provide these)
    role-description.txt            ← Your job description / terms of reference
    performance-review-template.txt ← Your org's appraisal form (plain text)
    sample-completed-review.md      ← (Optional) A previous filled review for tone/style reference
```

---

## Key Conventions

### Ticket Classification
- Classification is based **entirely on ticket Subject/Title keywords** at runtime — `analyze_tickets.py` does not use the CSV's own `Category`/`Group` field
- The CSV category field *can* be used when first setting up the tool via `setup.prompt.md` (Branch A) to bootstrap keyword patterns — but it is never read by the analysis script itself
- All classification logic lives in `Tools/config.json` — edit `categories` there to add/remove/adjust

### Report Voice
Default (staff fields only — `SUPERVISOR_MODE: staff_only`):
- **Performance Review self-assessment sections** → first person ("I developed...", "I supported...")
- **Supervisor/manager sections** → left as instructional placeholders for your supervisor to complete

Full mode (`SUPERVISOR_MODE: full` — only when explicitly requested):
- **Supervisor/manager sections** → third-person, supervisor voice ("[Name] demonstrated...", "Mr./Ms. [Surname]...")

### Numbers & Dates
- All statistics must come from `Tools/ticket_stats.txt` — never from old reports or estimates
- Dates: use whatever format your org's template expects

### Performance Review Template Adaptation
- Prompts 4 and 5 read `Reference/performance-review-template.txt` to understand your org's structure, fields, and character limits
- If you place a `Reference/sample-completed-review.md`, prompts will match its tone and style
- The AI adapts to your template — you are not locked into any fixed structure

---

## Workflow

> **First time?** Run `setup.prompt.md` before anything else — it reads your CSV and auto-configures `Tools/config.json` for your ITSM system and role.

Run these prompts in order when updating your reports:

| Step | Prompt | When to run |
|---|---|---|
| 0 | `0-orchestrator` | Start here — sets supervisor mode and execution plan |
| 1 | `1-analyze-tickets` | New CSV export available |
| 2 | `2-performance-analysis` | After step 1, or new email evidence |
| 3 | `3-achievements` | After new email evidence |
| 4 | `4-performance-review` | After steps 2 & 3 — formal appraisal |
| 5 | `5-annual-report` | Once per year — annual reporting |

Run individual prompts directly if only one document needs updating.

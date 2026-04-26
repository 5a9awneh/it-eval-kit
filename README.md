# it-eval-kit

A config-driven toolkit for IT service desk professionals to turn raw ticket data and email evidence into polished performance reports — using AI chat (VS Code + GitHub Copilot or similar).

---

## ✨ What it does

1. 🎯 **Classifies and analyses** your ITSM ticket export — resolution rates, category breakdown, deployment counts, peak periods
2. 📧 **Audits your email evidence** — project threads, event support, certifications
3. 📝 **Generates and updates** four report types via structured AI prompts: Performance Analysis, Achievements & Contributions, Performance Review, and Annual Report

All classification logic and ITSM field mappings live in a single `config.json` file — no code changes required to adapt to your organization's system.

---

## 🔄 Pipeline

```
┌─────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────┐
│  ITSM ticket export │───▶│  analyze_tickets.py      │───▶│  ticket_stats.txt    │
│  (CSV)              │    │  (config-driven)         │    │  (source of truth)   │
└─────────────────────┘    └──────────────────────────┘    └──────────┬───────────┘
                                                                       │
┌─────────────────────┐                                               ▼
│  Email evidence     │───▶  AI chat prompts (0–5)  ──────▶  Reports/
│  (txt threads)      │      .github/prompts/                Performance Analysis.md
└─────────────────────┘      reads workspace files            Achievements & Contributions.md
                                                              Performance Review.md
                                                              Annual Report.md
```

---

## 🛠️ Prerequisites

- 🐍 Python 3.8 or later
- 💻 [VS Code](https://code.visualstudio.com/) with [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat) (or any AI chat tool that can read workspace files)
- 📤 A ticket export from your ITSM system (ManageEngine, Jira, ServiceNow, or any CSV-based export)

---

## 📋 What Your CSV Needs to Contain

Your ITSM ticket export needs at least these columns (exact names don't matter — you'll map them in `config.json`):

| Field | Required | Purpose |
|---|---|---|
| Subject / Title | Yes | Ticket description — used for keyword classification |
| Status | Yes | Closed / Resolved / Canceled / Open |
| Requester / Caller | Yes | For unique user count |
| Created date | Yes | For time calculations and monthly breakdown |
| Resolved date | Yes | For resolution time; blank = still open |
| Category / Subcategory | Recommended | If your ITSM assigns these reliably, include them — the setup prompt can use them to build your `categories` config automatically |

> 💡 **Before exporting:** If your ITSM has a Category or Subcategory field and the values are accurate and consistently applied, select those columns in your export. The `setup.prompt.md` will detect them and use them to build your classification config — no manual keyword writing needed. If those fields are absent or inconsistently filled, the setup prompt will infer categories from ticket subjects instead.

---

## ⚡ Quick Start (with sample data)

```bash
# Clone the repo
git clone https://github.com/5a9awneh/it-eval-kit.git
cd it-eval-kit

# Run the sample data through the analyser
python Tools/analyze_tickets.py Evidence/sample/sample_tickets.csv
```

Output is written to `Tools/ticket_stats.txt`. Compare against `Evidence/sample/sample_ticket_stats.txt` to verify everything is working.

---

## 🚀 Setting Up for Your Data

### Step 1 — Configure for your ITSM system

> 💡 **Shortcut:** Run `setup.prompt.md` in Copilot Agent chat — it reads your CSV directly and writes `Tools/config.json` for you. The steps below document what it does if you prefer to configure manually.

Open `Tools/config.json` and update:

| Setting | What to change |
|---|---|
| `csv_columns` | Column indices for subject, status, requester, created, resolved in your CSV (0-indexed) |
| `csv_header_rows` | Number of non-data rows at the top of your export file |
| `date_format` | Date format in your created/resolved columns (e.g. `%m/%d/%Y %I:%M %p`) |
| `status_resolved`, `status_cancelled` | Exact status label strings used by your ITSM for closed/resolved and canceled tickets |
| `categories` | Keyword patterns for each ticket category — add, remove, or rename to match your environment |

The sample config ships with ManageEngine SDP defaults. Run with `--verbose` to see per-ticket classification and tune patterns as needed.

**Common ITSM column mappings** (0-indexed; these are typical defaults — verify against your own export's header row):

| ITSM Tool | subject | status | requester | created | resolved | header_rows |
|---|---|---|---|---|---|---|
| ManageEngine SDP | 1 | 2 | 3 | 6 | 7 | 4 |
| Jira Service Management | 1 | 2 | 4 | 6 | 7 | 0 |
| Freshdesk | 1 | 3 | 4 | 5 | 6 | 0 |
| ServiceNow | 2 | 3 | 5 | 6 | 7 | 0 |

> These are representative starting points. Always open your CSV and count columns from 0 to confirm before running.

### Step 2 — Place your Reference files

Add these files to `Reference/` (they are git-ignored — they stay local only):

| File | Purpose |
|---|---|
| `role-description.txt` | Your job description or terms of reference |
| `performance-review-template.txt` | Your org's appraisal form, pasted as plain text |
| `sample-completed-review.md` | (Optional) A previous review as a tone reference |

See `Reference/README.md` for details.

### Step 3 — Personalise the AI instructions

Open `.github/copilot-instructions.md` and fill in the placeholders:
- `{YOUR_NAME}`, `{YOUR_TITLE}`, `{YOUR_ORGANIZATION — DEPT}`, `{YOUR_SUPERVISOR_NAME}`, `{GRADE/LEVEL/CONTRACT}`

### Step 4 — Organise your evidence

Place files in `Evidence/` (git-ignored — local only):

```
Evidence/
  tickets/                     ← ITSM CSV exports
  email-evidence/
    projects-initiatives/      ← One .txt file per project email thread
    events-meetings/           ← Event and after-hours support threads
    learning-certs/            ← Certificates and training completions
```

For email evidence, export conversations from your email client as plain text (one file per thread). The `ExportEachConversationToTxt.bas` file in `Tools/` is an Outlook VBA macro that does this automatically.

💡 **Pre-filter tip:** Before exporting, filter your inbox by sender or subject to isolate relevant threads. Exporting your full inbox is neither necessary nor recommended.

---

## ▶️ Running the Analysis

```bash
# Basic run
python Tools/analyze_tickets.py Evidence/tickets/your-export.csv

# With per-ticket classification debug output
python Tools/analyze_tickets.py Evidence/tickets/your-export.csv --verbose

# Custom config file
python Tools/analyze_tickets.py Evidence/tickets/your-export.csv --config path/to/config.json
```

Output: `Tools/ticket_stats.txt` — this is the source of truth for all report numbers.

---

## 📊 Generating Reports

Open VS Code and start a Copilot Agent chat. To run a prompt, use any of these methods:

- **Slash command** — type `/` in the chat input → select the prompt by name from the dropdown
- **Run button** — open the `.prompt.md` file in the editor → click the ▶ **Run Prompt** button in the top-right toolbar
- **File reference** — type `#` in the chat input, select the prompt file, then send

**First-time setup** (run once when you first clone the repo or switch to a new ITSM system):

| Prompt | Purpose |
|---|---|
| `setup.prompt.md` | Reads your CSV, auto-configures `Tools/config.json` — column mapping, date format, status values, and categories |

**Ongoing workflow** — use these prompts in order whenever you update your data:

| Step | Prompt | When to use |
|---|---|---|
| 0 | `0-orchestrator.prompt.md` | Full guided update — start here |
| 1 | `1-analyze-tickets.prompt.md` | After placing a new ticket CSV |
| 2 | `2-performance-analysis.prompt.md` | After Prompt 1; updates KPI and project tables |
| 3 | `3-achievements.prompt.md` | After adding new email evidence |
| 4 | `4-performance-review.prompt.md` | After Prompts 2 & 3; adapts to your appraisal template |
| 5 | `5-annual-report.prompt.md` | Annual submission; after Prompts 2 & 3 |

### Supervisor mode

Prompts 4 and 5 support two modes:
- ✏️ **Staff-only** (default) — supervisor/manager sections are left as instructional placeholders
- 👔 **Full** — supervisor sections are drafted in third-person manager voice, which you can hand to your manager for review and sign-off

The orchestrator (Prompt 0) asks you which mode to use at the start of each session.

---

## 📁 Folder Structure

```
.github/
  copilot-instructions.md      ← Fill this in with your details
  prompts/
    setup.prompt.md              ← Run once: auto-configures config.json from your CSV
    0-orchestrator.prompt.md
    1-analyze-tickets.prompt.md
    2-performance-analysis.prompt.md
    3-achievements.prompt.md
    4-performance-review.prompt.md
    5-annual-report.prompt.md

Evidence/                      ← git-ignored; your local data
  README.md
  sample/                      ← committed sample data for quick-start testing

Reference/                     ← git-ignored; your org's templates
  README.md

Reports/                       ← Output documents (committed)
  Performance Analysis.md
  Achievements & Contributions.md
  Performance Review.md
  Annual Report.md

Tools/
  analyze_tickets.py
  config.json
  ticket_stats.txt             ← git-ignored; regenerated each run
  ExportEachConversationToTxt.bas   ← Outlook VBA macro for email export
```

---

## 📄 License

MIT — see `LICENSE`.

---
agent: agent
description: "First-time setup: reads your ITSM CSV export and auto-configures Tools/config.json — column mapping, date format, status values, and categories. Run once when you first clone the repo or switch ITSM systems."
---

# Setup — Auto-configure from your CSV

This is a one-time prompt. It reads your ticket export CSV and writes a fully configured `Tools/config.json` tailored to your ITSM system. Run it before using any of the numbered prompts.

---

## Step 1 — Locate the CSV

Ask the user:
> "What is the path to your ITSM ticket export CSV? (e.g. `Evidence/tickets/my-export.csv`)"

Read the file. If it cannot be read, stop and report the error.

---

## Step 2 — Detect structure

Inspect the raw file content (do not parse as CSV yet):

1. **Count preamble rows** — read lines from the top until you find a row that looks like a column header (contains multiple comma-separated text labels, not report metadata). The number of lines before that row is `csv_header_rows`. If the file starts directly with a header, `csv_header_rows` is 0.

2. **Read the header row** — identify column names and their 0-based indices. Report them to the user as a table:
   ```
   Index | Column name
   0     | ...
   1     | ...
   ```

3. **Map required columns** — match header names (case-insensitive, partial match acceptable) to these fields:

   | Config key | Look for header containing… |
   |---|---|
   | `subject` | "subject", "title", "summary", "description" |
   | `status` | "status", "state" |
   | `requester` | "requester", "caller", "customer", "user", "reporter" |
   | `created` | "created", "opened", "logged", "submitted", "raised" |
   | `resolved` | "resolved", "closed", "completed", "finished" |

   If a match is ambiguous or not found, ask the user to confirm the correct column index before proceeding.

4. **Check for Category columns** — look for headers containing "category", "subcategory", "type", "group", "classification". Note the indices and names of any matches — you will use them in Step 4.

---

## Step 3 — Infer date format and status values

Parse 5–10 data rows (skip preamble + header):

1. **Date format** — sample values from the `created` and `resolved` columns. Determine the Python `strptime` format string. Common patterns:
   - `%m/%d/%Y %H:%M:%S` — US datetime with 24h time
   - `%d/%m/%Y %H:%M:%S` — EU datetime
   - `%Y-%m-%d %H:%M:%S` — ISO 8601
   - `%m/%d/%Y %I:%M %p` — US with AM/PM
   - `%d/%m/%Y` — date only
   If the format is uncertain, show the user a sample value and ask them to confirm.

2. **Status values** — extract all unique values from the `status` column across the entire dataset. Present them to the user:
   ```
   Unique status values found:
   - Closed (n tickets)
   - Open (n tickets)
   - Cancelled (n tickets)
   - ...
   ```
   Ask: *"Which of these mean the ticket is fully resolved/closed? Which mean it was cancelled or abandoned?"*
   Record the confirmed values as `status_resolved` and `status_cancelled` lists.

---

## Step 4 — Build categories

Ask the user:

> "Does your CSV have a Category or Subcategory column with accurate, consistently applied values?"

**Branch A — Category column is available and reliable:**

1. Read all unique values from the category column(s) across the full dataset.
2. Show the user a frequency table:
   ```
   Category value          | Count
   Hardware                | 142
   Software                | 98
   ...
   ```
3. Ask: *"Are there any you want to rename, merge, or exclude?"* Apply their instructions.
4. For each final category name, derive keyword patterns from the category label itself (e.g. "Hardware" → `\\bhardware\\b`). The script will match on ticket subjects, so also include common synonyms if obvious (e.g. "Network" → `\\bnetwork\\b`, `\\bwi-?fi\\b`, `\\bconnect`).
5. Present the proposed category list with patterns for user approval before writing.

**Branch B — Category column absent or unreliable:**

1. Read all values from the `subject`/`title` column across the full dataset.
2. Cluster subjects into topic groups by scanning for recurring keywords and phrases. Aim for 6–12 categories — enough to be meaningful, not so many they overlap.
3. Present proposed categories with example ticket subjects for each:
   ```
   Proposed category: "Account/Access"
   Examples:
     - "Password reset for John"
     - "Cannot log in after MFA change"
     - "Account locked — please unlock"
   Keyword patterns: \baccount\b, \bpassword\b, \bmfa\b, \bsign.?in\b, \blogin\b, \block
   ```
4. For each proposed category, ask the user to confirm, rename, merge, or reject.
5. Ask if they want to add any categories you didn't propose.
6. Finalise the approved list with patterns.

**Pattern rules (apply to both branches):**
- Use `\b` word-boundary anchors around whole words
- Use partial matches (no closing `\b`) for prefixes: `\bencrypt`, `\bvulnerabilit`
- Patterns are case-insensitive at runtime — write lowercase
- More specific categories must come before broader ones in the output (first match wins)
- Common ordering: OS/Reformat → Security → Account/Access → Email → Printer → Network → Setup/Config → Software → Hardware

---

## Step 4b — Infer notable operation types from subjects

Using the full subject column already read in Step 4, identify the two most operationally distinct or high-effort ticket clusters — without asking the user anything yet.

**How to identify candidates:**
- Look for subjects containing action verbs or operation nouns that imply significant effort or a distinct workflow: words like *provision, deploy, setup new, configure new, reformat, reimage, reinstall, migrate, build, install OS, new laptop, new device, new server, new VM*, etc.
- Count how many resolved tickets match each cluster
- Prefer clusters that are mutually exclusive and collectively represent notable volume or effort
- Aim for exactly 2; if fewer than 2 meaningful clusters exist, propose only what is genuinely present

**For each candidate, auto-generate:**
1. A plain-English label derived from the dominant terminology in that cluster (e.g. subjects full of "new laptop / provision / setup new" → label: "New device provisioning")
2. 3–6 regex patterns using `\b` word-boundary anchors, broad enough to catch variations seen in the data
3. Any obvious exclusion patterns if false positives are apparent from the subjects (e.g. "excel.*format" to exclude formatting questions from a reformat cluster)

**Present proposals to the user — confirm only:**

> "Based on your ticket subjects, I identified these two high-effort operation types:
>
> **Metric 1 — [proposed label]** (N matching resolved tickets)
> Patterns: `pattern1`, `pattern2`, ...
>
> **Metric 2 — [proposed label]** (N matching resolved tickets)
> Patterns: `pattern1`, `pattern2`, ...
>
> Reply with one of:
> - `yes` — accept both as-is
> - `rename 1: [new label]` and/or `rename 2: [new label]` — keep patterns, change label
> - `skip 1` or `skip 2` — omit that metric (patterns will be empty, stat shows 0)
> - Any freeform correction — describe what to change"

Apply the user's response, then assign:
- Metric 1 → `deploy_label` + `deploy_patterns`
- Metric 2 → `reformat_label` + `reformat_patterns` + `reformat_exclusions`

---

## Step 5 — Write config.json

Construct the complete replacement `Tools/config.json`. Show the user the full proposed JSON before writing:

```json
{
    "_comment": "Auto-configured by setup.prompt.md on <date>. Override any value as needed. Pattern keys are role-specific — adapt to your actual work type.",
    "csv_columns": {
        "_comment": "Zero-based column indices from your CSV header row.",
        "subject": <index>,
        "status": <index>,
        "requester": <index>,
        "created": <index>,
        "resolved": <index>
    },
    "csv_header_rows": <n>,
    "_csv_header_rows_comment": "Rows to skip before the column header row.",
    "date_format": "<format>",
    "_date_format_comment": "Python strptime format string.",
    "status_resolved": [<values>],
    "status_cancelled": [<values>],
    "_status_comment": "Case-sensitive. Must exactly match your ITSM's status labels.",
    "output_path": "Tools/ticket_stats.txt",
    "deploy_label": "<Operation 1 name, e.g. 'New system deployments'>",
    "_deploy_label_comment": "Label shown in the stats report for metric 1.",
    "reformat_label": "<Operation 2 name, e.g. 'OS reformat operations'>",
    "_reformat_label_comment": "Label shown in the stats report for metric 2.",
    "deploy_patterns": ["<pattern1>", "<pattern2>"],
    "_deploy_patterns_comment": "Subject-keyword patterns identifying operation type 1 (resolved tickets only).",
    "reformat_patterns": ["<pattern1>", "<pattern2>"],
    "_reformat_patterns_comment": "Subject-keyword patterns identifying operation type 2 (resolved tickets only).",
    "reformat_exclusions": ["<exclusion1>"],
    "_reformat_exclusions_comment": "Patterns that disqualify a match from reformat_patterns (false-positive suppression).",
    "categories": {
        "_comment": "First matching category wins. More specific patterns before broad ones.",
        "<Category Name>": ["<pattern1>", "<pattern2>"],
        ...
    }
}
```

Ask: *"Does this look correct? Type 'yes' to write it to `Tools/config.json`, or tell me what to change."*

On confirmation, write the file.

---

## Step 6 — Verify

Run the analysis script on the user's CSV to confirm the config works:

```
python Tools/analyze_tickets.py <csv_path>
```

Check the output:
- Total ticket count is plausible
- Resolution rate is in an expected range (warn if below 50% or above 100%)
- No tickets in "Other" that should have been classified (if there are many, offer to add patterns)
- Date range matches the export period

Report a brief summary to the user and confirm setup is complete.

Remind the user:
> "You can now run the numbered prompts (start with `0-orchestrator.prompt.md`). Re-run this setup prompt only if you switch ITSM systems or your CSV format changes."

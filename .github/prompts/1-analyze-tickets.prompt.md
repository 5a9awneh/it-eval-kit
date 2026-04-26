---
agent: agent
description: "Prompt 1 — Ticket Data Analysis: Run analyze_tickets.py after a new ITSM CSV export. Always run before updating any report."
---

# Prompt 1 — Ticket Data Analysis

Read `.github/copilot-instructions.md` for project context.

## Task

A new ticket export CSV has been placed in `Evidence/tickets/`. Run the analysis script to produce fresh statistics.

## Steps

1. **Confirm the CSV path** — ask the user for the exact filename if not already known, or detect the most recent `.csv` file in `Evidence/tickets/`

2. **Check `Tools/config.json`** — verify:
   - `csv_columns` matches the column layout of the new CSV (open the file and check the header row)
   - `date_format` matches the date format in the Created/Resolved columns
   - `csv_header_rows` matches the number of non-data rows at the top of the file
   - If anything differs from the defaults, update `config.json` before running

3. **Run the script:**
   ```
   python Tools/analyze_tickets.py Evidence/tickets/<filename>.csv
   ```
   Or with debug output:
   ```
   python Tools/analyze_tickets.py Evidence/tickets/<filename>.csv --verbose
   ```

4. **Review `Tools/ticket_stats.txt`** — confirm the output looks correct:
   - Total ticket count is plausible for the period
   - Resolution rate is in an expected range
   - Date range matches the export period
   - Category breakdown covers the ticket types you handle
   - If any ticket types are landing in "Other", add their keywords to `categories` in `config.json` and rerun

5. **Report key numbers** to the user:
   - Total tickets, resolution rate, same-day rate, median resolution time
   - The two configured notable operation metrics (as labelled in `ticket_stats.txt`)
   - Peak month, peak quarter, unique requesters
   - Any categories with unexpectedly high or low counts

## Notes
- Classification is based on **subject/title keywords only** — not the CSV's category or group field
- If new ticket types aren't being classified correctly, add patterns to `config.json` — no code changes needed
- The script accepts a `--config` flag if you want to test an alternate config: `--config path/to/other-config.json`

# Evidence

This folder holds your local source data. **Nothing here is ever committed to git** (except `sample/`, which contains safe synthetic data for testing).

Place your files as follows:

```
Evidence/
  sample/                        ← Pre-included synthetic data (committed; safe to share)
  tickets/                       ← Your ITSM CSV exports (git-ignored)
  email-evidence/                ← Outlook-exported email threads (git-ignored)
    projects-initiatives/        ← Project updates, initiative emails
    events-meetings/             ← High-level meeting or event support emails
    learning-certs/              ← Training confirmations, certificates
```

## Tips

### Ticket export
Export a CSV from your ITSM tool (ManageEngine SDP, Jira Service Desk, Freshdesk, ServiceNow, etc.) and place it in `Evidence/tickets/`. See `README.md` for the minimum required columns.

### Email evidence
Use the included VBA macro (`Tools/ExportEachConversationToTxt.bas`) to export relevant Outlook email threads as `.txt` files. **Pre-filter before exporting** — use Outlook categories, flags, folders, or search folders to isolate only the emails worth documenting (project updates, escalations, event support, training). Bulk-exporting everything creates noise that degrades report quality.

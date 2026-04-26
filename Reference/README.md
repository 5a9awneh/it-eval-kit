# Reference

This folder contains your organization-specific inputs that the AI uses to adapt its outputs to your context.

| File | Required? | Purpose |
|---|---|---|
| `role-description.txt` | Recommended | Your job description, terms of reference, or assignment details. Prompts use this to understand what you are responsible for and contextualize your achievements. |
| `performance-review-template.txt` | Recommended | Your organization's actual appraisal or performance review form, pasted as plain text. Prompts read this to understand the required sections, field names, and character limits — and adapt the output to match exactly. |
| `sample-completed-review.md` | Optional | A previous filled-in performance review (your own or a generic example). Prompts use this as a tone, language, and format reference to match your organization's expectations and writing style. |

## How to prepare these files

### `role-description.txt`
Paste the plain-text content of your job description, terms of reference, or assignment description. Include your title, reporting line, key responsibilities, and deliverables. The more detail you provide, the better the AI can contextualize your achievements.

### `performance-review-template.txt`
Copy the text of your org's appraisal form into this file. Include:
- All section names and their labels exactly as they appear in the form
- Any guidance text or instructions included in the form
- Character or word limits for each section (if stated)
- Any rating scales or criteria used

The AI will adapt its output structure to match what your template requires.

### `sample-completed-review.md`
(Optional) Paste a previous performance review — yours from a prior period, or a representative example. This helps the AI match your organization's preferred tone, level of formality, and writing style. Personally identifiable information is fine since this file stays local (it is git-ignored).

## Privacy note

All files in this folder are **git-ignored** and stay on your local machine only. They are never committed to the repository.

"""
analyze_tickets.py — it-eval-kit
Analyzes a service desk CSV export and writes a statistics report.

Usage:
  python analyze_tickets.py <path/to/tickets.csv> [options]

Options:
  --config PATH   Path to config.json  (default: Tools/config.json)
  --verbose       Print each ticket's classified category to stdout
  --help          Show this message

Column mapping, date format, categories, and all other settings are
controlled via config.json — no code changes needed for different ITSM tools.
"""

import argparse
import csv
import io
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


# ── CLI ───────────────────────────────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Analyze a service desk CSV export and produce a statistics report.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("csv_path", help="Path to the ITSM CSV export file.")
    p.add_argument(
        "--config",
        default=None,
        help="Path to config.json (default: Tools/config.json next to this script).",
    )
    p.add_argument(
        "--verbose",
        action="store_true",
        help="Print each ticket's classified category to stdout.",
    )
    return p


# ── Config ────────────────────────────────────────────────────────────────
def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        sys.exit(f"ERROR: Config file not found: {config_path}")
    with open(config_path, encoding="utf-8") as f:
        raw = f.read()
    # Strip _comment keys before parsing (they're documentation, not data)
    data = json.loads(raw)
    return {k: v for k, v in data.items() if not k.startswith("_")}


# ── Classification ────────────────────────────────────────────────────────
def build_classifier(categories: dict):
    """Compile category regex patterns once for performance."""
    compiled = {}
    for cat, patterns in categories.items():
        if cat.startswith("_"):
            continue
        compiled[cat] = [re.compile(p, re.IGNORECASE) for p in patterns]
    return compiled


def classify(subject: str, compiled_categories: dict) -> str:
    """Return the first matching category for a ticket subject, or 'Other'."""
    for category, patterns in compiled_categories.items():
        for p in patterns:
            if p.search(subject):
                return category
    return "Other"


# ── Date parsing ──────────────────────────────────────────────────────────
def parse_dt(value: str, fmt: str):
    """Parse a date string using the configured format. Returns None on failure."""
    try:
        return datetime.strptime(value.strip(), fmt)
    except ValueError:
        return None


# ── Main ──────────────────────────────────────────────────────────────────
def main():
    args = build_parser().parse_args()

    # Ensure stdout handles Unicode safely on Windows terminals
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(errors="replace")

    script_dir = Path(__file__).parent
    config_path = Path(args.config) if args.config else script_dir / "config.json"
    cfg = load_config(config_path)

    csv_path = Path(args.csv_path)
    if not csv_path.exists():
        sys.exit(f"ERROR: CSV file not found: {csv_path}")

    # Column indices
    cols = cfg["csv_columns"]
    col_subject = cols["subject"]
    col_status = cols["status"]
    col_requester = cols["requester"]
    col_created = cols["created"]
    col_resolved = cols["resolved"]
    max_col = max(col_subject, col_status, col_requester, col_created, col_resolved)

    header_rows = cfg.get("csv_header_rows", 0)
    date_fmt = cfg.get("date_format", "%m/%d/%Y %H:%M:%S")
    status_resolved = set(cfg.get("status_resolved", ["Closed", "Resolved"]))
    status_cancelled = set(cfg.get("status_cancelled", ["Canceled", "Cancelled"]))
    output_path = Path(cfg.get("output_path", "Tools/ticket_stats.txt"))

    compiled_cats = build_classifier(cfg.get("categories", {}))

    deploy_label = cfg.get("deploy_label", "New system deployments")
    reformat_label = cfg.get("reformat_label", "OS reformat operations")
    deploy_pats = [re.compile(p, re.IGNORECASE) for p in cfg.get("deploy_patterns", [])]
    reformat_pats = [
        re.compile(p, re.IGNORECASE) for p in cfg.get("reformat_patterns", [])
    ]
    reformat_excl = [
        re.compile(p, re.IGNORECASE) for p in cfg.get("reformat_exclusions", [])
    ]

    # ── Load CSV ──────────────────────────────────────────────────────────
    rows = []
    date_parse_errors = 0

    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            # Skip preamble rows (metadata before the header)
            if i < header_rows:
                continue
            # Skip the column header row — always at index csv_header_rows,
            # regardless of ITSM tool or column naming conventions.
            if i == header_rows:
                continue
            # Skip empty or short rows
            if not row or len(row) <= max_col or not row[0].strip():
                continue
            rows.append(row)

    if not rows:
        sys.exit(
            "ERROR: No data rows found. Check csv_header_rows and column indices in config.json."
        )

    total = len(rows)

    # ── Status breakdown ──────────────────────────────────────────────────
    status_counts = Counter(r[col_status].strip() for r in rows)
    closed = sum(status_counts[s] for s in status_resolved if s in status_counts)
    canceled = sum(status_counts[s] for s in status_cancelled if s in status_counts)
    open_ = total - closed - canceled
    resolution_rate = closed / total * 100 if total else 0

    # ── Date metrics ──────────────────────────────────────────────────────
    created_dts = []
    resolved_dts = []
    for r in rows:
        cd = parse_dt(r[col_created], date_fmt)
        rd = parse_dt(r[col_resolved], date_fmt)
        if cd is None and r[col_created].strip():
            date_parse_errors += 1
        created_dts.append(cd)
        resolved_dts.append(rd)

    if date_parse_errors > 0:
        print(
            f"WARNING: {date_parse_errors} date(s) could not be parsed. "
            f"Check 'date_format' in config.json (current: \"{date_fmt}\"). "
            "Unparseable dates are excluded from time-based metrics.",
            file=sys.stderr,
        )

    valid_created = [d for d in created_dts if d]
    first_ticket = min(valid_created) if valid_created else None
    last_ticket = max(valid_created) if valid_created else None

    # Resolution times (resolved tickets only)
    res_times_h = []
    same_day = 0
    for r, cd, rd in zip(rows, created_dts, resolved_dts):
        if r[col_status].strip() in status_resolved and cd and rd:
            delta_h = (rd - cd).total_seconds() / 3600
            if delta_h >= 0:
                res_times_h.append(delta_h)
                if delta_h <= 24:
                    same_day += 1

    res_times_h.sort()
    n_res = len(res_times_h)
    median_h = res_times_h[n_res // 2] if n_res else 0
    avg_h = sum(res_times_h) / n_res if n_res else 0
    same_day_pct = same_day / closed * 100 if closed else 0

    # ── Monthly distribution ──────────────────────────────────────────────
    monthly = Counter()
    for d in valid_created:
        monthly[d.strftime("%Y-%m")] += 1
    sorted_months = sorted(monthly.items())
    peak_month = max(monthly, key=lambda k: monthly[k]) if monthly else "N/A"
    peak_count = monthly.get(peak_month, 0)
    monthly_avg = total / len(monthly) if monthly else 0

    # ── Day-of-week and hourly distribution ───────────────────────────────
    day_counter = Counter()
    hour_counter = Counter()
    for d in valid_created:
        day_counter[d.strftime("%A")] += 1
        hour_counter[d.hour] += 1
    peak_day = max(day_counter, key=lambda k: day_counter[k]) if day_counter else "N/A"
    peak_hour: int | None = (
        max(hour_counter, key=lambda k: hour_counter[k]) if hour_counter else None
    )

    # ── Unique requesters ─────────────────────────────────────────────────
    unique_requesters = len(
        {r[col_requester].strip() for r in rows if r[col_requester].strip()}
    )

    # ── Category classification ───────────────────────────────────────────
    ticket_categories = []
    for r in rows:
        cat = classify(r[col_subject], compiled_cats)
        ticket_categories.append(cat)
        if args.verbose:
            line = f"  [{cat}] {r[col_subject][:80]}"
            print(
                line.encode(sys.stdout.encoding, errors="replace").decode(
                    sys.stdout.encoding
                )
            )
    category_counts = Counter(ticket_categories)
    category_sorted = category_counts.most_common()

    # ── Deployments & reformats ───────────────────────────────────────────
    def _matches(subject, patterns):
        return any(p.search(subject) for p in patterns)

    resolved_rows = [r for r in rows if r[col_status].strip() in status_resolved]
    deploy_count = sum(
        1 for r in resolved_rows if _matches(r[col_subject], deploy_pats)
    )
    reformat_count = sum(
        1
        for r in resolved_rows
        if _matches(r[col_subject], reformat_pats)
        and not _matches(r[col_subject], reformat_excl)
    )

    # ── Quarterly breakdown ───────────────────────────────────────────────
    quarterly = Counter()
    for d in valid_created:
        q = f"Q{(d.month - 1) // 3 + 1} {d.year}"
        quarterly[q] += 1
    quarterly_sorted = sorted(quarterly.items())
    peak_quarter = max(quarterly, key=lambda k: quarterly[k]) if quarterly else "N/A"
    peak_q_count = quarterly.get(peak_quarter, 0)

    # ── Build output ──────────────────────────────────────────────────────
    L = []
    L.append("=" * 60)
    L.append("  SERVICE DESK TICKET STATISTICS")
    L.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    L.append("=" * 60)
    L.append("")

    L.append("── OVERVIEW ─────────────────────────────────────────────")
    L.append(f"  Total tickets:          {total:,}")
    L.append(
        f"  Date range:             "
        f"{first_ticket.strftime('%d %b %Y') if first_ticket else 'N/A'}"
        f"  →  "
        f"{last_ticket.strftime('%d %b %Y') if last_ticket else 'N/A'}"
    )
    L.append(f"  Tenure months:          {len(monthly)}")
    L.append(f"  Unique requesters:      {unique_requesters:,}")
    L.append(f"  {deploy_label}: {deploy_count:,}  (subject-keyword, resolved only)")
    L.append(
        f"  {reformat_label}: {reformat_count:,}  (subject-keyword, resolved only)"
    )
    L.append("")

    L.append("── STATUS BREAKDOWN ─────────────────────────────────────")
    L.append(f"  Resolved/Closed:        {closed:,}  ({closed/total*100:.1f}%)")
    L.append(f"  Cancelled:              {canceled:,}  ({canceled/total*100:.1f}%)")
    if open_ > 0:
        L.append(f"  Other/Open:             {open_:,}  ({open_/total*100:.1f}%)")
    L.append(f"  Resolution rate:        {resolution_rate:.1f}%  (Resolved / Total)")
    L.append("")

    L.append("── RESPONSE / RESOLUTION TIMES ──────────────────────────")
    L.append(f"  Resolved tickets timed: {n_res:,}")
    L.append(f"  Median resolution time: {median_h:.1f} hours  ({median_h*60:.0f} min)")
    L.append(f"  Average resolution:     {avg_h:.1f} hours")
    L.append(
        f"  Same-day (≤24h):        {same_day:,}  ({same_day_pct:.1f}% of Resolved)"
    )
    L.append("")

    L.append("── VOLUME PATTERNS ──────────────────────────────────────")
    L.append(f"  Monthly average:        {monthly_avg:.0f} tickets/month")
    L.append(f"  Peak month:             {peak_month}  ({peak_count:,} tickets)")
    L.append(f"  Peak quarter:           {peak_quarter}  ({peak_q_count:,} tickets)")
    L.append(
        f"  Peak day-of-week:       {peak_day}  ({day_counter.get(peak_day, 0):,} tickets)"
    )
    L.append(
        f"  Peak hour:              "
        + (
            f"{peak_hour:02d}:00  ({hour_counter[peak_hour]:,} tickets)"
            if peak_hour is not None
            else "N/A"
        )
    )
    L.append("")

    L.append("── MONTHLY BREAKDOWN ────────────────────────────────────")
    for ym, cnt in sorted_months:
        bar = "█" * (cnt // 5)
        L.append(f"  {ym}  {cnt:4d}  {bar}")
    L.append("")

    L.append("── QUARTERLY BREAKDOWN ──────────────────────────────────")
    for qtr, cnt in quarterly_sorted:
        L.append(f"  {qtr:<10}  {cnt:4d}")
    L.append("")

    L.append("── CATEGORY BREAKDOWN ───────────────────────────────────")
    L.append("  (Derived from subject-keyword analysis — CSV category field not used)")
    for cat, cnt in category_sorted:
        pct = cnt / total * 100
        L.append(f"  {cat:<25}  {cnt:4d}  ({pct:.1f}%)")
    L.append("")

    L.append("── DAY-OF-WEEK DISTRIBUTION ─────────────────────────────")
    for day in [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]:
        cnt = day_counter.get(day, 0)
        L.append(f"  {day:<12}  {cnt:4d}")
    L.append("")

    L.append("── HOURLY DISTRIBUTION ──────────────────────────────────")
    for h in range(24):
        cnt = hour_counter.get(h, 0)
        bar = "█" * (cnt // 10)
        L.append(f"  {h:02d}:00  {cnt:4d}  {bar}")
    L.append("")

    output = "\n".join(L)

    # Resolve output path relative to repo root (one level up from Tools/)
    out_full = (
        script_dir.parent / output_path
        if not Path(output_path).is_absolute()
        else Path(output_path)
    )
    out_full.parent.mkdir(parents=True, exist_ok=True)
    out_full.write_text(output, encoding="utf-8")

    print(output)
    print(f"\n✓ Stats saved to: {out_full}")


if __name__ == "__main__":
    main()

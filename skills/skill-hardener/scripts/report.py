#!/usr/bin/env python3
"""report.py — Plain-language, skill-first friction report for skill-hardener.

This is the view a human reads. It leads with "which skills gave you the most
grief", ranked, with simple bars — not raw signature counts (that's what
mine_friction.py is for, under the hood).

It consults the hardening ledger (hardening-log.jsonl) so a skill you've already
fixed only shows friction that happened AFTER the fix date. That answers the
question "did my fix work?":
  - fix worked  -> the skill drops to the bottom, marked done, next-worst rises.
  - fix failed  -> NEW post-fix grief appears and re-flags it.

Usage:
  report.py                 # all projects, last 30 days
  report.py --days 14
  report.py --project convex
  report.py --min 2         # how many rough moments before a skill is listed
"""
import argparse, glob, json, os, sys
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mine_friction import analyze_session, PROJECTS, session_mtime_days  # noqa: E402

LEDGER = os.path.join(os.path.dirname(HERE), "hardening-log.jsonl")

# Signals that genuinely mean "you had a bad time", in plain language.
TROUBLE = {
    "user_frustration": "pushed back / corrected it",
    "user_interrupt":   "stopped it mid-run",
    "repeated_tool_error": "it kept erroring",
}
# High-volume signals that are usually just normal writing work, not real
# trouble. Kept out of the ranking; mentioned only as a footnote.
NOISE = {"repeated_edit", "claimed_done_no_verify"}


def load_ledger():
    """Return {skill: latest_fix_date_iso}."""
    fixes = {}
    if os.path.exists(LEDGER):
        for line in open(LEDGER, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            sk, d = e.get("skill"), e.get("date")
            if sk and d and (sk not in fixes or d > fixes[sk]):
                fixes[sk] = d
    return fixes


def bar(n, mx, width=10):
    if mx <= 0:
        return "░" * width
    fill = round(width * n / mx)
    return "█" * fill + "░" * (width - fill)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--min", type=int, default=2,
                    help="min rough moments before a skill is listed")
    args = ap.parse_args()

    paths = glob.glob(os.path.join(PROJECTS, "*", "*.jsonl"))
    if args.project:
        paths = [p for p in paths if args.project.lower() in p.lower()]
    if args.days:
        paths = [p for p in paths if session_mtime_days(p) <= args.days]

    events = []
    for p in paths:
        try:
            events += analyze_session(p)
        except Exception:
            pass

    fixes = load_ledger()

    pre = defaultdict(Counter)    # trouble before a recorded fix (addressed)
    post = defaultdict(Counter)   # trouble after the fix, or no fix (current)
    noise_ct = Counter()
    for e in events:
        sk = e["active_skills"][-1] if e["active_skills"] else None
        if not sk:
            continue
        if e["signature"] in NOISE:
            noise_ct[sk] += 1
            continue
        if e["signature"] not in TROUBLE:
            continue
        fix = fixes.get(sk)
        if fix and e.get("timestamp", "")[:10] < fix:
            pre[sk][e["signature"]] += 1
        else:
            post[sk][e["signature"]] += 1

    rows = [(sk, sum(post[sk].values())) for sk in set(pre) | set(post)]
    rows.sort(key=lambda r: -r[1])
    mx = max([c for _, c in rows], default=0)

    title = "Which skills are giving you grief"
    if args.days:
        title += f" (last {args.days} days)"
    print(title)
    print("─" * 56)

    shown = 0
    for sk, cur in rows:
        fix = fixes.get(sk)
        had_pre = sum(pre[sk].values())
        # list it if it has current grief over the bar, OR it's a fixed skill
        # we want to show as resolved
        if cur < args.min and not (fix and had_pre):
            continue
        tag = ""
        if fix:
            tag = (f"   ✓ fixed {fix} — no new grief since" if cur == 0
                   else f"   ⚑ fixed {fix} — but these are NEW since the fix")
        print(f"{sk:<22} {bar(cur, mx)} {cur} rough moment(s){tag}")
        moments = ", ".join(f"{TROUBLE[s]} {n}x" for s, n in post[sk].most_common())
        if moments:
            print(f"{'':<22} {moments}")
        if fix and had_pre:
            print(f"{'':<22} (was {had_pre} before the fix — counted as addressed)")
        shown += 1

    if shown == 0:
        print("  Nothing above the bar. Quiet stretch — no skill stands out.")

    noisy = [f"{sk} ({n})" for sk, n in noise_ct.most_common(5) if n >= 20]
    if noisy:
        print("\nFootnote (usually just normal writing, not real trouble — "
              "lots of edits / 'done' claims): " + ", ".join(noisy))


if __name__ == "__main__":
    main()

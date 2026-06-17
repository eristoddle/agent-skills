#!/usr/bin/env python3
"""
mine_friction.py — Extract recurring failure signatures from Claude Code transcripts.

Reads ~/.claude/projects/<dir>/*.jsonl session logs and emits structured friction
events plus a clustered summary. Pure stdlib, read-only. It never edits anything;
it just gives the skill-hardener workflow evidence to reason over.

Usage:
  mine_friction.py                      # all projects, last 30 days
  mine_friction.py --days 14            # window
  mine_friction.py --project skillshare # substring-match one project dir
  mine_friction.py --session FILE.jsonl # a single transcript
  mine_friction.py --json out.json      # write full event list to file
  mine_friction.py --min-cluster 3      # only summarize signatures seen >= N times

Signature definitions live in references/signatures.md (keep in sync).
"""
import argparse, glob, json, os, re, sys, time
from collections import Counter, defaultdict

PROJECTS = os.path.expanduser("~/.claude/projects")

# --- frustration / correction lexicon (user pushback) ------------------------
# Precision-tuned: explicit correction / frustration phrasing only. Broad
# negations ("no", "don't", "again") were dropped — they fire constantly in
# normal planning speech and tanked precision. Structural signatures carry recall.
NEG_PATTERNS = [
    r"\bthat'?s (wrong|not (right|what|it))\b", r"\bnot what i (asked|wanted|said)\b",
    r"\bstop\b", r"\bundo (that|this)\b", r"\brevert\b", r"\bgaslight",
    r"\bendless loop\b", r"\bstill (broken|failing|wrong|not working)\b",
    r"\byou (didn'?t|keep|always|never|still)\b", r"\bwhy did you\b",
    r"\bi (already )?(said|told you|asked)\b", r"\bdon'?t (do|keep|change|touch)\b",
    r"\bget off\b", r"\bquit (doing|trying)\b", r"\bthis is (wrong|broken)\b",
]
NEG_RE = re.compile("|".join(NEG_PATTERNS), re.I)
# Plan reversal needs reversal-specific language, not generic negativity.
REVERSAL_RE = re.compile(
    r"\bthat'?s not the plan\b|\bdon'?t (do|build|implement) (that|this)\b|"
    r"\bnot what (we|i) (planned|agreed)\b|\bscrap (that|the plan)\b|"
    r"\b(go back|start over)\b|\bnot (like )?that\b", re.I)
INTERRUPT_RE = re.compile(r"\[Request interrupted by user", re.I)
DONE_RE = re.compile(r"\b(all set|done|fixed|should work|works now|that should|resolved|complete)\b", re.I)
VERIFY_TOOLS = {"Bash"}  # ran something
VERIFY_HINT_RE = re.compile(r"\b(test|pytest|npm test|run|build|verify|check)\b", re.I)


def text_of(content):
    """Flatten a message.content (str or list of blocks) to plain text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        out = []
        for b in content:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "text":
                out.append(b.get("text", ""))
            elif b.get("type") == "tool_result":
                c = b.get("content")
                out.append(text_of(c) if not isinstance(c, str) else c)
        return "\n".join(out)
    return ""


def caps_ratio(s):
    letters = [c for c in s if c.isalpha()]
    if len(letters) < 8:
        return 0.0
    return sum(c.isupper() for c in letters) / len(letters)


# Auto-generated user-role messages that are NOT human speech: plan-approval
# confirmations, harness reminders, skill SKILL.md text injected at load time,
# subagent/task notifications, and slash-command output injected as context.
AUTO_USER_RE = re.compile(
    r"^\s*(User has approved your plan|Your plan has been saved|"
    r"\[Request interrupted|<system-reminder|<task-notification|<command-name|"
    r"<local-command|Caveat:|This session is being continued|"
    r"Base directory for this skill:|The user just ran /|"
    r"Result of calling the|<user-prompt-submit-hook)",
    re.I,
)
SKILL_INJECT_RE = re.compile(r"<essential_principles>|<skill_instructions>|^Invoke this skill", re.M)


def real_user_text(content):
    """Return text ONLY for a genuine human-typed turn, else None.

    Critical: in Claude Code transcripts, tool results come back as role='user'
    messages (content is a list containing a tool_result block) and file reads
    show up as line-numbered dumps inside those results. Those are NOT user
    speech. We only accept a plain string, or a list whose blocks are all text
    (no tool_result), and we drop harness-generated messages.
    """
    if isinstance(content, str):
        txt = content
    elif isinstance(content, list):
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
            return None  # this is a tool result, not the user talking
        txt = "\n".join(b.get("text", "") for b in content
                        if isinstance(b, dict) and b.get("type") == "text")
    else:
        return None
    txt = txt.strip()
    if not txt or AUTO_USER_RE.match(txt) or SKILL_INJECT_RE.search(txt):
        return None
    return txt


def iter_events(path):
    """Yield parsed jsonl records in order."""
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def analyze_session(path):
    """Walk one transcript, return list of friction events."""
    events = []
    active_skills = []          # Skill tool invocations seen so far
    edit_counts = Counter()     # file_path -> times edited
    tool_errors = Counter()     # tool name -> consecutive-ish error count
    last_exit_plan = None       # timestamp/uuid of most recent plan presentation
    last_assistant_text = ""
    last_assistant_ran_check = False
    sess = os.path.basename(path)

    def emit(sig, ts, snippet, **extra):
        ev = {
            "session": sess, "path": path, "signature": sig,
            "timestamp": ts, "active_skills": list(active_skills),
            "snippet": (snippet or "")[:280].replace("\n", " "),
        }
        ev.update(extra)
        events.append(ev)

    for rec in iter_events(path):
        rtype = rec.get("type")
        ts = rec.get("timestamp", "")
        msg = rec.get("message") if isinstance(rec.get("message"), dict) else {}
        role = msg.get("role")
        content = msg.get("content")

        # --- track assistant actions -------------------------------------
        if rtype == "assistant" and isinstance(content, list):
            ran_check = False
            for b in content:
                if not isinstance(b, dict) or b.get("type") != "tool_use":
                    continue
                name = b.get("name", "")
                inp = b.get("input", {}) or {}
                if name == "Skill":
                    sk = inp.get("skill") or inp.get("command")
                    if sk:
                        active_skills.append(sk)
                if name in ("Edit", "Write", "NotebookEdit"):
                    fp = inp.get("file_path", "?")
                    edit_counts[fp] += 1
                    if edit_counts[fp] == 3:
                        emit("repeated_edit", ts, f"{fp} edited 3x in session",
                             file_path=fp)
                    elif edit_counts[fp] > 3:
                        # update the snippet count on the existing event
                        emit("repeated_edit", ts,
                             f"{fp} edited {edit_counts[fp]}x in session",
                             file_path=fp)
                if name in VERIFY_TOOLS:
                    cmd = json.dumps(inp)
                    if VERIFY_HINT_RE.search(cmd):
                        ran_check = True
                if name == "ExitPlanMode":
                    last_exit_plan = ts
            last_assistant_text = text_of(content)
            last_assistant_ran_check = ran_check
            # claimed-done-without-verify
            if DONE_RE.search(last_assistant_text) and not ran_check:
                emit("claimed_done_no_verify", ts, last_assistant_text)

        # --- track tool errors -------------------------------------------
        if rtype in ("user", "assistant") and isinstance(content, list):
            for b in content:
                if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("is_error"):
                    tool_errors["_"] += 1
                    if tool_errors["_"] in (3, 5, 8):
                        emit("repeated_tool_error", ts,
                             text_of(b.get("content", "")),
                             error_streak=tool_errors["_"])

        # --- user turns: frustration, interrupts, plan reversal ----------
        if rtype == "user":
            # interrupt marker is checked on raw content (it's filtered out of
            # real_user_text as harness-generated, but it IS a real signal)
            raw = text_of(content)
            if INTERRUPT_RE.search(raw) and not (
                isinstance(content, list)
                and any(isinstance(b, dict) and b.get("type") == "tool_result"
                        for b in content)
            ):
                emit("user_interrupt", ts, raw)
                tool_errors["_"] = 0
            utext = real_user_text(content)  # genuine human speech only
            if utext:
                hits = NEG_RE.search(utext)
                cap = caps_ratio(utext)
                # plan reversal: explicit reversal language shortly after a plan
                if last_exit_plan and REVERSAL_RE.search(utext):
                    emit("plan_reversal", ts, utext, caps_ratio=round(cap, 2))
                    last_exit_plan = None
                elif hits or cap > 0.6:
                    emit("user_frustration", ts, utext, caps_ratio=round(cap, 2))
                # a fresh human instruction relaxes the error streak
                tool_errors["_"] = max(0, tool_errors["_"] - 1)

        # --- system: hook blocks / prevented continuation ----------------
        if rtype == "system":
            if rec.get("preventedContinuation") or rec.get("hookErrors"):
                emit("hook_block", ts,
                     str(rec.get("hookErrors") or rec.get("stopReason") or "prevented"),
                     subtype=rec.get("subtype", ""))

    return events


def session_mtime_days(path):
    return (time.time() - os.path.getmtime(path)) / 86400.0


def collect(paths, days):
    all_events = []
    scanned = 0
    for p in paths:
        if days and session_mtime_days(p) > days:
            continue
        scanned += 1
        try:
            all_events.extend(analyze_session(p))
        except Exception as e:
            print(f"warn: failed {p}: {e}", file=sys.stderr)
    return all_events, scanned


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", help="substring match against project dir name")
    ap.add_argument("--session", help="single .jsonl transcript path")
    ap.add_argument("--days", type=int, default=30, help="only sessions modified within N days (0=all)")
    ap.add_argument("--min-cluster", type=int, default=2, help="min occurrences to show a signature cluster")
    ap.add_argument("--json", help="write full event list to this file")
    args = ap.parse_args()

    if args.session:
        paths = [args.session]
    else:
        pat = os.path.join(PROJECTS, "*", "*.jsonl")
        paths = glob.glob(pat)
        if args.project:
            paths = [p for p in paths if args.project.lower() in p.lower()]
    if not paths:
        print("No transcripts matched.", file=sys.stderr)
        sys.exit(2)

    events, scanned = collect(paths, args.days)

    # cluster by signature
    by_sig = defaultdict(list)
    for e in events:
        by_sig[e["signature"]].append(e)

    # cluster by (signature, active skill) for attribution
    by_attr = Counter()
    for e in events:
        sk = e["active_skills"][-1] if e["active_skills"] else "(base / CLAUDE.md)"
        by_attr[(e["signature"], sk)] += 1

    print(f"# Friction scan")
    print(f"scanned {scanned} sessions (window: {args.days or 'all'}d), "
          f"{len(events)} events\n")

    print("## Signature clusters (most frequent first)")
    for sig, evs in sorted(by_sig.items(), key=lambda kv: -len(kv[1])):
        if len(evs) < args.min_cluster:
            continue
        sessions = {e["session"] for e in evs}
        print(f"- **{sig}** — {len(evs)} events across {len(sessions)} sessions")

    print("\n## Attribution (signature → responsible artifact)")
    for (sig, sk), n in by_attr.most_common(25):
        if n < args.min_cluster:
            continue
        print(f"- {sig} :: {sk} — {n}")

    print("\n## Top examples")
    shown = 0
    for sig, evs in sorted(by_sig.items(), key=lambda kv: -len(kv[1])):
        if len(evs) < args.min_cluster:
            continue
        ex = evs[0]
        print(f"- [{sig}] {ex['session'][:8]} @ {ex['timestamp'][:19]}: {ex['snippet']}")
        shown += 1
        if shown >= 15:
            break

    if args.json:
        with open(args.json, "w") as fh:
            json.dump(events, fh, indent=2)
        print(f"\nwrote {len(events)} events -> {args.json}")


if __name__ == "__main__":
    main()

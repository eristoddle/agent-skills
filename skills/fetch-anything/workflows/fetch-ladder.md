# Fetch Ladder

Generic escalation for any URL with no registered custom handler. Climbs defuddle → webfetch → crawl4ai → playwright-cli → browser-act, stopping at the first rung that returns real content. On total failure, hands off to debug-research.

**Inputs:** a URL; optionally an extraction hint ("just the comments", "the price table").
**Prerequisites:** none. Each rung self-checks its tool's availability.

Read `references/tool-cheatsheet.md` before starting — it has the exact invocations and the failure-signal patterns that decide when to climb. Maintain the running error log described there across all rungs.

---

## Step 1 — Rung 1: defuddle

**Goal:** Get clean markdown the cheapest way.

1. Confirm the binary exists (`defuddle --version`). If missing, log "binary missing" and skip to Step 2.
2. Run defuddle on the URL per the cheatsheet.
3. Evaluate the output against the failure signals in the cheatsheet.
4. If it returned real content → go to Step 6 (Deliver). Otherwise append the result to the error log and go to Step 2.

**Output:** clean markdown (success) or an appended error-log line (failure).

---

## Step 2 — Rung 2: webfetch

**Goal:** Let the native fetch tool try, with an extraction prompt.

1. Call WebFetch with the URL and a prompt: the user's hint if given, else "Return the main readable content as markdown."
2. Evaluate against the failure signals.
3. If real content → go to Step 6 (Deliver). Otherwise append to the error log and go to Step 3.

**Output:** content (success) or an appended error-log line (failure).

---

## Step 3 — Rung 3: crawl4ai (stealth browser)

**Goal:** Render with an anti-bot-aware browser to defeat JS-shells, soft blocks, and bot challenges that plain playwright can't pass.

1. Confirm `crawl4ai` is available (`python -c "import crawl4ai"`). If missing: `pip install crawl4ai && crawl4ai-setup`. Log and skip to Step 4 if setup fails.
2. Run using the pattern from the cheatsheet (magic mode + simulate_user).
3. Evaluate the output against the failure signals.
4. If real content → go to Step 6 (Deliver). Otherwise append to the error log and go to Step 4.

**Output:** content (success) or an appended error-log line (failure).

---

## Step 4 — Rung 4: playwright-cli

**Goal:** Plain browser render — use when crawl4ai specifically fails (e.g., site blocks patchright but not stock Chromium).

1. Use the `playwright-cli` skill to render the page and dump HTML (cheatsheet has the pattern).
2. Feed the dumped HTML back through `defuddle parse page.html --md` to get token-cheap markdown.
3. Evaluate against the failure signals.
4. If real content → go to Step 6 (Deliver). Otherwise append to the error log and go to Step 5.

**Output:** content (success) or an appended error-log line (failure).

---

## Step 5 — Rung 5: browser-act (UNTESTED — last resort before debug-research)

**Goal:** Throw the heaviest available tool at the page: an anti-detection browser with captcha bypass, optional proxies, persistent sessions, and human-in-the-loop assist — the things crawl4ai and playwright-cli can't do.

⚠️ **This rung is UNTESTED in this skill.** It only runs after every proven rung above has failed. If it errors or behaves unexpectedly, don't fight it — log the result and fall through to debug-research (Step 7). Read `references/browser-act.md` before invoking; that file has the mandatory bootstrap, the exact commands, and the Confirmation Gate rules (browser-act requires explicit user approval before creating a browser or doing anything sensitive).

1. Confirm the CLI exists (`browser-act --version`). If missing, log "browser-act missing" and skip to Step 7.
2. Run the **mandatory bootstrap** first: `browser-act get-skills core --skill-version 2.0.2` (do NOT skip or truncate — it carries operational directives). Follow `references/browser-act.md`.
3. Try the cheap path first: `browser-act stealth-extract "<URL>"` (no session, no browser creation, no confirmation needed).
4. If that's still blocked and the content is worth a full session, escalate **within browser-act** to a real browser session — but only with user confirmation per the Confirmation Gate (captcha solving via `solve-captcha`, or `remote-assist` to hand the user the wheel).
5. Evaluate against the failure signals.
6. If real content → go to Step 6 (Deliver), noting it came from the untested rung. If this rung also fails, append to the error log and go to Step 7.

**Output:** content (success) or an appended error-log line (failure).

---

## Step 6 — Deliver

**Goal:** Hand the user usable content.

1. Return the markdown. If an extraction hint was given, narrow to what they asked for; otherwise give the full clean article.
2. Briefly note which rung succeeded only if it's interesting (e.g. "defuddle was blocked, got it via crawl4ai"; always flag it if the untested browser-act rung was what worked, so the user knows). Don't narrate on a clean first-rung success.

**Output:** final content to the user. Workflow ends here.

---

## Step 7 — Escalate to debug-research

**Goal:** Refuse to quit.

1. Do NOT tell the user it's impossible.
2. Read `workflows/debug-research.md` and follow it, passing the URL, the extraction hint, and the full error log.

**Output:** control passes to debug-research.

---

## Done

This workflow is complete when:
- [ ] The user has the content (a rung succeeded), OR
- [ ] Control was handed to `debug-research.md` with a complete error log — never a bare failure message.

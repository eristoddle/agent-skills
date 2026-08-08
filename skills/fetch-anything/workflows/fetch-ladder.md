# Fetch Ladder

Generic escalation for any URL with no registered custom handler. Three rungs:
**defuddle → crawl4ai → firecrawl**, stopping at the first that returns real content.
On total failure, hands off to debug-research.

**Inputs:** a URL; optionally an extraction hint ("just the comments", "the price table").
**Prerequisites:** none for rungs 1–2. Rung 3 needs `firecrawl` installed + an API key.

Read `references/tool-cheatsheet.md` before starting — it has the exact invocations
and the failure-signal patterns that decide when to climb. Maintain the running error
log described there across all rungs.

**Why these three.** Months of real use settled it: crawl4ai has by far the highest
success rate, so it sits early rather than buried at rung 3 of 5. defuddle stays first
purely on token economy — when it works it's the cheapest thing available. firecrawl is
the paid backstop that handles what a local browser can't. The rungs that used to sit
between them (webfetch, playwright-cli, browser-act) never earned their place: webfetch
fails on exactly the pages defuddle fails on, and the browser rungs were redundant with
crawl4ai. They aren't gone — they moved to `debug-research.md`'s toolbox, where a
diagnosis picks them deliberately instead of the ladder trying them by rote.

---

## Step 1 — Rung 1: defuddle

**Goal:** Get clean markdown the cheapest way.

1. Confirm the binary exists (`defuddle --version`). If missing, log "binary missing" and skip to Step 2.
2. Run defuddle on the URL per the cheatsheet.
3. Evaluate the output against the failure signals in the cheatsheet.
4. If it returned real content → go to Step 4 (Deliver). Otherwise append the result to the error log and go to Step 2.

Don't spend more than one attempt here. defuddle either cleanly gets the article or it
doesn't — retrying with different flags is wasted time, climb instead.

**Output:** clean markdown (success) or an appended error-log line (failure).

---

## Step 2 — Rung 2: crawl4ai (stealth browser) — the workhorse

**Goal:** Render with an anti-bot-aware browser. This rung defeats JS-shells, soft
blocks, and most bot challenges, and in practice succeeds more often than any other
rung in this skill.

1. Confirm `crawl4ai` is available (`python -c "import crawl4ai"`). If missing: `pip install crawl4ai && crawl4ai-setup`. Log and skip to Step 3 if setup fails.
2. Run using the pattern from the cheatsheet (magic mode + simulate_user).
3. Evaluate the output against the failure signals.
4. If real content → go to Step 4 (Deliver). Otherwise append to the error log and go to Step 3.

Because this rung carries the ladder, it's worth **one** retry before climbing when the
failure looks transient rather than structural — a timeout or `networkidle` that never
settled. Retry with `wait_until="domcontentloaded"` and a longer `page_timeout`. A 403
or a captcha is structural: don't retry, climb.

**Output:** content (success) or an appended error-log line (failure).

---

## Step 3 — Rung 3: firecrawl (paid API backstop)

**Goal:** Hand the page to a hosted service with its own proxy pool and rendering
infrastructure — the things a local browser can't provide.

1. Confirm the CLI exists (`firecrawl --version`). If missing, log "firecrawl missing" and skip to Step 5.
2. Run the scrape per the cheatsheet, **always with `-o` to a file** — never let a full
   page render into the transcript.
3. Read a bounded slice of the output file to evaluate it against the failure signals.
4. If still blocked, retry **once** with `--proxy auto` (firecrawl's own escalation — it
   costs more credits, so it's a deliberate second attempt, not the default).
5. If real content → go to Step 4 (Deliver). Otherwise append to the error log and go to Step 5.

This rung costs money per call. That's the reason it's last, and the reason rungs 1–2
get a genuine attempt first rather than a token one.

**Output:** content (success) or an appended error-log line (failure).

---

## Step 4 — Deliver

**Goal:** Hand the user usable content.

1. Return the markdown. If an extraction hint was given, narrow to what they asked for; otherwise give the full clean article.
2. Note which rung succeeded only if it's interesting — e.g. "defuddle was blocked, got it via crawl4ai", or always when firecrawl was what worked, since that one bills the user.
3. Don't narrate a clean first-rung success.

**Output:** final content to the user. Workflow ends here.

---

## Step 5 — Escalate to debug-research

**Goal:** Refuse to quit.

1. Do NOT tell the user it's impossible.
2. Read `workflows/debug-research.md` and follow it, passing the URL, the extraction hint, and the full error log. Its toolbox includes playwright-cli and browser-act — the ex-rungs — plus hidden APIs, alternate hosts, and archives.

**Output:** control passes to debug-research.

---

## Done

This workflow is complete when:
- [ ] The user has the content (a rung succeeded), OR
- [ ] Control was handed to `debug-research.md` with a complete error log — never a bare failure message.

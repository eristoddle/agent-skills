# Tool Cheatsheet

Exact invocations for each rung of the ladder, and the signal patterns that mean a rung
**failed** and you must climb. Read by `fetch-ladder.md` and `debug-research.md`.

Ladder: **defuddle → crawl4ai → firecrawl**. Everything below the horizontal break near
the bottom is the debug-research toolbox, not a rung.

---

## Bounded output — applies to every rung

A rendered page can be hundreds of KB. Dumping one into the transcript is the fastest
way to end a session.

- Prefer writing to a file and reading a bounded slice over printing to stdout.
- `firecrawl` has `-o`; use it always. For crawl4ai, write `result.markdown` to a path
  and print only its length, then read what you need.
- When only part of the page matters, narrow at the source (`css_selector`,
  `--include-tags`, `--only-main-content`) rather than fetching everything and skimming.

---

## Rung 1 — defuddle (internalized)

`defuddle` extracts the main article content from a URL or HTML file and returns clean
markdown, stripping nav/ads/sidebars. Cheapest rung for token usage — prefer it first.

```bash
# From a live URL (defuddle fetches it itself):
defuddle parse "<URL>" --md

# If you already have HTML on disk (e.g. a browser dumped it):
defuddle parse page.html --md

# Markdown is the default for most builds; if --md is unsupported, drop it.
defuddle parse "<URL>"
```

Notes:
- Check availability with `defuddle --version`. If missing, skip this rung and note it in the error log (don't abort the ladder).
- Best for article/blog/news pages. Weak on heavily interactive apps, infinite-scroll feeds, and login-walled pages — expect to climb for those.
- Also the **cleanup stage** for any rung that yields raw HTML: `defuddle parse page.html --md`.

---

## Rung 2 — crawl4ai (stealth browser) — highest success rate

Drives a headless browser with anti-bot bypass (patchright + magic mode). `magic=True`
randomizes fingerprints and simulates human behavior; `css_selector` narrows to a section
and cuts token cost.

```python
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

async def fetch(url: str, css_selector: str = None) -> str:
    browser_cfg = BrowserConfig(browser_type="chromium", headless=True)
    run_cfg = CrawlerRunConfig(
        magic=True,
        simulate_user=True,
        wait_until="networkidle",
        page_timeout=30000,
        css_selector=css_selector,  # omit to get the full page
    )
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(url=url, config=run_cfg)
        if not result.success:
            return f"Error: {result.error_message}"
        return result.markdown

md = asyncio.run(fetch("<URL>"))
open("/tmp/page.md", "w").write(md)   # write, don't print
print(len(md), "chars ->", "/tmp/page.md")
```

Check availability: `python -c "import crawl4ai"`. Install if missing: `pip install crawl4ai && crawl4ai-setup`.

**Transient-failure retry** (once, then climb): if it timed out or `networkidle` never
settled, retry with `wait_until="domcontentloaded"` and `page_timeout=60000`. A 403 or
captcha is structural — climb instead of retrying.

---

## Rung 3 — firecrawl (paid API backstop)

Hosted scraping API with its own proxy pool and rendering infra. **CLI, not MCP.**

### Setup (one-time)

Account + API key: https://firecrawl.link/stephan-miller — the free tier is 1,000
credits/month, which comfortably covers this rung's usage.

```bash
npm install -g firecrawl-cli
```

⚠️ Use the plain npm install, **not** the `curl … install.sh` one-liner and **not**
`firecrawl init`. Those install Firecrawl's own agent skills — and optionally its MCP
server — into every detected editor (Claude Code, Cursor, Windsurf…). This skill drives
the CLI directly and wants none of that.

Auth resolves in this order: `--api-key` flag → `FIRECRAWL_API_KEY` env var → the CLI's
stored login. Setting the env var permanently is enough (see the skill's setup note);
`firecrawl login --api-key fc-...` is the alternative and stores it in the CLI's config.
Use one or the other, not both.

### Gotcha: `firecrawl config` misreports env-var auth

With env-var auth, `firecrawl config` always prints this **contradictory-looking but
correct** output:

```
Status: ✓ Authenticated
API Key:  Not set
```

The `Status` line reflects env-var-or-file; the `API Key` line reflects the **stored
config file only**. Env-var users see `Authenticated` + `Not set` forever. Likewise
`firecrawl logout` prints "No credentials found. You are not logged in." — it clears the
file and cannot touch the environment.

**Never diagnose auth from `firecrawl config`.** Verify with an actual scrape:

```bash
firecrawl scrape "https://example.com" -o /tmp/fc-test.md; echo "exit=$?"
```

Exit 0 with real content in the file = auth is fine, whatever the config panel says.

### Usage

```bash
# Basic scrape → markdown, written to a file (never bare stdout)
firecrawl scrape "<URL>" --only-main-content -o /tmp/page.md

# JS-rendered page: give it time to settle
firecrawl scrape "<URL>" --only-main-content --wait-for 3000 -o /tmp/page.md

# Narrow to the content that matters (cheaper to read back)
firecrawl scrape "<URL>" --include-tags article,main -o /tmp/page.md
firecrawl scrape "<URL>" --exclude-tags nav,aside,footer -o /tmp/page.md

# Escalation retry when still blocked — costs more credits, use deliberately
firecrawl scrape "<URL>" --proxy auto --only-main-content -o /tmp/page.md
```

Then read a bounded slice of `/tmp/page.md` (Read with `limit`, or `head`), not the
whole file blind.

Useful extras: `--format links` (all links), `--format summary` (AI summary),
`--screenshot`, `--schema-file` (structured extraction against a JSON schema),
`--max-age <ms>` (accept cached content — cheaper and faster on repeat fetches).

Notes:
- Check availability with `firecrawl --version`.
- Multiple URLs can be passed at once and are scraped concurrently, each saved under `.firecrawl/` — handy for batches, but mind where that directory lands.
- This rung **bills per call**. Always flag to the user when firecrawl is what worked.

---

## Failure signals — when to climb

A rung has **failed** (climb to the next) when the output shows any of:

- **Empty / near-empty body** — fewer than a couple sentences of real content for a page that should have an article.
- **HTTP block** — `403`, `401`, `429`, `503`, Cloudflare/"Just a moment…"/"Attention Required" interstitials, "Access Denied", "Enable JavaScript".
- **Paywall / consent gate** — "Subscribe to read", "Sign in to continue", cookie/consent wall replacing the content, truncated article with a "continue reading" cutoff.
- **JS-required shell** — the response is mostly an empty `<div id="root">`/`<div id="app">` with script tags and no rendered text.
- **CAPTCHA / bot challenge** — "verify you are human", hCaptcha/reCAPTCHA markup.
- **Tool error** — non-zero exit, timeout, DNS/connection error.

When **rung 3 (firecrawl) shows any of these**, the ladder is exhausted → hand off to
`workflows/debug-research.md` with the full log. Do not report failure to the user from
inside the ladder.

## Error-log format

Carry a running log across rungs and into debug-research:

```
- defuddle:  <result — empty body / 403 / binary missing / ok>
- crawl4ai:  <result — include whether the retry was used>
- firecrawl: <result — include whether --proxy auto was tried>
```

---

# Debug-research toolbox (NOT ladder rungs)

These were rungs in the old five-step ladder. They didn't earn a fixed slot — the ladder
tried them by rote and they rarely added anything crawl4ai hadn't already settled. They
remain available to `debug-research.md`, which picks them **on a diagnosis** rather than
in sequence.

**playwright-cli** — plain stock-Chromium render. Reach for it on the specific diagnosis
that a site blocks patchright but not vanilla Chromium (rare, but real). Pattern: render
→ dump HTML → re-clean with defuddle.

```bash
playwright-cli open "<URL>" --wait-for-load --dump-html > page.html
defuddle parse page.html --md
```

**WebFetch** — the native fetch tool. Occasionally useful when a page needs an
LLM-directed extraction rather than a clean-article dump, but it fails on essentially the
same pages defuddle does, which is why it left the ladder.

**browser-act** (UNTESTED) — anti-detection browser CLI with captcha bypass, sessions,
proxies, and human-in-the-loop assist. The only tool here that can solve a captcha or
hand the user the wheel. Read `references/browser-act.md` before invoking — it has the
mandatory `get-skills core` bootstrap and the Confirmation Gate rules.

```bash
browser-act get-skills core --skill-version 2.0.2   # mandatory, don't truncate
browser-act stealth-extract "<URL>"                  # cheap path, no session
```

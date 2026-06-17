# Tool Cheatsheet

Exact invocations for each rung of the ladder, and the signal patterns that mean a rung **failed** and you must climb to the next one. Read by `fetch-ladder.md` and `debug-research.md`.

---

## Rung 1 — defuddle (internalized)

`defuddle` is a CLI that extracts the main article content from a URL or HTML file and returns clean markdown, stripping nav/ads/sidebars. It is the cheapest rung for token usage — prefer it first.

```bash
# From a live URL (defuddle fetches it itself):
defuddle parse "<URL>" --md

# If you already have HTML on disk (e.g. playwright dumped it):
defuddle parse page.html --md

# Markdown is the default for most builds; if --md is unsupported, drop it.
defuddle parse "<URL>"
```

Notes:
- Check availability with `defuddle --version`. If the binary is missing, skip this rung and note it in the error log (don't abort the ladder).
- defuddle is best for article/blog/news pages. It is weak on heavily interactive apps, infinite-scroll feeds, and login-walled pages — expect to climb for those.

---

## Rung 2 — webfetch

Use the native WebFetch tool with the URL and a prompt describing what to extract (pass through the user's hint if they gave one, else "the main readable content as markdown").

When to use over defuddle: defuddle returned empty/garbage, or the binary was unavailable.

---

## Rung 3 — crawl4ai (stealth browser)

Drives a headless browser with anti-bot bypass (patchright + magic mode). Use when defuddle and webfetch fail due to JS-rendering or bot challenges. `magic=True` randomizes fingerprints and simulates human behavior; `css_selector` narrows to a section and cuts token cost.

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

print(asyncio.run(fetch("<URL>")))
```

Check availability: `python -c "import crawl4ai"`. Install if missing: `pip install crawl4ai && crawl4ai-setup`.

---

## Rung 4 — playwright-cli

Last-resort browser render — use only when crawl4ai fails (rare; some sites block patchright but not stock Chromium). See the `playwright-cli` skill for full usage. Typical shape:

```bash
# Render the page and dump HTML, then feed the HTML back through defuddle for clean markdown:
playwright-cli open "<URL>" --wait-for-load --dump-html > page.html
defuddle parse page.html --md
```

Adjust to the actual `playwright-cli` interface (consult that skill). The pattern that matters: **render with a real browser → capture HTML → re-clean with defuddle** so you still get token-cheap markdown out the far end.

---

## Rung 5 — browser-act (UNTESTED, last resort)

Heaviest rung: an anti-detection browser CLI with captcha bypass, sessions, proxies, and human-in-the-loop assist. **Untested in this skill** — only runs after every rung above fails, and falls through to debug-research if it misbehaves. Full instructions, the mandatory `get-skills core` bootstrap, and the Confirmation Gate rules are in `references/browser-act.md` — **read that before invoking.**

```bash
# Mandatory first — do NOT skip or truncate (carries operational directives):
browser-act get-skills core --skill-version 2.0.2

# Cheap path: anti-detection content fetch, no browser session, no confirmation:
browser-act stealth-extract "<URL>"

# Escalate to a full session ONLY with user confirmation (Confirmation Gate):
#   browser-act browser create ... ; browser-act --session NAME browser open <id> "<URL>"
#   browser-act --session NAME get markdown / solve-captcha / remote-assist
```

When to use over playwright-cli: the page survives a stock-Chromium render (hard bot wall, captcha gate, or login-walled app) and you need stealth/captcha/human-assist. See `references/browser-act.md` for the escalation sequence.

---

## Failure signals — when to climb

A rung has **failed** (climb to the next) when the output shows any of:

- **Empty / near-empty body** — fewer than a couple sentences of real content for a page that should have an article.
- **HTTP block** — `403`, `401`, `429`, `503`, Cloudflare/"Just a moment…"/"Attention Required" interstitials, "Access Denied", "Enable JavaScript".
- **Paywall / consent gate** — "Subscribe to read", "Sign in to continue", cookie/consent wall replacing the content, truncated article with a "continue reading" cutoff.
- **JS-required shell** — the response is mostly an empty `<div id="root">`/`<div id="app">` with script tags and no rendered text.
- **CAPTCHA / bot challenge** — "verify you are human", hCaptcha/reCAPTCHA markup.
- **Tool error** — non-zero exit, timeout, DNS/connection error.

When the **top rung (browser-act, the untested last resort) shows any of these** — or simply errors, since it's unproven — the ladder is exhausted → hand off to `workflows/debug-research.md` with the full log. Do not report failure to the user from inside the ladder.

## Error-log format

Carry a running log across rungs and into debug-research:

```
- defuddle: <result — empty body / 403 / binary missing / ok>
- webfetch: <result>
- crawl4ai: <result>
- playwright-cli: <result>
- browser-act: <result — untested rung>
```

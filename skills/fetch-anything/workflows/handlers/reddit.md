# Reddit Handler

Fetches Reddit posts, comment threads, and listings as clean markdown. Reddit's public `.json` API is now frequently blocked (403), so this handler escalates: `.json` attempt first (cheapest), then the **Wayback Machine's archived copy** (free, no install, and the path that actually worked in 2026-09), then crawl4ai with stealth browser rendering on `old.reddit.com`, then firecrawl.

## Contents

- Step 1 — No-auth: the `.json` endpoint
- Step 2 — Free fallback: the Wayback Machine's archived copy
- Step 3 — Fallback: crawl4ai stealth browser
- Step 4 — Fallback: firecrawl (paid)
- Step 5 — Deliver
- Step 6 — Escalate to debug-research
- Done

The constant across every path is **`old.reddit.com`** — its flat server-rendered HTML is
far easier to parse than the new SPA, so rewrite the host before any render attempt.

**Inputs:** a `reddit.com` / `redd.it` URL; optionally a hint ("just the top comments", "the post body only").
**Prerequisites:** none for the `.json` path. crawl4ai path needs `crawl4ai` installed (see Step 3); firecrawl path needs the CLI + API key (see Step 4).

---

## Step 1 — No-auth: the `.json` endpoint

**Goal:** Get structured post + comments with zero setup.

1. Normalize the URL: strip tracking params; ensure it points at a post or listing.
2. Append `.json` to the path and fetch it via `curl` with a real User-Agent header:
   ```bash
   curl -s -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
     "https://www.reddit.com/r/<sub>/comments/<id>/<slug>.json"
   ```
   - Post: `https://www.reddit.com/r/<sub>/comments/<id>/<slug>.json`
   - Listing: `https://www.reddit.com/r/<sub>/top.json?t=week`
3. Parse the JSON: for a post, take `data.children[0].data` (title, selftext, author, score, url); for comments, walk the second listing's `data.children[*].data` (author, body, score, replies).
4. Render to markdown: post title as H1, body, then comments as a nested list with author + score. Apply the user's hint to narrow if given.
5. If the JSON came back (HTTP 200, valid body) → go to Step 5. If blocked (`429`, `403`, empty, HTML challenge) → log it and go to Step 2.

**Output:** markdown (success) or an appended error-log line (failure).

---

## Step 2 — Free fallback: the Wayback Machine's archived copy

**Goal:** Read the thread from archive.org when Reddit blocks live access. As of 2026-09 the live paths are all failing (`.json` 403, crawl4ai hits a login wall on old.reddit, firecrawl reports Reddit unsupported), while archived copies fetch cleanly. Archived content can be stale (missing the newest comments), which is fine for pain-point research and wrong for "what's happening this week".

1. Ask the availability API for the closest snapshot. Try the `old.reddit.com` form first (flat HTML), then `www.reddit.com`:
   ```bash
   curl -s "https://archive.org/wayback/available?url=old.reddit.com/r/<sub>/comments/<id>/<slug>/"
   ```
   The JSON's `archived_snapshots.closest.url` + `.timestamp` is the snapshot. Empty `archived_snapshots` → try the other host, then go to Step 3.
2. Fetch the **raw** archived page by inserting `id_` after the timestamp (drops the Wayback toolbar and URL rewriting). `--compressed` matters because archive.org serves gzip:
   ```bash
   curl -sL --compressed -A "Mozilla/5.0" \
     "https://web.archive.org/web/<timestamp>id_/https://old.reddit.com/r/<sub>/comments/<id>/<slug>/" -o /tmp/reddit.html
   ```
3. Parse it like live old.reddit: posts are `.thing` rows (`a.title` = post title), and comments are `.comment .usertext-body` inside `.sitetable`. Convert to markdown and check a bounded slice against the failure signals.
4. **No thread URL yet?** Reddit search is blocked too. Find threads with web search (`firecrawl search "site:reddit.com <topic>"` or the native search tool), then run steps 1–3 on each hit. A subreddit's front page (`old.reddit.com/r/<sub>/`) is usually archived often, and it lists recent thread URLs.
5. Real content → go to Step 5 and note in delivery that it came from an archived snapshot (give the timestamp). No snapshot or empty → log it and go to Step 3.

**Output:** markdown (success) or an appended error-log line (failure).

---

## Step 3 — Fallback: crawl4ai stealth browser

**Goal:** Render the page with an anti-bot-aware browser when the API is blocked.

1. Check `crawl4ai` is installed (`python -c "import crawl4ai"`). If not: `pip install crawl4ai && crawl4ai-setup`.
2. Convert the URL to `old.reddit.com` (simpler HTML than the new SPA):
   - Replace `www.reddit.com` or `redd.it` with `old.reddit.com` in the URL.
3. Run this Python snippet:
   ```python
   import asyncio
   from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

   async def fetch_reddit(url: str, css_selector: str) -> str:
       browser_cfg = BrowserConfig(browser_type="chromium", headless=True)
       run_cfg = CrawlerRunConfig(
           magic=True,
           simulate_user=True,
           wait_until="networkidle",
           page_timeout=30000,
           css_selector=css_selector,
       )
       async with AsyncWebCrawler(config=browser_cfg) as crawler:
           result = await crawler.arun(url=url, config=run_cfg)
           if not result.success:
               return f"Error: {result.error_message}"
           return result.markdown

   # For a post/thread: target the main content table
   # For a listing: target the post listing table
   selector = ".sitetable"  # works for both threads and listings
   print(asyncio.run(fetch_reddit(url, selector)))
   ```
4. The resulting markdown will contain post body + comments (thread) or ranked post list (listing). Parse out the user's hint if given.
5. If crawl4ai returns real content → go to Step 5. If it fails → log it and go to Step 4.

**Output:** markdown (success) or an appended error-log line (failure).

---

## Step 4 — Fallback: firecrawl (paid)

**Goal:** Let a hosted scraper with its own proxy pool take the page when the local
stealth browser is IP-blocked or rate-limited — the usual Reddit failure mode.

1. Confirm the CLI exists (`firecrawl --version`). If missing, log it and go to Step 6.
2. Keep the `old.reddit.com` rewrite from Step 3 — old Reddit's flat HTML is easier for
   any scraper, and firecrawl is no exception.
   ```bash
   firecrawl scrape "https://old.reddit.com/r/<sub>/comments/<id>/<slug>/" \
     --include-tags .sitetable --only-main-content -o /tmp/reddit.md
   ```
3. Read a bounded slice of `/tmp/reddit.md` to check it against the failure signals.
4. If still blocked, retry **once** with `--proxy auto`.
5. If real content → go to Step 5. Otherwise log it and go to Step 6.

Reddit rate-limits by IP, so this rung is more likely to pay off here than on a typical
site. It also bills per call — flag it in the delivery note.

**Output:** markdown (success) or an appended error-log line (failure).

---

## Step 5 — Deliver

**Goal:** Hand over clean Reddit content.

1. Return the markdown, narrowed to the user's hint if given.
2. Note which path worked only if relevant (e.g. "API was blocked, used crawl4ai on old.reddit.com"). Always say so if firecrawl was what worked — it bills per call.

**Output:** final content to the user. Workflow ends.

---

## Step 6 — Escalate to debug-research

**Goal:** Don't quit on Reddit.

1. Do NOT say Reddit can't be accessed.
2. Read `workflows/debug-research.md`, passing the URL, hint, and the full error log (the `.json`, Wayback, crawl4ai, and firecrawl failures). It will hunt for a workaround — pushshift-style mirrors, alternate hosts, header/UA tweaks, or a proxy.

**Output:** control passes to debug-research.

---

## Done

This workflow is complete when:
- [ ] The user has the post/comments as markdown, OR
- [ ] Control was handed to `debug-research.md` with all three failure paths logged.

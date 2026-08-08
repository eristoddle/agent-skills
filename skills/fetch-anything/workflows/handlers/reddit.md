# Reddit Handler

Fetches Reddit posts, comment threads, and listings as clean markdown. Reddit's public `.json` API is now frequently blocked (403), so this handler escalates: `.json` attempt first (cheapest), then crawl4ai with stealth browser rendering on `old.reddit.com`, then firecrawl.

The constant across every path is **`old.reddit.com`** — its flat server-rendered HTML is
far easier to parse than the new SPA, so rewrite the host before any render attempt.

**Inputs:** a `reddit.com` / `redd.it` URL; optionally a hint ("just the top comments", "the post body only").
**Prerequisites:** none for the `.json` path. crawl4ai path needs `crawl4ai` installed (see Step 2); firecrawl path needs the CLI + API key (see Step 3).

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
5. If the JSON came back (HTTP 200, valid body) → go to Step 3. If blocked (`429`, `403`, empty, HTML challenge) → log it and go to Step 2.

**Output:** markdown (success) or an appended error-log line (failure).

---

## Step 2 — Fallback: crawl4ai stealth browser

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
5. If crawl4ai returns real content → go to Step 4. If it fails → log it and go to Step 3.

**Output:** markdown (success) or an appended error-log line (failure).

---

## Step 3 — Fallback: firecrawl (paid)

**Goal:** Let a hosted scraper with its own proxy pool take the page when the local
stealth browser is IP-blocked or rate-limited — the usual Reddit failure mode.

1. Confirm the CLI exists (`firecrawl --version`). If missing, log it and go to Step 5.
2. Keep the `old.reddit.com` rewrite from Step 2 — old Reddit's flat HTML is easier for
   any scraper, and firecrawl is no exception.
   ```bash
   firecrawl scrape "https://old.reddit.com/r/<sub>/comments/<id>/<slug>/" \
     --include-tags .sitetable --only-main-content -o /tmp/reddit.md
   ```
3. Read a bounded slice of `/tmp/reddit.md` to check it against the failure signals.
4. If still blocked, retry **once** with `--proxy auto`.
5. If real content → go to Step 4. Otherwise log it and go to Step 5.

Reddit rate-limits by IP, so this rung is more likely to pay off here than on a typical
site. It also bills per call — flag it in the delivery note.

**Output:** markdown (success) or an appended error-log line (failure).

---

## Step 4 — Deliver

**Goal:** Hand over clean Reddit content.

1. Return the markdown, narrowed to the user's hint if given.
2. Note which path worked only if relevant (e.g. "API was blocked, used crawl4ai on old.reddit.com"). Always say so if firecrawl was what worked — it bills per call.

**Output:** final content to the user. Workflow ends.

---

## Step 5 — Escalate to debug-research

**Goal:** Don't quit on Reddit.

1. Do NOT say Reddit can't be accessed.
2. Read `workflows/debug-research.md`, passing the URL, hint, and the full error log (the `.json`, crawl4ai, and firecrawl failures). It will hunt for a workaround — pushshift-style mirrors, alternate hosts, header/UA tweaks, or a proxy.

**Output:** control passes to debug-research.

---

## Done

This workflow is complete when:
- [ ] The user has the post/comments as markdown, OR
- [ ] Control was handed to `debug-research.md` with all three failure paths logged.

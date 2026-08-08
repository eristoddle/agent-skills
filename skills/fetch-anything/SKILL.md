---
name: fetch-anything
description: |
  Fetches any web URL and returns clean markdown by escalating through defuddle → crawl4ai → firecrawl, with lazy-loaded per-domain handlers for sites that need special treatment.
  Use this skill whenever the user wants a page retrieved or its content read: "fetch this URL", "scrape this page", "get this article", "read this link", "grab this Reddit thread", "extract the content from", "this page is blocking me", "webfetch got rejected", or any time a plain fetch was refused or returned junk.
  Do NOT trigger for pure web *search* with no specific URL to retrieve — that path already works with the native search tool. This skill is for turning a known URL into usable content.
---

<essential_principles>

## What This Skill Does

Turns a known URL into clean, token-cheap markdown. It is a **three-rung escalation ladder** — defuddle → crawl4ai → firecrawl — trying the cheapest reliable method first and climbing only when a rung actually fails. It is NOT a search engine and NOT a one-shot wrapper around a single tool.

## Core Rules

1. **Never declare a fetch impossible.** A terminal failure is not an answer — it routes to `workflows/debug-research.md`, which finds a workaround or proposes a new handler. "Can't be scraped" is a bug in this skill, not a fact.
2. **Three rungs, in cost order.** defuddle (free, cheapest tokens) → crawl4ai (free, highest success rate — the workhorse) → firecrawl (paid API, the backstop). Climb only on real failure, and say so when the paid rung is what worked.
3. **Bounded output, always.** Write fetched pages to a file and read a bounded slice; never let a full page render into the transcript. A single large page can end a session.
4. **A failure carries its error forward.** Every rung that fails appends its actual error to a running log that the next rung — and ultimately debug-research — receives.
5. **Extend, don't fork.** New site needs special handling? Add a row to `references/handler-registry.md` and one file under `workflows/handlers/`. The router and ladder never change.

</essential_principles>

<intake>

I need a URL. If the user gave one, use it. If they described a page without a URL, ask for the exact link.

Once I have the URL, inspect it and route immediately — no menu, no confirmation:

1. Read `references/handler-registry.md`. If the URL's domain matches a registered handler, load that handler workflow (e.g. `workflows/handlers/reddit.md`) and follow it.
2. If no handler matches, go to `workflows/fetch-ladder.md`.
3. If the chosen path exhausts every rung and still fails, go to `workflows/debug-research.md` with the URL and the accumulated error log.

Capture an optional hint if the user gave one ("just the comments", "the main article body", "the price table") and pass it through as the extraction target.

</intake>

<instructions>

## Workflow Routing

### If the URL's domain matches a row in `references/handler-registry.md`:
Read the handler file named in that row (e.g. `workflows/handlers/reddit.md`) and follow it exactly. If the handler itself fails terminally, proceed to `workflows/debug-research.md`.

### If no handler matches:
Read `workflows/fetch-ladder.md` and follow it. It climbs defuddle → crawl4ai → firecrawl, using the signal patterns in `references/tool-cheatsheet.md` to decide when a rung has failed.

### If any path exhausts every rung:
Read `workflows/debug-research.md` with the URL and the full error log. It diagnoses the real cause, researches a workaround (hidden API, headers, alternate host, archive, proxy), and either retrieves the content or proposes a concrete new handler to register. Its toolbox includes playwright-cli and browser-act — former ladder rungs, now selected on a diagnosis rather than tried by rote.

## One-time setup: firecrawl (rung 3)

Rung 3 needs a Firecrawl account and the **CLI, not the MCP server**. The free tier is
1,000 credits/month (no card), which is far more than this skill will ever burn — sign up
at https://firecrawl.link/stephan-miller.

```bash
npm install -g firecrawl-cli
```

Do **not** use the `curl … install.sh` one-liner or `firecrawl init` — those push
Firecrawl's own agent skills, and optionally its MCP server, into every detected editor.
This skill drives the CLI directly.

The key comes from `FIRECRAWL_API_KEY` in the environment (or `firecrawl login --api-key fc-...`,
which stores it in the CLI's own config). If the rung reports a missing key, tell the user
the permanent fish command — `set -Ux FIRECRAWL_API_KEY fc-...` — not a session-only `set -x`.

## Reference Materials

- `references/handler-registry.md` — domain → handler-file lookup. Read at intake to decide routing. This is the extension point: add a row to register a new custom handler.
- `references/tool-cheatsheet.md` — exact invocations for all three rungs, the bounded-output rules, the "blocked / rejected / paywall / JS-required" signal patterns that mean a rung failed, and the debug-research toolbox (playwright-cli, WebFetch, browser-act). Read by `fetch-ladder.md` and `debug-research.md`.
- `references/browser-act.md` — bootstrap + Confirmation Gate rules for browser-act. Read only if debug-research selects it.

## Quality Checklist

The skill is done when:
- [ ] The user has the page content as clean markdown (or, for handler cases, the structured content they asked for).
- [ ] The cheapest rung that worked was used — no reaching for paid firecrawl when defuddle or crawl4ai would do.
- [ ] Nothing dumped a full page into the transcript — fetches went to files, reads were bounded.
- [ ] If firecrawl was what worked, the user was told (it bills per call).
- [ ] If anything failed, the failure was diagnosed and either worked around or turned into a concrete handler proposal — never a flat "it can't be done."

</instructions>

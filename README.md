# Agent Skills

A small, curated set of agent skills for AI coding tools: Claude Code, Codex, Cursor, OpenCode, GitHub Copilot, Gemini CLI, and anything else that reads the open `SKILL.md` standard.

Two things make this set different from most skill packs:

1. **Every skill is standalone.** Nothing here depends on anything else here. Grab the one folder you want, drop it in, done. You never have to take the whole pile to get one thing working.
2. **These are the ones I actually reach for.** They're a mirror of a slice of my personal shelf, cut down for sharing. I wrote about how I build and maintain skills in [The Agent Skills Guide I Wish I'd Had](https://www.stephanmiller.com/the-agent-skills-guide-i-wish-id-had/).

## What's a skill?

A skill is a folder with a `SKILL.md` inside: a little YAML frontmatter (a `name` and a `description`) on top, plain-markdown instructions underneath. The agent reads the description, decides on its own whether the skill is relevant to what you're doing, and loads the full thing only when it is. Conditionally loaded context. The long version is in [the guide](https://www.stephanmiller.com/the-agent-skills-guide-i-wish-id-had/).

## Install

Each skill is a self-contained folder under [`skills/`](./skills). To use one, copy its folder into your agent's skills directory:

| Tool | Drop the folder in |
|---|---|
| Claude Code | `.claude/skills/` (project) or `~/.claude/skills/` (global) |
| Codex | `.agents/skills/` |
| Cursor | `.cursor/skills/` or `.agents/skills/` |
| OpenCode | `.opencode/skills/`, `.claude/skills/`, or `.agents/skills/` |
| GitHub Copilot | `.github/skills/`, `.claude/skills/`, or `~/.copilot/skills/` |
| Gemini CLI | `.gemini/skills/` or `~/.gemini/skills/` |

For example, to use a skill in Claude Code globally:

```bash
git clone https://github.com/eristoddle/agent-skills.git
cp -r agent-skills/skills/<skill-name> ~/.claude/skills/
```

Or, if you manage skills across tools with [skillshare](https://github.com/runkids/skillshare):

```bash
skillshare install https://github.com/eristoddle/agent-skills
```

## Skills

### [fetch-anything](./skills/fetch-anything)

Turns a known URL into clean markdown, and refuses to accept "this page can't be scraped" as an answer. It climbs a three-rung ladder in cost order — [defuddle](https://github.com/kepano/defuddle) (free, cheapest tokens) → [crawl4ai](https://github.com/unclecode/crawl4ai) (free stealth browser, the workhorse) → [Firecrawl](https://firecrawl.link/stephan-miller) (hosted API, the paid backstop) — and only climbs when a rung actually fails, which it decides by pattern-matching the response for block pages, paywalls, login walls, and empty JS shells. If all three rungs are exhausted it doesn't report failure; it drops into a debug step that diagnoses the page and then picks a tool to match the diagnosis. Sites that need special treatment get a per-domain handler instead of a guess: Reddit ships as one, because you don't fight reddit.com, you quietly fetch `old.reddit.com` and take the clean HTML it still serves. Every fetch is written to a file and read back in bounded slices, so a 400KB page can't blow up your context.

**Reach for it when:** a page blocks you, a plain fetch returns junk, or you need a known URL turned into usable content while you're in the middle of something else.

### [skill-hardener](./skills/skill-hardener)

Mines your recent Claude Code transcripts for the mistakes your agent keeps making, traces each pattern back to the skill (or `CLAUDE.md` rule) responsible, and writes a targeted guardrail plus a regression test that proves the fix and catches the backslide. It's the diagnostic complement to a skill *creator*: it decides what to harden and why, using evidence from sessions you actually ran instead of your guess about what went wrong.

**Reach for it when:** the same friction keeps coming back, or your skills are quietly degrading and you want the fix driven by real history.

### [modular-skill-creator](./skills/modular-skill-creator)

Builds a skill — or converts one you already have — as a lazy-loading router: a thin `SKILL.md` under ~150 lines that holds only frontmatter, principles, and routing rules, delegating the actual prose to self-contained files under `workflows/` and `references/` that load only when they're needed. That's the difference between a skill that costs you a few hundred tokens to have available and one that costs you several thousand every time it triggers.

**Reach for it when:** you're authoring a skill with more than one distinct path through it, or splitting a monolith that's gotten expensive to load.

### [verbalized-sampling](./skills/verbalized-sampling)

A skill version of the [Verbalized Sampling](https://www.verbalized-sampling.com/) technique ([paper](https://arxiv.org/abs/2510.01171)). Instead of the single safest answer, it asks the model for several candidates *with explicit probabilities attached*, which sidesteps the mode collapse that makes AI brainstorms come back samey — the same five ideas everybody else's agent also produced. Training-free, no tooling, and it applies itself when it detects ideation rather than waiting to be summoned.

**Reach for it when:** you want real options out of brainstorming, naming, or creative work, not the most-likely one.

## Requirements

Three of these are pure-prompt skills with no external dependencies: drop the folder in and they work.

The exception is **fetch-anything**, which drives real tools. It degrades gracefully — it checks each one and skips any that's missing — so it does something useful with nothing installed, but the ladder is only as good as the rungs you give it. For the full thing:

- **defuddle** — rung 1, clean article extraction to markdown, no browser. [kepano/defuddle](https://github.com/kepano/defuddle): `npm install -g defuddle` (or let the skill run it on demand with `npx defuddle parse <url>`).
- **crawl4ai** — rung 2, the stealth-browser workhorse where most of the real success rate lives. [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai): `pip install crawl4ai && crawl4ai-setup`.
- **Firecrawl** — rung 3, the hosted backstop that handles rendering, proxy rotation, and blocking on somebody else's machine. [Sign up here](https://firecrawl.link/stephan-miller) (affiliate link), then `npm install -g firecrawl-cli` and put the key in `FIRECRAWL_API_KEY`.

On Firecrawl specifically, two notes.

The free tier is 1,000 credits a month — a thousand scrapes, no credit card, reset every month. That's the real selling point here, because of what this skill is for. It isn't a crawler grinding through a sitemap overnight; it's the thing an agent reaches for when *one* page won't open while you're busy doing something else.

Install it with plain `npm install -g firecrawl-cli`. **Not** the `curl … install.sh` one-liner, and **not** `firecrawl init` — those push Firecrawl's own agent skills, and optionally its MCP server, into every editor they can detect on your machine. This skill drives the CLI directly and wants none of that. (Also: `firecrawl config` reports `Status: ✓ Authenticated` and `API Key: Not set` at the same time when you authenticate by env var. Both lines are correct and you should ignore the panel entirely — verify auth by running an actual scrape.)

Two more tools sit *below* the ladder, in the debug step that only runs after all three rungs are exhausted. Neither is required, and neither is tried by rote — the skill diagnoses the page first and reaches for one only if the diagnosis calls for it:

- **playwright-cli** — a stock-Chromium render, for the specific case where a site blocks patchright but not vanilla Chromium. [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli): `npm install -g @playwright/cli@latest`.
- **browser-act** — captcha solving, proxies, persistent sessions, and a hand-the-user-the-wheel mode. [browser-act/skills](https://github.com/browser-act/skills). Fair warning: in two months of use it was invoked zero times, and I still haven't tested it.

## Compatibility

Everything here follows the open `SKILL.md` standard, so the same folder works unmodified across the tools above. Nothing is Claude-Code-specific.

## License

MIT. See [LICENSE](./LICENSE). Use them, fork them, ship them.

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

### [ebook-research](./skills/ebook-research)

Researches a topic against your own ebook library instead of the web, for the cases where a real author spent 300 pages on what a blog post covers in 800 words. It drives a local [Recoll](https://www.recoll.org) index through a four-level ladder: which books cover the subject, where inside the book, the actual prose, and then a cited synthesis. It never quotes a search snippet, because snippets are ~40-character fragments that misquote the author. All output goes through a bundled stdlib-only Python script that caps what it prints and caches full extractions to disk, so a 600KB PDF can't blow up your context. It also knows its limits: for anything current (releases, versions, news) it sends you to the web, and if your library has nothing good on a topic it says so instead of stretching a weak book into a citation.

**Reach for it when:** you want depth rather than recency: philosophy, craft, history, psychology, "the theory behind X", or a real source to back up a claim.

### [angle-board](./skills/angle-board)

Turns one piece of raw material — a coding session, a research file, a topic, a pile of notes, or a single how-to — into a pyramid of distinct article angles instead of one obvious post. It walks a five-rung altitude ladder (weeds → tutorial → story → practice → thesis), gives each angle its own lens and a named reader in a specific moment, rates the evidence behind it, then designates a pillar and spokes that each carry a "don't restate" constraint so four posts off one session don't cannibalize each other. The rule that makes it honest: altitude has an evidence requirement. One session can only support the bottom of the pyramid, so a thesis needs three independent proof points from across your notes, and an empty rung is reported as empty instead of padded with a confident-sounding take. A second mode inverts one *how* into many *whys* (payoff, actor, signal) to fan a single technique into use-case posts. The board is saved as a plain markdown checklist, and the skill stops at briefs; it never writes the article.

**Reach for it when:** you finish a project or research pass and suspect there's more than one post in it, or you want a backlog of article ideas with real evidence behind each.

### [living-plan](./skills/living-plan)

Owns the whole lifecycle of a project's planning docs: a hot, lean `PLAN.md` that's cheap enough to carry every session, a `TASKS.md` handoff contract, and an implementer agent that works the queue. It detects which state your project is in and routes to one of five actions. Four of them reshape what's already there — **scaffold** a fresh project, **adopt** the missing pieces into one that already half-does this, **rebalance** a bloated plan by relocating cooled material (old session logs, settled decisions, futures, reference) into linked `docs/` files and leaving one-line pointers behind, **evict** the finished task queues out of a `TASKS.md` that's quietly become an append-only log. The fifth, **grill**, is different in kind: it interviews you round by round until the design tree has actually been visited, and writes the answers into the decision record. That's the one that fixes the real failure — a decision record that records nothing, because scaffolding a project asks "what is this?" once and then never asks again. Greenfield now runs grill first, so the plan is born populated. It's portable across projects and tolerant of naming variance (`TASKS.md` vs `TASK.md`, `CLAUDE.md` vs `AGENTS.md`), every mutating step is propose-then-confirm with a manifest, and the process itself lazy-loads out of `workflows/` so the planning agent stays light. Formerly named `plan-rebalance`; that name still routes here. For how I use it in practice, see [Two Files and a Skill: How I Plan AI Coding Projects Without a Framework](https://www.stephanmiller.com/two-files-and-a-skill-how-i-plan-ai-coding-projects-without-a-framework/).

**Reach for it when:** `PLAN.md` has gotten heavy to read every session, `TASKS.md` is 90% checked boxes, you're starting something and don't know its shape yet, or you want someone to poke holes in a design before you build it.

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

Four of these are pure-prompt skills with no external dependencies: drop the folder in and they work (**angle-board**, **living-plan**, **modular-skill-creator**, **verbalized-sampling**).

**ebook-research** needs [Recoll](https://www.recoll.org) installed and an index built over your ebook folder (macOS DMG or `apt install recoll` on Linux; indexing a big library is slow, so run `recollindex` yourself). Its script is stdlib-only Python.

**skill-hardener** ships two Python scripts (standard library only, so `python3` is all you need) that read Claude Code session transcripts from `~/.claude/projects`.

The last exception is **fetch-anything**, which drives real tools. It degrades gracefully — it checks each one and skips any that's missing — so it does something useful with nothing installed, but the ladder is only as good as the rungs you give it. For the full thing:

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

Everything here follows the open `SKILL.md` standard, so the same folder loads unmodified across the tools above. Two things lean toward Claude Code: **skill-hardener** mines Claude Code's transcript format, so it only has material to work with there, and two skills mention Claude Code conventions: **modular-skill-creator** uses `AskUserQuestion` and **living-plan** looks in `.claude/agents/` (it also checks for the tool's own agent directory), which other tools will treat as plain instructions or substitute with their own equivalent.

## License

MIT. See [LICENSE](./LICENSE). Use them, fork them, ship them.

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

| Skill | What it does | Reach for it when |
|---|---|---|
| [fetch-anything](./skills/fetch-anything) | Climbs a ladder of fetch tools (defuddle → WebFetch → crawl4ai → playwright-cli → browser-act) until one returns the page as clean markdown. Refuses to accept "it can't be scraped." | A page blocks you, a plain fetch returns junk, or you need a known URL turned into usable content. |
| [skill-hardener](./skills/skill-hardener) | Mines your recent Claude Code transcripts for recurring failure patterns, traces each back to the skill responsible, and adds a targeted guardrail plus a regression test. | Your skills are quietly degrading and you want to fix repeat mistakes using real history, not guesses. |
| [modular-skill-creator](./skills/modular-skill-creator) | Builds (or converts) a skill as a lazy-loading router: a thin `SKILL.md` that delegates to focused sub-workflows instead of one fat file. | You're authoring a multi-workflow skill, or splitting a monolith so it stays cheap to load. |
| [verbalized-sampling](./skills/verbalized-sampling) | Asks the model for several candidate answers with explicit probabilities instead of its single safest response, sidestepping the mode collapse that makes AI brainstorms samey. | You want real options out of brainstorming or creative work, not the most-likely one. |

## Requirements

Three of these are pure-prompt skills with no external dependencies: drop the folder in and they work. The exception is **fetch-anything**, which drives a ladder of external fetch tools.

It degrades gracefully (it checks each tool and skips any that's missing), so with nothing installed it falls back to the agent's built-in `WebFetch`. For the full ladder, install:

- **defuddle** — CLI for the cheapest rung (clean article extraction to markdown). Checked via `defuddle --version`.
- **crawl4ai** — the stealth-browser rung: `pip install crawl4ai && crawl4ai-setup`.
- **playwright-cli** — last-resort real-browser render (also published as its own skill).
- **browser-act** — optional heaviest rung (captcha/proxy/human-assist); untested in the skill, only reached after everything else fails.

`WebFetch` (rung 2) is a built-in agent tool, so no install needed there.

## Compatibility

Everything here follows the open `SKILL.md` standard, so the same folder works unmodified across the tools above. Nothing is Claude-Code-specific.

## License

MIT. See [LICENSE](./LICENSE). Use them, fork them, ship them.

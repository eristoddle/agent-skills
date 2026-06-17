---
name: modular-skill-creator
description: Build or convert skills into a modular, lazy-loading multi-workflow architecture. Use for "modular skill", "router skill", or splitting a monolithic skill into sub-workflows. For simple single-file skills, use skill-creator instead.
---

<essential_principles>

## Architecture This Skill Produces

Every modular skill has three layers:

1. **Router (`SKILL.md`)** — loaded at invocation, under ~150 lines. Contains frontmatter, essential principles, intake logic, and routing rules only. No workflow prose lives here.

2. **Workflows (`workflows/*.md`)** — loaded on demand when the router decides which branch to execute. Each file is fully self-contained: it states its own inputs, prerequisites, steps, outputs, and done criteria.

3. **References (`references/*.md`)** — single-purpose data files (blacklists, templates, taxonomies, examples). Loaded by workflows when needed. Never contain procedural logic.

## Core Rules

1. **Router stays thin.** If you catch yourself writing multi-step procedure logic in SKILL.md, it belongs in a workflow file.
2. **Each workflow owns its scope.** A workflow file should not need to read another workflow file to complete its job — unless the skill is explicitly a stage-pipeline where step N hands off to step N+1.
3. **References are data, not logic.** A reference file contains lookup tables, lists, templates, or examples. It never says "now do X."
4. **Always ask project vs global.** Per the user's global preference, never assume a save location — always ask before writing files.

</essential_principles>

<intake>

**Before anything else, ask where to save the output skill** using AskUserQuestion:

> "Where should the new skill be saved?"
> - **Project-level** — `./.claude/skills/<skill-name>/` in the current repo (preferred ~75% of the time)
> - **Skillshare global** — `~/.config/skillshare/skills/<skill-name>/` (syncs to all your AI tools via skillshare)

Then ask what the user wants to do:

> "What would you like to do?"
> - **Build a new modular skill** — design it from scratch with router + workflows + references
> - **Convert an existing skill** — refactor a single-file SKILL.md into the modular pattern

Route based on the answer.

</intake>

<instructions>

## Workflow Routing

### If user wants to build a new modular skill:

1. Read `workflows/design-modular-skill.md` — run the interview to produce the skill spec.
2. Read `workflows/scaffold-router.md` — generate the `SKILL.md` router from the spec.
3. Read `workflows/scaffold-workflows.md` — generate each `workflows/*.md` file from the spec.
4. Write all files to the save location confirmed in intake.

### If user wants to convert an existing skill:

Read `workflows/refactor-monolithic-skill.md`. This workflow handles the full refactor end-to-end.

## Reference Materials

- `references/router-patterns.md` — read this during scaffold-router to get the correct template for the chosen routing pattern (menu-driven, input-shape detection, or stage-pipeline)
- `references/frontmatter-conventions.md` — read this to use only fields the user's existing skills use; prevents spurious fields from appearing in generated skills
- `references/examples.md` — read this when you need a concrete canonical example to explain the pattern to the user or sanity-check your output against

## Quality Checklist

Before reporting done:
- [ ] Router SKILL.md is under ~150 lines
- [ ] Router contains zero step-by-step procedure prose
- [ ] Every workflow file is self-contained (inputs, steps, outputs, done criteria all present)
- [ ] No `allowed-tools` field in frontmatter (not part of this user's convention)
- [ ] Description field is pushy and trigger-rich (50-100 words, lists trigger phrases)
- [ ] Save location was confirmed with user before any files were written

</instructions>

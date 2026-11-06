# Workflow: adopt / backfill (partial)

A project already uses the workflow but is missing pieces (the common real case — e.g. has
`PLAN.md` + `TASKS.md` + `AGENTS.md` but no implementer agent, or no `docs/` tree yet).
**Add only what's missing. Touch existing docs only to add pointers. Idempotent — running
twice changes nothing.**

## Step 1 — Diff against the full system

From Step 1 detection, list present vs. missing:

- planning doc ............ present? (don't recreate)
- task doc ................ present? (`TASK.md`/`TASKS.md`)
- conductor blurb ......... does `<conductor>` already describe the planning/implementer
  workflow + mention `living-plan`? (grep for it, and for the old name `plan-rebalance`)
- agent catalog ........... which catalog agents exist in `.claude/agents/` (or the tool's
  agent dir)? Catalog today: `{implementer}`. Missing = backfill candidates.
- docs/ tree ............. do the four subfolders + `docs/rebalance-log.md` exist?
- task mirror ............ does `<conductor>` name an **External task mirror**? (grep for
  it.) Absent is the normal case and not automatically a gap — see below.
- **empty decision record** ... does the planning doc have a `Decisions` section with nothing
  in it, or only the template's `<!-- D1 -->` placeholder? (`grep -c '^### D' <planning-doc>`)
  This is a gap, but not one you backfill — see below.

## Step 2 — Backfill only the gaps (propose-then-confirm)

For each missing piece, propose adding it from `templates/`, with the project's discovered
names substituted:

- Missing **task doc** → create empty from `TASKS.template.md` using the project's chosen
  name (respect `TASK.md` if that's the existing convention).
- Missing **conductor blurb** → append `CLAUDE-blurb.template.md` to the existing conductor
  (append, never rewrite the file).
- Missing **agent(s)** → write each missing catalog agent into the agent dir. For the
  implementer, use `templates/agents/implementer.template.md`, and **fill every placeholder**
  — `{{AGENT}}`, `{{PROJECT}}`, `{{TASK_DOC}}`, `{{MODEL}}`, `{{MODEL_LABEL}}`, `{{TEST_CMD}}`.
  Ask for the model if it isn't obvious; default `sonnet`. **A missing `model:` line is worse
  than an unfilled one** — it silently inherits the host session's model, so the implementer
  runs on the expensive model it exists to avoid, and nothing about the agent looks wrong.
  Verify: `grep '^model:' <agent-file>` must return a real model name.
- **Agent present but no `model:` line** → this is its own drift finding, not a "nothing
  missing." Report it and offer to add one; check the existing agents even when the agent dir
  looks complete.
- Missing **docs/ tree** → create the folders + seed `docs/rebalance-log.md` `## Config`
  with the discovered names + threshold.

- Missing **task mirror** → this one is a **question, not a backfill**. Ask once: "is there
  a copy of this task list outside the repo?" If yes, append the External task mirror
  paragraph from `CLAUDE-blurb.template.md` with the path filled in. If no, say nothing
  further and never propose it again this run — most projects do not have one, and inventing
  a mirror is worse than having none.

- Empty **decision record** → not a backfill; nothing can be written for the user here.
  Mention it once at the end of the report — "the Decisions section is empty; `grill` is what
  fills it" — and let them ask. A project can run fine for a long time with decisions living
  only in the maintainer's head; pushing an interview on someone who came here to add a
  missing agent file is the wrong moment for it.

Show the proposed additions as a list. Wait for approval. Write only approved items.

## The agent catalog is extensible

Don't hardcode "the implementer agent." Backfill = **diff the project's agents against the
catalog, add the missing ones**. To add a future agent type to the catalog, drop a new
`templates/agents/<name>.template.md` into this skill and register its name in the catalog
list above; every project can then adopt it through this same workflow. New agents sync as
plain `.md` files (skillshare handles agent fan-out).

## Step 3 — Report

List what was added and what was already present (skipped). Suggest a commit
(`chore: backfill planning workflow pieces`). Note: after backfilling a `docs/` tree on a
project with a heavy planning doc, offer to run `rebalance` next.

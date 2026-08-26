# Workflow: scaffold (greenfield)

Drop the planning/implementation workflow into a project that has none. **Interview first**,
then emit tailored boilerplate. Never overwrite an existing file — if one is present, this is
the wrong workflow (use `adopt.md`).

## Step 0 — Design first, plumbing second

Scaffold's interview is about **plumbing** — file names, agent names, a mirror. It is
deliberately brief. The *design* comes from `workflows/grill.md`, which runs first on
greenfield and hands over a disposed tree.

- **Arriving from a grill** — you already hold the tree. Skip Q1 below (the Overview and the
  decisions come from the grill), ask only the plumbing questions, and emit a **populated**
  planning doc in Step 2.
- **Arriving cold** — offer it once, in one line: *"Want to grill the design first, or scaffold
  empty docs now?"* Accept "scaffold now" immediately and move on; a grill can run any time
  afterward. Do not pitch it twice.

An empty Decisions section is the default failure mode of this workflow: the doc claims to be
an authoritative decision record while recording nothing, and every real decision then gets
made ad hoc in whatever session collides with it — or silently, by the implementer agent.

## Step 1 — Interview (brief; interpret intent, don't interrogate)

Ask only what you can't infer from the repo:

1. **What is this project?** (one or two sentences — becomes PLAN.md's Overview. Skip if a
   grill already produced it.)
2. **Doc naming preference** — default `PLAN.md` + `TASKS.md` + `CLAUDE.md`. Offer the
   variants you support (`TASK.md`, `AGENTS.md`) if the repo already leans that way
   (e.g. an `AGENTS.md` exists, or it's a non-Claude tool).
3. **Implementer agent?** — almost always yes; confirm the model (default Sonnet) and the
   agent name (default `implementer`).
4. **Any other agents** from the catalog now, or just the implementer? (Catalog today:
   `implementer`. Extensible — see adopt.md.)
5. **Is there an external task mirror?** — a second copy of the task list kept outside the
   repo (a note in a notes app, a shared doc, a tracker export) that gets edited when the
   user is away from the machine. Ask for a path or identifier, and accept "no." Ask it
   **at scaffold time**, because a mirror bolted on later is one nobody remembers exists.

Infer language/build/test commands from the repo where possible; ask only if unclear.

## Step 2 — Emit boilerplate (from `templates/`, with substitutions)

Fill the template placeholders (`{{PROJECT}}`, `{{TASK_DOC}}`, `{{CONDUCTOR}}`,
`{{TEST_CMD}}`, etc.) with interview answers, then write:

- `<planning-doc>` ← `templates/PLAN.template.md` (Overview filled, the `docs/` pointer
  header, the foundational-flag + rebalance-threshold notes). **If a grill preceded this**,
  the Decisions / Questions / Parking Lot sections are written from its disposition rather
  than left empty: decided nodes become `Dxx` records inline (marked `🔨` for work not yet
  built, `🔒` where the grill established a decision is foundational), and open/parked nodes
  become one-line pointers with their thread files written from
  `templates/QUESTION.template.md`. Otherwise those sections start empty as before.
- `<task-doc>` ← `templates/TASKS.template.md` (the handoff contract — the serial-queue
  shape with an empty active task + ✅ Done archive).
- A **blurb appended** to `<conductor>` ← `templates/CLAUDE-blurb.template.md` (the
  planning-vs-implementation workflow + "invoke `living-plan` when the planning doc gets
  heavy"). If no conductor exists, create one with just this blurb.
  **The External task mirror paragraph is conditional:** include it, with `{{MIRROR}}`
  replaced by the answer to interview Q5, only if a mirror was named. If not, delete that
  paragraph outright rather than leaving an unfilled placeholder or an empty promise.
- `.claude/agents/<agent>.md` (or the tool's agent dir) ← `templates/agents/implementer.template.md`.
- `docs/{decisions,questions,parking-lot,sessions}/` empty dirs + an empty
  `docs/rebalance-log.md` seeded with the `## Config` block (recording the chosen names +
  threshold) so future runs are deterministic.

## Step 3 — Confirm + report

Show the file list you're about to create, get approval, write, and report. Suggest the
first commit (`chore: scaffold planning workflow (living-plan)`) but let the user run it.

The **process itself is not copied into the project** — the project gets pointers; the
process stays in this skill. That's deliberate (keeps the project's hot docs light).

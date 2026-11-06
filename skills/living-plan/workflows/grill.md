# Workflow: grill

Interview the user until the design tree has been **visited**. This is the only workflow that
**generates** planning material — the other four reshape what already exists. It fills the
`Decisions`, `Open questions`, and `Parking lot` sections that `scaffold` otherwise creates
empty, and it is the only mechanism that ever moves an item *out* of those cold containers.

## Contents

- When it runs
- Modes
- Step 1 — Seed the tree (Mode B; never start blank)
- Step 2 — Compute the frontier
- Step 3 — Ask the round
- Step 4 — Dispose and record, at every round boundary
- Step 5 — Propose promotions
- Step 6 — Stop
- Invariants

Absorbed from the `grilling` technique, adapted to this skill's containers: grilling ends at a
shared understanding held in the conversation; here that understanding lands in the docs and
survives the session.

**Primary agent only.** The human pause is this workflow's entire contract — in a subagent the
pause is a no-op and the agent answers on the user's behalf. Never dispatch grill itself to a
subagent. (It may dispatch subagents *for facts* — see Step 3.)

## When it runs

Never automatically. Three entries:

- **Phrase trigger** — "grill me", "stress-test this", "poke holes in this", "what am I
  missing", "interrogate this idea".
- **Uncertainty offer** — the user signals they don't know the shape yet: "not sure where this
  is going", "maybe this might work", "I don't know if I should", thinking out loud with no
  question attached. **Offer in one line and wait** — *"Want me to grill this?"* Do not open a
  round. A grill launched at someone who was only thinking out loud is worse than a missed one.
- **Greenfield entry** — no planning doc exists and a project is starting. Grill runs *before*
  `scaffold` and hands it a populated tree (Mode A).

## Modes

**Mode A — greenfield (no planning doc yet).** The tree starts at the root ("what is this, and
what does it have to be true for?"). Nothing is written to a planning doc during the session
because there isn't one — hold the tree in session, and at the end hand the whole disposition
to `workflows/scaffold.md`, which emits a PLAN.md **already populated**. If the user stops
early, hand off whatever was settled anyway: scaffolding with three decisions and six open
questions beats scaffolding an empty template.

**Mode B — continuing (planning doc exists).** Re-entrant. Grill resumes the tree instead of
rebuilding it, which is what makes these docs a breadcrumb trail rather than a stack of
one-shot interviews. See Step 1.

## Step 1 — Seed the tree (Mode B; never start blank)

Read the planning doc and its `docs/` tree, and seed:

- **Existing decisions** → settled nodes. Pruned, not re-litigated. They are *prerequisites*,
  so each one pushes the frontier outward: the questions hanging off them are exactly what
  became askable.
- **Open questions** (`docs/questions/Qxx.md`) → open frontier nodes carried over, with
  whatever partial answers previous rounds accumulated.
- **Parking-lot items** (`docs/parking-lot/Pxx.md`) → dormant nodes. A parked item re-enters
  the frontier **only if something settled since it was parked makes it answerable now.**
  Otherwise it stays dormant. Do not drag every parked idea back every session; that is how a
  parking lot becomes noise the user learns to skip.
- **Declined promotions** (Step 5) → suppressed until new material lands on that thread.

## Step 2 — Compute the frontier

The frontier is every unsettled node whose prerequisites are already settled — the questions
answerable **now**, without guessing at answers not yet heard.

**A question whose answer depends on another question still open in this round belongs to a
later round.** That ordering rule is the whole technique; violating it produces answers the
user has to retract two rounds later.

## Step 3 — Ask the round

Ask the frontier in one numbered batch, each question carrying **your recommended answer**, so
the cheap reply is "yes to all but Q3":

```
Round 3 · 7 settled · 4 open

❓ **Q1** — **<question title>**: <body; may be several paragraphs, may offer choices>

➡️ <your recommended answer>

---

❓ **Q2** — **<question title>**: <body>

➡️ <your recommended answer>
```

The orientation line (`Round 3 · 7 settled · 4 open`) is a progress indicator, not a prompt to
continue. It exists so the user can judge whether to keep going. Never editorialize on it.

**Finding facts is your job, never the user's.** When a frontier question needs a fact from the
environment — filesystem, dependency versions, an API's actual behavior, what a competitor does
— dispatch a subagent to find it. Do not ask the user something you could look up. Do not block
on it either: a running lookup is an unsettled prerequisite, so only the questions *downstream*
of it wait; ask the rest of the frontier now. **The decisions are always the user's.**

**Cap a round at roughly seven questions.** A frontier wider than that goes out over consecutive
rounds *at the same depth* — never by dropping questions, only by sequencing them. Breadth is
the guarantee this workflow exists to provide; a wall of eighteen questions just gets skimmed,
which loses the breadth in practice while appearing to preserve it.

## Step 4 — Dispose and record, at every round boundary

**The frontier empties by disposition, not by answer.** A blind spot is an *unasked* question,
not an unanswered one — so every node must close as exactly one of:

| Disposition | Lands in | Meaning |
|---|---|---|
| **Decided** | `Decisions` (a `Dxx` record) | settled, load-bearing, act on it |
| **Open question** | `docs/questions/Qxx.md` + one-line pointer | matters, not answerable yet |
| **Parked** | `docs/parking-lot/Pxx.md` + one-line pointer | might matter later, not now |
| **N/A** | nothing | branch doesn't apply; say so once, don't record it |

Write **at each round boundary, not at the end.** The user can stop at any moment, so a
session that writes only on completion loses everything to a cutoff. Close each round with one
line: `recorded → D7, Q2, P3 (parked)`.

**Appends accumulate; they never overwrite.** A `Qxx.md` touched by a later grill gets a new
dated section appended under the existing ones. That growing file *is* the breadcrumb trail —
the record of what you thought in June that made the July answer obvious. Rewriting it to read
cleanly destroys the only thing it's for.

New question and parked threads are born from `templates/QUESTION.template.md`. The planning
doc holds the one-line pointer only — never the discussion (see
`references/cooled-heuristic.md`, "born as pointers").

## Step 5 — Propose promotions

Grill's natural endpoint is a decision record, so promotion is native to it, not a bolt-on.
Threads ripen along one ladder:

```
parking lot  →  open question  →  decision (Dxx)  →  task queue
```

When a thread has accumulated enough to move up, **propose it and wait** — everything in this
skill is propose-then-confirm:

> "Q2 (auth model) has three sessions of answers and nothing left open — promote to D7?"

- **Propose at most one or two promotions per round.** This fires often; unchecked it turns
  every round into a nag and the user starts reflexively saying no.
- **On approval**, write the `Dxx` record whole and inline in the planning doc, leave
  `→ promoted to D7` as the closing dated entry on the thread file, and set markers: a freshly
  promoted decision almost always describes work not yet built, so it carries `🔨`; ask
  whether it is `🔒 foundational` only when it plausibly is.
- **On decline**, record the decline and its date on the thread. Do not re-pitch that thread
  until new material lands on it. A promotion the user already said no to is settled until
  something changes.
- **Decision → tasks** is the last rung: when a `Dxx` is concrete and mechanical, it is
  queueable. Offer to write it into the task doc as numbered pieces; that handoff belongs to
  the task-doc contract, not here.

## Step 6 — Stop

Two endings, both clean:

1. **Natural** — the frontier is empty. Every branch visited, nothing silently assumed.
   Say so and stop.
2. **The user cuts it off** — at any point, in any wording.

**Stopping is never negotiated. This is an invariant, not a preference.** A workflow built to
push will try to push here, and that is exactly the behavior to suppress. On any stop signal:

- No "are you sure?", no "we haven't covered X yet", no "one more round?", no listing what's
  being missed as a way of relitigating the stop.
- Disposition everything unvisited — open question or parked, per Step 4 — write it, report in
  one line, done. **Nothing is lost by stopping**, which is precisely why stopping needs no
  defense.
- If the stop names a branch or topic, park **that branch** and continue elsewhere. Otherwise
  stop the **session**. When it is ambiguous, stop the session — the quieter reading is the
  correct one, and asking which they meant is itself a form of arguing.

Then append a session-log entry to the planning doc, and log the run to the ledger
(`docs/rebalance-log.md`, `## Runs`) as a `grill` entry: rounds run, what was decided,
promoted, opened, parked. That log is what lets a later grill know where the tree already went.

## Invariants

- Never act on the outcome — never start building — until the user confirms the shared
  understanding. Grill produces the record; it does not execute against it.
- Never answer a decision on the user's behalf, including when the recommended answer is
  obvious and they skipped the question. A skipped question is an open question.
- Never re-ask a settled decision. If a new answer contradicts one, say so plainly and offer to
  supersede it (`[[D19]] supersedes this` — see `references/cooled-heuristic.md`).
- The planning agent stays light: threads live in `docs/`, pointers live in the planning doc.

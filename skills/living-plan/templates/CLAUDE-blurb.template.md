## Development workflow — planning vs implementation

Planning and implementation run in two layers by design.

- **Planning (the main thread).** Question/answer and exploration, landing on decisions
  recorded in `{{PLANNING_DOC}}`. Reads test output, makes design calls, owns live testing.
  When the shape of something isn't clear yet, that exploration has a structured form: the
  **`living-plan`** skill's `grill` workflow interviews round-by-round until the design tree
  has been *visited*, so whatever stays undecided lands in Open questions or the Parking lot
  instead of staying invisible. Ask for it ("grill me", "what am I missing"); offer it in one
  line — never launch it — when the user is thinking out loud without a question.
- **Implementation (the `{{AGENT}}` agent).** Once a decision is concrete enough to build,
  the planning thread writes the active task into `{{TASK_DOC}}` and launches the `{{AGENT}}`
  agent. It runs in its own context window (keeping planning context clean) and can run in the
  background while planning continues. On return, the planning thread reviews the diff and
  oversees testing.

`{{TASK_DOC}}` is the handoff contract. The active task is a **serial queue of numbered
pieces** — stack as few or as many as you like, which serves both **pacing** (queue a little,
plan ahead while the agent grinds) and **unattended** (queue a lot and walk away). The default
is synchronous: one agent works the queue top-to-bottom and reports once at the end; a blocked
piece is skipped (not halted on) so the run finishes everything it legitimately can, and the
agent **logs run-state into `{{TASK_DOC}}` on every stop** (per-piece status + a ▶ Run state
note) so a killed or forgotten session is recoverable from the file on disk. Standing "how we
implement here" knowledge lives in the **agent definition**, not in every task. Only
fully-specified, mechanical work is delegable; design decisions, open questions, and live
testing stay in the planning thread.

**Synchronous is the default on purpose — the objective is pacing, not raw throughput.** The
agent's serial grind is the *gap* the planning thread spends deciding the next batch (often on
another project). Running *parallel* agents across disjoint files is a separate, explicit
**opt-in burst tactic** chosen per-task — never the default, and not a change to this
single-queue structure; the agent itself never self-parallelizes. Reach for concurrency only
when a run is truly unattended and the file-sets are disjoint; otherwise it just floods the
planning thread with all the verification work at once, which defeats the pacing it exists to
give you.

**External task mirror — `{{MIRROR}}`.** A second copy of this project's task list lives
outside the repo, so items can be captured away from the machine and read back here.
**Reconcile it before starting a queue and again after finishing one** — otherwise it drifts
silently and gets forgotten, which is the failure this line exists to prevent. An item present
on one side and missing from the other is **not** a decision to delete it: absence means "not
yet mirrored," never "dropped." Nothing in `{{PLANNING_DOC}}` or `{{TASK_DOC}}` exists to serve
the mirror — the mirror side owns the pointer and the reconciliation, and these docs stay
standalone without it.

`{{PLANNING_DOC}}` is the **hot** decision record — keep it lean. Cooled material (old
session logs, settled/superseded decisions, deferred ideas) is progressively disclosed into
`docs/` with one-line pointers left behind. When `{{PLANNING_DOC}}` grows heavy to read each
session, invoke the **`living-plan`** skill — it detects what has cooled and relocates it,
propose-then-confirm.

That skill both **fills** these docs and **maintains** them: `grill` generates decisions and
questions, while `rebalance` and `evict-tasks` relocate what has gone cold. Items ripen along
one ladder — parking lot → open question → decision → task queue — and only a grill moves one
up it, always propose-then-confirm. Nothing is lost by cutting a grill short; whatever is
unfinished is written out as a question or a parked item first.

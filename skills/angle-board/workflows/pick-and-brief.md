# Workflow: Pick and Brief

Take one or more angles off a board, turn each into a brief, hand each to the project's writer (or stop at the brief if there isn't one).

This skill still does not write prose. A writer owns the voice and is the only thing that drafts.

---

## Step 1 — Load the board, and read its voice

If you just built it, it's in context. Otherwise find it:

```bash
ls -la <output-dir>/*-angles-*.md
```

No board named → list them with their pending counts and ask which. Read the chosen board.

**Read the board's `voice:` frontmatter before briefing anything.** It names the voice reference the writer must carry at Step 4. If the project has no writer, this workflow stops at the brief and hands the author the brief file — say that up front rather than at the end.

---

## Step 2 — Take the pick

The author picks by ID (`A1-03`), by description ("the pillar", "the contrarian one"), or picks several at once. **Several at once is normal and expected** — it's the reason the board exists.

If they pick a `#ev/needs-you` (thin ice) angle: say up front that there's no session evidence behind it, so the brief will be a skeleton and they'll be supplying the receipts from memory. That's a fine choice — just don't let it be a surprise at draft time.

If they pick multiple, check them against each other **before briefing any of them**: do they overlap? Two spokes that both want to explain the same fix are one post. Tell them, and offer to merge or drop one.

---

## Step 3 — Build the brief (one per pick)

Pull everything the board already knows, then go back to the source for the raw material — the board holds pointers, not content. Follow the evidence pointers into the source file(s) and read the cited sections (bounded — the cited slices, not whole files).

Each brief carries:

- **Working title** and the angle ID
- **Altitude, lens, reader** — verbatim from the board, including the reader's *moment*
- **The argument or the deliverable** — what the reader leaves with. A belief (high altitude) or a working build (low altitude). Be explicit about which.
- **Evidence, expanded** — the actual session beats, error text, commit diffs, quotes, numbers. This is where the brief earns its keep: go get the real material, don't restate the board's one-line pointer.
- **The signal, specified** *(mode B angles only)* — the board names the derived metric in one line; the brief has to make it buildable. What gets fetched, what gets computed from it, why that column and not the obvious one, and what the output looks like when it works. This is the post's middle section and the reason it isn't regenerable — a brief that leaves it at the board's one-liner will produce another how.
- **Target length** from the altitude band in `axes.md`
- **`Don't restate:`** the constraint from the board, if it's a spoke — plus the pillar's working title so the writer knows what it's linking up into
- **Internal links** — the pillar, plus any published post the board's evidence touches
- **Open questions** the author needs to answer before or during the draft

---

## Step 4 — Confirm, then hand off

Show the author the brief. Let them correct the reader and the argument — those are the two things they'll want to move, and they're cheap to change now and expensive to change in a draft.

Then invoke the project's writing skill (if there is one) with the brief, passing the board's `voice:` reference, and tell it explicitly:

- it owns voice and prose; the brief is scaffolding, not copy
- the `Don't restate` constraint is binding
- if it's a spoke, link up to the pillar

For multiple picks, brief and draft them **one at a time**. Do not fan out parallel drafts — they'll converge on the same phrasing and you'll be de-duplicating your own output afterward. Finish one, then start the next with the finished one in view.

---

## Step 5 — Update the board

Check the task line off in the board file (`- [ ]` → `- [x]`) and add the draft path as a sub-bullet:

```markdown
- [x] **A3-01 — Title** 🔺 #altitude/story #lens/postmortem #ev/strong
	- **Draft:** posts/2026-07-13-the-long-struggle.md
```

The remaining angles stay pending. Remind the author what's still on the board and how many — that backlog is the deliverable, not the one post they just wrote.

# Workflow — EVICT completed queues out of the task doc

For a project whose `TASKS.md` has become an **append-only log**: the queue discipline is
working (pieces get checked, finished work gets collapsed under a `[tag]`), but nothing ever
*leaves*, so the file grows without bound and stale entries survive because nobody re-reads it.

This is the third stage the collapse rule usually forgets: **check → collapse → evict.**

Propose-then-confirm, like every other workflow here. Never relocate without showing a manifest.

---

## The rule

A collapsed block leaves the task doc when **both** hold:

1. **Every piece in it is checked** — a queue with one deferred piece is not evictable as a
   unit. Split it: the block goes, the open piece is re-homed as a live item (see below).
2. **Nothing still-open references it** — an open item that says "see the FIX-6 notes" pins
   those notes in place until it's resolved or rewritten to point at the archive.

Eviction is **never automatic at end-of-queue**. Condition 2 is a judgment call, and the
implementer agent must not relocate docs while it works — it would be editing the file that
holds its own run state.

## What stays, always

- Open checkboxes and the open-items list
- The deferred / later / pre-launch queue (future work)
- The active queue and its `▶ Run state` note
- The status header

## What goes

- Fully-done queues, verbatim
- Narrative "how we got here" prose from finished passes (design discussions that resolved,
  working-facts blocks for an executor that has finished executing)
- Resolved open questions

## The two carve-outs (do these or the archive eats them)

Some material in a finished block is load-bearing for **future** work, not history. Burying it
in an archive nobody opens is a silent loss. Before evicting, lift out:

1. **Reusable operational knowledge** → a `docs/references/lessons.md`-style file. Matcher
   gotchas, probe-design traps, scraper quirks, source-specific landmines, the project's
   definition-of-done. Test: *would the next person doing a similar pass need this?* If yes it
   is a lesson, not history.
2. **Artifact inventory** → the README next to the code. If the done blocks are the only record
   of which scripts exist and what each one does, that inventory belongs in the code's README as
   a table, not in an archive.

Everything else moves verbatim. Do not re-summarize an evicted block — it was already collapsed
once, and rewriting history loses detail the author chose to keep.

---

## Steps

### 1. Map the file before reading it whole

Get the section boundaries cheaply, then read only what you must:

```bash
wc -l TASKS.md
grep -n '^#\|^##\|^###' TASKS.md
grep -c '^\s*-\s*\[x\]' TASKS.md; grep -c '^\s*-\s*\[ \]' TASKS.md
```

Build a line-range table: section → range → live/done. Report the done-vs-live split in lines
and as a percentage — that number is what justifies the surgery to the user.

### 2. Find the stale contradictions

These are the strongest evidence the file has stopped being read. Cross-check the status header
against the deferred queue: an item listed as *upcoming* that the header says is *complete* is a
stale entry. List them; they get deleted, not archived.

### 3. Propose the manifest

Show the user, before touching anything:

- the done/live line split
- the destination file(s) and whether they exist
- one line per block to be evicted, with its `[tag]` and date range
- the lessons you intend to lift out
- anything stale you intend to delete outright
- what will remain in the task doc, and its projected size

Get confirmation.

### 4. Move mechanically, not by retyping

**Back up first** (`cp TASKS.md <scratch>/TASKS.md.bak`), then assemble the archive by piping
line ranges — `sed -n 'A,Bp'` — into the destination. Never re-type or paraphrase a block into
the new file: that is how detail gets lost and how a 700-line move burns context. Verify the
seams afterward with a heading grep on the result, not by reading it back.

**Watch the working directory.** These runs mix `cd` into subdirectories with relative paths;
a persisted `cd` silently redirects later `ls`/`git ls-files`/`find` checks and will make you
conclude files don't exist when they do. Prefer absolute paths, or re-anchor with `cd <root> &&`
in each command.

### 5. Rewrite the task doc

Header → active/next → open items → deferred → **Done index**. The Done index is a table: one
row per `[tag]`, what it was, dates, and a link to the archive. That table is what replaces
hundreds of lines.

### 6. Wire it up so it doesn't regress

- Add the eviction stage to the project's conductor rule for the task doc (`CLAUDE.md` /
  `AGENTS.md` — resolve the symlink and edit the real target). State all three stages and the
  "what never leaves" list explicitly; a collapse-only rule is what caused the bloat.
- Add the new archive + lessons files to the project's docs index.
- Note the eviction in the ledger (`references/ledger.md`) with the date and the line counts.

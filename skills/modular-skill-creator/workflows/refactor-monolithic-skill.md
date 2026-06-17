# Refactor Monolithic Skill Workflow

Convert an existing single-file SKILL.md into the modular router + workflows/ + references/ architecture. The goal is to hollow out SKILL.md to routing-only while preserving all behavior.

---

## Step 1 — Read the Existing Skill

Ask for the path to the existing SKILL.md if not already provided.

Read the entire file. Take stock of:
- Current line count
- What the frontmatter contains (fields, description quality)
- How many distinct decision branches or procedural stages exist
- How much of the file is routing/intake vs. step-by-step procedure
- What data (word lists, templates, examples) is embedded inline that should be a reference file

---

## Step 2 — Identify the Seams

Scan for natural split points:

**Decision branches** — places where the skill chooses between two different paths based on user input or input shape. Each branch becomes its own workflow file.

**Sequential passes** — numbered or lettered stages (Pass 1, Pass 2; Step A, Step B; Phase 1, Phase 2). Each pass becomes its own workflow file, or group closely-related lightweight passes into one.

**Data blobs** — inline word lists, lookup tables, examples, or templates that aren't procedural instructions. These become reference files.

**Size rule of thumb:** If a section is more than ~30 lines of procedural instructions, it warrants its own workflow file. If it's 5 lines, it can probably stay in the router.

---

## Step 3 — Design the New Structure

Produce and show the user a refactor map before writing anything:

```
REFACTOR MAP: <skill-name>/SKILL.md
──────────────────────────────────────────────
STAYS IN ROUTER (~N lines after refactor):
  - frontmatter
  - <essential_principles> block (keep or trim)
  - <intake> block (routing logic only)
  - Workflow routing section (one rule per workflow)
  - Reference materials list

MOVES TO workflows/:
  - [lines X-Y] "<section name>" → workflows/<file>.md
  [repeat]

MOVES TO references/:
  - [lines X-Y] "<data block name>" → references/<file>.md
  [repeat]
──────────────────────────────────────────────
Estimated router size after refactor: ~N lines
```

Ask: "Does this mapping look right? Anything to change before I start?"

Do not proceed until confirmed.

---

## Step 4 — Extract Workflow Files

For each section being extracted:

1. Create `workflows/<filename>.md`
2. Copy the procedural content verbatim — do not rewrite, only reformat into the standard workflow shape:
   - Add `# <Workflow Name>` header
   - Add one-sentence description below the header
   - Wrap existing steps in `## Step N — NAME` sections if they aren't already
   - Add `**Output:**` line at the end of each step if missing
   - Add `## Done` checklist at end
3. Update any cross-references: if the extracted content said "see below" or "as described above," replace with explicit file references

---

## Step 5 — Extract Reference Files

For each data blob being extracted:

1. Create `references/<filename>.md`
2. Copy the data verbatim — do not summarize or restructure content, only add a header and brief description
3. If the blob is a list or table, keep it as-is; add a table of contents if over 50 lines

---

## Step 6 — Rewrite the Router

Rewrite SKILL.md in place:

1. **Frontmatter** — keep as-is unless the description needs improvement (see scaffold-router.md Step 2 for description rules)
2. **`<essential_principles>`** — keep or trim to core rules only; anything procedural moves to workflows
3. **`<intake>`** — keep routing logic; replace any embedded step-by-step instructions with "Read `workflows/<file>.md`"
4. **`<instructions>`** — replace each extracted section with a one-line routing rule: "If [condition], read `workflows/<file>.md`." Add a `## Reference Materials` section listing all extracted reference files.
5. **Remove** all extracted content from SKILL.md

---

## Step 7 — Verify the Refactor

Line count check: router should be under ~150 lines. If it's still large, re-examine what's left.

Behavior check — read through the new router and ask: "If Claude reads only SKILL.md, will it know:
- When to trigger?
- What to ask the user (if anything)?
- Which workflow to load for each situation?
- What reference files exist and when to use them?"

If the answer to any is "no," fix it before reporting done.

---

## Step 8 — Report

Show the user the final manifest (same format as scaffold-workflows.md Step 3) and note what was extracted where.

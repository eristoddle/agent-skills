# Scaffold Workflows Workflow

Generate each `workflows/<name>.md` file declared in the skill spec. Also scaffold any `references/<name>.md` files that need to be created.

---

## Step 1 — Generate Each Workflow File

For each workflow entry in the spec, produce a file at `workflows/<filename>.md`.

**Every workflow file must contain these sections in order:**

### Header
```markdown
# <Workflow Name>

<One-sentence description of what this workflow does, its inputs, and its outputs.>
```

### Inputs / Prerequisites (if non-obvious)
Only include if the workflow needs specific inputs that won't always be self-evident from context:
```markdown
**Inputs:** <file path, artifact from prior step, etc.>
**Prerequisites:** <what must exist before this runs>
```

### Steps

Numbered steps, each with:
- A bold goal line: `**Goal:** <what this step accomplishes>`
- Numbered sub-instructions
- Explicit output: what gets written, displayed, or passed on

Use this shape (from ct-fact-checker's verify-claims.md pattern):
```markdown
## Step N — STEP NAME

**Goal:** <one sentence>

1. <instruction>
2. <instruction>
3. If [condition], do X. Otherwise do Y.

**Output:** <what this step produces>

---
```

For multi-pass workflows (like ct-humanizer's full-humanize.md), use `## Pass N` instead of `## Step N`.

**Rules for workflow steps:**
- Write the steps procedurally — the executor reads this file and follows it literally
- Reference other files explicitly: `read \`references/foo.md\`` not "consult the foo reference"
- State file write actions explicitly: "Write the transformed article back to the file path." / "Do NOT write to the file in this step."
- End each step with what it produced (display to user? write to disk? pass to next step?)

### Done Criteria
```markdown
## Done

This workflow is complete when:
- [ ] <condition 1>
- [ ] <condition 2>
```

---

## Step 2 — Scaffold Reference Files

For each reference file in the spec:

1. Create `references/<filename>.md`
2. Write a header and a brief table of contents or structure outline
3. Add placeholder content with clear `[FILL IN: ...]` markers for any data the user must supply (e.g., word lists, example content, lookup tables)
4. If the reference type is a standard pattern (word blacklist, claim-type lookup table, template library), scaffold a realistic structure with a few example entries and a note that the user should expand it

Reference file structure:
```markdown
# <Reference Name>

<One-sentence description of what this file contains and when to use it.>

---

## [Section 1]

[content or placeholder]

---

## [Section 2]

[content or placeholder]
```

---

## Step 3 — Report File Manifest

After writing all files, show the user a manifest:

```
Files written to <save-path>/<skill-name>/

SKILL.md                    ← router (~N lines)
workflows/
  <file>.md                 ← <one-line purpose>
  [repeat]
references/
  <file>.md                 ← <one-line purpose>
  [repeat]
```

Then show next steps:
1. Review each workflow file and replace any `[FILL IN: ...]` placeholders with real content
2. Test by invoking the skill in a new session and checking that the router loads quickly and routes correctly
3. If using skillshare: run `skillshare sync` to distribute the skill to all configured targets

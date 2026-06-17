# Design Modular Skill Workflow

Interview the user to produce a complete skill specification. This spec is consumed by scaffold-router.md and scaffold-workflows.md in the next steps.

---

## Step 1 — Gather Core Identity

Use AskUserQuestion to collect:

1. **Skill name** — kebab-case, e.g. `ct-humanizer`, `my-research-tool`. Confirm it doesn't collide with an existing skill at the chosen save path.

2. **One-sentence purpose** — what does this skill do? This becomes the opening line of the description field.

3. **Primary trigger phrases** — what would the user say to invoke this skill? List 4-6 phrases. These go into the description to combat undertriggering. Examples: "humanize an article", "remove AI writing", "scan for AI patterns".

4. **Anti-trigger** — what should NOT trigger this skill (to prevent collision with related skills)? Example: ct-humanizer anti-trigger is "fiction" (that's ct-fiction-humanizer's domain).

---

## Step 2 — Design the Workflow Branches

Ask: "Walk me through the distinct stages or branches of work this skill needs to do."

For each branch the user describes:
- Assign a workflow filename (kebab-case `.md`, no spaces)
- Write a one-sentence description of what that workflow does
- Identify its inputs (what does it need to start?) and outputs (what does it produce or write?)

Common patterns to listen for:
- **Diagnostic vs. execution** — one workflow assesses, another transforms (like quick-scan vs. full-humanize)
- **Stages in a pipeline** — step A produces artifact that step B consumes (like verify → fix → re-verify)
- **Type-based branches** — different inputs route to different workflows (like "if file path → verify; if outline → draft")

Record the workflow list as:
```
workflows:
  - file: <filename>.md
    purpose: <one-sentence>
    inputs: <what it needs>
    outputs: <what it produces>
```

---

## Step 3 — Design the Reference Files

Ask: "What data does this skill need that doesn't belong in procedural logic?"

Common reference types:
- Word/phrase lists (blacklists, glossaries, keyword tables)
- Templates or skeleton patterns
- Lookup tables (claim types → verification source)
- Example before/afters or annotated samples
- Style guides or constraint lists

For each reference file:
- Assign a filename
- Write a one-sentence description of what it contains
- Note which workflow(s) use it

---

## Step 4 — Choose the Routing Pattern

Ask: "How should the router decide which workflow to run?"

Present three options (read `references/router-patterns.md` for the full templates):

1. **Menu-driven** — router asks the user to pick from named options via AskUserQuestion. Best for: interactive skills, skills with clearly distinct modes, skills the user invokes by choice. Example: ct-humanizer (Full humanize vs. Quick scan).

2. **Input-shape detection** — router inspects the input (file present? content type? called from another skill?) and selects a workflow automatically, no questions asked. Best for: autonomous loops, skills called from other skills, skills with obvious input signals. Example: ct-fact-checker.

3. **Stage-pipeline** — router runs workflows in a fixed sequence: A → B → C. Each workflow ends with an explicit handoff. Best for: skills with mandatory sequential steps where every invocation runs all stages.

4. **Hybrid** — e.g., menu at top level, then automatic routing within each branch.

Record the chosen pattern.

---

## Step 5 — Decide on Model Pin

Ask: "Does this skill need a specific model pinned, or should it run on whatever model is active?"

Guidelines to share:
- **Pin `claude-haiku-4-5`** for autonomous loops that run many iterations (like fact-checker). Faster and cheaper for mechanical verification work.
- **Pin `claude-sonnet-4-6`** for complex reasoning, writing quality, or judgment-heavy tasks.
- **No pin (default)** for most interactive skills that benefit from the current session model.

---

## Step 6 — Output the Spec

Produce a structured spec block and show it to the user for confirmation before proceeding:

```
SKILL SPEC
──────────────────────────────────────────
Name:         <kebab-case>
Save path:    <confirmed path from intake>
Purpose:      <one sentence>
Trigger phrases: <list>
Anti-trigger: <what should NOT trigger this>
Model pin:    <model or "none">
Routing:      <menu-driven | input-shape | stage-pipeline | hybrid>

Workflows:
  - <file>.md — <purpose> | inputs: <X> → outputs: <Y>
  [repeat]

References:
  - <file>.md — <what it contains> | used by: <workflows>
  [repeat]
──────────────────────────────────────────
```

Ask: "Does this spec look right? Any changes before I generate the files?"

Do not proceed to scaffold-router.md until the user confirms the spec.

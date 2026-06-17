# Scaffold Router Workflow

Given the confirmed skill spec from design-modular-skill.md, generate the `SKILL.md` router file. Read `references/router-patterns.md` to get the correct routing template for the chosen pattern before writing.

---

## Step 1 — Read the Router Pattern Template

Open `references/router-patterns.md` and locate the section matching the spec's routing pattern:
- Menu-driven → use the Menu-Driven template
- Input-shape detection → use the Input-Shape template
- Stage-pipeline → use the Stage-Pipeline template
- Hybrid → combine the relevant sections

Keep that template in context for Steps 3-4.

---

## Step 2 — Build the Frontmatter

Read `references/frontmatter-conventions.md` before writing any frontmatter.

Assemble the frontmatter block:

```yaml
---
name: <kebab-case from spec>
description: |
  <See description rules below>
```

Add these optional fields only if the spec calls for them:
- `model: <model-id>` — only if the spec has a model pin
- `metadata.targets: [claude]` — only if the skill should stay Claude-only and not sync to other tools
- `version: <semver>` — only if the user explicitly wants versioning from the start
- `argument-hint: "<hint string>"` — only if the skill takes a positional argument

**Description rules:**
- Write as a YAML block scalar (pipe `|`)
- First sentence: what the skill does (the "purpose" from spec)
- Second sentence: the specific trigger phrases — "Use this skill when…" or "Trigger when the user says…" followed by the trigger phrase list
- Third sentence: anti-trigger — "Do NOT trigger when…" (use the anti-trigger from spec)
- Target 50-100 words total; pushy and specific is better than vague and short
- Do not pad with generic language

---

## Step 3 — Write `<essential_principles>`

Open with `<essential_principles>` tag.

Include:
1. **What This Skill Does** — one paragraph explaining the skill's purpose and scope. What it is, what it is NOT.
2. **Core Rules** — numbered list of 3-6 constraints the executor must follow regardless of workflow. These are the invariants.

Close with `</essential_principles>`.

Keep this section tight: 60-120 words total. No workflow steps here.

---

## Step 4 — Write `<intake>`

Open with `<intake>` tag.

Use the routing pattern template from Step 1 to write the intake block:

**For menu-driven:** Write an AskUserQuestion block that presents the workflow options as named choices. Each option maps to exactly one workflow file. Label the options clearly (they become the routing keys in Step 5).

**For input-shape detection:** Write a conditional logic block that inspects the input and assigns the workflow path without asking the user. Conditions to check: file path provided? content type? called from another skill? prior step output present?

**For stage-pipeline:** Write a minimal intake that collects only what's needed to start the first stage (usually just a file path or input artifact), then states "Proceed directly to `workflows/<first-stage>.md`."

**For hybrid:** Combine the relevant blocks, clearly separated.

Close with `</intake>`.

---

## Step 5 — Write `<instructions>`

Open with `<instructions>` tag.

### Workflow Routing section

For each workflow in the spec, write one routing rule:

```markdown
### If [condition / user chose option X]:
Read `workflows/<file>.md` [and follow it exactly / then proceed to `workflows/<next>.md`].
```

Be explicit. "Read `workflows/foo.md`" is better than "run the foo workflow."

For stage-pipelines, number the stages and show the handoff chain:
```
1. Read `workflows/stage-a.md` — produces [output].
2. Read `workflows/stage-b.md` — consumes [output], produces [next].
3. Read `workflows/stage-c.md` — final step, reports to user.
```

### Reference Materials section

List every reference file with a one-line "read when…" description:
```markdown
- `references/<file>.md` — [what it contains; when to read it]
```

### Quality Checklist section (optional but recommended)

Add a short done-criteria checklist at the end of the instructions block. These are the conditions under which the skill can report completion. Model on the ct-humanizer "Quality Standards" section.

Close with `</instructions>`.

---

## Step 6 — Final Router Checks

Before writing the file:

1. Count the lines. **If over 150 lines**, identify what to move. Step-by-step instructions belong in workflow files, not the router.
2. Verify zero multi-step procedure prose appears in the router body.
3. Verify the description field is 50-100 words and lists at least 4 trigger phrases.
4. Verify no `allowed-tools` field is present.

Write the SKILL.md file to the confirmed save path.

Report to the user: "Router written. Moving to scaffold-workflows.md."

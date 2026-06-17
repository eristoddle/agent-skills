# Router Patterns

Three minimal template patterns for the `<intake>` and `<instructions>` sections of a modular skill router. Use the one that matches the spec's routing pattern. Copy the relevant sections into scaffold-router.md.

---

## Pattern 1: Menu-Driven

**When to use:** The user should pick which workflow to run. The choice is meaningful and non-obvious from the input alone. Best for: interactive editing skills with distinct modes, tools where the user controls the scope.

**Reference skill:** `ct-humanizer`

### Intake block

```markdown
<intake>

I need the [primary input]. What's the [file path / URL / content]?

After the user provides the input, ask follow-up questions using AskUserQuestion:

1. "[Optional context question]" — [what to do with the answer]

2. "What would you like to do?" — Options:
   - **[Option A name]** — [short description of what this mode does]
   - **[Option B name]** — [short description of what this mode does]
   - **[Option C name]** — [short description of what this mode does]

Then route to the appropriate workflow.

</intake>
```

### Instructions block (routing rules)

```markdown
## Workflow Routing

### If user selects "[Option A name]":
Read `workflows/<file-a>.md` exactly. [One sentence on what it does.]

### If user selects "[Option B name]":
Read `workflows/<file-b>.md`. [One sentence on what it does.]

### If user selects "[Option C name]":
Read `workflows/<file-c>.md`. [One sentence on what it does.]
```

---

## Pattern 2: Input-Shape Detection

**When to use:** The correct workflow is determinable from the input itself — no need to ask. Best for: autonomous loops, skills called from other skills, pipelines with obvious input signals (file path present/absent, content type, prior step output).

**Reference skill:** `ct-fact-checker`

### Intake block

```markdown
<intake>

Run immediately on the provided [input type]. No questions needed unless [input] is missing.

**If called from another skill** ([skill-name], [skill-name], etc.): receive the [input] and run without prompting.

**If invoked directly** (`/[skill-name]`): ask for the [input], then run.

After receiving the [input], go directly to `workflows/<primary-workflow>.md`. Do not ask for confirmation.

</intake>
```

Or for more complex shape detection:

```markdown
<intake>

Inspect the input and route immediately:

- **If [condition 1]** (e.g., a file path is provided): go to `workflows/<workflow-a>.md`
- **If [condition 2]** (e.g., raw text is provided): go to `workflows/<workflow-b>.md`
- **If [condition 3]** (e.g., called with `--flag`): go to `workflows/<workflow-c>.md`
- **If no input is provided**: ask for [what's needed], then route.

</intake>
```

### Instructions block (routing rules)

```markdown
## Workflow

Execute in order:

1. **[STAGE NAME]** — Read `workflows/<file-a>.md`. Produces [output].
2. **[STAGE NAME]** — Read `workflows/<file-b>.md` on any [items] with status `[condition]`.
3. **[STAGE NAME]** — Re-run `workflows/<file-a>.md` on [subset] only.
4. **CLEAR or LOOP** — If [done condition], report cleared. If any remain, loop back to step 2.
```

---

## Pattern 3: Stage-Pipeline

**When to use:** Every invocation runs all stages in sequence. Stages are mandatory and order-dependent. Stage N always hands off to Stage N+1. Best for: end-to-end content pipelines (research → outline → draft → review), multi-phase processing where each step transforms an artifact for the next.

### Intake block

```markdown
<intake>

I need [primary input] to begin. What's the [file path / topic / artifact]?

[Optional: one clarifying question if needed to pick the right pipeline variant.]

After receiving the input, proceed directly to Stage 1.

</intake>
```

### Instructions block (routing rules)

```markdown
## Pipeline

Run all stages in sequence. Each stage reads the output of the previous.

1. **[STAGE 1 NAME]** — Read `workflows/<stage-1>.md`. Input: [what]. Output: [artifact name].
2. **[STAGE 2 NAME]** — Read `workflows/<stage-2>.md`. Input: [artifact from stage 1]. Output: [artifact name].
3. **[STAGE 3 NAME]** — Read `workflows/<stage-3>.md`. Input: [artifact from stage 2]. Output: [final artifact].

Each workflow file ends with an explicit handoff instruction to load the next stage.
```

### Handoff pattern (at end of each stage workflow file)

```markdown
## Handoff

This stage is complete when [done criteria].

Proceed to `workflows/<next-stage>.md` with [output artifact / file path].
```

---

## Hybrid Notes

A hybrid typically uses menu-driven routing at the top level (user picks a mode) with stage-pipeline within the chosen mode. Structure the intake as menu-driven; structure each mode's workflow chain as a mini-pipeline with explicit handoffs.

Example: "User picks 'Full' mode → runs stage A → B → C in sequence. User picks 'Quick' mode → runs single-stage D."

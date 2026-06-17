# Frontmatter Conventions

Only the fields that appear in the user's actual skills. Do not add fields not on this list — especially `allowed-tools`, which is not part of this user's convention.

---

## Required Fields

### `name`
- Type: string
- Format: kebab-case, matches the directory name exactly
- Example: `name: ct-humanizer`

### `description`
- Type: string (plain) or YAML block scalar (pipe `|`)
- Content: 50-100 words, pushy, trigger-rich. Must list specific trigger phrases so the skill doesn't undertrigger.
- Format as block scalar when multi-sentence (preferred for modular skills):
  ```yaml
  description: |
    First sentence: what the skill does.
    Second sentence: "Use this skill when the user wants to..." + trigger phrase list.
    Third sentence: "Do NOT trigger for..." + anti-trigger.
  ```
- Format as single-line when short and simple:
  ```yaml
  description: Short one-sentence description.
  ```

---

## Optional Fields

### `model`
- Type: string — a specific Claude model ID
- Use when: the skill benefits from a specific model (e.g., haiku for autonomous loops)
- Example: `model: claude-haiku-4-5`
- Do NOT add unless the spec calls for it. Most skills should inherit the session model.
- Current model IDs: `claude-haiku-4-5-20251001`, `claude-sonnet-4-6`, `claude-opus-4-7`

### `version`
- Type: string — semver without `v` prefix
- Example: `version: 1.0.0`
- Add only if the user explicitly wants version tracking from the start.

### `metadata.version`
- Type: string — semver with `v` prefix (used by skillshare itself)
- Example: `metadata.version: v1.0.0`
- Distinct from `version`. Use `version` for skill content versioning; `metadata.version` is skillshare's own convention.

### `metadata.targets`
- Type: array of strings
- Use when: the skill should only sync to specific AI tool targets and not others
- Example: `metadata.targets: [claude]`
- Omit when the skill should sync everywhere.

### `argument-hint`
- Type: string
- Use when: the skill is invoked with positional arguments that the user should see as a hint
- Example: `argument-hint: "<file-path> [--mode full|quick]"`
- Only add if the skill has a clear CLI-style argument pattern.

---

## Fields NOT Used Here

- `allowed-tools` — not part of this user's convention; do not add to generated skills
- `tools` — same
- `tags` — same
- Any field not listed above — omit unless the user explicitly asks for it

---

## Example: Complete Frontmatter

Minimal (most common):
```yaml
---
name: my-skill
description: |
  Does X by running Y. Use when the user asks to "do X", "run X on a file",
  "X this article", or wants X applied to content. Do NOT trigger for Z tasks.
---
```

With model pin:
```yaml
---
name: my-autonomous-skill
description: |
  Autonomous loop that does X. Trigger when user says "run X", "check X", or "verify X".
  Called directly or from another skill. Do NOT trigger for interactive editing tasks.
model: claude-haiku-4-5-20251001
---
```

With target restriction:
```yaml
---
name: my-claude-only-skill
description: Uses Claude-specific features. Use when...
metadata:
  targets: [claude]
---
```

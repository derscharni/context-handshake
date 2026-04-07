# Context Handshake Specification

Version: 0.1.0

## Overview

A Context Handshake consists of two files in YAML-frontmatter markdown format:

1. **`identity.md`** — Persistent. Describes who you are across sessions.
2. **`session-intent.md`** — Per-session. Describes what this session should accomplish.

Both files use YAML frontmatter for structured fields and freeform markdown for extended context.

---

## identity.md

### Required Fields

| Field | Type | Description |
|---|---|---|
| `name` | string | Your full name |
| `role` | string | Professional role or primary context |
| `working-style` | list | How you think and work (bullet points) |
| `communication` | list | Tone, language, what you don't need |
| `constraints` | list | What the agent must never do |

### Optional Fields

| Field | Type | Description |
|---|---|---|
| `frameworks` | list | Your own concepts or frameworks the agent should know |
| `infrastructure` | string | Technical stack, if relevant |
| `closer` | string | Recurring sign-off or signature phrase |

### Rules

- All required fields must be present and non-empty.
- `working-style`, `communication`, and `constraints` are lists with at least one item each.
- Freeform markdown below the frontmatter is allowed and should be treated as extended context.

---

## session-intent.md

### Required Fields

| Field | Type | Description |
|---|---|---|
| `date` | string | ISO 8601 date or datetime (e.g. `2026-04-07` or `2026-04-07T14:30`) |
| `session-type` | enum | One of: `writing`, `research`, `technical`, `framework`, `exploration` |
| `goal` | string | What should exist at the end that doesn't exist now |
| `constraints` | list | Language, format, scope limitations |

### Optional Fields

| Field | Type | Description |
|---|---|---|
| `active-context` | string | What happened since last session that's relevant |
| `open-questions` | list | What's unresolved |

### Rules

- `session-type` must be one of the five defined values.
- `goal` must be a single, concrete statement.
- `constraints` is a list with at least one item.

---

## File Format

Both files use YAML frontmatter delimited by `---`:

```markdown
---
name: ...
role: ...
working-style:
  - ...
  - ...
---

Any additional freeform context goes here.
```

## Validation

Use `validate.py` to check files against this spec. Exit code 0 means valid. Non-zero means missing or empty required fields.

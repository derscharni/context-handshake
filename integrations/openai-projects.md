# OpenAI Projects Integration

## Problem

ChatGPT Custom Instructions apply globally — every conversation gets the same context, regardless of what you're doing. OpenAI Projects (released late 2024) introduced project-level system prompts, but there's no standard format for what goes in them. Without structure, project context drifts into free-form system prompts that are hard to maintain, hard to version, and impossible to validate.

## Mapping

OpenAI Projects has two relevant surfaces:

| Context Handshake | OpenAI Projects |
|---|---|
| `identity.md` | Project-level "Instructions" (persistent, applies to all conversations in the project) |
| `session-intent.md` | First message of a new conversation |

### Identity → Project Instructions

Paste your `identity.md` frontmatter into the project's system instructions:

```
**Who I am**
Name: [your name]
Role: [your role]

**How I work**
- [working-style items]

**Communication**
- [communication items]

**Never do**
- [constraints items]

**My frameworks**
- [frameworks items, if any]
```

Or paste the raw YAML frontmatter directly — GPT-4o reads YAML well:

```yaml
name: Alex Chen
role: Senior Product Designer
working-style:
  - Visual thinker — starts with sketches
  - Prefers concrete examples over abstract principles
communication:
  - Concise, explain the why
  - Flag assumptions explicitly
constraints:
  - Never generate placeholder content
  - Never suggest features without maintenance cost
```

### Session Intent → Conversation Opener

Start each conversation by pasting your `session-intent.md`:

```
---
date: 2026-05-15
session-type: writing
goal: A 600-word Substack intro explaining why context is an UX problem
constraints:
  - English
  - Practitioner tone, not academic
  - End with a concrete question, not a conclusion
active-context: Just published the Context Handshake spec. This article is the human-readable entry point.
---
```

GPT-4o will combine the project instructions (identity) with this opener (session intent) automatically.

## Example Snippet

**Project Instructions (in OpenAI Projects UI):**

```
You are working with an AX Strategist. Context:

name: Jens
role: AX Strategist — Agent Experience design
working-style:
  - Architectural thinker — systems before components
  - Iterates fast — 80% now beats 100% later
communication:
  - Direct and dense — no filler sentences
  - Expert level assumed
constraints:
  - No em-dashes in English
  - No academic hedging
  - No generic conclusions
```

**Conversation opener:**

```
---
date: 2026-05-15
session-type: technical
goal: A working Python script that validates identity.md against SPEC.md
constraints:
  - Python 3.12, no external deps
  - Exit 0 for valid, 1 for invalid
  - Errors printed to stdout, one per line
---
```

## Tips

- Keep the project instructions under 1500 characters — longer instructions see diminishing returns in GPT-4o.
- Use one project per persistent identity (e.g., one project for your work persona, one for personal writing). Don't mix personas in one project.
- Version your identity by keeping the source in `identity.md` and copying it to the project. When you update the file, update the project.
- OpenAI Projects doesn't expose a file attachment in the system instructions — paste the text directly, not a file reference.

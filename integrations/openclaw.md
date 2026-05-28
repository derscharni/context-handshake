# OpenClaw Integration

## Problem

OpenClaw agents use `SOUL.md` and `USER.md` as their persistent context layer. These files describe the agent's character and the user's preferences, but they're freeform and agent-specific — there's no standard format. When you work with multiple OpenClaw agents, or want to share context between them, there's no portable layer to carry across.

Context Handshake maps cleanly onto OpenClaw's existing pattern: `identity.md` is the user side of `USER.md`, and `session-intent.md` is what today's task files already do manually.

## Mapping

| Context Handshake | OpenClaw |
|---|---|
| `identity.md` | `USER.md` (user preferences and constraints) |
| `session-intent.md` | Task files in `inbox/` or session-start message |
| `identity.frameworks` | Concepts referenced in `SOUL.md` or `USER.md` |
| `identity.infrastructure` | Tool stack, binary paths in `TOOLS.md` |

### identity.md → USER.md

`USER.md` in OpenClaw is the persistent user context that every agent reads at session start. You can either:

**Option A: Replace USER.md with identity.md**

Keep a single source of truth. Name it `identity.md`, validate it with `validate.py`, then symlink or copy:

```bash
cp identity.md ~/.openclaw/workspace/USER.md
```

**Option B: Include identity.md from USER.md**

Keep USER.md as the OpenClaw-specific wrapper and reference your identity:

```markdown
# USER.md

## Identity
<!-- identity.md fields pasted here, kept in sync -->
name: Jens
role: AX Strategist
working-style:
  - Architectural — systems before components
communication:
  - Direct, expert level assumed
constraints:
  - No em-dashes in English

## OpenClaw-specific
[vault paths, tool paths, etc.]
```

### session-intent.md → Task Files

OpenClaw agents already process task files from `inbox/`. Structure them as `session-intent.md` so they're portable and validatable:

```markdown
---
date: 2026-05-26
session-type: technical
goal: Refactor the membrane router to support priority queues
constraints:
  - Python 3.12
  - No new external dependencies
  - All tests must pass
active-context: Just merged the trust-stack branch. Router is the next bottleneck.
open-questions:
  - Should priority be per-sender or per-message-type?
---
```

Run `validate.py session-intent.md` before dropping it in the inbox. If it passes, the structure is correct and the agent gets clean context.

## Example Snippet

**USER.md with Context Handshake fields:**

```markdown
# USER.md

## Context Handshake

name: Jens
role: AX Strategist — Agent Experience design
working-style:
  - Architectural thinker — systems before components
  - Iterates fast — 80% now beats 100% later
  - Writes in English, thinks sometimes in German, never mixes
communication:
  - Direct and dense
  - Expert level assumed — no basics
constraints:
  - No em-dashes in English
  - No academic hedging
  - No generic conclusions
frameworks:
  - AX Stack — five-layer model for Agent Experience (Intent, Authority, Context, Orchestration, Accountability)
  - Context Sovereignty — user-owned context layer

## Infrastructure

vault: /Users/jens/.napkin
openclaw: /Users/agent/.openclaw/workspace
```

**Inbox task file as session-intent.md:**

```markdown
---
date: 2026-05-26
session-type: technical
goal: A complete MVP of the context-handshake validator with edge case tests
constraints:
  - Python 3.12, no external deps
  - Tests as pytest, not unittest
active-context: validate.py exists, covers happy path. Edge cases untested.
open-questions:
  - Should we test hidden Unicode injection in the validator itself?
---
```

## Why This Pattern Works

OpenClaw already implements the Context Handshake pattern informally:

- `SOUL.md` = agent identity (the other side of the handshake)
- `USER.md` = user identity (maps to `identity.md`)
- Task files = session intent (maps to `session-intent.md`)

Making the user side explicit and validatable means context stays consistent across agents, across sessions, and across tools — not just within OpenClaw.

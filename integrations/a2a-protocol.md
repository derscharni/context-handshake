# A2A Protocol Integration

## Problem

Multi-agent pipelines pass tasks between agents — but typically only pass the task, not the context that authorizes it. Agent B receives a goal from Agent A, but doesn't know: who originally authorized this work, what constraints apply, or how fresh the context is.

Without a structured handshake, Agent B either has to trust Agent A blindly or ask the human to repeat their preferences — which defeats the purpose of autonomous pipelines.

Context Handshake solves this by making context **declared and attached**, not inferred or reconstructed.

## Mapping

In a two-agent handoff (Agent A → Agent B):

| Context Handshake | A2A Role |
|---|---|
| `identity.md` | The human authority behind the pipeline. Attached once, forwarded by every agent. |
| `session-intent.md` | The task being delegated. Updated (or generated) by Agent A before passing to Agent B. |
| `identity.constraints` | What Agent B must never do, regardless of what Agent A instructs. |
| `identity.frameworks` | Domain concepts Agent B needs to interpret the task correctly. |

## The Pattern: Envelope + Task

Think of it as an envelope: the identity is the return address (who authorized this, what rules apply), the session-intent is the letter (what to do).

```
┌─────────────────────────────────────┐
│  Context Envelope                   │
│  identity.md — constant, attached   │
│  session-intent.md — per-task       │
├─────────────────────────────────────┤
│  Agent A (orchestrator)             │
│  generates session-intent           │
│  forwards envelope to Agent B       │
├─────────────────────────────────────┤
│  Agent B (executor)                 │
│  reads identity (constraints first) │
│  executes session-intent goal       │
└─────────────────────────────────────┘
```

## Example Snippet

**Research Agent → Writing Agent handoff:**

Agent A (Research) generates a session intent for Agent B (Writing):

```markdown
---
date: 2026-05-10T14:23:00Z
session-type: writing
goal: A 400-word research note on Temporal Integrity in agent memory systems
constraints:
  - English
  - Critical angle mandatory — no neutral summaries
  - Output as markdown to /inbox/2026-05-10-temporal-integrity.md
active-context: Research complete. Sources synthesized. Key claim — most agent memory systems treat recency as a proxy for relevance, which breaks under asynchronous pipelines.
open-questions:
  - Should we challenge the recency assumption directly or frame it as a design gap?
---
```

This session intent is passed to Agent B alongside the original `identity.md` from the human. Agent B reads the identity first (to know what constraints and frameworks apply), then executes the session intent.

**What Agent B knows:**
- Who authorized this: the human identity in `identity.md`
- What to do: the goal in `session-intent.md`
- What never to do: the constraints in `identity.constraints`
- Domain concepts: the frameworks in `identity.frameworks`

## Authorization Fields (Extended Pattern)

For pipelines that need explicit provenance, add these optional fields to the session intent:

```markdown
---
date: 2026-05-10T14:23:00Z
session-type: technical
goal: Run the full test suite and report failures
constraints:
  - Read-only — no file writes except the report
  - Report to /tmp/test-report.md only
authorized-by: jens
authorization-scope: read, test, report
originating-agent: research-agent-v1
confidence: 0.92
---
```

These fields aren't in the core SPEC (which stays minimal), but they're valid freeform frontmatter that consuming agents can use for trust decisions.

## Integration with Google A2A / OpenAI Swarm

Both Google's A2A protocol and OpenAI's Swarm framework pass task messages between agents. Context Handshake works as the context layer on top of either:

- **Google A2A**: Attach `identity.md` and `session-intent.md` as parts of the A2A message payload. The receiving agent reads them before executing the task.
- **OpenAI Swarm**: Pass both files as part of the context dict when transferring between agents. Use `identity.constraints` as a hard filter before the agent acts.

The spec is format-agnostic. The two-file structure works as strings, as file attachments, as JSON fields, or as multipart message payloads.

## Security Note

When context travels between agents, the attack surface grows. A compromised Agent A could inject malicious instructions into the session intent it generates. Two mitigations:

1. **Sanitize on receipt**: Every agent receiving a handshake should run `sanitize.py` on it before reading. This strips hidden Unicode injection payloads.
2. **Identity is immutable**: The `identity.md` originates from the human and should never be modified by an agent in the pipeline. If an agent needs to add context, it adds to `session-intent.md`, not to `identity.md`.

See also: [`../examples/agent-to-agent-handshake.md`](../examples/agent-to-agent-handshake.md) for a full A2A example.

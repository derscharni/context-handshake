---
type: example
scenario: agent-to-agent
description: Context handshake passed between two agents in a multi-agent pipeline
---

# Agent-to-Agent Context Handshake

This example shows how a Context Handshake travels between agents — no human in the loop.

The format is identical to a human-to-agent handshake. The difference: the orchestrating agent generates and passes it, not the human. The receiving agent knows who authorized the context, what scope applies, and when it was issued.

---

## Example: Research Agent → Writing Agent

```markdown
# context-handshake.md

## Authority
authorized-by: jens.scharnetzki
authorization-timestamp: 2026-04-10T14:23:00Z
authorization-scope: research, writing, ax-frameworks
session-id: sess_8f2a91bc

## Identity
role: AX Strategist — thought leader in Agent Experience design
working-style:
  - architektonisch — thinks in layers and systems
  - provokativ — a sharp wrong thesis beats a safe right one
constraints:
  - no em-dashes
  - English for all published content

## Context
source: research-agent-v1
source-timestamp: 2026-04-10T14:20:00Z
confidence: 0.85

## Session Intent
task: write a 400-word research note on Temporal Integrity in agent memory systems
output-format: markdown, critical angle mandatory
output-destination: /inbox/claude/2026-04-10-temporal-integrity.md
```

---

## Why this matters

When Agent A passes context to Agent B, Agent B doesn't have to infer:
- Who authorized this task
- What constraints apply
- How fresh the context is

The handshake makes provenance **declared**, not inferred.

Three Layers of Agent Memory Trust:
- Layer 1: Security — is the token safe?
- Layer 2: Provenance — who authorized this? (this file)
- Layer 3: Temporal integrity — is it still true? (confidence + timestamp)

---

## Minimal version

```markdown
# context-handshake.md
authorized-by: [human or agent id]
timestamp: [ISO 8601]
scope: [what the receiving agent is allowed to do]
task: [one sentence]
```

*See also: [SPEC.md](../SPEC.md)*

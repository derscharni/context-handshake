# Context Handshake

AI agents read your context. But they never ask what you actually need. Context Handshake is a lightweight spec for telling agents who you are and what this session is about — before they start guessing.

## What it is

Two markdown files that travel with you across tools, models, and sessions:

- **`identity.md`** — Who you are, how you work, what the agent should never do
- **`session-intent.md`** — What this session is for, what should exist at the end

No server. No auth. No vendor lock-in. Just structured context that any agent can read.

## Quickstart

1. Copy `identity-template.md` and fill in your details
2. Copy `session-intent-template.md` for each new session
3. Point your agent at both files (paste, attach, or reference via system prompt)

## Spec

See [SPEC.md](SPEC.md) for the full field definitions and validation rules.

## Validator

```bash
python3 validate.py identity.md session-intent.md
```

Checks that all required fields are present and non-empty.

## Examples

- [`examples/identity-example.md`](examples/identity-example.md) — A filled-out identity file
- [`examples/session-intent-writing.md`](examples/session-intent-writing.md) — Writing session
- [`examples/session-intent-technical.md`](examples/session-intent-technical.md) — Technical session

## Why

Every AI agent starts a session with zero context about you. Most try to infer it from your first message. Some guess well. Many don't. The result: you spend the first five minutes correcting assumptions instead of working.

Context Handshake gives you a portable, human-readable way to front-load the context that matters. It's not a protocol — it's a handshake.

## Article

[Coming soon — Context Handshake: The Missing Layer Between You and Your Agent]

## License

MIT

---

*by [Jens Scharnetzki](https://www.linkedin.com/in/scharnetzki/) — UX/AX Strategist, working on Agent Experience design and context sovereignty.*

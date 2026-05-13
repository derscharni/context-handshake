# Claude Code Integration

Add your Context Handshake to `~/.claude/CLAUDE.md` so every Claude Code session starts with your context.

## Setup

Sanitize and append your identity to your CLAUDE.md:

```bash
# Sanitize first — strips hidden Unicode injection payloads
python3 sanitize.py identity.md

# Then append the clean content
python3 -c "
from sanitize import load_handshake
ctx = load_handshake('identity.md')
open('~/.claude/CLAUDE.md', 'a').write(ctx['identity'])
"
```

Or use the library directly (recommended — no intermediate file):

```python
from sanitize import load_handshake
ctx = load_handshake("identity.md")
# ctx["identity"] is clean — append to CLAUDE.md or pass directly to the agent
```

Or reference it:

```markdown
# In ~/.claude/CLAUDE.md

## Context Handshake
See [identity.md](path/to/identity.md) for who I am and how I work.
```

## Per-session intent

At the start of a session, paste or attach your `session-intent.md`. Claude Code will use both files — the persistent identity from CLAUDE.md and the session-specific intent from your message.

## Project-level identity

For team projects, put `identity.md` in the project root. Claude Code picks up `CLAUDE.md` files from the working directory — rename your identity to `CLAUDE.md` or include it in an existing one:

```markdown
# In ./CLAUDE.md (project root)

## Team Context
We're a 4-person backend team. We write Go, test everything, deploy via ArgoCD.

## My Context
<!-- paste your identity.md fields here -->
```

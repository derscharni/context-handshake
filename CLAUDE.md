# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Validate one or more handshake files
python3 validate.py identity.md session-intent.md

# Sanitize (strip hidden Unicode) and check output
python3 sanitize.py identity.md session-intent.md

# Use as a library (primary safe integration pattern)
from sanitize import load_handshake
ctx = load_handshake("identity.md", "session-intent.md")
# ctx["identity"], ctx["session_intent"] are clean strings
# ctx["warnings"] lists anything stripped
```

No build step, no package manager, no external dependencies — stdlib only.

## Architecture

**Two-file spec.** A Context Handshake is `identity.md` (persistent, describes the user) + `session-intent.md` (per-session, describes the goal). Both use YAML frontmatter + freeform markdown. See `SPEC.md` for required/optional fields and validation rules.

**`validate.py`** — CLI validator. Determines which schema to apply via filename heuristic (`"identity" in name` → identity schema, `"session"/"intent"` → session schema). Falls back to field detection. Contains its own `parse_frontmatter()` — a custom line-by-line YAML parser, intentionally not using PyYAML to keep zero dependencies. Also contains `check_hidden_chars()` for security warnings.

**`sanitize.py`** — security tool and library entry point. `load_handshake()` is the function callers should use in integrations. The CLI mode prints status but does not write cleaned output to disk — the library return value is the only safe integration path. `HIDDEN_RANGES` defines the Unicode ranges stripped; these ranges are duplicated in `validate.py`'s `HIDDEN_CHAR_PATTERN` regex.

**Known duplication:** Hidden character patterns exist independently in both `validate.py` and `sanitize.py`. Changes to one must be mirrored in the other.

**A2A format.** `examples/agent-to-agent-handshake.md` introduces fields (`authorized-by`, `authorization-scope`, `confidence`, `source-timestamp`, `session-id`) that are **not defined in SPEC.md**. This is a separate informal format for multi-agent pipelines, not yet specced.

## Spec Version

Current spec is `v0.1.0`. `identity-template.md` and `session-intent-template.md` are the canonical starting points for new files.

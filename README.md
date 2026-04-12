# Context Handshake

AI agents read your context. But they never ask what you actually need. Context Handshake is a lightweight spec for telling agents who you are and what this session is about — before they start guessing.

**Designed for human-to-agent and agent-to-agent context dispatch.** The format is the same whether a human writes the handshake manually or an orchestrating agent generates it automatically.

## The Problem

Every AI interaction starts with a gap. The agent knows nothing about you — your expertise, your constraints, your communication style, the specific outcome you need. So it guesses. It defaults to generic, over-explained, one-size-fits-all responses. You spend the first five minutes correcting assumptions instead of working.

This isn't a model problem. It's a context problem. And it gets worse as agents become more autonomous: an agent that doesn't know your constraints will confidently do things you'd never approve.

Current solutions are platform-specific. OpenAI has Memory. Copilot has its context files. Claude has `CLAUDE.md`. None of them are portable. When you switch tools, your context stays behind.

## The Idea

Context Handshake is a portable, human-readable spec for agent context. Two markdown files:

- **`identity.md`** — Who you are, how you work, what the agent should never do. Persistent across sessions.
- **`session-intent.md`** — What this session is for, what should exist at the end that doesn't exist now. Per-session.

That's it. No server. No auth. No SDK. No vendor lock-in. Just structured context in files you own and control.

## Design Principles

**Portable.** Plain markdown with YAML frontmatter. Works with any agent, any model, any tool that can read text. Copy it, paste it, attach it, reference it in a system prompt.

**Human-readable.** You should be able to read your own context files and immediately understand what the agent knows about you. No embeddings, no vector stores, no opaque memory formats.

**User-owned.** The files live on your machine, in your repo, in your vault. Not in a vendor's cloud. You decide what to share, when, and with whom.

**Minimal.** Five required fields in identity, three in session-intent. Enough structure to be useful, little enough to actually fill out.

## Quickstart

1. Copy `identity-template.md` and fill in your details
2. Copy `session-intent-template.md` for each new session
3. Point your agent at both files (paste, attach, or reference via system prompt)

Already using a specific tool? See the integration guides:

- [**Claude Code**](integrations/claude-code.md) — Add to `~/.claude/CLAUDE.md`
- [**ChatGPT**](integrations/chatgpt.md) — Map to Custom Instructions
- [**Cursor / Copilot**](integrations/cursor-copilot.md) — Drop into `.cursorrules` or `.github/copilot-instructions.md`

## Spec

See [SPEC.md](SPEC.md) for the full field definitions and validation rules.

## Validator

```bash
python3 validate.py identity.md session-intent.md
```

Checks that all required fields are present and non-empty.

## Examples

- [**EXAMPLE.md**](EXAMPLE.md) — Full walkthrough: same prompt with and without Context Handshake
- [`examples/identity-example.md`](examples/identity-example.md) — Product designer identity
- [`examples/identity-consumer.md`](examples/identity-consumer.md) — Everyday consumer identity
- [`examples/session-intent-writing.md`](examples/session-intent-writing.md) — Writing session
- [`examples/session-intent-technical.md`](examples/session-intent-technical.md) — Technical session
- [`examples/session-intent-entertainment.md`](examples/session-intent-entertainment.md) — Family movie night

## Where This Fits

Context Handshake isn't trying to replace platform-specific memory systems. It fills the gap between them:

```
┌─────────────────────────────────────────────┐
│  Platform Memory (OpenAI, Claude, Copilot)  │  Vendor-specific, not portable
├─────────────────────────────────────────────┤
│  Context Handshake (identity + intent)      │  Portable, user-owned, human-readable
├─────────────────────────────────────────────┤
│  Raw conversation                           │  No persistent context
└─────────────────────────────────────────────┘
```

Think of it as the layer you carry with you. Your platform memory makes one tool smarter about you. Your Context Handshake makes every tool smarter about you.

## Security

Context Handshake files are text that gets fed to an AI agent. If someone injects hidden Unicode characters into your files — zero-width spaces, invisible formatters, tag characters — those characters are invisible to you but readable by the agent. This is a real attack vector ([steganographic prompt injection](https://embracethered.com/blog/posts/2024/hiding-and-finding-text-with-unicode-tags/)).

The built-in sanitizer strips these characters automatically:

```bash
# Sanitize before dispatching to any agent
python3 sanitize.py identity.md session-intent.md

# Or use as a library
from sanitize import load_handshake
ctx = load_handshake("identity.md", "session-intent.md")
# ctx["identity"] and ctx["session_intent"] are clean
# ctx["warnings"] lists anything that was stripped
```

The validator (`validate.py`) also checks for hidden characters and warns if found.

## Part of the Trust Stack

Context Handshake is Layer 2 (Authorization and Context) of the [Trust Stack](https://github.com/derscharni/trust-stack). For the full sovereign context layer — sanitizing, compression, routing, and archival — see [membrane](https://github.com/derscharni/membrane).

## FAQ

**Why not just use a system prompt?**
You can — and Context Handshake works great as a system prompt. The difference is structure. A freeform system prompt is hard to validate, hard to version, hard to share. A structured handshake file can be checked, diffed, and evolved over time.

**Why markdown and not JSON/YAML?**
Because humans need to read and edit these files. Markdown with YAML frontmatter gives you structure where it matters (required fields, validation) and flexibility where it matters (freeform context below the frontmatter).

**Does this work with [specific agent/tool]?**
If it can read text, yes. Paste the contents, attach the file, or reference it in the system prompt. The format is deliberately simple so it works everywhere.

**What about privacy?**
You control what goes in the files. Don't include anything you wouldn't paste into a chat with that agent. The identity file is about working style and constraints, not personal data.

## Related Work

**Karpathy's Wiki Loop.** Andrej Karpathy describes a personal LLM knowledge system: raw sources go in, an agent compiles markdown wiki articles, Obsidian serves as the IDE, and Q&A outputs feed back into the wiki. No RAG needed at ~100 articles. The agent maintains its own index files. It works — and it independently validates the index-based approach (SESSION.md, INDEX.md as agent-maintained context layers instead of vector search).

But Karpathy's system has one author, one agent, one trust level. He's alone. The moment a second agent writes into the same wiki — or raw sources contain compromised content that the compiler agent ingests uncritically — new questions emerge that his architecture doesn't answer: Who wrote this article? Was it the agent or was it injected? How does a reading agent distinguish trusted from compromised knowledge? Context Handshake addresses one piece of this: every session that writes into a shared system should declare its identity and intent. Not as security theater, but as the minimum legible context for anyone — human or agent — reviewing what happened later.

**Platform-specific context systems.** OpenAI Memory, GitHub Copilot's context files, Anthropic's `CLAUDE.md`, Cursor Rules. All solve the same problem but lock your context into one platform. Context Handshake is the portable layer underneath.

**MCP (Model Context Protocol).** Anthropic's protocol for tool integration. Context Handshake is complementary — MCP defines how agents connect to tools, Context Handshake defines what the agent should know about the human before using them.

## Article

[Coming soon — Context Handshake: The Missing Layer Between You and Your Agent]

## Contributing

This is an early spec. If you use it and something's missing or broken, open an issue. If you've adapted it for a specific tool or workflow, PRs are welcome.

## License

MIT

---

*by [Jens Scharnetzki](https://www.linkedin.com/in/scharnetzki/) — working on Agent Experience design and context sovereignty.*

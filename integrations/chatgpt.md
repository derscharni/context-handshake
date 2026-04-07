# ChatGPT Integration

## Custom Instructions

Copy the contents of your `identity.md` frontmatter into ChatGPT's Custom Instructions (Settings → Personalization → Custom Instructions).

Map the fields:

| Context Handshake | ChatGPT field |
|---|---|
| `name`, `role`, `working-style` | "What would you like ChatGPT to know about you?" |
| `communication`, `constraints` | "How would you like ChatGPT to respond?" |

## Per-session intent

Start a new conversation by pasting your `session-intent.md` as the first message. ChatGPT will use your Custom Instructions (identity) plus the session intent together.

## GPT Builder

If you use custom GPTs, paste your `identity.md` into the GPT's system instructions. This gives every conversation with that GPT your context automatically.

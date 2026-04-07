# Context Handshake in Practice

A walkthrough showing what changes when an agent has your context.

## Setup

Alex is a product designer. They filled out their `identity.md` once:

```yaml
---
name: Alex Chen
role: Senior Product Designer at a B2B SaaS company
working-style:
  - Visual thinker — starts with sketches and flows before writing
  - Prefers concrete examples over abstract principles
  - Works in short bursts with frequent check-ins
communication:
  - Concise, but explain the why behind recommendations
  - Use bullet points and headers for scannability
  - Flag assumptions explicitly
constraints:
  - Never generate placeholder content in user-facing text
  - Never suggest features without considering the maintenance cost
frameworks:
  - Jobs to Be Done
  - Double Diamond
infrastructure: Figma, Linear, Next.js frontend, Python backend
---
```

For today's session, they wrote a quick `session-intent.md`:

```yaml
---
date: 2026-04-07
session-type: writing
goal: A blog post draft (~800 words) explaining why onboarding flows fail for power users
constraints:
  - Practitioner audience, not academic
  - Include at least one concrete product example
  - No generic conclusions
active-context: We shipped a new onboarding last quarter. Activation improved for new users but power users started skipping it entirely.
---
```

## The Difference

### Without Context Handshake

**Prompt:** "Write an opening paragraph about why onboarding fails for power users."

> Onboarding is one of the most critical parts of any software product. It's the first impression users get, and it can make or break retention. But while most teams focus on optimizing onboarding for new users, they often overlook a key segment: power users. In this article, we'll explore why traditional onboarding flows fall short for experienced users and what product teams can do to bridge the gap.

Generic. Explains what onboarding is (the reader already knows). Ends with "we'll explore" filler.

### With Context Handshake

**Same prompt**, but the agent has both files:

> We redesigned our onboarding last quarter. Activation went up 15% for new signups. And our power users? They started hitting "Skip" on step one and never looked back. The flow we built to reduce friction became the friction. That's the pattern nobody warns you about: onboarding optimized for first-time clarity actively repels the people who already know what they want. The job the power user is hiring your product for isn't "learn how this works" — it's "get me to my workspace in under ten seconds."

Concrete (uses the team's actual situation from `active-context`). Uses JTBD framing (from `frameworks`). Practitioner tone (from `constraints`). No filler.

## What the Agent Used

| Handshake field | How it shaped the output |
|---|---|
| `working-style: concrete examples` | Led with a real scenario, not a definition |
| `frameworks: Jobs to Be Done` | Framed the problem as a job mismatch |
| `constraints: no generic conclusions` | Ended with a specific insight, not "let's explore" |
| `active-context` | Referenced the actual product situation |
| `communication: concise` | Skipped the "onboarding is important" preamble |

## Key Takeaway

The agent didn't become smarter. It became relevant. The same model, the same prompt — but with five minutes of structured context, the output went from "could be about any product" to "this is about our product."

That's the handshake.

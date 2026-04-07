# Cursor / GitHub Copilot Integration

## Cursor Rules

Cursor reads `.cursorrules` from your project root. Paste your identity fields there:

```bash
cp identity.md .cursorrules
```

Or append to an existing rules file:

```bash
echo "" >> .cursorrules
cat identity.md >> .cursorrules
```

## GitHub Copilot

Copilot reads `.github/copilot-instructions.md` from your repo. Same approach:

```bash
mkdir -p .github
cp identity.md .github/copilot-instructions.md
```

## Per-session intent

Both tools work with chat. Start a chat session by pasting your `session-intent.md` — the tool combines it with the persistent rules file automatically.

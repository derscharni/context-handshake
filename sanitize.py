#!/usr/bin/env python3
"""
Context Handshake Sanitizer
Strips hidden Unicode characters from identity.md and session-intent.md
before they are dispatched to any agent.

Protects against steganographic prompt injection via the context layer.
See: https://github.com/derscharni/context-handshake
"""

import re
import sys
from pathlib import Path

HIDDEN_RANGES = [
    (0x0001, 0x0008),   # C0 controls (before tab)
    (0x000B, 0x000C),   # VT, FF
    (0x000E, 0x001F),   # C0 controls (after CR)
    (0x007F, 0x007F),   # DEL
    (0x00AD, 0x00AD),   # Soft Hyphen
    (0x180E, 0x180E),   # Mongolian Vowel Separator
    (0x200B, 0x200F),   # Zero-Width spaces
    (0x200C, 0x200D),   # Zero-Width Joiners
    (0x202A, 0x202E),   # Directional Overrides
    (0x2028, 0x2029),   # Line/Paragraph Separators (YAML newline injection)
    (0x2060, 0x2064),   # Invisible Characters
    (0x2066, 0x2069),   # Directional Isolates
    (0xFE00, 0xFE0F),   # Variation Selectors
    (0xFEFF, 0xFEFF),   # BOM / Zero-Width No-Break Space
    (0xE0000, 0xE007F), # Tag Characters
]

HIDDEN_PATTERN = re.compile(
    "[" + "".join(
        rf"\U{lo:08X}-\U{hi:08X}" for lo, hi in HIDDEN_RANGES
    ) + "]"
)


def sanitize(text: str) -> tuple[str, list[str]]:
    found = []
    def replace(match):
        char = match.group(0)
        found.append(f"U+{ord(char):04X}")
        return ""
    cleaned = HIDDEN_PATTERN.sub(replace, text)
    return cleaned, found


def sanitize_file(path) -> tuple[str, list[str]]:
    content = Path(path).read_text(encoding="utf-8")
    return sanitize(content)


def load_handshake(identity_path, session_intent_path=None, verbose=False):
    """
    Load and sanitize a Context Handshake.
    Returns dict with 'identity', 'session_intent', 'warnings'.
    """
    result = {"identity": "", "session_intent": "", "warnings": []}

    identity_path = Path(identity_path)
    if not identity_path.exists():
        raise FileNotFoundError(f"identity.md not found: {identity_path}")

    content, found = sanitize_file(identity_path)
    result["identity"] = content
    if found:
        msg = f"[sanitize] stripped {len(found)} hidden chars from identity.md: {', '.join(found)}"
        result["warnings"].append(msg)
        if verbose:
            print(msg, file=sys.stderr)

    if session_intent_path:
        session_intent_path = Path(session_intent_path)
        if not session_intent_path.exists():
            result["warnings"].append(f"[sanitize] session-intent not found: {session_intent_path}")
        else:
            content, found = sanitize_file(session_intent_path)
            result["session_intent"] = content
            if found:
                msg = f"[sanitize] stripped {len(found)} hidden chars from session-intent.md: {', '.join(found)}"
                result["warnings"].append(msg)
                if verbose:
                    print(msg, file=sys.stderr)

    return result


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    inplace = "--inplace" in sys.argv

    if not args:
        print("Usage: sanitize.py [--inplace] <identity.md> [session-intent.md]")
        print("  --inplace  write cleaned content back to the original files")
        sys.exit(1)

    identity = Path(args[0])
    session = Path(args[1]) if len(args) > 1 else None
    try:
        ctx = load_handshake(identity, session, verbose=True)
        dirty = [w for w in ctx["warnings"] if "stripped" in w]
        if not dirty:
            print("Clean — no hidden characters found")
        elif inplace:
            identity.write_text(ctx["identity"], encoding="utf-8")
            if session and ctx["session_intent"]:
                session.write_text(ctx["session_intent"], encoding="utf-8")
            print(f"Sanitized — {len(dirty)} file(s) cleaned in place")
        else:
            print(f"WARNING: {len(dirty)} file(s) contain hidden chars — re-run with --inplace to clean")
        sys.exit(0)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

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
    (0x200B, 0x200F),
    (0x2060, 0x2064),
    (0xFE00, 0xFE0F),
    (0xE0000, 0xE007F),
    (0x202A, 0x202E),
    (0x2066, 0x2069),
    (0xFEFF, 0xFEFF),
    (0x00AD, 0x00AD),
    (0x180E, 0x180E),
    (0x200C, 0x200D),
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
        if session_intent_path.exists():
            content, found = sanitize_file(session_intent_path)
            result["session_intent"] = content
            if found:
                msg = f"[sanitize] stripped {len(found)} hidden chars from session-intent.md: {', '.join(found)}"
                result["warnings"].append(msg)
                if verbose:
                    print(msg, file=sys.stderr)

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sanitize.py <identity.md> [session-intent.md]")
        sys.exit(1)
    identity = Path(sys.argv[1])
    session = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    try:
        ctx = load_handshake(identity, session, verbose=True)
        if not ctx["warnings"]:
            print("Clean — no hidden characters found")
        else:
            print(f"Sanitized — {len(ctx['warnings'])} file(s) had hidden chars")
        sys.exit(0)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

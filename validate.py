#!/usr/bin/env python3
"""
Context Handshake Validator
Checks identity.md and session-intent.md against the spec.
"""

import sys
import re
from pathlib import Path

IDENTITY_REQUIRED = ["name", "role", "working-style", "communication", "constraints"]
IDENTITY_LISTS = ["working-style", "communication", "constraints"]

SESSION_REQUIRED = ["date", "session-type", "goal", "constraints"]
SESSION_LISTS = ["constraints"]
SESSION_TYPES = ["writing", "research", "technical", "framework", "exploration"]


def parse_frontmatter(text):
    """Extract YAML frontmatter as a simple dict."""
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None

    fields = {}
    current_key = None
    current_list = []

    for line in match.group(1).split("\n"):
        if line.startswith("#") or not line.strip():
            continue

        list_match = re.match(r"^\s+-\s+(.*)", line)
        if list_match:
            if current_key:
                current_list.append(list_match.group(1).strip())
            continue

        kv_match = re.match(r"^(\S+):\s*(.*)", line)
        if kv_match:
            if current_key and current_list:
                fields[current_key] = current_list
            current_key = kv_match.group(1)
            current_list = []
            value = kv_match.group(2).strip()
            if value:
                fields[current_key] = value
                current_key = None

    if current_key and current_list:
        fields[current_key] = current_list

    return fields


def validate_identity(path):
    text = Path(path).read_text()
    fields = parse_frontmatter(text)
    if fields is None:
        return ["No YAML frontmatter found"]

    errors = []
    for field in IDENTITY_REQUIRED:
        if field not in fields:
            errors.append(f"Missing required field: {field}")
        elif not fields[field]:
            errors.append(f"Empty required field: {field}")

    for field in IDENTITY_LISTS:
        if field in fields and not isinstance(fields[field], list):
            errors.append(f"{field} should be a list")
        elif field in fields and len(fields[field]) == 0:
            errors.append(f"{field} list is empty")

    return errors


def validate_session(path):
    text = Path(path).read_text()
    fields = parse_frontmatter(text)
    if fields is None:
        return ["No YAML frontmatter found"]

    errors = []
    for field in SESSION_REQUIRED:
        if field not in fields:
            errors.append(f"Missing required field: {field}")
        elif not fields[field]:
            errors.append(f"Empty required field: {field}")

    if "session-type" in fields and fields["session-type"] not in SESSION_TYPES:
        errors.append(
            f"Invalid session-type: '{fields['session-type']}'. "
            f"Must be one of: {', '.join(SESSION_TYPES)}"
        )

    for field in SESSION_LISTS:
        if field in fields and not isinstance(fields[field], list):
            errors.append(f"{field} should be a list")

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate.py <file.md> [file2.md ...]")
        print("Validates identity.md and session-intent.md files against the Context Handshake spec.")
        sys.exit(1)

    all_valid = True
    for path in sys.argv[1:]:
        p = Path(path)
        if not p.exists():
            print(f"  {path}: File not found")
            all_valid = False
            continue

        name = p.name.lower()
        if "identity" in name:
            errors = validate_identity(path)
        elif "session" in name or "intent" in name:
            errors = validate_session(path)
        else:
            text = p.read_text()
            fields = parse_frontmatter(text)
            if fields and "session-type" in fields:
                errors = validate_session(path)
            elif fields and "name" in fields:
                errors = validate_identity(path)
            else:
                print(f"  {path}: Cannot determine file type (use 'identity' or 'session' in filename)")
                all_valid = False
                continue

        if errors:
            print(f"  {path}:")
            for e in errors:
                print(f"    - {e}")
            all_valid = False
        else:
            print(f"  {path}: Valid")

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()

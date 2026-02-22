#!/usr/bin/env python3
"""Validate a Claude Code skill's structure and quality.

Usage:
    python3 quick_validate.py <path/to/skill>

Checks:
    - SKILL.md existence and valid YAML frontmatter
    - Required fields (name, description)
    - Naming conventions (kebab-case, matches directory)
    - Description quality (trigger phrases)
    - Body line count (warns >500)
    - Referenced files exist
    - No extraneous documentation files
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


EXTRANEOUS_FILES = {
    "README.md", "README.zh.md", "CHANGELOG.md",
    "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md",
    "CONTRIBUTING.md", "SETUP.md",
}

ALLOWED_FRONTMATTER = {
    "name", "description", "version", "tools", "license",
    "disable-model-invocation", "user-invocable", "argument-hint",
    "metadata", "compatibility",
}


def parse_frontmatter(content: str) -> tuple[dict[str, str], str, list[str]]:
    """Parse YAML frontmatter from SKILL.md. Returns (fields, body, errors)."""
    errors = []

    if not content.startswith("---"):
        errors.append("SKILL.md must start with YAML frontmatter (---)")
        return {}, content, errors

    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("SKILL.md frontmatter not properly closed (missing second ---)")
        return {}, content, errors

    yaml_text = parts[1].strip()
    body = parts[2].strip()
    fields: dict[str, str] = {}

    current_key = None
    current_value_lines: list[str] = []

    for line in yaml_text.splitlines():
        # Check for new key
        match = re.match(r'^(\w[\w-]*):\s*(.*)', line)
        if match:
            # Save previous key
            if current_key:
                fields[current_key] = " ".join(current_value_lines).strip()
            current_key = match.group(1)
            val = match.group(2).strip()
            if val == ">-" or val == ">":
                current_value_lines = []
            else:
                current_value_lines = [val]
        elif current_key and line.startswith("  "):
            current_value_lines.append(line.strip())

    # Save last key
    if current_key:
        fields[current_key] = " ".join(current_value_lines).strip()

    return fields, body, errors


def validate(skill_path: Path) -> list[str]:
    """Validate a skill directory. Returns list of issues."""
    issues: list[str] = []
    warnings: list[str] = []

    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        issues.append("SKILL.md not found")
        return issues

    content = skill_md.read_text()
    fields, body, parse_errors = parse_frontmatter(content)
    issues.extend(parse_errors)

    # Required fields
    if "name" not in fields:
        issues.append("Missing required field: name")
    if "description" not in fields:
        issues.append("Missing required field: description")

    # Name validation
    name = fields.get("name", "")
    if name:
        if not re.match(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$', name):
            issues.append(f"Name '{name}' is not valid kebab-case")
        if name != skill_path.name:
            warnings.append(f"Name '{name}' doesn't match directory '{skill_path.name}'")

    # Description quality
    desc = fields.get("description", "")
    if desc:
        if len(desc) < 30:
            issues.append(f"Description too short ({len(desc)} chars). Be more comprehensive.")
        quoted = re.findall(r'"[^"]+?"', desc)
        if len(quoted) < 2:
            warnings.append(
                f"Description has {len(quoted)} quoted trigger phrase(s). "
                "Recommend 3-5 for reliable triggering."
            )
    else:
        issues.append("Description is empty")

    # Body size
    body_lines = len(body.splitlines())
    if body_lines > 500:
        warnings.append(
            f"Body is {body_lines} lines (target: <500). "
            "Consider moving details to references/."
        )
    elif body_lines > 400:
        warnings.append(f"Body is {body_lines} lines — approaching 500-line target.")

    # Check for referenced files (skip those inside code blocks)
    body_no_codeblocks = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
    ref_pattern = re.findall(r'`((?:references|scripts|assets|examples)/[^`]+)`', body_no_codeblocks)
    for ref in ref_pattern:
        ref_path = skill_path / ref
        if not ref_path.exists():
            issues.append(f"Referenced file not found: {ref}")

    # Extraneous files
    for f in skill_path.iterdir():
        if f.is_file() and f.name in EXTRANEOUS_FILES:
            warnings.append(
                f"Extraneous file: {f.name} — skills should not include "
                "user-facing documentation. The skill IS the documentation."
            )

    # Unknown frontmatter fields
    for key in fields:
        if key not in ALLOWED_FRONTMATTER:
            warnings.append(f"Unknown frontmatter field: {key}")

    # Print results
    if issues:
        print(f"FAIL — {len(issues)} error(s):")
        for i in issues:
            print(f"  [ERROR] {i}")
    else:
        print("PASS — no errors")

    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  [WARN] {w}")

    return issues


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        msg = "Usage: python3 quick_validate.py <path/to/skill>"
        if sys.argv[1:] and sys.argv[1] in ("-h", "--help"):
            print(msg)
            sys.exit(0)
        print(msg, file=sys.stderr)
        sys.exit(1)

    skill_path = Path(sys.argv[1]).resolve()
    if not skill_path.is_dir():
        print(f"Error: '{skill_path}' is not a directory", file=sys.stderr)
        sys.exit(1)

    issues = validate(skill_path)
    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()

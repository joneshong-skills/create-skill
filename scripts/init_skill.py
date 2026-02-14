#!/usr/bin/env python3
"""Initialize a new Claude Code skill with proper structure and templates.

Usage:
    python3 init_skill.py <skill-name> [--path <output-directory>]

Examples:
    python3 init_skill.py pdf-editor
    python3 init_skill.py pdf-editor --path ~/my-plugins/skills/
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKILLS_DIR = Path.home() / ".claude" / "skills"


def validate_name(name: str) -> str | None:
    """Validate skill name is kebab-case. Returns error message or None."""
    if not re.match(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$', name):
        return (
            f"Invalid skill name '{name}'. "
            "Must be kebab-case (lowercase letters, numbers, hyphens). "
            "Examples: pdf-editor, code-review, my-skill"
        )
    if len(name) > 50:
        return f"Skill name too long ({len(name)} chars). Max 50."
    return None


SKILL_MD_TEMPLATE = '''---
name: {name}
description: >-
  TODO: Describe when this skill should be used.
  Include 3-5 specific trigger phrases in quotes.
  Example: This skill should be used when the user asks to "do X",
  "do Y", "do Z", mentions keyword, or discusses topic area.
version: 0.1.0
---

# {title}

TODO: Brief description of purpose (1-2 sentences).

## Core Concepts

TODO: Essential knowledge Claude doesn't already have.

## Workflow

TODO: Step-by-step procedures.

### Step 1: ...

### Step 2: ...

## Quick Reference

TODO: Tables, cheat sheets, decision trees.

## Additional Resources

### Reference Files
- **`references/guide.md`** — TODO: Description and when to read it

### Scripts
- **`scripts/example.py`** — TODO: Description
'''

EXAMPLE_REFERENCE = '''# Reference Guide

TODO: Detailed documentation that supports the skill.

## Section 1

...

## Section 2

...
'''

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""TODO: Description of what this script does.

Usage:
    python3 example.py [args]
"""

import sys


def main():
    print("TODO: Implement this script")


if __name__ == "__main__":
    main()
'''

EXAMPLE_ASSET_README = '''# Assets

Place files here that are used in the skill's output but should NOT be loaded
into Claude's context window. Examples: templates, images, fonts, boilerplate code.
'''


def init_skill(name: str, base_path: Path) -> Path:
    """Create skill directory with template files."""
    skill_dir = base_path / name

    if skill_dir.exists():
        print(f"Error: '{skill_dir}' already exists.", file=sys.stderr)
        sys.exit(1)

    # Create directories
    skill_dir.mkdir(parents=True)
    (skill_dir / "scripts").mkdir()
    (skill_dir / "references").mkdir()
    (skill_dir / "assets").mkdir()

    # Generate title from name
    title = name.replace("-", " ").title()

    # Write files
    (skill_dir / "SKILL.md").write_text(
        SKILL_MD_TEMPLATE.format(name=name, title=title)
    )
    (skill_dir / "references" / "guide.md").write_text(EXAMPLE_REFERENCE)
    (skill_dir / "scripts" / "example.py").write_text(EXAMPLE_SCRIPT)
    (skill_dir / "assets" / ".gitkeep").write_text("")

    return skill_dir


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new Claude Code skill"
    )
    parser.add_argument("name", help="Skill name (kebab-case)")
    parser.add_argument(
        "--path", default=str(SKILLS_DIR),
        help=f"Output directory (default: {SKILLS_DIR})"
    )
    args = parser.parse_args()

    error = validate_name(args.name)
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    base_path = Path(args.path)
    skill_dir = init_skill(args.name, base_path)

    print(f"Skill '{args.name}' created at {skill_dir}/")
    print()
    print("Files created:")
    for f in sorted(skill_dir.rglob("*")):
        if f.is_file():
            rel = f.relative_to(skill_dir)
            print(f"  {rel}")
    print()
    print("Next steps:")
    print(f"  1. Edit {skill_dir}/SKILL.md — fill in TODO placeholders")
    print(f"  2. Customize or remove placeholder files in scripts/, references/, assets/")
    print(f"  3. Validate: python3 ~/.claude/skills/create-skill/scripts/quick_validate.py {skill_dir}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Package a Claude Code skill into a distributable .skill file.

Usage:
    python3 package_skill.py <path/to/skill> [output-directory]

The .skill file is a zip archive with .skill extension containing
all skill files (excluding .git, __pycache__, etc.).
Runs validation automatically before packaging.
"""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

EXCLUDE_PATTERNS = {
    ".git", "__pycache__", ".DS_Store", "*.pyc",
    ".env", "node_modules", ".skill",
}

VALIDATOR = Path(__file__).parent / "quick_validate.py"


def should_exclude(path: Path, skill_root: Path) -> bool:
    """Check if a path should be excluded from packaging."""
    rel = path.relative_to(skill_root)
    parts = rel.parts
    for part in parts:
        if part in EXCLUDE_PATTERNS:
            return True
        for pattern in EXCLUDE_PATTERNS:
            if pattern.startswith("*") and part.endswith(pattern[1:]):
                return True
    return False


def package_skill(skill_path: Path, output_dir: Path) -> Path | None:
    """Validate and package a skill. Returns .skill file path or None on failure."""
    skill_path = skill_path.resolve()
    skill_name = skill_path.name

    # Run validation first
    print(f"Validating '{skill_name}'...")
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(skill_path)],
        capture_output=True, text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        print("Packaging aborted — fix validation errors first.")
        return None

    # Package
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{skill_name}.skill"

    print(f"\nPackaging '{skill_name}'...")
    file_count = 0
    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(skill_path.rglob("*")):
            if f.is_file() and not should_exclude(f, skill_path):
                arcname = f"{skill_name}/{f.relative_to(skill_path)}"
                zf.write(f, arcname)
                file_count += 1

    size_kb = output_file.stat().st_size / 1024
    print(f"Created: {output_file} ({file_count} files, {size_kb:.1f} KB)")
    return output_file


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        msg = "Usage: python3 package_skill.py <path/to/skill> [output-dir]"
        if sys.argv[1:] and sys.argv[1] in ("-h", "--help"):
            print(msg)
            sys.exit(0)
        print(msg, file=sys.stderr)
        sys.exit(1)

    skill_path = Path(sys.argv[1]).resolve()
    output_dir = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path.cwd()

    if not skill_path.is_dir():
        print(f"Error: '{skill_path}' is not a directory", file=sys.stderr)
        sys.exit(1)

    result = package_skill(skill_path, output_dir)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()

---
name: create-skill
description: >-
  Guide for creating effective skills. This skill should be used when users
  want to create a new skill, update an existing skill, "make a new skill",
  "build a skill", "add a skill", "write a skill", "generate a skill",
  "set up a skill", or discusses creating Claude Code skills,
  skill development, skill templates, or SKILL.md authoring.
version: 0.3.0
tools: Read, Glob, Grep, Bash, Edit, Write, WebSearch
argument-hint: "<skill description or name>"
---

# Create Skill for Claude Code

Guide the creation of effective, well-structured Claude Code skills. A skill is an
"onboarding guide" that transforms Claude from a general-purpose agent into a specialized one
equipped with procedural knowledge no model fully possesses.

## Core Principles

### Concise is Key

The context window is a shared resource. Skills share it with system prompt, conversation
history, other skills' metadata, and the user's request.

**Default assumption: Claude is already very smart.** Only add what Claude doesn't know.
Challenge every paragraph: "Does this justify its token cost?" Prefer concise examples
over verbose explanations.

### Set Appropriate Degrees of Freedom

Match specificity to the task's fragility:

| Freedom | When | Form |
|---------|------|------|
| **High** | Multiple valid approaches, context-dependent | Text instructions, heuristics |
| **Medium** | Preferred pattern exists, some variation OK | Pseudocode, parameterized scripts |
| **Low** | Fragile operations, strict sequence required | Specific scripts, few parameters |

Think of it as a path: a narrow cliff bridge needs guardrails (low freedom);
an open field allows many routes (high freedom).

### Progressive Disclosure

Skills use a three-level loading system:

1. **Metadata** (name + description) — Always in context (~100 words)
2. **SKILL.md body** — Loaded when skill triggers (target: <500 lines)
3. **Bundled resources** — Loaded on demand by Claude (unlimited)

**Critical**: The `description` field is the ONLY part always visible to Claude.
All trigger conditions and "when to use" information MUST be in the description.
Writing "When to Use" sections in the body is wasteful — the body loads only AFTER triggering.

## Specification Freshness Check

Before creating or updating a skill, verify alignment with the latest official specification.
Run this check periodically (every 2-4 weeks) or when encountering unfamiliar frontmatter fields.

### Quick Check (GitHub API)

```bash
# Check recent changes to Anthropic's skill spec
gh api repos/anthropics/skills/commits --jq '.[0:5] | .[] | {date: .commit.author.date, message: .commit.message}'
```

If new commits exist since the `Last verified` date in `references/official-spec.md`:

1. Fetch the latest skill-creator SKILL.md and `quick_validate.py` from Anthropic
2. Compare against `references/official-spec.md` § Frontmatter Fields and § Content Guidelines
3. If differences found: update `references/official-spec.md`, note changes in § Changelog,
   and adjust this skill's guidance accordingly
4. Update `Last verified` date

### Deep Check (Web Search)

Use WebSearch when the quick check shows significant changes, or quarterly:

- `"agent skills specification" site:agentskills.io` — open standard updates
- `"claude code skills" site:code.claude.com` — Claude Code-specific changes
- `anthropic skills changelog` — release notes

See `references/official-spec.md` § Freshness Check Queries for the full query list.

## Skill Creation Workflow

### Phase 1: Understand with Concrete Examples

**Do not skip this phase.** Before planning structure, collect concrete usage examples:

1. "What should the skill do? Give 2-3 example tasks."
2. "What would a user say to trigger this skill?" — Collect 3-5 specific phrases.
3. "What would Claude need to know that it doesn't already?"

For each example, consider: How would this be executed from scratch? What knowledge or
resources would make it faster the second time?

Keep questions concise. Ask 2-3 at a time, not all at once.

### Phase 2: Plan Reusable Contents

Analyze the concrete examples to identify reusable resources:

| Resource | Purpose | Example |
|----------|---------|---------|
| `scripts/` | Deterministic, repeatable operations | `rotate_pdf.py`, `validate.py` |
| `references/` | Domain knowledge loaded on demand | `schema.md`, `api-docs.md` |
| `assets/` | Files used in output, not loaded into context | `template/`, `logo.png` |

Also determine:
- **Invocation style**: Auto-invoke (default) or user-only (`disable-model-invocation: true`)?
- **Placement**: User skill (`~/.claude/skills/`) or plugin skill?

### Phase 3: Initialize the Skill

Run the scaffolding script to create the directory structure:

```bash
python3 ~/.claude/skills/create-skill/scripts/init_skill.py <skill-name> [--path <dir>]
```

The script creates:
- `SKILL.md` with frontmatter template and TODO placeholders
- `scripts/`, `references/`, `assets/` directories with example files
- Validates naming conventions (kebab-case)

Default path: `~/.claude/skills/<skill-name>/`

After initialization, customize or remove placeholder files as needed.

### Phase 4: Edit the Skill

Remember: **the skill is being written for another Claude instance to use.**
Include information that would be beneficial and non-obvious to Claude.

#### Frontmatter (Required)

```yaml
---
name: skill-name
description: >-
  This skill should be used when the user asks to "phrase 1", "phrase 2",
  "phrase 3", mentions keyword, or discusses topic area.
version: 0.1.0
---
```

Rules:
- `name`: kebab-case identifier
- `description`: Include BOTH what the skill does AND all trigger phrases/contexts.
  This is the primary triggering mechanism — be comprehensive.
- Only `name` and `description` are required. Optional fields: `version`, `tools`,
  `disable-model-invocation`, `user-invocable`, `argument-hint`, `license`

#### Body Content

Write in **imperative/infinitive form** (verb-first), never second person:
- Good: "Parse the config file before processing."
- Bad: "You should parse the config file."

Body structure:

```markdown
# Skill Title

Brief purpose (1-2 sentences).

## Core Concepts / Principles
[Essential knowledge Claude doesn't already have]

## Workflow
[Step-by-step procedures — the main content]

## Quick Reference
[Tables, cheat sheets, decision trees]

## Additional Resources

### Reference Files
- **`references/file.md`** — Description and when to read it
```

**Size guidelines:**
- Body: under 500 lines. If approaching this limit, split into reference files.
- Reference files over 100 lines: include a TOC at the top.
- Reference files over 10k words: include grep search patterns in SKILL.md.

#### Start with Reusable Contents

Implement `scripts/`, `references/`, and `assets/` files first, then write SKILL.md
to reference them. Test added scripts by actually running them.

Delete any placeholder files from `init_skill.py` that aren't needed.

#### Consult Design Patterns

- **Multi-step processes**: See `references/workflows.md`
- **Output format/quality standards**: See `references/output-patterns.md`
- **Common skill archetypes**: See `references/skill-patterns.md`

### Phase 5: Validate

Run the validation script:

```bash
python3 ~/.claude/skills/create-skill/scripts/quick_validate.py <path/to/skill>
```

The script checks:
- SKILL.md existence and valid YAML frontmatter
- Required fields (`name`, `description`)
- Naming conventions (kebab-case, name matches directory)
- Description quality (starts with trigger context, includes quoted phrases)
- Body line count (warns if >500 lines)
- All referenced files exist
- No extraneous documentation files

### Phase 6: Package (Optional)

For distributing skills as `.skill` files:

```bash
python3 ~/.claude/skills/create-skill/scripts/package_skill.py <path/to/skill> [output-dir]
```

Creates a `.skill` file (zip format) after running validation automatically.

### Phase 7: Iterate

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Update SKILL.md or resources
4. Test again

Use the `skill-optimizer` skill to systematically analyze and improve skills after use.

## What NOT to Include

A skill should only contain files that directly support its functionality. Do NOT create:

- README.md, CHANGELOG.md, INSTALLATION_GUIDE.md
- User-facing documentation (the skill IS the documentation)
- Setup/testing procedures (those belong in scripts)
- Files that duplicate information already in SKILL.md

The audience is an AI agent, not a human reader.

## Common Skill Types

| Type | Characteristics | Key Resources |
|------|----------------|---------------|
| **Knowledge/Guidance** | Domain expertise, standards | Lean SKILL.md + detailed references |
| **Automation/Workflow** | Multi-step procedures | SKILL.md workflow + scripts |
| **Template/Generator** | Boilerplate creation | Assets directory + examples |
| **CLI Wrapper** | External tool integration | Scripts + reference docs |
| **User-Only** | Side effects, irreversible actions | `disable-model-invocation: true` |

For detailed examples of each type, see `references/skill-patterns.md`.

## Additional Resources

### Reference Files
- **`references/official-spec.md`** — Canonical skill specification from agentskills.io + Claude Code docs, freshness check queries, and changelog
- **`references/skill-patterns.md`** — Detailed examples of all 5 skill types with full structure
- **`references/output-patterns.md`** — Template and example patterns for consistent output
- **`references/workflows.md`** — Sequential and conditional workflow design patterns

### Scripts
- **`scripts/init_skill.py`** — Scaffold a new skill directory
- **`scripts/quick_validate.py`** — Validate skill structure and quality
- **`scripts/package_skill.py`** — Package skill for distribution

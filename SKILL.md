---
name: create-skill
description: This skill should be used when the user asks to "create a skill", "make a new skill", "build a skill", "add a skill", "write a skill", "generate a skill", "set up a skill", or discusses creating Claude Code skills, skill development, skill templates, or SKILL.md authoring.
version: 0.1.0
tools: Read, Glob, Grep, Bash, Edit, Write
---

# Create Skill for Claude Code

This skill guides the creation of new Claude Code skills based on user requirements. Follow the process below to transform a user's description into a well-structured, effective skill.

## Skill Creation Workflow

### Phase 1: Gather Requirements

Before creating anything, understand the user's intent through targeted questions:

1. **Core purpose**: What should the skill do? What problem does it solve?
2. **Trigger scenarios**: What would users say to invoke this skill? Collect 3-5 concrete phrases.
3. **Invocation style**: Should Claude auto-invoke it (default), or should it be user-only (`disable-model-invocation: true`)?
4. **Resources needed**: Does the skill require scripts, reference docs, or asset files?

Keep questions concise. Ask 2-3 at a time, not all at once.

### Phase 2: Plan the Skill Structure

Based on requirements, determine the appropriate structure:

**Minimal** (simple knowledge/guidance):
```
skill-name/
└── SKILL.md
```

**Standard** (most skills):
```
skill-name/
├── SKILL.md
├── references/
│   └── detailed-guide.md
└── examples/
    └── working-example.sh
```

**Complete** (complex domains):
```
skill-name/
├── SKILL.md
├── references/
│   ├── patterns.md
│   └── advanced.md
├── examples/
│   ├── example1.sh
│   └── example2.json
└── scripts/
    └── validate.sh
```

Determine the skill's placement:
- **User skill**: `~/.claude/skills/skill-name/` — personal, always available
- **Plugin skill**: `plugin-name/skills/skill-name/` — distributed with a plugin

Default to user skill unless the user specifies a plugin context.

### Phase 3: Write SKILL.md

#### Frontmatter (Required)

```yaml
---
name: skill-name
description: This skill should be used when the user asks to "phrase 1", "phrase 2", "phrase 3", mentions "keyword", or discusses topic area.
version: 0.1.0
---
```

**Frontmatter rules:**
- `name`: kebab-case identifier
- `description`: Third person, starts with "This skill should be used when the user asks to". Include 3-5 specific trigger phrases in quotes.
- `version`: Start at `0.1.0`
- Optional: `tools`, `disable-model-invocation`, `user-invocable`, `argument-hint`

#### Body Content

Write in **imperative/infinitive form** (verb-first), never second person:
- Correct: "Parse the config file before processing."
- Incorrect: "You should parse the config file."

**Body structure template:**

```markdown
# Skill Title

Brief description of purpose (1-2 sentences).

## Core Concepts
[Essential knowledge needed to use the skill]

## Workflow / Process
[Step-by-step procedures, the main content]

## Quick Reference
[Tables, cheat sheets, common patterns]

## Additional Resources

### Reference Files
- **`references/file.md`** - Description

### Example Files
- **`examples/file.sh`** - Description
```

**Target length:** 1,500-2,000 words for the body. Move detailed content to `references/`.

### Phase 4: Create Supporting Resources

#### References (`references/`)
- Documentation loaded into context as needed
- Use for: detailed patterns, API docs, schemas, policies
- Keep SKILL.md lean by moving details here

#### Examples (`examples/`)
- Working, runnable code samples
- Users can copy and adapt directly

#### Scripts (`scripts/`)
- Executable utilities for deterministic tasks
- Benefits: token-efficient, deterministic, can run without loading into context

#### Assets (`assets/`)
- Files used in output (templates, images, fonts)
- Not loaded into context, referenced in output

### Phase 5: Validate

Run through this checklist before finalizing:

**Structure:**
- [ ] SKILL.md exists with valid YAML frontmatter
- [ ] `name` and `description` fields present
- [ ] All referenced files exist
- [ ] Only necessary directories created

**Description quality:**
- [ ] Third person ("This skill should be used when...")
- [ ] 3-5 specific trigger phrases in quotes
- [ ] Concrete, not vague

**Content quality:**
- [ ] Imperative/infinitive form throughout
- [ ] Body under 2,000 words (details in references/)
- [ ] No duplicated information across files
- [ ] Resources clearly referenced in SKILL.md

**Progressive disclosure:**
- [ ] Core concepts in SKILL.md
- [ ] Detailed docs in references/
- [ ] Working code in examples/
- [ ] Utilities in scripts/

### Phase 6: Register (if needed)

User skills in `~/.claude/skills/` are auto-discovered — no registration needed.

Plugin skills require the plugin to be enabled in `~/.claude/settings.json`:
```json
{
  "enabledPlugins": {
    "plugin-name@marketplace": true
  }
}
```

## Writing Style Guide

### Description Field
- Always start: "This skill should be used when the user asks to"
- List trigger phrases in quotes: `"create X"`, `"configure Y"`
- Include keywords and topic areas
- Use OR logic to expand triggers

### Body Content
- **DO**: Use imperative form ("Configure the server", "Validate input")
- **DON'T**: Use second person ("You should configure", "You need to")
- **DO**: Be specific and actionable
- **DON'T**: Be vague or generic

### Optional Frontmatter Fields

| Field | Type | Purpose |
|-------|------|---------|
| `version` | string | Semantic version (e.g., `0.1.0`) |
| `tools` | string | Comma-separated tool list |
| `disable-model-invocation` | boolean | `true` = user-only invocation |
| `user-invocable` | boolean | `false` = Claude-only invocation |
| `argument-hint` | string | Hint for slash command arguments |

## Common Patterns

### Knowledge/Guidance Skill
For skills that provide domain knowledge (e.g., coding standards, API docs):
- Lean SKILL.md with core rules
- Detailed references for comprehensive docs
- No scripts needed

### Automation Skill
For skills that execute workflows (e.g., deploy, generate reports):
- SKILL.md describes the workflow steps
- Scripts for deterministic operations
- Examples showing common invocations

### Template Skill
For skills that generate boilerplate (e.g., frontend apps, configs):
- Assets directory with template files
- SKILL.md describes customization options
- Examples of generated output

## Additional Resources

### Reference Files

For detailed guidance on skill content patterns:
- **`references/skill-patterns.md`** - Common skill patterns with full examples

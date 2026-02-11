# Official Skill Specification Reference

Canonical specification details for Claude Code skills, sourced from the
Agent Skills open standard and Claude Code documentation.

**Last verified**: 2026-02-11

## Table of Contents

- [Authoritative Sources](#authoritative-sources)
- [Frontmatter Fields](#frontmatter-fields)
- [File Structure](#file-structure)
- [Content Guidelines](#content-guidelines)
- [String Substitutions](#string-substitutions)
- [Freshness Check Queries](#freshness-check-queries)
- [Changelog](#changelog)

---

## Authoritative Sources

| Source | URL | What to Check |
|--------|-----|---------------|
| **Open Standard Spec** | https://agentskills.io/specification | Field definitions, validation rules |
| **Claude Code Skills Docs** | https://code.claude.com/docs/en/skills | Claude Code-specific extensions |
| **Best Practices Guide** | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | Writing guidelines |
| **Anthropic Skills Repo** | https://github.com/anthropics/skills | Reference implementations |
| **Anthropic Engineering Blog** | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | Design philosophy |

---

## Frontmatter Fields

### Open Standard Fields (agentskills.io)

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | **Yes** | Max 64 chars. Lowercase letters, numbers, hyphens. No start/end hyphen, no `--`. Must match directory name. |
| `description` | **Yes** | Max 1024 chars. Non-empty. No XML tags/angle brackets. |
| `license` | No | License name or reference to bundled file. |
| `compatibility` | No | Max 500 chars. Environment requirements (OS, tools, etc.). |
| `metadata` | No | Arbitrary key-value mapping (string keys → string values). |
| `allowed-tools` | No | Space-delimited list of pre-approved tools. (Experimental) |

### Claude Code Extension Fields

| Field | Description |
|-------|-------------|
| `argument-hint` | Hint shown during autocomplete (e.g., `[issue-number]`). |
| `disable-model-invocation` | `true` prevents Claude from auto-loading. Default: `false`. |
| `user-invocable` | `false` hides from `/` menu. Default: `true`. |
| `model` | Model to use when skill is active. |
| `context` | Set to `fork` for subagent execution. |
| `agent` | Subagent type when `context: fork` (e.g., `Explore`, `Plan`). |
| `hooks` | Hooks scoped to skill lifecycle. |

### Validation Notes

Anthropic's `quick_validate.py` only allows standard fields: `name`, `description`,
`license`, `allowed-tools`, `metadata`, `compatibility`. Extension fields like
`argument-hint`, `disable-model-invocation`, etc. are recognized by Claude Code
runtime but would emit warnings in strict validation.

---

## File Structure

```
skill-name/                    # Must match `name` field
├── SKILL.md                   # Required: frontmatter + instructions
├── scripts/                   # Optional: executable code
├── references/                # Optional: on-demand documentation
└── assets/                    # Optional: files used in output
```

**Excluded files**: README.md, CHANGELOG.md, INSTALLATION_GUIDE.md,
QUICK_REFERENCE.md, or any auxiliary documentation.

---

## Content Guidelines

- Body under **500 lines**; details in `references/`
- **Imperative/infinitive** form ("Parse the config", not "You should parse")
- **Third person** descriptions ("Processes X, generates Y", not "This skill should be used when")
- References one level deep (no nested reference chains)
- Reference files >100 lines: include TOC
- Progressive disclosure: metadata (~100 tokens) → body (<5k tokens) → resources (unlimited)

---

## String Substitutions

Available in Claude Code skill body and scripts:

| Syntax | Description |
|--------|-------------|
| `$ARGUMENTS` | Full argument string |
| `$ARGUMENTS[N]` / `$N` | Positional argument (0-indexed) |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `` !`command` `` | Dynamic context injection (shell command output) |

---

## Freshness Check Queries

### GitHub API (fastest, most reliable)

```bash
# Recent commits to Anthropic skills repo
gh api repos/anthropics/skills/commits --jq '.[0:5] | .[] | {date: .commit.author.date, message: .commit.message}'

# Current skill-creator SKILL.md
gh api repos/anthropics/skills/contents/skills/skill-creator/SKILL.md \
  -H "Accept: application/vnd.github.raw+json"

# Current validation script
gh api repos/anthropics/skills/contents/skills/skill-creator/scripts/quick_validate.py \
  -H "Accept: application/vnd.github.raw+json"
```

### Web Search (broader coverage)

```
"claude code skills" site:code.claude.com 2026
"agent skills specification" site:agentskills.io 2026
anthropic skills changelog 2026
"claude code" skills release notes 2026
"SKILL.md" frontmatter fields anthropic
```

### What to Compare

After fetching latest spec, check for differences in:

1. **Allowed frontmatter fields** — new fields added? old fields deprecated?
2. **Validation rules** — name length, description constraints changed?
3. **File structure** — new standard directories or file types?
4. **Content guidelines** — line limits, writing style updated?
5. **Extension fields** — new Claude Code-specific features?

---

## Changelog

### 2026-02-06
- `compatibility` field added to open standard
- `name` max length increased from 40 → 64 characters
- "hyphen-case" renamed to "kebab-case" in documentation

### 2026-02-04
- Major updates to Anthropic's built-in skills (docx, xlsx, pdf, pptx)

### 2026-01 (approx)
- Agent Skills open standard published at agentskills.io
- `model`, `context`, `agent`, `hooks` extension fields documented

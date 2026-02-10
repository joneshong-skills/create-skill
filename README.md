# create-skill

A Claude Code skill that guides the creation of new Claude Code skills from user requirements.

## Description

This skill transforms a user's description into a well-structured Claude Code skill. It walks through the full skill creation workflow: gathering requirements, planning the file structure, writing the SKILL.md with proper frontmatter, creating supporting resources (references, examples, scripts), and validating the result.

## What It Does

- Asks targeted questions to understand the skill's purpose and trigger scenarios
- Determines the appropriate structure (minimal, standard, or complete)
- Generates a SKILL.md with valid YAML frontmatter and imperative-form body content
- Creates supporting files: reference docs, runnable examples, utility scripts, and asset templates
- Validates the final skill against a comprehensive checklist
- Covers common patterns: knowledge/guidance, automation, template generation, CLI wrappers, and user-only skills

## Install

Copy the skill directory into your Claude Code skills folder:

```
cp -r create-skill ~/.claude/skills/
```

Skills placed in `~/.claude/skills/` are auto-discovered by Claude Code. No additional registration is needed.

## Usage

Invoke the skill by asking Claude Code to create a skill. Example prompts:

- "Create a skill for deploying with Docker"
- "Make a new skill that helps write unit tests"
- "Build a skill for code review standards"
- "Generate a skill template for API endpoint scaffolding"

Claude will walk through the requirement gathering, planning, writing, and validation phases automatically.

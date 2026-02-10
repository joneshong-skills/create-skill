# Skill Patterns Reference

Detailed patterns and examples for common skill types.

## Pattern 1: Knowledge/Guidance Skill

A skill that provides specialized domain knowledge to Claude.

### Example: Code Review Standards

```yaml
---
name: code-review
description: This skill should be used when the user asks to "review code", "check code quality", "audit code", or mentions code review standards, best practices, or coding guidelines.
version: 0.1.0
---
```

```markdown
# Code Review Standards

This skill provides coding standards and review checklists for the team's codebase.

## Review Checklist

### Security
- Validate all user input at system boundaries
- Sanitize output to prevent XSS
- Use parameterized queries for database access
...

## Additional Resources
- **`references/security-checklist.md`** - Detailed security review guide
- **`references/performance-checklist.md`** - Performance review guide
```

**Structure:**
```
code-review/
├── SKILL.md
└── references/
    ├── security-checklist.md
    └── performance-checklist.md
```

---

## Pattern 2: Automation/Workflow Skill

A skill that guides Claude through a multi-step workflow.

### Example: Database Migration

```yaml
---
name: db-migration
description: This skill should be used when the user asks to "create a migration", "migrate database", "add a database column", "modify schema", or discusses database schema changes, migration scripts, or schema versioning.
version: 0.1.0
tools: Read, Bash, Edit, Write
disable-model-invocation: true
---
```

```markdown
# Database Migration Workflow

This skill guides the creation and execution of database migration scripts.

## Migration Process

### Step 1: Generate Migration File
Create a timestamped migration file:
\`\`\`bash
bash scripts/create-migration.sh "description_of_change"
\`\`\`

### Step 2: Write Migration SQL
Edit the generated file with up/down migrations...

### Step 3: Test Migration
Run against test database before applying to production...

## Additional Resources
- **`references/schema.md`** - Current database schema
- **`scripts/create-migration.sh`** - Migration file generator
- **`scripts/test-migration.sh`** - Migration tester
```

**Structure:**
```
db-migration/
├── SKILL.md
├── references/
│   └── schema.md
└── scripts/
    ├── create-migration.sh
    └── test-migration.sh
```

---

## Pattern 3: Template/Generator Skill

A skill that creates boilerplate from templates.

### Example: API Endpoint Generator

```yaml
---
name: api-endpoint
description: This skill should be used when the user asks to "create an endpoint", "add an API route", "generate API", "scaffold endpoint", or discusses REST API development, endpoint creation, or route handlers.
version: 0.1.0
tools: Read, Write, Bash
---
```

```markdown
# API Endpoint Generator

Generate consistent API endpoints following the project's conventions.

## Endpoint Creation Process

### Step 1: Determine Endpoint Details
Gather: resource name, HTTP methods, auth requirements, validation rules.

### Step 2: Generate Files
For each endpoint, create:
1. Route handler from template
2. Validation schema
3. Test file

Use the template in `assets/endpoint-template/` as the starting point.

### Step 3: Register Route
Add the route to the router configuration...

## Additional Resources
- **`assets/endpoint-template/`** - Endpoint boilerplate files
- **`references/api-conventions.md`** - API style guide
- **`examples/user-endpoint.ts`** - Complete working example
```

**Structure:**
```
api-endpoint/
├── SKILL.md
├── assets/
│   └── endpoint-template/
│       ├── handler.ts
│       ├── schema.ts
│       └── test.ts
├── references/
│   └── api-conventions.md
└── examples/
    └── user-endpoint.ts
```

---

## Pattern 4: CLI Wrapper Skill

A skill that wraps an external CLI tool for headless/scripted use.

### Example: Docker Deployment

```yaml
---
name: docker-deploy
description: This skill should be used when the user asks to "deploy with docker", "build docker image", "run docker compose", "containerize", or discusses Docker deployment, container orchestration, or Dockerfile creation.
version: 0.1.0
tools: Bash, Read, Write
argument-hint: "[service or flags]"
disable-model-invocation: true
---
```

```markdown
# Docker Deployment

Deploy services using Docker and Docker Compose.

## Environment Checks
\`\`\`bash
docker --version
docker compose version
\`\`\`

## Deployment Workflow
...

## Common Recipes
### Build and deploy a service
### Scale services
### View logs
```

---

## Pattern 5: Headless/User-Only Skill

For skills with side effects that should only run when explicitly invoked.

### Key characteristics:
- Set `disable-model-invocation: true` in frontmatter
- User invokes via `/skill-name` slash command
- Appropriate for: deploy, send, publish, commit actions

### When to use `disable-model-invocation`:
- The skill performs irreversible actions
- The skill sends data externally (email, Slack, API calls)
- The skill modifies production systems
- The skill should only run with explicit user intent

---

## Anti-Patterns to Avoid

### 1. Overly Broad Description
```yaml
# BAD
description: Helps with coding tasks.
# GOOD
description: This skill should be used when the user asks to "format Python code", "apply black formatting", "fix PEP8 issues", or mentions Python code style, linting, or auto-formatting.
```

### 2. Monolithic SKILL.md
Keep SKILL.md under 2,000 words. If it exceeds 3,000 words, split into references.

### 3. Unreferenced Resources
Always mention bundled resources in the SKILL.md body so Claude knows they exist.

### 4. Duplicate Information
Information should live in either SKILL.md or references, not both.

### 5. Second Person Writing
Never use "you should", "you need to", "you can". Always use imperative form.

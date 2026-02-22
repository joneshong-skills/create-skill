# Output Patterns

Patterns for skills that need to produce consistent, high-quality output.

## Template Pattern

Provide templates for output format. Match strictness to requirements.

**Strict (API responses, data formats):**

```markdown
## Report structure

ALWAYS use this exact template:

# [Analysis Title]

## Executive summary
[One-paragraph overview]

## Key findings
- Finding 1 with data
- Finding 2 with data

## Recommendations
1. Actionable recommendation
2. Actionable recommendation
```

**Flexible (when adaptation is useful):**

```markdown
## Report structure

Sensible default — adapt as needed:

# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on discoveries]

## Recommendations
[Tailor to context]
```

## Examples Pattern

For skills where output quality depends on seeing examples, provide input/output pairs:

```markdown
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication

**Example 2:**
Input: Fixed bug where dates displayed incorrectly
Output: fix(reports): correct date formatting in timezone conversion

Follow this style: type(scope): brief description.
```

Examples help Claude understand desired style more clearly than descriptions alone.

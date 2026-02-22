# Workflow Patterns

Design patterns for skills with multi-step or branching workflows.

## Sequential Workflows

Break complex tasks into clear, numbered steps. Give an overview first:

```markdown
Processing a form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

Each step should be independently understandable.
Link to scripts or references for complex steps.

## Conditional Workflows

For tasks with branching logic, guide through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow:
   a. Generate template from assets/
   b. Fill in required fields
   c. Validate output

3. Editing workflow:
   a. Read existing file
   b. Apply modifications
   c. Validate changes preserved original structure
```

## Decision Tree Pattern

For skills with multiple paths based on input characteristics:

```markdown
## Route Selection

| Input type | Size | Route |
|-----------|------|-------|
| PDF | <10 pages | Direct extraction |
| PDF | >10 pages | Chunked processing |
| DOCX | Any | XML-based extraction |
| Image | Any | OCR pipeline |

Follow the matching route below.
```

## Error Recovery Pattern

For fragile operations, define fallback paths:

```markdown
## Processing Pipeline

1. Try primary approach (fast, may fail)
2. If step 1 fails → try fallback approach
3. If step 2 fails → report error with diagnostics

Always capture error output for debugging.
```

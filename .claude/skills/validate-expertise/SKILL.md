---
name: validate-expertise
description: Validates expertise YAML files for structure and required fields. Use after creating/editing expertise files, before commits, in expertise-curator agent, or when auditing quality.
---

# Validate Expertise Skill

This skill validates expertise YAML files used by the expert agent system. It ensures that expertise files follow the required structure and contain all mandatory fields.

## Usage

When you need to validate an expertise YAML file, use this skill by running the validation script:

```bash
python .claude/skills/validate-expertise/scripts/validate_expertise.py <path-to-expertise-yaml>
```

### Examples

Validate a single expertise file:
```bash
python .claude/skills/validate-expertise/scripts/validate_expertise.py expertise/authentication.yaml
```

Validate all expertise files in a directory:
```bash
for file in expertise/*.yaml; do
  python .claude/skills/validate-expertise/scripts/validate_expertise.py "$file"
done
```

## What This Skill Validates

### Mandatory Requirements (Errors)
- **YAML syntax**: File must be valid YAML
- **description field**: Must exist, must be non-empty, must be a string

### Recommended Best Practices (Warnings)
- **Description length**: Should be 20-500 characters for optimal readability
- **Recommended fields**: Suggests including `category`, `concepts`, and `details` fields
- **Field types**: Validates that fields use the correct data types (list, string, etc.)

## Expertise YAML Structure

The minimal valid expertise file requires only a description:

```yaml
description: "Brief overview of what this expertise covers"
```

A well-structured expertise file follows this recommended format:

```yaml
description: |
  Brief, clear description of what this expertise covers.
  This helps the expert agent decide if this file is relevant to their research.

category: "technical"  # or domain, architecture, business-logic, etc.

concepts:
  - "Key concept 1"
  - "Key concept 2"
  - "Key concept 3"

details: |
  Detailed explanation of concepts, patterns, and knowledge.
  Keep this at a conceptual level - avoid specific implementation details.

related_files:
  - "src/module/**/*.ts"
  - "config/*.yaml"

# Additional custom fields as needed
```

## When to Use This Skill

Use this skill:
1. **After creating** a new expertise file
2. **After editing** an existing expertise file
3. **Before committing** expertise files to version control
4. **In the expertise-curator agent** - automatically validate after curation
5. **Periodically** - to audit all expertise files for quality

## Exit Codes

- **0**: Validation passed (file is valid, may have warnings)
- **1**: Validation failed (file has errors and must be fixed)

## Integration with Agents

### Expertise-Curator Agent
The expertise-curator agent should use this skill after creating or editing expertise files:

```yaml
# In .claude/agents/expertise-curator.md
skills: [validate-expertise]
```

### Expert Agent
The expert agent may use this skill to verify expertise files are valid before using them:

```yaml
# In .claude/agents/expert.md
skills: [validate-expertise]
```

## Tips for Writing Good Expertise Files

1. **Clear descriptions**: Write descriptions that help agents quickly decide relevance
2. **Conceptual focus**: Focus on "what" and "why", not implementation details
3. **Avoid specifics**: Don't include line numbers, variable names, or code snippets
4. **Patterns over examples**: Describe patterns and relationships, not specific instances
5. **Maintain consistency**: Use consistent terminology across expertise files
6. **Right-size content**: Aim for 50-300 lines per file (focused but not sparse)

## Troubleshooting

### Common Errors

**"Missing required field: 'description'"**
- Add a description field to your YAML file

**"YAML parsing error"**
- Check for syntax errors like incorrect indentation, missing colons, or unquoted special characters
- Use a YAML validator or linter to identify the exact issue

**"File 'description' cannot be empty"**
- Provide a meaningful description (at least 20 characters recommended)

### Common Warnings

**"Description is quite short"**
- Expand your description to provide more context (1-3 sentences recommended)

**"Missing recommended fields"**
- Consider adding `category`, `concepts`, and `details` fields for better structure

**"Field should be a list/string"**
- Ensure you're using the correct YAML data type for each field

---
name: expertise-curator
description: Curate and maintain expertise YAML files in the expertise/ directory. Use when discovering new architectural patterns, domain concepts, or design decisions that should be documented. Decides whether to create new expertise files or update existing ones. Validates YAML structure and maintains quality standards.
---

# Expertise Curator

## Overview

This skill helps maintain high-quality expertise YAML files that document architectural patterns, domain concepts, and design decisions discovered in the codebase. Use this skill when research uncovers knowledge worth preserving for future reference.

## Workflow

### Phase 1: Decision - New File or Update Existing?

When new findings need to be documented:

1. **Understand the Findings** - What topic/area does this knowledge cover? What concepts or patterns are being described?

2. **Discover Existing Expertise** - Use Glob to find all `expertise/*.yaml` files, then read the `description` field of each file to understand what they cover.

3. **Decide: New File or Update Existing**

   **Create a NEW file if:**
   - No existing file covers this topic
   - The topic is distinct enough to warrant its own file
   - Adding to existing files would make them unfocused or too large
   - This represents a new domain area or architectural component

   **Update EXISTING file if:**
   - An existing file already covers this topic
   - The new knowledge complements or expands existing expertise
   - The file won't become too large or unfocused

4. **Choose the File**
   - If creating new: Choose a descriptive kebab-case name (e.g., `user-authentication.yaml`)
   - If updating existing: Select the most relevant existing file and read its full content

### Phase 2: Curation - Add Knowledge with Quality

Add the knowledge while maintaining high quality:

1. **Focus on Concepts, Not Implementation** - Describe patterns, relationships, and design decisions. Avoid specific file paths, line numbers, variable names.
   - Good: "Uses JWT tokens for stateless authentication"
   - Bad: "JWT token is validated in src/auth/middleware.ts:42"

2. **Remove Duplicates** - Check if the knowledge is already captured. If it exists, don't repeat it. If the new information refines existing knowledge, update the existing text.

3. **Keep It Concise and Clear** - Use clear, scannable language. Break complex topics into bullet points. Use consistent terminology.

4. **Maintain Structure**:
   - Keep the `description` field brief (1-3 sentences)
   - Add details to the `details` field
   - Update `concepts` list with key concepts
   - Add file patterns to `related_files` if helpful (use globs, not specific paths)
   - Use consistent `category` values: `technical`, `domain`, `business-logic`, `architecture`, `integration`

5. **Right-Size Content** - Single file should be 50-300 lines. If growing too large (>300 lines), consider splitting. If too sparse (<50 lines), consider merging with related expertise.

### Phase 3: Validation - Ensure Quality

After creating or editing the expertise file:

1. **Validate the YAML** - Use the `validate-expertise` skill to check structure and required fields

2. **Fix Any Errors** - If validation fails, read the error messages and fix the issues (usually YAML syntax or missing description). Validate again until it passes.

3. **Address Warnings (Optional)** - Warnings are not blockers, but consider improving description length or adding recommended fields.

## Curation Principles

### What to Include
- Architectural patterns and design decisions
- Domain concepts and their relationships
- Business rules and workflows
- Key constraints and requirements
- Integration patterns
- Error handling strategies
- Authentication/authorization approaches
- Data flow and state management patterns

### What to Avoid
- Specific line numbers or code locations
- Variable or function names
- Implementation details that change frequently
- Code snippets (unless showing a pattern)
- Overly technical details that aren't conceptual
- Personal opinions without rationale
- Outdated information

## File Naming

Use descriptive kebab-case names:
- Good: `user-authentication-flow.yaml`, `api-error-handling.yaml`, `database-schema-design.yaml`
- Bad: `auth.yaml` (too vague), `stuff.yaml` (not descriptive), `user_auth.yaml` (use kebab-case)

## Output Format

After completing the curation, provide a summary:

```
## Expertise Curation Summary

**Action**: [Created new file / Updated existing file]
**File**: expertise/<filename>.yaml
**Topic**: [Brief topic description]

### Changes Made
- [List key changes or additions]
- [What concepts were added]
- [What duplicates were removed, if any]

### Validation
[PASS/FAIL] YAML validation result

### Recommendations
- [Any recommendations for follow-up research]
- [Suggestions for related areas to explore]
```

## Quality Standards

Every expertise file should:
- Have a clear, scannable description
- Contain conceptual knowledge, not implementation details
- Be well-organized and free of duplicates
- Follow consistent structure and terminology
- Pass YAML validation

These files help researchers (both AI and human) understand the codebase more effectively.

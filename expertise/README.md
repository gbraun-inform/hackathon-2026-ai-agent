# Expertise System

This directory contains **expertise YAML files** that serve as a mental model for the expert agent system. These files store curated knowledge about the codebase, domain concepts, architectural patterns, and business logic.

## What Are Expertise Files?

Expertise files are YAML documents that capture conceptual knowledge about different aspects of the codebase. They help AI agents:
- Quickly understand unfamiliar areas of the codebase
- Research and explore with guided context
- Learn from accumulated knowledge over time
- Make informed decisions based on domain expertise

Think of them as **living documentation** that evolves as the codebase is explored and understood.

## Directory Structure

```
expertise/
├── README.md              # This file
├── _template.yaml         # Template for new expertise files
├── authentication.yaml    # Example: Authentication system expertise
├── api-design.yaml        # Example: API design patterns
└── ...                    # More expertise files as needed
```

## Expertise File Format

### Minimal Valid File

Only the `description` field is mandatory:

```yaml
description: "Brief overview of what this expertise covers"
```

### Recommended Structure

For maximum usefulness, include these recommended fields:

```yaml
description: |
  Brief, clear description of what this expertise covers.
  This helps the expert agent decide if this file is relevant to their research.
  Keep it concise (1-3 sentences).

category: "technical"  # or domain, architecture, business-logic, etc.

concepts:
  - "Key concept 1"
  - "Key concept 2"
  - "Key concept 3"

details: |
  Detailed explanation of the concepts, patterns, and knowledge.

  This is where the mental model lives:
  - Architectural patterns used
  - Business logic explanations
  - Domain concepts and relationships
  - Design decisions and rationale

  Keep this at a conceptual level - avoid specific file paths,
  line numbers, or implementation details that change frequently.

related_files:
  - "src/module-name/**/*.ts"
  - "config/*.yaml"

# Additional custom fields as needed
```

## The Expert Agent System

### How It Works

1. **Expert Agent** - Researches the codebase using expertise files as a guide
   - Discovers relevant expertise by reading descriptions
   - Uses expertise as a mental model during research
   - Calls the curator when new knowledge is discovered

2. **Expertise-Curator Agent** - Maintains and updates expertise files
   - Decides whether to create new files or update existing ones
   - Curates content to avoid duplicates
   - Validates YAML structure
   - Keeps knowledge conceptual and well-organized

3. **Validate-Expertise Skill** - Ensures YAML files are valid
   - Checks required fields
   - Validates structure
   - Provides helpful error messages

### Agent Workflow

```
User Request → Expert Agent
                  ↓
            1. Discovers expertise files (reads descriptions)
            2. Selects relevant expertise
            3. Researches codebase using expertise as guide
            4. Makes new findings
                  ↓
            Calls Curator Agent
                  ↓
            1. Decides: new file or existing
            2. Adds knowledge, curates content
            3. Validates YAML
                  ↓
            Returns to Expert with updated knowledge
```

## Creating Expertise Files

### Using the Expert Agent

The easiest way to create expertise is to use the expert agent. It will automatically:
1. Research the codebase
2. Discover new knowledge
3. Call the curator to create or update expertise files

### Manual Creation

1. Copy `_template.yaml` to a new file
2. Name it descriptively using kebab-case (e.g., `authentication-flow.yaml`)
3. Fill in the fields
4. Validate using the validate-expertise skill:
   ```bash
   python .claude/skills/validate-expertise/scripts/validate_expertise.py expertise/your-file.yaml
   ```

## Best Practices

### Content Guidelines

1. **Focus on Concepts, Not Implementation**
   - ✓ "Uses JWT tokens for stateless authentication"
   - ✗ "JWT token is validated in auth.ts line 42"

2. **Describe Patterns and Relationships**
   - ✓ "User service depends on authentication middleware"
   - ✗ "userService.ts imports from auth/middleware.ts"

3. **Keep Descriptions Clear and Scannable**
   - First sentence should immediately convey relevance
   - Use 1-3 sentences for the description field
   - Make it easy for agents to quickly decide if this expertise is relevant

4. **Avoid Duplicates**
   - Check existing expertise before creating new files
   - Update existing files rather than creating overlapping content
   - Use the curator agent to help maintain consistency

5. **Right-Size Your Files**
   - One focused topic per file
   - Aim for 50-300 lines
   - Split large topics into multiple focused files
   - Merge very sparse files with related topics

### Naming Conventions

- Use kebab-case: `api-design-patterns.yaml`
- Be descriptive: `user-authentication-flow.yaml` not `auth.yaml`
- Use noun phrases: `error-handling.yaml` not `how-errors-work.yaml`
- Group related files with prefixes if needed: `api-endpoints.yaml`, `api-middleware.yaml`

### Categories

Use consistent category names across files:
- `technical` - Technical implementation patterns, architecture
- `domain` - Business domain knowledge, domain concepts
- `business-logic` - Business rules, workflows, processes
- `architecture` - High-level system architecture, design decisions
- `integration` - External integrations, APIs, third-party services

## Validating Expertise Files

Use the validate-expertise skill to ensure files are valid:

```bash
# Validate a single file
python .claude/skills/validate-expertise/scripts/validate_expertise.py expertise/your-file.yaml

# Validate all files
for file in expertise/*.yaml; do
  python .claude/skills/validate-expertise/scripts/validate_expertise.py "$file"
done
```

## Version Control

Expertise files should be version controlled with git:
- Track how knowledge evolves over time
- Review changes to expertise in pull requests
- Collaborate on domain knowledge with your team
- Maintain consistency across team members

## Maintenance

### Regular Audits

Periodically review expertise files to:
- Remove outdated information
- Merge duplicate content
- Validate all files still parse correctly
- Ensure descriptions are clear and helpful

### When to Update

Update expertise files when:
- Architectural patterns change
- New domain concepts are introduced
- Business logic evolves
- The codebase is refactored
- New discoveries are made during research

### When to Create New Files

Create new expertise files when:
- Researching a topic not covered by existing files
- A file becomes too large (>300 lines)
- A new major feature or domain area is introduced
- You need to document a new architectural pattern

## Examples

See the expertise files in this directory for examples:
- `_template.yaml` - Template for creating new files
- Other `.yaml` files - Real expertise about this codebase

## Questions?

For more information about the expert agent system:
- Read `.claude/agents/expert.md`
- Read `.claude/agents/expertise-curator.md`
- Read `.claude/skills/validate-expertise/SKILL.md`

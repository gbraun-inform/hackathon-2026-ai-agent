---
name: agent-creator
description: Guide for creating custom Claude Code agents (subagents). Use when users want to create specialized AI agents with custom system prompts, tool restrictions, permission modes, or specific workflows. Use immediately when the user says they want to build/create an agent, or when designing a specialized agent to delegate isolated tasks to.
---

# Agent Creator

This skill provides guidance for creating effective Claude Code agents—specialized autonomous subagents that handle isolated, focused tasks.

## About Agents

Agents are custom AI subprocesses that Claude delegates to using the `Task` tool. Unlike skills (which share the main conversation context), agents have isolated context windows and can be configured with custom system prompts, restricted tool access, and specific permission modes.

### When to Use Agents vs. Skills

| Aspect | Agents | Skills |
|--------|--------|--------|
| **Structure** | Single .md file | Directory with SKILL.md + resources |
| **Context** | Isolated context window | Shares main context |
| **Triggering** | Claude delegates via Task tool | User/Claude invokes via Skill tool |
| **Configuration** | Custom tools, models, permissions | No tool/permission config |
| **Nesting** | CANNOT spawn other agents | Can invoke other skills |
| **Best For** | Isolated operations, parallel work, constraints | Reusable workflows in main context |

**Use agents when you need:**
- Isolated execution context (no context bleed)
- Parallel independent tasks
- Restricted tool access (security/compliance)
- Custom system prompts for specialized behavior
- Background task processing
- Focused single-purpose operations

**Use skills when you need:**
- Interactive guidance in main context
- Multi-step workflows with branching
- Bundled resources (scripts, templates, references)
- Deep integration with main conversation

## Core Principles for Agents

### Single-Purpose Focus

Each agent should have one clear responsibility. An agent that does "code review, testing, and deployment" tries to do too much. Break this into: code-reviewer, test-runner, and deployment-orchestrator agents.

**Good agent scope:**
- "Review TypeScript for type safety"
- "Run test suite and report failures"
- "Build project and report errors"

**Bad agent scope:**
- "Review, test, and deploy everything"
- "Do whatever the user asks"

### Clear Delegation Triggers

The agent's description field is how Claude decides when to delegate. Write it to be specific about when this agent should be invoked:

**Good descriptions:**
- "Code review specialist. Use immediately after writing or modifying code to review for quality, security, and type safety."
- "Background research agent for exploring codebases, searching for patterns, and answering questions about code structure."
- "Test executor that runs test suites and reports failures with actionable error messages."

**Bad descriptions:**
- "A code reviewer"
- "Does code stuff"
- "General purpose agent"

### Context Isolation

Agents don't have access to the main conversation history. This is both a constraint and a feature:

**Constraint:** You must pass all needed context explicitly in the system prompt or Task description.

**Feature:** No context bleed from main conversation. An agent's behavior is predictable and isolated.

## Anatomy of an Agent

Every agent is a single `.md` file with YAML frontmatter and a markdown system prompt.

### Frontmatter (Required)

```yaml
---
name: agent-name              # hyphen-case, 1-64 chars
description: [Complete text...] # When should Claude delegate to this agent?
tools: [Read, Grep, Bash]    # Optional: specify allowed tools
model: inherit               # Optional: sonnet, opus, haiku, inherit
permissionMode: default      # Optional: default, acceptEdits, dontAsk, bypassPermissions, plan
skills: [skill-name]         # Optional: skills available to agent
hooks:                        # Optional: advanced validation/processing
  PreToolUse: ...
---
```

**Required fields:**
- `name`: Hyphenated lowercase name (e.g., `code-reviewer`, `db-researcher`)
- `description`: Clear statement of what agent does and when to delegate to it

**Optional fields:**
- `tools`: Array of tool names (Read, Write, Edit, Grep, Bash, Glob, WebFetch, WebSearch, etc.). If omitted, agent inherits default tools.
- `disallowedTools`: Array of tools to block (useful for security restrictions)
- `model`: Which Claude model to use (default: inherit from parent)
- `permissionMode`: Controls how agent handles user interactions (see references/permission-modes.md)
- `skills`: Array of skill names available to agent
- `hooks`: Advanced configuration for pre/post-tool processing

### System Prompt (Markdown Body)

The markdown body is your agent's system prompt. It should be:

- **Concise**: 200-2000 words typically
- **Specific**: About the agent's exact role and constraints
- **Instructive**: Clear steps or decision trees
- **Bounded**: Define what's in/out of scope

**Example structure:**
```markdown
You are a [specific role].

Your task: [what you do]

When invoked:
1. [First step]
2. [Second step]
3. [Report results as...]

Constraints:
- Only [specific tools/actions]
- Do NOT [specific anti-patterns]
- [Specific format/quality requirements]
```

## Agent Creation Workflow (6 Steps)

Follow these steps in order to create an effective agent.

### Step 1: Understand the Agent's Purpose

Start with concrete examples of how the agent will be used:

- "When should Claude delegate to this agent?"
- "What specific problem does it solve?"
- "What tools does it need?"
- "What constraints matter? (scope, tool access, output format, etc.)"

For example: "I want an agent that reviews code for type safety after I write TypeScript." This clarifies the agent should focus on types, trigger after code changes, and use tools like Read/Grep/Bash.

### Step 2: Plan the Agent

Decide:

1. **Single purpose**: One clear responsibility
2. **Delegation trigger**: When Claude should invoke it (from description field)
3. **Tool access**: What tools the agent needs
4. **Model**: Standard (inherit) or specialized (opus for complex analysis, haiku for fast operations)
5. **Permission mode**: How agent handles user interactions
6. **System prompt approach**: Workflow-based, checklist-based, or decision-tree-based

For the code reviewer example:
- Purpose: Find type errors and quality issues
- Trigger: Immediately after code changes
- Tools: Read, Grep, Bash (to check types)
- Model: inherit (use default)
- Mode: default (standard permission checking)
- Approach: Workflow-based with checklist

### Step 3: Initialize the Agent

Create the agent .md file using `init_agent.py`:

```bash
scripts/init_agent.py <agent-name> --path <output-directory> --type <type>
```

Templates available:
- `basic`: Minimal agent with required fields only
- `read-only`: For explorers/analyzers (Read, Grep, Glob, Bash)
- `editor`: For editors/fixers (Read, Write, Edit, Bash)
- `restricted`: With hooks for validation
- `custom`: Interactive prompts for all fields

**Example:**
```bash
scripts/init_agent.py code-reviewer --path .claude/agents --type read-only
```

This creates `.claude/agents/code-reviewer.md` with a template.

### Step 4: Edit the Agent

Write the system prompt in the markdown body:

1. **Be specific about role**: "You are a type safety checker" not "You are helpful"
2. **Define scope**: "Focus on TypeScript type errors, ignore linting"
3. **Specify behavior**: "Run these checks: 1) Types, 2) Null safety, 3) Generics"
4. **Set output format**: "Report each error as: [FILE:LINE] [ERROR TYPE] [message]"
5. **Add constraints**: "Do NOT: fix code, run tests, or modify package.json"

### Step 5: Validate the Agent

Check agent configuration with `validate_agent.py`:

```bash
scripts/validate_agent.py <path-to-agent.md>
```

Validates:
- Required frontmatter fields
- Naming conventions
- Tool configuration
- Permission modes
- Quality warnings

Fix any validation errors and run again until valid.

### Step 6: Test the Agent

Place the agent in `.claude/agents/` directory and invoke it:

```python
from anthropic import Anthropic

client = Anthropic()
response = client.beta.messages.create(
    model="claude-opus-4-5-20251101",
    max_tokens=2048,
    system="Your system prompt here...",
    messages=[
        {
            "role": "user",
            "content": "Your task description here..."
        }
    ],
    betas=["agents-2025-12-04"]
)
```

Or use Claude Code's Task tool to invoke it during a session.

## Quick Start Example: Code Reviewer Agent

Here's a complete, working code-reviewer agent you can adapt:

```markdown
---
name: code-reviewer
description: Expert code review specialist. Use immediately after writing or modifying code to check for type safety, security issues, and code quality problems. Reviews TypeScript/JavaScript, Python, and other languages.
tools: Read, Grep, Bash, Glob
model: inherit
permissionMode: default
---

You are a senior code review specialist focused on finding quality and security issues.

Your task: Review code changes for:
1. Type safety (TypeScript, type hints)
2. Security vulnerabilities (injection, XSS, exposed secrets)
3. Code clarity and maintainability
4. Proper error handling
5. Test coverage gaps

When invoked:

1. Run git diff to identify changed files
2. Read each modified file to understand context
3. Perform targeted checks:
   - Use grep for common security patterns
   - Check for proper null/undefined handling
   - Verify error boundaries exist
   - Look for console statements (debug code)
4. Report findings by priority:
   - CRITICAL: Security issues, type errors (must fix)
   - WARNING: Logic errors, missing error handling (should fix)
   - INFO: Style suggestions, potential improvements (consider)

Output format:
```
[CRITICAL] src/auth.ts:42 - Exposed API key in code
[WARNING] src/db.ts:15 - Unhandled promise rejection
[INFO] src/utils.ts:5 - Consider extracting repeated logic
```

Constraints:
- Do NOT fix code (only report findings)
- Do NOT run tests (focus on code inspection)
- Focus on modified lines, mention context as needed
- Stop after first 10 issues to keep output focused
```

## Key Configuration Fields

### description

**Purpose**: Controls when Claude delegates to your agent. This is THE most important field.

Include:
- What the agent does (specific action, not vague)
- When to invoke it (after writing code? before deployment? for analysis?)
- What problems it solves
- Any specific contexts or file types

**Examples:**
- ✅ "Use after writing code to review for type safety and security issues"
- ❌ "A code reviewer"

### tools

**Purpose**: Restrict which tools agent can access (security & focus).

```yaml
tools: [Read, Grep, Bash]        # agent can only use these
disallowedTools: [Write, Edit]   # agent cannot use these (alternative syntax)
```

**Common combinations:**
- Read-only agents: `[Read, Grep, Glob, Bash]`
- Editor agents: `[Read, Write, Edit, Bash]`
- Research agents: `[Read, Grep, Glob, WebFetch, WebSearch]`

See `references/tool-integration.md` for detailed guidance.

### model

**Purpose**: Choose which Claude model to use.

```yaml
model: sonnet    # Fast, general purpose (default)
model: opus      # Most capable, for complex analysis
model: haiku     # Fastest, cheapest for simple tasks
model: inherit   # Use parent context's model (recommended)
```

### permissionMode

**Purpose**: Controls permission/confirmation behavior.

```yaml
permissionMode: default          # Standard permission checks
permissionMode: acceptEdits      # Auto-approve edits
permissionMode: dontAsk          # Skip prompts
permissionMode: bypassPermissions # Dangerous: skip all checks
permissionMode: plan             # Read-only mode
```

See `references/permission-modes.md` for when to use each mode.

## Resources

This skill includes reference documentation and scripts to support agent creation:

### scripts/

- **init_agent.py**: Generate agent .md files from templates
- **validate_agent.py**: Validate agent configuration

Usage:
```bash
scripts/init_agent.py my-agent --path .claude/agents --type read-only
scripts/validate_agent.py .claude/agents/my-agent.md
```

### references/

- **agent-patterns.md** (~1500 lines): 10+ complete agent examples with patterns
- **tool-integration.md** (~800 lines): Guide to tool selection and restrictions
- **permission-modes.md** (~600 lines): Reference for permission modes
- **hooks-guide.md** (~1200 lines): Advanced hooks configuration

When to use each reference:
- Creating an agent? Read agent-patterns.md for similar examples
- Choosing tools? Read tool-integration.md for decision tree
- Configuring permissions? Read permission-modes.md for guidance
- Advanced validation? Read hooks-guide.md

### assets/templates/

Template agents ready to adapt:
- code-reviewer-template.md
- debugger-template.md
- research-agent-template.md
- restricted-agent-template.md

## Common Patterns

### Read-Only Analysis Agents

For code review, exploration, research:

```yaml
tools: [Read, Grep, Glob, Bash]
permissionMode: plan
```

Agent can explore but cannot modify anything.

### Focused Editor Agents

For fixing, refactoring, or generating code:

```yaml
tools: [Read, Write, Edit, Bash, Grep, Glob]
permissionMode: acceptEdits
```

Agent can make changes automatically.

### Restricted Research Agents

For data analysis with safety limits:

```yaml
tools: [Read, Grep, WebFetch]
disallowedTools: [Bash, Write]
permissionMode: dontAsk
```

Agent can research but not execute arbitrary code or modify files.

## Troubleshooting

**Agent not being invoked?**
- Check description field—is the trigger condition clear?
- Make sure description explains when agent should be used
- Is the agent in `.claude/agents/` directory?

**Agent has wrong tool access?**
- Check `tools` field in frontmatter
- Verify tool names match exactly (case-sensitive)
- Run validate_agent.py to check configuration

**Agent needs more context?**
- Add context to system prompt explicitly
- Mention specific files/patterns to focus on
- Include code snippets in Task description

**Validation fails?**
- Check name: must be hyphen-case, lowercase, 1-64 chars
- Check description: must be 10-1024 characters
- Verify frontmatter YAML syntax
- Run validate_agent.py for detailed error messages

## Next Steps

1. Choose an agent to create (from references/agent-patterns.md or plan a new one)
2. Run `scripts/init_agent.py` with appropriate template
3. Edit the system prompt to match your needs
4. Run `scripts/validate_agent.py` to check configuration
5. Place in `.claude/agents/` and test
6. Iterate based on results

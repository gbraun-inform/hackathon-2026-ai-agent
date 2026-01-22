# Hooks in Agents: Advanced Configuration Guide

This guide covers implementing lifecycle hooks within agent definitions. Hooks are deterministic scripts that run during an agent's execution to validate inputs, filter outputs, and perform cleanup—all without LLM involvement.

**When to use hooks in agents:**
- Validate tool inputs before execution
- Filter or transform tool outputs
- Enforce safety constraints
- Run cleanup when agent finishes
- Make agents safer and more predictable

## Why Hooks in Agents?

Agent-scoped hooks are different from global hooks:

| Feature | Agent Hooks | Global Hooks |
|---------|------------|--------------|
| **Scope** | Only run while agent is active | Run in all sessions |
| **Lifecycle** | Auto-cleaned when agent finishes | Persist in settings |
| **Purpose** | Agent-specific validation | Project-wide automation |
| **Complexity** | Simple, focused scripts | Can be complex workflows |

**Use agent hooks for:**
- Tool validation specific to that agent's workflow
- Output filtering to keep agent context clean
- Safety constraints for specialized agents
- Setup/cleanup tied to agent lifetime

**Use global hooks for:**
- Project-wide automation (linting, formatting)
- Session setup/teardown
- Team-wide safety policies
- Environment configuration

## Hook Events in Agents

Agents support three hook events:

| Event | When | Use For |
|-------|------|---------|
| **PreToolUse** | Before agent uses any tool | Validate inputs, block operations |
| **PostToolUse** | After agent uses a tool | Filter output, verify results |
| **Stop** | When agent finishes | Cleanup, reporting |

## Quick Start: Add Your First Hook to an Agent

### Example: Safe Database Agent with Read-Only Validation

Create a file `db-reader.md`:

```yaml
---
name: db-reader
description: Execute read-only database queries and analyze results
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-query.sh"
---

You are a database analyst with read-only query access.

Execute SELECT queries to answer questions about the data.
When asked to analyze data:
1. Write efficient queries with appropriate filters
2. Present results with clear insights
3. Suggest follow-up questions based on findings

You cannot modify data—only SELECT queries are allowed.
```

Create `.claude/hooks/validate-query.sh`:

```bash
#!/bin/bash
# Validates that only SELECT queries are executed

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries allowed" >&2
  exit 2
fi

exit 0
```

Make it executable:
```bash
chmod +x .claude/hooks/validate-query.sh
```

**What happens:**
1. Before Bash executes, the hook runs
2. If command contains write operations, hook exits with code 2
3. Command is blocked, agent sees error message
4. Agent learns from the constraint

### Example: Code Reviewer with Auto-Linting

Create `code-reviewer.md`:

```yaml
---
name: code-reviewer
description: Review code changes and suggest improvements with automatic formatting
tools: Read, Edit, Bash, Grep
model: sonnet
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---

You are a code reviewer analyzing code changes.

Review code for:
- Code quality and clarity
- Type safety and null checks
- Security vulnerabilities
- Test coverage gaps
- Performance concerns

When you modify code files, linting runs automatically to ensure quality.
```

Create `.claude/hooks/run-linter.sh`:

```bash
#!/bin/bash

INPUT=$(cat)
tool=$(echo "$INPUT" | jq -r '.tool // empty')

# Only run linter after file edits
if [[ "$tool" =~ Edit|Write ]]; then
  # Find changed files and run linter
  changed_files=$(git diff --name-only --diff-filter=d | grep -E '\.(ts|js|py)$')

  for file in $changed_files; do
    # Run appropriate linter
    if [[ "$file" =~ \.(ts|js)$ ]]; then
      npx eslint "$file" --fix 2>/dev/null || true
    elif [[ "$file" =~ \.py$ ]]; then
      black "$file" 2>/dev/null || true
    fi
  done
fi

exit 0
```

**What happens:**
1. After agent edits a file, PostToolUse hook fires
2. Hook automatically runs linter on changed files
3. Formatting issues fixed immediately
4. Agent continues with clean code

## Hook Syntax in Agents

### Frontmatter Format

```yaml
---
name: agent-name
description: What this agent does
tools: Read, Bash, Edit
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/post-edit.sh"
  Stop:
    hooks:
      - type: command
        command: "./scripts/cleanup.sh"
---

Your agent system prompt here...
```

### Key Fields

- `PreToolUse` / `PostToolUse`: Event type
- `matcher`: Which tool(s) to hook (tool name or regex like `"Bash"`, `"Edit|Write"`)
- `hooks`: Array of hook commands
- `type: "command"`: Always use command type for agent hooks
- `command`: Script path to run

## Common Patterns

### Pattern 1: Input Validation (PreToolUse)

Validate and potentially modify inputs before tool execution:

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-bash.sh"
```

Script: `.claude/hooks/validate-bash.sh`

```bash
#!/bin/bash

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Example: Only allow npm commands (not arbitrary bash)
if ! echo "$COMMAND" | grep -E '^(npm|node|yarn)' > /dev/null; then
  # If not allowed, exit with code 2 to block
  echo "Only npm/node commands allowed" >&2
  exit 2
fi

exit 0
```

**Exit codes:**
- `0`: Allow the operation
- `2`: Block the operation (command fails)

### Pattern 2: Output Filtering (PostToolUse)

Filter verbose output to keep agent context clean:

```yaml
hooks:
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/filter-output.sh"
```

Script: `.claude/hooks/filter-output.sh`

```bash
#!/bin/bash

INPUT=$(cat)
hook_event=$(echo "$INPUT" | jq -r '.hook_event_name // ""')

if [ "$hook_event" = "PostToolUse" ]; then
  output=$(echo "$INPUT" | jq -r '.tool_output.stdout // ""')

  # Only keep meaningful lines, filter noise
  filtered=$(echo "$output" | grep -v '^$' | grep -v '^loading' | tail -20)

  # Return filtered output as additional context
  echo "{\"hookSpecificOutput\":{\"additionalContext\":\"Output summary:\n$filtered\"}}"
  exit 0
fi

exit 0
```

**PostToolUse output:**
- `additionalContext`: Text to add to agent's context about the tool result
- Useful for summarizing large outputs

### Pattern 3: Conditional Blocking

Block operations based on conditions:

```yaml
hooks:
  PreToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "./scripts/block-critical-files.sh"
```

Script: `.claude/hooks/block-critical-files.sh`

```bash
#!/bin/bash

INPUT=$(cat)

# For Edit tool, get the file path
file_path=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Block modifications to critical files
critical_files=("package.json" "tsconfig.json" "Dockerfile" ".env")

for critical in "${critical_files[@]}"; do
  if [[ "$file_path" == *"$critical" ]]; then
    echo "Cannot edit critical file: $critical" >&2
    exit 2
  fi
done

exit 0
```

### Pattern 4: Command Transformation

Modify commands before execution:

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/transform-command.sh"
```

Script: `.claude/hooks/transform-command.sh`

```bash
#!/bin/bash

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Add safety flags to npm scripts
if [[ "$COMMAND" =~ npm\ install ]]; then
  modified="$COMMAND --audit --audit-level=moderate"
  echo "{\"hookSpecificOutput\":{\"updatedInput\":{\"command\":\"$modified\"}}}"
  exit 0
fi

exit 0
```

**PreToolUse with modification:**
```json
{
  "hookSpecificOutput": {
    "updatedInput": {
      "command": "modified command here"
    }
  }
}
```

### Pattern 5: Cleanup (Stop Hook)

Run cleanup when agent finishes:

```yaml
hooks:
  Stop:
    hooks:
      - type: command
        command: "./scripts/agent-cleanup.sh"
```

Script: `.claude/hooks/agent-cleanup.sh`

```bash
#!/bin/bash

# Cleanup operations when agent finishes
# (no input for Stop hooks)

# Remove temporary files
rm -f /tmp/agent-*.tmp

# Restore original state
if [ -f ".env.backup" ]; then
  cp .env.backup .env
fi

# Log completion
echo "Agent cleanup completed at $(date)" >> ~/.claude/agent.log

exit 0
```

## Real-World Examples

### Example 1: Safe Code Modifier

Prevents accidental deletion and auto-formats:

```yaml
---
name: code-fixer
description: Fix code issues automatically with safety constraints
tools: Read, Edit, Bash
hooks:
  PreToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "./scripts/prevent-deletion.sh"
  PostToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "./scripts/auto-format.sh"
---

You fix code issues automatically.

When modifying code:
1. Make minimal targeted changes
2. Preserve existing formatting where possible
3. Add comments explaining complex logic

Never delete entire files—request permission instead.
```

Scripts:

`.claude/hooks/prevent-deletion.sh`:
```bash
#!/bin/bash
INPUT=$(cat)
file=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
new_content=$(echo "$INPUT" | jq -r '.tool_input.new_string // ""')

# Prevent setting file to empty
if [ -z "$new_content" ]; then
  echo "Cannot delete file content. Use Write for new files." >&2
  exit 2
fi

exit 0
```

`.claude/hooks/auto-format.sh`:
```bash
#!/bin/bash
INPUT=$(cat)
file=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Auto-format Python files
if [[ "$file" =~ \.py$ ]]; then
  black "$file" 2>/dev/null || true
fi

exit 0
```

### Example 2: Data Analyst with Query Logging

Logs all queries and validates read-only access:

```yaml
---
name: data-analyst
description: Query data warehouse and generate reports
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-sql.sh"
        - type: command
          command: "./scripts/log-query.sh"
---

You are a data analyst with read-only access to the warehouse.

Execute SELECT queries to:
1. Understand data structure
2. Answer analytical questions
3. Generate insights

All queries are logged for audit purposes.
```

`.claude/hooks/validate-sql.sh`:
```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Only SELECT queries
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE)\b' > /dev/null; then
  echo "Write operations not allowed" >&2
  exit 2
fi

exit 0
```

`.claude/hooks/log-query.sh`:
```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Log query
echo "[$timestamp] Query: $COMMAND" >> ~/.claude/query-audit.log

exit 0
```

### Example 3: DevOps Agent with Dry-Run Testing

Tests all commands before execution:

```yaml
---
name: devops-executor
description: Execute infrastructure operations with automatic dry-run validation
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/dry-run-first.sh"
---

You execute infrastructure commands.

For every command:
1. The hook runs a dry-run first
2. If dry-run succeeds, execute real command
3. If dry-run fails, show error without executing

This prevents unintended infrastructure changes.
```

`.claude/hooks/dry-run-first.sh`:
```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Add --dry-run if it's a terraform or deployment command
if [[ "$COMMAND" =~ terraform\ apply ]]; then
  dry_run="${COMMAND/apply/plan}"

  # Run dry-run
  if ! eval "$dry_run" > /tmp/dryrun.log 2>&1; then
    echo "Dry-run failed. Command blocked:" >&2
    cat /tmp/dryrun.log >&2
    exit 2
  fi

  echo "Dry-run succeeded. Proceeding with real command." >&2
fi

exit 0
```

## Hook Input/Output Reference

### PreToolUse Input

```json
{
  "tool": "Bash",
  "tool_input": {
    "command": "npm test"
  },
  "cwd": "/home/user/project",
  "hook_event_name": "PreToolUse"
}
```

**Output Options:**

Allow operation:
```json
{"hookSpecificOutput": {"permissionDecision": "allow"}}
```

Block operation:
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "deny",
    "permissionDecisionReason": "Reason why blocked"
  }
}
```

Modify input:
```json
{
  "hookSpecificOutput": {
    "updatedInput": {
      "command": "modified command"
    }
  }
}
```

### PostToolUse Input

```json
{
  "tool": "Bash",
  "tool_input": {"command": "npm test"},
  "tool_output": {
    "stdout": "...",
    "stderr": "...",
    "exit_code": 0
  },
  "hook_event_name": "PostToolUse"
}
```

**Output:**

Add context about result:
```json
{
  "hookSpecificOutput": {
    "additionalContext": "Tests passed: 42 passing"
  }
}
```

### Stop Hook Input

Stop hooks receive no specific input. They run when agent finishes.

## Debugging Agent Hooks

### Enable Debug Logging

```bash
claude --debug hooks
```

### Test Hook Locally

Create test input JSON file:

```bash
cat > test-input.json << 'EOF'
{
  "tool": "Bash",
  "tool_input": {"command": "npm test"},
  "hook_event_name": "PreToolUse"
}
EOF
```

Run hook:
```bash
cat test-input.json | bash .claude/hooks/validate.sh
echo "Exit code: $?"
```

### Common Issues

**Hook not executing:**
- Verify script is executable: `chmod +x .claude/hooks/*.sh`
- Check frontmatter YAML syntax (use a YAML validator)
- Verify matcher matches tool name exactly
- Check script path is correct

**Hook timing out:**
- Add timeout to hook: `timeout 5 ./script.sh`
- Optimize script performance
- Use jq for efficient JSON parsing

**JSON parsing errors:**
- Validate input: `cat test-input.json | jq .`
- Use `jq -r` to extract strings
- Escape special characters properly

**Permission denied:**
- Run `chmod +x` on all hook scripts
- Check script shebang: `#!/bin/bash`
- Verify user has execute permission

## Best Practices

### ✅ Do

1. **Make scripts fast** - Hooks run synchronously, slow hooks block agent
2. **Use meaningful exit codes** - 0 for success, 2 for deny, 1 for error
3. **Escape JSON carefully** - Use `jq` for safe parsing
4. **Log issues** - Write errors to stderr for debugging
5. **Keep it simple** - One concern per hook
6. **Test locally** - Verify script behavior before using in agent

### ❌ Don't

1. **Don't make complex decisions** - Hooks are for validation, not logic
2. **Don't make hooks slow** - Keep execution under 1 second
3. **Don't modify files unnecessarily** - Only transform inputs/outputs
4. **Don't assume file existence** - Check paths with `[ -f ]` first
5. **Don't hardcode paths** - Use `$CLAUDE_PROJECT_DIR` for paths
6. **Don't forget error handling** - Always handle edge cases

## Security Considerations

### Hook Execution Context

- Hooks run with your user permissions
- Can access/modify any files you can access
- Run on your local system (not in container)
- Have access to environment variables

### Safe Hook Writing

```bash
#!/bin/bash
# ✅ Good: Validate inputs, use allowlists

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Only allow specific commands
if [[ "$COMMAND" =~ ^(npm|yarn|node) ]]; then
  exit 0
else
  exit 2
fi
```

```bash
#!/bin/bash
# ❌ Bad: Trust everything, use blocklists

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block just rm (but could sneak in other destructive commands)
if [[ "$COMMAND" == *"rm"* ]]; then
  exit 2
fi

exit 0
```

## Comparison: When to Use Hooks vs. Other Features

| Need | Use | Why |
|------|-----|-----|
| Validate before tool runs | PreToolUse hook | Synchronous blocking |
| Filter tool output | PostToolUse hook | Keeps context clean |
| Cleanup after agent | Stop hook | Automatic teardown |
| Always-on validation | Global hooks | Project-wide consistency |
| Complex workflow | Skills/Agents | LLM involvement needed |

## References

- [Sub-agents Documentation](/en/sub-agents) - Full agent configuration
- [Hooks Reference](/en/hooks) - Global hooks (different from agent hooks)
- [Settings Files](/en/settings) - Where to configure hooks

## Next Steps

1. Choose a simple validation use case (block dangerous git commands)
2. Create a test agent with a PreToolUse hook
3. Test locally with test-input.json
4. Add filtering with PostToolUse hooks
5. Include cleanup with Stop hooks
6. Share specialized agent with team

**Start small:** a single validation hook is often more useful than trying to do everything at once.

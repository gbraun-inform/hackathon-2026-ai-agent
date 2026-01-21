# Permission Modes Reference

Permission modes control how agents handle user interactions, confirmations, and permission checking. This reference explains each mode and when to use it.

## Overview

Permission modes determine whether/how agents need user approval for operations:

```yaml
permissionMode: default          # Standard permission checks (default)
permissionMode: acceptEdits      # Auto-approve file edits
permissionMode: dontAsk          # Skip prompts (auto-deny)
permissionMode: bypassPermissions # Skip all permission checks (dangerous)
permissionMode: plan             # Read-only mode
```

Each mode represents a different balance between **automation** (fewer prompts) and **control** (user approval).

---

## Permission Modes Reference

### default

**Behavior**: Standard permission checking. Agent must request permission for sensitive operations.

**When Claude makes a tool call:**
- **Safe operations** (Read, Grep, Glob): Proceed automatically
- **Modification operations** (Write, Edit): Prompt user for approval
- **External operations** (WebFetch, WebSearch): Proceed
- **Dangerous operations** (Bash, Task): Prompt user

**Example flow:**
```
Agent: "I'll fix the bug by editing src/auth.ts"
Claude Code: [Prompts user] "Allow edit to src/auth.ts? (yes/no)"
User: "yes"
→ Edit proceeds
```

**Use when:**
- Agent can modify code (general editing)
- User wants visibility into changes
- Making changes that need approval
- Standard development workflow

**Example:**
```yaml
name: bug-fixer
description: Find and fix bugs
tools: [Read, Edit, Bash]
permissionMode: default
```

---

### acceptEdits

**Behavior**: Automatically approve file modification operations without user confirmation.

**Operations:**
- **Safe operations** (Read, Grep, Glob): Proceed
- **Modification operations** (Write, Edit): Proceed automatically
- **External operations** (WebFetch, WebSearch): Proceed
- **Dangerous operations** (Bash): Proceed automatically
- **Note**: Some critical operations may still prompt

**Example flow:**
```
Agent: "I'll fix the bug by editing src/auth.ts"
Claude Code: [Proceeds immediately, no prompt]
→ Edit applied automatically
```

**Advantages:**
- Higher productivity (no confirmation delays)
- Fewer interruptions
- Good for automated fixes

**Disadvantages:**
- Less visibility into changes
- Agent could modify unexpected files
- Mistakes aren't caught by user approval

**Use when:**
- Agent is highly specialized and reliable
- Fixing obvious issues (linting, formatting)
- Changes are low-risk (tests, documentation)
- Development environment (not production)
- Agent has restricted tool access

**Risk mitigation:**
- Combine with restrictive tool access
- Use specific file patterns
- Verify changes in version control
- Run tests after agent completes

**Example:**
```yaml
name: formatter
description: Format code style
tools: [Read, Edit]
permissionMode: acceptEdits

# Safer because:
# - Restricted to Edit only (no Bash/Write)
# - Read + Edit = targeted fixing
# - Formatting is low-risk operation
```

---

### dontAsk

**Behavior**: Skip permission prompts entirely. Operations proceed or fail silently based on tool access.

**Operations:**
- **All operations**: No user prompts
- **If tool is allowed**: Operation proceeds
- **If tool is blocked**: Operation fails silently

**Example flow:**
```
Agent: "I'll analyze the code and report findings"
Claude Code: [Proceeds with allowed operations]
         [Silently skips blocked operations]
→ No prompts at any point
```

**Advantages:**
- Maximum automation
- Useful for background agents
- No interruptions

**Disadvantages:**
- Very limited visibility
- Easy for agent to do unexpected things
- Hard to debug issues
- Agent can't request user clarification

**Use when:**
- Agent is read-only (no modifications)
- Background/automated tasks
- Highly restricted tool access
- Trusted, well-tested agents
- Research/analysis agents

**Example:**
```yaml
name: code-analyzer
description: Analyze code structure
tools: [Read, Grep, Glob]
permissionMode: dontAsk

# Safe because:
# - Read-only (can't modify)
# - Limited tools (no Bash/Write/Edit)
# - Analysis only (no dangerous operations)
```

**Typical use case:**
```
Claude delegates to analyzer:
→ Analyzer reads files, searches patterns
→ No prompts, all operations succeed
→ Reports findings back to Claude
→ Claude provides summary to user
```

---

### plan

**Behavior**: Read-only mode. Agent can explore and plan but cannot make changes.

**Operations:**
- **Safe operations** (Read, Grep, Glob, Bash): Proceed
- **Modification operations** (Write, Edit): Blocked
- **External operations** (WebFetch, WebSearch): Proceed
- **Dangerous operations**: Blocked

**Example flow:**
```
Agent: "I'll explore the codebase structure"
Claude Code: [Allows read operations]
         [Blocks write/edit operations]
→ Agent explores but cannot modify

Agent: "I'll write the fix"
Claude Code: [Blocks Write operation]
         [User sees error: "Cannot write in plan mode"]
```

**Advantages:**
- Completely safe (read-only)
- Agent can still explore and analyze
- No accidental modifications
- Good for planning phases

**Disadvantages:**
- Agent can't make changes
- More limited usefulness
- Requires follow-up action

**Use when:**
- Planning and analysis phase
- Reviewing/auditing code
- Exploratory work
- Initial investigation
- High-risk environments

**Example:**
```yaml
name: code-reviewer
description: Review code quality
tools: [Read, Grep, Bash]
permissionMode: plan

# Perfect because:
# - Read-only by nature
# - Can run linters/type checkers (Bash)
# - Cannot modify code
# - Safe for any environment
```

**Typical workflow:**
```
1. Claude delegates to reviewer (plan mode)
   → Reviewer analyzes code
   → Reviewer reports issues
2. Claude provides issues to user
3. User decides how to fix
4. Claude delegates to fixer (acceptEdits)
   → Fixer implements solutions
```

---

### bypassPermissions

**Behavior**: Skip ALL permission checks. Agent can do anything with its configured tools without any confirmation.

⚠️ **SECURITY WARNING**: This mode is dangerous and should be used only in restricted environments.

**Operations:**
- ALL operations proceed without checks
- No confirmation prompts
- No validation
- Maximum autonomy

**Advantages:**
- Complete automation
- Useful for CI/CD
- No delays

**Disadvantages:**
- Very dangerous
- Easy for agent to cause damage
- Hard to audit
- Should not be used for general agents

**Use when:**
- Fully automated CI/CD pipeline
- Restricted service account
- Highly constrained tool access
- Trusted, audited agent code
- Development/testing environments ONLY

**NEVER use when:**
- In production with external agents
- With high-privilege operations (Bash, Write)
- Without thorough testing
- In multi-user environments
- With untested agent behavior

**Example (only in CI/CD):**
```yaml
name: ci-pipeline-agent
description: Run CI/CD pipeline
tools: [Read, Bash]  # Very restricted!
permissionMode: bypassPermissions

# Only safe because:
# - Used in CI/CD (controlled environment)
# - Service account (no user interaction)
# - Restricted tools (Read + Bash only)
# - Tested and audited
```

**If you need bypassPermissions, first verify:**
1. Tool access is extremely restricted
2. Agent behavior is thoroughly tested
3. Environment is restricted/controlled
4. Audit trail is enabled (hooks)
5. Damage is limited even if agent misbehaves

---

## Choosing the Right Permission Mode

Use this decision tree:

```
Question: What should the agent do?

├─ Agent only analyzes/explores?
│  └─ YES → Use "plan" mode
│           tools: [Read, Grep, Glob]
│           (read-only is safest)
│
├─ Agent needs visibility for changes?
│  └─ YES → Use "default" mode
│           (user approves each change)
│
├─ Agent makes obvious/low-risk fixes?
│  └─ YES → Use "acceptEdits" mode
│           BUT restrict tools carefully!
│           (combine with dontAsk OR default)
│
├─ Agent is background/automated?
│  └─ YES → Use "dontAsk" mode
│           ONLY if tools are read-only!
│           tools: [Read, Grep, Bash]
│
└─ Agent needs complete autonomy?
   └─ DANGER → Only if:
              - CI/CD environment
              - Heavily restricted tools
              - Thoroughly tested
              - Audit enabled
              → Use "bypassPermissions"
```

---

## Permission Mode Comparison

| Mode | User Prompts | Edit Changes | External Calls | Best For |
|------|-------------|--------------|----------------|----------|
| **default** | Yes (for edits) | Ask permission | Auto | General editing |
| **acceptEdits** | No | Auto-approve | Auto | Quick fixes |
| **dontAsk** | No | Blocked/silent | Auto | Background work |
| **plan** | No | Blocked | Auto | Exploration/review |
| **bypassPermissions** | No | Auto-approve | Auto | CI/CD only ⚠️ |

---

## Common Configurations

### Configuration 1: Safe Review Agent

```yaml
name: code-reviewer
description: Review code for quality issues
tools: [Read, Grep, Glob, Bash]
permissionMode: plan
```

**Why this works:**
- Read-only mode ensures safety
- Can still run tools (linters, type-checkers)
- No dangerous operations possible
- Safe in any environment

---

### Configuration 2: Careful Bug Fixer

```yaml
name: bug-fixer
description: Find and fix bugs
tools: [Read, Edit, Bash, Grep]
permissionMode: default
```

**Why this works:**
- User sees what changes are proposed
- User approves each fix
- Still can run tests to verify
- Good balance of productivity + safety

---

### Configuration 3: Fast Formatter

```yaml
name: code-formatter
description: Format code style
tools: [Read, Edit]
permissionMode: acceptEdits
```

**Why this works:**
- Formatting is low-risk
- Edit-only (no other tools)
- No need for user approval
- Clear, focused responsibility

---

### Configuration 4: Background Analyzer

```yaml
name: architecture-analyzer
description: Analyze codebase architecture
tools: [Read, Grep, Glob]
permissionMode: dontAsk
```

**Why this works:**
- Read-only operations only
- No prompts needed
- Can run in background
- Reports findings when done

---

### Configuration 5: Dangerous Pattern (AVOID)

```yaml
# ❌ DO NOT USE:
name: bad-agent
tools: [Read, Write, Edit, Bash]
permissionMode: bypassPermissions
```

**Why this is dangerous:**
- Unrestricted tools
- Bypasses all permission checking
- Can modify/delete anything
- No safety net

---

## Permission Mode + Tool Access Strategy

The best agents combine tool restrictions with permission modes:

```
Low Risk:
├─ Limited tools + plan mode
│  └─ tools: [Read, Grep] + permissionMode: plan
│     (Almost no risk)
│
├─ Limited tools + dontAsk mode
│  └─ tools: [Read, Grep, Bash] + permissionMode: dontAsk
│     (Very low risk)
│
├─ Limited tools + acceptEdits mode
│  └─ tools: [Read, Edit] + permissionMode: acceptEdits
│     (Low risk - limited editing)
│
Medium Risk:
├─ Moderate tools + default mode
│  └─ tools: [Read, Write, Edit, Bash] + permissionMode: default
│     (User approval for changes)
│
High Risk:
├─ Extensive tools + default mode
│  └─ tools: [Read, Write, Edit, Bash, WebFetch] + permissionMode: default
│     (Many capabilities, approval needed)
│
├─ Extensive tools + acceptEdits mode
│  └─ tools: [Read, Write, Edit, Bash] + permissionMode: acceptEdits
│     (No approval needed - high risk)
│
Extreme Risk:
├─ Any tools + bypassPermissions
│  └─ ⚠️  Only in CI/CD with heavy restrictions
```

---

## Troubleshooting Permission Issues

### "Agent keeps asking for permission"
→ You're using `permissionMode: default`
→ If tired of prompts, switch to `acceptEdits` (for low-risk changes)
→ Or switch to `dontAsk` (for read-only agents)

### "Agent made unexpected changes"
→ You're using `acceptEdits` with too many tools
→ Restrict tools: remove Write, keep only Edit
→ Or switch back to `default` for approval

### "Agent can't complete its task"
→ Permissions are too restrictive
→ Check if agent needs more tool access
→ Or higher permissionMode (dontAsk → acceptEdits → default)

### "Agent modifying files I don't want changed"
→ Tool access is too broad
→ Restrict to specific tools needed
→ Use `plan` mode for safety

### "Agent doing things silently"
→ You're using `dontAsk` or `bypassPermissions`
→ Switch to `default` for visibility
→ Or use hooks to log operations

---

## Best Practices

1. **Start restrictive**: Use `plan` mode initially, upgrade as needed
2. **Match tools to permissions**: Limited tools work with `acceptEdits`, extensive tools need `default`
3. **Read-only = safe**: `plan` mode is safest, use for analysis
4. **Approval for uncertainty**: Use `default` if unsure about agent behavior
5. **Document rationale**: Comment why you chose this permission mode
6. **Audit production**: Use hooks/logging with higher permission modes
7. **Test thoroughly**: Test permission behavior before deployment
8. **Never assume `bypassPermissions` is OK**: Really think through risks

---

## Quick Reference Decision Table

**Choose mode based on:**

| Scenario | Recommended Mode | Why |
|----------|-----------------|-----|
| Code review/analysis | `plan` | Safe read-only |
| Bug fixing (approval each time) | `default` | User sees changes |
| Low-risk auto-fixes | `acceptEdits` | With restricted tools |
| Background analysis | `dontAsk` | With read-only tools |
| CI/CD automation | `bypassPermissions` | With extreme caution ⚠️ |

Remember: The safest agent is one that can't do damage even if compromised.

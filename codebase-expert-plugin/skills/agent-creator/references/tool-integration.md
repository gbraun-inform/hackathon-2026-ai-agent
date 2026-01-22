# Tool Integration Guide

This reference explains how to select and configure tools for agents. Tool selection is critical—it defines what an agent can and cannot do, and impacts both capability and security.

## Understanding Tool Access

### Tool Inheritance Model

Agents inherit the default tool set from Claude Code unless you explicitly specify different tools:

```yaml
# Option 1: No tools field (inherit defaults)
name: my-agent
description: ...

# Option 2: Specify allowed tools (allowlist)
tools: [Read, Grep, Bash]

# Option 3: Specify disallowed tools (denylist)
disallowedTools: [Write, Edit]

# Option 4: Both (denylist takes precedence over defaults)
tools: [Read, Write, Edit, Bash]
disallowedTools: [Edit]
```

**Best Practice:** Use explicit allowlist (`tools:`) for restricted agents. Use denylist (`disallowedTools:`) only when you want most tools but need to block a few.

### Why Tool Restrictions Matter

**Security:**
```yaml
# Risky: Agent can write anywhere
tools: [Read, Write, Bash]

# Better: Restrict write scope with permissions/validation
tools: [Read, Write]
permissionMode: acceptEdits

# Best: Read-only for auditing
tools: [Read, Grep, Glob]
```

**Focus:**
```yaml
# Unfocused: Agent tries to do everything
tools: [Read, Write, Edit, Bash, WebFetch, WebSearch]

# Focused: Agent has right tools for job
tools: [Read, Grep, Bash]
```

---

## Tool Categories

### Read-Only Tools

These tools do not modify state. Safe for unrestricted access.

#### Read

- **Purpose**: Read file contents
- **When to use**: Exploring code, analyzing files, understanding structure
- **Safety**: Very safe (read-only)
- **Typical use**: In all analysis agents

```yaml
tools: [Read, Grep, Bash]  # Analysis agent
```

#### Grep

- **Purpose**: Search file contents with regex
- **When to use**: Finding patterns, locating specific code
- **Safety**: Very safe (read-only)
- **Typical use**: Combined with Read for analysis

#### Glob

- **Purpose**: Find files by pattern
- **When to use**: Discovering files, understanding structure
- **Safety**: Very safe (read-only)
- **Typical use**: Project exploration, finding test files

#### Bash

- **Purpose**: Execute shell commands
- **When to use**: Running tools (tsc, eslint, pytest, git, etc.)
- **Safety**: Moderate - can read system state, execute tools
- **Restrictions**: Consider for sensitive environments
- **Typical use**: Validation, testing, compilation

Example read-only agent:
```yaml
name: code-analyzer
tools: [Read, Grep, Glob, Bash]
description: Analyze codebase structure and find patterns
```

### Modification Tools

These tools modify files. Require careful consideration.

#### Write

- **Purpose**: Create or replace entire files
- **When to use**: Creating new files, generating code
- **Safety**: Moderate - overwrites files
- **Risk**: Accidentally overwriting important files
- **Typical use**: Code generation, test generation

#### Edit

- **Purpose**: Modify specific content in files
- **When to use**: Fixing bugs, applying targeted changes
- **Safety**: Higher than Write (edits specific content)
- **Risk**: Breaking file structure if edit targets wrong text
- **Typical use**: Bug fixes, refactoring, formatting

**Combination strategy:**
```yaml
# For safe generation (new files only)
tools: [Read, Write, Glob]

# For safe editing (targeted changes)
tools: [Read, Edit, Bash]

# For full editing (new + modify)
tools: [Read, Write, Edit, Bash]
```

### External Tools

These tools interact with external systems.

#### WebFetch

- **Purpose**: Fetch content from URLs
- **When to use**: Researching documentation, retrieving data
- **Safety**: Moderate - depends on URLs fetched
- **Risk**: SSRF attacks, fetching malicious content
- **Typical use**: API documentation, research

#### WebSearch

- **Purpose**: Search the web for information
- **When to use**: Research, finding documentation
- **Safety**: Moderate - searches public internet
- **Risk**: Can access any public information
- **Typical use**: Finding solutions, researching patterns

**Research agent example:**
```yaml
name: research-agent
tools: [Read, WebFetch, WebSearch, Grep]
description: Research and find information about technologies
```

### Meta Tools

These tools manage agent lifecycle or invoke other agents.

#### Task (Agent Invocation)

- **Purpose**: Delegate to other agents
- **When to use**: Coordinate parallel tasks, delegate specialized work
- **Safety**: Depends on delegated agent
- **Risk**: Complex chains, loss of context
- **Typical use**: Orchestration agents

#### EnterPlanMode / ExitPlanMode

- **Purpose**: Planning and design mode
- **When to use**: Complex tasks needing design phase
- **Safety**: Read-only (planning phase)
- **Typical use**: Specialist agents for analysis

#### Skill

- **Purpose**: Invoke skills
- **When to use**: Leverage existing skills
- **Safety**: Depends on skill
- **Typical use**: Specialized functionality

---

## Tool Selection Decision Tree

Use this decision tree to choose tools for your agent:

```
Start: What does your agent do?

├─ Read/Analyze Code?
│  └─ YES → Use [Read, Grep, Glob, Bash]
│
├─ Find/Create New Files?
│  └─ YES → Add Write: [Read, Write, Glob, Bash]
│
├─ Fix/Modify Existing Files?
│  └─ YES → Add Edit: [Read, Edit, Bash]
│
├─ External Research/API Calls?
│  └─ YES → Add WebFetch/WebSearch: [Read, WebFetch, WebSearch]
│
├─ Need to Run Tests/Build?
│  └─ YES → Keep Bash: [Read, Bash]
│
└─ Complex Multi-Step Work?
   └─ YES → Consider Task for sub-agents: [..., Task]
```

### Quick Reference: Common Tool Combinations

| Agent Type | Purpose | Tools |
|-----------|---------|-------|
| **Code Reviewer** | Review code quality | `[Read, Grep, Glob, Bash]` |
| **Security Auditor** | Security analysis | `[Read, Grep, Glob, Bash]` |
| **Test Generator** | Create tests | `[Read, Write, Bash, Grep]` |
| **Bug Fixer** | Fix bugs | `[Read, Edit, Bash, Grep]` |
| **Refactorer** | Improve structure | `[Read, Edit, Bash, Grep]` |
| **Code Generator** | Create new code | `[Read, Write, Glob, Bash]` |
| **Researcher** | Find information | `[Read, WebFetch, WebSearch]` |
| **API Designer** | Design APIs | `[Read, Grep, Glob]` |
| **DB Optimizer** | Optimize queries | `[Read, Grep, Bash]` |
| **Build Validator** | Check builds | `[Read, Edit, Bash, Grep, Glob]` |

---

## Security Considerations: Principle of Least Privilege

Always give agents only the minimum tools they need.

### Security Risk Levels

**VERY HIGH RISK (Avoid):**
```yaml
# Agent can modify anything
tools: [Read, Write, Edit, Bash]
permissionMode: bypassPermissions
```

**HIGH RISK (Use with caution):**
```yaml
# Agent can modify code without restrictions
tools: [Read, Write, Edit, Bash]
```

**MODERATE RISK (Acceptable):**
```yaml
# Agent can modify but needs approval
tools: [Read, Write, Edit, Bash]
permissionMode: default

# Or: Agent can only modify specific types
tools: [Read, Edit]
disallowedTools: [Bash, Write]
```

**LOWER RISK (Preferred):**
```yaml
# Agent can create new files but not modify existing
tools: [Read, Write, Glob]
disallowedTools: [Edit]

# Or: Agent is read-only
tools: [Read, Grep, Glob]
```

### Environment-Specific Tool Choices

**Development Environment:**
```yaml
# More permissive during development
tools: [Read, Write, Edit, Bash, Grep, Glob]
```

**Production Environment:**
```yaml
# Restricted in production
tools: [Read, Grep, Glob]  # Read-only analysis

# Or careful editing with approval
tools: [Read, Edit]
permissionMode: default
```

**CI/CD Pipeline:**
```yaml
# Limited tools for automation
tools: [Read, Bash]
# Or for code generation:
tools: [Read, Write, Bash]
```

---

## Tool Restrictions: Allowlist vs Denylist

### Allowlist Approach (Recommended)

```yaml
# Explicit: "Agent can use ONLY these tools"
tools: [Read, Grep, Bash]
```

**Advantages:**
- Clear and explicit about capabilities
- Secure by default (can't use unexpected tools)
- Easy to audit and review
- Future-proof (new tools don't affect agent)

**When to use:**
- Security-sensitive agents
- Restricted environments
- Production systems
- Public/untrusted agents

### Denylist Approach

```yaml
# Implicit: "Agent can use all tools EXCEPT these"
disallowedTools: [Write, Edit]
```

**Advantages:**
- Less restrictive
- Easier to write (fewer tools to list)
- Automatically gets new tools

**Disadvantages:**
- Less secure (unexpected tools available)
- Hard to predict future behavior (new tools)
- More complex to audit

**When to use:**
- Internal/trusted agents only
- Agents that need flexible tool access
- Research/development

---

## Tool Combinations for Common Scenarios

### Scenario: Code Review Agent

**Goal**: Review code for quality/security without modifying

```yaml
name: code-reviewer
tools: [Read, Grep, Glob, Bash]
description: Review code for quality issues
permissionMode: plan
```

**Rationale:**
- **Read**: Examine code files
- **Grep**: Find patterns, search for issues
- **Glob**: Discover related files
- **Bash**: Run linters, type checkers
- **No Write/Edit**: Can't accidentally modify code

### Scenario: Bug Fix Agent

**Goal**: Find and fix bugs in code

```yaml
name: bug-fixer
tools: [Read, Edit, Bash, Grep]
description: Find and fix bugs
permissionMode: acceptEdits
```

**Rationale:**
- **Read**: Understand buggy code
- **Edit**: Fix specific issues
- **Bash**: Run tests to verify fix
- **Grep**: Search for related issues
- **No Write**: Don't create new files
- **acceptEdits**: Auto-approve fixes

### Scenario: Documentation Generator

**Goal**: Create/update documentation

```yaml
name: doc-generator
tools: [Read, Write, Glob]
description: Generate documentation
```

**Rationale:**
- **Read**: Understand code to document
- **Write**: Create .md files
- **Glob**: Find files to document
- **No Bash**: No need to execute
- **No Edit**: Create new files, not modify existing

### Scenario: Research Agent

**Goal**: Research and explore information

```yaml
name: research-agent
tools: [Read, WebFetch, WebSearch, Grep]
description: Research information and technologies
permissionMode: plan
```

**Rationale:**
- **Read**: Local file research
- **WebFetch**: Get specific URLs
- **WebSearch**: Search web for info
- **Grep**: Search local patterns
- **No modification tools**: Read-only

### Scenario: Build Pipeline Agent

**Goal**: Run builds, tests, and validation

```yaml
name: build-validator
tools: [Read, Edit, Bash, Grep]
description: Validate and fix build issues
```

**Rationale:**
- **Read**: Understand build config and errors
- **Edit**: Fix configuration issues
- **Bash**: Run build commands, tests
- **Grep**: Find error patterns
- **No Write**: Don't create test files directly

---

## Combining Tools with Permission Modes

Tool access and permission modes work together:

```yaml
# Read-only agent (safest)
tools: [Read, Grep, Bash]
permissionMode: plan
# Agent can read but not modify

# Auto-approving agent (productive)
tools: [Read, Write, Edit, Bash]
permissionMode: acceptEdits
# Agent can make changes without approval

# Approval-required agent (balanced)
tools: [Read, Write, Edit, Bash]
permissionMode: default
# Agent can request to make changes, needs approval

# Restricted/validated agent (compliance)
tools: [Read, Bash]
disallowedTools: [Write, Edit]
# Limited tools for sensitive contexts
```

---

## Testing Tool Configurations

When you create an agent, test its tool access:

1. **Verify allowlist works:**
   ```bash
   # Can agent use allowed tools?
   # Try each tool and verify success
   ```

2. **Verify denylist works:**
   ```bash
   # Does agent fail when using blocked tools?
   # Try each blocked tool and verify rejection
   ```

3. **Verify tool combinations:**
   ```bash
   # Do tools work well together?
   # Can agent accomplish its task?
   ```

4. **Test edge cases:**
   ```bash
   # What if agent tries unexpected tool combo?
   # Does security model hold?
   ```

---

## Troubleshooting Tool Issues

### "Agent can't find files"
→ Check Glob is included, or at least Read for traversal

### "Agent can't make changes"
→ Check Write/Edit are included, check permissionMode

### "Agent makes changes without approval"
→ Check permissionMode is not acceptEdits or bypassPermissions

### "Agent can't run tests/build"
→ Check Bash is included and executable

### "Agent can access external systems"
→ If unintended: Add to disallowedTools [WebFetch, WebSearch]

### "Agent seems too restricted"
→ Review allowed tools, consider adding necessary capabilities

---

## Best Practices

1. **Start restrictive**: Begin with fewer tools, add as needed
2. **Use allowlist**: Explicit `tools:` over `disallowedTools:` for security
3. **Match purpose**: Tool set should exactly match agent's responsibility
4. **Document rationale**: Comment why specific tools are needed/blocked
5. **Audit regularly**: Review tool access as agent evolves
6. **Test thoroughly**: Verify tool access works as intended
7. **Combine with permissions**: Use permissionMode to add another security layer

Example well-designed agent:
```yaml
name: code-reviewer
description: Review code quality and security

# Explicit tool access for security
tools: [Read, Grep, Glob, Bash]

# Read-only mode prevents changes
permissionMode: plan

# Model choice reflects task complexity
model: opus
```

This agent:
- Has clear, restricted tool access ✅
- Is explicitly read-only ✅
- Matches its purpose (review, not modify) ✅
- Uses capable model for complex analysis ✅
- Is secure and focused ✅

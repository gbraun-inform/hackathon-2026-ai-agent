---
name: agent-creator
description: Comprehensive guide for creating Claude Code agents. Use this skill when building autonomous agents that can work on complex, multi-step tasks. Supports agent design, planning, implementation, testing, and packaging. Includes scaffolding tools and best practices for specialized agents, multi-turn workflows, and agent orchestration patterns.
---

# Agent Creator

This skill provides complete guidance for creating effective Claude Code agents—autonomous task executors equipped with specialized knowledge, tools, and multi-step workflows.

## What Are Agents?

Agents are autonomous Claude instances designed to handle complex tasks independently. Unlike skills (which provide procedural knowledge), agents are independent workers that can:

- Execute multi-step workflows without user intervention
- Use tools autonomously to accomplish goals
- Handle task planning and error recovery
- Maintain context across multiple tool calls
- Work in the background on long-running tasks

### When to Create an Agent

Create an agent when:
- The task requires multiple steps executed in sequence
- Decisions must be made based on intermediate results
- The work is primarily autonomous (minimal user interaction needed)
- Error handling and recovery are important
- The agent needs to manage its own planning and progress

## Agent Design Principles

### 1. Clear Purpose and Scope

Define agents with a single, well-defined responsibility:
- **Good**: "Analyze code repository for security vulnerabilities"
- **Bad**: "Do everything related to security"

### 2. Appropriate Context Loading

Use progressive disclosure just like skills:
- **Agent prompt** (always loaded): High-level instructions and tool overview (~500 words)
- **Reference files** (as needed): Detailed documentation, patterns, schemas
- **Tool availability** (explicitly defined): Only agents tools needed for the task

### 3. Clear Success Criteria

Agents should understand:
- What success looks like
- When to stop working
- What constitutes a complete result
- How to report findings

## Agent Creation Process

### Step 1: Define the Agent

Answer these questions before coding:

1. **Purpose**: What specific task does this agent solve?
2. **Scope**: What's in scope and explicitly out of scope?
3. **Inputs**: What does the agent receive as input?
4. **Outputs**: What should the agent produce?
5. **Tools**: What tools does the agent need?
6. **Autonomous Duration**: How long should the agent run before returning results?

### Step 2: Plan Agent Architecture

Decide on the agent's structure:

- **Simple sequential**: Run steps in order, no branching
- **Decision tree**: Make choices based on results
- **Iterative refinement**: Loop until criteria met
- **Parallel operations**: Run independent tasks concurrently

See [agent-design-guide.md](references/agent-design-guide.md) for detailed patterns.

### Step 3: Initialize the Agent

Use the `init_agent.py` script to scaffold a new agent:

```bash
python scripts/init_agent.py <agent-name> --path <output-directory>
```

Example:
```bash
python scripts/init_agent.py security-auditor --path agents/
```

This creates:
```
security-auditor/
├── agent.py (main agent implementation)
├── AGENT.md (documentation)
├── references/
│   ├── security_checks.md
│   └── patterns.md
└── tools/
    ├── scanner.py
    └── analyzer.py
```

### Step 4: Implement the Agent

Edit the generated `agent.py` to:

1. **Define tool setup** - Configure tools the agent can use
2. **Write instructions** - Clear guidance for agent behavior
3. **Plan workflows** - Define step-by-step execution
4. **Add error handling** - Graceful failure recovery
5. **Set termination conditions** - When the agent should stop

Key patterns to follow:

- Use clear variable names for agent state tracking
- Break complex workflows into named functions
- Include logging at key decision points
- Validate tool outputs before using them
- Implement retry logic for transient failures

### Step 5: Test the Agent

Before deploying:

1. Test with sample inputs matching expected use cases
2. Verify tool usage is correct
3. Check error handling works as expected
4. Ensure output format matches specifications
5. Monitor token usage and adjust as needed

### Step 6: Package and Deploy

Once tested, package the agent for distribution or deployment.

## Agent Types Reference

See [agent-types-reference.md](references/agent-types-reference.md) for patterns including:

- **Analysis Agents**: Examine data/code and produce reports
- **Automation Agents**: Execute workflows and modify systems
- **Research Agents**: Gather and synthesize information
- **Planning Agents**: Break down problems and create plans
- **Coordination Agents**: Orchestrate other agents or services

## Common Agent Patterns

### Error Recovery Pattern

```
1. Attempt primary action
2. If error occurs:
   - Log error details
   - Check if retryable
   - Implement backoff/retry
   - If final failure, report gracefully
3. Continue or escalate as needed
```

### Iterative Refinement Pattern

```
1. Produce initial result
2. Evaluate against criteria
3. If criteria not met:
   - Identify gaps
   - Refine approach
   - Try again
   - Repeat up to max attempts
4. Return best result achieved
```

### Multi-Phase Pattern

```
1. Phase 1: Gather information
2. Phase 2: Process/analyze
3. Phase 3: Generate output
4. Phase 4: Validate and report
```

## Resources

This skill includes tools and guidance for agent creation:

### scripts/init_agent.py
Scaffolds a new agent with template code, prompts, and directory structure.

```bash
python scripts/init_agent.py <agent-name> --path <output-directory>
```

### scripts/quick_validate_agent.py
Validates agent structure before packaging. Run this to catch issues early:

```bash
python scripts/quick_validate_agent.py agents/my-agent
```

Checks for:
- AGENT.md exists with proper frontmatter
- agent.py main implementation file
- Required frontmatter fields (name, type, description)
- Proper directory structure (tools/, references/)
- Content quality and length

### scripts/package_agent.py
Creates a distributable agent package. Automatically runs validation:

```bash
python scripts/package_agent.py agents/my-agent
python scripts/package_agent.py agents/my-agent ./dist
```

### references/
Detailed documentation for:
- **agent-design-guide.md** - Design patterns, architecture decisions, workflow planning
- **agent-types-reference.md** - Common agent archetypes with examples

## Best Practices

1. **Keep instructions concise** - Agents learn best from clear, specific guidance
2. **Use typed parameters** - Make tool inputs/outputs explicit
3. **Plan before implementing** - Use Step 1 thoroughly
4. **Test incrementally** - Verify each major component works
5. **Monitor performance** - Track token usage and execution time
6. **Document decisions** - Maintain clear AGENT.md for future iteration
7. **Implement graceful degradation** - Handle missing tools or data gracefully
8. **Set realistic timeouts** - Prevent indefinite execution

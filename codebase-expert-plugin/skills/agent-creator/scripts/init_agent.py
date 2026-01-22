#!/usr/bin/env python3
"""
Agent Initializer - Creates a new agent from template

Usage:
    init_agent.py <agent-name> --path <path> --type <type>

Examples:
    init_agent.py code-reviewer --path .claude/agents --type read-only
    init_agent.py db-debugger --path .claude/agents --type editor
    init_agent.py my-agent --path .claude/agents --type basic
"""

import sys
from pathlib import Path
from typing import Union


BASIC_TEMPLATE = """---
name: {agent_name}
description: [TODO: When should Claude delegate to this agent? Be specific about the trigger condition and what problem it solves.]
tools: []
model: inherit
permissionMode: default
---

You are a specialized agent for [TODO: specific task].

Your purpose: [TODO: What specific task do you handle?]

When invoked:
1. [TODO: First step]
2. [TODO: Second step]
3. [TODO: Report results as...]

Constraints:
- [TODO: What are you focused on?]
- [TODO: What should you NOT do?]
"""

READ_ONLY_TEMPLATE = """---
name: {agent_name}
description: [TODO: When should Claude delegate to this agent for analysis/research? Include specific use cases.]
tools: [Read, Grep, Glob, Bash]
model: inherit
permissionMode: plan
---

You are a specialized analyst and researcher focused on [TODO: specific domain].

Your purpose: [TODO: What specific analysis or research do you perform?]

When invoked:
1. Identify files or patterns to search
2. Use Read for file content, Grep for patterns, Glob for discovery
3. Analyze findings systematically
4. Report results with specific file:line references

Output format:
- Start with summary of findings
- List specific locations: file:line - finding
- Include relevant code snippets for context
- End with recommendations

Constraints:
- Read-only: Do NOT modify files
- Do NOT execute arbitrary code beyond Bash for tooling
- Focus on [TODO: specific areas], ignore [TODO: what to exclude]
- Provide actionable findings
"""

EDITOR_TEMPLATE = """---
name: {agent_name}
description: [TODO: When should Claude delegate to this agent for editing? Include specific use cases like "after writing code" or "when tests fail".]
tools: [Read, Write, Edit, Bash, Grep, Glob]
model: inherit
permissionMode: acceptEdits
---

You are a specialized editor and fixer focused on [TODO: specific task type].

Your purpose: [TODO: What specific edits or fixes do you perform?]

When invoked:
1. Understand the task and scope
2. Read relevant files to understand context
3. Plan changes needed
4. Make targeted edits using Edit tool
5. Verify changes with Bash or Read
6. Report what was changed and why

Output format:
- Summarize changes made
- List modified files
- Explain reasoning for each change
- Report verification results

Constraints:
- Make focused, targeted changes only
- Do NOT make unnecessary modifications
- Do NOT change [TODO: specific restrictions]
- Preserve existing code style and patterns
- Run verification after changes
"""

RESTRICTED_TEMPLATE = """---
name: {agent_name}
description: [TODO: When should Claude delegate to this restricted agent? Include security or compliance context.]
tools: [Read, Grep, Bash]
disallowedTools: [Write, Edit]
model: inherit
permissionMode: dontAsk
hooks:
  PreToolUse: scripts/validate_tool_use.sh
---

You are a restricted agent for [TODO: specific task with security/compliance requirements].

Your purpose: [TODO: What task do you perform with these restrictions?]

Security model: [TODO: Why are these tools restricted? What compliance requirement?]

When invoked:
1. Verify you have necessary context
2. Use only approved tools (Read, Grep, Bash)
3. Do NOT attempt to use Write or Edit tools
4. Perform [TODO: specific actions]
5. Report findings

Constraints:
- Tool restrictions: Write and Edit are disabled
- Do NOT: [TODO: specific anti-patterns]
- Log all operations for audit trail
- [TODO: Other compliance requirements]
"""

CUSTOM_TEMPLATE = """---
name: {agent_name}
description: [TODO: Complete description of when/why Claude should delegate to this agent]
tools: [TODO: List tools agent can use, e.g., [Read, Grep, Bash]]
model: inherit
permissionMode: default
---

You are [TODO: Describe your role and specialization].

Your purpose: [TODO: What specific task do you handle?]

Capabilities: [TODO: What can you do?]

Constraints: [TODO: What should you NOT do?]

When invoked, your workflow is:
[TODO: Describe step-by-step workflow]
"""


def title_case_agent_name(agent_name: str) -> str:
    """Convert hyphenated agent name to Title Case for display."""
    return " ".join(word.capitalize() for word in agent_name.split("-"))


def get_template(template_type: str) -> str:
    """Get template content by type."""
    templates = {
        "basic": BASIC_TEMPLATE,
        "read-only": READ_ONLY_TEMPLATE,
        "editor": EDITOR_TEMPLATE,
        "restricted": RESTRICTED_TEMPLATE,
        "custom": CUSTOM_TEMPLATE,
    }

    if template_type not in templates:
        print(f"[ERROR] Unknown template type: {template_type}")
        print(f"[INFO] Available types: {', '.join(templates.keys())}")
        sys.exit(1)

    return templates[template_type]


def init_agent(
    agent_name: str, path: Union[str, Path], template_type: str = "basic"
) -> Union[Path, None]:
    """
    Initialize a new agent .md file from template.

    Args:
        agent_name: Name of the agent (hyphen-case)
        path: Directory where agent should be created
        template_type: Template type (basic, read-only, editor, restricted, custom)

    Returns:
        Path to created agent file, or None if error
    """
    # Determine agent file path
    output_path = Path(path).resolve()

    # Create output directory if needed
    output_path.mkdir(parents=True, exist_ok=True)

    agent_file = output_path / f"{agent_name}.md"

    # Check if file already exists
    if agent_file.exists():
        print(f"[ERROR] Agent file already exists: {agent_file}")
        return None

    # Get template content
    template = get_template(template_type)

    # Format template with agent name and title
    agent_title = title_case_agent_name(agent_name)
    agent_content = template.format(agent_name=agent_name, agent_title=agent_title)

    # Write agent file
    try:
        agent_file.write_text(agent_content, encoding='utf-8')
        print(f"[OK] Created agent: {agent_file}")
    except OSError as e:
        print(f"[ERROR] Error creating agent file: {e}")
        return None

    # Print next steps
    print(f"\n[OK] Agent '{agent_name}' initialized successfully")
    print(f"     Type: {template_type}")
    print(f"     Location: {agent_file}")
    print("\nNext steps:")
    print("1. Edit the agent .md file to complete TODO items")
    print("2. Update the description field with specific delegation trigger")
    print("3. Write the system prompt in the markdown body")
    print("4. Run validate_agent.py to check configuration")
    print("5. Place in .claude/agents/ and test")

    return agent_file


def main() -> None:
    """Parse command-line arguments and initialize a new agent."""
    if len(sys.argv) < 4 or sys.argv[2] != "--path":
        print("Usage: init_agent.py <agent-name> --path <path> [--type <type>]")
        print("\nAgent name requirements:")
        print("  - Hyphen-case identifier (e.g., 'code-reviewer')")
        print("  - Lowercase letters, digits, and hyphens only")
        print("  - Max 64 characters")
        print("\nTemplate types (--type, default: basic):")
        print("  - basic: Minimal agent with required fields only")
        print("  - read-only: For analyzers (Read, Grep, Glob, Bash)")
        print("  - editor: For editors (Read, Write, Edit, Bash)")
        print("  - restricted: With tool restrictions and hooks")
        print("  - custom: Interactive prompts for all fields")
        print("\nExamples:")
        print("  init_agent.py code-reviewer --path .claude/agents --type read-only")
        print("  init_agent.py db-debugger --path .claude/agents --type editor")
        print("  init_agent.py my-agent --path .claude/agents")
        sys.exit(1)

    agent_name = sys.argv[1]
    path = sys.argv[3]
    template_type = "basic"

    # Check for optional --type flag
    if len(sys.argv) >= 6 and sys.argv[4] == "--type":
        template_type = sys.argv[5]

    print(f">> Initializing agent: {agent_name}")
    print(f"   Location: {path}")
    print(f"   Template: {template_type}")
    print()

    result = init_agent(agent_name, path, template_type)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

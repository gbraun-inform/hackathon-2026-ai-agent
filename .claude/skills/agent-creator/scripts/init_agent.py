#!/usr/bin/env python3
"""
Agent Initializer - Creates a new Claude Code agent from template

Usage:
    init_agent.py <agent-name> --path <path>

Examples:
    init_agent.py security-auditor --path agents/
    init_agent.py code-reviewer --path agents/public
    init_agent.py data-analyzer --path /custom/location
"""

import sys
from pathlib import Path


AGENT_TEMPLATE = """#!/usr/bin/env python3
\"\"\"
Agent: {agent_name}

Purpose: [TODO: Clear one-sentence description of what this agent does]

Responsibilities:
  - [TODO: List key responsibilities]
  - [TODO: What does this agent produce?]
  - [TODO: When does it stop?]

Tools used: [TODO: List tools this agent uses]
\"\"\"

from typing import Dict, List, Any, Optional
import logging

# Configure logging for the agent
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class {AgentClass}:
    \"\"\"
    {agent_title} agent

    [TODO: Brief description of agent capabilities and behavior]
    \"\"\"

    def __init__(self, **config):
        \"\"\"Initialize the agent with configuration.

        Args:
            **config: Agent configuration parameters
        \"\"\"
        self.config = config
        self.state = {{}}
        logger.info(f"Initializing {{{agent_title}}} agent")

    def execute(self, task_input: Any) -> Dict[str, Any]:
        \"\"\"
        Execute the agent's main workflow.

        Args:
            task_input: Input data or task description

        Returns:
            Dictionary with results and status
        \"\"\"
        logger.info(f"Starting task execution: {{task_input}}")

        try:
            # TODO: Implement main workflow
            # Step 1: Analyze input
            # Step 2: Plan approach
            # Step 3: Execute main logic
            # Step 4: Validate results
            # Step 5: Return findings

            result = {{
                "status": "success",
                "message": "[TODO: Replace with actual result]",
                "data": None
            }}

            logger.info(f"Task completed successfully")
            return result

        except Exception as e:
            logger.error(f"Error during execution: {{str(e)}}", exc_info=True)
            return {{
                "status": "error",
                "message": str(e),
                "data": None
            }}

    def _step_one(self) -> Any:
        \"\"\"[TODO: Name and implement first workflow step]\"\"\"
        # TODO: Implement step logic
        pass

    def _step_two(self) -> Any:
        \"\"\"[TODO: Name and implement second workflow step]\"\"\"
        # TODO: Implement step logic
        pass

    def _validate_result(self, result: Any) -> bool:
        \"\"\"
        Validate that result meets quality criteria.

        Args:
            result: The result to validate

        Returns:
            True if valid, False otherwise
        \"\"\"
        # TODO: Implement validation logic
        return True


def main():
    \"\"\"Entry point for standalone agent execution.\"\"\"
    # TODO: Configure for command-line execution if needed
    agent = {AgentClass}()
    result = agent.execute(input("Enter task: "))
    print(result)


if __name__ == "__main__":
    main()
\"\"\"


AGENT_DOCS_TEMPLATE = \"\"\"---
name: {agent_name}
type: agent
description: [TODO: One-sentence description of what this agent does and when to use it. Be specific about the agent's purpose and outcomes.]
---

# {agent_title} Agent

## Overview

[TODO: 1-2 sentences explaining what this agent does and when to use it]

## Purpose and Scope

### What it does
- [TODO: Capability 1]
- [TODO: Capability 2]
- [TODO: Capability 3]

### What it doesn't do
- [TODO: Out of scope items]

## Input and Output

### Input
[TODO: Describe expected input format and requirements]

### Output
[TODO: Describe output format and structure]

## Agent Workflow

The agent executes the following workflow:

1. **Phase 1: Analysis** - [TODO: What does the agent analyze?]
2. **Phase 2: Planning** - [TODO: How does it plan its approach?]
3. **Phase 3: Execution** - [TODO: Main work steps]
4. **Phase 4: Validation** - [TODO: How are results validated?]
5. **Phase 5: Reporting** - [TODO: How are results presented?]

## Success Criteria

The agent considers its work complete when:

- [TODO: Criterion 1]
- [TODO: Criterion 2]
- [TODO: Criterion 3]

## Error Handling

The agent handles errors by:

- [TODO: Error scenario 1 - how it's handled]
- [TODO: Error scenario 2 - how it's handled]
- [TODO: Fallback behavior]

## Tools and Capabilities

The agent uses:

- [TODO: Tool/capability 1]
- [TODO: Tool/capability 2]
- [TODO: Tool/capability 3]

## Usage Example

```
# TODO: Provide example of how to use this agent
result = agent.execute({{
    # TODO: Example input
}})
```

## Configuration

[TODO: List configurable parameters, if any]

- `param_name`: Description of parameter

## Performance Notes

[TODO: Any performance considerations or limitations]

- Expected execution time: [TODO]
- Token usage: [TODO: Typical range]
- Scalability: [TODO: How does it handle large inputs?]
\"\"\"


EXAMPLE_TOOL = \"\"\"#!/usr/bin/env python3
\"\"\"
Example tool for {agent_name} agent

This is a helper module that provides utilities for the agent.
Replace with actual tool implementation or delete if not needed.

Example real tools from other agents:
- scanner.py - Scans for specific patterns or issues
- analyzer.py - Analyzes data or code
- reporter.py - Generates formatted reports
\"\"\"


def example_function():
    \"\"\"Example helper function.\"\"\"
    # TODO: Implement actual tool logic
    pass
\"\"\"


EXAMPLE_REFERENCE = \"\"\"# Reference Documentation for {agent_title}

This is placeholder reference documentation for the {agent_title} agent.

Replace with actual reference content or delete if not needed.

## When Reference Docs Are Useful

Reference docs are ideal for:
- Patterns and best practices specific to this agent
- Detailed technical information
- Schema documentation
- Error codes and troubleshooting
- Configuration options

## Example Sections

### Patterns and Best Practices
- How to structure input data
- Common workflow variations
- Performance optimization tips

### Technical Reference
- Algorithm details
- Tool specifications
- Data format specifications

### Troubleshooting
- Common errors and solutions
- Performance tuning
- Debug logging
\"\"\"


def title_case_name(name: str) -> str:
    \"\"\"Convert hyphenated name to Title Case.\"\"\"
    return ' '.join(word.capitalize() for word in name.split('-'))


def name_to_class(name: str) -> str:
    \"\"\"Convert hyphenated name to PascalCase for class names.\"\"\"
    return ''.join(word.capitalize() for word in name.split('-'))


def init_agent(agent_name: str, path: str) -> Optional[Path]:
    \"\"\"
    Initialize a new agent directory with template files.

    Args:
        agent_name: Name of the agent (hyphenated)
        path: Path where the agent directory should be created

    Returns:
        Path to created agent directory, or None if error
    \"\"\"
    # Determine agent directory path
    agent_dir = Path(path).resolve() / agent_name

    # Check if directory already exists
    if agent_dir.exists():
        print(f"❌ Error: Agent directory already exists: {agent_dir}")
        return None

    # Create agent directory
    try:
        agent_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Created agent directory: {agent_dir}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None

    agent_title = title_case_name(agent_name)
    agent_class = name_to_class(agent_name)

    # Create agent.py main file
    try:
        agent_code = AGENT_TEMPLATE.format(
            agent_name=agent_name,
            agent_title=agent_title,
            AgentClass=agent_class
        )
        agent_py = agent_dir / 'agent.py'
        agent_py.write_text(agent_code)
        agent_py.chmod(0o755)
        print("✅ Created agent.py")
    except Exception as e:
        print(f"❌ Error creating agent.py: {e}")
        return None

    # Create AGENT.md documentation
    try:
        agent_docs = AGENT_DOCS_TEMPLATE.format(
            agent_name=agent_name,
            agent_title=agent_title
        )
        agent_md = agent_dir / 'AGENT.md'
        agent_md.write_text(agent_docs)
        print("✅ Created AGENT.md")
    except Exception as e:
        print(f"❌ Error creating AGENT.md: {e}")
        return None

    # Create tools directory with example tool
    try:
        tools_dir = agent_dir / 'tools'
        tools_dir.mkdir(exist_ok=True)

        # Create __init__.py for Python package
        init_file = tools_dir / '__init__.py'
        init_file.write_text('\"\"\"Tools for {} agent\"\"\"\n'.format(agent_title))

        # Create example tool
        example_tool = tools_dir / 'example.py'
        tool_code = EXAMPLE_TOOL.format(agent_name=agent_name)
        example_tool.write_text(tool_code)
        example_tool.chmod(0o755)
        print("✅ Created tools/example.py")
    except Exception as e:
        print(f"❌ Error creating tools directory: {e}")
        return None

    # Create references directory with example reference doc
    try:
        references_dir = agent_dir / 'references'
        references_dir.mkdir(exist_ok=True)

        example_reference = references_dir / 'patterns.md'
        ref_content = EXAMPLE_REFERENCE.format(agent_title=agent_title)
        example_reference.write_text(ref_content)
        print("✅ Created references/patterns.md")
    except Exception as e:
        print(f"❌ Error creating references directory: {e}")
        return None

    # Print next steps
    print(f"\n✅ Agent '{agent_name}' initialized successfully at {agent_dir}")
    print("\nNext steps:")
    print("1. Edit agent.py to implement the agent's core logic")
    print("2. Update AGENT.md with complete documentation")
    print("3. Implement actual tools in tools/ directory")
    print("4. Customize or delete example files as needed")
    print("5. Test the agent thoroughly before deployment")

    return agent_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("Usage: init_agent.py <agent-name> --path <path>")
        print("\nAgent name requirements:")
        print("  - Hyphen-case identifier (e.g., 'code-reviewer')")
        print("  - Lowercase letters, digits, and hyphens only")
        print("  - Max 40 characters")
        print("\nExamples:")
        print("  init_agent.py security-auditor --path agents/")
        print("  init_agent.py code-reviewer --path agents/public")
        print("  init_agent.py data-analyzer --path /custom/location")
        sys.exit(1)

    agent_name = sys.argv[1]
    path = sys.argv[3]

    print(f"🚀 Initializing agent: {agent_name}")
    print(f"   Location: {path}")
    print()

    result = init_agent(agent_name, path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Agent validation script - validates agent configuration

Usage:
    validate_agent.py <path-to-agent.md>

Example:
    validate_agent.py .claude/agents/code-reviewer.md
"""

import re
import sys
from pathlib import Path
from typing import Any, cast

import yaml


# Valid tools that can be specified in agent configuration
VALID_TOOLS = {
    "Read",
    "Write",
    "Edit",
    "Bash",
    "Grep",
    "Glob",
    "WebFetch",
    "WebSearch",
    "Skill",
    "Task",
    "ExitPlanMode",
    "EnterPlanMode",
    "AskUserQuestion",
    "NotebookEdit",
    "mcp__ide__getDiagnostics",
    "mcp__ide__executeCode",
}

# Valid permission modes
VALID_PERMISSION_MODES = {
    "default",
    "acceptEdits",
    "dontAsk",
    "bypassPermissions",
    "plan",
}

# Valid models
VALID_MODELS = {
    "sonnet",
    "opus",
    "haiku",
    "inherit",
}

# Valid hook types
VALID_HOOK_TYPES = {
    "PreToolUse",
    "PostToolUse",
    "Stop",
}


def validate_agent(agent_path: str | Path) -> tuple[bool, list[str]]:
    """
    Validate an agent configuration.

    Returns:
        (is_valid, messages) where messages are warnings and errors
    """
    agent_path = Path(agent_path)
    messages: list[str] = []

    # Check file exists
    if not agent_path.exists():
        return False, [f"Agent file not found: {agent_path}"]

    if not agent_path.is_file():
        return False, [f"Not a file: {agent_path}"]

    if agent_path.suffix != ".md":
        messages.append(f"WARNING: Agent file should have .md extension, got {agent_path.suffix}")

    # Read and validate frontmatter
    content = agent_path.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return False, ["No YAML frontmatter found"]

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, ["Invalid frontmatter format"]

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, ["Frontmatter must be a YAML dictionary"]
        # Cast for type checker after runtime validation
        frontmatter = cast(dict[str, Any], frontmatter)
    except yaml.YAMLError as e:
        return False, [f"Invalid YAML in frontmatter: {e}"]

    # Define allowed properties
    allowed_properties = {
        "name",
        "description",
        "tools",
        "disallowedTools",
        "model",
        "permissionMode",
        "skills",
        "hooks",
    }

    # Check for unexpected properties
    unexpected_keys = set(frontmatter.keys()) - allowed_properties
    if unexpected_keys:
        return False, [
            f"Unexpected key(s) in frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(allowed_properties))}"
        ]

    # Validate required fields
    if 'name' not in frontmatter:
        return False, ["Missing required field: 'name'"]

    if 'description' not in frontmatter:
        return False, ["Missing required field: 'description'"]

    # Validate name
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, [f"'name' must be a string, got {type(name).__name__}"]

    name = name.strip()
    if not name:
        return False, ["'name' cannot be empty"]

    if not re.match(r"^[a-z0-9-]+$", name):
        return False, [
            f"Name '{name}' should be hyphen-case "
            "(lowercase letters, digits, and hyphens only)"
        ]

    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, [
            f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        ]

    if len(name) > 64:
        return False, [
            f"Name is too long ({len(name)} characters). Maximum is 64 characters."
        ]

    # Validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, [
            f"'description' must be a string, got {type(description).__name__}"
        ]

    description = description.strip()
    if not description:
        return False, ["'description' cannot be empty"]

    if "<" in description or ">" in description:
        return False, ["'description' cannot contain angle brackets (< or >)"]

    if len(description) < 10:
        messages.append(
            f"WARNING: 'description' is very short ({len(description)} chars). "
            "Consider being more specific about when/why to invoke this agent."
        )

    if len(description) > 1024:
        return False, [
            f"'description' is too long ({len(description)} characters). "
            "Maximum is 1024 characters."
        ]

    # Check for clear delegation trigger in description
    trigger_keywords = ["use", "when", "invoke", "delegate", "after", "if", "for"]
    if not any(keyword in description.lower() for keyword in trigger_keywords):
        messages.append(
            "WARNING: 'description' should include when/why Claude should delegate. "
            "Consider adding context like 'Use when...', 'Invoke after...', etc."
        )

    # Validate tools field (optional)
    if 'tools' in frontmatter:
        tools = frontmatter.get('tools')
        if tools is not None:
            if not isinstance(tools, list):
                return False, ["'tools' must be a list or null"]
            # Cast for type checker after runtime validation
            tools = cast(list[Any], tools)
            for tool in tools:
                if not isinstance(tool, str):
                    return False, [f"Tool names must be strings, got {type(tool).__name__}"]
                if tool not in VALID_TOOLS:
                    messages.append(f"WARNING: Unknown tool '{tool}'. Valid tools: {', '.join(sorted(VALID_TOOLS))}")

    # Validate disallowedTools field (optional)
    if 'disallowedTools' in frontmatter:
        disallowed = frontmatter.get('disallowedTools')
        if disallowed is not None:
            if not isinstance(disallowed, list):
                return False, ["'disallowedTools' must be a list or null"]
            # Cast for type checker after runtime validation
            disallowed = cast(list[Any], disallowed)
            for tool in disallowed:
                if not isinstance(tool, str):
                    return False, [f"Tool names must be strings, got {type(tool).__name__}"]
                if tool not in VALID_TOOLS:
                    messages.append(f"WARNING: Unknown tool '{tool}' in disallowedTools")

    # Check for both tools and disallowedTools
    if 'tools' in frontmatter and 'disallowedTools' in frontmatter:
        if frontmatter['tools'] and frontmatter['disallowedTools']:
            messages.append(
                "WARNING: Using both 'tools' and 'disallowedTools' may be confusing. "
                "Prefer using one or the other."
            )

    # Validate model field (optional)
    if 'model' in frontmatter:
        model = frontmatter.get('model')
        if model is not None:
            if not isinstance(model, str):
                return False, [f"'model' must be a string, got {type(model).__name__}"]
            if model not in VALID_MODELS:
                return False, [
                    f"Invalid model '{model}'. Valid models: {', '.join(VALID_MODELS)}"
                ]

    # Validate permissionMode field (optional)
    if 'permissionMode' in frontmatter:
        mode = frontmatter.get('permissionMode')
        if mode is not None:
            if not isinstance(mode, str):
                return False, [f"'permissionMode' must be a string, got {type(mode).__name__}"]
            if mode not in VALID_PERMISSION_MODES:
                return False, [
                    f"Invalid permissionMode '{mode}'. Valid modes: {', '.join(VALID_PERMISSION_MODES)}"
                ]
            if mode == "bypassPermissions":
                messages.append(
                    "SECURITY WARNING: permissionMode 'bypassPermissions' bypasses all permission checks. "
                    "Use only in restricted/trusted environments."
                )

    # Validate skills field (optional)
    if 'skills' in frontmatter:
        skills = frontmatter.get('skills')
        if skills is not None:
            if not isinstance(skills, list):
                return False, ["'skills' must be a list or null"]
            # Cast for type checker after runtime validation
            skills = cast(list[Any], skills)
            for skill in skills:
                if not isinstance(skill, str):
                    return False, [f"Skill names must be strings, got {type(skill).__name__}"]
                if not re.match(r"^[a-z0-9-]+$", skill):
                    messages.append(f"WARNING: Skill name '{skill}' should be hyphen-case")

    # Validate hooks field (optional, advanced)
    if 'hooks' in frontmatter:
        hooks = frontmatter.get('hooks')
        if hooks is not None:
            if not isinstance(hooks, dict):
                return False, ["'hooks' must be a dictionary or null"]
            # Cast for type checker after runtime validation
            hooks = cast(dict[str, Any], hooks)
            for hook_type in hooks.keys():
                if hook_type not in VALID_HOOK_TYPES:
                    messages.append(
                        f"WARNING: Unknown hook type '{hook_type}'. Valid types: {', '.join(VALID_HOOK_TYPES)}"
                    )

    # Check if body exists and has content
    body_start = len("---\n" + frontmatter_text + "\n---\n")
    body = content[body_start:].strip()

    if not body:
        messages.append("WARNING: Agent has no system prompt in body. Add instructions after frontmatter.")

    if len(body) > 5000:
        messages.append(
            f"WARNING: Agent system prompt is very long ({len(body)} chars). "
            "Consider if this agent has too much responsibility."
        )

    return len([m for m in messages if m.startswith("ERROR")]) == 0, messages


def main() -> None:
    """Validate agent file."""
    if len(sys.argv) != 2:
        print("Usage: validate_agent.py <path-to-agent.md>")
        print("Example: validate_agent.py .claude/agents/code-reviewer.md")
        sys.exit(1)

    agent_path = sys.argv[1]

    valid, messages = validate_agent(agent_path)

    # Separate errors and warnings
    errors = [m for m in messages if m.startswith("ERROR") or m.startswith("SECURITY")]
    warnings = [m for m in messages if m.startswith("WARNING")]

    # Print errors
    for error in errors:
        print(f"❌ {error}")

    # Print warnings
    for warning in warnings:
        print(f"⚠️  {warning}")

    # Print summary
    if not messages:
        print("✅ Agent is valid!")
    elif not valid:
        print(f"\n❌ Agent validation FAILED ({len(errors)} error(s))")
        sys.exit(1)
    else:
        print(f"\n✅ Agent is valid with {len(warnings)} warning(s)")

    sys.exit(0)


if __name__ == "__main__":
    main()

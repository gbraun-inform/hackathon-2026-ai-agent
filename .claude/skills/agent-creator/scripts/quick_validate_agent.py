#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick validation script for agents - minimal version

Validates agent structure and required files before packaging.

Usage:
    python quick_validate_agent.py <agent_directory>

Example:
    python quick_validate_agent.py agents/my-agent
"""

import sys
import io
import os
import re
import yaml
from pathlib import Path

# Force UTF-8 output encoding on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def validate_agent(agent_path):
    """Basic validation of an agent directory structure.

    Args:
        agent_path: Path to the agent directory

    Returns:
        Tuple of (valid: bool, message: str)
    """
    agent_path = Path(agent_path)

    # Check agent directory exists
    if not agent_path.exists():
        return False, f"Agent directory not found: {agent_path}"

    if not agent_path.is_dir():
        return False, f"Path is not a directory: {agent_path}"

    # Check AGENT.md exists
    agent_md = agent_path / 'AGENT.md'
    if not agent_md.exists():
        return False, "AGENT.md not found in agent directory"

    # Read and validate AGENT.md frontmatter
    try:
        content = agent_md.read_text(encoding='utf-8')
    except Exception as e:
        return False, f"Failed to read AGENT.md: {e}"

    if not content.startswith('---'):
        return False, "AGENT.md: No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "AGENT.md: Invalid frontmatter format (must start and end with ---)"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "AGENT.md: Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, f"AGENT.md: Invalid YAML in frontmatter: {e}"

    # Check required fields
    if 'name' not in frontmatter:
        return False, "AGENT.md: Missing 'name' in frontmatter"
    if 'type' not in frontmatter:
        return False, "AGENT.md: Missing 'type' in frontmatter (should be 'agent')"
    if 'description' not in frontmatter:
        return False, "AGENT.md: Missing 'description' in frontmatter"

    # Validate name
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"AGENT.md: name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        # Check naming convention (hyphen-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"AGENT.md: name '{name}' should be hyphen-case (lowercase letters, digits, hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"AGENT.md: name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        if len(name) > 64:
            return False, f"AGENT.md: name is too long ({len(name)} characters). Maximum is 64 characters."

    # Validate type
    agent_type = frontmatter.get('type', '')
    if agent_type != 'agent':
        return False, f"AGENT.md: type must be 'agent', got '{agent_type}'"

    # Validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"AGENT.md: description must be a string, got {type(description).__name__}"
    description = description.strip()
    if not description:
        return False, "AGENT.md: description cannot be empty"
    if '<' in description or '>' in description:
        return False, "AGENT.md: description cannot contain angle brackets (< or >)"
    if len(description) > 1024:
        return False, f"AGENT.md: description is too long ({len(description)} characters). Maximum is 1024 characters."

    # Check for required files/directories
    agent_py = agent_path / 'agent.py'
    if not agent_py.exists():
        return False, "agent.py not found (main agent implementation file)"

    # Validate agent.py is readable
    try:
        agent_py.read_text(encoding='utf-8')
    except Exception as e:
        return False, f"Failed to read agent.py: {e}"

    # Check tools directory structure
    tools_dir = agent_path / 'tools'
    if tools_dir.exists():
        if not tools_dir.is_dir():
            return False, "tools/ must be a directory"

        # Check for __init__.py
        init_file = tools_dir / '__init__.py'
        if not init_file.exists():
            return False, "tools/__init__.py not found (required for Python package)"

    # Check references directory if it exists
    references_dir = agent_path / 'references'
    if references_dir.exists():
        if not references_dir.is_dir():
            return False, "references/ must be a directory"

        # All files in references should be markdown or other docs
        for ref_file in references_dir.iterdir():
            if ref_file.is_file() and ref_file.name.startswith('.'):
                continue  # Skip hidden files

    # Optional: Check for common patterns
    body_content = content.split('---', 2)[-1].strip() if '---' in content else content
    if len(body_content) < 100:
        return False, "AGENT.md: Body content seems too short (should have meaningful documentation)"

    return True, "Agent structure is valid!"


def main():
    if len(sys.argv) != 2:
        print("Usage: python quick_validate_agent.py <agent_directory>")
        sys.exit(1)

    agent_path = sys.argv[1]
    valid, message = validate_agent(agent_path)
    print(message)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()

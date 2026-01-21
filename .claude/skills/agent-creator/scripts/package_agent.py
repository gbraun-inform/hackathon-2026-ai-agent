#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Packager - Creates a distributable agent package

Usage:
    python package_agent.py <path/to/agent-folder> [output-directory]

Example:
    python package_agent.py agents/my-agent
    python package_agent.py agents/my-agent ./dist
"""

import sys
import io
import zipfile
from pathlib import Path
from quick_validate_agent import validate_agent

# Force UTF-8 output encoding on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def package_agent(agent_path, output_dir=None):
    """
    Package an agent folder into a distributable archive.

    Args:
        agent_path: Path to the agent folder
        output_dir: Optional output directory for the archive (defaults to current directory)

    Returns:
        Path to the created archive, or None if error
    """
    agent_path = Path(agent_path).resolve()

    # Validate agent folder exists
    if not agent_path.exists():
        print(f"Error: Agent folder not found: {agent_path}")
        return None

    if not agent_path.is_dir():
        print(f"Error: Path is not a directory: {agent_path}")
        return None

    # Run validation before packaging
    print("Validating agent...")
    valid, message = validate_agent(agent_path)
    if not valid:
        print(f"Validation failed: {message}")
        print("   Please fix the validation errors before packaging.")
        return None
    print(f"{message}\n")

    # Determine output location
    agent_name = agent_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    agent_filename = output_path / f"{agent_name}.agent"

    # Create the .agent file (zip format)
    try:
        with zipfile.ZipFile(agent_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the agent directory
            for file_path in agent_path.rglob('*'):
                if file_path.is_file():
                    # Calculate the relative path within the zip
                    arcname = file_path.relative_to(agent_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  Added: {arcname}")

        print(f"\nSuccessfully packaged agent to: {agent_filename}")
        print(f"File size: {agent_filename.stat().st_size} bytes")
        return agent_filename

    except Exception as e:
        print(f"Error creating agent package: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python package_agent.py <path/to/agent-folder> [output-directory]")
        print("\nExample:")
        print("  python package_agent.py agents/my-agent")
        print("  python package_agent.py agents/my-agent ./dist")
        sys.exit(1)

    agent_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Packaging agent: {agent_path}")
    if output_dir:
        print(f"   Output directory: {output_dir}")
    print()

    result = package_agent(agent_path, output_dir)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

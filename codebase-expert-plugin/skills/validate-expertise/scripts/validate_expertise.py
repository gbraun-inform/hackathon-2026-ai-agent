#!/usr/bin/env python3
"""
Validates expertise YAML files for the expert agent system.

Usage:
    python validate_expertise.py <path-to-expertise-yaml>

Exit codes:
    0 - Validation passed
    1 - Validation failed
"""

import sys
import yaml
from pathlib import Path


def validate_expertise(file_path: str) -> tuple[bool, list[str]]:
    """
    Validates an expertise YAML file.

    Args:
        file_path: Path to the expertise YAML file

    Returns:
        Tuple of (is_valid, list of errors/warnings)
    """
    errors = []
    warnings = []

    # Check if file exists
    path = Path(file_path)
    if not path.exists():
        errors.append(f"File not found: {file_path}")
        return False, errors

    # Read and parse YAML
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        errors.append(f"YAML parsing error: {e}")
        return False, errors
    except Exception as e:
        errors.append(f"Error reading file: {e}")
        return False, errors

    # Check if data is a dictionary
    if not isinstance(data, dict):
        errors.append("YAML file must contain a dictionary at the root level")
        return False, errors

    # MANDATORY: Check for description field
    if 'description' not in data:
        errors.append("Missing required field: 'description'")
    elif not data['description']:
        errors.append("Field 'description' cannot be empty")
    elif not isinstance(data['description'], str):
        errors.append("Field 'description' must be a string")
    else:
        desc = data['description'].strip()
        desc_len = len(desc)

        if desc_len < 20:
            warnings.append(f"Description is quite short ({desc_len} chars). Consider adding more context (recommended: 20-500 chars)")
        elif desc_len > 500:
            warnings.append(f"Description is quite long ({desc_len} chars). Consider keeping it concise (recommended: 20-500 chars)")

    # Check for recommended fields (warnings only)
    recommended_fields = ['category', 'concepts', 'details']
    missing_recommended = [field for field in recommended_fields if field not in data]

    if missing_recommended:
        warnings.append(f"Missing recommended fields: {', '.join(missing_recommended)}")

    # Validate related_files if present
    if 'related_files' in data:
        if not isinstance(data['related_files'], list):
            warnings.append("Field 'related_files' should be a list")

    # Validate concepts if present
    if 'concepts' in data:
        if not isinstance(data['concepts'], list):
            warnings.append("Field 'concepts' should be a list")

    # Validate category if present
    if 'category' in data:
        if not isinstance(data['category'], str):
            warnings.append("Field 'category' should be a string")

    # Print results
    is_valid = len(errors) == 0
    return is_valid, errors + warnings


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_expertise.py <path-to-expertise-yaml>")
        sys.exit(1)

    file_path = sys.argv[1]

    print(f"Validating: {file_path}")
    print("-" * 60)

    is_valid, messages = validate_expertise(file_path)

    if not messages:
        print("[PASS] Validation passed - no issues found")
        sys.exit(0)

    # Print errors and warnings
    has_errors = False
    for msg in messages:
        if msg.startswith("Missing required") or msg.startswith("YAML parsing") or msg.startswith("Field 'description'") or "not found" in msg or "must contain" in msg:
            print(f"[ERROR] {msg}")
            has_errors = True
        else:
            print(f"[WARNING] {msg}")

    print("-" * 60)

    if is_valid:
        print("[PASS] Validation passed (with warnings)")
        sys.exit(0)
    else:
        print("[FAIL] Validation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

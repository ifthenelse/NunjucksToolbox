#!/usr/bin/env python3
"""
JSON file validator for Nunjucks Toolbox.
Validates all JSON configuration files for syntax and structure.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def validate_json_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate a single JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, f"Valid JSON: {file_path}"
    except json.JSONDecodeError as e:
        return False, f"JSON syntax error in {file_path}: {e}"
    except Exception as e:
        return False, f"Error reading {file_path}: {e}"


def validate_completions_structure(file_path: str) -> Tuple[bool, str]:
    """Validate Sublime Text completions file structure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check required structure for completions
        if not isinstance(data, dict):
            return False, "Completions file must be a JSON object"
        
        if 'scope' not in data:
            return False, "Missing 'scope' field in completions"
        
        if 'completions' not in data:
            return False, "Missing 'completions' array"
        
        if not isinstance(data['completions'], list):
            return False, "'completions' must be an array"
        
        # Validate individual completions
        for i, completion in enumerate(data['completions']):
            if isinstance(completion, str):
                continue  # Simple string completion is valid
            elif isinstance(completion, dict):
                if 'trigger' not in completion:
                    return False, f"Completion {i}: missing 'trigger' field"
                if 'contents' not in completion:
                    return False, f"Completion {i}: missing 'contents' field"
            else:
                return False, f"Completion {i}: invalid type, must be string or object"
        
        return True, f"Completions structure valid ({len(data['completions'])} completions)"
        
    except Exception as e:
        return False, f"Error validating completions structure: {e}"


def validate_snippets_structure(file_path: str) -> Tuple[bool, str]:
    """Validate Sublime Text snippets file structure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check required structure for snippets
        if not isinstance(data, dict):
            return False, "Snippets file must be a JSON object"
        
        if 'scope' not in data:
            return False, "Missing 'scope' field in snippets"
        
        if 'snippets' not in data:
            return False, "Missing 'snippets' array"
        
        if not isinstance(data['snippets'], list):
            return False, "'snippets' must be an array"
        
        # Validate individual snippets
        for i, snippet in enumerate(data['snippets']):
            if not isinstance(snippet, dict):
                return False, f"Snippet {i}: must be an object"
            
            required_fields = ['trigger', 'contents']
            for field in required_fields:
                if field not in snippet:
                    return False, f"Snippet {i}: missing '{field}' field"
        
        return True, f"Snippets structure valid ({len(data['snippets'])} snippets)"
        
    except Exception as e:
        return False, f"Error validating snippets structure: {e}"


def validate_package_json(file_path: str) -> Tuple[bool, str]:
    """Validate package.json structure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check required fields
        required_fields = ['name', 'version', 'description']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return False, f"Missing required fields: {missing_fields}"
        
        # Validate field types
        if not isinstance(data['name'], str):
            return False, "'name' must be a string"
        
        if not isinstance(data['version'], str):
            return False, "'version' must be a string"
        
        if not isinstance(data['description'], str):
            return False, "'description' must be a string"
        
        return True, f"Package.json valid (name: {data['name']}, version: {data['version']})"
        
    except Exception as e:
        return False, f"Error validating package.json: {e}"


def validate_messages_json(file_path: str) -> Tuple[bool, str]:
    """Validate messages.json structure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, dict):
            return False, "Messages file must be a JSON object"
        
        # Validate that all values are strings (message paths)
        for key, value in data.items():
            if not isinstance(value, str):
                return False, f"Message entry '{key}' must be a string"
        
        return True, f"Messages.json valid ({len(data)} message entries)"
        
    except Exception as e:
        return False, f"Error validating messages.json: {e}"


def validate_all_json_files(project_root: str = ".") -> bool:
    """
    Validate all JSON files in the project.
    
    Args:
        project_root: Root directory of the project
        
    Returns:
        True if all files are valid, False otherwise
    """
    print("🔍 Validating JSON files...")
    
    # Define files to validate with their specific validators
    files_to_validate = {
        'Completions/NunjucksToolbox.sublime-completions': validate_completions_structure,
        'Snippets/NunjucksToolbox.sublime-snippets': validate_snippets_structure,
        'package.json': validate_package_json,
        'messages.json': validate_messages_json
    }
    
    all_valid = True
    results = []
    
    for relative_path, validator in files_to_validate.items():
        full_path = os.path.join(project_root, relative_path)
        
        # First check if it's valid JSON
        json_valid, json_message = validate_json_file(full_path)
        
        if json_valid:
            # Then check structure if file exists
            structure_valid, structure_message = validator(full_path)
            
            if structure_valid:
                print(f"✅ {relative_path}: {structure_message}")
                results.append(f"✅ {relative_path}")
            else:
                print(f"❌ {relative_path}: {structure_message}")
                results.append(f"❌ {relative_path}: {structure_message}")
                all_valid = False
        else:
            if "File not found" in json_message:
                print(f"⚠️  {relative_path}: File not found (optional)")
                results.append(f"⚠️  {relative_path}: Not found")
            else:
                print(f"❌ {relative_path}: {json_message}")
                results.append(f"❌ {relative_path}: {json_message}")
                all_valid = False
    
    return all_valid, results


def generate_json_validation_report(project_root: str = ".") -> None:
    """Generate a JSON validation report."""
    print("\n📄 Generating JSON validation report...")
    
    all_valid, results = validate_all_json_files(project_root)
    
    report_content = f"""# JSON Validation Report

## Summary
- **Status**: {'✅ All files valid' if all_valid else '❌ Some files have issues'}
- **Files checked**: {len(results)}

## Validation Results

"""
    
    for result in results:
        report_content += f"- {result}\n"
    
    report_content += f"""
## File Structure Requirements

### Completions File
- Must have 'scope' field
- Must have 'completions' array
- Each completion must have 'trigger' and 'contents'

### Snippets File  
- Must have 'scope' field
- Must have 'snippets' array
- Each snippet must have 'trigger' and 'contents'

### Package.json
- Must have 'name', 'version', 'description' fields
- All required fields must be strings

### Messages.json
- Must be a JSON object
- All values must be strings (file paths)

---
*Generated automatically by JSON validation script*
"""
    
    report_path = os.path.join(project_root, "json-validation-report.md")
    
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"✅ Report saved to: {report_path}")
    except Exception as e:
        print(f"❌ Failed to save report: {e}")


if __name__ == "__main__":
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    
    print("🔧 Starting JSON validation...")
    
    # Validate all files
    all_valid, _ = validate_all_json_files(project_root)
    
    # Generate report
    generate_json_validation_report(project_root)
    
    # Exit with appropriate code
    if all_valid:
        print("\n🎉 All JSON files are valid!")
        sys.exit(0)
    else:
        print("\n💥 Some JSON files have validation errors!")
        sys.exit(1)

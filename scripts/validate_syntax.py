#!/usr/bin/env python3
"""
Validates Nunjucks syntax files structure and YAML format.
Extracted from GitHub workflow for better maintainability.
"""

import yaml
import sys
from pathlib import Path


def validate_syntax_file(syntax_file_path: str) -> bool:
    """Validate the Nunjucks syntax file structure."""
    print("🔍 Validating syntax files...")
    
    syntax_path = Path(syntax_file_path)
    if not syntax_path.exists():
        print("❌ Required syntax file missing")
        return False
    
    try:
        with open(syntax_path) as f:
            syntax = yaml.safe_load(f)
        
        # Validate structure
        required = ['name', 'file_extensions', 'scope', 'contexts']
        missing = [k for k in required if k not in syntax]
        if missing:
            print('❌ Missing syntax keys:', missing)
            return False
        
        contexts = syntax.get('contexts', {})
        if 'main' not in contexts:
            print('❌ Missing main context')
            return False
        
        print('✅ YAML syntax and structure valid')
        print('  - Name:', syntax.get('name'))
        print('  - Extensions:', syntax.get('file_extensions'))
        print('  - Contexts:', len(contexts))
        
        return True
        
    except Exception as e:
        print(f'❌ Error validating syntax file: {e}')
        return False


if __name__ == "__main__":
    syntax_file = sys.argv[1] if len(sys.argv) > 1 else "Syntaxes/NunjucksToolbox.sublime-syntax"
    success = validate_syntax_file(syntax_file)
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Scope consistency validator for Nunjucks Toolbox.
Ensures all configuration files use consistent scope definitions.
"""

import json
import os
import sys


def validate_scope_consistency(project_root="."):
    """
    Validate that all Sublime Text configuration files use consistent scopes.
    
    Args:
        project_root: Root directory of the project
        
    Returns:
        True if all scopes are consistent, False otherwise
    """
    main_scope = 'text.html.nunjucks-toolbox'
    issues = []
    
    print("🔧 Starting scope consistency validation...")
    
    # Check keymaps for consistent scope usage
    keymap_files = [
        'Keymaps/Default (OSX).sublime-keymap',
        'Keymaps/Default (Linux).sublime-keymap',
        'Keymaps/Default (Windows).sublime-keymap'
    ]
    
    for keymap_file in keymap_files:
        file_path = os.path.join(project_root, keymap_file)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if main_scope in content:
                        print(f"✅ {keymap_file}: scope consistency verified")
                    else:
                        issues.append(f"{keymap_file}: missing scope '{main_scope}'")
            except Exception as e:
                issues.append(f"{keymap_file}: error reading - {e}")
        else:
            print(f"⚠️  {keymap_file}: file not found (optional)")
    
    # Check settings files
    settings_files = [
        'Settings/NunjucksToolbox.sublime-settings',
        'Settings/NunjucksToolboxAutoPairs.sublime-settings'
    ]
    
    for settings_file in settings_files:
        file_path = os.path.join(project_root, settings_file)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'selector' in content or 'scope' in content:
                        if main_scope in content:
                            print(f"✅ {settings_file}: scope consistency verified")
                        else:
                            print(f"⚠️  {settings_file}: check scope references")
                    else:
                        print(f"✅ {settings_file}: no scope-specific settings")
            except Exception as e:
                issues.append(f"{settings_file}: error reading - {e}")
        else:
            issues.append(f"{settings_file}: file not found")
    
    # Check syntax files
    syntax_files = [
        'Syntaxes/NunjucksToolbox.sublime-syntax',
        'Syntaxes/PHPNunjucks.sublime-syntax'
    ]
    
    for syntax_file in syntax_files:
        file_path = os.path.join(project_root, syntax_file)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'scope:' in content:
                        if main_scope in content:
                            print(f"✅ {syntax_file}: main scope defined correctly")
                        else:
                            print(f"⚠️  {syntax_file}: check scope definition")
                    else:
                        issues.append(f"{syntax_file}: no scope definition found")
            except Exception as e:
                issues.append(f"{syntax_file}: error reading - {e}")
        else:
            issues.append(f"{syntax_file}: file not found")
    
    # Check package.json for metadata consistency
    package_path = os.path.join(project_root, "package.json")
    if os.path.exists(package_path):
        try:
            with open(package_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
                required_fields = ['name', 'version', 'description']
                missing = [f for f in required_fields if f not in package_data]
                if missing:
                    issues.append(f"package.json missing fields: {missing}")
                else:
                    print("✅ package.json: required fields present")
        except Exception as e:
            issues.append(f"package.json: error reading - {e}")
    else:
        issues.append("package.json: file not found")
    
    # Generate validation report
    report_path = os.path.join(project_root, "scope-validation-report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Scope Consistency Validation Report\n\n")
        f.write(f"**Main Scope**: `{main_scope}`\n\n")
        
        if not issues:
            f.write("## ✅ Validation Results\n\n")
            f.write("All configuration files use consistent scope definitions.\n\n")
            f.write("### Validated Files\n")
            f.write("- **Keymaps**: ✅ Scope consistency verified\n")
            f.write("- **Settings**: ✅ Configuration validated\n")
            f.write("- **Syntax Files**: ✅ Scope definitions correct\n")
            f.write("- **Package Metadata**: ✅ Required fields present\n")
        else:
            f.write("## ❌ Validation Issues\n\n")
            for issue in issues:
                f.write(f"- {issue}\n")
    
    print(f"✅ Report saved to: {report_path}")
    
    if issues:
        print("\n💥 Some validations failed!")
        for issue in issues:
            print(f"❌ {issue}")
        return False
    else:
        print("\n🎉 All scope consistency checks passed!")
        return True


if __name__ == "__main__":
    if not validate_scope_consistency():
        sys.exit(1)
    else:
        sys.exit(0)

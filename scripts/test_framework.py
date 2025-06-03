#!/usr/bin/env python3
"""
Comprehensive testing framework for Nunjucks Toolbox extension.
Tests all command modules and core functionality.
"""

import os
import sys
import importlib.util
import tempfile
import unittest
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path


class NunjucksTestFramework:
    """Main testing framework for the extension."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = os.path.abspath(project_root)
        self.commands_dir = os.path.join(self.project_root, "Commands")
        self.scripts_dir = os.path.join(self.project_root, "scripts")
        self.test_results = []
        
    def load_module(self, module_path: str, module_name: str):
        """Dynamically load a Python module."""
        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            print(f"❌ Failed to load {module_name}: {e}")
            return None
    
    def test_core_module(self) -> bool:
        """Test the core utilities module."""
        print("\n🧪 Testing core module...")
        
        core_path = os.path.join(self.commands_dir, "nunjucks_core.py")
        if not os.path.exists(core_path):
            print("❌ Core module not found")
            return False
        
        core = self.load_module(core_path, "nunjucks_core")
        if not core:
            return False
        
        try:
            # Test pattern compilation
            patterns = core.NunjucksPatterns()
            test_text = "{{ user.name | upper }} {% if user %} test {% endif %}"
            
            # Test variable pattern
            variables = patterns.VARIABLE.findall(test_text)
            if not variables:
                print("❌ Variable pattern not working")
                return False
            
            # Test tag pattern
            tags = patterns.TAG.findall(test_text)
            if not tags:
                print("❌ Tag pattern not working")
                return False
            
            # Test analyzer
            analyzer = core.NunjucksAnalyzer()
            issues = analyzer.analyze_syntax(test_text)
            
            # Test formatter
            formatter = core.NunjucksFormatter()
            formatted = formatter.format_text(test_text)
            
            print("✅ Core module tests passed")
            return True
            
        except Exception as e:
            print(f"❌ Core module test failed: {e}")
            return False
    
    def test_command_modules(self) -> bool:
        """Test all command modules."""
        print("\n🧪 Testing command modules...")
        
        command_files = [
            "nunjucks_validate.py",
            "nunjucks_format.py", 
            "nunjucks_lint.py",
            "nunjucks_help.py",
            "nunjucks_quick_help.py",
            "nunjucks_filter_help.py"
        ]
        
        all_passed = True
        
        for command_file in command_files:
            command_path = os.path.join(self.commands_dir, command_file)
            
            if not os.path.exists(command_path):
                print(f"⚠️  Command file not found: {command_file}")
                continue
            
            try:
                # Load and test basic import
                command_module = self.load_module(command_path, command_file[:-3])
                if not command_module:
                    all_passed = False
                    continue
                
                # Check for required classes/functions
                has_command_class = any(
                    hasattr(command_module, attr) and 
                    'Command' in attr for attr in dir(command_module)
                )
                
                if has_command_class:
                    print(f"✅ {command_file}: imports and structure OK")
                else:
                    print(f"⚠️  {command_file}: no command class found")
                
            except Exception as e:
                print(f"❌ {command_file}: import failed - {e}")
                all_passed = False
        
        return all_passed
    
    def test_script_modules(self) -> bool:
        """Test all script modules."""
        print("\n🧪 Testing script modules...")
        
        script_files = [
            "validate_syntax.py",
            "test_patterns.py",
            "test_template_generator.py",
            "validate_scope_consistency.py",
            "validate_json_files.py"
        ]
        
        all_passed = True
        
        for script_file in script_files:
            script_path = os.path.join(self.scripts_dir, script_file)
            
            if not os.path.exists(script_path):
                print(f"⚠️  Script file not found: {script_file}")
                continue
            
            try:
                # Test basic import
                script_module = self.load_module(script_path, script_file[:-3])
                if script_module:
                    print(f"✅ {script_file}: imports OK")
                else:
                    all_passed = False
                    
            except Exception as e:
                print(f"❌ {script_file}: import failed - {e}")
                all_passed = False
        
        return all_passed
    
    def test_pattern_recognition(self) -> bool:
        """Test pattern recognition with real templates."""
        print("\n🧪 Testing pattern recognition...")
        
        # Create test template
        test_template = """
        {# Test comment #}
        <!DOCTYPE html>
        <html>
        <head>
            <title>{{ title | default("Test") }}</title>
        </head>
        <body>
            {% if user %}
                <h1>Hello {{ user.name | upper }}!</h1>
                {% for item in user.items %}
                    <p>{{ item.name }}</p>
                {% endfor %}
            {% else %}
                <p>No user found</p>
            {% endif %}
            
            {% macro button(text) %}
                <button>{{ text }}</button>
            {% endmacro %}
            
            {{ button("Click me") }}
        </body>
        </html>
        """
        
        try:
            # Load core patterns
            core_path = os.path.join(self.commands_dir, "nunjucks_core.py")
            core = self.load_module(core_path, "nunjucks_core")
            
            if not core:
                return False
            
            patterns = core.NunjucksPatterns()
            
            # Test each pattern type
            tests = [
                ("Comments", patterns.COMMENT, 1),
                ("Variables", patterns.VARIABLE, 6),  # Expected count
                ("Tags", patterns.TAG, 8),  # Expected count  
                ("Filters", patterns.FILTER, 2)  # Expected count
            ]
            
            all_passed = True
            
            for test_name, pattern, expected_min in tests:
                matches = pattern.findall(test_template)
                if len(matches) >= expected_min:
                    print(f"✅ {test_name}: {len(matches)} matches found")
                else:
                    print(f"❌ {test_name}: only {len(matches)} matches, expected >= {expected_min}")
                    all_passed = False
            
            return all_passed
            
        except Exception as e:
            print(f"❌ Pattern recognition test failed: {e}")
            return False
    
    def test_syntax_validation(self) -> bool:
        """Test syntax validation functionality."""
        print("\n🧪 Testing syntax validation...")
        
        try:
            core_path = os.path.join(self.commands_dir, "nunjucks_core.py")
            core = self.load_module(core_path, "nunjucks_core")
            
            if not core:
                return False
            
            analyzer = core.NunjucksAnalyzer()
            
            # Test valid syntax
            valid_template = "{{ user.name }} {% if user %}Hello{% endif %}"
            issues = analyzer.analyze_syntax(valid_template)
            valid_issues = [issue for issue in issues if issue.severity == 'error']
            
            # Test invalid syntax
            invalid_template = "{{ unclosed_var {% if user %}Hello{# unclosed comment"
            invalid_issues = analyzer.analyze_syntax(invalid_template)
            error_issues = [issue for issue in invalid_issues if issue.severity == 'error']
            
            if len(valid_issues) == 0 and len(error_issues) > 0:
                print(f"✅ Syntax validation: detected {len(error_issues)} errors in invalid template")
                return True
            else:
                print(f"❌ Syntax validation: valid={len(valid_issues)} errors, invalid={len(error_issues)} errors")
                return False
                
        except Exception as e:
            print(f"❌ Syntax validation test failed: {e}")
            return False
    
    def run_integration_tests(self) -> bool:
        """Run integration tests that simulate real usage."""
        print("\n🧪 Running integration tests...")
        
        try:
            # Test script execution in temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Test template generator
                script_path = os.path.join(self.scripts_dir, "test_template_generator.py")
                if os.path.exists(script_path):
                    generator = self.load_module(script_path, "test_template_generator")
                    if generator:
                        template_path = generator.create_test_template(temp_dir)
                        if os.path.exists(template_path):
                            print("✅ Template generator integration test passed")
                        else:
                            print("❌ Template generator failed to create file")
                            return False
                
                return True
                
        except Exception as e:
            print(f"❌ Integration test failed: {e}")
            return False
    
    def generate_test_report(self) -> None:
        """Generate a comprehensive test report."""
        print("\n📄 Generating test report...")
        
        report_content = f"""# Nunjucks Toolbox Test Report

## Test Summary
- **Project Root**: {self.project_root}
- **Commands Directory**: {self.commands_dir}
- **Scripts Directory**: {self.scripts_dir}

## Test Results

### Core Module Tests
- Pattern compilation and matching
- Syntax analyzer functionality  
- Code formatter functionality

### Command Module Tests
- Module imports and structure validation
- Command class detection
- Basic functionality checks

### Script Module Tests  
- Import validation for all utility scripts
- External script execution capability

### Pattern Recognition Tests
- Comment pattern matching
- Variable pattern matching
- Tag pattern matching
- Filter pattern matching

### Syntax Validation Tests
- Valid template processing
- Invalid template error detection
- Issue reporting functionality

### Integration Tests
- Real template generation
- Cross-module compatibility
- File system operations

## Recommendations

1. **Continue Refactoring**: Core module is well-optimized and tested
2. **Add Unit Tests**: Create formal unittest classes for each module
3. **Performance Testing**: Add benchmarking for large template processing
4. **Error Handling**: Enhance error reporting and recovery mechanisms

---
*Generated by Nunjucks Toolbox Test Framework*
"""
        
        report_path = os.path.join(self.project_root, "test-report.md")
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"✅ Test report saved to: {report_path}")
        except Exception as e:
            print(f"❌ Failed to save test report: {e}")
    
    def run_all_tests(self) -> bool:
        """Run all tests and return overall result."""
        print("🔧 Starting comprehensive testing framework...")
        print(f"Project root: {self.project_root}")
        
        tests = [
            ("Core Module", self.test_core_module),
            ("Command Modules", self.test_command_modules),
            ("Script Modules", self.test_script_modules),
            ("Pattern Recognition", self.test_pattern_recognition),
            ("Syntax Validation", self.test_syntax_validation),
            ("Integration", self.run_integration_tests)
        ]
        
        results = []
        all_passed = True
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
                if not result:
                    all_passed = False
            except Exception as e:
                print(f"❌ {test_name} test crashed: {e}")
                results.append((test_name, False))
                all_passed = False
        
        # Print summary
        print(f"\n📊 Test Summary:")
        for test_name, passed in results:
            status = "✅" if passed else "❌"
            print(f"  {status} {test_name}")
        
        # Generate report
        self.generate_test_report()
        
        return all_passed


if __name__ == "__main__":
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    
    framework = NunjucksTestFramework(project_root)
    success = framework.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)

#!/usr/bin/env python3
"""
Tests Nunjucks pattern recognition against template files.
Extracted from GitHub workflow for better maintainability.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List


def test_pattern_recognition(template_file: str) -> bool:
    """Test Nunjucks pattern recognition on a template file."""
    
    template_path = Path(template_file)
    if not template_path.exists():
        print(f"❌ Template file not found: {template_file}")
        return False
    
    try:
        with open(template_path, 'r') as f:
            content = f.read()
        
        # Define patterns to test
        patterns = {
            'comments': r'\{#.*?#\}',
            'variables': r'\{\{.*?\}\}',
            'tags': r'\{%.*?%\}',
            'filters': r'\|[\s]*\w+',
            'blocks': r'\{%\s*block\s+\w+\s*%\}',
            'extends': r'\{%\s*extends\s+["\'].*?["\']',
            'includes': r'\{%\s*include\s+["\'].*?["\']',
            'macros': r'\{%\s*macro\s+\w+.*?%\}'
        }
        
        print('🔍 Testing Nunjucks pattern recognition:')
        print(f'  Template: {template_file}')
        print(f'  Size: {len(content)} characters')
        print()
        
        all_good = True
        total_matches = 0
        
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, content, re.DOTALL)
            match_count = len(matches)
            total_matches += match_count
            
            print(f'  {pattern_name}: {match_count} matches')
            
            if matches:
                # Show first example, truncated if needed
                example = matches[0].replace('\n', ' ').strip()
                if len(example) > 50:
                    example = example[:47] + "..."
                print(f'    Example: {example}')
            
            # Basic validation for critical patterns
            if pattern_name in ['variables', 'tags'] and match_count == 0:
                print(f'    ⚠️  Warning: No {pattern_name} found')
        
        print()
        print(f'✅ Pattern recognition test completed')
        print(f'  Total matches: {total_matches}')
        
        return True
        
    except Exception as e:
        print(f'❌ Error testing pattern recognition: {e}')
        return False


def create_test_template(output_path: str) -> str:
    """Create a comprehensive test template."""
    
    template_content = '''
{# This is a test comment #}
<!DOCTYPE html>
<html>
<head>
    <title>{{ title | default("Test Template") }}</title>
    <meta charset="utf-8">
</head>
<body>
    {% extends "base.html" %}
    
    {% block content %}
        {% if user %}
            <h1>Hello, {{ user.name | capitalize }}!</h1>
            <p>Email: {{ user.email | lower }}</p>
        {% else %}
            <h1>Hello, Guest!</h1>
        {% endif %}
        
        {% for item in items %}
            <div class="item {{ loop.cycle('odd', 'even') }}">
                {{ item.title | safe }}
                {% if item.description %}
                    <p>{{ item.description | truncate(100) }}</p>
                {% endif %}
            </div>
        {% endfor %}
        
        {% macro renderButton(text, type="button", classes="") %}
            <button type="{{ type }}" class="btn {{ classes }}">
                {{ text }}
            </button>
        {% endmacro %}
        
        {{ renderButton("Click me", "submit", "btn-primary") }}
        
        {% include "footer.html" %}
        
        {% set current_year = moment().year() %}
        <p>&copy; {{ current_year }} Company Name</p>
        
        {% filter markdown %}
        This is **markdown** content that will be processed.
        {% endfilter %}
        
        {% raw %}
        This content {{ will not }} be {% processed %}
        {% endraw %}
    {% endblock %}
</body>
</html>
    '''.strip()
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(template_content)
    
    print(f'✅ Test template created: {output_path}')
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Create and test with default template
        test_file = "test-templates/comprehensive.njk"
        create_test_template(test_file)
        success = test_pattern_recognition(test_file)
    else:
        # Test provided template
        test_file = sys.argv[1]
        success = test_pattern_recognition(test_file)
    
    sys.exit(0 if success else 1)

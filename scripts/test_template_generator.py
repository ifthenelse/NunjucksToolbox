#!/usr/bin/env python3
"""
Test template generator for Nunjucks syntax validation.
Creates comprehensive test templates covering all Nunjucks features.
"""

import os
import sys
from pathlib import Path


def create_test_template(output_dir: str = "test-templates") -> str:
    """
    Create a comprehensive test template file.
    
    Args:
        output_dir: Directory to create the template in
        
    Returns:
        Path to the created template file
    """
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    template_content = """
{# This is a comment #}
<!DOCTYPE html>
<html>
<head>
    <title>{{ title | default("Default Title") }}</title>
    <meta charset="utf-8">
    <style>
        .item { margin: 10px 0; }
        .highlight { color: {{ theme.primary | default("#007acc") }}; }
    </style>
</head>
<body>
    {# User authentication section #}
    {% if user %}
        <h1>Hello, {{ user.name | capitalize }}!</h1>
        {% if user.isAdmin %}
            <p>Welcome, administrator!</p>
        {% elif user.isPremium %}
            <p>Premium user detected</p>
        {% else %}
            <p>Regular user</p>
        {% endif %}
    {% else %}
        <h1>Hello, Guest!</h1>
    {% endif %}
    
    {# Items listing with loops #}
    {% if items %}
        <h2>Items ({{ items | length }})</h2>
        {% for item in items %}
            <div class="item" data-index="{{ loop.index }}">
                <span>{{ loop.index }}. {{ item.name | upper }}</span>
                {% if item.description %}
                    <p>{{ item.description | truncate(100) }}</p>
                {% endif %}
            </div>
            {% if not loop.last %}<hr>{% endif %}
        {% else %}
            <p>No items in the list</p>
        {% endfor %}
    {% endif %}
    
    {# Macro definitions #}
    {% macro renderButton(text, type="button", className="btn") %}
        <button type="{{ type }}" class="{{ className }}">
            {{ text | escape }}
        </button>
    {% endmacro %}
    
    {% macro renderCard(title, content, footer=None) %}
        <div class="card">
            <h3>{{ title }}</h3>
            <div class="content">{{ content | safe }}</div>
            {% if footer %}
                <div class="footer">{{ footer }}</div>
            {% endif %}
        </div>
    {% endmacro %}
    
    {# Macro usage #}
    {{ renderButton("Primary Action", "submit", "btn-primary") }}
    {{ renderButton("Cancel") }}
    
    {# Filter examples #}
    <div class="filters-demo">
        <p>Original: {{ sample_text }}</p>
        <p>Upper: {{ sample_text | upper }}</p>
        <p>Lower: {{ sample_text | lower }}</p>
        <p>Capitalized: {{ sample_text | capitalize }}</p>
        <p>Escaped: {{ dangerous_html | escape }}</p>
        <p>Safe: {{ trusted_html | safe }}</p>
        <p>Length: {{ sample_array | length }}</p>
        <p>Join: {{ sample_array | join(", ") }}</p>
        <p>Default: {{ missing_var | default("N/A") }}</p>
    </div>
    
    {# Conditional blocks #}
    {% set show_debug = config.debug | default(false) %}
    {% if show_debug %}
        <div class="debug-info">
            <h3>Debug Information</h3>
            <pre>{{ debug_data | pprint }}</pre>
        </div>
    {% endif %}
    
    {# Advanced loops with conditions #}
    {% for category in categories %}
        {% if category.visible %}
            <section class="category">
                <h2>{{ category.name }}</h2>
                {% for product in category.products %}
                    {% if product.inStock %}
                        <div class="product available">
                            <h4>{{ product.name }} - ${{ product.price | round(2) }}</h4>
                            <p>{{ product.description | truncate(150) }}</p>
                        </div>
                    {% else %}
                        <div class="product unavailable">
                            <h4>{{ product.name }} (Out of Stock)</h4>
                        </div>
                    {% endif %}
                {% endfor %}
            </section>
        {% endif %}
    {% endfor %}
    
    {# Block inheritance example #}
    {% block content %}
        <p>Default content</p>
    {% endblock %}
    
    {# Include example #}
    {% include "partials/footer.html" ignore missing %}
    
    {# Raw content #}
    {% raw %}
        <script>
            // This should not be processed by Nunjucks
            var template = "{{ user.name }}";
            console.log(template);
        </script>
    {% endraw %}
    
</body>
</html>
""".strip()
    
    template_path = os.path.join(output_dir, "test.njk")
    
    try:
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
        print(f"✅ Test template created: {template_path}")
        return template_path
    except Exception as e:
        print(f"❌ Failed to create test template: {e}")
        sys.exit(1)


def create_additional_templates(output_dir: str = "test-templates") -> list:
    """Create additional specialized test templates."""
    templates = []
    
    # Error-prone template for testing validation
    error_template = """
{# Template with intentional errors for testing #}
{% if user %}
    <p>Hello {{ user.name }}</p>
{# Missing endif - should be caught by validation #}

{% for item in items
    <p>{{ item }}</p>
{# Missing endfor and malformed tag #}

{{ unclosed_variable

{# Unclosed comment
""".strip()
    
    error_path = os.path.join(output_dir, "error_test.njk")
    with open(error_path, 'w', encoding='utf-8') as f:
        f.write(error_template)
    templates.append(error_path)
    
    # Minimal template
    minimal_template = """
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ heading }}</h1>
    <p>{{ content | safe }}</p>
</body>
</html>
""".strip()
    
    minimal_path = os.path.join(output_dir, "minimal.njk")
    with open(minimal_path, 'w', encoding='utf-8') as f:
        f.write(minimal_template)
    templates.append(minimal_path)
    
    print(f"✅ Created {len(templates)} additional test templates")
    return templates


if __name__ == "__main__":
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "test-templates"
    
    print("🔧 Creating test templates...")
    main_template = create_test_template(output_dir)
    additional_templates = create_additional_templates(output_dir)
    
    print(f"✅ Template generation completed!")
    print(f"   Main template: {main_template}")
    print(f"   Additional templates: {len(additional_templates)}")

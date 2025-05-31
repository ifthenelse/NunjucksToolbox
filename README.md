# Nunjucks-toolbox

A [Nunjucks](https://mozilla.github.io/nunjucks/) syntax definition for Sublime Text 3 and 4.

## Features

- 🎨 **Syntax Highlighting** - Full Nunjucks template syntax support
- 🏷️ **Multiple Extensions** - Supports `.nunjucks`, `.nunjs`, `.njk`, and `.html` files
- 🔧 **Template Tags** - Complete support for all Nunjucks control structures
- 🎯 **Filters** - Built-in filter highlighting and completion
- 💬 **Comments** - Both line and block comment support
- 🌐 **HTML Integration** - Seamless integration with HTML syntax
- ⚡ **Performance** - Optimized for large template files

## Installation

### Via Package Control (Recommended)
1. Install [Package Control](https://packagecontrol.io/installation)
2. Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
3. Run "Package Control: Install Package"
4. Search for "Nunjucks-toolbox" and install

### Manual Installation
1. Download the latest release from [GitHub Releases](https://github.com/andreacollet/nunjucks-toolbox/releases)
2. Extract to your Sublime Text `Packages` directory
3. Restart Sublime Text

## Supported File Extensions

The syntax automatically activates for files with these extensions:
- `.nunjucks`
- `.nunjs` 
- `.njk`
- `.html` (when containing Nunjucks syntax)

## Syntax Examples

### Variables and Filters
```nunjucks
{{ title | default("Welcome") | upper }}
{{ user.name | capitalize }}
{{ items | length }}
```

### Control Structures
```nunjucks
{% if user.isActive %}
    <p>Welcome back, {{ user.name }}!</p>
{% else %}
    <p>Please log in.</p>
{% endif %}

{% for item in items %}
    <li>{{ item.title }}</li>
{% endfor %}
```

### Template Inheritance
```nunjucks
{% extends "base.html" %}
{% block content %}
    <h1>{{ page.title }}</h1>
{% endblock %}
```

### Macros
```nunjucks
{% macro renderField(name, value="", type="text") %}
    <input type="{{ type }}" name="{{ name }}" value="{{ value }}">
{% endmacro %}

{{ renderField("email", user.email, "email") }}
```

### Comments
```nunjucks
{# This is a line comment #}
{% comment %}
This is a 
block comment
{% endcomment %}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

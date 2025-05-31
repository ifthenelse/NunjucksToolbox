# Nunjucks-toolbox

A comprehensive [Nunjucks](https://mozilla.github.io/nunjucks/) development package for Sublime Text 3 & 4, providing complete syntax highlighting and intelligent development features.

## 🚀 Features

### Core Syntax Support

- 🎨 **Advanced Syntax Highlighting** - Complete Nunjucks template syntax with proper scoping
- 🏷️ **Multi-Extension Support** - `.nunjucks`, `.nunjs`, `.njk`, and `.html` files
- 🔧 **All Template Tags** - Full support for control structures, inheritance, macros, and filters
- 💬 **Smart Comments** - Line (`{# #}`) and block (`{% comment %}`) comment support
- 🌐 **HTML Integration** - Seamless integration with HTML, CSS, and JavaScript

### Developer Productivity

- ⚡ **Auto-Completion** - Smart snippets for common Nunjucks patterns
- 🎯 **Symbol Navigation** - Quick navigation to blocks, macros, and variables via `Ctrl+R`/`Cmd+R`
- 📝 **Auto-Pairing** - Intelligent bracket matching and auto-closing for Nunjucks tags
- 🔧 **Build System** - Integrated template validation and linting
- 📐 **Smart Indentation** - Automatic indentation for nested template structures
- 💡 **Comment Toggle** - Quick commenting with `Ctrl+/`/`Cmd+/`

### Quality Assurance

- ✅ **Template Validation** - Built-in syntax checking and error reporting
- 🧪 **Comprehensive Testing** - Automated testing of all syntax features
- 📊 **CI/CD Integration** - Continuous validation and testing workflows

## 📦 Installation

### Via Package Control (Recommended)

1. Install [Package Control](https://packagecontrol.io/installation)
2. Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
3. Run "Package Control: Install Package"
4. Search for "Nunjucks-toolbox" and install

### Manual Installation

1. Download the latest release from [GitHub Releases](https://github.com/andreacollet/nunjucks-toolbox/releases)
2. Extract to your Sublime Text `Packages` directory
3. Restart Sublime Text

## 🎯 Quick Start

### Available Snippets

Type these triggers and press `Tab` to expand:

| Trigger   | Description          | Output                                      |
| --------- | -------------------- | ------------------------------------------- |
| `for`     | For loop             | `{% for item in items %}...{% endfor %}`    |
| `if`      | If statement         | `{% if condition %}...{% endif %}`          |
| `ifelse`  | If-else statement    | `{% if %}...{% else %}...{% endif %}`       |
| `block`   | Template block       | `{% block name %}...{% endblock %}`         |
| `macro`   | Macro definition     | `{% macro name(params) %}...{% endmacro %}` |
| `extends` | Template inheritance | `{% extends "base.html" %}`                 |
| `include` | Include template     | `{% include "template.html" %}`             |
| `set`     | Variable assignment  | `{% set variable = value %}`                |
| `var`     | Variable output      | `{{ variable }}`                            |
| `filter`  | Variable with filter | `{{ variable \| filter }}`                  |
| `comment` | Line comment         | `{# comment #}`                             |

### Build System Usage

1. Open any `.njk`, `.nunjucks`, or `.nunjs` file
2. Press `Ctrl+B`/`Cmd+B` to validate template syntax
3. Use `Ctrl+Shift+B`/`Cmd+Shift+B` for lint-only mode

## 📝 Syntax Examples

### Variables and Filters

```nunjucks
{{ title | default("Welcome") | upper }}
{{ user.name | capitalize }}
{{ items | length }}
{{ price | round(2) }}
```

### Control Structures

```nunjucks
{% if user.isActive %}
    <p>Welcome back, {{ user.name }}!</p>
{% elif user.isPending %}
    <p>Please verify your account.</p>
{% else %}
    <p>Please log in.</p>
{% endif %}

{% for item in items %}
    <div class="item">{{ item.title }}</div>
{% endfor %}
```

### Template Inheritance

```nunjucks
{% extends "base.html" %}

{% block title %}{{ page.title }}{% endblock %}

{% block content %}
    <h1>{{ page.heading }}</h1>
    <p>{{ page.content }}</p>
{% endblock %}
```

### Macros

```nunjucks
{% macro renderField(name, value="", type="text", required=false) %}
    <div class="field">
        <input
            type="{{ type }}"
            name="{{ name }}"
            value="{{ value }}"
            {% if required %}required{% endif %}
        >
    </div>
{% endmacro %}

{{ renderField("email", user.email, "email", true) }}
```

### Advanced Features

```nunjucks
{# Whitespace control #}
{%- for item in items -%}
    <li>{{ item.name }}</li>
{%- endfor -%}

{# Filters with arguments #}
{{ content | truncate(100) | striptags }}
{{ data | tojson | safe }}

{# Template imports #}
{% from "macros.html" import button, input %}
{{ button("Submit", type="primary") }}
```

## 🔧 Configuration

### Symbol Navigation

The package automatically recognizes:

- **Blocks**: `{% block name %}` - Navigate with `Ctrl+R`/`Cmd+R`
- **Macros**: `{% macro name() %}` - Jump to macro definitions
- **Variables**: `{% set var = value %}` - Find variable assignments

### Auto-Completion

- Type `{%` to trigger tag completion
- Type `{{` to trigger variable completion
- Use `Tab` to cycle through snippet placeholders

### Build System Requirements

For template validation, ensure Node.js and Nunjucks are installed:

```bash
npm install nunjucks
```

## 🧪 Supported File Extensions

The syntax automatically activates for:

- `.nunjucks` - Full Nunjucks templates
- `.nunjs` - Nunjucks JavaScript templates
- `.njk` - Short Nunjucks extension
- `.html` - HTML files with Nunjucks syntax

## 🏗️ Development

### Running Tests

The package includes comprehensive testing:

```bash
# Validate syntax files
python -c "import yaml; yaml.safe_load(open('Nunjucks-toolbox.sublime-syntax'))"

# Test snippet completion
# Open any .njk file and test snippet triggers
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📋 Requirements

- **Sublime Text**: Version 3 or 4
- **Node.js**: Optional, for template validation
- **Nunjucks**: Optional, for build system functionality

## 🆘 Troubleshooting

### Syntax Not Highlighting

1. Check file extension is supported
2. Manually set syntax: `View → Syntax → Nunjucks-toolbox`
3. Restart Sublime Text

### Snippets Not Working

1. Verify scope: syntax should show as "HTML (Nunjucks-toolbox)"
2. Check `Preferences → Settings` for tab completion settings
3. Ensure file is recognized as Nunjucks template

### Build System Issues

1. Install Node.js and Nunjucks: `npm install -g nunjucks`
2. Check file path contains no spaces
3. Verify template syntax is valid

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Nunjucks](https://mozilla.github.io/nunjucks/) templating engine
- [Sublime Text](https://www.sublimetext.com/) editor
- Community contributors and testers

---

**⭐ Star this repo if you find it useful!**

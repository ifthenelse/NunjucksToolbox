# Nunjucks Toolbox for Sublime Text

An advanced [Nunjucks](https://mozilla.github.io/nunjucks/) templating syntax package for Sublime Text 3 & 4.

> **Note**: This is "Nunjucks Toolbox" - a comprehensive package with enhanced features. There's also a separate "Nunjucks" package available.

## Features

- 📝 **24+ New Snippets** - Additional code templates for faster development

- 🎨 **Complete Syntax Highlighting** - Advanced Nunjucks template syntax support
- 📝 **Smart Completions** - Auto-completion for tags, filters, and structures
- 🏷️ **Multiple File Extensions** - `.nunjucks`, `.nunjs`, `.njk`, `.html`
- 🔧 **Build System** - Template validation and linting
- ⚡ **Auto-Pairing** - Intelligent bracket matching
- 💬 **Comment Support** - Line and block comments
- 🎯 **Symbol Navigation** - Jump to blocks, macros, and variables
- 🛠️ **Enhanced Toolbox** - Additional developer productivity features

## Installation

### Package Control (Recommended)

1. Install [Package Control](https://packagecontrol.io/installation)
2. Open Command Palette (`Ctrl+Shift+P`/`Cmd+Shift+P`)
3. Run "Package Control: Install Package"
4. Search for "Nunjucks Toolbox" and install

### Manual Installation

1. Download the latest release
2. Extract to your Sublime Text `Packages/Nunjucks Toolbox` directory
3. Restart Sublime Text

## Usage

The syntax automatically activates for:

- `.nunjucks` files
- `.nunjs` files
- `.njk` files
- `.html` files with Nunjucks syntax

### Snippets

Type these triggers and press `Tab`:

| Trigger   | Description          | Output                                      |
| --------- | -------------------- | ------------------------------------------- |
| `for`     | For loop             | `{% for item in items %}...{% endfor %}`    |
| `if`      | If statement         | `{% if condition %}...{% endif %}`          |
| `block`   | Template block       | `{% block name %}...{% endblock %}`         |
| `macro`   | Macro definition     | `{% macro name(params) %}...{% endmacro %}` |
| `extends` | Template inheritance | `{% extends "base.html" %}`                 |

### Build System

Press `Ctrl+B`/`Cmd+B` to validate template syntax using Node.js.

## Project Structure

```
Syntaxes/           # Syntax definitions
Completions/        # Auto-completion files
Snippets/           # Code snippets
Settings/           # Package settings
Preferences/        # Editor preferences
BuildSystems/       # Build system definitions
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

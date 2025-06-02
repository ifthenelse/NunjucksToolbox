# 📦 Nunjucks Toolbox Installation Guide

## Quick Installation

### Method 1: Package Control (Recommended)

1. Open Sublime Text
2. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
3. Type "Package Control: Install Package"
4. Search for "NunjucksToolbox"
5. Press Enter to install

### Method 2: Manual Installation

1. Download the latest release from the [releases page](https://github.com/ifthenelse/NunjucksToolbox/releases)
2. Extract the archive
3. Copy the `NunjucksToolbox` folder to your Sublime Text `Packages` directory:
   - **Windows**: `%APPDATA%\Sublime Text\Packages\`
   - **macOS**: `~/Library/Application Support/Sublime Text/Packages/`
   - **Linux**: `~/.config/sublime-text/Packages/`

### Method 3: Git Clone

```bash
cd ~/Library/Application\ Support/Sublime\ Text/Packages/  # macOS
# cd ~/.config/sublime-text/Packages/  # Linux
# cd %APPDATA%\Sublime Text\Packages\  # Windows

git clone https://github.com/ifthenelse/NunjucksToolbox.git
```

## 🚀 Features

### ✨ Syntax Highlighting

- Complete Nunjucks syntax support (`.njk`, `.nunjucks`, `.html`)
- HTML + Nunjucks mixed content
- PHP + Nunjucks integration
- Proper scoping for themes

### 🎯 Auto-completion

- All Nunjucks tags: `{% if %}`, `{% for %}`, `{% block %}`, etc.
- Built-in filters: `|escape`, `|default`, `|length`, etc.
- Loop variables: `loop.index`, `loop.first`, `loop.last`
- Smart triggers for `{{`, `{%`, `{#`, and `|`

### 📝 Snippets

- `if` → Complete if/else block
- `for` → For loop with else
- `block` → Template block
- `macro` → Macro definition
- `template` → Complete template with inheritance
- `while` → While loop
- `switch` → Switch statement
- `ternary` → Conditional expression
- And many more!

### 🔧 Commands & Tools

- **Format Template** (`Cmd+Shift+F`): Auto-format with proper indentation
- **Lint Template** (`Cmd+Shift+L`): Check for syntax errors and best practices
- **Validate Template** (`Cmd+Shift+V`): Full template validation
- **Quick Help** (`Cmd+Shift+H`): Quick reference panel

### 🎨 Advanced Features

- Smart indentation rules
- Comment toggling (HTML and Nunjucks styles)
- Symbol navigation (Goto Symbol)
- Build system with multiple variants
- Context menu integration
- Enhanced auto-pairs

## ⌨️ Default Key Bindings

| Command           | macOS         | Windows/Linux  | Description             |
| ----------------- | ------------- | -------------- | ----------------------- |
| Toggle Comment    | `Cmd+/`       | `Ctrl+/`       | Toggle line comments    |
| Block Comment     | `Cmd+Shift+/` | `Ctrl+Shift+/` | Toggle block comments   |
| Format Template   | `Cmd+Shift+F` | `Ctrl+Shift+F` | Auto-format template    |
| Lint Template     | `Cmd+Shift+L` | `Ctrl+Shift+L` | Check for errors        |
| Validate Template | `Cmd+Shift+V` | `Ctrl+Shift+V` | Full validation         |
| Insert Variable   | `Alt+Shift+V` | `Alt+Shift+V`  | Insert `{{ variable }}` |
| Quick Help        | `F1`          | `F1`           | Show help panel         |

## 📋 Build System

The package includes a comprehensive build system with multiple variants:

1. **Default**: Full template validation
2. **Syntax Check Only**: Quick syntax validation
3. **Render with Sample Data**: Test rendering with mock data
4. **Precompile Template**: Precompile for production

Access via `Tools` → `Build System` → `Nunjucks Template Validation`

## 🛠️ Configuration

### File Associations

The package automatically associates with:

- `.njk` files
- `.nunjucks` files
- `.html` files (when containing Nunjucks syntax)

### Settings

Customize in `Preferences` → `Package Settings` → `NunjucksToolbox` → `Settings`:

```json
{
  "auto_complete": true,
  "tab_size": 2,
  "translate_tabs_to_spaces": true,
  "word_wrap": true,
  "rulers": [80, 120]
}
```

## 🔌 Integration with Other Languages

### PHP Integration

The package includes `PHPNunjucks.sublime-syntax` for PHP files containing Nunjucks templates:

```php
<?php
$template = '
    <h1>{{ title }}</h1>
    {% for item in items %}
        <p>{{ item.name }}</p>
    {% endfor %}
';
?>
```

### JavaScript Integration

Works seamlessly with JavaScript template strings containing Nunjucks:

```javascript
const template = `
    <div class="user">
        <h2>{{ user.name }}</h2>
        <p>{{ user.email }}</p>
    </div>
`;
```

## 🧪 Testing

Test your installation by creating a new `.njk` file and trying these features:

1. **Syntax Highlighting**: Create a file with `.njk` extension
2. **Auto-completion**: Type `{{` or `{%` and press `Ctrl+Space`
3. **Snippets**: Type `for` + Tab, `if` + Tab, or `block` + Tab
4. **Build System**: Press `Ctrl+B` / `Cmd+B` to validate syntax
5. **Commands**: Use `Ctrl+Shift+P` and search for "Nunjucks"

## 📚 Documentation Links

- [Nunjucks Official Documentation](https://mozilla.github.io/nunjucks/)
- [Template Inheritance Guide](https://mozilla.github.io/nunjucks/templating.html#template-inheritance)
- [Built-in Filters](https://mozilla.github.io/nunjucks/templating.html#builtin-filters)
- [Global Functions](https://mozilla.github.io/nunjucks/templating.html#builtin-globals)

## 🐛 Troubleshooting

### Template Not Recognized

If syntax highlighting isn't working:

1. Check file extension (`.njk`, `.nunjucks`, `.html`)
2. Manually set syntax: `View` → `Syntax` → `NunjucksToolbox`
3. For mixed content, use `View` → `Syntax` → `PHP with Nunjucks`

### Build System Not Working

1. Ensure Node.js is installed and in PATH
2. Install Nunjucks: `npm install -g nunjucks`
3. Restart Sublime Text

### Completions Not Appearing

1. Check scope: Place cursor in template content
2. Verify settings: `auto_complete` should be `true`
3. Manual trigger: `Ctrl+Space` (Windows/Linux) or `Cmd+Space` (macOS)

## 📈 Version History

### v3.0.0 (Latest)

- ✨ Advanced linting and formatting commands
- 🎯 Enhanced completions with loop variables
- 🔧 PHP integration support
- 📝 New snippets for complex patterns
- 🎨 Improved symbol navigation
- 🚀 Enhanced build system variants

### v2.2.0

- 🎯 Auto-completion improvements
- 📝 Additional snippets
- 🔧 Build system enhancements

### v2.1.0

- 🎨 Syntax highlighting improvements
- 📋 Symbol list support

### v2.0.0

- 🎯 Complete rewrite with advanced features
- 📝 Comprehensive snippet library

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 💡 Support

- 🐛 [Report Issues](https://github.com/ifthenelse/NunjucksToolbox/issues)
- 💬 [Discussions](https://github.com/ifthenelse/NunjucksToolbox/discussions)
- 📧 [Email Support](mailto:support@example.com)

---

**Happy templating with Nunjucks! 🎉**

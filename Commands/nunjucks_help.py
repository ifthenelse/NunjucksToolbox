import sublime
import sublime_plugin
import webbrowser

class NunjucksHelpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """Show Nunjucks documentation options."""
        
        options = [
            ["📖 Nunjucks Documentation", "Open the official Nunjucks documentation"],
            ["🎯 Template Syntax", "Learn about template syntax and tags"],
            ["🔧 Filters Reference", "View all available filters"],
            ["⚙️ Functions Reference", "See global functions and utilities"],
            ["🧩 Template Inheritance", "Learn about blocks and extends"],
            ["🔄 Control Structures", "Loops, conditionals, and macros"],
            ["💡 Best Practices", "Tips and patterns for Nunjucks"],
            ["🐛 Troubleshooting", "Common issues and solutions"]
        ]
        
        def on_done(index):
            if index == -1:
                return
                
            urls = [
                "https://mozilla.github.io/nunjucks/templating.html",
                "https://mozilla.github.io/nunjucks/templating.html#tags",
                "https://mozilla.github.io/nunjucks/templating.html#builtin-filters",
                "https://mozilla.github.io/nunjucks/templating.html#builtin-functions",
                "https://mozilla.github.io/nunjucks/templating.html#template-inheritance",
                "https://mozilla.github.io/nunjucks/templating.html#if",
                "https://mozilla.github.io/nunjucks/templating.html",
                "https://github.com/mozilla/nunjucks/issues"
            ]
            
            webbrowser.open(urls[index])
        
        self.view.window().show_quick_panel(options, on_done)
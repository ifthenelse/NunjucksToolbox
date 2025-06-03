import sublime
import sublime_plugin
import webbrowser


class NunjucksQuickHelpCommand(sublime_plugin.WindowCommand):
    """Quick help panel for common Nunjucks features"""
    
    def run(self):
        items = [
            ["Variables", "{{ variable }}", "Display variables"],
            ["Variables with Filter", "{{ variable | filter }}", "Apply filters to variables"],
            ["Comments", "{# comment #}", "Template comments"],
            ["If Statement", "{% if condition %} ... {% endif %}", "Conditional logic"],
            ["For Loop", "{% for item in items %} ... {% endfor %}", "Iterate over collections"],
            ["Block", "{% block name %} ... {% endblock %}", "Template inheritance blocks"],
            ["Extend", "{% extends 'base.html' %}", "Template inheritance"],
            ["Include", "{% include 'partial.html' %}", "Include other templates"],
            ["Macro", "{% macro name(args) %} ... {% endmacro %}", "Reusable template functions"],
            ["Set Variable", "{% set var = value %}", "Define variables"],
            ["Filter Block", "{% filter upper %} ... {% endfilter %}", "Apply filters to blocks"],
            ["Raw Block", "{% raw %} ... {% endraw %}", "Disable template processing"],
            ["Autoescape", "{% autoescape true %} ... {% endautoescape %}", "Control auto-escaping"],
            ["Call Macro", "{% call macro_name() %} ... {% endcall %}", "Call macros with content"],
            ["With Context", "{% with var = value %} ... {% endwith %}", "Create local context"],
            ["Loop Variables", "loop.index, loop.first, loop.last", "Special loop variables"],
            ["Filters Documentation", "Open Nunjucks filters docs", "View all available filters"],
            ["Template Documentation", "Open Nunjucks templating docs", "Complete templating guide"]
        ]
        
        self.window.show_quick_panel(items, self.on_done)
    
    def on_done(self, index):
        if index == -1:
            return
        
        items = [
            "{{ variable }}",
            "{{ variable | filter }}",
            "{# comment #}",
            "{% if condition %}\n\t$1\n{% endif %}",
            "{% for item in items %}\n\t$1\n{% endfor %}",
            "{% block name %}\n\t$1\n{% endblock %}",
            "{% extends 'base.html' %}",
            "{% include 'partial.html' %}",
            "{% macro name(args) %}\n\t$1\n{% endmacro %}",
            "{% set var = value %}",
            "{% filter upper %}\n\t$1\n{% endfilter %}",
            "{% raw %}\n\t$1\n{% endraw %}",
            "{% autoescape true %}\n\t$1\n{% endautoescape %}",
            "{% call macro_name() %}\n\t$1\n{% endcall %}",
            "{% with var = value %}\n\t$1\n{% endwith %}",
            "loop.index",
            "https://mozilla.github.io/nunjucks/templating.html#builtin-filters",
            "https://mozilla.github.io/nunjucks/templating.html"
        ]
        
        if index >= len(items):
            return
        
        snippet = items[index]
        
        # Open documentation links
        if snippet.startswith("http"):
            webbrowser.open(snippet)
            return
        
        # Insert snippet in active view
        view = self.window.active_view()
        if view:
            view.run_command("insert_snippet", {"contents": snippet})

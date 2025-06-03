import sublime
import sublime_plugin
from .nunjucks_core import NunjucksFormatter


class NunjucksFormatCommand(sublime_plugin.TextCommand):
    """Optimized Nunjucks template formatter command."""

    def run(self, edit):
        """Format the current Nunjucks template."""
        try:
            # Get content
            content = self.view.substr(sublime.Region(0, self.view.size()))

            # Get formatting settings from Sublime Text preferences
            settings = self.view.settings()
            tab_size = settings.get('tab_size', 2)
            use_tabs = not settings.get('translate_tabs_to_spaces', True)

            # Format content
            formatter = NunjucksFormatter(tab_size, use_tabs)
            formatted_content = formatter.format(content)

            # Apply changes if content changed
            if formatted_content != content:
                self.view.replace(
                    edit,
                    sublime.Region(0, self.view.size()),
                    formatted_content
                )
                sublime.status_message("✅ Nunjucks template formatted")
            else:
                sublime.status_message("✅ Template already properly formatted")

        except Exception as e:
            sublime.error_message(f"Formatting error: {str(e)}")

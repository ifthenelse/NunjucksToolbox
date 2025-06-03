import sublime
import sublime_plugin
from .nunjucks_core import get_analyzer, NunjucksUtils


class NunjucksValidateCommand(sublime_plugin.TextCommand):
    """Optimized Nunjucks template validation command."""

    def run(self, edit):
        """Validate Nunjucks template syntax."""
        try:
            content = self.view.substr(sublime.Region(0, self.view.size()))
            analyzer = get_analyzer()
            results = analyzer.analyze(content)

            issues = results['issues']
            is_valid = results['is_valid']

            if not is_valid:
                errors = [i for i in issues if i.severity == 'error']
                self._show_results("❌ Validation Errors Found", errors)
            elif issues:
                warnings = [i for i in issues if i.severity == 'warning']
                self._show_results("⚠️ Validation Warnings", warnings)
            else:
                sublime.status_message("✅ Nunjucks template is valid")

        except Exception as e:
            sublime.error_message(f"Validation error: {str(e)}")

    def _show_results(self, title, issues):
        """Show validation results in a popup."""
        content = NunjucksUtils.format_issues(issues)
        NunjucksUtils.show_popup(self.view, title, content)

import sublime
import sublime_plugin
from .nunjucks_core import get_analyzer, NunjucksUtils


class NunjucksLintCommand(sublime_plugin.TextCommand):
    """Optimized Nunjucks template linting command."""
    
    def run(self, edit):
        """Run linting on current template."""
        try:
            content = self.view.substr(sublime.Region(0, self.view.size()))
            analyzer = get_analyzer()
            results = analyzer.analyze(content)
            
            issues = results['issues']
            if issues:
                self._show_results(issues)
            else:
                sublime.status_message("✅ No linting issues found")
                
        except Exception as e:
            sublime.error_message(f"Linting error: {str(e)}")
    
    def _show_results(self, issues):
        """Display linting results in output panel."""
        # Sort issues by line number and severity
        sorted_issues = sorted(issues, key=lambda x: (x.line, x.severity))
        
        # Format output
        content_lines = ["Nunjucks Linting Results", "=" * 40, ""]
        
        for issue in sorted_issues:
            severity_icon = {
                'error': '❌',
                'warning': '⚠️',
                'info': 'ℹ️'
            }.get(issue.severity, '•')
            
            content_lines.append(
                f"{severity_icon} Line {issue.line}: {issue.message}"
            )
        
        content_lines.extend(["", f"Found {len(sorted_issues)} issue(s)"])
        
        NunjucksUtils.show_panel(
            self.view,
            "Nunjucks Lint Results",
            "\n".join(content_lines),
            "nunjucks_lint"
        )

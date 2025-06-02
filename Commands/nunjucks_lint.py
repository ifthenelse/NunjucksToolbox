import sublime
import sublime_plugin
import re
import json


class NunjucksLintCommand(sublime_plugin.TextCommand):
    """Advanced Nunjucks template linting command"""
    
    def run(self, edit):
        content = self.view.substr(sublime.Region(0, self.view.size()))
        issues = self.lint_template(content)
        
        if issues:
            self.show_issues(issues)
        else:
            sublime.status_message("Nunjucks template: No issues found")

    def lint_template(self, content):
        """Perform comprehensive linting of Nunjucks template"""
        issues = []
        lines = content.split('\n')
        
        # Check for unmatched tags
        tag_stack = []
        tag_patterns = {
            'if': r'{%\s*if\b',
            'for': r'{%\s*for\b',
            'block': r'{%\s*block\b',
            'macro': r'{%\s*macro\b',
            'call': r'{%\s*call\b',
            'filter': r'{%\s*filter\b',
            'with': r'{%\s*with\b',
            'without': r'{%\s*without\b',
            'autoescape': r'{%\s*autoescape\b',
            'raw': r'{%\s*raw\b',
            'verbatim': r'{%\s*verbatim\b',
            'asynceach': r'{%\s*asynceach\b',
            'asyncall': r'{%\s*asyncall\b',
            'while': r'{%\s*while\b'
        }
        
        end_patterns = {
            'if': r'{%\s*endif\b',
            'for': r'{%\s*endfor\b',
            'block': r'{%\s*endblock\b',
            'macro': r'{%\s*endmacro\b',
            'call': r'{%\s*endcall\b',
            'filter': r'{%\s*endfilter\b',
            'with': r'{%\s*endwith\b',
            'without': r'{%\s*endwithout\b',
            'autoescape': r'{%\s*endautoescape\b',
            'raw': r'{%\s*endraw\b',
            'verbatim': r'{%\s*endverbatim\b',
            'asynceach': r'{%\s*endasynceach\b',
            'asyncall': r'{%\s*endasyncall\b',
            'while': r'{%\s*endwhile\b'
        }
        
        for line_num, line in enumerate(lines, 1):
            # Check for opening tags
            for tag, pattern in tag_patterns.items():
                if re.search(pattern, line):
                    tag_stack.append((tag, line_num))
            
            # Check for closing tags
            for tag, pattern in end_patterns.items():
                if re.search(pattern, line):
                    if tag_stack and tag_stack[-1][0] == tag:
                        tag_stack.pop()
                    else:
                        issues.append({
                            'line': line_num,
                            'type': 'error',
                            'message': f'Unmatched end tag: end{tag}'
                        })
            
            # Check for common mistakes
            self.check_common_mistakes(line, line_num, issues)
        
        # Check for unclosed tags
        for tag, line_num in tag_stack:
            issues.append({
                'line': line_num,
                'type': 'error',
                'message': f'Unclosed tag: {tag}'
            })
        
        return issues
    
    def check_common_mistakes(self, line, line_num, issues):
        """Check for common Nunjucks mistakes"""
        
        # Check for unescaped variables in JavaScript context
        if re.search(r'<script[^>]*>', line, re.IGNORECASE):
            if re.search(r'{{\s*\w+\s*}}', line):
                issues.append({
                    'line': line_num,
                    'type': 'warning',
                    'message': 'Unescaped variable in JavaScript context. Consider using |tojson filter.'
                })
        
        # Check for missing filters on user input
        user_input_patterns = [
            r'{{\s*(user\.|request\.|params\.|query\.)',
            r'{{\s*\w*input\w*',
            r'{{\s*\w*form\w*'
        ]
        
        for pattern in user_input_patterns:
            if re.search(pattern, line):
                if not re.search(r'\|\s*(escape|e|safe)\b', line):
                    issues.append({
                        'line': line_num,
                        'type': 'warning',
                        'message': 'User input should be escaped. Consider adding |escape filter.'
                    })
        
        # Check for deprecated syntax
        if re.search(r'{%\s*endif\s+\w+', line):
            issues.append({
                'line': line_num,
                'type': 'warning',
                'message': 'Named endif is deprecated. Use {% endif %} instead.'
            })
    
    def show_issues(self, issues):
        """Display linting issues in a panel"""
        output_view = self.view.window().create_output_panel("nunjucks_lint")
        output_view.set_name("Nunjucks Lint Results")
        
        output_text = "Nunjucks Linting Results:\n" + "=" * 30 + "\n\n"
        
        for issue in issues:
            output_text += f"Line {issue['line']}: [{issue['type'].upper()}] {issue['message']}\n"
        
        output_view.run_command("append", {"characters": output_text})
        self.view.window().run_command("show_panel", {"panel": "output.nunjucks_lint"})

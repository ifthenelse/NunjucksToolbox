"""
Core utilities and optimized patterns for Nunjucks Toolbox.
Eliminates code duplication and provides high-performance shared functionality.
"""

import re
import sublime
from typing import Dict, List, Tuple, Optional, NamedTuple
from functools import lru_cache


class NunjucksIssue(NamedTuple):
    """Immutable issue representation for better performance."""
    line: int
    severity: str  # 'error', 'warning', 'info'
    message: str
    issue_type: str = 'syntax'


class NunjucksPatterns:
    """Pre-compiled regex patterns for optimal performance."""

    def __init__(self):
        # Core patterns - compiled once for reuse
        self.VARIABLE = re.compile(r'\{\{\s*([^}]+)\s*\}\}')
        self.TAG = re.compile(r'\{%\s*([^%]+)\s*%\}')
        self.COMMENT = re.compile(r'\{#([^#]*?)#\}', re.DOTALL)
        self.FILTER = re.compile(r'\|\s*([a-zA-Z_][a-zA-Z0-9_]*)')

        # Block matching - optimized patterns
        self.BLOCKS = {
            'if': (
                re.compile(r'\{%\s*if\s+'),
                re.compile(r'\{%\s*endif\s*%\}')
            ),
            'for': (
                re.compile(r'\{%\s*for\s+'),
                re.compile(r'\{%\s*endfor\s*%\}')
            ),
            'block': (
                re.compile(r'\{%\s*block\s+'),
                re.compile(r'\{%\s*endblock\s*(?:\s+\w+)?\s*%\}')
            ),
            'macro': (
                re.compile(r'\{%\s*macro\s+'),
                re.compile(r'\{%\s*endmacro\s*%\}')
            ),
            'call': (
                re.compile(r'\{%\s*call\s+'),
                re.compile(r'\{%\s*endcall\s*%\}')
            ),
            'filter': (
                re.compile(r'\{%\s*filter\s+'),
                re.compile(r'\{%\s*endfilter\s*%\}')
            ),
            'with': (
                re.compile(r'\{%\s*with\s+'),
                re.compile(r'\{%\s*endwith\s*%\}')
            ),
            'without': (
                re.compile(r'\{%\s*without\s+'),
                re.compile(r'\{%\s*endwithout\s*%\}')
            ),
            'autoescape': (
                re.compile(r'\{%\s*autoescape\s+'),
                re.compile(r'\{%\s*endautoescape\s*%\}')
            ),
            'raw': (
                re.compile(r'\{%\s*raw\s*%\}'),
                re.compile(r'\{%\s*endraw\s*%\}')
            ),
            'verbatim': (
                re.compile(r'\{%\s*verbatim\s*%\}'),
                re.compile(r'\{%\s*endverbatim\s*%\}')
            ),
            'asynceach': (
                re.compile(r'\{%\s*asynceach\s+'),
                re.compile(r'\{%\s*endasynceach\s*%\}')
            ),
            'asyncall': (
                re.compile(r'\{%\s*asyncall\s+'),
                re.compile(r'\{%\s*endasyncall\s*%\}')
            ),
            'while': (
                re.compile(r'\{%\s*while\s+'),
                re.compile(r'\{%\s*endwhile\s*%\}')
            )
        }

        # Special control structures
        self.ELSE_ELIF = re.compile(r'\{%\s*(?:else|elif|elseif)(?:\s|%)')

        # Security and best practice patterns
        self.SECURITY = {
            'user_input': re.compile(
                r'\{\{\s*(?:user\.|request\.|params\.|query\.|'
                r'\w*input\w*|\w*form\w*)'
            ),
            'script_context': re.compile(r'<script[^>]*>', re.IGNORECASE),
            'unescaped_var': re.compile(r'\{\{\s*\w+\s*\}\}'),
            'escape_filter': re.compile(r'\|\s*(?:escape|e|safe)\b')
        }

        # Bracket balance patterns
        self.BRACKETS = [
            ('variable', re.compile(r'\{\{'), re.compile(r'\}\}')),
            ('tag', re.compile(r'\{%'), re.compile(r'%\}')),
            ('comment', re.compile(r'\{#'), re.compile(r'#\}'))
        ]

    @lru_cache(maxsize=256)
    def get_block_info(self, tag_name: str) -> Optional[Tuple]:
        """Cached block pattern lookup."""
        return self.BLOCKS.get(tag_name)


class NunjucksAnalyzer:
    """High-performance template analyzer with optimized parsing."""

    def __init__(self):
        self.patterns = NunjucksPatterns()
        self._reset()

    def _reset(self):
        """Reset analyzer state."""
        self.tag_stack: List[Tuple[str, int]] = []
        self.issues: List[NunjucksIssue] = []
        self.stats = {
            'blocks_defined': set(),
            'blocks_used': set(),
            'variables_used': set(),
            'filters_used': set(),
            'extends_template': None,
            'includes': set()
        }

    def analyze(self, content: str) -> Dict:
        """Perform comprehensive template analysis."""
        self._reset()

        # Quick bracket balance check first
        bracket_issues = self._check_brackets(content)
        self.issues.extend(bracket_issues)

        # Line-by-line analysis
        lines = content.splitlines()
        for line_num, line in enumerate(lines, 1):
            self._analyze_line(line, line_num)

        # Final checks
        self._check_unclosed_tags()
        self._check_template_structure()

        return {
            'issues': self.issues,
            'statistics': self.stats,
            'is_valid': not any(
                issue.severity == 'error' for issue in self.issues
            )
        }

    def _analyze_line(self, line: str, line_num: int):
        """Analyze a single line efficiently."""
        # Check block structures
        self._check_blocks(line, line_num)

        # Extract and analyze variables
        self._extract_variables(line)

        # Security and best practice checks
        self._check_security(line, line_num)

        # Template inheritance patterns
        self._check_inheritance(line)

    def _check_blocks(self, line: str, line_num: int):
        """Check block opening/closing patterns."""
        blocks = self.patterns.BLOCKS.items()
        for block_name, (open_pattern, close_pattern) in blocks:
            # Check for opening tags
            if open_pattern.search(line):
                self.tag_stack.append((block_name, line_num))

                # Extract block names for 'block' tags
                if block_name == 'block':
                    block_match = re.search(r'\{%\s*block\s+(\w+)', line)
                    if block_match:
                        self.stats['blocks_defined'].add(
                            block_match.group(1)
                        )

            # Check for closing tags
            elif close_pattern.search(line):
                if self.tag_stack and self.tag_stack[-1][0] == block_name:
                    self.tag_stack.pop()
                else:
                    self.issues.append(NunjucksIssue(
                        line_num, 'error',
                        f'Unmatched closing tag: end{block_name}',
                        'block_mismatch'
                    ))

        # Check else/elif placement
        if self.patterns.ELSE_ELIF.search(line):
            valid_context = ['if', 'for']
            if (not self.tag_stack or
                    self.tag_stack[-1][0] not in valid_context):
                self.issues.append(NunjucksIssue(
                    line_num, 'error',
                    'else/elif outside of if/for block',
                    'syntax'
                ))

        # Deprecated syntax
        if re.search(r'\{%\s*endif\s+\w+', line):
            self.issues.append(NunjucksIssue(
                line_num, 'warning',
                'Named endif is deprecated. Use {% endif %}.',
                'deprecated'
            ))

    def _extract_variables(self, line: str):
        """Extract variables and filters from line."""
        for var_match in self.patterns.VARIABLE.finditer(line):
            var_content = var_match.group(1).strip()

            # Extract base variable name
            base_var = var_content.split('|')[0].split('.')[0].strip()
            if base_var:
                self.stats['variables_used'].add(base_var)

            # Extract filters
            filter_matches = self.patterns.FILTER.finditer(var_content)
            for filter_match in filter_matches:
                self.stats['filters_used'].add(filter_match.group(1))

    def _check_security(self, line: str, line_num: int):
        """Check for security issues and best practices."""
        # Check for potential XSS in script context
        if (self.patterns.SECURITY['script_context'].search(line) and
                self.patterns.SECURITY['unescaped_var'].search(line)):
            if not self.patterns.SECURITY['escape_filter'].search(line):
                self.issues.append(NunjucksIssue(
                    line_num, 'warning',
                    'Unescaped variable in JavaScript context. '
                    'Use |tojson filter.',
                    'security'
                ))

        # User input without escaping
        if self.patterns.SECURITY['user_input'].search(line):
            if not self.patterns.SECURITY['escape_filter'].search(line):
                self.issues.append(NunjucksIssue(
                    line_num, 'warning',
                    'User input should be escaped for security',
                    'security'
                ))

    def _check_inheritance(self, line: str):
        """Check template inheritance patterns."""
        # Extends
        extends_match = re.search(
            r'\{%\s*extends\s+["\']([^"\']+)["\']', line
        )
        if extends_match:
            self.stats['extends_template'] = extends_match.group(1)

        # Includes
        include_match = re.search(
            r'\{%\s*include\s+["\']([^"\']+)["\']', line
        )
        if include_match:
            self.stats['includes'].add(include_match.group(1))

    def _check_brackets(self, content: str) -> List[NunjucksIssue]:
        """Check bracket balance efficiently."""
        issues = []

        for bracket_type, open_pattern, close_pattern in (
                self.patterns.BRACKETS):
            open_count = len(open_pattern.findall(content))
            close_count = len(close_pattern.findall(content))

            if open_count != close_count:
                issues.append(NunjucksIssue(
                    0, 'error',
                    f'Unmatched {bracket_type} brackets: '
                    f'{open_count} open, {close_count} close',
                    'bracket_mismatch'
                ))

        return issues

    def _check_unclosed_tags(self):
        """Check for unclosed block tags."""
        for tag_name, line_num in self.tag_stack:
            self.issues.append(NunjucksIssue(
                line_num, 'error',
                f'Unclosed {tag_name} tag',
                'unclosed_tag'
            ))

    def _check_template_structure(self):
        """Check overall template structure."""
        # Check if child template defines blocks without extending
        if (self.stats['blocks_defined'] and
                not self.stats['extends_template']):
            self.issues.append(NunjucksIssue(
                0, 'info',
                'Template defines blocks but doesn\'t extend '
                'a base template',
                'template_structure'
            ))


class NunjucksFormatter:
    """Optimized template formatter with intelligent indentation."""

    def __init__(self, tab_size: int = 2, use_tabs: bool = False):
        self.indent_char = '\t' if use_tabs else ' ' * tab_size
        self.patterns = NunjucksPatterns()

        # Tags that increase indentation
        self.indent_tags = {
            'if', 'for', 'block', 'macro', 'call', 'filter',
            'with', 'without', 'autoescape', 'raw', 'verbatim',
            'asynceach', 'asyncall', 'while'
        }

        # Tags that decrease indentation permanently
        self.dedent_tags = {
            'endif', 'endfor', 'endblock', 'endmacro', 'endcall',
            'endfilter', 'endwith', 'endwithout', 'endautoescape',
            'endraw', 'endverbatim', 'endasynceach', 'endasyncall',
            'endwhile'
        }

        # Tags that temporarily decrease indentation
        self.temp_dedent_tags = {'else', 'elif', 'elseif'}

    def format(self, content: str) -> str:
        """Format template with proper indentation."""
        lines = content.splitlines()
        formatted_lines = []
        indent_level = 0

        for line in lines:
            stripped = line.strip()

            # Skip empty lines
            if not stripped:
                formatted_lines.append('')
                continue

            # Check for temporary dedent (else, elif)
            temp_dedent = any(
                re.search(r'\{%\s*' + tag + r'(?:\s|%)', stripped)
                for tag in self.temp_dedent_tags
            )

            # Check for permanent dedent (end tags)
            perm_dedent = any(
                re.search(r'\{%\s*' + tag + r'\s*%\}', stripped)
                for tag in self.dedent_tags
            )

            # Calculate current line indentation
            current_indent = max(
                0, indent_level - (1 if temp_dedent or perm_dedent else 0)
            )

            # Add formatted line
            formatted_lines.append(
                self.indent_char * current_indent + stripped
            )

            # Adjust indentation for next line
            if perm_dedent:
                indent_level = max(0, indent_level - 1)
            elif any(
                re.search(r'\{%\s*' + tag + r'\s+', stripped)
                for tag in self.indent_tags
            ):
                indent_level += 1

        return '\n'.join(formatted_lines)


class NunjucksUtils:
    """Utility functions for Sublime Text integration."""

    @staticmethod
    def show_panel(view: sublime.View, title: str, content: str,
                   panel_name: str = "nunjucks_output"):
        """Show content in Sublime Text output panel."""
        window = view.window()
        if not window:
            return

        panel = window.create_output_panel(panel_name)
        panel.set_name(title)

        # Clear and populate panel
        panel.run_command("select_all")
        panel.run_command("right_delete")
        panel.run_command("append", {"characters": content})


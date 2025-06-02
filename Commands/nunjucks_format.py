import sublime
import sublime_plugin
import re


class NunjucksFormatCommand(sublime_plugin.TextCommand):
    """Format Nunjucks templates with proper indentation"""
    
    def run(self, edit):
        content = self.view.substr(sublime.Region(0, self.view.size()))
        formatted_content = self.format_template(content)
        
        if formatted_content != content:
            self.view.replace(edit, sublime.Region(0, self.view.size()), formatted_content)
            sublime.status_message("Nunjucks template formatted")
        else:
            sublime.status_message("Nunjucks template already properly formatted")
    
    def format_template(self, content):
        """Format Nunjucks template with proper indentation"""
        lines = content.split('\n')
        formatted_lines = []
        indent_level = 0
        indent_char = '    '  # 4 spaces
        
        # Tags that increase indentation
        increase_indent_tags = [
            'if', 'for', 'block', 'macro', 'call', 'filter', 
            'with', 'without', 'autoescape', 'raw', 'verbatim',
            'asynceach', 'asyncall', 'while'
        ]
        
        # Tags that decrease indentation
        decrease_indent_tags = [
            'endif', 'endfor', 'endblock', 'endmacro', 'endcall', 
            'endfilter', 'endwith', 'endwithout', 'endautoescape',
            'endraw', 'endverbatim', 'endasynceach', 'endasyncall', 
            'endwhile', 'else', 'elif', 'elseif'
        ]
        
        for line in lines:
            stripped_line = line.strip()
            
            # Skip empty lines
            if not stripped_line:
                formatted_lines.append('')
                continue
            
            # Check if this line should decrease indentation
            should_decrease = False
            for tag in decrease_indent_tags:
                if re.search(r'{%\s*' + tag + r'\b', stripped_line):
                    should_decrease = True
                    break
            
            # Apply indentation
            if should_decrease:
                current_indent = max(0, indent_level - 1)
            else:
                current_indent = indent_level
            
            formatted_line = (indent_char * current_indent) + stripped_line
            formatted_lines.append(formatted_line)
            
            # Update indent level for next line
            if should_decrease and not any(re.search(r'{%\s*' + tag + r'\b', stripped_line) for tag in ['else', 'elif', 'elseif']):
                indent_level = max(0, indent_level - 1)
            
            # Check if this line should increase indentation for next line
            for tag in increase_indent_tags:
                if re.search(r'{%\s*' + tag + r'\b', stripped_line):
                    # Don't increase if it's a self-closing tag or has end tag on same line
                    if not re.search(r'{%\s*end' + tag + r'\s*%}', stripped_line):
                        indent_level += 1
                    break
        
        return '\n'.join(formatted_lines)

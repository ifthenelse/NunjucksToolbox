import sublime
import sublime_plugin
import re

class NunjucksValidateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """Validate Nunjucks template syntax."""
        
        content = self.view.substr(sublime.Region(0, self.view.size()))
        
        errors = []
        warnings = []
        
        try:
            # Check for unclosed brackets
            self.check_brackets(content, errors)
            
            # Check for proper block structure
            self.check_blocks(content, errors, warnings)
            
            # Check for common issues
            self.check_common_issues(content, warnings)
            
            if errors:
                self.show_results("❌ Validation Errors Found", errors, warnings)
            elif warnings:
                self.show_results("⚠️ Validation Warnings", [], warnings)
            else:
                sublime.status_message("✅ Nunjucks template is valid")
                
        except Exception as e:
            sublime.error_message(f"Validation error: {str(e)}")
    
    def check_brackets(self, content, errors):
        """Check for unmatched brackets."""
        
        patterns = [
            (r'\{\{', r'\}\}', 'Variable brackets'),
            (r'\{%', r'%\}', 'Tag brackets'),
            (r'\{#', r'#\}', 'Comment brackets')
        ]
        
        for open_pattern, close_pattern, name in patterns:
            open_count = len(re.findall(open_pattern, content))
            close_count = len(re.findall(close_pattern, content))
            
            if open_count != close_count:
                errors.append(f"Unmatched {name}: {open_count} opening, {close_count} closing")
    
    def check_blocks(self, content, errors, warnings):
        """Check block structure."""
        
        # Find all block definitions
        blocks = re.findall(r'{%\s*block\s+(\w+)\s*%}', content)
        endblocks = re.findall(r'{%\s*endblock(?:\s+(\w+))?\s*%}', content)
        
        if len(blocks) != len(endblocks):
            errors.append(f"Block count mismatch: {len(blocks)} blocks, {len(endblocks)} endblocks")
        
        # Check for unused blocks in child templates
        extends = re.findall(r'{%\s*extends\s+["\']([^"\']+)["\']', content)
        if not extends and blocks:
            warnings.append("Template defines blocks but doesn't extend a base template")
    
    def check_common_issues(self, content, warnings):
        """Check for common Nunjucks issues."""
        
        # Check for potentially unsafe variables
        unsafe_vars = re.findall(r'{{\s*(\w+)\s*}}', content)
        for var in unsafe_vars:
            if var in ['user_input', 'raw_html', 'untrusted']:
                warnings.append(f"Variable '{var}' might need escaping or |safe filter")
        
        # Check for missing filters on loops
        for_loops = re.findall(r'{%\s*for\s+\w+\s+in\s+(\w+)\s*%}', content)
        for loop_var in for_loops:
            if not re.search(rf'{{\s*{loop_var}\s*\|\s*\w+', content):
                warnings.append(f"Loop variable '{loop_var}' used without filters - consider adding |default() or similar")
    
    def show_results(self, title, errors, warnings):
        """Show validation results in a popup."""
        
        content = f"<body><h3>{title}</h3>"
        
        if errors:
            content += "<h4>❌ Errors:</h4><ul>"
            for error in errors:
                content += f"<li>{error}</li>"
            content += "</ul>"
        
        if warnings:
            content += "<h4>⚠️ Warnings:</h4><ul>"
            for warning in warnings:
                content += f"<li>{warning}</li>"
            content += "</ul>"
        
        content += "</body>"
        
        self.view.show_popup(content, max_width=600, max_height=400)
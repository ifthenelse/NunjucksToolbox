# Commands/nunjucks_validate.py
import sublime
import sublime_plugin

class NunjucksValidateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        content = self.view.substr(sublime.Region(0, self.view.size()))
        
        try:
            # Basic Nunjucks syntax validation
            if not self.validate_brackets(content):
                sublime.error_message("Invalid Nunjucks bracket syntax!")
                return
                
            sublime.status_message("✓ Nunjucks template is valid")
            
        except Exception as e:
            sublime.error_message(f"Validation error: {str(e)}")
    
    def validate_brackets(self, content):
        import re
        
        # Check for unclosed brackets
        open_vars = len(re.findall(r'\{\{', content))
        close_vars = len(re.findall(r'\}\}', content))
        
        open_tags = len(re.findall(r'\{%', content))
        close_tags = len(re.findall(r'%\}', content))
        
        open_comments = len(re.findall(r'\{#', content))
        close_comments = len(re.findall(r'#\}', content))
        
        return (open_vars == close_vars and 
                open_tags == close_tags and 
                open_comments == close_comments)
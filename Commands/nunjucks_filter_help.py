# Commands/nunjucks_filter_help.py
import sublime_plugin

class NunjucksFilterHelpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filters = {
            'abs': 'Get absolute value of a number',
            'capitalize': 'Capitalize the first letter',
            'default': 'Provide default value if variable is undefined',
            'escape': 'Escape HTML characters',
            'first': 'Get first item from array',
            'join': 'Join array elements with separator',
            'last': 'Get last item from array',
            'length': 'Get length of array or string',
            'lower': 'Convert to lowercase',
            'replace': 'Replace substring with another',
            'reverse': 'Reverse array or string',
            'round': 'Round number to specified precision',
            'safe': 'Mark string as safe (no escaping)',
            'slice': 'Extract slice from array',
            'sort': 'Sort array',
            'title': 'Convert to title case',
            'trim': 'Remove whitespace',
            'upper': 'Convert to uppercase',
            'urlencode': 'URL encode string'
        }
        
        filter_list = [f"{name}: {desc}" for name, desc in filters.items()]
        
        def on_done(index):
            if index >= 0:
                filter_name = list(filters.keys())[index]
                self.view.run_command('insert', {'characters': filter_name})
        
        self.view.window().show_quick_panel(filter_list, on_done)
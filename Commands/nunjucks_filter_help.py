import sublime
import sublime_plugin

class NunjucksFilterHelpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """Show Nunjucks filter reference and insert selected filter."""
        
        filters = [
            ["abs", "Get absolute value of a number", "{{ number | abs }}"],
            ["capitalize", "Capitalize the first letter", "{{ string | capitalize }}"],
            ["default", "Provide default value if variable is undefined", "{{ var | default('fallback') }}"],
            ["escape", "Escape HTML characters", "{{ html | escape }}"],
            ["first", "Get first item from array", "{{ array | first }}"],
            ["join", "Join array elements with separator", "{{ array | join(', ') }}"],
            ["last", "Get last item from array", "{{ array | last }}"],
            ["length", "Get length of array or string", "{{ items | length }}"],
            ["lower", "Convert to lowercase", "{{ string | lower }}"],
            ["replace", "Replace substring with another", "{{ string | replace('old', 'new') }}"],
            ["reverse", "Reverse array or string", "{{ array | reverse }}"],
            ["round", "Round number to specified precision", "{{ number | round(2) }}"],
            ["safe", "Mark string as safe (no escaping)", "{{ html | safe }}"],
            ["slice", "Extract slice from array", "{{ array | slice(1, 5) }}"],
            ["sort", "Sort array", "{{ array | sort }}"],
            ["title", "Convert to title case", "{{ string | title }}"],
            ["trim", "Remove whitespace", "{{ string | trim }}"],
            ["upper", "Convert to uppercase", "{{ string | upper }}"],
            ["urlencode", "URL encode string", "{{ string | urlencode }}"]
        ]
        
        # Format for display
        display_options = [f"{name} - {desc}" for name, desc, _ in filters]
        
        def on_done(index):
            if index == -1:
                return
            
            filter_name, _, example = filters[index]
            
            # Show example in a popup
            content = f"""
            <body>
                <style>
                    body {{ font-family: system; margin: 10px; }}
                    .filter {{ color: var(--orangish); font-weight: bold; }}
                    .example {{ background: var(--background); padding: 10px; border-radius: 4px; }}
                    .usage {{ color: var(--foreground); font-family: monospace; }}
                </style>
                <h3><span class="filter">{filter_name}</span> filter</h3>
                <div class="example">
                    <strong>Usage:</strong><br>
                    <code class="usage">{example}</code>
                </div>
            </body>
            """
            
            self.view.show_popup(content, max_width=400, max_height=200)
            
            # Also insert just the filter name at cursor
            self.view.run_command('insert', {'characters': filter_name})
        
        self.view.window().show_quick_panel(display_options, on_done)
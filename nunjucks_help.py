import sublime
import sublime_plugin
import webbrowser
import urllib.parse

print("NunjucksHelpCommand loaded!")

class NunjucksHelpCommand(sublime_plugin.TextCommand):
    """Nunjucks help command with API lookup functionality."""

    def run(self, edit):
        """Show help dialog with API lookup options."""
        # Get selected text for potential API lookup
        selected_text = ""
        for region in self.view.sel():
            if not region.empty():
                selected_text = self.view.substr(region).strip()
                break

        api_text = "Look up Nunjucks API"
        if selected_text:
            api_text += " for: {}".format(selected_text)

        items = [
            ["🔍 API Lookup", api_text],
            ["📖 Documentation", "Open the official Nunjucks documentation"],
            ["🎯 Template Syntax", "Learn about template syntax and tags"],
            ["🔧 Filters Reference", "View all available filters"],
            ["⚙️ Functions Reference", "See global functions and utilities"],
            ["🧩 Template Inheritance", "Learn about blocks and extends"],
            ["🔄 Control Structures", "Loops, conditionals, and macros"],
            ["💡 Best Practices", "Tips and patterns for Nunjucks"],
            ["🐛 Troubleshooting", "Common issues and solutions"],
            ["📋 Format Template", "Format the current Nunjucks template"],
            ["✅ Validate Template", "Validate the current Nunjucks template"],
        ]

        self.view.window().show_quick_panel(
            items,
            self.on_help_selected
        )

    def on_help_selected(self, index):
        """Handle help selection."""
        if index == -1:
            return

        if index == 0:  # API Lookup
            self.lookup_api()
        elif index == 9:  # Format Template
            self.view.run_command("nunjucks_format")
        elif index == 10:  # Validate Template
            self.view.run_command("nunjucks_validate")
        else:  # Documentation links
            base_url = "https://mozilla.github.io/nunjucks/"
            urls = [
                "",  # API Lookup - handled above
                base_url + "templating.html",
                base_url + "templating.html#tags",
                base_url + "templating.html#builtin-filters",
                base_url + "templating.html#builtin-functions",
                base_url + "templating.html#template-inheritance",
                base_url + "templating.html#if",
                base_url + "templating.html",
                "https://github.com/mozilla/nunjucks/issues",
                "",  # Format - handled above
                "",  # Validate - handled above
            ]

            if 1 <= index <= 8 and urls[index]:
                webbrowser.open(urls[index])

    def lookup_api(self):
        """Show API lookup options or search for selected text."""
        # Get selected text
        selected_text = ""
        for region in self.view.sel():
            if not region.empty():
                selected_text = self.view.substr(region).strip()
                break

        if selected_text:
            # Direct lookup for selected text
            self.search_api(selected_text)
        else:
            # Show API categories
            self.show_api_categories()

    def show_api_categories(self):
        """Show Nunjucks API categories."""
        api_items = [
            ["🌍 Environment", "Environment configuration and setup"],
            ["📄 Template", "Template rendering and compilation"],
            ["🔧 Filters", "Built-in and custom filters"],
            ["🔤 Functions", "Global functions"],
            ["🧩 Extensions", "Custom extensions"],
            ["📂 Loaders", "Template loaders"],
            ["🔍 Search API", "Search for specific API method"],
        ]

        self.view.window().show_quick_panel(
            api_items,
            self.on_api_category_selected
        )

    def on_api_category_selected(self, index):
        """Handle API category selection."""
        if index == -1:
            return

        categories = [
            "environment",
            "template",
            "templating#builtin-filters",
            "templating#global-functions",
            "api#custom-filters",
            "api#loaders",
            ""  # Search
        ]

        if index == 6:  # Search
            self.show_api_search()
        else:
            url = "https://mozilla.github.io/nunjucks/api.html"
            if categories[index]:
                if categories[index].startswith('templating#'):
                    base = "https://mozilla.github.io/nunjucks/"
                    url = base + categories[index]
                else:
                    url += "#" + categories[index]
            webbrowser.open(url)

    def show_api_search(self):
        """Show input panel for API search."""
        self.view.window().show_input_panel(
            "Search Nunjucks API:",
            "",
            self.search_api,
            None,
            None
        )

    def search_api(self, query):
        """Search for API method and open documentation."""
        if not query:
            return

        # Common API methods mapping
        api_methods = {
            # Environment methods
            'environment': '',
            'configure': 'configure',
            'render': 'render',
            'renderstring': 'renderstring',
            'addfilter': 'addfilter',
            'addextension': 'addextension',
            'addglobal': 'addglobal',
            'getfilter': 'getfilter',
            'getglobal': 'getglobal',
            'gettemplate': 'gettemplate',

            # Template methods
            'template': 'template',
            'compile': 'compile',

            # Loaders
            'filesystemloader': 'filesystemloader',
            'webloader': 'webloader',
            'precompiledloader': 'precompiledloader',

            # Built-in filters
            'abs': 'templating#abs',
            'batch': 'templating#batch',
            'capitalize': 'templating#capitalize',
            'center': 'templating#center',
            'default': 'templating#default-d',
            'dictsort': 'templating#dictsort',
            'dump': 'templating#dump',
            'escape': 'templating#escape-e',
            'first': 'templating#first',
            'float': 'templating#float',
            'forceescape': 'templating#forceescape',
            'groupby': 'templating#groupby',
            'indent': 'templating#indent',
            'int': 'templating#int',
            'join': 'templating#join',
            'last': 'templating#last',
            'length': 'templating#length',
            'list': 'templating#list',
            'lower': 'templating#lower',
            'nl2br': 'templating#nl2br',
            'random': 'templating#random',
            'reject': 'templating#reject',
            'rejectattr': 'templating#rejectattr',
            'replace': 'templating#replace',
            'reverse': 'templating#reverse',
            'round': 'templating#round',
            'safe': 'templating#safe',
            'select': 'templating#select',
            'selectattr': 'templating#selectattr',
            'slice': 'templating#slice',
            'sort': 'templating#sort',
            'string': 'templating#string',
            'striptags': 'templating#striptags',
            'sum': 'templating#sum',
            'title': 'templating#title',
            'trim': 'templating#trim',
            'truncate': 'templating#truncate',
            'upper': 'templating#upper',
            'urlencode': 'templating#urlencode',
            'urlize': 'templating#urlize',
            'wordcount': 'templating#wordcount',
            'wordwrap': 'templating#wordwrap',
        }

        query_lower = query.lower().strip()

        # Direct match
        if query_lower in api_methods:
            anchor = api_methods[query_lower]
            if anchor.startswith('templating#'):
                url = "https://mozilla.github.io/nunjucks/" + anchor
            else:
                url = "https://mozilla.github.io/nunjucks/api.html"
                if anchor:
                    url += "#" + anchor
        else:
            # Partial match or general search
            matches = [method for method in api_methods.keys()
                       if query_lower in method]
            if matches:
                # Use first match
                anchor = api_methods[matches[0]]
                if anchor.startswith('templating#'):
                    base = "https://mozilla.github.io/nunjucks/"
                    url = base + anchor
                else:
                    url = "https://mozilla.github.io/nunjucks/api.html"
                    if anchor:
                        url += "#" + anchor
            else:
                # General search - go to main API page
                url = "https://mozilla.github.io/nunjucks/api.html"

        webbrowser.open(url)

        # Show status message
        msg = "Opened Nunjucks API documentation for: " + query
        sublime.status_message(msg)
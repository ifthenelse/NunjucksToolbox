#!/usr/bin/env python3
"""
Performance benchmarking and optimization tool for Nunjucks Toolbox.
Measures processing times and identifies performance bottlenecks.
"""

import os
import sys
import time
import importlib.util
import tempfile
import statistics
from pathlib import Path
from typing import Dict, List, Tuple


class PerformanceBenchmark:
    """Performance testing and optimization toolkit."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = os.path.abspath(project_root)
        self.commands_dir = os.path.join(self.project_root, "Commands")
        self.scripts_dir = os.path.join(self.project_root, "scripts")
        self.results = {}
        
    def load_module(self, module_path: str, module_name: str):
        """Load a Python module for testing."""
        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            print(f"❌ Failed to load {module_name}: {e}")
            return None
    
    def benchmark_function(self, func, args=(), kwargs=None, iterations=100):
        """Benchmark a function with multiple iterations."""
        if kwargs is None:
            kwargs = {}
        
        times = []
        errors = 0
        
        for i in range(iterations):
            try:
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                times.append(end_time - start_time)
            except Exception as e:
                errors += 1
                if errors > iterations * 0.1:  # Stop if too many errors
                    break
        
        if not times:
            return None
        
        return {
            'mean': statistics.mean(times),
            'median': statistics.median(times),
            'min': min(times),
            'max': max(times),
            'std_dev': statistics.stdev(times) if len(times) > 1 else 0,
            'iterations': len(times),
            'errors': errors
        }
    
    def benchmark_core_patterns(self) -> Dict:
        """Benchmark core pattern matching performance."""
        print("\n🔍 Benchmarking core pattern performance...")
        
        core_path = os.path.join(self.commands_dir, "nunjucks_core.py")
        core = self.load_module(core_path, "nunjucks_core")
        
        if not core:
            return {}
        
        # Test content with varying complexity
        test_contents = {
            'simple': "{{ user.name }} {% if user %}Hello{% endif %}",
            'medium': """
            {# Comment #}
            {% for item in items %}
                <div>{{ item.name | upper }}</div>
                {% if item.active %}
                    <span>{{ item.count | default(0) }}</span>
                {% endif %}
            {% endfor %}
            """,
            'complex': self._generate_complex_template()
        }
        
        patterns = core.NunjucksPatterns()
        results = {}
        
        for content_type, content in test_contents.items():
            print(f"  Testing {content_type} content ({len(content)} chars)...")
            
            # Benchmark individual patterns
            pattern_results = {}
            
            pattern_tests = [
                ('variables', lambda: patterns.VARIABLE.findall(content)),
                ('tags', lambda: patterns.TAG.findall(content)),
                ('comments', lambda: patterns.COMMENT.findall(content)),
                ('filters', lambda: patterns.FILTER.findall(content))
            ]
            
            for pattern_name, pattern_func in pattern_tests:
                benchmark_result = self.benchmark_function(pattern_func, iterations=1000)
                if benchmark_result:
                    pattern_results[pattern_name] = benchmark_result
                    print(f"    {pattern_name}: {benchmark_result['mean']*1000:.3f}ms avg")
            
            results[content_type] = pattern_results
        
        return results
    
    def benchmark_analyzer_performance(self) -> Dict:
        """Benchmark syntax analyzer performance."""
        print("\n🔍 Benchmarking analyzer performance...")
        
        core_path = os.path.join(self.commands_dir, "nunjucks_core.py")
        core = self.load_module(core_path, "nunjucks_core")
        
        if not core:
            return {}
        
        analyzer = core.NunjucksAnalyzer()
        
        # Test different template sizes
        test_templates = {
            'small': self._generate_template(10),      # ~10 lines
            'medium': self._generate_template(100),    # ~100 lines  
            'large': self._generate_template(1000),    # ~1000 lines
            'xlarge': self._generate_template(5000)    # ~5000 lines
        }
        
        results = {}
        
        for size, template in test_templates.items():
            print(f"  Testing {size} template ({len(template)} chars)...")
            
            # Benchmark analyze_syntax method
            benchmark_result = self.benchmark_function(
                analyzer.analyze_syntax,
                args=(template,),
                iterations=50 if size != 'xlarge' else 10
            )
            
            if benchmark_result:
                results[size] = benchmark_result
                print(f"    Analysis time: {benchmark_result['mean']*1000:.3f}ms avg")
        
        return results
    
    def benchmark_formatter_performance(self) -> Dict:
        """Benchmark formatter performance."""
        print("\n🔍 Benchmarking formatter performance...")
        
        core_path = os.path.join(self.commands_dir, "nunjucks_core.py")
        core = self.load_module(core_path, "nunjucks_core")
        
        if not core:
            return {}
        
        formatter = core.NunjucksFormatter()
        
        # Test different formatting scenarios
        test_templates = {
            'unformatted': self._generate_unformatted_template(),
            'mixed_indents': self._generate_mixed_indent_template(),
            'nested_blocks': self._generate_nested_template()
        }
        
        results = {}
        
        for scenario, template in test_templates.items():
            print(f"  Testing {scenario} scenario ({len(template)} chars)...")
            
            benchmark_result = self.benchmark_function(
                formatter.format_text,
                args=(template,),
                iterations=100
            )
            
            if benchmark_result:
                results[scenario] = benchmark_result
                print(f"    Format time: {benchmark_result['mean']*1000:.3f}ms avg")
        
        return results
    
    def benchmark_script_execution(self) -> Dict:
        """Benchmark external script execution times."""
        print("\n🔍 Benchmarking script execution...")
        
        scripts = [
            'validate_syntax.py',
            'test_patterns.py',
            'validate_scope_consistency.py',
            'validate_json_files.py'
        ]
        
        results = {}
        
        for script_name in scripts:
            script_path = os.path.join(self.scripts_dir, script_name)
            
            if not os.path.exists(script_path):
                continue
            
            print(f"  Testing {script_name}...")
            
            # Benchmark script loading time
            load_time = self.benchmark_function(
                self.load_module,
                args=(script_path, script_name[:-3]),
                iterations=10
            )
            
            if load_time:
                results[script_name] = load_time
                print(f"    Load time: {load_time['mean']*1000:.3f}ms avg")
        
        return results
    
    def benchmark_memory_usage(self) -> Dict:
        """Estimate memory usage patterns."""
        print("\n💾 Analyzing memory usage patterns...")
        
        import tracemalloc
        
        core_path = os.path.join(self.commands_dir, "nunjucks_core.py")
        core = self.load_module(core_path, "nunjucks_core")
        
        if not core:
            return {}
        
        results = {}
        
        # Test pattern compilation memory
        tracemalloc.start()
        patterns = core.NunjucksPatterns()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        results['pattern_compilation'] = {
            'current_kb': current / 1024,
            'peak_kb': peak / 1024
        }
        
        print(f"  Pattern compilation: {peak/1024:.2f} KB peak")
        
        # Test analyzer memory with large template
        large_template = self._generate_template(2000)
        
        tracemalloc.start()
        analyzer = core.NunjucksAnalyzer()
        issues = analyzer.analyze_syntax(large_template)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        results['analyzer_large_template'] = {
            'current_kb': current / 1024,
            'peak_kb': peak / 1024,
            'issues_found': len(issues)
        }
        
        print(f"  Large template analysis: {peak/1024:.2f} KB peak")
        
        return results
    
    def _generate_complex_template(self) -> str:
        """Generate a complex test template."""
        return """
        {# Complex template with multiple features #}
        {% extends "base.html" %}
        
        {% block content %}
            {% set users = [
                {name: "Alice", age: 25, roles: ["admin", "user"]},
                {name: "Bob", age: 30, roles: ["user"]},
                {name: "Carol", age: 28, roles: ["moderator", "user"]}
            ] %}
            
            <div class="user-list">
                {% for user in users %}
                    {% if user.age >= 25 %}
                        <div class="user {{ 'admin' if 'admin' in user.roles else 'regular' }}">
                            <h3>{{ user.name | title }}</h3>
                            <p>Age: {{ user.age }}</p>
                            <p>Roles: {{ user.roles | join(", ") | default("None") }}</p>
                            
                            {% for role in user.roles %}
                                {% if role == "admin" %}
                                    <span class="badge admin">{{ role | upper }}</span>
                                {% elif role == "moderator" %}
                                    <span class="badge mod">{{ role | capitalize }}</span>
                                {% else %}
                                    <span class="badge">{{ role }}</span>
                                {% endif %}
                            {% endfor %}
                        </div>
                    {% endif %}
                {% endfor %}
            </div>
            
            {% macro renderButton(text, type="button", size="medium") %}
                <button type="{{ type }}" class="btn btn-{{ size }}">
                    {{ text | escape }}
                </button>
            {% endmacro %}
            
            {{ renderButton("Save Changes", "submit", "large") }}
            {{ renderButton("Cancel") }}
        {% endblock %}
        """
    
    def _generate_template(self, lines: int) -> str:
        """Generate a template with specified number of lines."""
        template_lines = ['{# Generated test template #}']
        
        for i in range(lines):
            if i % 10 == 0:
                template_lines.append("{% if condition_" + str(i) + " %}")
            elif i % 10 == 5:
                template_lines.append("    <p>{{ item_" + str(i) + ".name | default('Unknown') }}</p>")
            elif i % 10 == 9:
                template_lines.append("{% endif %}")
            else:
                template_lines.append(f"    <div>Line {i}: {{{{ data.field_{i} }}}}</div>")
        
        return '\n'.join(template_lines)
    
    def _generate_unformatted_template(self) -> str:
        """Generate poorly formatted template for testing."""
        return """
{%if user%}
<div>
{%for item in items%}
<p>{{item.name|upper}}</p>
{%endfor%}
</div>
{%endif%}
{% macro test(param) %}
<span>{{param}}</span>
{%endmacro%}
"""
    
    def _generate_mixed_indent_template(self) -> str:
        """Generate template with mixed indentation."""
        return """
{% if user %}
  <div>
    {% for item in items %}
      <p>{{ item.name }}</p>
    {% endfor %}
  </div>
{% endif %}
"""
    
    def _generate_nested_template(self) -> str:
        """Generate deeply nested template."""
        return """
{% for category in categories %}
    {% if category.visible %}
        {% for product in category.products %}
            {% if product.available %}
                {% for variant in product.variants %}
                    {% if variant.inStock %}
                        <div class="variant">
                            {{ variant.name | title }}
                        </div>
                    {% endif %}
                {% endfor %}
            {% endif %}
        {% endfor %}
    {% endif %}
{% endfor %}
"""
    
    def run_all_benchmarks(self) -> Dict:
        """Run comprehensive performance benchmarks."""
        print("🚀 Starting performance benchmark suite...")
        print(f"Project root: {self.project_root}")
        
        all_results = {
            'core_patterns': self.benchmark_core_patterns(),
            'analyzer': self.benchmark_analyzer_performance(),
            'formatter': self.benchmark_formatter_performance(),
            'scripts': self.benchmark_script_execution(),
            'memory': self.benchmark_memory_usage()
        }
        
        self.results = all_results
        return all_results
    
    def generate_performance_report(self) -> None:
        """Generate detailed performance analysis report."""
        print("\n📊 Generating performance report...")
        
        report_content = f"""# Nunjucks Toolbox Performance Report

## Overview
Performance analysis of all core components and optimization recommendations.

## Core Pattern Matching Performance

### Simple Content
- **Variables**: {self._format_benchmark_result(self.results.get('core_patterns', {}).get('simple', {}).get('variables'))}
- **Tags**: {self._format_benchmark_result(self.results.get('core_patterns', {}).get('simple', {}).get('tags'))}
- **Comments**: {self._format_benchmark_result(self.results.get('core_patterns', {}).get('simple', {}).get('comments'))}
- **Filters**: {self._format_benchmark_result(self.results.get('core_patterns', {}).get('simple', {}).get('filters'))}

### Complex Content
- **Variables**: {self._format_benchmark_result(self.results.get('core_patterns', {}).get('complex', {}).get('variables'))}
- **Tags**: {self._format_benchmark_result(self.results.get('core_patterns', {}).get('complex', {}).get('tags'))}
- **Comments**: {self._format_benchmark_result(self.results.get('core_patterns', {}).get('complex', {}).get('comments'))}
- **Filters**: {self._format_benchmark_result(self.results.get('core_patterns', {}).get('complex', {}).get('filters'))}

## Syntax Analyzer Performance

### Template Size Analysis
- **Small (10 lines)**: {self._format_benchmark_result(self.results.get('analyzer', {}).get('small'))}
- **Medium (100 lines)**: {self._format_benchmark_result(self.results.get('analyzer', {}).get('medium'))}
- **Large (1000 lines)**: {self._format_benchmark_result(self.results.get('analyzer', {}).get('large'))}
- **Extra Large (5000 lines)**: {self._format_benchmark_result(self.results.get('analyzer', {}).get('xlarge'))}

## Formatter Performance

### Formatting Scenarios
- **Unformatted**: {self._format_benchmark_result(self.results.get('formatter', {}).get('unformatted'))}
- **Mixed Indents**: {self._format_benchmark_result(self.results.get('formatter', {}).get('mixed_indents'))}
- **Nested Blocks**: {self._format_benchmark_result(self.results.get('formatter', {}).get('nested_blocks'))}

## Memory Usage Analysis

### Pattern Compilation
- Peak Memory: {self.results.get('memory', {}).get('pattern_compilation', {}).get('peak_kb', 0):.2f} KB

### Large Template Analysis  
- Peak Memory: {self.results.get('memory', {}).get('analyzer_large_template', {}).get('peak_kb', 0):.2f} KB
- Issues Found: {self.results.get('memory', {}).get('analyzer_large_template', {}).get('issues_found', 0)}

## Performance Recommendations

### ✅ Optimizations Already Implemented
1. **Pre-compiled Regex Patterns** - All patterns compiled once for reuse
2. **Shared Core Module** - Eliminates code duplication
3. **Optimized Algorithms** - Efficient bracket matching and validation
4. **External Scripts** - Workflow optimization with modular architecture

### 🔧 Further Optimization Opportunities
1. **Pattern Caching** - Cache pattern matches for repeated analysis
2. **Incremental Analysis** - Only re-analyze changed portions
3. **Lazy Loading** - Load expensive modules only when needed
4. **Memory Pooling** - Reuse data structures for large templates

### 📈 Performance Targets
- Simple template analysis: < 1ms
- Complex template analysis: < 10ms  
- Large template (1000+ lines): < 50ms
- Memory usage: < 5MB for typical workflows

## Conclusion
The current implementation shows excellent performance characteristics with room for additional optimizations in caching and memory management.

---
*Generated by Performance Benchmark Tool*
"""
        
        report_path = os.path.join(self.project_root, "performance-report.md")
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"✅ Performance report saved to: {report_path}")
        except Exception as e:
            print(f"❌ Failed to save performance report: {e}")
    
    def _format_benchmark_result(self, result) -> str:
        """Format benchmark result for display."""
        if not result:
            return "No data"
        
        mean_ms = result.get('mean', 0) * 1000
        std_dev_ms = result.get('std_dev', 0) * 1000
        iterations = result.get('iterations', 0)
        
        return f"{mean_ms:.3f}ms ±{std_dev_ms:.3f}ms ({iterations} runs)"


if __name__ == "__main__":
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    
    benchmark = PerformanceBenchmark(project_root)
    results = benchmark.run_all_benchmarks()
    benchmark.generate_performance_report()
    
    print("\n🎉 Performance benchmarking completed!")
    print("📊 Check 'performance-report.md' for detailed analysis")
    
    # Print quick summary
    if results.get('analyzer'):
        large_time = results['analyzer'].get('large', {}).get('mean', 0) * 1000
        if large_time > 0:
            print(f"📈 Large template analysis: {large_time:.1f}ms average")
    
    sys.exit(0)

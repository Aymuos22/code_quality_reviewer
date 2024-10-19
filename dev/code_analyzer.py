import ast
import tokenize
from io import BytesIO
import re
from radon.complexity import cc_visit

class CodeAnalyzer:
    def __init__(self, code):
        self.code = code
        self.tree = ast.parse(code)
        self.tokens = list(tokenize.tokenize(BytesIO(code.encode('utf-8')).readline))
    
    def count_lines_of_code(self):
        """Count total lines of code."""
        return len(self.code.splitlines())

    def calculate_cyclomatic_complexity(self):
        """Calculate cyclomatic complexity using radon."""
        complexities = cc_visit(self.code)
        total_complexity = sum(comp.complexity for comp in complexities)
        return total_complexity

    def count_functions_methods(self):
        """Count the number of functions and methods."""
        return sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in ast.walk(self.tree))

    def calculate_depth_of_inheritance(self):
        """Calculate depth of inheritance."""
        class_defs = [node for node in ast.walk(self.tree) if isinstance(node, ast.ClassDef)]
        max_depth = 0
        for class_def in class_defs:
            depth = 0
            for base in class_def.bases:
                if isinstance(base, ast.Name):
                    depth += 1
            max_depth = max(max_depth, depth)
        return max_depth

    def check_naming_conventions(self):
        """Check naming conventions for variables and functions."""
        good_conventions = 0
        total_names = 0

        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                total_names += 1
                if re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    good_conventions += 1
            elif isinstance(node, ast.Name):
                total_names += 1
                if re.match(r'^[a-z_][a-z0-9_]*$', node.id):
                    good_conventions += 1

        return good_conventions / total_names if total_names > 0 else 1

    def check_code_formatting(self):
        """Check code formatting according to PEP 8."""
        lines = self.code.splitlines()
        total_lines = len(lines)
        well_formatted_lines = 0

        for line in lines:
            if line.rstrip() != line or len(line) > 79:
                continue
            well_formatted_lines += 1

        return well_formatted_lines / total_lines if total_lines > 0 else 1

    def calculate_comment_density(self):
        """Calculate comment density."""
        code_lines = 0
        comment_lines = 0

        for token in self.tokens:
            if token.type == tokenize.COMMENT:
                comment_lines += 1
            elif token.type == tokenize.NL or token.type == tokenize.NEWLINE:
                code_lines += 1

        return comment_lines / code_lines if code_lines > 0 else 0

    def analyze(self):
        """Analyze the code and return all metrics."""
        return {
            'lines_of_code': self.count_lines_of_code(),
            'cyclomatic_complexity': self.calculate_cyclomatic_complexity(),
            'num_functions_methods': self.count_functions_methods(),
            'depth_of_inheritance': self.calculate_depth_of_inheritance(),
            'naming_conventions': self.check_naming_conventions(),
            'code_formatting': self.check_code_formatting(),
            'comment_density': self.calculate_comment_density(),
        }

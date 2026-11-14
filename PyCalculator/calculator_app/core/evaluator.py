"""Restricted arithmetic expression evaluator (does not use eval)."""
import ast
import operator


class SafeEvaluator(ast.NodeVisitor):
    """Evaluate a small, explicit subset of Python arithmetic syntax."""
    OPS = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.Mod: operator.mod,
        ast.UAdd: operator.pos, ast.USub: operator.neg,
    }

    def visit_Expression(self, node):
        return self.visit(node.body)

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise ValueError("Invalid number")

    def visit_BinOp(self, node):
        op_type = type(node.op)
        if op_type not in self.OPS:
            raise ValueError("Unsupported operator")
        left, right = self.visit(node.left), self.visit(node.right)
        if op_type is ast.Pow and abs(right) > 8:
            raise ValueError("Exponent too large")
        result = self.OPS[op_type](left, right)
        if abs(result) > 10**15:
            raise ValueError("Result too large")
        return result

    def visit_UnaryOp(self, node):
        op_type = type(node.op)
        if op_type not in self.OPS:
            raise ValueError("Unsupported operator")
        return self.OPS[op_type](self.visit(node.operand))

    def generic_visit(self, node):
        raise ValueError("Invalid expression")


def evaluate(expression):
    """Parse and evaluate an arithmetic expression using the safe visitor."""
    return SafeEvaluator().visit(ast.parse(expression, mode="eval"))

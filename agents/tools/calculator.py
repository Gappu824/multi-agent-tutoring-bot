# multi_agent_tutor/agents/tools/calculator.py
import ast
import operator as op

# Supported operators
OPERATORS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
    ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
    ast.USub: op.neg
}

def eval_expr(node):
    """
    Safely evaluates an arithmetic expression node.
    Source: Adapted from a common pattern for safe eval.
    """
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        return OPERATORS[type(node.op)](eval_expr(node.left), eval_expr(node.right))
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        return OPERATORS[type(node.op)](eval_expr(node.operand))
    else:
        raise TypeError(node)

def simple_calculator(expression: str) -> str:
    """
    A safer calculator that evaluates basic arithmetic expressions.
    Supports +, -, *, /, ** (power).
    Example: "2 * 5 + (3 - 1) / 2 ** 2"
    """
    try:
        # Parse the expression into an AST node
        node = ast.parse(expression, mode='eval').body
        result = eval_expr(node)
        return str(result)
    except (TypeError, SyntaxError, KeyError, ZeroDivisionError) as e:
        return f"Error: Could not evaluate expression. Invalid format, unsupported operation, or division by zero. ({str(e)})"
    except Exception as e:
        return f"Error: An unexpected error occurred during calculation. {str(e)}"

# Example Usage (for testing)
if __name__ == "__main__":
    print(f"'10 + 5 * 2': {simple_calculator('10 + 5 * 2')}")
    print(f"'10 / 0': {simple_calculator('10 / 0')}")
    print(f"'(2 + 3) * (7 - 2) / 5': {simple_calculator('(2 + 3) * (7 - 2) / 5')}")
    print(f"'2**3': {simple_calculator('2**3')}")
    print(f"'sqrt(9)': {simple_calculator('sqrt(9)')}")
    print(f"'os.system(\"clear\")': {simple_calculator('os.system(\"clear\")')}")
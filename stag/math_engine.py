"""Safe spoken-arithmetic normalization and evaluation for Stag."""
import ast
import math
import re

class MathNormalizer:
    """Normalize spoken arithmetic and evaluate it with a strict AST allowlist."""
    REPLACEMENTS = {
        "multiplied by":"*", "divided by":"/", "to the power of":"**",
        "square root of":"math.sqrt(", "cube root of":"math.cbrt(",
        "factorial of":"math.factorial(", "percent of":"/100*",
        "squared":"**2", "cubed":"**3", "plus":"+", "minus":"-",
        "times":"*", "over":"/", "modulo":"%", "mod":"%",
        "percent":"/100", "pi":"math.pi", "e":"math.e", "x":"*",
    }
    WORD_NUMBERS = {
        "zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,
        "seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,
        "thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,
        "eighteen":18,"nineteen":19,"twenty":20,"thirty":30,"forty":40,
        "fifty":50,"sixty":60,"seventy":70,"eighty":80,"ninety":90,
        "hundred":100,"thousand":1000,
    }

    @classmethod
    def _replace_word_numbers(cls, expression):
        tokens, output, index = expression.split(), [], 0
        while index < len(tokens):
            if tokens[index] not in cls.WORD_NUMBERS:
                output.append(tokens[index]); index += 1; continue
            total = current = 0
            while index < len(tokens) and tokens[index] in cls.WORD_NUMBERS:
                value = cls.WORD_NUMBERS[tokens[index]]
                if value == 100: current = max(current, 1) * 100
                elif value == 1000: total += max(current, 1) * 1000; current = 0
                else: current += value
                index += 1
            output.append(str(total + current))
        return " ".join(output)

    @classmethod
    def normalize(cls, expr):
        """Convert spoken math into a compact expression for safe_eval()."""
        if not isinstance(expr, str): raise TypeError("Math expression must be text")
        expr = cls._replace_word_numbers(expr.lower().strip())
        for phrase, symbol in sorted(cls.REPLACEMENTS.items(), key=lambda item: -len(item[0])):
            expr = re.sub(rf"\b{re.escape(phrase)}\b", lambda _m, v=symbol: v, expr)
        expr = re.sub(r"\s+", "", expr)
        if expr.count("(") > expr.count(")"):
            expr += ")" * (expr.count("(") - expr.count(")"))
        return expr

    @classmethod
    def safe_eval(cls, expr):
        """Evaluate arithmetic without eval(), builtins, or arbitrary calls."""
        if not isinstance(expr, str) or not expr.strip(): raise ValueError("Empty expression")
        if len(expr) > 256: raise ValueError("Expression is too long")
        try: tree = ast.parse(expr, mode="eval")
        except (SyntaxError, ValueError) as exc: raise ValueError(f"Invalid math expression: {exc}") from exc
        if sum(1 for _ in ast.walk(tree)) > 64: raise ValueError("Expression is too complex")
        binary = {
            ast.Add:lambda a,b:a+b, ast.Sub:lambda a,b:a-b, ast.Mult:lambda a,b:a*b,
            ast.Div:lambda a,b:a/b, ast.FloorDiv:lambda a,b:a//b, ast.Mod:lambda a,b:a%b,
            ast.Pow:lambda a,b:a**b,
        }
        unary = {ast.UAdd:lambda x:+x, ast.USub:lambda x:-x}
        def checked(value):
            if isinstance(value,bool) or not isinstance(value,(int,float)): raise ValueError("Only numeric results are allowed")
            try: finite=math.isfinite(value)
            except (OverflowError,TypeError): finite=False
            if not finite or abs(value)>1e100: raise ValueError("Result is outside the supported range")
            return value
        def visit(node):
            if isinstance(node,ast.Expression): return visit(node.body)
            if isinstance(node,ast.Constant):
                if type(node.value) not in (int,float): raise ValueError("Only numeric literals are allowed")
                return checked(node.value)
            if isinstance(node,ast.BinOp):
                op=binary.get(type(node.op))
                if op is None: raise ValueError("Operator is not allowed")
                left,right=visit(node.left),visit(node.right)
                if isinstance(node.op,ast.Pow) and abs(right)>100: raise ValueError("Exponent is too large")
                return checked(op(left,right))
            if isinstance(node,ast.UnaryOp):
                op=unary.get(type(node.op))
                if op is None: raise ValueError("Unary operator is not allowed")
                return checked(op(visit(node.operand)))
            if isinstance(node,ast.Attribute):
                if isinstance(node.value,ast.Name) and node.value.id=="math" and node.attr in ("pi","e"):
                    return getattr(math,node.attr)
                raise ValueError("Math attribute is not allowed")
            if isinstance(node,ast.Call):
                if node.keywords: raise ValueError("Keyword arguments are not allowed")
                if isinstance(node.func,ast.Name) and node.func.id in ("abs","round"):
                    function=abs if node.func.id=="abs" else round
                    allowed=(1,) if node.func.id=="abs" else (1,2)
                    if len(node.args) not in allowed: raise ValueError("Invalid function arguments")
                elif (isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name)
                      and node.func.value.id=="math" and node.func.attr in ("sqrt","cbrt","factorial")):
                    function=getattr(math,node.func.attr,None)
                    if function is None or len(node.args)!=1: raise ValueError("Unsupported math function")
                else: raise ValueError("Function call is not allowed")
                args=[visit(arg) for arg in node.args]
                if isinstance(node.func,ast.Attribute) and node.func.attr=="factorial":
                    value=args[0]
                    if not isinstance(value,int) or value<0 or value>170:
                        raise ValueError("factorial() requires an integer from 0 to 170")
                return checked(function(*args))
            raise ValueError(f"Expression element is not allowed: {type(node).__name__}")
        try: return visit(tree)
        except ValueError: raise
        except Exception as exc: raise ValueError(f"Could not evaluate expression: {exc}") from exc



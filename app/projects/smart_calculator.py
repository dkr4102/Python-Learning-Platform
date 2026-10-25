"""
Project 1: Smart Calculator
Performs arithmetic, percentage discounts, and scientific calculations with comprehensive validation.
"""
import math
from typing import Dict, Any, Union

def calculate(op: str, num1: float, num2: float = 0.0) -> Dict[str, Any]:
    """
    Execute mathematical operations with guardrails.
    Returns: {"success": bool, "result": float, "formatted": str, "error": str}
    """
    try:
        if op == "+":
            res = num1 + num2
            return {"success": True, "result": res, "formatted": f"{num1} + {num2} = {res:g}", "error": ""}
        elif op == "-":
            res = num1 - num2
            return {"success": True, "result": res, "formatted": f"{num1} - {num2} = {res:g}", "error": ""}
        elif op == "*":
            res = num1 * num2
            return {"success": True, "result": res, "formatted": f"{num1} × {num2} = {res:g}", "error": ""}
        elif op == "/":
            if num2 == 0:
                return {"success": False, "result": 0.0, "formatted": "", "error": "ZeroDivisionError: Division by zero is undefined in mathematics."}
            res = num1 / num2
            return {"success": True, "result": res, "formatted": f"{num1} ÷ {num2} = {res:.6g}", "error": ""}
        elif op == "//":
            if num2 == 0:
                return {"success": False, "result": 0.0, "formatted": "", "error": "ZeroDivisionError: Integer division by zero is undefined."}
            res = num1 // num2
            return {"success": True, "result": res, "formatted": f"{num1} // {num2} = {res:g}", "error": ""}
        elif op == "%":
            if num2 == 0:
                return {"success": False, "result": 0.0, "formatted": "", "error": "ZeroDivisionError: Modulo by zero is undefined."}
            res = num1 % num2
            return {"success": True, "result": res, "formatted": f"{num1} % {num2} = {res:g}", "error": ""}
        elif op == "^" or op == "**":
            res = num1 ** num2
            return {"success": True, "result": res, "formatted": f"{num1}^{num2} = {res:g}", "error": ""}
        elif op == "sqrt":
            if num1 < 0:
                return {"success": False, "result": 0.0, "formatted": "", "error": "ValueError: Square root of a negative number is undefined in real numbers."}
            res = math.sqrt(num1)
            return {"success": True, "result": res, "formatted": f"√({num1}) = {res:.6g}", "error": ""}
        elif op == "discount":
            # num1 is price, num2 is discount percentage (e.g. 15%)
            discount_amount = (num1 * num2) / 100.0
            final_price = num1 - discount_amount
            return {
                "success": True,
                "result": final_price,
                "formatted": f"Base: ${num1:.2f} | Discount ({num2}%): -${discount_amount:.2f} | Final: ${final_price:.2f}",
                "error": ""
            }
        else:
            return {"success": False, "result": 0.0, "formatted": "", "error": f"Unknown operator '{op}'."}
    except Exception as e:
        return {"success": False, "result": 0.0, "formatted": "", "error": str(e)}

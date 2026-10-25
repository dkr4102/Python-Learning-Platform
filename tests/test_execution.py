"""
Tests for Python isolated subprocess code execution and security guardrails.
"""
from app.execution.runner import run_python_code
from app.execution.evaluator import evaluate_exercise

def test_safe_execution_stdout():
    code = "print('Hello from Pip Learn')"
    res = run_python_code(code)
    assert res["success"] is True
    assert res["stdout"].strip() == "Hello from Pip Learn"
    assert res["exit_code"] == 0
    assert res["elapsed_ms"] > 0

def test_timeout_protection():
    # Infinite loop must be terminated cleanly
    code = "while True: pass"
    res = run_python_code(code, timeout_sec=1.5)
    assert res["success"] is False
    assert res["timeout"] is True
    assert "Timed Out" in res["stderr"]

def test_security_violation_rejection():
    dangerous_code = "import os; os.system('ls -la')"
    res = run_python_code(dangerous_code)
    assert res["success"] is False
    assert res["security_violation"] is True
    assert "Security restriction" in res["stderr"]

def test_syntax_error_explanation():
    bad_code = "if True\n    print('Missing colon')"
    res = run_python_code(bad_code)
    assert res["success"] is False
    assert "Syntax Error" in res["explanation"]

def test_exercise_evaluator_matching():
    learner_code = "celsius = 37.0; fahrenheit = (celsius * 9/5) + 32; print(f'{celsius:.1f} C = {fahrenheit:.1f} F')"
    test_cases = [{"input": "", "expected_output": "37.0 C = 98.6 F", "description": "Temp check"}]
    res = evaluate_exercise(learner_code, test_cases, expected_substrings=["celsius", "fahrenheit"])
    assert res["passed"] is True
    assert len(res["test_results"]) == 1
    assert res["test_results"][0]["passed"] is True

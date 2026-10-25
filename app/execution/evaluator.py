"""
Exercise evaluator for validating learner code against expected test cases and criteria.
"""
from typing import Dict, Any, List
from app.execution.runner import run_python_code

def evaluate_exercise(
    learner_code: str,
    test_cases: List[Dict[str, Any]],
    expected_substrings: List[str] = None
) -> Dict[str, Any]:
    """
    Evaluate learner code against test cases.
    Each test case can specify:
        input: str (optional input data)
        expected_output: str (expected stdout or part of stdout)
        description: str
    """
    if expected_substrings:
        for substr in expected_substrings:
            if substr not in learner_code:
                return {
                    "passed": False,
                    "message": f"Code must include: `{substr}`",
                    "details": f"Your solution is expected to utilize or define '{substr}'.",
                    "test_results": []
                }

    results = []
    all_passed = True

    # If test cases are provided, execute each
    if test_cases:
        for idx, tc in enumerate(test_cases, 1):
            inp = tc.get("input", "")
            expected = tc.get("expected_output", "").strip()
            desc = tc.get("description", f"Test Case {idx}")

            exec_res = run_python_code(learner_code, timeout_sec=3.0, input_data=inp)
            actual = exec_res["stdout"].strip()

            passed = exec_res["success"] and (expected in actual if expected else True)
            if not passed:
                all_passed = False

            results.append({
                "case_index": idx,
                "description": desc,
                "passed": passed,
                "expected": expected,
                "actual": actual,
                "error": exec_res["stderr"]
            })
    else:
        # Default run check
        exec_res = run_python_code(learner_code, timeout_sec=3.0)
        all_passed = exec_res["success"]
        results.append({
            "case_index": 1,
            "description": "Standard Execution",
            "passed": all_passed,
            "actual": exec_res["stdout"].strip(),
            "error": exec_res["stderr"]
        })

    return {
        "passed": all_passed,
        "message": "All test assertions passed successfully!" if all_passed else "Some assertions did not match expectations.",
        "test_results": results
    }

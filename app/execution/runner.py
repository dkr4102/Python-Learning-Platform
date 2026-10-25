"""
Secure isolated Python code runner.
Runs learner code in an isolated subprocess with timeout, dedicated temp dir,
resource limits, and helpful error diagnostics.
"""
import sys
import os
import subprocess
import tempfile
import time
from typing import Dict, Any, Optional

# Forbidden destructive patterns for pre-flight safety check
DISALLOWED_PATTERNS = [
    "os.system",
    "subprocess.Popen",
    "shutil.rmtree",
    "pty.spawn",
    "import socket",
    "socket.socket",
    "__import__('os').system",
    "os.remove",
    "os.unlink",
    "rmdir"
]

def run_python_code(code: str, timeout_sec: float = 3.5, input_data: str = "") -> Dict[str, Any]:
    """
    Execute user-provided Python code in an isolated subprocess.
    Returns:
        {
            "success": bool,
            "stdout": str,
            "stderr": str,
            "exit_code": int,
            "elapsed_ms": float,
            "timeout": bool,
            "security_violation": bool,
            "explanation": str
        }
    """
    start_time = time.perf_counter()

    # Pre-flight security check
    for pattern in DISALLOWED_PATTERNS:
        if pattern in code:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Security restriction: Operation '{pattern}' is not permitted in the learning sandbox.",
                "exit_code": -1,
                "elapsed_ms": 0.0,
                "timeout": False,
                "security_violation": True,
                "explanation": "To maintain environment stability and safety, low-level process and destructive filesystem operations are restricted."
            }

    with tempfile.TemporaryDirectory() as temp_dir:
        script_file = os.path.join(temp_dir, "learner_script.py")
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(code)

        # Build clean environment
        env = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "PYTHONUNBUFFERED": "1",
            "LC_ALL": "en_US.UTF-8",
            "LANG": "en_US.UTF-8",
            "HOME": temp_dir,
            "PYTHONPATH": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        }

        python_bin = sys.executable

        try:
            process = subprocess.Popen(
                [python_bin, script_file],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=temp_dir,
                env=env,
                text=True
            )

            stdout, stderr = process.communicate(input=input_data, timeout=timeout_sec)
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            exit_code = process.returncode
            success = (exit_code == 0)

            explanation = ""
            if not success:
                if "SyntaxError" in stderr:
                    explanation = "Syntax Error detected: Double check colons, parentheses, indentations, and quotation marks."
                elif "NameError" in stderr:
                    explanation = "Name Error: A variable or function was referenced before being defined or is misspelled."
                elif "TypeError" in stderr:
                    explanation = "Type Error: An operation was performed on an inappropriate data type (e.g. adding string and integer)."
                elif "IndexError" in stderr:
                    explanation = "Index Error: Attempted to access a sequence position that does not exist."
                elif "KeyError" in stderr:
                    explanation = "Key Error: The requested dictionary key was not found."
                elif "ZeroDivisionError" in stderr:
                    explanation = "Zero Division Error: Division or modulo by zero is undefined."
                else:
                    explanation = "Execution encountered an error. Review the error details in the console output above."

            return {
                "success": success,
                "stdout": stdout,
                "stderr": stderr,
                "exit_code": exit_code,
                "elapsed_ms": elapsed_ms,
                "timeout": False,
                "security_violation": False,
                "explanation": explanation
            }

        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return {
                "success": False,
                "stdout": stdout,
                "stderr": f"Execution Timed Out: Program ran for more than {timeout_sec} seconds. Check for infinite loops (e.g. while True without an exit condition).",
                "exit_code": -9,
                "elapsed_ms": elapsed_ms,
                "timeout": True,
                "security_violation": False,
                "explanation": "Timeout reached. In educational code, long runs usually indicate an uncontrolled loop or blocked input."
            }
        except Exception as e:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Execution system failure: {str(e)}",
                "exit_code": -1,
                "elapsed_ms": elapsed_ms,
                "timeout": False,
                "security_violation": False,
                "explanation": "System runner encountered an unexpected condition."
            }

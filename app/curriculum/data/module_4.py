"""
Module 4: File Handling and Exception Handling
Marwadi University 01AP0303 - Unit 4 (6 Contact Hours, 12 Marks Assessment)
Mini-Project: Log File Analyzer
"""
from app.curriculum.models import Module, Lesson, PracticeExercise, QuizQuestion, ProjectInfo, CommonMistake, MiniCheckpoint

MODULE_4 = Module(
    id=4,
    code="MOD-04",
    title="File Handling and Exception Handling",
    syllabus_unit="Unit 4: File I/O, Context Managers & Exception Architecture",
    contact_hours=6,
    assessment_marks=12,
    description="Learn production file persistence, text and CSV streams, deterministic resource cleanup with context managers, custom exception hierarchies, and diagnostic Python logging.",
    learning_objectives=[
        "Read and write text and CSV files safely using context managers (with open)",
        "Control file cursor positioning with seek() and tell()",
        "Construct resilient try, except, else, and finally exception blocks",
        "Author domain-specific custom exception classes inheriting from Exception",
        "Implement diagnostic application logging across standard severity levels"
    ],
    topics_covered=[
        "File Modes: Read ('r'), Write ('w'), Append ('a'), Binary ('b')",
        "Deterministic Cleanup with Context Managers (with statement)",
        "File Pointer Manipulation: seek() and tell()",
        "CSV File Processing with the csv Module",
        "The Exception Hierarchy & Multi-Catch Blocks",
        "The complete try / except / else / finally lifecycle",
        "Custom User-Defined Exception Classes",
        "Application Logging (logging module, levels, handlers)"
    ],
    artwork_id="ART-08",
    project=ProjectInfo(
        id="proj-log-analyzer",
        title="Log File Analyzer",
        subtitle="Server Telemetry Parser, Error Rate Classifier & Audit Generator",
        objective="Build an automated log inspection engine that parses structured system logs, categorizes entries by severity (INFO, WARNING, ERROR, CRITICAL), identifies recurring fault signatures, and outputs an audit report.",
        requirements=[
            "Parse timestamp, log level, component name, and log message from raw text",
            "Handle malformed log lines gracefully without crashing using try-except",
            "Calculate summary statistics (total events, count per severity, error percentage)",
            "Detect and highlight critical error messages for administrator triage",
            "Export an itemized audit summary report"
        ],
        starter_snippet="""# Module 4 Project: Log File Analyzer
SAMPLE_LOG = '''
2026-10-24 10:15:02 [INFO] Auth: User 102 logged in successfully.
2026-10-24 10:15:30 [WARNING] Storage: Disk usage exceeded 85%.
2026-10-24 10:16:12 [ERROR] Database: Connection pool exhausted.
2026-10-24 10:17:05 [CRITICAL] PaymentGateway: Transaction timeout on order 4091.
'''

def analyze_logs(log_text):
    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}
    for line in log_text.strip().split('\\n'):
        for lvl in counts:
            if f"[{lvl}]" in line:
                counts[lvl] += 1
    return counts
""",
        module_id=4
    ),
    lessons=[
        Lesson(
            id="m4-l1",
            title="File I/O & The Context Manager (with)",
            subtitle="Deterministic resource release and standard file access modes.",
            reading_time_min=7,
            concept_markdown="""### Safe File Operations in Python

Every operating system has a limit on the number of file descriptors a program can hold open simultaneously. If you open a file and an exception occurs before `.close()`, the file descriptor leaks and the file lock may remain held.

#### The Context Manager (`with` Statement)
Python provides the **`with` statement**, which guarantees that the file is closed automatically as soon as execution leaves the block—even if an unhandled exception or return statement occurs!

```python
# The Pythonic standard:
with open("report.txt", "w", encoding="utf-8") as f:
    f.write("Line 1: University Report\\n")
    f.write("Line 2: 01AP0303 Python\\n")
# File is guaranteed closed here!
```

#### File Modes:
- `'r'`: Read (default). Raises `FileNotFoundError` if file is missing.
- `'w'`: Write. Truncates/overwrites file if it exists, creates it if not.
- `'a'`: Append. Preserves existing contents and writes to the end.
- `'r+'`: Read and write simultaneously.
- `'b'`: Binary mode (e.g. `'rb'`, `'wb'`) for images and serialized bytes.
""",
            syntax_example="""# Reading lines into a list
with open("demo.txt", "w") as f:
    f.write("First Line\\nSecond Line\\nThird Line\\n")

with open("demo.txt", "r") as f:
    for line_num, content in enumerate(f, 1):
        print(f"Line {line_num}: {content.strip()}")
""",
            executable_code="""# Executable file writing and reading in memory
import tempfile
import os

with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
    tmp.write("Marwadi University\\nCourse: 01AP0303\\nUnit 4: File Handling\\n")
    tmp_path = tmp.name

try:
    with open(tmp_path, "r") as reader:
        lines = [line.strip() for line in reader]
    print(f"Successfully read {len(lines)} lines:")
    for line in lines:
        print(" ->", line)
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
""",
            expected_output="""Successfully read 3 lines:
 -> Marwadi University
 -> Course: 01AP0303
 -> Unit 4: File Handling""",
            output_explanation="Using tempfile ensures a clean temporary file is created, written with the context manager, read back safely, and deleted in the finally block.",
            common_mistakes=[
                CommonMistake(
                    mistake="Using raw open() without a with block: f = open('data.txt', 'w'); f.write('hi')",
                    explanation="If an exception occurs during write, the file descriptor remains locked and data in the OS buffer may never flush to disk.",
                    correction="Always wrap file access in a `with open(...) as f:` block."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="Why is using `with open(...)` preferred over manually calling `open()` and `close()`?",
                options=[
                    "It makes the file read faster",
                    "It automatically guarantees file closure even if an exception is raised",
                    "It encrypts the file on disk",
                    "It is the only way Python allows writing files"
                ],
                correct_index=1,
                explanation="Context managers guarantee that the `__exit__` method closes the file resource deterministically."
            )
        ),
        Lesson(
            id="m4-l2",
            title="File Cursor: seek() and tell()",
            subtitle="Navigating byte and character offsets within file streams.",
            reading_time_min=5,
            concept_markdown="""### File Stream Offsets

When reading or writing files, the operating system maintains an internal **cursor position** pointing to the byte where the next I/O operation will occur:

- `f.tell()`: Returns the current cursor position as an integer (byte offset).
- `f.seek(offset, whence)`: Repositions the file cursor.

#### Whence Parameters:
- `0` (default): Absolute offset from the beginning of the file.
- `1`: Relative offset from the current cursor position.
- `2`: Relative offset from the end of the file (requires binary mode `'rb'`).
""",
            syntax_example="""# Resetting cursor to start
with open("data.txt", "w+") as f:
    f.write("ABCDEFGHIJ")
    print("Cursor at end:", f.tell())  # 10
    f.seek(0)  # Rewind to beginning
    print("Read after rewind:", f.read(5))  # 'ABCDE'
""",
            executable_code="""# Executable seek and tell demonstration
import tempfile
import os

with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
    tmp.write("0123456789ABCDEF")
    tmp_path = tmp.name

try:
    with open(tmp_path, "r") as f:
        print("Initial position:", f.tell())
        chunk1 = f.read(5)
        print("Read 5 chars:", chunk1, "| Position now:", f.tell())
        f.seek(10)
        print("Repositioned to offset 10. Position now:", f.tell())
        chunk2 = f.read(6)
        print("Read next 6 chars:", chunk2)
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
""",
            expected_output="""Initial position: 0
Read 5 chars: 01234 | Position now: 5
Repositioned to offset 10. Position now: 10
Read next 6 chars: ABCDEF""",
            output_explanation="f.seek(10) immediately moves the file pointer to byte index 10, enabling arbitrary jumps within the stream.",
            common_mistakes=[
                CommonMistake(
                    mistake="Using relative whence values (1 or 2) in standard text mode on non-zero offsets",
                    explanation="In text mode, Python only allows seeking relative to the start (0) or seeking to offset 0 from the end.",
                    correction="Open the file in binary mode ('rb') if you require arbitrary relative seek offsets."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What does calling `f.seek(0)` do on an open file object?",
                options=[
                    "Erases the first character",
                    "Rewinds the file cursor back to the beginning of the file",
                    "Closes the file",
                    "Calculates the file size"
                ],
                correct_index=1,
                explanation="f.seek(0) repositions the file stream pointer to offset 0 (the start)."
            )
        ),
        Lesson(
            id="m4-l3",
            title="Exception Architecture: try, except, else, finally",
            subtitle="The complete fault-tolerant error lifecycle in production Python.",
            reading_time_min=7,
            concept_markdown="""### The Complete Exception Lifecycle

In Python, errors during runtime are represented as exception objects. Handling them cleanly prevents applications from abruptly crashing.

```
       +------------------------------------+
       |              try:                  |
       |  Code that might raise an error    |
       +-----------------+------------------+
                         |
           +-------------+-------------+
           | Exception?                | No Exception?
           v                           v
+----------------------+     +----------------------+
|       except:        |     |        else:         |
| Error recovery logic |     | Runs ONLY on success |
+----------+-----------+     +----------+-----------+
           |                            |
           +-------------+--------------+
                         |
                         v
              +----------------------+
              |       finally:       |
              | ALWAYS runs clean-up |
              +----------------------+
```

#### Structure and Rules:
1. `try`: Wrap vulnerable statements (e.g. file access, parsing, division).
2. `except SpecificError as e`: Catch specific error types. Always avoid bare `except:`!
3. `else`: Executes **only if no exception was raised** in the try block.
4. `finally`: Executes unconditionally, regardless of whether an error occurred, was caught, or was re-raised. Ideal for closing network sockets or database connections.
""",
            syntax_example="""# Complete 4-clause exception handling
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError as err:
        print(f"Handled error: {err}")
        return None
    except TypeError:
        print("Inputs must be numbers!")
        return None
    else:
        print("Calculation successful!")
        return result
    finally:
        print("Operation concluded.")

print(safe_divide(10, 2))
""",
            executable_code="""# Executable try-except-else-finally demo
def parse_integer_ratio(numerator_str, denominator_str):
    try:
        num = int(numerator_str)
        den = int(denominator_str)
        ratio = num / den
    except ValueError as val_err:
        return f"Conversion Error: {val_err}"
    except ZeroDivisionError:
        return "Math Error: Denominator cannot be zero."
    else:
        return f"Ratio computed successfully: {ratio:.4f}"
    finally:
        pass  # Cleanup hook

print(parse_integer_ratio("100", "4"))
print(parse_integer_ratio("100", "0"))
print(parse_integer_ratio("abc", "4"))
""",
            expected_output="""Ratio computed successfully: 25.0000
Math Error: Denominator cannot be zero.
Conversion Error: invalid literal for int() with base 10: 'abc'""",
            output_explanation="Different exception blocks intercept distinct runtime failures (ZeroDivisionError vs ValueError) while preserving program stability.",
            common_mistakes=[
                CommonMistake(
                    mistake="Catching `except Exception:` blindly and ignoring it with `pass`",
                    explanation="A silent broad catch hides bugs, syntax errors, and KeyboardInterrupt, making debugging impossible.",
                    correction="Catch specific exception types, log the exception traceback, and handle the failure gracefully."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="Under what condition does the `else:` block of a `try...except...else...finally` statement run?",
                options=[
                    "Whenever an exception is caught by except",
                    "Only if the try block executes without raising any exception",
                    "On every execution, right before finally",
                    "Only when an exception cannot be handled"
                ],
                correct_index=1,
                explanation="The `else` clause in exception handling runs only when the `try` block completes successfully without any exception."
            )
        ),
        Lesson(
            id="m4-l4",
            title="Custom Exceptions & Error Hierarchies",
            subtitle="Creating domain-specific exceptions inheriting from Exception.",
            reading_time_min=6,
            concept_markdown="""### Domain-Specific Custom Exceptions

In professional software development, built-in exceptions like `ValueError` are often too generic to communicate specific domain business logic violations.

By subclassing Python's base `Exception`, you can establish a clear, structured error taxonomy for your application:

```python
# Base application error
class PipLearnError(Exception):
    '''Base exception for all Pip Learn domain errors.'''
    pass

class InsufficientBalanceError(PipLearnError):
    def __init__(self, current_balance, requested_amount):
        self.balance = current_balance
        self.requested = requested_amount
        super().__init__(
            f"Cannot withdraw ${requested_amount:.2f}; available balance is only ${current_balance:.2f}."
        )

class InvalidCourseCodeError(PipLearnError):
    pass
```
""",
            syntax_example="""# Raising and catching custom domain exceptions
def validate_enrollment(course_code):
    if not course_code.startswith("01AP"):
        raise InvalidCourseCodeError(f"'{course_code}' is not a valid Marwadi University engineering course code.")
    return True
""",
            executable_code="""# Executable custom exception demonstration
class ApplicationError(Exception):
    pass

class NegativeValueError(ApplicationError):
    def __init__(self, value, field_name):
        self.value = value
        self.field_name = field_name
        super().__init__(f"Field '{field_name}' cannot be negative (received: {value})")

def set_employee_salary(name, salary):
    if salary < 0:
        raise NegativeValueError(salary, "base_salary")
    return f"Employee {name} salary recorded: ${salary:,.2f}"

try:
    print(set_employee_salary("Aarav", 55000))
    print(set_employee_salary("Rohan", -1200))
except NegativeValueError as err:
    print(f"Validation Failure Caught: {err}")
""",
            expected_output="""Employee Aarav salary recorded: $55,000.00
Validation Failure Caught: Field 'base_salary' cannot be negative (received: -1200)""",
            output_explanation="NegativeValueError cleanly captures domain error semantics, storing relevant attributes and formatting a descriptive error message.",
            common_mistakes=[
                CommonMistake(
                    mistake="Inheriting custom exceptions directly from `BaseException`",
                    explanation="BaseException is reserved for system exits like KeyboardInterrupt and SystemExit. Normal exceptions must inherit from `Exception`.",
                    correction="Always subclass `Exception` (or a subclass thereof) for custom errors."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What class should your custom domain exception inherit from in standard Python?",
                options=["BaseException", "Exception", "RuntimeErrorOnly", "object"],
                correct_index=1,
                explanation="Standard custom exceptions should always inherit from `Exception`."
            )
        ),
        Lesson(
            id="m4-l5",
            title="Python Logging & Telemetry",
            subtitle="Diagnostic logging with DEBUG, INFO, WARNING, ERROR, and CRITICAL.",
            reading_time_min=6,
            concept_markdown="""### The Python `logging` Standard Library

Using `print()` for debugging in production is hazardous: print statements cannot easily be routed to files, cannot be filtered by severity levels, and lack timestamps and contextual metadata.

#### Standard Logging Severity Levels:
1. `DEBUG` (10): Detailed diagnostic information for developers.
2. `INFO` (20): Confirmation that events are proceeding as expected.
3. `WARNING` (30): An indication of an unexpected event or impending resource constraint (e.g. disk low).
4. `ERROR` (40): A failure in a specific operation; application continues running.
5. `CRITICAL` (50): Severe error; the application may be unable to continue.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("PipLearn")
logger.info("System initialized successfully.")
logger.warning("Network latency higher than 200ms.")
```
""",
            syntax_example="""# Basic logging setup
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("AuthService")
log.info("User session verified.")
""",
            executable_code="""# Executable logging demonstration
import logging
import io

log_stream = io.StringIO()
handler = logging.StreamHandler(log_stream)
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger("TestTelemetry")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

logger.info("Database connection established.")
logger.warning("Cache miss rate at 42%.")
logger.error("Failed to fetch exchange rates.")

print("Captured Log Stream:")
print(log_stream.getvalue().strip())
""",
            expected_output="""Captured Log Stream:
[INFO] Database connection established.
[WARNING] Cache miss rate at 42%.
[ERROR] Failed to fetch exchange rates.""",
            output_explanation="The logger directs messages above the INFO threshold into the stream handler with standardized severity prefixes.",
            common_mistakes=[
                CommonMistake(
                    mistake="Leaving logging level set to DEBUG in high-throughput production environments",
                    explanation="DEBUG generates massive log volumes that consume disk space and degrade I/O performance.",
                    correction="Set production logging level to INFO or WARNING."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="Which standard Python logging level has higher severity than WARNING but lower severity than CRITICAL?",
                options=["DEBUG", "INFO", "ERROR", "TRACE"],
                correct_index=2,
                explanation="The hierarchy is DEBUG (10) < INFO (20) < WARNING (30) < ERROR (40) < CRITICAL (50)."
            )
        )
    ],
    practice_exercises=[
        PracticeExercise(
            id="m4-ex1",
            title="Safe Numeric File Reader",
            difficulty="Beginner",
            problem_statement="Write a function `sum_numbers_from_text(text_data)` that iterates over lines in a string, parses integers, skips malformed non-integer lines using a try-except block, and returns the total sum.",
            input_output_expectations="For text '10\\ninvalid\\n25\\n40\\ncorrupted', output must be Sum: 75",
            starter_code="""def sum_numbers_from_text(text_data):
    total = 0
    for line in text_data.strip().split('\\n'):
        try:
            total += int(line.strip())
        except ValueError:
            # Skip non-integer line
            continue
    return total

sample_input = "10\\ninvalid\\n25\\n40\\ncorrupted"
result = sum_numbers_from_text(sample_input)
print(f"Sum: {result}")
""",
            hints=[
                "Use try: total += int(line) except ValueError: continue",
                "Split with text_data.strip().split('\\n')"
            ],
            test_cases=[
                {"input": "", "expected_output": "Sum: 75", "description": "Sum of valid integers 10 + 25 + 40"}
            ],
            expected_substrings=["try", "except", "ValueError"],
            solution="""def sum_numbers_from_text(text_data):
    total = 0
    for line in text_data.strip().split('\\n'):
        try:
            total += int(line.strip())
        except ValueError:
            continue
    return total

sample_input = "10\\ninvalid\\n25\\n40\\ncorrupted"
result = sum_numbers_from_text(sample_input)
print(f"Sum: {result}")
"""
        ),
        PracticeExercise(
            id="m4-ex2",
            title="Custom Validation Exception",
            difficulty="Intermediate",
            problem_statement="Define a custom exception `PasswordLengthError(Exception)`. Create a function `validate_password(pwd)` that raises PasswordLengthError if len(pwd) < 8. Catch the exception and print 'Rejected: Password too short'.",
            input_output_expectations="Passing 'sec12' must trigger exception and print 'Rejected: Password too short'",
            starter_code="""class PasswordLengthError(Exception):
    pass

def validate_password(pwd):
    if len(pwd) < 8:
        raise PasswordLengthError("Password too short")
    return "Password Accepted"

try:
    validate_password("sec12")
except PasswordLengthError:
    print("Rejected: Password too short")
""",
            hints=[
                "class PasswordLengthError(Exception): pass",
                "raise PasswordLengthError('...') if len(pwd) < 8"
            ],
            test_cases=[
                {"input": "", "expected_output": "Rejected: Password too short", "description": "Short password validation"}
            ],
            expected_substrings=["PasswordLengthError", "raise PasswordLengthError"],
            solution="""class PasswordLengthError(Exception):
    pass

def validate_password(pwd):
    if len(pwd) < 8:
        raise PasswordLengthError("Password too short")
    return "Password Accepted"

try:
    validate_password("sec12")
except PasswordLengthError:
    print("Rejected: Password too short")
"""
        )
    ],
    quiz_questions=[
        QuizQuestion(
            id="m4-q1",
            question="What happens if you open an existing file with mode 'w'?",
            options=[
                "The file contents are preserved and new text is appended",
                "The file is immediately truncated (its previous contents are erased)",
                "Python raises a FileExistsError",
                "The file is opened in read-only mode"
            ],
            correct_index=1,
            explanation="Mode 'w' truncates existing files to zero bytes before writing."
        ),
        QuizQuestion(
            id="m4-q2",
            question="Which block in a try-except statement is guaranteed to execute regardless of whether an exception occurred?",
            options=[
                "else",
                "finally",
                "catch",
                "ensure"
            ],
            correct_index=1,
            explanation="The `finally` block always runs, making it ideal for deterministic cleanup of system resources."
        ),
        QuizQuestion(
            id="m4-q3",
            question="Why should you avoid using a bare `except:` clause without specifying an exception class?",
            options=[
                "It causes a compilation error in Python 3",
                "It catches system-exiting signals like KeyboardInterrupt and hides critical programming errors",
                "It converts all errors into strings",
                "It runs slower than if-else statements"
            ],
            correct_index=1,
            explanation="A bare `except:` intercepts BaseException subclasses like KeyboardInterrupt (Ctrl+C) and SystemExit."
        ),
        QuizQuestion(
            id="m4-q4",
            question="What does calling `f.tell()` on an open file object return?",
            options=[
                "The total number of words in the file",
                "The current file cursor byte offset position",
                "The file encoding format",
                "The file creation timestamp"
            ],
            correct_index=1,
            explanation="`f.tell()` returns an integer denoting the current byte offset of the file stream cursor."
        ),
        QuizQuestion(
            id="m4-q5",
            question="What is the default minimum severity level displayed by Python's standard `logging` module if not reconfigured?",
            options=[
                "DEBUG",
                "INFO",
                "WARNING",
                "ERROR"
            ],
            correct_index=2,
            explanation="Python's default logging threshold is WARNING; messages with DEBUG and INFO are suppressed by default."
        )
    ]
)

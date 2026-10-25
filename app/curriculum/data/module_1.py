"""
Module 1: Python Fundamentals
Marwadi University 01AP0303 - Unit 1 (6 Contact Hours, 10 Marks Assessment)
Mini-Project: Smart Calculator
"""
from app.curriculum.models import Module, Lesson, PracticeExercise, QuizQuestion, ProjectInfo, CommonMistake, MiniCheckpoint

MODULE_1 = Module(
    id=1,
    code="MOD-01",
    title="Python Fundamentals",
    syllabus_unit="Unit 1: Introduction, Environment & Core Syntax",
    contact_hours=6,
    assessment_marks=10,
    description="Establish an unshakable foundation in Python syntax, variable memory models, dynamic type inference, arithmetic precision, and console I/O.",
    learning_objectives=[
        "Understand Python's interpreted runtime and execution pipeline",
        "Master variable declarations, dynamic typing, and memory references",
        "Perform explicit type casting between strings, integers, and floats",
        "Apply arithmetic, comparison, logical, and compound assignment operators",
        "Construct robust console interaction with user input validation"
    ],
    topics_covered=[
        "Python Runtime & Interpreter",
        "IDEs: VS Code & Jupyter Notebooks",
        "Variables & Dynamic Memory Binding",
        "Primitive Data Types (int, float, str, bool)",
        "Type Conversion & Casting",
        "Arithmetic & Operator Precedence (PEMDAS)",
        "Comparison & Logical Operators",
        "Standard Input / Formatted Output (f-strings)"
    ],
    artwork_id="ART-05",
    project=ProjectInfo(
        id="proj-smart-calc",
        title="Smart Calculator",
        subtitle="Precision Scientific & Arithmetic Engine with Error Guardrails",
        objective="Develop an interactive computational tool that executes arithmetic, percentage discounts, and scientific calculations (powers, square roots) with comprehensive user input validation.",
        requirements=[
            "Support standard arithmetic (+, -, *, /, //, %)",
            "Support power (**) and square root calculations",
            "Support percentage calculation (e.g. discount and tax calculation)",
            "Prevent ZeroDivisionError with explicit mathematical safeguards",
            "Validate non-numeric inputs and output formatted floating-point results"
        ],
        starter_snippet="""# Module 1 Project: Smart Calculator
def calculate(num1, op, num2=None):
    if op == '+':
        return num1 + num2
    elif op == '/':
        if num2 == 0:
            return "Error: Division by zero is undefined."
        return num1 / num2
    # Expand with percentage, power, and scientific operations
""",
        module_id=1
    ),
    lessons=[
        Lesson(
            id="m1-l1",
            title="The Python Architecture & Syntax",
            subtitle="How Python compiles bytecode, manages objects, and enforces readable whitespace.",
            reading_time_min=6,
            concept_markdown="""### What Happens When You Run Python?

Python is designed to feel intuitive and human-friendly. When you write instructions in a Python file, you are writing clear, readable statements that tell the computer what to do step by step.

#### 1. The Simple Idea: Top-to-Bottom Execution
When you run a Python script, the Python interpreter reads your program from top to bottom, one statement at a time:
- It assigns values to variables as it encounters them.
- It computes expressions right away.
- It calls functions like `print()` to send output directly to your screen.

If there is a typo or error on line 5, Python executes lines 1 through 4 successfully first, and then stops at line 5 with a helpful error message. This instant feedback loop is what makes Python so approachable for learning.

#### 2. Under the Hood: The CPython Pipeline
While Python feels like it runs directly from plain text, a smart engineering process happens behind the scenes:

1. **Source Code (`.py`)**: You write readable instructions in a text file.
2. **Parsing & Syntax Checking**: CPython parses your code into an Abstract Syntax Tree (AST) to ensure correct grammar.
3. **Bytecode Compilation (`.pyc`)**: CPython compiles your statements into compact, low-level instructions called *bytecode*.
4. **Python Virtual Machine (PVM)**: The runtime engine reads each bytecode instruction sequentially and evaluates it with your computer's operating system.

```
+----------------+      +-------------------+      +-----------------------+
|  script.py     | ---> | Bytecode (.pyc)   | ---> | Python Virtual Mach.  | ---> Machine Output
| (Source Code)  |      | (CPython Compiler)|      | (Runtime Execution)   |
+----------------+      +-------------------+      +-----------------------+
```

Because CPython handles this compilation automatically in memory, you never have to run a separate manual compilation step like in C or Java.

#### 3. Meaningful Indentation
Unlike languages that rely on curly braces `{}` to group statements, Python uses **indentation** (standard 4 spaces). In Python, how your code looks is how it runs:
- Statements at the same indentation level belong to the same block.
- Indented lines beneath an `if`, `for`, or `def` form an inner block.

#### 4. Comments and Documentation
- `# Single-line comment`: Notes written for humans; ignored by the Python interpreter.
- `'''Triple quotes'''`: Multi-line text strings, often used as docstrings to explain what a function or module does.
""",
            syntax_example="""# Python indentation and simple output
greeting = "Welcome to Pip Learn"
version = 3.12

print(f"{greeting} (Python {version})")
if version >= 3.0:
    print("Modern Python 3 environment confirmed.")
""",
            executable_code="""# Executable demonstration of Python syntax and introspection
course = "01AP0303 - Programming with Python"
hours = 45
is_active = True

print(f"Course: {course}")
print(f"Total Contact Hours: {hours}")
print(f"Status Active: {is_active}")
print(f"Object Memory Identity: {id(course)}")
""",
            expected_output="""Course: 01AP0303 - Programming with Python
Total Contact Hours: 45
Status Active: True
Object Memory Identity: [Memory Address]""",
            output_explanation="Python allocates the string in heap memory and assigns the reference label 'course' to point to it. The id() function returns the memory address of the object.",
            common_mistakes=[
                CommonMistake(
                    mistake="Mixing tabs and spaces in code indentation",
                    explanation="Python 3 prohibits mixing tabs and spaces for indentation in the same block, throwing an IndentationError or TabError.",
                    correction="Configure your editor to insert 4 spaces whenever you press the Tab key."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What happens when CPython executes a .py file?",
                options=[
                    "It converts it directly into binary machine code without an interpreter",
                    "It compiles the source into bytecode which the Python Virtual Machine (PVM) executes",
                    "It sends the script to a web browser to run JavaScript",
                    "It requires manual linking like a C program"
                ],
                correct_index=1,
                explanation="CPython compiles the human-readable Python code into intermediate bytecode, which the Python Virtual Machine executes."
            )
        ),
        Lesson(
            id="m1-l2",
            title="Variables, Memory References & Data Types",
            subtitle="Understanding Python's object pointer model and fundamental data types.",
            reading_time_min=7,
            concept_markdown="""### Variables as Named Pointers

In Python, a variable is **not a fixed bucket of memory** that holds raw bytes. Instead, **everything in Python is an object**, and variables are **named references (pointers)** that bind to those objects in memory.

When you write:
```python
x = 100
y = x
```
Both `x` and `y` point to the exact same integer object `100` in memory. If you reassign `x = 200`, `x` now points to a new integer object `200`, while `y` still references `100`.

### Python's Core Primitive Types

| Type | Name | Examples | Mutability |
|---|---|---|---|
| `int` | Arbitrary-precision Integer | `-42`, `0`, `1000000` | Immutable |
| `float` | IEEE 754 Floating-point | `3.14159`, `-0.001`, `2.5e3` | Immutable |
| `str` | Unicode Text Character Sequence | `'Pip'`, `"Python"`, `'''Doc'''` | Immutable |
| `bool` | Boolean Truth Values | `True`, `False` | Immutable |

### Dynamic Typing and Type Checking
Python is **dynamically typed** (types are determined at runtime based on the assigned object) and **strongly typed** (Python will not silently convert types in illegal operations like `"Score: " + 95`).
""",
            syntax_example="""# Type inspection with type() and isinstance()
score = 98.5
total_students = 60
title = "Marwadi University"

print(type(score))           # <class 'float'>
print(isinstance(total_students, int))  # True
""",
            executable_code="""# Demonstrating variable reassignment and type introspection
val = 42
print(f"Value: {val}, Type: {type(val).__name__}")

val = "Now I am a string"
print(f"Value: {val}, Type: {type(val).__name__}")

val = 3.14159
print(f"Value: {val}, Type: {type(val).__name__}")
""",
            expected_output="""Value: 42, Type: int
Value: Now I am a string, Type: str
Value: 3.14159, Type: float""",
            output_explanation="Because Python is dynamically typed, the variable identifier 'val' can reference any object type throughout its lifecycle without explicit type declarations.",
            common_mistakes=[
                CommonMistake(
                    mistake="Attempting to concatenate a string and a number: 'Result: ' + 42",
                    explanation="Python is strongly typed and will raise TypeError: can only concatenate str (not 'int') to str.",
                    correction="Use formatted f-strings: f'Result: {42}' or explicit casting: 'Result: ' + str(42)."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="Why does Python allow a variable originally holding an integer to later hold a string?",
                options=[
                    "Python variables are weakly typed and cast everything to text",
                    "Variables are labels pointing to objects in memory, not fixed memory slots",
                    "The Python compiler deletes the variable and recreates it behind the scenes",
                    "It is a bug in the interpreter"
                ],
                correct_index=1,
                explanation="In Python, variables are object reference labels. Reassignment simply rebinds the label to a different object."
            )
        ),
        Lesson(
            id="m1-l3",
            title="Type Conversion & Casting",
            subtitle="Implicit coercion vs explicit conversion functions.",
            reading_time_min=5,
            concept_markdown="""### Implicit vs Explicit Conversion

#### 1. Implicit Type Conversion (Coercion)
Python automatically converts data types when no information loss occurs. For example, adding an `int` and a `float` results in a `float`:
```python
result = 10 + 3.5  # 13.5 (float)
```

#### 2. Explicit Type Conversion (Casting)
When converting across fundamentally different representations (e.g. text input into numbers), you must call explicit conversion constructors:
- `int(x)`: Converts to integer (truncates floats towards zero, parses numeric strings).
- `float(x)`: Converts to floating point.
- `str(x)`: Converts any object into its string representation.
- `bool(x)`: Evaluates truthiness (0, `""`, `None`, empty collections evaluate to `False`).
""",
            syntax_example="""# Explicit casting examples
user_entry = "450"
units = int(user_entry)
unit_price = float("19.99")
total = units * unit_price
print(f"Total: ${total:,.2f}")
""",
            executable_code="""# Demonstrating type casting and boolean truthiness
raw_age = "19"
age = int(raw_age)

raw_gpa = "3.85"
gpa = float(raw_gpa)

print(f"Age in 5 years: {age + 5}")
print(f"GPA rounded: {round(gpa, 1)}")
print(f"Truthiness of 0: {bool(0)}")
print(f"Truthiness of 'Python': {bool('Python')}")
""",
            expected_output="""Age in 5 years: 24
GPA rounded: 3.9
Truthiness of 0: False
Truthiness of 'Python': True""",
            output_explanation="Strings '19' and '3.85' are explicitly cast to numeric types before performing arithmetic. Boolean evaluation confirms 0 is falsy while non-empty strings are truthy.",
            common_mistakes=[
                CommonMistake(
                    mistake="Calling int('3.14') directly on a floating-point string",
                    explanation="int() on a string expecting integer digits raises ValueError: invalid literal for int() with base 10: '3.14'.",
                    correction="First parse with float: int(float('3.14'))."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What is the result of bool('False') in Python?",
                options=[
                    "False, because the word is False",
                    "True, because any non-empty string evaluates to True",
                    "TypeError, because strings cannot be booleans",
                    "None"
                ],
                correct_index=1,
                explanation="In Python, non-empty strings are truthy regardless of what characters they contain."
            )
        ),
        Lesson(
            id="m1-l4",
            title="Operators: Arithmetic, Logic & Precedence",
            subtitle="Mastering calculations, boolean logic, and operator precedence rules.",
            reading_time_min=6,
            concept_markdown="""### The Complete Python Operator Set

#### Arithmetic Operators
- `+` Addition, `-` Subtraction
- `*` Multiplication, `/` True Division (always returns float, e.g. `7 / 2 = 3.5`)
- `//` Floor Division (rounds down to nearest integer, e.g. `7 // 2 = 3`)
- `%` Modulo (remainder, e.g. `7 % 2 = 1`)
- `**` Exponentiation (e.g. `2 ** 3 = 8`)

#### Comparison Operators (Return bool)
- `==` Equality, `!=` Inequality
- `>`, `<`, `>=`, `<=` Relative comparisons

#### Logical Operators (Short-circuit evaluation)
- `and`: True only if both operands are true
- `or`: True if at least one operand is true
- `not`: Inverts boolean state

#### Operator Precedence (PEMDAS)
1. Parentheses `()`
2. Exponentiation `**`
3. Unary signs `+x`, `-x`
4. Multiplication, Division, Floor division, Modulo `*`, `/`, `//`, `%`
5. Addition and Subtraction `+`, `-`
6. Comparisons `==`, `!=`, `<`, `>`, `<=`, `>=`
7. Logical `not`, `and`, `or`
""",
            syntax_example="""# Precision and floor division
hours = 125
days = hours // 24
remaining_hours = hours % 24
print(f"{hours} hours = {days} days and {remaining_hours} hours")
""",
            executable_code="""# Demonstrating arithmetic and precedence
base_salary = 50000
bonus_rate = 0.15
tax_rate = 0.10

# Correct precedence using parentheses
net_salary = (base_salary * (1 + bonus_rate)) * (1 - tax_rate)

print(f"Base: ${base_salary}")
print(f"Gross with 15% Bonus: ${base_salary * (1 + bonus_rate):,.2f}")
print(f"Net after 10% Tax: ${net_salary:,.2f}")
print(f"2 ** 3 ** 2 = {2 ** 3 ** 2} (right-to-left associativity)")
""",
            expected_output="""Base: $50000
Gross with 15% Bonus: $57,500.00
Net after 10% Tax: $51,750.00
2 ** 3 ** 2 = 512 (right-to-left associativity)""",
            output_explanation="Exponentiation ** evaluates right-to-left: 3 ** 2 = 9, then 2 ** 9 = 512. Parentheses guarantee financial calculations occur in the intended order.",
            common_mistakes=[
                CommonMistake(
                    mistake="Confusing == (equality check) with = (assignment)",
                    explanation="Writing if x = 10 will raise a SyntaxError in Python.",
                    correction="Use == for comparison and = strictly for assigning values to variables."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What is the output of 15 // 4 and 15 % 4?",
                options=[
                    "3.75 and 0",
                    "3 and 3",
                    "4 and 1",
                    "3 and 0"
                ],
                correct_index=1,
                explanation="Floor division 15 // 4 is 3. The remainder (modulo) 15 % 4 is 3 (because 4 * 3 = 12, leaving 3)."
            )
        ),
        Lesson(
            id="m1-l5",
            title="Formatted Output with f-strings & User Input",
            subtitle="Building professional console interfaces and formatted displays.",
            reading_time_min=6,
            concept_markdown="""### Modern Python String Formatting

Introduced in Python 3.6, **f-strings (Formatted String Literals)** are evaluated at runtime, offering superior speed, readability, and formatting capabilities.

#### Formatting Specifiers
- `{val:.2f}`: Format float to 2 decimal places.
- `{val:,}`: Add comma as thousands separator (e.g. `1,000,000`).
- `{val:>10}`: Right-align in a field 10 characters wide.
- `{val:<10}`: Left-align in a field 10 characters wide.
- `{val:^10}`: Center in a field 10 characters wide.
- `{val:04d}`: Pad integer with leading zeroes to 4 digits.

#### Reading Input
The built-in `input(prompt)` function pauses execution, displays the prompt, and captures whatever the user types as a **`str`**. You must always cast it if expecting numbers!
""",
            syntax_example="""# Formatted financial and scientific table
item = "Microcontroller"
cost = 14.5
qty = 150
total = cost * qty

print(f"{'Item':<18} | {'Qty':>6} | {'Cost':>8} | {'Total':>10}")
print("-" * 50)
print(f"{item:<18} | {qty:>6} | ${cost:>7.2f} | ${total:>9.2f}")
""",
            executable_code="""# Executable f-string formatting demonstration
student = "Priya Patel"
enrollment = 240101
marks_python = 94.678
scholarship_ratio = 0.85

print(f"Student: {student} (ID: {enrollment:08d})")
print(f"Python Score: {marks_python:.1f}%")
print(f"Scholarship Coverage: {scholarship_ratio:.1%}")
""",
            expected_output="""Student: Priya Patel (ID: 00240101)
Python Score: 94.7%
Scholarship Coverage: 85.0%""",
            output_explanation="Specifiers format the enrollment with leading zeros to 8 digits, round marks to 1 decimal place, and format the ratio directly as a percentage.",
            common_mistakes=[
                CommonMistake(
                    mistake="Forgetting that input() always returns a string",
                    explanation="num = input('Enter number: '); print(num + 5) will crash with TypeError.",
                    correction="Always wrap with int() or float(): num = float(input('Enter number: '))."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="How do you format a floating-point number 'pi = 3.14159' to display exactly 2 decimal places using f-strings?",
                options=[
                    "f'{pi.2}'",
                    "f'{pi:.2f}'",
                    "f'{round(pi, 2):float}'",
                    "f'%2f(pi)'"
                ],
                correct_index=1,
                explanation="The format specifier `:.2f` specifies a fixed-point floating representation rounded to 2 decimal places."
            )
        )
    ],
    practice_exercises=[
        PracticeExercise(
            id="m1-ex1",
            title="Temperature Conversion Utility",
            difficulty="Beginner",
            problem_statement="Write a Python program that converts a Celsius temperature of 37.0 into Fahrenheit using the formula: F = (C * 9/5) + 32. Print the result formatted to 1 decimal place.",
            input_output_expectations="Expected stdout must contain: '37.0 C = 98.6 F'",
            starter_code="""# Convert Celsius to Fahrenheit
celsius = 37.0

# Calculate fahrenheit below
fahrenheit = (celsius * 9/5) + 32

print(f"{celsius:.1f} C = {fahrenheit:.1f} F")
""",
            hints=[
                "Use the formula: (celsius * 9 / 5) + 32",
                "Format with f'{celsius:.1f} C = {fahrenheit:.1f} F'"
            ],
            test_cases=[
                {"input": "", "expected_output": "37.0 C = 98.6 F", "description": "Celsius 37.0 standard body temp conversion"}
            ],
            expected_substrings=["celsius", "fahrenheit"],
            solution="""celsius = 37.0
fahrenheit = (celsius * 9 / 5) + 32
print(f"{celsius:.1f} C = {fahrenheit:.1f} F")
"""
        ),
        PracticeExercise(
            id="m1-ex2",
            title="Compound Bill and Tip Calculator",
            difficulty="Beginner",
            problem_statement="Given a bill amount of 120.0, a tax percentage of 8.5%, and a tip percentage of 15.0%, calculate the total amount payable and the amount per person if split among 3 people. Format all currency values to 2 decimal places.",
            input_output_expectations="Output must display Total: $148.20 and Per Person: $49.40",
            starter_code="""bill = 120.0
tax_rate = 0.085
tip_rate = 0.15
people = 3

# Compute tax, tip, total, and split_amount
tax = bill * tax_rate
tip = bill * tip_rate
total = bill + tax + tip
per_person = total / people

print(f"Total: ${total:.2f}")
print(f"Per Person: ${per_person:.2f}")
""",
            hints=[
                "Tax = bill * 0.085",
                "Tip = bill * 0.15",
                "Total = bill + tax + tip",
                "Divide total by people to get the split"
            ],
            test_cases=[
                {"input": "", "expected_output": "Total: $148.20", "description": "Verify Total Calculation"},
                {"input": "", "expected_output": "Per Person: $49.40", "description": "Verify Split Calculation"}
            ],
            expected_substrings=["total", "per_person"],
            solution="""bill = 120.0
tax_rate = 0.085
tip_rate = 0.15
people = 3

tax = bill * tax_rate
tip = bill * tip_rate
total = bill + tax + tip
per_person = total / people

print(f"Total: ${total:.2f}")
print(f"Per Person: ${per_person:.2f}")
"""
        )
    ],
    quiz_questions=[
        QuizQuestion(
            id="m1-q1",
            question="Which of the following is an invalid Python variable name?",
            options=[
                "_total_score",
                "student_1st_rank",
                "1st_student_rank",
                "CourseCode01AP0303"
            ],
            correct_index=2,
            explanation="Variable names in Python cannot begin with a numeric digit. '1st_student_rank' raises a SyntaxError."
        ),
        QuizQuestion(
            id="m1-q2",
            question="What is the exact data type and value returned by the expression 10 / 2 in Python 3?",
            options=[
                "int with value 5",
                "float with value 5.0",
                "str with value '5'",
                "int with value 5 if imported from math"
            ],
            correct_index=1,
            explanation="In Python 3, the single slash division operator '/' always performs true division and produces a float."
        ),
        QuizQuestion(
            id="m1-q3",
            question="What does short-circuit evaluation mean for the logical 'and' operator?",
            options=[
                "Both expressions are evaluated simultaneously using multi-threading",
                "If the first operand is False, Python immediately returns False without evaluating the second operand",
                "If an error occurs, it resets the variable to zero",
                "It converts all operands into integers"
            ],
            correct_index=1,
            explanation="With 'and', if the first operand is falsy, the result cannot possibly be true, so Python stops evaluating immediately."
        ),
        QuizQuestion(
            id="m1-q4",
            question="What does the floor division operator '//' do when evaluating -7 // 2?",
            options=[
                "-3 (truncates towards zero)",
                "-4 (floors towards negative infinity)",
                "-3.5 (returns exact float)",
                "Raises a ValueError"
            ],
            correct_index=1,
            explanation="Floor division rounds down towards negative infinity. -3.5 rounded down is -4."
        ),
        QuizQuestion(
            id="m1-q5",
            question="Which statement correctly casts a string variable `user_input = '100'` into an integer?",
            options=[
                "val = to_int(user_input)",
                "val = (int) user_input",
                "val = int(user_input)",
                "val = Integer.parseInt(user_input)"
            ],
            correct_index=2,
            explanation="Python uses built-in type constructors like int(x), float(x), str(x) for explicit type casting."
        )
    ]
)

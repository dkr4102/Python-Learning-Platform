"""
Module 2: Control Flow and Functions
Marwadi University 01AP0303 - Unit 2 (6 Contact Hours, 12 Marks Assessment)
Mini-Project: Employee Payroll Processing System
"""
from app.curriculum.models import Module, Lesson, PracticeExercise, QuizQuestion, ProjectInfo, CommonMistake, MiniCheckpoint

MODULE_2 = Module(
    id=2,
    code="MOD-02",
    title="Control Flow and Functions",
    syllabus_unit="Unit 2: Decision Making, Iteration & Modular Programming",
    contact_hours=6,
    assessment_marks=12,
    description="Master structural decision trees, iterative algorithms with range and while loops, function call stacks, scope resolution, lambda expressions, and modular function design.",
    learning_objectives=[
        "Implement complex branching logic with if, elif, else and nested conditions",
        "Design efficient for and while loops with range(), break, continue, and loop-else constructs",
        "Generate geometric pattern sequences programmatically",
        "Define reusable functions with default arguments, variable parameters (*args, **kwargs), and explicit return statements",
        "Apply lambda functions, recursion basics, and the LEGB variable scope hierarchy"
    ],
    topics_covered=[
        "Conditional Logic (if, elif, else, ternary expressions)",
        "Nested Conditionals & Guard Clauses",
        "Iterating with for Loops & range()",
        "Indefinite Iteration with while Loops",
        "Loop Control: break, continue, pass & loop else",
        "Pattern Generation Algorithms",
        "Function Signatures, Default Arguments & Variable Parameters",
        "Variable Scope: Local, Enclosing, Global, Built-in (LEGB)",
        "Lambda Anonymous Functions & Recursion Basics"
    ],
    artwork_id="ART-06",
    project=ProjectInfo(
        id="proj-payroll-system",
        title="Employee Payroll Processing System",
        subtitle="Automated Salary, Overtime, Tax Bracket & Deduction Engine",
        objective="Implement a comprehensive enterprise payroll calculation system that determines gross salary, overtime premiums, progressive tax brackets, and net pay for diverse employee roles.",
        requirements=[
            "Calculate base pay from regular hours worked and hourly pay rate",
            "Apply overtime rules: 1.5x hourly rate for hours worked beyond 40 hours",
            "Calculate progressive tax deductions based on income brackets",
            "Deduct health insurance and pension contributions",
            "Generate an itemized payslip breakdown report"
        ],
        starter_snippet="""# Module 2 Project: Employee Payroll System
def calculate_payroll(employee_name, hours_worked, hourly_rate, health_deduction=50.0):
    regular_hours = min(hours_worked, 40)
    overtime_hours = max(0, hours_worked - 40)
    base_pay = regular_hours * hourly_rate
    overtime_pay = overtime_hours * (hourly_rate * 1.5)
    gross_pay = base_pay + overtime_pay
    
    # Calculate tax (e.g. 10% under 1000, 15% above 1000)
    tax = gross_pay * 0.15 if gross_pay > 1000 else gross_pay * 0.10
    net_pay = gross_pay - tax - health_deduction
    
    return {
        "employee": employee_name,
        "gross": gross_pay,
        "tax": tax,
        "net": net_pay
    }
""",
        module_id=2
    ),
    lessons=[
        Lesson(
            id="m2-l1",
            title="Conditional Branching & Guard Clauses",
            subtitle="Structuring clean decision trees without deeply nested arrow anti-patterns.",
            reading_time_min=6,
            concept_markdown="""### Decision Making in Python

Programs make decisions by evaluating boolean expressions. The `if`, `elif`, and `else` statements evaluate conditions top-to-bottom:

```python
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
```

#### Guard Clauses vs Nested Ifs
Deeply nested `if` statements create difficult-to-maintain code (the "Arrow Anti-pattern"). Instead, favor **guard clauses** that handle edge cases and exit early:

```python
# Bad: Nested pyramid
def process_user(user):
    if user is not None:
        if user.is_active:
            return "Active"

# Good: Guard clauses
def process_user(user):
    if user is None:
        return "No user"
    if not user.is_active:
        return "Inactive"
    return "Active"
```

#### Conditional Expressions (Ternary Operator)
Python supports compact inline conditional assignment:
```python
status = "Adult" if age >= 18 else "Minor"
```
""",
            syntax_example="""# Guard clause and ternary operator
def evaluate_attendance(attended_hours, total_hours=45):
    percentage = (attended_hours / total_hours) * 100
    eligibility = "Eligible for Exam" if percentage >= 75.0 else "Ineligible (Debarred)"
    return percentage, eligibility

pct, status = evaluate_attendance(36)
print(f"Attendance: {pct:.1f}% -> {status}")
""",
            executable_code="""# Executable decision branching
score = 88.5

if score >= 90:
    tier = "Distinction"
elif score >= 75:
    tier = "First Class"
elif score >= 50:
    tier = "Pass"
else:
    tier = "Fail"

award = "Merit Scholarship" if score >= 85 else "Standard Admission"
print(f"Score: {score} | Tier: {tier} | Award: {award}")
""",
            expected_output="""Score: 88.5 | Tier: First Class | Award: Merit Scholarship""",
            output_explanation="Because 88.5 satisfies score >= 75 (after failing score >= 90), the tier is 'First Class'. The ternary operator checks score >= 85 and assigns 'Merit Scholarship'.",
            common_mistakes=[
                CommonMistake(
                    mistake="Using multiple separate `if` statements instead of `elif`",
                    explanation="Separate `if` statements all execute independently, potentially overriding prior assignments.",
                    correction="Use `elif` to ensure that exactly one branch in the chain executes."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What is the result of: 'Passed' if 75 >= 50 else 'Failed'?",
                options=["'Failed'", "'Passed'", "SyntaxError", "True"],
                correct_index=1,
                explanation="The condition 75 >= 50 is True, so the expression evaluates to the left-hand value 'Passed'."
            )
        ),
        Lesson(
            id="m2-l2",
            title="Loops & Iteration: for, while, and range()",
            subtitle="Mastering definite iteration, range step parameters, and while loops.",
            reading_time_min=7,
            concept_markdown="""### Iteration Paradigms

#### 1. Definite Iteration: `for` Loops and `range()`
The `for` loop iterates over any iterable (sequences, lists, ranges, strings):
```python
range(stop)              # 0 to stop-1
range(start, stop)       # start to stop-1
range(start, stop, step) # increment by step (positive or negative)
```

Example countdown:
```python
for count in range(5, 0, -1):
    print(count)  # 5, 4, 3, 2, 1
```

#### 2. Indefinite Iteration: `while` Loops
The `while` loop continues executing as long as its condition remains `True`.

#### 3. Loop Control Statements
- `break`: Terminate the loop immediately.
- `continue`: Skip the rest of the current iteration and jump to the next one.
- `pass`: A syntactical placeholder statement doing nothing.
- `for ... else`: The `else` block runs **only if the loop completed naturally** without hitting a `break`!
""",
            syntax_example="""# Loop with break and else for prime number checking
number = 29
is_prime = True

for divisor in range(2, int(number ** 0.5) + 1):
    if number % divisor == 0:
        is_prime = False
        break
else:
    # Executes only if no break was triggered
    is_prime = True

print(f"{number} is prime: {is_prime}")
""",
            executable_code="""# Executable loop demonstration with range and step
print("Even numbers from 2 to 10:")
even_nums = []
for n in range(2, 11, 2):
    even_nums.append(n)
print(even_nums)

print("Accumulating sum with while loop:")
total = 0
current = 1
while current <= 5:
    total += current
    current += 1
print(f"Sum 1 to 5 = {total}")
""",
            expected_output="""Even numbers from 2 to 10:
[2, 4, 6, 8, 10]
Accumulating sum with while loop:
Sum 1 to 5 = 15""",
            output_explanation="range(2, 11, 2) starts at 2, increments by 2, and stops before 11. The while loop runs 5 times accumulating 1+2+3+4+5 = 15.",
            common_mistakes=[
                CommonMistake(
                    mistake="Off-by-one errors with range(1, 10)",
                    explanation="range(1, 10) stops at 9, not 10, because the stop boundary is exclusive.",
                    correction="Use range(1, 11) if you wish to include 10."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="When does the 'else' block of a Python 'for ... else' statement execute?",
                options=[
                    "Whenever the loop encounters an error",
                    "Only when the loop completes its iterations without hitting a 'break' statement",
                    "On every iteration of the loop",
                    "Only if the iterable was empty"
                ],
                correct_index=1,
                explanation="In Python, the loop 'else' clause executes when the loop finishes normally without being terminated by a break statement."
            )
        ),
        Lesson(
            id="m2-l3",
            title="Pattern Generation Algorithms",
            subtitle="Developing nested loop logic through 2D coordinate patterns.",
            reading_time_min=6,
            concept_markdown="""### Algorithmic Pattern Generation

Pattern generation is a foundational exercise in university curricula (such as Marwadi University 01AP0303) because it trains your brain to map 2D coordinates `(row, col)` into conditional prints.

#### Key Principles:
1. Outer loop controls the **row count** (`i`).
2. Inner loop controls the **column count** (`j`).
3. The `print('*', end='')` argument prevents the default newline, printing characters side-by-side.
4. Calling `print()` without arguments at the end of the outer loop moves down to the next line.
""",
            syntax_example="""# Right triangle star pattern
rows = 5
for i in range(1, rows + 1):
    for j in range(i):
        print("* ", end="")
    print()
""",
            executable_code="""# Executable pyramid and number triangle
rows = 4
print("Number Triangle:")
for i in range(1, rows + 1):
    for j in range(1, i + 1):
        print(j, end=" ")
    print()

print("\nCentered Asterisk Pyramid:")
for i in range(1, rows + 1):
    spaces = " " * (rows - i)
    stars = "* " * i
    print(spaces + stars)
""",
            expected_output="""Number Triangle:
1 
1 2 
1 2 3 
1 2 3 4 

Centered Asterisk Pyramid:
   * 
  * * 
 * * * 
* * * * """,
            output_explanation="String multiplication (' ' * (rows - i)) generates left-padding spaces to center each row of stars.",
            common_mistakes=[
                CommonMistake(
                    mistake="Omitting end='' in print()",
                    explanation="Default print() appends a newline \\n after every single character, creating a vertical line instead of a 2D pattern.",
                    correction="Specify end=' ' or end='' when printing items within the same row."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What parameter in Python's print() function controls what character is printed at the end of the output?",
                options=["sep", "end", "flush", "terminator"],
                correct_index=1,
                explanation="The 'end' parameter in print() controls the trailing string (defaulting to '\\n')."
            )
        ),
        Lesson(
            id="m2-l4",
            title="User-Defined Functions & Scope (LEGB)",
            subtitle="Signatures, return values, default arguments, and namespace resolution.",
            reading_time_min=7,
            concept_markdown="""### Modular Programming with Functions

Functions encapsulate reusable logic, improve testability, and keep code DRY (Don't Repeat Yourself).

```python
def function_name(param1, param2=default_val):
    '''Optional docstring explaining function behavior.'''
    result = param1 + param2
    return result
```

#### Argument Types:
- **Positional Arguments**: Assigned in order.
- **Keyword Arguments**: Assigned by name (`calc(b=20, a=10)`).
- **Default Arguments**: Optional parameters with fallback values.
- **Arbitrary Positional (`*args`)**: Bundles extra positional args into a tuple.
- **Arbitrary Keyword (`**kwargs`)**: Bundles extra keyword args into a dictionary.

#### The LEGB Scope Resolution Rule
When Python looks up a variable name, it checks namespaces in this exact order:
1. **L**ocal: Inside current function.
2. **E**nclosing: In any enclosing outer functions (closures).
3. **G**lobal: At the module top-level.
4. **B**uilt-in: Python built-ins like `len`, `range`, `print`.
""",
            syntax_example="""# Flexible arguments with *args and **kwargs
def calculate_summary(*values, **metadata):
    total = sum(values)
    avg = total / len(values) if values else 0.0
    print(f"Report for: {metadata.get('subject', 'General')}")
    return {"total": total, "average": avg}

res = calculate_summary(85, 92, 78, subject="Python Exam")
print(res)
""",
            executable_code="""# Demonstrating default args, *args, and return values
def compute_gross_pay(hours, hourly_rate=25.0, bonus=0.0):
    regular = min(hours, 40)
    overtime = max(0, hours - 40)
    pay = (regular * hourly_rate) + (overtime * hourly_rate * 1.5) + bonus
    return pay

print(f"Standard 40 hours: ${compute_gross_pay(40):.2f}")
print(f"Overtime 50 hours + bonus: ${compute_gross_pay(50, hourly_rate=30.0, bonus=100.0):.2f}")
""",
            expected_output="""Standard 40 hours: $1000.00
Overtime 50 hours + bonus: $1750.00""",
            output_explanation="The function applies default hourly_rate of $25.0 for the first call, and calculates 40*30 + 10*(30*1.5) + 100 = 1200 + 450 + 100 = $1750.00 for the second.",
            common_mistakes=[
                CommonMistake(
                    mistake="Using a mutable object (like a list or dict) as a default argument: def add_item(x, lst=[]):",
                    explanation="Default arguments are evaluated once when the function is defined, sharing the same list across all calls.",
                    correction="Use None as default: def add_item(x, lst=None): if lst is None: lst = []"
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="In Python's LEGB scope rule, which namespace is checked first when resolving a variable name?",
                options=["Global", "Enclosing", "Local", "Built-in"],
                correct_index=2,
                explanation="Local scope (variables inside the current function) is checked first."
            )
        ),
        Lesson(
            id="m2-l5",
            title="Lambda Functions & Recursion Basics",
            subtitle="Anonymous single-expression functions and recursive base cases.",
            reading_time_min=6,
            concept_markdown="""### Lambda Functions (Anonymous Expressions)

A `lambda` function is a compact, anonymous function defined without `def`. It can take multiple arguments but contains **only a single expression** whose evaluated value is returned:

```python
# Syntax: lambda arguments: expression
square = lambda x: x ** 2
print(square(6))  # 36
```

Often used in sorting or higher-order functions:
```python
students = [("Aarav", 88), ("Priya", 95), ("Rohan", 72)]
students.sort(key=lambda s: s[1], reverse=True)
```

### Recursion: Functions Calling Themselves
A recursive function solves a problem by solving smaller instances of the same problem. Every recursive function **must have two parts**:
1. **Base Case**: The termination condition where recursion stops.
2. **Recursive Step**: The call to itself with reduced arguments.

```python
def factorial(n):
    if n <= 1:  # Base case
        return 1
    return n * factorial(n - 1)  # Recursive step
```
""",
            syntax_example="""# Sorting with lambda and calculating factorial recursively
students = [{"name": "Aarav", "marks": 89}, {"name": "Priya", "marks": 96}]
sorted_students = sorted(students, key=lambda s: s["marks"], reverse=True)
print("Top student:", sorted_students[0]["name"])
""",
            executable_code="""# Executable recursion and lambda demo
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

fib_sequence = [fibonacci(i) for i in range(7)]
print("Fibonacci Sequence (first 7 terms):", fib_sequence)

# Lambda multiplier
multiplier = lambda base, factor: base * factor
print("Multiplier result (15 * 4):", multiplier(15, 4))
""",
            expected_output="""Fibonacci Sequence (first 7 terms): [0, 1, 1, 2, 3, 5, 8]
Multiplier result (15 * 4): 60""",
            output_explanation="The recursive function breaks down fibonacci numbers with base cases for 0 and 1. The list comprehension evaluates indices 0 through 6.",
            common_mistakes=[
                CommonMistake(
                    mistake="Forgetting the base case in a recursive function",
                    explanation="Without a base case, recursion repeats until hitting Python's recursion depth limit, raising RecursionError: maximum recursion depth exceeded.",
                    correction="Always define and test your base case condition before writing the recursive step."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What limitation exists on Python lambda functions?",
                options=[
                    "They cannot accept parameters",
                    "They can only contain a single expression, not multi-line statements",
                    "They can only return strings",
                    "They cannot be used with sorted()"
                ],
                correct_index=1,
                explanation="Python lambdas are restricted to a single expression that automatically returns its value."
            )
        )
    ],
    practice_exercises=[
        PracticeExercise(
            id="m2-ex1",
            title="Overtime Pay Calculator Function",
            difficulty="Beginner",
            problem_statement="Define a function `compute_pay(hours, rate)` that calculates gross earnings. If hours > 40, pay 1.5 times the hourly rate for all hours worked above 40. Test with 45 hours at $20.00/hour.",
            input_output_expectations="Calling compute_pay(45, 20.0) must return 950.0 and print 'Gross Pay: $950.00'",
            starter_code="""def compute_pay(hours, rate):
    # Calculate base and overtime
    if hours <= 40:
        return hours * rate
    else:
        regular = 40 * rate
        overtime = (hours - 40) * (rate * 1.5)
        return regular + overtime

pay = compute_pay(45, 20.0)
print(f"Gross Pay: ${pay:.2f}")
""",
            hints=[
                "Overtime hours = hours - 40",
                "Overtime rate = rate * 1.5",
                "Total = (40 * rate) + (overtime_hours * overtime_rate)"
            ],
            test_cases=[
                {"input": "", "expected_output": "Gross Pay: $950.00", "description": "45 hours at $20 rate"}
            ],
            expected_substrings=["compute_pay"],
            solution="""def compute_pay(hours, rate):
    if hours <= 40:
        return hours * rate
    return (40 * rate) + ((hours - 40) * rate * 1.5)

pay = compute_pay(45, 20.0)
print(f"Gross Pay: ${pay:.2f}")
"""
        ),
        PracticeExercise(
            id="m2-ex2",
            title="Recursive Power Function",
            difficulty="Intermediate",
            problem_statement="Write a recursive function `power(base, exp)` that computes base raised to exp (non-negative integer exp) without using ** or math.pow(). Base case: exp == 0 returns 1.",
            input_output_expectations="Calling power(2, 5) must print '2^5 = 32'",
            starter_code="""def power(base, exp):
    # Implement recursive base case and step
    if exp == 0:
        return 1
    return base * power(base, exp - 1)

result = power(2, 5)
print(f"2^5 = {result}")
""",
            hints=[
                "If exp == 0, return 1",
                "Otherwise return base * power(base, exp - 1)"
            ],
            test_cases=[
                {"input": "", "expected_output": "2^5 = 32", "description": "2 to power 5 is 32"}
            ],
            expected_substrings=["power", "exp - 1"],
            solution="""def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp - 1)

result = power(2, 5)
print(f"2^5 = {result}")
"""
        )
    ],
    quiz_questions=[
        QuizQuestion(
            id="m2-q1",
            question="What is the output of range(3, 10, 3) converted to a list?",
            options=[
                "[3, 6, 9]",
                "[3, 6, 9, 12]",
                "[3, 4, 5, 6, 7, 8, 9, 10]",
                "[0, 3, 6, 9]"
            ],
            correct_index=0,
            explanation="range(3, 10, 3) starts at 3, steps by 3, and stops before reaching 10, yielding [3, 6, 9]."
        ),
        QuizQuestion(
            id="m2-q2",
            question="What does the 'continue' keyword do inside a loop?",
            options=[
                "Terminates the loop completely",
                "Skips the rest of the current iteration and advances to the next iteration",
                "Restarts the entire loop from the initial condition",
                "Pauses execution for 1 second"
            ],
            correct_index=1,
            explanation="'continue' immediately abandons the remainder of the current iteration and begins the next loop cycle."
        ),
        QuizQuestion(
            id="m2-q3",
            question="What happens if a Python function does not include an explicit return statement?",
            options=[
                "It raises an UnboundReturnError",
                "It returns 0 by default",
                "It returns None implicitly",
                "It returns False"
            ],
            correct_index=2,
            explanation="Functions without an explicit return statement implicitly return None upon exiting."
        ),
        QuizQuestion(
            id="m2-q4",
            question="How are extra positional arguments collected into a function parameter defined with `*args`?",
            options=[
                "As a list",
                "As a tuple",
                "As a dictionary",
                "As a set"
            ],
            correct_index=1,
            explanation="The `*args` syntax packages arbitrary positional arguments into an immutable tuple."
        ),
        QuizQuestion(
            id="m2-q5",
            question="Which rule governs variable name resolution order in Python?",
            options=[
                "FIFO (First In First Out)",
                "LEGB (Local, Enclosing, Global, Built-in)",
                "DOM (Document Object Model)",
                "LIFO (Last In First Out)"
            ],
            correct_index=1,
            explanation="Python resolves identifiers using the LEGB hierarchy: Local -> Enclosing -> Global -> Built-in."
        )
    ]
)

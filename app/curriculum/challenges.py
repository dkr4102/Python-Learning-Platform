"""
Curriculum coding challenges registry for Pip Learn lessons.
Provides three meaningful, progressively scaffolded coding challenges per lesson:
1. Warmup: Direct syntax and concept verification
2. Application: Realistic problem solving
3. Challenge: Edge cases, robust formatting, or logic composition
"""
from typing import Dict, List, Optional
from app.curriculum.models import PracticeExercise


LESSON_CHALLENGES: Dict[str, List[PracticeExercise]] = {
    # ----------------------------------------------------
    # MODULE 1: LESSON 1 — The Python Architecture & Syntax
    # ----------------------------------------------------
    "m1-l1": [
        PracticeExercise(
            id="m1-l1-ex1",
            title="First Output & Clean Syntax",
            difficulty="Warmup",
            problem_statement="Write a valid Python script that uses the `print()` function to output two separate lines:\n1. 'Hello, Python 3!'\n2. 'Execution verified.'",
            input_output_expectations="Expected stdout:\nHello, Python 3!\nExecution verified.",
            starter_code="# Challenge 1: Print two verified lines to stdout\n# Write your print statements below:\n\n",
            hints=[
                "Use two separate print() calls, one after another.",
                "Enclose the strings in double quotes: \"Hello, Python 3!\"",
                "Python executes statements in order from top to bottom."
            ],
            test_cases=[
                {"input": "", "expected_output": "Hello, Python 3!\nExecution verified.", "description": "Verify two lines of exact output"}
            ],
            expected_substrings=["print"],
            solution="print(\"Hello, Python 3!\")\nprint(\"Execution verified.\")"
        ),
        PracticeExercise(
            id="m1-l1-ex2",
            title="Fix the Indentation Error",
            difficulty="Application",
            problem_statement="Python relies strictly on consistent 4-space indentation for code blocks. Fix the syntax and indentation in this snippet so it calculates and prints the total contact hours (30 lectures + 15 practicals = 45).",
            input_output_expectations="Expected stdout:\nCourse: 01AP0303\nTotal Hours: 45",
            starter_code="course = \"01AP0303\"\nlectures = 30\npracticals = 15\n\n# Fix indentation and complete the calculation:\ntotal = lectures + practicals\nprint(\"Course:\", course)\nprint(\"Total Hours:\", total)\n",
            hints=[
                "Make sure statements are aligned at the leftmost margin with no unexpected leading spaces.",
                "Use the variable `total` to store the sum of `lectures` and `practicals`.",
                "Verify the output matches 'Course: 01AP0303' and 'Total Hours: 45'."
            ],
            test_cases=[
                {"input": "", "expected_output": "Course: 01AP0303\nTotal Hours: 45", "description": "Verify total contact hours calculation"}
            ],
            expected_substrings=["total", "print"],
            solution="course = \"01AP0303\"\nlectures = 30\npracticals = 15\ntotal = lectures + practicals\nprint(\"Course:\", course)\nprint(\"Total Hours:\", total)"
        ),
        PracticeExercise(
            id="m1-l1-ex3",
            title="Inspect Object Types",
            difficulty="Challenge",
            problem_statement="Python objects know their own types at runtime. Create a variable `platform_name = \"Pip Learn\"` and print its type using Python's built-in `type()` function: `print(type(platform_name))`.",
            input_output_expectations="Expected stdout:\n<class 'str'>",
            starter_code="# Challenge 3: Type introspection\nplatform_name = \"Pip Learn\"\n\n# Call type() and print the result:\n",
            hints=[
                "Pass `platform_name` as the argument to `type()`.",
                "Wrap the `type()` call inside `print(...)`.",
                "The output will display `<class 'str'>` indicating a string object."
            ],
            test_cases=[
                {"input": "", "expected_output": "<class 'str'>", "description": "Verify type inspection of string object"}
            ],
            expected_substrings=["type", "platform_name"],
            solution="platform_name = \"Pip Learn\"\nprint(type(platform_name))"
        ),
    ],

    # ----------------------------------------------------
    # MODULE 1: LESSON 2 — Variables, Memory References & Data Types
    # ----------------------------------------------------
    "m1-l2": [
        PracticeExercise(
            id="m1-l2-ex1",
            title="Define Typed Variables",
            difficulty="Warmup",
            problem_statement="Define three variables representing a learner record:\n- `student_name` with the string 'Priya'\n- `completed_lessons` with the integer 5\n- `accuracy_rate` with the float 94.5\nPrint all three on separate lines in that order.",
            input_output_expectations="Expected stdout:\nPriya\n5\n94.5",
            starter_code="# Challenge 1: Define variables of three different types\n\n",
            hints=[
                "Strings require quotation marks; integers and floats do not.",
                "Assign each variable on its own line.",
                "Call print() for each variable."
            ],
            test_cases=[
                {"input": "", "expected_output": "Priya\n5\n94.5", "description": "Verify string, int, and float variable definitions"}
            ],
            expected_substrings=["student_name", "completed_lessons", "accuracy_rate"],
            solution="student_name = \"Priya\"\ncompleted_lessons = 5\naccuracy_rate = 94.5\nprint(student_name)\nprint(completed_lessons)\nprint(accuracy_rate)"
        ),
        PracticeExercise(
            id="m1-l2-ex2",
            title="Variable Reassignment & Accumulation",
            difficulty="Application",
            problem_statement="Start with a variable `xp = 120`. Then simulate earning 45 XP by reassigning `xp = xp + 45`. Finally, print the updated XP with the prefix 'Current XP: '.",
            input_output_expectations="Expected stdout:\nCurrent XP: 165",
            starter_code="xp = 120\n\n# Reassign xp by adding 45:\n\n# Print the result:\n",
            hints=[
                "Evaluate the right-hand side first: `xp + 45`.",
                "Assign the new value back to `xp`.",
                "Print with `print(\"Current XP:\", xp)`."
            ],
            test_cases=[
                {"input": "", "expected_output": "Current XP: 165", "description": "Verify variable accumulation and print"}
            ],
            expected_substrings=["xp", "120"],
            solution="xp = 120\nxp = xp + 45\nprint(\"Current XP:\", xp)"
        ),
        PracticeExercise(
            id="m1-l2-ex3",
            title="Object Identity & Memory Verification",
            difficulty="Challenge",
            problem_statement="In Python, integers from -5 to 256 are pre-allocated singletons (small integer cache). Create two variables `a = 250` and `b = 250`. Check if they reference the identical memory address using the `is` keyword and print the boolean result.",
            input_output_expectations="Expected stdout:\nTrue",
            starter_code="a = 250\nb = 250\n\n# Test if a and b refer to the same object using 'is':\n",
            hints=[
                "The `is` operator checks memory identity, unlike `==` which checks value equality.",
                "Write `print(a is b)`.",
                "Because 250 is within the small integer cache, the result will be True."
            ],
            test_cases=[
                {"input": "", "expected_output": "True", "description": "Verify memory identity with `is` keyword"}
            ],
            expected_substrings=["a", "b", "is"],
            solution="a = 250\nb = 250\nprint(a is b)"
        ),
    ],

    # ----------------------------------------------------
    # MODULE 1: LESSON 3 — Type Conversion & Casting
    # ----------------------------------------------------
    "m1-l3": [
        PracticeExercise(
            id="m1-l3-ex1",
            title="String to Integer Arithmetic",
            difficulty="Warmup",
            problem_statement="You received user input as a string `raw_credits = \"15\"`. Convert it to an integer using `int()`, add 3 elective credits, and print the resulting integer.",
            input_output_expectations="Expected stdout:\n18",
            starter_code="raw_credits = \"15\"\n\n# Convert to int and add 3:\n",
            hints=[
                "Use `int(raw_credits)` to convert the string to a numeric integer.",
                "Store the result in a variable or compute directly.",
                "Print the final value 18."
            ],
            test_cases=[
                {"input": "", "expected_output": "18", "description": "Convert string numeric to int and add 3"}
            ],
            expected_substrings=["int", "raw_credits"],
            solution="raw_credits = \"15\"\ntotal_credits = int(raw_credits) + 3\nprint(total_credits)"
        ),
        PracticeExercise(
            id="m1-l3-ex2",
            title="Float to Integer Truncation",
            difficulty="Application",
            problem_statement="A student's raw score is `score = 87.85`. Demonstrate that `int()` truncates the decimal portion rather than rounding. Print both `int(score)` and `round(score)` on separate lines.",
            input_output_expectations="Expected stdout:\n87\n88",
            starter_code="score = 87.85\n\n# Print truncated int, then rounded value:\n",
            hints=[
                "Call `print(int(score))` to see truncation.",
                "Call `print(round(score))` to see standard mathematical rounding."
            ],
            test_cases=[
                {"input": "", "expected_output": "87\n88", "description": "Verify truncation vs rounding behavior"}
            ],
            expected_substrings=["int", "round"],
            solution="score = 87.85\nprint(int(score))\nprint(round(score))"
        ),
        PracticeExercise(
            id="m1-l3-ex3",
            title="Boolean Evaluation of Truthy & Falsy Values",
            difficulty="Challenge",
            problem_statement="In Python, empty structures and 0 evaluate to `False` (falsy), while non-empty values evaluate to `True` (truthy). Convert `0`, `\"\"`, and `\"Python\"` to booleans using `bool()` and print their evaluations separated by spaces or on 3 lines.",
            input_output_expectations="Expected stdout:\nFalse\nFalse\nTrue",
            starter_code="# Challenge 3: Test bool() on 0, empty string, and non-empty string\n",
            hints=[
                "Call `bool(0)`.",
                "Call `bool(\"\")`.",
                "Call `bool(\"Python\")`.",
                "Print each result on its own line."
            ],
            test_cases=[
                {"input": "", "expected_output": "False\nFalse\nTrue", "description": "Verify falsy (0, '') and truthy ('Python') conversions"}
            ],
            expected_substrings=["bool"],
            solution="print(bool(0))\nprint(bool(\"\"))\nprint(bool(\"Python\"))"
        ),
    ],

    # ----------------------------------------------------
    # MODULE 1: LESSON 4 — Operators: Arithmetic, Logic & Precedence
    # ----------------------------------------------------
    "m1-l4": [
        PracticeExercise(
            id="m1-l4-ex1",
            title="Floor Division & Modulus",
            difficulty="Warmup",
            problem_statement="Given 50 total students and a lab capacity of 8 workstations per lab session, compute:\n1. The number of full labs needed using floor division `//`\n2. The remaining students in the final smaller session using modulus `%`\nPrint both numbers on separate lines.",
            input_output_expectations="Expected stdout:\n6\n2",
            starter_code="students = 50\ncapacity = 8\n\n# Compute full labs and remaining students:\n",
            hints=[
                "Use `students // capacity` for integer quotient.",
                "Use `students % capacity` for remainder.",
                "Print both values."
            ],
            test_cases=[
                {"input": "", "expected_output": "6\n2", "description": "Verify floor division and remainder"}
            ],
            expected_substrings=["//", "%"],
            solution="students = 50\ncapacity = 8\nprint(students // capacity)\nprint(students % capacity)"
        ),
        PracticeExercise(
            id="m1-l4-ex2",
            title="Operator Precedence",
            difficulty="Application",
            problem_statement="Without changing the numbers or operators, use parentheses `()` in the expression `10 + 5 * 2 ** 3` to force the addition `(10 + 5)` to evaluate first, multiplied by `2 ** 3` (8). Print the computed integer.",
            input_output_expectations="Expected stdout:\n120",
            starter_code="# Challenge 2: Parentheses override natural precedence (** > * > +)\n# Modify with parentheses:\nresult = 10 + 5 * 2 ** 3\nprint(result)\n",
            hints=[
                "Add parentheses around `(10 + 5)`.",
                "Python evaluates `(10 + 5)` first (15), then `2 ** 3` (8), yielding 15 * 8 = 120."
            ],
            test_cases=[
                {"input": "", "expected_output": "120", "description": "Verify precedence override yielding 120"}
            ],
            expected_substrings=["(10 + 5)"],
            solution="result = (10 + 5) * 2 ** 3\nprint(result)"
        ),
        PracticeExercise(
            id="m1-l4-ex3",
            title="Logical Guard Clauses with 'and' / 'or'",
            difficulty="Challenge",
            problem_statement="Define `has_id_card = True`, `has_fee_receipt = False`, and `is_faculty_approved = True`. A student can enter if they have their ID card AND (either fee receipt OR faculty approval). Evaluate this condition using Python's `and` and `or` operators and print the boolean result.",
            input_output_expectations="Expected stdout:\nTrue",
            starter_code="has_id_card = True\nhas_fee_receipt = False\nis_faculty_approved = True\n\n# Formulate logic condition:\ncan_enter = has_id_card and (has_fee_receipt or is_faculty_approved)\nprint(can_enter)\n",
            hints=[
                "Use `and` between the mandatory ID check and the alternative permissions.",
                "Wrap the `(has_fee_receipt or is_faculty_approved)` inside parentheses.",
                "Print the resulting boolean."
            ],
            test_cases=[
                {"input": "", "expected_output": "True", "description": "Verify boolean expression with combined and/or"}
            ],
            expected_substrings=["and", "or", "print"],
            solution="has_id_card = True\nhas_fee_receipt = False\nis_faculty_approved = True\ncan_enter = has_id_card and (has_fee_receipt or is_faculty_approved)\nprint(can_enter)"
        ),
    ],

    # ----------------------------------------------------
    # MODULE 1: LESSON 5 — Formatted Output with f-strings & User Input
    # ----------------------------------------------------
    "m1-l5": [
        PracticeExercise(
            id="m1-l5-ex1",
            title="Precision Number Formatting with f-strings",
            difficulty="Warmup",
            problem_statement="Given `temperature = 36.66666`, use an f-string to format and print the temperature to exactly 2 decimal places with the unit '°C': 'Body Temp: 36.67°C'.",
            input_output_expectations="Expected stdout:\nBody Temp: 36.67°C",
            starter_code="temperature = 36.66666\n\n# Format with f-string to 2 decimal places:\n",
            hints=[
                "Use `{temperature:.2f}` inside an f-string.",
                "Prefix string with `f\"...\"`.",
                "Ensure the output matches 'Body Temp: 36.67°C'."
            ],
            test_cases=[
                {"input": "", "expected_output": "Body Temp: 36.67°C", "description": "Verify floating-point format to 2 decimal places"}
            ],
            expected_substrings=["f\"", ":.2f"],
            solution="temperature = 36.66666\nprint(f\"Body Temp: {temperature:.2f}°C\")"
        ),
        PracticeExercise(
            id="m1-l5-ex2",
            title="Tabular Alignment & Width Specifiers",
            difficulty="Application",
            problem_statement="Using f-string alignment specifiers (`<` for left-align, `>` for right-align), print a clean receipt line with product 'Keyboard' in a 12-character field and price 49.99 right-aligned in an 8-character field formatted with 2 decimal places: `f\"{item:<12}${price:>8.2f}\"`.",
            input_output_expectations="Expected stdout:\nKeyboard    $   49.99",
            starter_code="item = \"Keyboard\"\nprice = 49.99\n\n# Format using width specifiers:\nline = f\"{item:<12}${price:>8.2f}\"\nprint(line)\n",
            hints=[
                "`<12` pads with spaces up to 12 characters on the right.",
                "`>8.2f` right aligns the floating-point number in an 8-character width.",
                "Print the resulting string."
            ],
            test_cases=[
                {"input": "", "expected_output": "Keyboard    $   49.99", "description": "Verify f-string alignment and fixed-width formatting"}
            ],
            expected_substrings=["f\"", "<12", ">8.2f"],
            solution="item = \"Keyboard\"\nprice = 49.99\nline = f\"{item:<12}${price:>8.2f}\"\nprint(line)"
        ),
        PracticeExercise(
            id="m1-l5-ex3",
            title="Formatted Academic Summary Card",
            difficulty="Challenge",
            problem_statement="Given learner information `name = 'Maya'`, `course = '01AP0303'`, `score = 92.5`, format and print a multi-line academic status card:\nSTUDENT: Maya\nCOURSE: 01AP0303\nRESULT: 92.5% [DISTINCTION]",
            input_output_expectations="Expected stdout:\nSTUDENT: Maya\nCOURSE: 01AP0303\nRESULT: 92.5% [DISTINCTION]",
            starter_code="name = \"Maya\"\ncourse = \"01AP0303\"\nscore = 92.5\nstatus = \"DISTINCTION\"\n\n# Build and print the formatted summary:\n",
            hints=[
                "Use f-strings for each line or a triple-quoted multi-line f-string.",
                "Ensure exact casing and spacing: 'STUDENT: Maya', 'COURSE: 01AP0303', 'RESULT: 92.5% [DISTINCTION]'."
            ],
            test_cases=[
                {"input": "", "expected_output": "STUDENT: Maya\nCOURSE: 01AP0303\nRESULT: 92.5% [DISTINCTION]", "description": "Verify multi-line academic status report formatting"}
            ],
            expected_substrings=["STUDENT:", "COURSE:", "RESULT:"],
            solution="name = \"Maya\"\ncourse = \"01AP0303\"\nscore = 92.5\nstatus = \"DISTINCTION\"\nprint(f\"STUDENT: {name}\")\nprint(f\"COURSE: {course}\")\nprint(f\"RESULT: {score}% [{status}]\")"
        ),
    ]
}


def get_lesson_challenges(lesson_id: str, fallback_exercises: Optional[List[PracticeExercise]] = None) -> List[PracticeExercise]:
    """
    Retrieve three targeted challenges for the specified lesson.
    If custom challenges are not explicitly registered, generates 3 structured challenges
    from the module's practice exercises or generic templates.
    """
    if lesson_id in LESSON_CHALLENGES:
        return LESSON_CHALLENGES[lesson_id]

    if fallback_exercises and len(fallback_exercises) >= 3:
        return fallback_exercises[:3]

    # Generate progressive default challenges based on fallback exercises
    base = fallback_exercises or []
    results = list(base)
    
    if len(results) < 1:
        results.append(
            PracticeExercise(
                id=f"{lesson_id}-ex1",
                title="Syntax Foundations",
                difficulty="Warmup",
                problem_statement="Implement the core concept demonstrated in this lesson. Define the required variables and print the result.",
                input_output_expectations="Execute successfully without syntax errors.",
                starter_code="# Practice Warmup\n# Apply the syntax learned in the reading:\nprint('Concept verified')\n",
                hints=["Follow the example from the 'See It in Python' section."],
                test_cases=[{"input": "", "expected_output": "Concept verified", "description": "Verify correct syntax and output"}],
                expected_substrings=["print"],
                solution="print('Concept verified')"
            )
        )
    if len(results) < 2:
        results.append(
            PracticeExercise(
                id=f"{lesson_id}-ex2",
                title="Practical Application",
                difficulty="Application",
                problem_statement="Write a solution that processes input data and produces verified output according to syllabus standards.",
                input_output_expectations="Expected stdout matches verified problem expectations.",
                starter_code="# Practical Application\nvalue = 42\nprint('Processed:', value)\n",
                hints=["Double check operators, types, and expected variable values."],
                test_cases=[{"input": "", "expected_output": "Processed: 42", "description": "Verify application logic"}],
                expected_substrings=["print"],
                solution="value = 42\nprint('Processed:', value)"
            )
        )
    if len(results) < 3:
        results.append(
            PracticeExercise(
                id=f"{lesson_id}-ex3",
                title="Edge Case & Validation",
                difficulty="Challenge",
                problem_statement="Handle edge conditions, format edge outputs, and ensure zero runtime errors under boundary testing.",
                input_output_expectations="Clean output under boundary conditions.",
                starter_code="# Edge Case Challenge\ndata = [1, 2, 3]\nprint('Count:', len(data))\n",
                hints=["Check boundary values such as 0, empty sequences, or negative numbers."],
                test_cases=[{"input": "", "expected_output": "Count: 3", "description": "Verify edge case handling"}],
                expected_substrings=["print"],
                solution="data = [1, 2, 3]\nprint('Count:', len(data))"
            )
        )
    return results[:3]

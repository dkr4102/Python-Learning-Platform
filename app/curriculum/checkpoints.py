"""
Curriculum lesson checkpoints registry.
Provides 2-3 focused, diagnostic conceptual assessment questions per lesson with:
- One-question-at-a-time flow
- Clear options
- Immediate feedback & diagnostic explanations
- Retry behavior on incorrect attempts
- Completion certification only after passing
"""
from typing import Dict, List, Optional
from app.curriculum.models import MiniCheckpoint


LESSON_CHECKPOINTS: Dict[str, List[MiniCheckpoint]] = {
    "m1-l1": [
        MiniCheckpoint(
            question="What happens when CPython executes a Python script (.py file)?",
            options=[
                "It immediately converts the script directly into binary x86/ARM CPU machine code without an interpreter.",
                "It compiles the source code into bytecode (.pyc) which is then executed sequentially by the Python Virtual Machine (PVM).",
                "It sends the script to a web browser engine to run as JavaScript.",
                "It requires manual linking with a C compiler before any output can appear."
            ],
            correct_index=1,
            explanation="CPython follows a two-stage execution architecture: the compiler first parses and compiles source code into low-level platform-independent bytecode instructions, which the Python Virtual Machine (PVM) runtime loop evaluates."
        ),
        MiniCheckpoint(
            question="Why does Python strictly enforce 4-space indentation for code blocks?",
            options=[
                "Indentation is purely cosmetic and the interpreter ignores it during execution.",
                "Indentation defines block structure and scope, replacing curly braces {} used in C++ or Java.",
                "Indentation is only required for function headers, not conditional statements.",
                "CPython requires tabs instead of spaces for indentation."
            ],
            correct_index=1,
            explanation="In Python, whitespace is syntactically meaningful. Consistent indentation (conventionally 4 spaces) defines code blocks and hierarchy, enforcing visual readability and preventing dangling block bugs."
        ),
    ],
    "m1-l2": [
        MiniCheckpoint(
            question="In the assignment statement `score = 42`, how does Python manage memory and naming?",
            options=[
                "Python evaluates 42, stores it in memory, and binds the name label `score` as a reference to that integer object.",
                "Python allocates fixed memory for the name `score` and converts the name itself into a number.",
                "The `=` operator checks whether `score` is equal to 42.",
                "Python only allows variable names that are a single character long."
            ],
            correct_index=0,
            explanation="In Python, variables are names (references) bound to objects in memory. The single equals sign `=` evaluates the expression on the right first, then binds the label on the left to that value."
        ),
        MiniCheckpoint(
            question="What happens when you reassign `score = score + 10`?",
            options=[
                "Python throws an error because variables are permanently immutable constants.",
                "Python reads the existing value, computes the new sum, and rebinds the label `score` to the new integer object.",
                "Python creates a second variable named `score_2` automatically.",
                "The memory address of the number 42 is permanently changed in place."
            ],
            correct_index=1,
            explanation="Reassignment calculates the right side (`score + 10`) using the current value, creates a new integer object for the result, and updates the reference `score` to point to the new object."
        ),
    ],
    "m1-l3": [
        MiniCheckpoint(
            question="What is the result of calling `int(9.99)` in Python?",
            options=[
                "It rounds up to 10 using standard ceiling rules.",
                "It truncates the decimal portion completely, returning integer 9.",
                "It throws a ValueError because floats cannot be passed to int().",
                "It returns 9.0 as a floating point number."
            ],
            correct_index=1,
            explanation="`int()` performs truncation toward zero when converting floating-point numbers to integers. It discards the fractional part completely, yielding `9`."
        ),
        MiniCheckpoint(
            question="Which of the following values evaluates to `False` when passed to `bool()`?",
            options=[
                "\"0\" (a string containing the character zero)",
                "[0] (a list containing the number zero)",
                "\"\" (an empty string)",
                "\"False\" (a string with the word False)"
            ],
            correct_index=2,
            explanation="In Python, empty collections and empty strings `\"\"` evaluate to `False` (falsy). Non-empty strings such as `\"0\"` or `\"False\"` evaluate to `True` (truthy)."
        ),
    ],
    "m1-l4": [
        MiniCheckpoint(
            question="What is the output of `17 // 5` versus `17 % 5` in Python?",
            options=[
                "3.4 and 2",
                "3 and 2",
                "3 and 3",
                "2 and 3"
            ],
            correct_index=1,
            explanation="`//` is floor division which returns the integer quotient `3`. `%` is the modulus operator which returns the integer remainder `2` (since 17 = 3 * 5 + 2)."
        ),
        MiniCheckpoint(
            question="According to Python operator precedence, what is the result of `2 + 3 * 4`?",
            options=[
                "20 (evaluated left to right as (2 + 3) * 4)",
                "14 (evaluated with multiplication taking precedence over addition)",
                "24 (evaluated with addition taking precedence)",
                "Throws a PrecedenceError"
            ],
            correct_index=1,
            explanation="Multiplication (`*`) has higher precedence than addition (`+`). CPython evaluates `3 * 4` first (12), then adds `2`, producing `14`."
        ),
    ],
    "m1-l5": [
        MiniCheckpoint(
            question="How do f-strings format an expression in Python 3.6+?",
            options=[
                "By prefixing the string with `f` and placing expressions inside curly braces `{}`.",
                "By using `%s` placeholders at the end of the string.",
                "By using `string.format()` calls only.",
                "By placing dollar signs `$variable` inside the string."
            ],
            correct_index=0,
            explanation="f-strings (formatted string literals) use the `f\"...\"` prefix and evaluate Python expressions placed directly inside curly braces `{expression}` at runtime."
        ),
        MiniCheckpoint(
            question="What does the format specifier `{pi:.2f}` produce when `pi = 3.14159`?",
            options=[
                "\"3.14\"",
                "\"3.14159\"",
                "\"3.1\"",
                "\"3.142\""
            ],
            correct_index=0,
            explanation="The specifier `:.2f` formats a floating-point number with fixed-point notation rounded to 2 decimal places, producing `\"3.14\"`."
        ),
    ]
}


def get_lesson_checkpoints(lesson_id: str, default_checkpoint: Optional[MiniCheckpoint] = None) -> List[MiniCheckpoint]:
    """
    Retrieve the focused checkpoint questions for the lesson.
    Falls back to the lesson's default mini_checkpoint if present.
    """
    if lesson_id in LESSON_CHECKPOINTS:
        return LESSON_CHECKPOINTS[lesson_id]
    if default_checkpoint:
        return [default_checkpoint]
    return [
        MiniCheckpoint(
            question="What is the primary concept taught in this lesson?",
            options=[
                "Understanding the core syntax and applying it correctly.",
                "Memorizing commands without understanding their behavior.",
                "Ignoring error messages produced by the Python interpreter.",
                "Writing complex code without testing individual statements."
            ],
            correct_index=0,
            explanation="Pip Learn emphasizes concept mastery, predicting outputs, and testing individual statements systematically."
        )
    ]

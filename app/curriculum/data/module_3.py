"""
Module 3: Data Structures
Marwadi University 01AP0303 - Unit 3 (6 Contact Hours, 12 Marks Assessment)
Mini-Project: Inventory Management Tracker & Student Grade Analyzer
"""
from app.curriculum.models import Module, Lesson, PracticeExercise, QuizQuestion, ProjectInfo, CommonMistake, MiniCheckpoint

MODULE_3 = Module(
    id=3,
    code="MOD-03",
    title="Data Structures",
    syllabus_unit="Unit 3: Lists, Tuples, Sets, Dictionaries & Strings",
    contact_hours=6,
    assessment_marks=12,
    description="Explore Python's built-in collection types: mutable lists, hash-based sets and dictionaries, immutable tuples, string slicing, and comprehension expressions.",
    learning_objectives=[
        "Manipulate lists with slicing, in-place sorting, list comprehensions, and nested matrices",
        "Utilize immutable tuples for data integrity and tuple packing/unpacking",
        "Leverage set theory operations: union, intersection, difference, and uniqueness guarantees",
        "Construct high-performance key-value lookups with dictionaries and nested records",
        "Perform advanced string manipulations: formatting, tokenization, slicing, and validation"
    ],
    topics_covered=[
        "Lists: Dynamic Arrays, Indexing, Slicing & Methods",
        "List Comprehensions & Transformation Pipelines",
        "Tuples: Immutability & Structural Unpacking",
        "Sets: O(1) Hash Lookups & Set Operations",
        "Dictionaries: Key-Value Mapping & Iteration",
        "String Manipulation: Methods, Slicing & Joining",
        "Nested Data Structures (Lists of Dicts, JSON-like trees)"
    ],
    artwork_id="ART-07",
    project=ProjectInfo(
        id="proj-inventory-tracker",
        title="Inventory Management Tracker",
        subtitle="Stock Level, Reorder Alerts & Category Analytics Engine",
        objective="Construct a robust inventory tracking platform using nested dictionaries and list operations to manage warehouse catalog items, update stock counts, issue reorder warnings, and calculate valuation.",
        requirements=[
            "Support SKU-based item addition, updating, and removal",
            "Track item name, category, unit price, and stock count",
            "Generate automatic reorder warnings when stock falls below threshold",
            "Calculate total inventory valuation by category",
            "Include Student Grade Analyzer activity as a companion data analysis tool"
        ],
        starter_snippet="""# Module 3 Project: Inventory Tracker
inventory = {
    "SKU-001": {"name": "Mechanical Keyboard", "category": "Electronics", "price": 75.0, "stock": 14},
    "SKU-002": {"name": "USB-C Hub", "category": "Accessories", "price": 28.5, "stock": 4}
}

def check_reorders(inv, threshold=5):
    return [item["name"] for sku, item in inv.items() if item["stock"] < threshold]
""",
        module_id=3
    ),
    lessons=[
        Lesson(
            id="m3-l1",
            title="Lists: Indexing, Slicing & Comprehensions",
            subtitle="Mastering dynamic arrays, negative indexing, and concise list comprehensions.",
            reading_time_min=7,
            concept_markdown="""### The Python List: Dynamic Heterogeneous Arrays

A `list` in Python is an ordered, mutable sequence of object pointers.

```python
# List indexing (0-based) and negative indexing (-1 is the last item)
fruits = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]
#           0        1         2        3         4
#          -5       -4        -3       -2        -1
```

#### Slicing Syntax: `sequence[start:stop:step]`
- `fruits[1:4]` -> `['Banana', 'Cherry', 'Date']` (excludes stop index 4)
- `fruits[:3]` -> First 3 elements
- `fruits[::-1]` -> Reverses the list!

#### List Comprehensions: Expressive Transformations
Instead of writing multi-line loop accumulator boilerplate:
```python
# Boilerplate
squares = []
for x in range(6):
    if x % 2 == 0:
        squares.append(x ** 2)

# Pythonic List Comprehension: [expression for item in iterable if condition]
squares = [x ** 2 for x in range(6) if x % 2 == 0]  # [0, 4, 16]
```
""",
            syntax_example="""# List operations and comprehensions
scores = [78, 92, 85, 64, 89, 95]
high_scores = [s for s in scores if s >= 85]
grades = ["Pass" if s >= 70 else "Review" for s in scores]

print("High scores:", high_scores)
print("Grades:", grades)
""",
            executable_code="""# Executable list slicing and comprehension demo
languages = ["Python", "JavaScript", "C++", "Rust", "Go", "Kotlin"]

print("Original:", languages)
print("Slice [1:4]:", languages[1:4])
print("Every second item [::2]:", languages[::2])
print("Reversed [::-1]:", languages[::-1])

# Transform with comprehension
upper_short = [lang.upper() for lang in languages if len(lang) <= 4]
print("Short languages (<= 4 chars, uppercase):", upper_short)
""",
            expected_output="""Original: ['Python', 'JavaScript', 'C++', 'Rust', 'Go', 'Kotlin']
Slice [1:4]: ['JavaScript', 'C++', 'Rust']
Every second item [::2]: ['Python', 'C++', 'Go']
Reversed [::-1]: ['Kotlin', 'Go', 'Rust', 'C++', 'JavaScript', 'Python']
Short languages (<= 4 chars, uppercase): ['C++', 'RUST', 'GO']""",
            output_explanation="Slicing extracts subsequences cleanly without mutating the original list. Slicing with step -1 creates a reversed copy.",
            common_mistakes=[
                CommonMistake(
                    mistake="Assigning a copy via new_list = old_list",
                    explanation="This copies the object reference, NOT the contents! Modifying new_list will mutate old_list.",
                    correction="Use a shallow slice copy: new_list = old_list[:] or new_list = list(old_list)."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What does the slice `numbers[::-1]` do to a list?",
                options=[
                    "Returns a list with only the first element",
                    "Returns a new list with elements in reverse order",
                    "Raises a SliceStepError",
                    "Deletes all negative numbers"
                ],
                correct_index=1,
                explanation="A slice step of -1 iterates through the sequence backwards from end to start."
            )
        ),
        Lesson(
            id="m3-l2",
            title="Tuples & Immutability",
            subtitle="Fixed records, packing, unpacking, and dictionary key compatibility.",
            reading_time_min=5,
            concept_markdown="""### Tuples: The Immutable Sequence

A `tuple` is an ordered collection that **cannot be modified after creation**.

```python
# Defined with parentheses (or bare commas)
point = (10, 20)
rgb = (255, 128, 0)
single_item = (42,)  # Note trailing comma!
```

#### Why use Tuples over Lists?
1. **Data Integrity / Defense**: Guarantees that records (e.g. database rows, geometric coordinates) cannot be accidentally altered.
2. **Hashability**: Because they are immutable, tuples containing immutable types can be used as **keys in dictionaries** or stored in sets.
3. **Memory & Performance**: Tuples have slightly smaller memory footprints and faster construction times than lists.

#### Tuple Packing and Unpacking
```python
# Multiple return values from functions are packed tuples
def get_user_stats():
    return "Aarav", 94, "First Class"  # Packed tuple

name, score, rank = get_user_stats()  # Unpacked directly!
```
""",
            syntax_example="""# Tuple unpacking and swap trick
a = 10
b = 20
a, b = b, a  # Idiomatic Python swap via tuple packing/unpacking
print(f"a = {a}, b = {b}")
""",
            executable_code="""# Executable tuple demonstration
geo_location = ("Marwadi University", 22.3693, 70.7981)
campus, lat, lon = geo_location

print(f"Location: {campus}")
print(f"Coordinates: {lat}° N, {lon}° E")

# Using tuples as dictionary keys
grid_map = {
    (0, 0): "Origin Point",
    (1, 2): "Lecture Hall A",
    (2, 3): "Computer Science Lab"
}
print("Grid Lookup (1, 2):", grid_map[(1, 2)])
""",
            expected_output="""Location: Marwadi University
Coordinates: 22.3693° N, 70.7981° E
Grid Lookup (1, 2): Lecture Hall A""",
            output_explanation="Tuple unpacking binds variables to elements in order. Because coordinates (1, 2) are immutable, they serve as valid hashable dictionary keys.",
            common_mistakes=[
                CommonMistake(
                    mistake="Trying to create a 1-element tuple with `t = (5)`",
                    explanation="(5) evaluates as parenthesized integer 5, not a tuple.",
                    correction="Include a trailing comma: `t = (5,)`."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="Can a Python list be used as a dictionary key?",
                options=[
                    "Yes, any object can be a dictionary key",
                    "No, because lists are mutable and unhashable",
                    "Yes, but only if the list has fewer than 5 items",
                    "Only if sorted"
                ],
                correct_index=1,
                explanation="Dictionary keys must be hashable and immutable. Lists are mutable, raising TypeError: unhashable type: 'list'."
            )
        ),
        Lesson(
            id="m3-l3",
            title="Sets: Fast Lookups & Mathematical Set Theory",
            subtitle="Hash sets, uniqueness, union, intersection, and symmetric difference.",
            reading_time_min=6,
            concept_markdown="""### The Python Set: Unordered Unique Elements

A `set` is an unordered collection of unique, hashable objects. Membership testing (`x in my_set`) operates in **average O(1) constant time** compared to O(N) linear time for lists.

```python
# Definition with curly braces or set() constructor
enrolled_python = {"Aarav", "Priya", "Rohan", "Sneha"}
enrolled_java = {"Rohan", "Sneha", "Vikram", "Ananya"}
```

#### Set Operations:
- **Union (`|` or `.union()`)**: All elements from both sets.
- **Intersection (`&` or `.intersection()`)**: Elements present in both sets.
- **Difference (`-` or `.difference()`)**: Elements in set A but not set B.
- **Symmetric Difference (`^` or `.symmetric_difference()`)**: Elements in either set, but not both.
""",
            syntax_example="""# Deduplicating list and set operations
raw_tags = ["python", "code", "python", "ai", "web", "ai"]
unique_tags = set(raw_tags)
print("Unique tags:", unique_tags)
""",
            executable_code="""# Executable set operations
py_students = {"Aarav", "Priya", "Rohan", "Sneha"}
db_students = {"Rohan", "Sneha", "Vikram", "Ananya"}

both_courses = py_students & db_students
only_python = py_students - db_students
all_unique = py_students | db_students

print("Enrolled in BOTH:", sorted(list(both_courses)))
print("Enrolled ONLY in Python:", sorted(list(only_python)))
print("Total Unique Learners:", len(all_unique))
""",
            expected_output="""Enrolled in BOTH: ['Rohan', 'Sneha']
Enrolled ONLY in Python: ['Aarav', 'Priya']
Total Unique Learners: 6""",
            output_explanation="Set intersection (&) isolates learners enrolled in both courses. Set difference (-) filters out anyone taking database connectivity.",
            common_mistakes=[
                CommonMistake(
                    mistake="Initializing an empty set with `s = {}`",
                    explanation="In Python, `{}` creates an empty dictionary, not an empty set.",
                    correction="Use `s = set()` to initialize an empty set."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What is the average time complexity of checking membership `item in my_collection` for a set vs a list?",
                options=[
                    "O(1) for set, O(N) for list",
                    "O(N) for set, O(1) for list",
                    "O(N^2) for both",
                    "O(log N) for both"
                ],
                correct_index=0,
                explanation="Sets use hash tables offering O(1) average lookup, whereas lists require checking each element sequentially (O(N))."
            )
        ),
        Lesson(
            id="m3-l4",
            title="Dictionaries: Key-Value Architecture & Nested Records",
            subtitle="Hash maps, safe lookups with .get(), iteration patterns, and dictionary comprehensions.",
            reading_time_min=7,
            concept_markdown="""### The Python Dictionary: Fast Key-Value Hash Tables

Dictionaries (`dict`) store associations between unique immutable keys and arbitrary values.

```python
student = {
    "name": "Priya Patel",
    "id": 240101,
    "scores": {"quiz": 92, "lab": 96, "final": 90}
}
```

#### Safe Access with `.get()`
Accessing `student["gpa"]` when the key does not exist raises a fatal `KeyError`. Use `.get(key, default)`:
```python
gpa = student.get("gpa", 0.0)  # Returns 0.0 without crashing
```

#### Iterating Over Dictionaries:
- `for key in dict:` iterates keys
- `for value in dict.values():` iterates values
- `for key, value in dict.items():` iterates both simultaneously!

#### Dictionary Comprehensions:
```python
names = ["Aarav", "Priya", "Rohan"]
grades = [88, 95, 78]
gradebook = {name: grade for name, grade in zip(names, grades)}
```
""",
            syntax_example="""# Updating and filtering dictionaries
stock = {"laptops": 12, "monitors": 4, "keyboards": 25}
# Filter items needing reorder (< 5 units)
reorder_items = {k: v for k, v in stock.items() if v < 5}
print("Reorder needed:", reorder_items)
""",
            executable_code="""# Executable dictionary and nested lookup demo
course_catalog = {
    "01AP0303": {
        "title": "Programming with Python",
        "units": 8,
        "hours": 45,
        "faculty": "Marwadi University Dept. of CSE"
    },
    "01AP0304": {
        "title": "Database Management Systems",
        "units": 6,
        "hours": 40,
        "faculty": "Dept. of IT"
    }
}

for code, info in course_catalog.items():
    print(f"[{code}] {info['title']} - {info['hours']} Contact Hours ({info['faculty']})")
""",
            expected_output="""[01AP0303] Programming with Python - 45 Contact Hours (Marwadi University Dept. of CSE)
[01AP0304] Database Management Systems - 40 Contact Hours (Dept. of IT)""",
            output_explanation="The loop unpacks the key (code) and value (nested dictionary), formatting the details into a clear summary.",
            common_mistakes=[
                CommonMistake(
                    mistake="Modifying a dictionary's keys while iterating over it",
                    explanation="for k in my_dict: if condition: del my_dict[k] raises RuntimeError: dictionary changed size during iteration.",
                    correction="Iterate over a copy of the keys: for k in list(my_dict.keys()):"
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="Why is `my_dict.get('status', 'Pending')` safer than `my_dict['status']`?",
                options=[
                    "It encrypts the key",
                    "It avoids raising a KeyError if 'status' does not exist, returning 'Pending' instead",
                    "It converts the value to an integer",
                    "It deletes the key after reading"
                ],
                correct_index=1,
                explanation="The `.get()` method provides a graceful fallback without crashing if the key is missing."
            )
        ),
        Lesson(
            id="m3-l5",
            title="String Processing & Slicing",
            subtitle="Text transformations, split/join pipelines, stripping whitespace, and searching.",
            reading_time_min=6,
            concept_markdown="""### Strings: Immutable Character Sequences

In Python, strings are immutable sequences of Unicode characters. Slicing and indexing behave identically to lists.

#### Common String Methods:
- `.strip()`: Remove leading and trailing whitespace.
- `.split(delimiter)`: Tokenize string into a list of words.
- `delimiter.join(iterable)`: Join list of strings into one string.
- `.upper()`, `.lower()`, `.title()`: Case transformations.
- `.startswith(prefix)`, `.endswith(suffix)`: Boolean prefix/suffix inspection.
- `.replace(old, new)`: Replace occurrences.
- `.find(substr)`: Return lowest index or -1 if not found.
""",
            syntax_example="""# Tokenize CSV record and clean fields
raw_record = "  240101 , Priya Patel , 94.5 , Computer Science  "
fields = [field.strip() for field in raw_record.split(",")]
cleaned_csv = ",".join(fields)
print("Cleaned:", cleaned_csv)
""",
            executable_code="""# Executable string manipulation demo
sentence = "Python is powerful, expressive, and elegant."
words = sentence.replace(".", "").split(", ")
print("Extracted words:", words)

# Join with bullet separator
formatted_bullet = " • ".join(words)
print("Formatted:", formatted_bullet)

# Check substring and title-case
print("Contains 'expressive':", "expressive" in sentence)
print("Title case:", sentence.title())
""",
            expected_output="""Extracted words: ['Python is powerful', 'expressive', 'and elegant']
Formatted: Python is powerful • expressive • and elegant
Contains 'expressive': True
Title case: Python Is Powerful, Expressive, And Elegant.""",
            output_explanation="String methods create new strings without altering the immutable original string.",
            common_mistakes=[
                CommonMistake(
                    mistake="Attempting in-place modification: s = 'Hello'; s[0] = 'J'",
                    explanation="Python strings are immutable, raising TypeError: 'str' object does not support item assignment.",
                    correction="Construct a new string: s = 'J' + s[1:]."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What method combines a list of strings `['A', 'B', 'C']` into a single string separated by hyphens `'A-B-C'`?",
                options=[
                    "'-'.join(['A', 'B', 'C'])",
                    "['A', 'B', 'C'].split('-')",
                    "join('-', ['A', 'B', 'C'])",
                    "['A', 'B', 'C'].concat('-')"
                ],
                correct_index=0,
                explanation="The delimiter string calls `.join(iterable)`, producing 'A-B-C'."
            )
        )
    ],
    practice_exercises=[
        PracticeExercise(
            id="m3-ex1",
            title="Student Grade Analyzer",
            difficulty="Beginner",
            problem_statement="Given a dictionary of student scores: `scores = {'Aarav': 88, 'Priya': 95, 'Rohan': 72, 'Sneha': 90}`, calculate the class average, identify the student with the highest score, and identify the student with the lowest score.",
            input_output_expectations="Expected stdout must include: Average: 86.25, Highest: Priya (95), Lowest: Rohan (72)",
            starter_code="""scores = {'Aarav': 88, 'Priya': 95, 'Rohan': 72, 'Sneha': 90}

# Calculate average, highest, lowest
avg = sum(scores.values()) / len(scores)
highest_student = max(scores, key=scores.get)
lowest_student = min(scores, key=scores.get)

print(f"Average: {avg:.2f}")
print(f"Highest: {highest_student} ({scores[highest_student]})")
print(f"Lowest: {lowest_student} ({scores[lowest_student]})")
""",
            hints=[
                "sum(scores.values()) gives total marks",
                "max(scores, key=scores.get) returns the student name with the highest score"
            ],
            test_cases=[
                {"input": "", "expected_output": "Average: 86.25", "description": "Verify average calculation"},
                {"input": "", "expected_output": "Highest: Priya (95)", "description": "Verify highest student"},
                {"input": "", "expected_output": "Lowest: Rohan (72)", "description": "Verify lowest student"}
            ],
            expected_substrings=["scores", "highest_student"],
            solution="""scores = {'Aarav': 88, 'Priya': 95, 'Rohan': 72, 'Sneha': 90}
avg = sum(scores.values()) / len(scores)
highest_student = max(scores, key=scores.get)
lowest_student = min(scores, key=scores.get)

print(f"Average: {avg:.2f}")
print(f"Highest: {highest_student} ({scores[highest_student]})")
print(f"Lowest: {lowest_student} ({scores[lowest_student]})")
"""
        ),
        PracticeExercise(
            id="m3-ex2",
            title="List Deduplication and Frequency Counter",
            difficulty="Intermediate",
            problem_statement="Write a program that takes a list of words: `words = ['python', 'code', 'data', 'python', 'ai', 'data', 'python']`, builds a dictionary of word frequencies, and sorts the unique words alphabetically.",
            input_output_expectations="Frequency of 'python' must be 3, and sorted unique words must be: ['ai', 'code', 'data', 'python']",
            starter_code="""words = ['python', 'code', 'data', 'python', 'ai', 'data', 'python']

counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1

unique_sorted = sorted(list(set(words)))

print("Frequencies:", counts)
print("Sorted Unique:", unique_sorted)
""",
            hints=[
                "Use counts[w] = counts.get(w, 0) + 1 to accumulate counts",
                "sorted(list(set(words))) yields alphabetically sorted unique items"
            ],
            test_cases=[
                {"input": "", "expected_output": "'python': 3", "description": "Python count = 3"},
                {"input": "", "expected_output": "['ai', 'code', 'data', 'python']", "description": "Sorted unique list"}
            ],
            expected_substrings=["counts", "unique_sorted"],
            solution="""words = ['python', 'code', 'data', 'python', 'ai', 'data', 'python']
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1
unique_sorted = sorted(list(set(words)))
print("Frequencies:", counts)
print("Sorted Unique:", unique_sorted)
"""
        )
    ],
    quiz_questions=[
        QuizQuestion(
            id="m3-q1",
            question="Which data structure in Python is mutable and maintains insertion order (as of Python 3.7+)?",
            options=[
                "Tuple",
                "Dictionary",
                "Frozenset",
                "String"
            ],
            correct_index=1,
            explanation="Dictionaries in Python 3.7+ are guaranteed to maintain insertion order while being mutable."
        ),
        QuizQuestion(
            id="m3-q2",
            question="What is the result of expression: {1, 2, 3} & {2, 3, 4}?",
            options=[
                "{1, 4}",
                "{2, 3}",
                "{1, 2, 3, 4}",
                "TypeError"
            ],
            correct_index=1,
            explanation="The '&' operator computes set intersection, isolating elements common to both sets ({2, 3})."
        ),
        QuizQuestion(
            id="m3-q3",
            question="Which method safely retrieves a dictionary value without raising KeyError if the key is absent?",
            options=[
                "dict.fetch(key)",
                "dict.get(key, default)",
                "dict.find(key)",
                "dict.search(key)"
            ],
            correct_index=1,
            explanation="dict.get(key, default) gracefully returns the default value (or None) if key is not found."
        ),
        QuizQuestion(
            id="m3-q4",
            question="How do you reverse a list `items` in-place without creating a new copy?",
            options=[
                "items[::-1]",
                "items.reverse()",
                "reversed(items)",
                "items.sort(reverse=False)"
            ],
            correct_index=1,
            explanation="items.reverse() mutates the list in-place, returning None. items[::-1] creates a new list copy."
        ),
        QuizQuestion(
            id="m3-q5",
            question="What is the output of `'python'.upper()[:3]`?",
            options=[
                "'PYT'",
                "'PYTHON'",
                "'pyt'",
                "'P'"
            ],
            correct_index=0,
            explanation="'python'.upper() yields 'PYTHON'. Slicing [:3] takes the first 3 characters: 'PYT'."
        )
    ]
)

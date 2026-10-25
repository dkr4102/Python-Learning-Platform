"""Pip Learn curriculum 2026.1.

This is the authoritative, dependency-ordered curriculum.  The former module
files remain importable only as a source of module/project metadata while old
learner records are migrated under the ``legacy-v1`` curriculum namespace.
"""
from __future__ import annotations

from typing import Dict, List

from app.curriculum.models import (
    CommonMistake, ContentSection, Experiment, Lesson, MiniCheckpoint, Module,
    PracticeExercise, ProjectInfo, QuizQuestion,
)
from app.curriculum.data.module_1 import MODULE_1 as OLD_1
from app.curriculum.data.module_2 import MODULE_2 as OLD_2
from app.curriculum.data.module_3 import MODULE_3 as OLD_3
from app.curriculum.data.module_4 import MODULE_4 as OLD_4
from app.curriculum.data.module_5 import MODULE_5 as OLD_5
from app.curriculum.data.module_6 import MODULE_6 as OLD_6
from app.curriculum.data.module_7 import MODULE_7 as OLD_7
from app.curriculum.data.module_8 import MODULE_8 as OLD_8

CURRICULUM_VERSION = "2026.1"


# title, subtitle, plain-language concept, runnable example, expected stdout,
# likely mistake, correction.  Every row is intentionally topic-specific.
SPECS: Dict[int, List[tuple[str, str, str, str, str, str, str]]] = {
    1: [
        ("Welcome to Programming and Python", "What programs are, why Python is useful, and where it is used.",
         "Programming means writing precise instructions that a computer follows. Python is a readable programming language used for web services, automation, science, data analysis, education, and many other tasks. A program is simply an ordered set of instructions; you do not need to understand interpreter internals to begin.",
         'message = "Python turns instructions into useful work."\nprint(message)', "Python turns instructions into useful work.",
         "Treating Python like ordinary English and omitting required punctuation.", "Copy the small example exactly, then change only the text between quotes."),
        ("Install Python and Set Up Your Environment", "Install Python 3 and choose VS Code, IDLE, or Jupyter Notebook.",
         "Python must be installed before a local computer can run Python files. Confirm the installation with `python3 --version` (or `python --version` on Windows), then create a file ending in `.py`. VS Code is a general editor; Jupyter runs code in notebook cells; IDLE is included with many Python installations.",
         'import sys\nprint("Python is ready")\nprint(sys.version_info.major >= 3)', "Python is ready\nTrue",
         "Installing an editor but not the Python interpreter.", "Install Python from python.org first, then select that interpreter inside the editor."),
        ("Your First Program: Hello, World!", "Create, save, and run one complete Python program.",
         "A first program should make cause and effect visible. `print()` sends a value to standard output—the text area shown by a terminal, notebook cell, or Pip Learn console. Save the line in a `.py` file and run it; changing the quoted text changes the output.",
         'print("Hello, World!")', "Hello, World!",
         "Using curly quotation marks copied from a word processor.", 'Use straight quotes: `print("Hello, World!")`.'),
        ("Understanding print(), Strings and Output", "Use print calls, quoted strings, separators, and line endings.",
         "Text in Python is called a string and is surrounded by matching quotes. `print()` displays its arguments. Commas separate multiple arguments and insert spaces by default; `sep` changes that separator and `end` changes what follows the output.",
         'print("Pip", "Learn", sep="-")\nprint("Ready", end="!\\n")', "Pip-Learn\nReady!",
         "Forgetting a closing quote or parenthesis.", "Pair every opening quote and parenthesis with a matching closing symbol."),
        ("Variables and Assignment", "Name values, update them, and follow clear naming conventions.",
         "A variable is a name attached to a value. The assignment symbol `=` evaluates the right side and binds the result to the name on the left. Use descriptive `snake_case` names such as `student_score`; names cannot start with a digit and are case-sensitive.",
         'student_name = "Mira"\ncompleted_lessons = 2\ncompleted_lessons = completed_lessons + 1\nprint(student_name, completed_lessons)', "Mira 3",
         "Reading `=` as 'is equal forever'.", "Read assignment right-to-left: calculate the value, then store it under the name."),
        ("Numbers and Basic Arithmetic", "Calculate with integers, floats, and arithmetic operators.",
         "Integers are whole numbers; floats include a decimal point. Python supports addition, subtraction, multiplication, true division, floor division, remainder, and powers. Parentheses make the intended calculation order explicit.",
         'price = 120\nquantity = 3\ndiscount = 20\ntotal = price * quantity - discount\nprint(total)', "340",
         "Expecting `/` to discard the decimal part.", "Use `/` for true division and `//` only when floor division is intended."),
        ("Data Types and Type Conversion", "Recognize core types and convert data deliberately.",
         "A value has a type that determines valid operations. Common beginner types are `str`, `int`, `float`, and `bool`. `type()` reports a type; `int()`, `float()`, and `str()` create converted values when the source representation is valid.",
         'raw_age = "18"\nage = int(raw_age)\nprint(type(raw_age).__name__)\nprint(age + 1)', "str\n19",
         "Adding a numeric string directly to an integer.", "Convert the string first: `int(raw_value) + number`."),
        ("User Input and Interactive Programs", "Collect text input and validate before calculating.",
         "`input(prompt)` pauses a console program and returns what the user typed as a string. Convert only when a number is required, and anticipate invalid entries. In the sandbox example, a saved response stands in for keyboard input so it runs without blocking.",
         'typed_response = "Asha"  # stands in for input("Name: ")\nname = typed_response.strip()\nprint(f"Welcome, {name}!")', "Welcome, Asha!",
         "Assuming `input()` returns a number.", "Remember that input returns text; validate and convert it explicitly."),
        ("Operators and Expressions", "Combine arithmetic, comparison, assignment, and Boolean operators.",
         "An expression produces a value. Comparisons such as `>=` produce booleans, while `and`, `or`, and `not` combine conditions. Arithmetic follows precedence: parentheses, powers, multiplication/division, then addition/subtraction.",
         'score = 72\nattendance = 85\neligible = score >= 40 and attendance >= 75\nprint(eligible)\nprint((2 + 3) * 4)', "True\n20",
         "Confusing assignment `=` with equality `==`.", "Use `=` to store and `==` to compare."),
        ("Formatting Output and Building Small Programs", "Present calculated results clearly and debug beginner errors.",
         "Formatted string literals begin with `f` and place expressions inside braces. Format specifications such as `.2f` control decimal places. Small programs usually follow input → process → output; test each step and read the final traceback line when an error occurs.",
         'item = "Notebook"\nprice = 49.5\nquantity = 2\ntotal = price * quantity\nprint(f"{item}: {quantity} × ₹{price:.2f} = ₹{total:.2f}")', "Notebook: 2 × ₹49.50 = ₹99.00",
         "Writing braces in a normal string without the leading `f`.", "Prefix the opening quote with `f` whenever braces should be evaluated."),
    ],
    2: [
        ("Booleans, Comparisons, and Decisions", "Turn questions into True or False values.", "Boolean values represent two states: `True` and `False`. Comparisons answer questions about values and become the conditions used by decisions.", 'temperature = 31\nprint(temperature > 30)\nprint(20 <= temperature <= 35)', "True\nTrue", "Writing `true` or `false` in lowercase.", "Python Boolean literals begin with capital letters: `True`, `False`."),
        ("if, elif, else, and Nested Decisions", "Choose exactly the branch that matches a condition.", "An `if` block runs when its condition is true. `elif` checks another condition only when earlier branches fail, and `else` handles everything remaining. Indentation defines each block.", 'score = 76\nif score >= 80:\n    grade = "A"\nelif score >= 60:\n    grade = "B"\nelse:\n    grade = "C"\nprint(grade)', "B", "Forgetting the colon or indentation.", "End each branch header with `:` and indent its body consistently."),
        ("for Loops, range(), and Loop Patterns", "Repeat a known number of times and accumulate results.", "A `for` loop visits each value in an iterable. `range(start, stop)` includes the start but excludes the stop. Common patterns count, total, search, or build a new collection.", 'total = 0\nfor number in range(1, 5):\n    total += number\nprint(total)', "10", "Expecting the stop value in `range` to be included.", "Remember that `range(1, 5)` produces 1, 2, 3, 4."),
        ("while, break, continue, and pass", "Control repetition with a condition and deliberate exits.", "A `while` loop repeats while its condition remains true. Update the controlling state to avoid an infinite loop. `break` exits, `continue` starts the next iteration, and `pass` is an explicit do-nothing placeholder.", 'number = 0\nwhile number < 5:\n    number += 1\n    if number == 3:\n        continue\n    print(number)', "1\n2\n4\n5", "Never changing the loop condition.", "Trace the control variable on paper and ensure every path can reach an exit."),
        ("Functions, Parameters, Returns, and Scope", "Package reusable behavior behind a clear interface.", "A function definition names a reusable block. Parameters receive arguments; `return` sends a result to the caller. Local names exist inside their function, which keeps separate tasks from interfering.", 'def final_price(price, discount=10):\n    return price * (1 - discount / 100)\n\nprint(f"{final_price(200):.2f}")', "180.00", "Printing a result inside a function when the caller needs the value.", "Return the value; let the caller decide whether and how to print it."),
        ("Lambda, Recursion, Modules, and Program Design", "Recognize compact functions and split programs into testable parts.", "A lambda is a small single-expression function. Recursion is a function calling itself with a smaller problem and requires a base case. Most application code is clearer as ordinary named functions grouped into modules.", 'double = lambda value: value * 2\ndef countdown(n):\n    if n == 0:\n        return "Go"\n    return f"{n}, " + countdown(n - 1)\nprint(double(6))\nprint(countdown(3))', "12\n3, 2, 1, Go", "Writing recursion without a reachable base case.", "Identify and test the smallest input first, then reduce every recursive call toward it."),
    ],
    3: [
        ("Strings: Indexing, Slicing, and Methods", "Read, transform, and search text safely.", "Strings are immutable sequences of Unicode characters. Indexing selects one character; slicing selects a range; methods return transformed strings without changing the original.", 'course = "Python Basics"\nprint(course[0])\nprint(course[:6])\nprint(course.upper())', "P\nPython\nPYTHON BASICS", "Using an index outside the string.", "Check `len(text)` and remember that valid indexes end at length minus one."),
        ("Lists and List Methods", "Store an ordered, changeable collection.", "Lists preserve order and may be changed. `append`, `insert`, `remove`, and `pop` update a list; indexing and slicing read items.", 'tasks = ["read", "code"]\ntasks.append("test")\ntasks[0] = "review"\nprint(tasks)', "['review', 'code', 'test']", "Assigning the result of `append()` back to the list.", "Call `items.append(value)` directly; it mutates the list and returns `None`."),
        ("Iteration, Built-ins, and Comprehensions", "Process collections with readable loop patterns.", "Iteration visits each item without manual indexing. Built-ins such as `len`, `sum`, `min`, `max`, `sorted`, and `enumerate` express common operations; comprehensions build collections concisely.", 'scores = [72, 91, 65, 88]\npassing = [score for score in scores if score >= 70]\nprint(passing)\nprint(round(sum(scores) / len(scores), 1))', "[72, 91, 88]\n79.0", "Changing a list while iterating over it.", "Build a new list or iterate over a copy when filtering."),
        ("Tuples and Immutability", "Use fixed ordered records and unpack values.", "A tuple is an ordered sequence that cannot be changed after creation. This makes it useful for coordinates, database rows, and returning several related values.", 'point = (12, 7)\nx, y = point\nprint(f"x={x}, y={y}")', "x=12, y=7", "Forgetting the comma in a one-item tuple.", "Write `(value,)`; parentheses alone do not create a tuple."),
        ("Sets and Set Operations", "Keep unique values and compare groups.", "Sets store unique hashable values without a guaranteed display order. Union combines, intersection finds shared values, and difference finds values present in only one side.", 'required = {"python", "sql", "git"}\ncompleted = {"python", "git"}\nprint(sorted(required - completed))\nprint(required <= completed)', "['sql']\nFalse", "Depending on set iteration order.", "Sort a set before displaying it when deterministic order matters."),
        ("Dictionaries and Nested Collections", "Model records with key-value pairs.", "A dictionary maps unique keys to values. Use bracket access when a key must exist and `get` when it may be absent. Values can themselves be lists or dictionaries.", 'student = {"name": "Ravi", "marks": [80, 90]}\nstudent["marks"].append(85)\nprint(student["name"])\nprint(sum(student["marks"]) // len(student["marks"]))', "Ravi\n85", "Looking up a missing key with brackets.", "Use `record.get(key, default)` when absence is expected."),
        ("Choosing Structures, Storage, and Retrieval", "Select a collection by the operations the program needs.", "Choose a list for ordered changeable items, tuple for fixed records, set for uniqueness and membership, and dictionary for key-based lookup. Real applications often nest these structures.", 'inventory = {"PEN": {"price": 10, "stock": 12}, "BOOK": {"price": 80, "stock": 3}}\nvalue = sum(item["price"] * item["stock"] for item in inventory.values())\nprint(value)', "360", "Choosing a structure only because it is familiar.", "Start from required operations: ordering, mutation, uniqueness, or lookup by key."),
    ],
    4: [
        ("Paths, Text Files, and File Modes", "Open files deliberately and understand read, write, and append modes.", "A path identifies a file. Text mode decodes bytes into strings. Mode `r` reads, `w` replaces, and `a` adds to the end; use explicit UTF-8 encoding for portable text.", 'from pathlib import Path\npath = Path("notes.txt")\nprint(path.suffix)\nprint(path.name)', ".txt\nnotes.txt", "Opening an important file with `w` by accident.", "Use `r` while inspecting and write to a new test path before replacing data."),
        ("Reading, Writing, with, seek(), and tell()", "Manage file resources and cursor positions.", "The `with` statement closes a file even when an error occurs. Reading advances a cursor; `tell()` reports its position and `seek()` moves it. The sandbox uses an in-memory text stream to practise safely.", 'from io import StringIO\nf = StringIO("alpha\\nbeta\\n")\nprint(f.readline().strip())\nprint(f.tell())\nf.seek(0)\nprint(f.readline().strip())', "alpha\n6\nalpha", "Using a file after its `with` block has closed.", "Perform file operations inside the `with` block and store only the data you need later."),
        ("CSV Reading and Writing", "Represent tabular rows with the standard csv module.", "CSV stores rows as delimited text, but quoting rules make manual splitting unreliable. `csv.DictReader` and `DictWriter` map headings to values and handle escaping.", 'import csv, io\ndata = "name,score\\nAsha,88\\nRavi,76\\n"\nrows = list(csv.DictReader(io.StringIO(data)))\nprint(rows[0]["name"])\nprint(sum(int(r["score"]) for r in rows))', "Asha\n164", "Splitting every CSV line on commas.", "Use the `csv` module so quoted commas and line endings are handled correctly."),
        ("Exceptions: try, except, else, finally", "Recover from expected runtime failures without hiding bugs.", "Exceptions report conditions that interrupt normal execution. Catch only errors you can handle. `else` runs after a successful try, and `finally` runs whether success or failure occurs.", 'raw = "12x"\ntry:\n    value = int(raw)\nexcept ValueError:\n    print("Enter whole digits")\nelse:\n    print(value * 2)\nfinally:\n    print("Validation finished")', "Enter whole digits\nValidation finished", "Using bare `except:` around a large block.", "Catch a specific exception around the smallest statement that can raise it."),
        ("Raising and Designing Custom Exceptions", "Make invalid application states explicit.", "Use `raise` when input violates a rule that a caller must handle. A custom exception class gives domain errors a meaningful name while preserving normal exception behavior.", 'class InvalidScoreError(ValueError):\n    pass\ndef validate(score):\n    if not 0 <= score <= 100:\n        raise InvalidScoreError("score must be 0..100")\n    return score\ntry:\n    validate(120)\nexcept InvalidScoreError as error:\n    print(error)', "score must be 0..100", "Raising a string instead of an exception object.", "Raise an exception class or instance, such as `raise ValueError(message)`."),
        ("Logging and Practical File Workflows", "Record useful events and process files predictably.", "Logging preserves diagnostic events with severity levels DEBUG, INFO, WARNING, ERROR, and CRITICAL. A robust workflow validates the path, reads, parses each record, counts rejected records, writes results safely, and logs failures.", 'import logging\nlogging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")\nrecords = ["INFO ok", "ERROR failed", "INFO ready"]\nerrors = sum(line.startswith("ERROR") for line in records)\nprint(f"errors={errors}")', "errors=1", "Using print statements as the only permanent diagnostic record.", "Use logging with an appropriate level; keep learner-facing output separate."),
    ],
    5: [
        ("Why OOP? Classes and Objects", "Group related state and behavior into reusable models.", "Object-oriented programming is useful when many entities share behavior but keep separate state. A class is a blueprint; each object is an instance created from it.", 'class Lamp:\n    def turn_on(self):\n        return "light on"\nlamp = Lamp()\nprint(lamp.turn_on())', "light on", "Calling an instance method on the class without an object.", "Create an instance first, then call `instance.method()`."),
        ("Attributes, Methods, self, and __init__", "Initialize valid objects and access their own state.", "`__init__` runs after an instance is created. The `self` parameter refers to that particular instance, so attributes such as `self.name` remain separate between objects.", 'class Student:\n    def __init__(self, name):\n        self.name = name\n    def greet(self):\n        return f"Hello, {self.name}"\nprint(Student("Neha").greet())', "Hello, Neha", "Omitting `self` from an instance method.", "Make `self` the first parameter and access instance attributes through it."),
        ("Instance and Class Variables", "Distinguish per-object state from shared class data.", "Instance variables belong to one object. Class variables live on the class and are shared defaults or counters. Avoid using a mutable class variable for per-instance data.", 'class Course:\n    institution = "MU"\n    def __init__(self, title):\n        self.title = title\na = Course("Python")\nb = Course("SQL")\nprint(a.institution, b.title)', "MU SQL", "Putting an empty list at class level for every object's items.", "Create per-object mutable collections inside `__init__`."),
        ("Encapsulation and Properties", "Protect invariants behind a small public interface.", "Encapsulation keeps implementation details together and exposes safe operations. Python uses naming conventions and properties rather than absolute privacy; a setter can validate changes.", 'class Account:\n    def __init__(self, balance):\n        self._balance = balance\n    @property\n    def balance(self):\n        return self._balance\nprint(Account(500).balance)', "500", "Directly changing internal attributes from unrelated code.", "Expose a method or validated property for changes that must preserve rules."),
        ("Inheritance and Method Overriding", "Reuse a base contract and specialize behavior.", "Inheritance lets a subclass reuse and extend a base class. Overriding supplies a more specific implementation; `super()` can invoke base initialization.", 'class Employee:\n    def role(self): return "employee"\nclass Developer(Employee):\n    def role(self): return "developer"\nprint(Developer().role())', "developer", "Using inheritance only to share a few helper functions.", "Prefer inheritance for a genuine is-a relationship; otherwise use composition."),
        ("Polymorphism and Abstraction", "Program to shared behavior instead of concrete types.", "Polymorphism means different objects respond to the same operation. Abstraction highlights what callers need and hides details. Abstract base classes can enforce required methods in larger designs.", 'class EmailReport:\n    def send(self): return "email sent"\nclass ScreenReport:\n    def send(self): return "screen shown"\nfor report in (EmailReport(), ScreenReport()):\n    print(report.send())', "email sent\nscreen shown", "Checking every object's exact type before calling shared behavior.", "Define a common interface and let each object implement it."),
        ("Reusable OOP Modules and System Modeling", "Turn requirements into collaborating classes.", "Model nouns as candidate objects, responsibilities as methods, and business rules as invariants. Keep persistence, presentation, and domain behavior separate so each part can be tested.", 'class Cart:\n    def __init__(self): self.prices = []\n    def add(self, price): self.prices.append(price)\n    def total(self): return sum(self.prices)\ncart = Cart()\ncart.add(40)\ncart.add(60)\nprint(cart.total())', "100", "Creating one giant class that handles UI, storage, and all rules.", "Give each class one focused responsibility and connect objects through clear methods."),
    ],
    6: [
        ("Relational Database Fundamentals", "Understand tables, rows, columns, and primary keys.", "A relational database stores structured rows in tables. Columns define fields, and a primary key uniquely identifies each row. Relationships connect keys between tables.", 'customers = [{"id": 1, "name": "Asha"}, {"id": 2, "name": "Ravi"}]\nprint(customers[0]["id"], customers[0]["name"])', "1 Asha", "Using a person's name as a guaranteed unique identifier.", "Use a stable primary key independent of changeable descriptive fields."),
        ("SQLite Connections and Table Creation", "Open, use, and close a local database connection.", "SQLite is an embedded relational database included with Python. A connection owns transactions; a cursor executes SQL. An in-memory database is ideal for safe exercises.", 'import sqlite3\nwith sqlite3.connect(":memory:") as connection:\n    connection.execute("CREATE TABLE learner (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")\n    count = connection.execute("SELECT count(*) FROM learner").fetchone()[0]\nprint(count)', "0", "Forgetting that a connection should be closed.", "Use a context manager or a `try/finally` lifecycle."),
        ("Create and Read Operations", "Insert rows and select only the data you need.", "`INSERT` creates a row and `SELECT` reads rows. Column lists make intent clear. Use cursor results such as `fetchone()` and `fetchall()` deliberately.", 'import sqlite3\nwith sqlite3.connect(":memory:") as db:\n    db.execute("CREATE TABLE item (id INTEGER PRIMARY KEY, name TEXT)")\n    db.execute("INSERT INTO item(name) VALUES (?)", ("Pen",))\n    print(db.execute("SELECT name FROM item").fetchone()[0])', "Pen", "Building SQL by concatenating user input.", "Put data in parameter placeholders and pass values separately."),
        ("Update, Delete, and Parameterized Queries", "Modify targeted rows without SQL injection.", "`UPDATE` changes matched rows and `DELETE` removes them. Always include and verify the `WHERE` condition. Parameterized queries keep data separate from SQL syntax and prevent injection.", 'import sqlite3\nwith sqlite3.connect(":memory:") as db:\n    db.execute("CREATE TABLE item (id INTEGER PRIMARY KEY, stock INTEGER)")\n    db.execute("INSERT INTO item VALUES (?, ?)", (1, 5))\n    db.execute("UPDATE item SET stock=? WHERE id=?", (8, 1))\n    print(db.execute("SELECT stock FROM item WHERE id=?", (1,)).fetchone()[0])', "8", "Running UPDATE or DELETE without a WHERE clause.", "Select with the same condition first and execute changes inside a transaction."),
        ("Transactions, Commit, Rollback, and Errors", "Keep related database changes all-or-nothing.", "A transaction groups statements into one unit. Commit makes them durable; rollback cancels them after failure. Transfers and multi-row updates must never be partially applied.", 'import sqlite3\ndb = sqlite3.connect(":memory:")\ndb.execute("CREATE TABLE balance (amount INTEGER)")\ndb.execute("INSERT INTO balance VALUES (100)")\ndb.commit()\ntry:\n    db.execute("UPDATE balance SET amount=50")\n    raise ValueError("cancel")\nexcept ValueError:\n    db.rollback()\nprint(db.execute("SELECT amount FROM balance").fetchone()[0])\ndb.close()', "100", "Committing halfway through one business operation.", "Commit only after every related statement succeeds; rollback on error."),
        ("MySQL Connectivity and Database Integration", "Transfer the connection lifecycle to a server database safely.", "MySQL uses the same SQL ideas but requires a server, driver, credentials, and network connection. Store secrets in environment variables, use parameter syntax required by the driver, close resources, and provide SQLite as an offline learning path.", 'config = {"host": "localhost", "database": "pip_learn", "ssl": True}\nrequired = {"host", "database", "ssl"}\nprint(required <= config.keys())\nprint("Use environment variables for credentials")', "True\nUse environment variables for credentials", "Hard-coding a production password in source code.", "Read credentials from environment variables or a secret manager and never commit them."),
    ],
    7: [
        ("APIs, Web Services, HTTP, and REST", "Understand request-response communication before writing network code.", "An API is a documented interface between programs. HTTP requests use methods, URLs, headers, parameters, and optional bodies; responses contain a status code, headers, and body. REST commonly models resources with predictable URLs and methods.", 'request = {"method": "GET", "path": "/weather", "params": {"city": "Rajkot"}}\nprint(request["method"], request["path"])\nprint(request["params"]["city"])', "GET /weather\nRajkot", "Assuming every response with a body is successful.", "Check the HTTP status code before trusting or parsing response data."),
        ("Requests: GET, POST, Parameters, Headers, and JSON", "Make explicit requests and validate structured responses.", "The `requests` library sends HTTP requests. Use `params` for query data, `json` for a JSON body, `headers` for metadata, and a timeout so the program cannot wait forever. `raise_for_status()` turns error statuses into exceptions.", 'import json\nbody = "{\\"temperature_c\\": 30, \\"city\\": \\"Rajkot\\"}"\ndata = json.loads(body)\nprint(data["city"], data["temperature_c"])', "Rajkot 30", "Calling `.json()` without handling invalid JSON or error status.", "Check status, catch request/JSON errors, and validate required response fields."),
        ("Network Errors and Third-Party Integration", "Design timeouts, retries, credentials, and offline fallbacks.", "Networks fail normally: timeouts, DNS errors, rate limits, authentication failures, and schema changes must be expected. Limit retries, avoid retrying invalid requests, redact secrets, and use deterministic mock data for offline learning.", 'def weather_label(payload):\n    if "temperature_c" not in payload:\n        return "Unavailable"\n    return f"{payload[\'temperature_c\']}°C"\nprint(weather_label({"temperature_c": 29}))\nprint(weather_label({}))', "29°C\nUnavailable", "Catching every exception and displaying fake successful data.", "Report the failure honestly and label cached or mock data as offline data."),
        ("Email, Scheduling, Reports, and API Dashboards", "Automate safely with previews and learner-controlled actions.", "Email automation builds a message, previews it, and sends only after explicit confirmation. Scheduled jobs should be idempotent, log outcomes, and keep secrets outside code. Dashboards summarize validated API data and show freshness and failure states.", 'from email.message import EmailMessage\nmessage = EmailMessage()\nmessage["Subject"] = "Weekly learning report"\nmessage["To"] = "learner@example.test"\nmessage.set_content("This is preview mode; nothing was sent.")\nprint(message["Subject"])\nprint("preview only")', "Weekly learning report\npreview only", "Sending a real email automatically during a demonstration.", "Default to preview/test mode and require an explicit learner action before sending."),
    ],
    8: [
        ("NumPy Arrays and Operations", "Use typed arrays for numerical work.", "A NumPy array stores values in a compact, usually uniform data type and applies operations element-wise. Shape describes dimensions; vectorized operations replace many manual loops.", 'import numpy as np\nvalues = np.array([10, 20, 30])\nprint((values * 2).tolist())\nprint(values.mean())', "[20, 40, 60]\n20.0", "Expecting Python list multiplication to perform numeric scaling.", "Convert numeric data to an array before element-wise arithmetic."),
        ("Pandas Series, DataFrames, and Import/Export", "Represent labeled columns and tabular datasets.", "A Series is one labeled column; a DataFrame is a table of aligned columns. Pandas reads and writes CSV and Excel files; inspect columns, dtypes, shape, and sample rows immediately after import.", 'import pandas as pd\nframe = pd.DataFrame({"product": ["A", "B"], "sales": [120, 180]})\nprint(frame["sales"].sum())\nprint(list(frame.columns))', "300\n['product', 'sales']", "Analyzing a file without checking inferred data types.", "Inspect `frame.info()` and convert columns deliberately before calculations."),
        ("Cleaning, Missing Values, Filtering, Grouping", "Turn untidy rows into defensible summaries.", "Missing values can be dropped, filled, or investigated depending on meaning. Boolean masks filter rows; `groupby` splits data into groups and aggregation computes summaries. Record cleaning choices because they affect conclusions.", 'import pandas as pd\nframe = pd.DataFrame({"region": ["West", "West", "East"], "sales": [100, None, 250]})\nframe["sales"] = frame["sales"].fillna(0)\nprint(frame.groupby("region")["sales"].sum().to_dict())', "{'East': 250.0, 'West': 100.0}", "Filling every missing value with zero without checking meaning.", "Choose a missing-value rule per column and document the assumption."),
        ("Matplotlib Charts and Dashboard Reporting", "Choose honest bar, line, and pie charts for a decision.", "Bar charts compare categories, line charts show ordered change, and pie charts are suitable only for a few parts of one whole. Label axes, units, time range, and source; dashboards should pair charts with concise metrics and data freshness.", 'sales = {"Jan": 120, "Feb": 150, "Mar": 135}\nbest_month = max(sales, key=sales.get)\nprint(best_month, sales[best_month])\nprint("bar: compare months; line: show trend")', "Feb 150\nbar: compare months; line: show trend", "Using a pie chart for many categories or values that are not parts of one whole.", "Select a chart from the comparison question, not from decoration preferences."),
    ],
}


def _lesson(module_id: int, position: int, spec: tuple[str, str, str, str, str, str, str]) -> Lesson:
    title, subtitle, concept, code, output, mistake, correction = spec
    lesson_id = f"py-v2-u{module_id}-l{position:02d}"
    previous = f"py-v2-u{module_id}-l{position - 1:02d}" if position > 1 else (
        f"py-v2-u{module_id - 1}-l{len(SPECS[module_id - 1]):02d}" if module_id > 1 else ""
    )
    prerequisite_text = (
        f"[{previous}](/module/{module_id if position > 1 else module_id - 1}/lesson/{previous})"
        if previous else "None — this is the starting lesson."
    )
    objectives = [
        f"Explain {title.lower()} in your own words",
        "Read and trace a small Python example before running it",
        "Modify the example and diagnose a likely mistake",
    ]
    syntax_lines = "\n".join(f"- Line {i}: `{line}`" for i, line in enumerate(code.splitlines(), 1))
    sections = [
        ContentSection(id=f"{lesson_id}-orientation", title="Prerequisites & Objectives", eyebrow="START HERE",
            markdown=f"## Before you begin\n\n**Prerequisite:** {prerequisite_text}\n\nYou need only the ideas taught in that lesson. New terms are defined below.\n\n### Learning objectives\n" + "\n".join(f"- {item}" for item in objectives)),
        ContentSection(id=f"{lesson_id}-concept", title="Understand the Concept", eyebrow="PLAIN-LANGUAGE MODEL",
            markdown=f"## {title}\n\n{concept}\n\n### Smallest meaningful example\n\n```python\n{code}\n```"),
        ContentSection(id=f"{lesson_id}-syntax", title="Syntax, Step by Step", eyebrow="READ THE SYMBOLS",
            markdown=f"## Read the program line by line\n\n{syntax_lines}\n\nNames refer to values, parentheses call a function, commas separate arguments, and a colon—when present—opens an indented block. Run the complete example before changing it."),
        ContentSection(id=f"{lesson_id}-worked", title="Worked Example & Output", eyebrow="PREDICT · RUN · EXPLAIN",
            markdown=f"## Runnable example\n\n```python\n{code}\n```\n\n### Expected output\n\n```text\n{output}\n```\n\nThe output follows from evaluating each statement from top to bottom. Change one value, predict the new output, and run again.\n\n### Real-world use\n\nThis pattern appears in the unit project and in small scripts that transform input into a clear, testable result."),
        ContentSection(id=f"{lesson_id}-debug", title="Debugging, Recap & Deeper Learning", eyebrow="FIX AND CONSOLIDATE",
            markdown=f"## Common mistake\n\n**Symptom:** {mistake}\n\n**Fix:** {correction}\n\nWhen Python shows a traceback, read its final line first, then inspect the named source line.\n\n### Recap\n\n- State what the program receives, what it changes, and what it produces.\n- Predict before running; compare the actual output with the prediction.\n- Keep the smallest working version while debugging.\n\n### Optional deeper learning\n\nAfter mastering the required behavior, explore how Python represents and executes this feature internally. Interpreter bytecode and memory implementation details are enrichment, not prerequisites."),
    ]
    experiment = Experiment(
        id=f"{lesson_id}-experiment", title=f"Change and explain: {title}",
        prediction_prompt=f"Without running the program, write the exact output you expect: `{output}` is the reference behavior.",
        instructions=["Predict the output.", "Run the unchanged program.", "Compare actual and expected output.", "Modify one value or expression.", "Run again and explain the difference."],
        starter_code=code, expected_output=output,
        observation_prompt="Which line produced each output line?",
        modification_prompt="Change one input value while preserving valid syntax; predict before the second run.",
    )
    practices = [
        PracticeExercise(id=f"{lesson_id}-practice-1", title="Introductory: Predict and verify", difficulty="Introductory",
            problem_statement=f"Run the lesson example for **{title}** and make its output match the specification.", input_output_expectations=f"Expected stdout:\n{output}", starter_code=code,
            hints=["Trace from the first line.", "Compare spelling, spaces, punctuation, and line breaks."], test_cases=[{"input": "", "expected_output": output, "description": "Exact reference behavior"}], solution=code),
        PracticeExercise(id=f"{lesson_id}-practice-2", title="Guided: Repair the program", difficulty="Guided",
            problem_statement=f"Complete or repair a program that demonstrates **{title}**. It must produce the shown behavior, not merely contain a particular variable name.", input_output_expectations=f"Expected stdout:\n{output}", starter_code="# Rebuild the worked example below.\n# Use the hints, then run the real behavior tests.\n",
            hints=[f"Review the Syntax section for {title}.", "Build one statement at a time and run often.", f"Target output begins with: {output.splitlines()[0]}"], test_cases=[{"input": "", "expected_output": output, "description": "Guided behavior and formatting"}], solution=code),
        PracticeExercise(id=f"{lesson_id}-practice-3", title="Independent: Recreate from requirements", difficulty="Independent",
            problem_statement=f"From a blank editor, write a fresh program that proves you understand **{title}** and produces the required output. No working solution is prefilled.", input_output_expectations=f"Required stdout:\n{output}", starter_code="# Independent solution: write your program here.\n",
            hints=["Describe the required input, processing, and output on paper.", "Use the smallest valid program first.", "Test exact behavior, including edge-sensitive formatting."], test_cases=[{"input": "", "expected_output": output, "description": "Independent behavioral test"}], solution=code),
    ]
    checkpoints = [
        MiniCheckpoint(question=f"Which statement best describes the purpose of this lesson on {title}?", options=[subtitle, "It requires memorising CPython bytecode before coding", "It replaces testing with visual inspection", "It guarantees every input is valid"], correct_index=0, explanation=f"The lesson goal is: {subtitle}"),
        MiniCheckpoint(question="What should you do before and after changing the worked example?", options=["Predict the effect, run it, then explain the observed difference", "Change several lines and ignore the output", "Mark the lesson complete without running", "Copy an unrelated solution"], correct_index=0, explanation="Prediction and observation connect code changes to program behavior."),
    ]
    return Lesson(
        id=lesson_id, module_id=module_id, position=position, title=title, subtitle=subtitle,
        description=subtitle, reading_time_min=10, prerequisites=[previous] if previous else [], learning_objectives=objectives,
        concept_markdown=concept, syntax_example=code, executable_code=code, expected_output=output,
        output_explanation="Trace the statements from top to bottom and connect each printed value to the expression that produced it.",
        common_mistakes=[CommonMistake(mistake=mistake, explanation=mistake, correction=correction)],
        mini_checkpoint=checkpoints[0], content_sections=sections, experiment=experiment,
        practice_tasks=practices, checkpoint_questions=checkpoints,
        completion_criteria=["Read all sections", "Run and modify the experiment", "Pass all three behavioral practices", "Answer every checkpoint correctly"],
        optional_deeper_learning="Interpreter and implementation details are optional enrichment after the required behavior is understood.",
    )


def _project(project: ProjectInfo, prerequisites: List[str], milestones: List[str], tests: List[str], evidence: str) -> ProjectInfo:
    return project.model_copy(update={
        "prerequisites": prerequisites,
        "milestones": milestones,
        "testing_criteria": tests,
        "expected_behavior": "The learner controls inputs, receives real computed output, and sees honest validation or error feedback.",
        "error_handling": ["Reject invalid or unsafe input", "Show a useful explanation", "Do not claim external actions succeeded in test mode"],
        "evidence": evidence,
    })


LEGACY = [OLD_1, OLD_2, OLD_3, OLD_4, OLD_5, OLD_6, OLD_7, OLD_8]
CONTACT_HOURS = [5, 6, 7, 6, 7, 6, 4, 4]
ASSESSMENT_MARKS = [10, 12, 12, 12, 12, 12, 12, 0]
PROJECT_EVIDENCE = [
    "app/projects/smart_calculator.py and tests/test_projects.py::test_smart_calculator_operations",
    "app/projects/payroll_system.py and tests/test_projects.py::test_payroll_system",
    "app/projects/inventory_tracker.py plus app/projects/grade_analyzer.py",
    "app/projects/log_analyzer.py and tests/test_projects.py::test_log_file_analyzer",
    "app/projects/banking_system.py and tests/test_projects.py::test_banking_ledger_system",
    "app/projects/customer_crm.py and tests/test_projects.py::test_customer_crm_crud",
    "app/projects/weather_dashboard.py plus app/projects/email_automator.py",
    "app/projects/sales_analytics.py and tests/test_projects.py::test_sales_analytics",
]


def _build_modules() -> Dict[int, Module]:
    registry: Dict[int, Module] = {}
    for module_id, old in enumerate(LEGACY, 1):
        lessons = [_lesson(module_id, i, spec) for i, spec in enumerate(SPECS[module_id], 1)]
        primary = _project(
            old.project, [lessons[max(0, len(lessons) - 3)].id],
            ["Clarify inputs and outputs", "Implement the smallest working feature", "Add validation and error handling", "Run normal and edge-case tests", "Record completion evidence"],
            ["Normal case produces the documented result", "Invalid input is rejected safely", "An edge case is tested", "No completion is awarded merely for opening the project"],
            PROJECT_EVIDENCE[module_id - 1],
        )
        projects = [primary]
        if module_id == 3:
            projects.append(ProjectInfo(id="proj-grade-analyzer", title="Student Grade Analyzer", subtitle="Analyze lists of learner records", objective="Compute class statistics and grade summaries from validated records.", requirements=["Validate scores", "Calculate average, highest, lowest, grades", "Handle empty input"], starter_snippet="from app.projects.grade_analyzer import analyze_student_grades", module_id=3, prerequisites=[lessons[-2].id], milestones=["Validate records", "Calculate statistics", "Present a summary"], testing_criteria=["Empty and boundary inputs", "Known average"], expected_behavior="Returns defensible class statistics.", error_handling=["Reject scores outside 0..100"], evidence="app/projects/grade_analyzer.py"))
        if module_id == 7:
            projects.append(ProjectInfo(id="proj-email-automation", title="Email Automation Tool", subtitle="Preview safe scheduled reports", objective="Build and preview MIME email without automatic real-world sending.", requirements=["Render subject and body", "Preview mode", "Explicit send control", "Secure credentials"], starter_snippet="from app.projects.email_automator import render_email_template", module_id=7, prerequisites=[lessons[-1].id], milestones=["Render template", "Preview MIME", "Configure test mode", "Document explicit send"], testing_criteria=["No automatic send", "Valid recipient and MIME"], expected_behavior="Creates a preview and never sends during a demo.", error_handling=["Reject malformed addresses", "Report SMTP failures"], evidence="app/projects/email_automator.py"))
        checkpoint_bank = [question for lesson in lessons for question in lesson.checkpoint_questions]
        quiz_questions = [
            QuizQuestion(id=f"py-v2-u{module_id}-quiz-{i+1:02d}", question=q.question, options=q.options, correct_index=q.correct_index, explanation=q.explanation)
            for i, q in enumerate(checkpoint_bank[:max(5, len(lessons))])
        ]
        registry[module_id] = old.model_copy(update={
            "contact_hours": CONTACT_HOURS[module_id - 1],
            "assessment_marks": ASSESSMENT_MARKS[module_id - 1],
            "description": f"Beginner-first Unit {module_id} learning path with explicit prerequisites, real execution, behavioral practice, and assessment.",
            "learning_objectives": [objective for l in lessons for objective in l.learning_objectives[:1]],
            "topics_covered": [l.title for l in lessons],
            "project": primary,
            "projects": projects,
            "lessons": lessons,
            "practice_exercises": [task for l in lessons for task in l.practice_tasks],
            "quiz_questions": quiz_questions,
            "curriculum_version": CURRICULUM_VERSION,
        })
    return registry


CURRICULUM_REGISTRY = _build_modules()


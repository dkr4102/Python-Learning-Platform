"""
Module 6: Database Connectivity
Marwadi University 01AP0303 - Unit 6 (6 Contact Hours, 12 Marks Assessment)
Mini-Project: Customer Record Management Application
"""
from app.curriculum.models import Module, Lesson, PracticeExercise, QuizQuestion, ProjectInfo, CommonMistake, MiniCheckpoint

MODULE_6 = Module(
    id=6,
    code="MOD-06",
    title="Database Connectivity",
    syllabus_unit="Unit 6: SQLite, MySQL Concepts & Relational CRUD Persistence",
    contact_hours=6,
    assessment_marks=12,
    description="Connect Python applications to relational database engines using sqlite3, design normalized schemas, execute parameterized queries to defeat SQL injection, and manage ACID transactions.",
    learning_objectives=[
        "Architect relational database schemas with primary keys, constraints, and data integrity rules",
        "Manage SQLite database connections, cursor objects, and deterministic statement execution",
        "Implement complete CRUD operations (Create, Read, Update, Delete) with parameterized queries",
        "Manage transactions with commit and rollback to guarantee ACID consistency",
        "Understand client-server relational databases (MySQL) and compare them with embedded SQLite engines"
    ],
    topics_covered=[
        "Relational Database Principles & Schema Normalization",
        "SQLite Engine Architecture (Embedded, Zero-Configuration)",
        "The Python sqlite3 Standard Module & Cursor Life-Cycle",
        "DDL & DML Statements (CREATE TABLE, INSERT, SELECT, UPDATE, DELETE)",
        "Security Safeguards: Parameterized Queries vs SQL Injection Vulnerabilities",
        "Transaction Management: Commit, Rollback & ACID Guarantees",
        "MySQL vs SQLite: Client-Server Architecture & Connection Strings"
    ],
    artwork_id="ART-10",
    project=ProjectInfo(
        id="proj-customer-crm",
        title="Customer Record Management Application",
        subtitle="Zero-Config SQLite CRUD CRM with Optional MySQL Learning Path",
        objective="Engineer a complete, database-backed Customer Relationship Management (CRM) system that supports creating, viewing, updating, searching, and deleting customer profiles with parameterized SQL queries and transaction safety.",
        requirements=[
            "Initialize a persistent SQLite customer table with id, name, email, phone, and tier",
            "Implement parameterized queries preventing SQL injection on all inputs",
            "Provide search functionality by name, email, or customer tier",
            "Enforce unique email constraints and handle sqlite3.IntegrityError gracefully",
            "Document clearly the optional MySQL enterprise connection pathway"
        ],
        starter_snippet="""# Module 6 Project: Customer CRM Database
import sqlite3

def init_crm_db(db_path=":memory:"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            tier TEXT DEFAULT 'Standard'
        )
    ''')
    conn.commit()
    return conn

def add_customer(conn, name, email, tier='Standard'):
    cur = conn.cursor()
    cur.execute("INSERT INTO customers (name, email, tier) VALUES (?, ?, ?)", (name, email, tier))
    conn.commit()
    return cur.lastrowid
""",
        module_id=6
    ),
    lessons=[
        Lesson(
            id="m6-l1",
            title="Relational Database Fundamentals & SQLite",
            subtitle="Embedded relational databases, tables, keys, and zero-configuration storage.",
            reading_time_min=6,
            concept_markdown="""### The Relational Database Paradigm

A relational database organizes data into **tables** composed of rows (records) and columns (attributes).

#### Key Principles:
- **Primary Key (PK)**: A column (or set of columns) that uniquely identifies each row (e.g. `id INTEGER PRIMARY KEY AUTOINCREMENT`).
- **Foreign Key (FK)**: A reference from one table to the primary key of another table, establishing relational integrity.
- **Constraints**: `NOT NULL`, `UNIQUE`, `CHECK`, and `DEFAULT` enforce data validity at the storage layer.

#### Why SQLite?
Python includes **SQLite (`sqlite3`) in the standard library**:
1. **Serverless & Embedded**: Runs in-process with the application without requiring a background daemon.
2. **Zero-Configuration**: Stores the entire database inside a single cross-platform disk file (or `:memory:`).
3. **Full ACID Compliance**: Atomicity, Consistency, Isolation, and Durability guarantees.
""",
            syntax_example="""# Basic SQLite connection and table creation
import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        enrollment TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        course TEXT NOT NULL
    )
''')
conn.commit()
print("Table created successfully.")
conn.close()
""",
            executable_code="""# Executable SQLite table initialization and inspection
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

cur.execute('''
    CREATE TABLE courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        credits INTEGER DEFAULT 4
    )
''')

courses = [
    ("01AP0303", "Programming with Python", 4),
    ("01AP0304", "Database Management Systems", 4)
]
cur.executemany("INSERT INTO courses (code, name, credits) VALUES (?, ?, ?)", courses)
conn.commit()

cur.execute("SELECT code, name FROM courses")
rows = cur.fetchall()
for code, name in rows:
    print(f"Course: {code} -> {name}")

conn.close()
""",
            expected_output="""Course: 01AP0303 -> Programming with Python
Course: 01AP0304 -> Database Management Systems""",
            output_explanation="executemany batches multiple rows cleanly using parameterized placeholders, followed by commit() and fetchall().",
            common_mistakes=[
                CommonMistake(
                    mistake="Forgetting to call `conn.commit()` after INSERT or UPDATE statements",
                    explanation="In Python sqlite3, changes remain pending in an active transaction and are discarded when the connection closes unless committed.",
                    correction="Always call `conn.commit()` to persist state modifications to disk."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What is the advantage of using `:memory:` when connecting to SQLite via `sqlite3.connect(':memory:')`?",
                options=[
                    "It automatically uploads data to the cloud",
                    "It creates a fast, RAM-only database that requires no disk file, perfect for testing",
                    "It allows unlimited concurrent network connections",
                    "It disables SQL constraints"
                ],
                correct_index=1,
                explanation="`:memory:` instantiates a transient database purely in RAM, ideal for testing and fast isolated experiments."
            )
        ),
        Lesson(
            id="m6-l2",
            title="Parameterized Queries vs SQL Injection",
            subtitle="Defeating security vulnerabilities using placeholder bindings (?, %s).",
            reading_time_min=7,
            concept_markdown="""### The Danger of SQL Injection (SQLi)

**SQL Injection** is one of the most critical security vulnerabilities in web and software engineering (OWASP Top 10). It occurs when untrusted user input is directly concatenated or formatted into an SQL query string:

```python
# CATASTROPHIC VULNERABILITY (Do NOT write this!):
user_search = "' OR '1'='1"
query = f"SELECT * FROM users WHERE email = '{user_search}'"
# Evaluates to: SELECT * FROM users WHERE email = '' OR '1'='1'
# Result: Leaks every user record in the entire database!
```

#### The Solution: Parameterized Queries
Instead of string concatenation, use **query placeholders (`?`)**:
```python
# SECURE: Database engine treats input purely as raw data literal
cursor.execute("SELECT * FROM users WHERE email = ?", (user_search,))
```
The database driver compiles the SQL structure first, then binds the parameter values separately. Input can never alter query syntax!
""",
            syntax_example="""# Secure parameterized insert
username = "Aarav Sharma"
email = "aarav@marwadi.edu"

# Pass values as a separate tuple
cursor.execute(
    "INSERT INTO learners (name, email) VALUES (?, ?)",
    (username, email)
)
""",
            executable_code="""# Executable SQL Injection demonstration and defense
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("CREATE TABLE users (id INT, name TEXT, secret TEXT)")
cur.execute("INSERT INTO users VALUES (1, 'Admin', 'SUPER_SECRET_TOKEN_42')")
conn.commit()

# Attacker tries to inject SQL
malicious_input = "Admin' OR '1'='1"

# Safe parameterized query
cur.execute("SELECT id, name FROM users WHERE name = ?", (malicious_input,))
safe_result = cur.fetchall()
print("Safe query matched records:", safe_result)

cur.execute("SELECT id, name FROM users WHERE name = ?", ("Admin",))
admin_record = cur.fetchone()
print("Legitimate query matched:", admin_record)
conn.close()
""",
            expected_output="""Safe query matched records: []
Legitimate query matched: (1, 'Admin')""",
            output_explanation="The parameterized query treated the malicious string as literal text to match, so zero records matched. The database remained secure.",
            common_mistakes=[
                CommonMistake(
                    mistake="Using f-strings for SQL queries: cursor.execute(f'SELECT * FROM t WHERE id = {user_id}')",
                    explanation="f-strings perform raw string interpolation prior to execution, creating direct SQL injection vectors.",
                    correction="Always pass query arguments as a tuple parameter: cursor.execute('SELECT * FROM t WHERE id = ?', (user_id,))."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="Why does a parameterized query prevent SQL injection?",
                options=[
                    "It hashes the input with SHA-256",
                    "The database engine separates query code compilation from data evaluation",
                    "It removes quotation marks from the input",
                    "It only allows numbers to be queried"
                ],
                correct_index=1,
                explanation="Placeholders ensure the database engine compiles the SQL syntax tree before binding user inputs purely as literal values."
            )
        ),
        Lesson(
            id="m6-l3",
            title="Complete CRUD Implementation & Queries",
            subtitle="Create, Read, Update, and Delete patterns in Python.",
            reading_time_min=7,
            concept_markdown="""### The CRUD Matrix in Python

| Operation | SQL Command | Python Method |
|---|---|---|
| **C**reate | `INSERT INTO ...` | `cursor.execute(...)` + `conn.commit()` |
| **R**ead | `SELECT ... FROM ... WHERE ...` | `cursor.execute(...)` + `cursor.fetchall()` / `fetchone()` |
| **U**pdate | `UPDATE ... SET ... WHERE ...` | `cursor.execute(...)` + `conn.commit()` |
| **D**elete | `DELETE FROM ... WHERE ...` | `cursor.execute(...)` + `conn.commit()` |

#### Fetch Methods:
- `cur.fetchone()`: Returns next row as a tuple or `None`.
- `cur.fetchmany(size)`: Returns next `size` rows.
- `cur.fetchall()`: Returns all remaining matching rows in memory.
- `cur.rowcount`: Returns the number of rows affected by an UPDATE or DELETE.
""",
            syntax_example="""# Updating a customer tier
cursor.execute(
    "UPDATE customers SET tier = ? WHERE id = ?",
    ("Premium", customer_id)
)
conn.commit()
print(f"Updated {cursor.rowcount} row(s).")
""",
            executable_code="""# Executable complete CRUD lifecycle
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

# 1. CREATE Table
cur.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INT)")

# 2. INSERT (Create)
cur.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", ("Keyboard", 45.0, 10))
prod_id = cur.lastrowid
conn.commit()

# 3. READ
cur.execute("SELECT * FROM products WHERE id = ?", (prod_id,))
print("Created record:", cur.fetchone())

# 4. UPDATE
cur.execute("UPDATE products SET price = ?, stock = ? WHERE id = ?", (49.99, 15, prod_id))
conn.commit()
cur.execute("SELECT * FROM products WHERE id = ?", (prod_id,))
print("Updated record:", cur.fetchone())

# 5. DELETE
cur.execute("DELETE FROM products WHERE id = ?", (prod_id,))
conn.commit()
cur.execute("SELECT * FROM products WHERE id = ?", (prod_id,))
print("After deletion:", cur.fetchone())

conn.close()
""",
            expected_output="""Created record: (1, 'Keyboard', 45.0, 10)
Updated record: (1, 'Keyboard', 49.99, 15)
After deletion: None""",
            output_explanation="The script demonstrates the complete database record lifecycle: creation, retrieval, modification, and deletion.",
            common_mistakes=[
                CommonMistake(
                    mistake="Omitting the WHERE clause in an UPDATE or DELETE statement",
                    explanation="Writing UPDATE products SET price = 0 without WHERE will update EVERY row in the entire table!",
                    correction="Always double-check that your WHERE clause specifies the exact target primary key."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What does `cursor.rowcount` indicate after running an UPDATE statement?",
                options=[
                    "The total number of columns in the table",
                    "The number of rows that were modified by the update operation",
                    "The ID of the last row",
                    "The number of characters in the query"
                ],
                correct_index=1,
                explanation="`rowcount` reflects the number of records affected by the DML operation."
            )
        ),
        Lesson(
            id="m6-l4",
            title="Transactions, Rollback & ACID Principles",
            subtitle="Atomicity, Consistency, Isolation, and Durability in financial systems.",
            reading_time_min=6,
            concept_markdown="""### The ACID Guarantees

In financial and enterprise software, multiple database updates must often succeed or fail as a **single indivisible unit**:

- **Atomicity**: "All or nothing." If step 3 of 5 fails, steps 1 and 2 are completely undone.
- **Consistency**: The database transitions only between valid states conforming to all schema constraints.
- **Isolation**: Concurrent transactions cannot see each other's intermediate uncommitted states.
- **Durability**: Once a transaction is committed, data persists permanently even during a server power outage.

#### Managing Transactions in Python
```python
try:
    cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
    conn.commit()  # All successful!
except Exception as e:
    conn.rollback()  # Undo everything back to clean state!
```
""",
            syntax_example="""# Transaction rollback demonstration
try:
    cur.execute("INSERT INTO ledger ...")
    conn.commit()
except sqlite3.Error:
    conn.rollback()
""",
            executable_code="""# Executable transaction rollback simulation
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("CREATE TABLE ledger (id INTEGER PRIMARY KEY, account TEXT, balance REAL)")
cur.execute("INSERT INTO ledger VALUES (1, 'Aarav', 500.0), (2, 'Priya', 300.0)")
conn.commit()

# Attempt a bank transfer that fails midway
try:
    # Deduct from Aarav
    cur.execute("UPDATE ledger SET balance = balance - 200.0 WHERE account = 'Aarav'")
    
    # Simulate a network/system failure before credit
    raise ConnectionResetError("Lost connection to inter-bank network!")
    
    cur.execute("UPDATE ledger SET balance = balance + 200.0 WHERE account = 'Priya'")
    conn.commit()
except Exception as e:
    conn.rollback()
    print(f"Transaction aborted & rolled back safely: {e}")

# Inspect balances
cur.execute("SELECT account, balance FROM ledger")
print("Balances after rollback:", cur.fetchall())
conn.close()
""",
            expected_output="""Transaction aborted & rolled back safely: Lost connection to inter-bank network!
Balances after rollback: [('Aarav', 500.0), ('Priya', 300.0)]""",
            output_explanation="Because rollback() was called upon exception, Aarav's balance was not deducted, preserving atomicity.",
            common_mistakes=[
                CommonMistake(
                    mistake="Committing individual steps inside a multi-step financial transfer",
                    explanation="If step 1 commits and step 2 crashes, money disappears from one account without reaching the recipient.",
                    correction="Issue a single `conn.commit()` only after all constituent statements succeed."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What ACID property guarantees that a multi-step transaction either completes entirely or leaves data unchanged?",
                options=["Atomicity", "Consistency", "Isolation", "Durability"],
                correct_index=0,
                explanation="Atomicity guarantees that all operations in the transaction succeed together or are rolled back completely."
            )
        ),
        Lesson(
            id="m6-l5",
            title="MySQL Concepts & Enterprise Connectivity",
            subtitle="Client-server relational architecture, connection strings, and mysql-connector.",
            reading_time_min=6,
            concept_markdown="""### SQLite vs MySQL / MariaDB

While SQLite is optimal for embedded apps, mobile devices, and local development, high-concurrency multi-user systems often deploy client-server relational databases like **MySQL** or **PostgreSQL**.

| Feature | SQLite | MySQL |
|---|---|---|
| **Architecture** | Serverless / Embedded in-process | Client-Server Network Daemon |
| **Concurrency** | Single-writer lock | Row-level locking & high concurrent writes |
| **Storage** | Single local `.db` file | Clustered database engine files |
| **Access** | File system permissions | User accounts, host permissions, passwords |

#### Connecting to MySQL in Python
To connect to MySQL, developers install drivers like `mysql-connector-python` or `PyMySQL`:

```python
# Optional MySQL connection snippet
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="secure_password",
    database="pip_learn_crm",
    port=3306
)
cursor = connection.cursor(dictionary=True)
cursor.execute("SELECT * FROM customers WHERE tier = %s", ("Enterprise",))
```
Notice the parameterized placeholder in MySQL is `%s` rather than SQLite's `?`.
""",
            syntax_example="""# Python DB-API 2.0 uniformity
# Both sqlite3 and mysql-connector adhere to PEP 249 (Python Database API Specification v2.0)
# Meaning connect(), cursor(), execute(), fetchall(), commit(), and rollback() share identical signatures!
""",
            executable_code="""# Demonstrating PEP 249 DB-API 2.0 compliant dictionary row factory
import sqlite3

conn = sqlite3.connect(":memory:")
# Configure SQLite to return dictionary-like row objects
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("CREATE TABLE faculty (name TEXT, department TEXT)")
cur.execute("INSERT INTO faculty VALUES ('Dr. Sharma', 'Computer Science')")
conn.commit()

cur.execute("SELECT * FROM faculty")
row = cur.fetchone()
print(f"Row by column name: {row['name']} ({row['department']})")
print("Row keys:", list(row.keys()))
conn.close()
""",
            expected_output="""Row by column name: Dr. Sharma (Computer Science)
Row keys: ['name', 'department']""",
            output_explanation="sqlite3.Row provides dictionary-like column access identical to modern MySQL dictionary cursors, ensuring code portability.",
            common_mistakes=[
                CommonMistake(
                    mistake="Hardcoding database passwords in plaintext in source repositories",
                    explanation="Exposes credentials to security breaches if code is shared or pushed to GitHub.",
                    correction="Load credentials from environment variables using os.environ or python-dotenv."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What standard Python specification guarantees that database modules (sqlite3, psycopg2, mysql-connector) share standard method signatures?",
                options=["PEP 8", "PEP 249 (Python DB-API 2.0)", "PEP 484", "WSGI"],
                correct_index=1,
                explanation="PEP 249 establishes the uniform Database API Specification 2.0 across all Python relational drivers."
            )
        )
    ],
    practice_exercises=[
        PracticeExercise(
            id="m6-ex1",
            title="Safe Parameterized Insertion",
            difficulty="Beginner",
            problem_statement="Write a function `insert_student(conn, name, gpa)` that creates a table `students (id INTEGER PRIMARY KEY, name TEXT, gpa REAL)` if not exists, safely inserts the student using parameterized placeholders, commits, and returns the count of students with GPA >= 3.5.",
            input_output_expectations="Inserting ('Aarav', 3.8) and ('Rohan', 3.2) must return Honors Count: 1",
            starter_code="""import sqlite3

def setup_and_count():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT, gpa REAL)")
    
    # Insert students safely
    students = [("Aarav", 3.8), ("Rohan", 3.2)]
    cur.executemany("INSERT INTO students (name, gpa) VALUES (?, ?)", students)
    conn.commit()
    
    cur.execute("SELECT COUNT(*) FROM students WHERE gpa >= ?", (3.5,))
    count = cur.fetchone()[0]
    conn.close()
    return count

print(f"Honors Count: {setup_and_count()}")
""",
            hints=[
                "Use cur.executemany with (?, ?)",
                "cur.execute('SELECT COUNT(*) FROM students WHERE gpa >= ?', (3.5,))"
            ],
            test_cases=[
                {"input": "", "expected_output": "Honors Count: 1", "description": "Verify honors student count"}
            ],
            expected_substrings=["sqlite3", "CREATE TABLE", "INSERT INTO", "commit"],
            solution="""import sqlite3

def setup_and_count():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT, gpa REAL)")
    students = [("Aarav", 3.8), ("Rohan", 3.2)]
    cur.executemany("INSERT INTO students (name, gpa) VALUES (?, ?)", students)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM students WHERE gpa >= ?", (3.5,))
    count = cur.fetchone()[0]
    conn.close()
    return count

print(f"Honors Count: {setup_and_count()}")
"""
        ),
        PracticeExercise(
            id="m6-ex2",
            title="Atomic Transaction Transfer",
            difficulty="Intermediate",
            problem_statement="Implement a transfer function `transfer_funds(conn, from_acc, to_acc, amount)` that checks if from_acc has enough balance, deducts amount, adds to to_acc, and commits. If insufficient funds, raises ValueError without modifying balances.",
            input_output_expectations="Transferring 150 from account with 200 to account with 100 must leave balances at 50 and 250",
            starter_code="""import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("CREATE TABLE bank (acc TEXT PRIMARY KEY, balance REAL)")
cur.execute("INSERT INTO bank VALUES ('A', 200.0), ('B', 100.0)")
conn.commit()

def transfer_funds(conn, from_acc, to_acc, amount):
    cur = conn.cursor()
    cur.execute("SELECT balance FROM bank WHERE acc = ?", (from_acc,))
    bal = cur.fetchone()[0]
    if bal < amount:
        raise ValueError("Insufficient balance")
    cur.execute("UPDATE bank SET balance = balance - ? WHERE acc = ?", (amount, from_acc))
    cur.execute("UPDATE bank SET balance = balance + ? WHERE acc = ?", (amount, to_acc))
    conn.commit()

transfer_funds(conn, 'A', 'B', 150.0)
cur.execute("SELECT acc, balance FROM bank ORDER BY acc")
print("Balances:", cur.fetchall())
conn.close()
""",
            hints=[
                "Check bal < amount before executing updates",
                "Execute both updates and call conn.commit()"
            ],
            test_cases=[
                {"input": "", "expected_output": "[('A', 50.0), ('B', 250.0)]", "description": "Verify transfer balances"}
            ],
            expected_substrings=["transfer_funds", "conn.commit"],
            solution="""import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("CREATE TABLE bank (acc TEXT PRIMARY KEY, balance REAL)")
cur.execute("INSERT INTO bank VALUES ('A', 200.0), ('B', 100.0)")
conn.commit()

def transfer_funds(conn, from_acc, to_acc, amount):
    cur = conn.cursor()
    cur.execute("SELECT balance FROM bank WHERE acc = ?", (from_acc,))
    bal = cur.fetchone()[0]
    if bal < amount:
        raise ValueError("Insufficient balance")
    cur.execute("UPDATE bank SET balance = balance - ? WHERE acc = ?", (amount, from_acc))
    cur.execute("UPDATE bank SET balance = balance + ? WHERE acc = ?", (amount, to_acc))
    conn.commit()

transfer_funds(conn, 'A', 'B', 150.0)
cur.execute("SELECT acc, balance FROM bank ORDER BY acc")
print("Balances:", cur.fetchall())
conn.close()
"""
        )
    ],
    quiz_questions=[
        QuizQuestion(
            id="m6-q1",
            question="What is the default standard database engine included with Python's standard library?",
            options=[
                "PostgreSQL",
                "SQLite (sqlite3)",
                "MySQL",
                "MongoDB"
            ],
            correct_index=1,
            explanation="Python includes SQLite as a built-in standard module (`sqlite3`), requiring no external server installation."
        ),
        QuizQuestion(
            id="m6-q2",
            question="Why should user inputs NEVER be formatted directly into SQL query strings with f-strings or % formatting?",
            options=[
                "It causes syntax errors on spaces",
                "It exposes the application to SQL Injection (SQLi) attacks",
                "It makes the database read-only",
                "Python does not support string interpolation"
            ],
            correct_index=1,
            explanation="Raw string interpolation in SQL opens direct vulnerabilities for attackers to inject arbitrary SQL statements."
        ),
        QuizQuestion(
            id="m6-q3",
            question="What method must be called on a connection object to persist changes made by INSERT, UPDATE, or DELETE?",
            options=[
                "conn.save()",
                "conn.commit()",
                "conn.flush()",
                "conn.persist()"
            ],
            correct_index=1,
            explanation="In standard Python database drivers, `commit()` permanently writes pending transaction operations to disk."
        ),
        QuizQuestion(
            id="m6-q4",
            question="What does `conn.rollback()` do?",
            options=[
                "Restores the database to its initial installation state",
                "Cancels the current uncommitted transaction and reverts pending modifications",
                "Deletes all tables",
                "Reboots the database server"
            ],
            correct_index=1,
            explanation="`rollback()` aborts the pending transaction, reverting any changes made since the last commit."
        ),
        QuizQuestion(
            id="m6-q5",
            question="What placeholder character does SQLite use for parameterized query arguments in Python?",
            options=[
                "?",
                "%s",
                ":val",
                "$"
            ],
            correct_index=0,
            explanation="The Python `sqlite3` driver uses `?` as its positional parameter marker."
        )
    ]
)

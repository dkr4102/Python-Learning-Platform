# Marwadi University Course 01AP0303 — Syllabus Coverage Matrix
## Programming with Python (45 Contact Hours • 8 Units)

This document provides a formal, bidirectional traceability matrix between Marwadi University's syllabus units for Course 01AP0303 and the curriculum lessons, practice laboratories, and practical projects implemented in Pip Learn 2.0.

---

### Unit 1 — Python Fundamentals & Syntax (6 Hours)
- **Module ID**: `MOD-01`
- **Assessment Weight**: 10 Marks
- **Artwork Reference**: `ART-05 The First Light`
- **Mini-Project**: Smart Calculator Engine

| Syllabus Requirement | Lesson ID | Topic & Practical Implementation |
|---|---|---|
| Introduction to Python & Architecture | `m1-l1` | CPython runtime compilation, bytecode (`.pyc`), PVM execution model, indentation rules |
| Variables, Naming & Dynamic Typing | `m1-l2` | Object pointers in heap memory, id() addresses, immutable primitive types (int, float, str, bool) |
| Type Conversion & Casting | `m1-l3` | Implicit coercion vs explicit casting constructors (int, float, str, bool truthiness) |
| Operators & Precedence (PEMDAS) | `m1-l4` | Arithmetic, floor division (`//`), modulo (`%`), comparisons, logical short-circuiting |
| Formatted Console I/O | `m1-l5` | f-string format specifiers (`:.2f`, `:,`, `:04d`, padding) and standard input handling |
| Practice Challenges | `m1-ex1`, `m1-ex2` | Temperature Conversion Utility (`m1-ex1`), Compound Bill & Tip Splitter (`m1-ex2`) |
| Practical Project | `proj-smart-calc` | Interactive Smart Calculator with arithmetic, percentage discounts, scientific powers, square roots, and ZeroDivisionError safeguards |

---

### Unit 2 — Control Flow, Loops & Functions (6 Hours)
- **Module ID**: `MOD-02`
- **Assessment Weight**: 12 Marks
- **Artwork Reference**: `ART-06 The Crossroads`
- **Mini-Project**: Employee Payroll Processing System

| Syllabus Requirement | Lesson ID | Topic & Practical Implementation |
|---|---|---|
| Conditional Branching & Guard Clauses | `m2-l1` | `if`, `elif`, `else`, ternary expressions, guard clause restructuring to defeat arrow anti-patterns |
| Iteration Paradigms & Control | `m2-l2` | `for` loops, `while` loops, `range(start, stop, step)`, `break`, `continue`, `pass`, and `for...else` |
| Pattern Generation Algorithms | `m2-l3` | 2D coordinate matrices, number triangles, right-angled star patterns, and centered pyramids |
| Modular Functions & Scope (LEGB) | `m2-l4` | Function signatures, default arguments, `*args`, `**kwargs`, and Local/Enclosing/Global/Built-in scope |
| Lambda Expressions & Recursion | `m2-l5` | Anonymous lambdas in sorting, recursive base cases vs recursive steps, Fibonacci sequences |
| Practice Challenges | `m2-ex1`, `m2-ex2` | Overtime Pay Function (`m2-ex1`), Recursive Exponentiation Function (`m2-ex2`) |
| Practical Project | `proj-payroll-system` | Enterprise Employee Payroll System with 1.5x overtime, 3 progressive tax brackets, deductions, and itemized payslips |

---

### Unit 3 — Built-in Data Structures & Strings (6 Hours)
- **Module ID**: `MOD-03`
- **Assessment Weight**: 12 Marks
- **Artwork Reference**: `ART-07 The Collection`
- **Mini-Project**: Inventory Management Tracker & Student Grade Analyzer

| Syllabus Requirement | Lesson ID | Topic & Practical Implementation |
|---|---|---|
| Lists, Slicing & Comprehensions | `m3-l1` | Dynamic arrays, negative indexing, step slicing, in-place sorting, list comprehensions |
| Tuples & Immutability | `m3-l2` | Fixed records, data integrity, tuple packing/unpacking, dictionary key hashability |
| Sets & Set Theory | `m3-l3` | O(1) hash lookups, uniqueness guarantees, union (`\|`), intersection (`&`), difference (`-`) |
| Dictionaries & Nested Records | `m3-l4` | Hash maps, safe access with `.get()`, dict comprehensions, nested JSON-like structures |
| String Processing & Methods | `m3-l5` | Slicing, strip, split, join, case transformations, substring validation |
| Practice Challenges | `m3-ex1`, `m3-ex2` | Student Grade Analyzer (`m3-ex1`), List Deduplication & Word Frequency Counter (`m3-ex2`) |
| Practical Project | `proj-inventory-tracker` | Complete Inventory Management Tracker supporting SKU addition, stock tracking, category valuation, and reorder alerts |

---

### Unit 4 — File Handling & Exception Architecture (6 Hours)
- **Module ID**: `MOD-04`
- **Assessment Weight**: 12 Marks
- **Artwork Reference**: `ART-08 The Archive`
- **Mini-Project**: Log File Analyzer

| Syllabus Requirement | Lesson ID | Topic & Practical Implementation |
|---|---|---|
| File I/O & Context Managers | `m4-l1` | File access modes (`r`, `w`, `a`, `b`), deterministic resource release with `with open` |
| File Pointers | `m4-l2` | Cursor manipulation using `seek(offset, whence)` and `tell()` |
| Exception Lifecycle | `m4-l3` | Multi-catch blocks, `try`, `except SpecificError`, `else` (success-only), `finally` (guaranteed cleanup) |
| Custom Exception Hierarchies | `m4-l4` | Domain-specific exception classes inheriting from `Exception` with custom contextual payloads |
| Python Diagnostic Logging | `m4-l5` | Telemetry configuration using the `logging` standard library across standard severity tiers |
| Practice Challenges | `m4-ex1`, `m4-ex2` | Fault-tolerant text accumulator (`m4-ex1`), Custom PasswordLengthError validator (`m4-ex2`) |
| Practical Project | `proj-log-analyzer` | Telemetry log analyzer parsing timestamps, log levels (INFO/WARNING/ERROR/CRITICAL), error rates, and audit reports |

---

### Unit 5 — Object-Oriented Programming (6 Hours)
- **Module ID**: `MOD-05`
- **Assessment Weight**: 12 Marks
- **Artwork Reference**: `ART-09 The Structure`
- **Mini-Project**: Banking Account Management System

| Syllabus Requirement | Lesson ID | Topic & Practical Implementation |
|---|---|---|
| Classes, Objects & `self` | `m5-l1` | Blueprints, instance allocation, `__init__` constructor, receiver binding via explicit `self` |
| Encapsulation & Properties | `m5-l2` | Data protection, private attributes (`__attr`), name mangling, Pythonic `@property` getters and setters |
| Inheritance & MRO | `m5-l3` | Single/multiple inheritance, `super()` delegation, Method Resolution Order (C3 Linearization) |
| Polymorphism & Abstraction | `m5-l4` | Duck-typing, abstract base classes (`abc.ABC`), and contract enforcement with `@abstractmethod` |
| Special Dunder Protocols | `m5-l5` | Operator overloading, `__str__`, `__repr__`, `__len__`, `__eq__`, `__add__` |
| Practice Challenges | `m5-ex1`, `m5-ex2` | Encapsulated BankAccount class (`m5-ex1`), Manager inheritance and pay override (`m5-ex2`) |
| Practical Project | `proj-banking-system` | Banking Account Management System with abstract Account base, Savings/Checking subclasses, and ledger audit history |

---

### Unit 6 — Relational Database Connectivity (6 Hours)
- **Module ID**: `MOD-06`
- **Assessment Weight**: 12 Marks
- **Artwork Reference**: `ART-10 The Connections`
- **Mini-Project**: Customer Record Management Application (SQLite + MySQL)

| Syllabus Requirement | Lesson ID | Topic & Practical Implementation |
|---|---|---|
| Relational Concepts & SQLite | `m6-l1` | Tables, schema design, primary keys, SQLite embedded engine, in-memory databases |
| SQL Injection Defense | `m6-l2` | Vulnerabilities of string interpolation vs secure parameterized query placeholders (`?`, `%s`) |
| Complete CRUD Operations | `m6-l3` | `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`, `fetchone`, `fetchall`, `rowcount` |
| ACID Transactions & Rollback | `m6-l4` | Atomicity, consistency, isolation, durability, `conn.commit()`, and `conn.rollback()` error recovery |
| Client-Server MySQL Concepts | `m6-l5` | Server architecture, connection strings, driver selection, PEP 249 DB-API 2.0 standards |
| Practice Challenges | `m6-ex1`, `m6-ex2` | Parameterized student database creator (`m6-ex1`), Atomic inter-account transfer function (`m6-ex2`) |
| Practical Project | `proj-customer-crm` | Database-backed CRM system supporting parameterized create, list, search, update, and delete with unique constraints |

---

### Unit 7 — REST APIs, Automation & Reporting (6 Hours)
- **Module ID**: `MOD-07`
- **Assessment Weight**: 12 Marks
- **Artwork Reference**: `ART-11 The Horizon`
- **Mini-Project**: Weather API Dashboard & Email Automation Tool

| Syllabus Requirement | Lesson ID | Topic & Practical Implementation |
|---|---|---|
| REST Architecture & HTTP | `m7-l1` | Client-server model, GET/POST/PUT/DELETE verbs, headers, payload formats, HTTP status code families |
| Consuming APIs with `requests` | `m7-l2` | Query parameters, JSON deserialization with `.json()`, header passing, `raise_for_status()` |
| Network Error Recovery | `m7-l3` | Handling `ConnectionError`, `Timeout`, and `HTTPError` with clean offline fallback recovery |
| Email Automation & Security | `m7-l4` | MIME multi-part construction (`email.mime`), plain-text/HTML, safe dispatch previews, credential hygiene |
| Automated Report Synthesis | `m7-l5` | Telemetry aggregation, scheduled execution pipelines, automated markdown audit synthesis |
| Practice Challenges | `m7-ex1`, `m7-ex2` | Safe API JSON parser (`m7-ex1`), MIME academic score notice template generator (`m7-ex2`) |
| Practical Project | `proj-weather-dashboard` | Live meteorological REST ingestion dashboard with multi-city weather lookup and offline fallback recovery, paired with the Email Automation Tool |

---

### Unit 8 — Numerical Computing & Data Visualization (3 Hours)
- **Module ID**: `MOD-08`
- **Assessment Weight**: 10 Marks
- **Artwork Reference**: `ART-12 The Observatory`
- **Mini-Project**: Sales Analytics Dashboard

| Syllabus Requirement | Lesson ID | Topic & Practical Implementation |
|---|---|---|
| NumPy Arrays & Vectorization | `m8-l1` | High-performance contiguous C buffers, homogeneous typing, 2D matrix slicing, broadcasting |
| Pandas Series & DataFrames | `m8-l2` | Tabular data modeling, labeled columns and indices, boolean masking, statistical `.describe()` |
| Data Hygiene & Missing Values | `m8-l3` | Handling `NaN`, `.isna()`, `.dropna()`, `.fillna()`, deduplication, compound filtering |
| Split-Apply-Combine Groupby | `m8-l4` | Grouping tabular records by category and region, computing sum, mean, and count aggregations |
| Matplotlib Chart Generation | `m8-l5` | Figures, axes, bar charts, pie charts, base64 raster export in headless environments (`matplotlib.use('Agg')`) |
| Practice Challenges | `m8-ex1`, `m8-ex2` | Vectorized revenue calculation with NumPy (`m8-ex1`), Pandas department salary groupby (`m8-ex2`) |
| Practical Project | `proj-sales-analytics` | Comprehensive commercial sales dashboard with vectorized revenue calculation, multi-dimensional group aggregations, and Matplotlib chart generation |

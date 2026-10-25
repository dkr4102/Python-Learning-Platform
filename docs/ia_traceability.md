# Marwadi University Course 01AP0303 — Internal Assessment Traceability
## 100-Mark Comprehensive Academic Evaluation Rubric

This document maps each evaluation criterion from the Marwadi University Internal Assessment (IA) scheme for Course 01AP0303 (Programming with Python) to the specific architecture, modules, test evidence, and user experiences delivered in Pip Learn 2.0.

---

## 1. Evaluation Breakdown Structure

| Evaluation Category | Allocated Marks | Core Subject Area | Verification Mechanism |
|---|---|---|---|
| **Module 1 Assessment** | 10 Marks | Python Fundamentals & Core Syntax | Module 1 Quiz, Practice Lab (`m1-ex1`, `m1-ex2`), Smart Calculator |
| **Module 2 Assessment** | 12 Marks | Control Flow, Iteration & Functions | Module 2 Quiz, Practice Lab (`m2-ex1`, `m2-ex2`), Payroll System |
| **Module 3 Assessment** | 12 Marks | Data Structures & String Processing | Module 3 Quiz, Practice Lab (`m3-ex1`, `m3-ex2`), Inventory Tracker & Grade Analyzer |
| **Module 4 Assessment** | 12 Marks | File Handling & Exception Architecture | Module 4 Quiz, Practice Lab (`m4-ex1`, `m4-ex2`), Log File Analyzer |
| **Module 5 Assessment** | 12 Marks | Object-Oriented Programming (OOP) | Module 5 Quiz, Practice Lab (`m5-ex1`, `m5-ex2`), Banking System |
| **Module 6 Assessment** | 12 Marks | Relational Database Connectivity (SQL) | Module 6 Quiz, Practice Lab (`m6-ex1`, `m6-ex2`), Customer CRM Application |
| **Module 7 Assessment** | 12 Marks | REST APIs, Task Automation & MIME | Module 7 Quiz, Practice Lab (`m7-ex1`, `m7-ex2`), Weather Dashboard & Email Tool |
| **Common Evaluation: Creativity & UX** | 4 Marks | Aesthetics, Restrained Warmth, Identity | Editorial CSS, Curated Palette, 12 Artworks, Responsive Scrims |
| **Common Evaluation: Smooth Navigation** | 4 Marks | UX Flow & Architectural Consistency | 12 Core Screen Types, Full Breadcrumb Interconnection |
| **Common Evaluation: Testing & QA** | 4 Marks | Automated Testing, Runner Security | Pytest Suite (22 Passing Tests), Subprocess Isolation Sandbox |
| **Common Evaluation: Documentation** | 3 Marks | Project Architecture, Code Integrity | Technical README, Architecture Maps, Traceability Dossiers |
| **Common Evaluation: Presentation** | 3 Marks | Working Demonstrations & Viva Readiness | 10 Interactive Functional Mini-Projects, Live Code Execution |
| **Total Evaluation Marks** | **100 Marks** | **Complete Python Academic Suite** | **Fully Satisfied & Verifiable Locally** |

---

## 2. Detailed Evidence by Assessment Criterion

### 2.1 Module 1: Python Fundamentals (10 Marks)
- **Conceptual Coverage**: Architecture of CPython compiler, AST generation, bytecode interpretation on PVM, immutable primitive memory allocations, explicit casting, operator precedence.
- **Working Code Examples**: 5 executable lessons with live interactive workbenches and memory pointer visualization.
- **Practice Problems**: Temperature Conversion Utility (`m1-ex1`), Compound Bill & Tip Splitter (`m1-ex2`).
- **Assessment**: 5-question multiple-choice assessment evaluating valid identifiers, division float semantics, and type casting.
- **Mini-Project**: Smart Calculator Engine performing arithmetic, percentage discounts, square roots, and power calculations with zero-division guardrails.

### 2.2 Module 2: Control Flow & Functions (12 Marks)
- **Conceptual Coverage**: Decision trees, ternary expressions, guard clauses, definite iteration with range steps, indefinite while loops, pattern generation, modular functions, LEGB scope rules, lambda functions, and recursive base cases.
- **Working Code Examples**: 5 executable lessons including number triangles, pyramid asterisks, and recursive Fibonacci.
- **Practice Problems**: Overtime Pay Calculator (`m2-ex1`), Recursive Exponentiation Function (`m2-ex2`).
- **Assessment**: 5-question assessment evaluating range steps, loop-else semantics, `*args` tuple packing, and LEGB namespace priority.
- **Mini-Project**: Employee Payroll Processing System with 1.5x overtime premiums, progressive tax brackets, and itemized net pay statements.

### 2.3 Module 3: Data Structures (12 Marks)
- **Conceptual Coverage**: Dynamic list slicing (`[start:stop:step]`), list comprehensions, immutable tuples as dictionary keys, O(1) hash sets, mathematical set theory (union, intersection, difference), dictionary hash tables with `.get()`, and string manipulation.
- **Working Code Examples**: 5 lessons with interactive slicing coordinate visualizer.
- **Practice Problems**: Student Grade Analyzer (`m3-ex1`), List Deduplication and Word Frequency Counter (`m3-ex2`).
- **Assessment**: 5-question assessment evaluating collection mutability, set intersection operators, safe dictionary retrieval, and string slicing.
- **Mini-Projects**: 
  1. Inventory Management Tracker with SKU-based cataloging, stock counts, category valuation, and reorder alerts.
  2. Student Grade Analyzer computing averages, GPA points, and letter grades.

### 2.4 Module 4: File Handling & Exception Handling (12 Marks)
- **Conceptual Coverage**: Deterministic context managers (`with open`), text vs binary modes, cursor offsets with `seek()` and `tell()`, the complete 4-clause exception lifecycle (`try...except...else...finally`), custom exception classes, and the standard `logging` library.
- **Working Code Examples**: 5 executable lessons with in-memory stream testing.
- **Practice Problems**: Fault-tolerant integer accumulator (`m4-ex1`), Custom PasswordLengthError exception validator (`m4-ex2`).
- **Assessment**: 5-question assessment evaluating file truncation modes, guaranteed finally execution, bare except risks, and logging severity hierarchies.
- **Mini-Project**: Server Log File Analyzer classifying events into INFO, WARNING, ERROR, and CRITICAL with automated error rate calculation.

### 2.5 Module 5: Object-Oriented Programming (12 Marks)
- **Conceptual Coverage**: Class blueprints vs heap instances, constructor initialization (`__init__`), instance receiver binding (`self`), access control (`_protected`, `__private` name mangling), `@property` getters/setters, single/multiple inheritance, `super()` delegation, MRO C3 linearization, duck typing, abstract base classes (`abc.ABC`, `@abstractmethod`), and dunder protocols (`__str__`, `__repr__`, `__len__`, `__eq__`, `__add__`).
- **Working Code Examples**: 5 executable lessons with OOP encapsulation and vector mathematics.
- **Practice Problems**: Encapsulated BankAccount class (`m5-ex1`), Manager inheritance and pay override (`m5-ex2`).
- **Assessment**: 5-question assessment evaluating constructor roles, super() delegation, property decorators, and dunder protocols.
- **Mini-Project**: Banking Account Management System featuring abstract BaseAccount, specialized SavingsAccount (compound interest) and CheckingAccount (overdraft limits), and transaction ledger audits.

### 2.6 Module 6: Database Connectivity (12 Marks)
- **Conceptual Coverage**: Relational database principles, schema design, primary keys, SQLite embedded engine, SQL injection vulnerabilities, parameterized placeholder queries (`?`, `%s`), full CRUD operations, ACID transactions (`commit` and `rollback`), and client-server MySQL comparisons.
- **Working Code Examples**: 5 executable lessons with in-memory SQLite schema creation and execution.
- **Practice Problems**: Parameterized student database creator (`m6-ex1`), Atomic inter-account transfer function (`m6-ex2`).
- **Assessment**: 5-question assessment evaluating built-in database engines, SQL injection mitigation, commit persistence, and rollback semantics.
- **Mini-Project**: Database-backed Customer Relationship Management (CRM) application with SQLite storage, full CRUD operations, search filtering, unique email constraints, and documented MySQL connection guidelines.

### 2.7 Module 7: API Integration, Automation & Reporting (12 Marks)
- **Conceptual Coverage**: REST architecture, HTTP methods (GET, POST), headers, status code families (2xx, 3xx, 4xx, 5xx), the `requests` library, JSON deserialization with `.json()`, network failure recovery (`ConnectionError`, `Timeout`, `HTTPError`), MIME email construction (`email.mime`), and automated markdown report generation.
- **Working Code Examples**: 5 executable lessons with interactive REST flow diagram.
- **Practice Problems**: Safe API JSON parser (`m7-ex1`), MIME academic score notice template generator (`m7-ex2`).
- **Assessment**: 5-question assessment evaluating HTTP verbs, timeout necessity, JSON decoding, and SMTP protocols.
- **Mini-Projects**: 
  1. Weather API Dashboard consuming live public REST meteorological endpoints with offline fallback.
  2. Email Automation Tool generating RFC-compliant MIME message templates with safe preview mode.

### 2.8 Common Internal Assessment Criteria (18 Marks)
- **Creativity, UI/UX and Learner Engagement (4 Marks)**: Built as an editorial learning studio inspired by classical fine art and modern software craftsmanship. Uses curated typography (`Instrument Serif`, `Inter`, `JetBrains Mono`), tailored color palette (`#F5F2EC`, `#FBF8F3`, `#23342B`), and integration of 12 original oil painting masterworks.
- **Smooth Navigation and Integration (4 Marks)**: Seamless routing across 12 core screen types, persistent header navigation, breadcrumb hierarchies, and interlinked module/practice/project flows.
- **Testing, Debugging and Feedback (4 Marks)**: Fully automated Pytest test suite with 22 tests validating curriculum schemas, database persistence, isolated execution security, and all 10 practical applications.
- **Documentation and Project Report (3 Marks)**: Comprehensive architectural documentation, syllabus mapping matrix, and live downloadable JSON/Markdown academic reports.
- **Presentation and Viva Readiness (3 Marks)**: Fully runnable local application with interactive project workshops ready for real-time university faculty demonstration.

"""
Module 5: Object-Oriented Programming
Marwadi University 01AP0303 - Unit 5 (6 Contact Hours, 12 Marks Assessment)
Mini-Project: Banking Account Management System
"""
from app.curriculum.models import Module, Lesson, PracticeExercise, QuizQuestion, ProjectInfo, CommonMistake, MiniCheckpoint

MODULE_5 = Module(
    id=5,
    code="MOD-05",
    title="Object-Oriented Programming",
    syllabus_unit="Unit 5: Classes, Objects, Inheritance & Abstraction",
    contact_hours=6,
    assessment_marks=12,
    description="Model complex real-world software domains with classes, encapsulation, inheritance hierarchies, polymorphic interfaces, property decorators, and dunder methods.",
    learning_objectives=[
        "Author clean Python classes with constructor initialization (__init__) and self binding",
        "Enforce data encapsulation using protected (_attr) and private (__attr) mangled attributes and @property decorators",
        "Construct inheritance hierarchies with single and multiple inheritance, super(), and MRO resolution",
        "Implement polymorphism via method overriding and duck-typing",
        "Define formal interfaces with abstract base classes (abc.ABC) and dunder protocols (__str__, __repr__, __eq__)"
    ],
    topics_covered=[
        "Classes & Instantiation (__init__, self, instance vs class state)",
        "Encapsulation: Access Modifiers & Python's Name Mangling",
        "Pythonic Properties (@property, getter, setter, deleter)",
        "Inheritance: Parent-Child Hierarchies & super()",
        "Multiple Inheritance & Method Resolution Order (C3 Linearization / MRO)",
        "Polymorphism & Duck-Typing",
        "Abstraction with abc.ABC & @abstractmethod",
        "Special Dunder Protocols (__str__, __repr__, __len__, __add__)"
    ],
    artwork_id="ART-09",
    project=ProjectInfo(
        id="proj-banking-system",
        title="Banking Account Management System",
        subtitle="Secure Ledger, Transaction Audit & Account Hierarchy Engine",
        objective="Design an enterprise banking software suite implementing an abstract Account base class, specialized SavingsAccount (with interest calculation) and CheckingAccount (with overdraft protection), transaction ledger history, and security PIN validation.",
        requirements=[
            "Encapsulate account balance and transaction ledger with private attributes",
            "Support verified deposits, withdrawals, and inter-account transfers",
            "Implement overdraft protection rules for checking accounts",
            "Accrue monthly compound interest on savings accounts",
            "Generate timestamped ledger statements showing transaction histories"
        ],
        starter_snippet="""# Module 5 Project: Banking Account System
class BankAccount:
    def __init__(self, account_number, holder_name, initial_balance=0.0):
        self.account_number = account_number
        self.holder_name = holder_name
        self._balance = initial_balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        self.transactions.append(f"Deposit: +${amount:.2f}")
        return self._balance

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient balance.")
        self._balance -= amount
        self.transactions.append(f"Withdrawal: -${amount:.2f}")
        return self._balance
""",
        module_id=5
    ),
    lessons=[
        Lesson(
            id="m5-l1",
            title="Classes, Objects, and the `self` Binding",
            subtitle="Understanding how Python instantiates objects and resolves method receivers.",
            reading_time_min=7,
            concept_markdown="""### The Blueprint and the Instance

A **class** is a blueprint defining attributes (state) and methods (behavior). An **object** is a concrete instance allocated in memory.

```python
class Student:
    # Class variable (shared across all instances)
    institution = "Marwadi University"

    # Constructor method
    def __init__(self, name, enrollment_no):
        # Instance variables (unique to each object)
        self.name = name
        self.enrollment_no = enrollment_no
```

#### What is `self`?
In Python, `self` is not a magic language keyword, but an explicit parameter that represents the **specific object instance** calling the method.
When you call:
```python
student1.get_details()
```
Python internally translates this into:
```python
Student.get_details(student1)
```
The caller instance is passed automatically as the first argument.
""",
            syntax_example="""# Class definition and instance creation
class Course:
    def __init__(self, code, name, credits=4):
        self.code = code
        self.name = name
        self.credits = credits

    def display(self):
        return f"{self.code}: {self.name} ({self.credits} Credits)"

c1 = Course("01AP0303", "Programming with Python")
print(c1.display())
""",
            executable_code="""# Executable class and instance demonstration
class BankCustomer:
    bank_name = "Pip Reserve Bank"

    def __init__(self, customer_id, name):
        self.customer_id = customer_id
        self.name = name
        self.active = True

    def summary(self):
        return f"Customer #{self.customer_id:04d}: {self.name} [{self.bank_name}]"

c1 = BankCustomer(101, "Aarav Sharma")
c2 = BankCustomer(102, "Priya Patel")

print(c1.summary())
print(c2.summary())
print("Same bank entity?", c1.bank_name is c2.bank_name)
""",
            expected_output="""Customer #0101: Aarav Sharma [Pip Reserve Bank]
Customer #0102: Priya Patel [Pip Reserve Bank]
Same bank entity? True""",
            output_explanation="Both instances have distinct customer_id and name attributes, while sharing the class-level variable bank_name.",
            common_mistakes=[
                CommonMistake(
                    mistake="Forgetting to put `self` as the first parameter of an instance method",
                    explanation="Calling my_obj.method() passes my_obj as the first arg; omitting self raises TypeError: method() takes 0 positional arguments but 1 was given.",
                    correction="Always include `self` as the first argument for standard instance methods."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What is the fundamental difference between an instance variable and a class variable?",
                options=[
                    "Instance variables are stored in files, class variables are in memory",
                    "Instance variables belong to a specific object; class variables are shared across all instances of the class",
                    "Class variables cannot be modified",
                    "Instance variables must always be numbers"
                ],
                correct_index=1,
                explanation="Instance variables maintain separate values per object, whereas class variables are shared at the class level."
            )
        ),
        Lesson(
            id="m5-l2",
            title="Encapsulation & The @property Decorator",
            subtitle="Data hiding, name mangling, and idiomatic Pythonic getters/setters.",
            reading_time_min=7,
            concept_markdown="""### Encapsulation and Data Protection

Encapsulation restricts direct external access to internal object state to prevent corruption.

#### Python's Naming Conventions:
- `public_var`: Accessible from anywhere.
- `_protected_var`: Single leading underscore. Indicates internal API; subclasses may access it, but external code should treat it as non-public.
- `__private_var`: Double leading underscore. Triggers **name mangling** (Python renames it internally to `_ClassName__private_var` to prevent accidental overriding in subclasses).

#### The `@property` Decorator
Java and C++ require explicit `getBalance()` and `setBalance(val)` methods. In Python, the `@property` decorator allows method calls with clean attribute access syntax:

```python
class Account:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):
        '''Getter property'''
        return self._balance

    @balance.setter
    def balance(self, value):
        '''Setter with validation'''
        if value < 0:
            raise ValueError("Balance cannot be negative!")
        self._balance = value
```
Now callers can write `acc.balance = 500` or `print(acc.balance)` while still executing your validation logic!
""",
            syntax_example="""# Using @property for temperature conversion
class Temperature:
    def __init__(self, celsius=0.0):
        self._celsius = celsius

    @property
    def fahrenheit(self):
        return (self._celsius * 9/5) + 32

t = Temperature(25.0)
print(f"25C = {t.fahrenheit}F")
""",
            executable_code="""# Executable @property and name mangling demonstration
class SecureWallet:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # Private attribute

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.__balance += amount
        return self.__balance

wallet = SecureWallet("Priya", 150.0)
print(f"Owner: {wallet.owner}, Balance: ${wallet.balance:.2f}")
wallet.deposit(50.0)
print(f"New Balance: ${wallet.balance:.2f}")
print("Mangled attribute exists:", hasattr(wallet, "_SecureWallet__balance"))
""",
            expected_output="""Owner: Priya, Balance: $150.00
New Balance: $200.00
Mangled attribute exists: True""",
            output_explanation="Direct access to wallet.__balance fails, but the @property getter safely exposes the read-only balance. Name mangling is confirmed via _SecureWallet__balance.",
            common_mistakes=[
                CommonMistake(
                    mistake="Naming the property getter and the internal variable identically: @property def balance(self): return self.balance",
                    explanation="Calling self.balance inside the balance getter triggers infinite recursion: RecursionError: maximum recursion depth exceeded.",
                    correction="Use a leading underscore for the private storage attribute: return self._balance."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What does Python do to an attribute declared with double leading underscores, such as `__balance`?",
                options=[
                    "Deletes it from memory",
                    "Encrypts it using AES-256",
                    "Performs name mangling, prefixing it with _ClassName",
                    "Makes it accessible only to C extensions"
                ],
                correct_index=2,
                explanation="Python performs name mangling, transforming `__balance` in `Account` into `_Account__balance` to prevent namespace collisions."
            )
        ),
        Lesson(
            id="m5-l3",
            title="Inheritance, super(), and MRO",
            subtitle="Extending classes, calling superclass initializers, and Method Resolution Order.",
            reading_time_min=7,
            concept_markdown="""### Class Inheritance

Inheritance allows a child class to acquire attributes and behaviors from a parent class, facilitating code reuse and domain modeling.

```python
class Account:
    def __init__(self, account_no, balance=0.0):
        self.account_no = account_no
        self.balance = balance

class SavingsAccount(Account):
    def __init__(self, account_no, balance=0.0, interest_rate=0.04):
        # Delegate initialization to parent class
        super().__init__(account_no, balance)
        self.interest_rate = interest_rate
```

#### Method Resolution Order (MRO)
In multiple inheritance, Python resolves attribute lookups using the **C3 Linearization Algorithm**:
```python
print(SavingsAccount.mro())
# [SavingsAccount, Account, object]
```
The `super()` function guarantees each parent class in the MRO chain is visited in predictable, consistent order.
""",
            syntax_example="""# Single inheritance hierarchy
class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, major):
        super().__init__(name)
        self.major = major

s = Student("Aarav", "Computer Engineering")
print(s.name, "-", s.major)
""",
            executable_code="""# Executable inheritance and MRO inspection
class BaseAccount:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance

    def get_info(self):
        return f"Acc #{self.account_id}: Balance ${self.balance:.2f}"

class SavingsAccount(BaseAccount):
    def __init__(self, account_id, balance, rate=0.035):
        super().__init__(account_id, balance)
        self.rate = rate

    def apply_interest(self):
        interest = self.balance * self.rate
        self.balance += interest
        return interest

sav = SavingsAccount("SA-1001", 1000.0)
print(sav.get_info())
earned = sav.apply_interest()
print(f"Interest earned @ 3.5%: ${earned:.2f}")
print("Updated:", sav.get_info())
print("MRO:", [cls.__name__ for cls in SavingsAccount.mro()])
""",
            expected_output="""Acc #SA-1001: Balance $1000.00
Interest earned @ 3.5%: $35.00
Updated: Acc #SA-1001: Balance $1035.00
MRO: ['SavingsAccount', 'BaseAccount', 'object']""",
            output_explanation="SavingsAccount inherits BaseAccount's attributes and methods while extending it with interest calculations. MRO shows resolution up to object.",
            common_mistakes=[
                CommonMistake(
                    mistake="Overriding `__init__` in a child class without calling `super().__init__(...)`",
                    explanation="If super().__init__() is omitted, parent attributes are never initialized, causing AttributeError when accessed.",
                    correction="Always invoke `super().__init__(...)` inside derived class constructors."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What built-in method or attribute shows the order in which Python searches parent classes for methods?",
                options=[
                    "class.search_path",
                    "class.mro() or class.__mro__",
                    "class.parents()",
                    "class.__bases__"
                ],
                correct_index=1,
                explanation="The `.mro()` method or `.__mro__` attribute returns the Method Resolution Order tuple."
            )
        ),
        Lesson(
            id="m5-l4",
            title="Polymorphism & Abstract Base Classes (ABC)",
            subtitle="Contract-driven architecture with abc.ABC and @abstractmethod.",
            reading_time_min=7,
            concept_markdown="""### Polymorphism and Abstract Interfaces

**Polymorphism** allows different classes to respond to the same method invocation in their own specialized way.

#### Abstract Base Classes (`abc.ABC`)
An **Abstract Base Class (ABC)** defines a contract or interface that derived classes must implement. You **cannot instantiate an ABC directly**:

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        '''Abstract method: subclasses MUST implement this.'''
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Charging ${amount:.2f} to Credit Card.")
        return True

class UPIProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Initiating UPI transfer of ${amount:.2f}.")
        return True
```
If a subclass fails to implement `@abstractmethod`, Python refuses to instantiate it, raising `TypeError: Can't instantiate abstract class with abstract methods`.
""",
            syntax_example="""# Duck typing in Python
def process_checkout(processor, total):
    # Doesn't care about type, as long as it has .process_payment()
    return processor.process_payment(total)
""",
            executable_code="""# Executable ABC and Polymorphism demo
from abc import ABC, abstractmethod

class NotificationSender(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> str:
        pass

class EmailNotifier(NotificationSender):
    def send(self, recipient: str, message: str) -> str:
        return f"[Email to {recipient}] {message}"

class SMSNotifier(NotificationSender):
    def send(self, recipient: str, message: str) -> str:
        return f"[SMS to {recipient}] {message}"

# Polymorphic dispatcher
notifiers = [EmailNotifier(), SMSNotifier()]
for notifier in notifiers:
    print(notifier.send("user@marwadi.edu", "Internal Assessment starts Monday."))
""",
            expected_output="""[Email to user@marwadi.edu] Internal Assessment starts Monday.
[SMS to user@marwadi.edu] Internal Assessment starts Monday.""",
            output_explanation="Both concrete classes adhere to the NotificationSender abstract interface, allowing polymorphic dispatch across any notifier implementation.",
            common_mistakes=[
                CommonMistake(
                    mistake="Attempting to instantiate an abstract base class directly: p = PaymentProcessor()",
                    explanation="Python blocks instantiation of classes containing unimplemented @abstractmethod decorators.",
                    correction="Instantiate concrete subclasses that implement all abstract methods."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What happens if a concrete subclass fails to implement an `@abstractmethod` defined in its parent ABC?",
                options=[
                    "It defaults to returning None",
                    "Python raises TypeError when attempting to instantiate the subclass",
                    "The program crashes during import",
                    "It creates an empty method"
                ],
                correct_index=1,
                explanation="Python prevents instantiation of any class with unimplemented abstract methods."
            )
        ),
        Lesson(
            id="m5-l5",
            title="Dunder Protocols: __str__, __repr__, and __len__",
            subtitle="Customizing Python object representation and operator overloading.",
            reading_time_min=6,
            concept_markdown="""### Special "Dunder" (Double Underscore) Methods

Python classes integrate with built-in language operations (like `print()`, `str()`, `len()`, `+`) through special methods with double underscores:

#### Representation:
- `__str__(self)`: Human-friendly string intended for end-users (called by `print()` and `str()`).
- `__repr__(self)`: Unambiguous, developer-oriented string (ideally valid Python code that could recreate the object).

#### Sequence & Math Protocols:
- `__len__(self)`: Called by `len(my_obj)`.
- `__eq__(self, other)`: Called by `my_obj == other`.
- `__add__(self, other)`: Overloads the `+` operator.
""",
            syntax_example="""# Implementing __str__ and __repr__
class Account:
    def __init__(self, id, balance):
        self.id = id
        self.balance = balance

    def __str__(self):
        return f"Account #{self.id} (${self.balance:,.2f})"

    def __repr__(self):
        return f"Account(id={self.id!r}, balance={self.balance!r})"
""",
            executable_code="""# Executable dunder method demonstration
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    def __str__(self):
        return f"<{self.x}, {self.y}>"

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

v1 = Vector2D(3, 4)
v2 = Vector2D(1, 2)
v3 = v1 + v2

print("v1 string:", str(v1))
print("v3 representation:", repr(v3))
print("v1 + v2 =", v3)
print("v3 == Vector2D(4, 6):", v3 == Vector2D(4, 6))
""",
            expected_output="""v1 string: <3, 4>
v3 representation: Vector2D(4, 6)
v1 + v2 = <4, 6>
v3 == Vector2D(4, 6): True""",
            output_explanation="Overriding __add__ enables mathematical '+' syntax on Vector2D objects, while __str__ and __repr__ provide clean text representations.",
            common_mistakes=[
                CommonMistake(
                    mistake="Returning a non-string object from `__str__` or `__repr__`",
                    explanation="Python expects `__str__` and `__repr__` to return `str`; returning an int or None raises TypeError.",
                    correction="Ensure the return value is explicitly formatted as a string."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="Which special method is invoked when `print(obj)` or `str(obj)` is called on an instance?",
                options=["__print__", "__repr__", "__str__", "__format__"],
                correct_index=2,
                explanation="The `__str__` method provides user-facing string representation for print() and str()."
            )
        )
    ],
    practice_exercises=[
        PracticeExercise(
            id="m5-ex1",
            title="Encapsulated Bank Account Class",
            difficulty="Beginner",
            problem_statement="Create a class `BankAccount` with private attribute `__balance`. Provide a property getter `balance`, and methods `deposit(amount)` and `withdraw(amount)`. Withdrawals exceeding balance must raise ValueError('Insufficient funds').",
            input_output_expectations="Initialize with 100, deposit 50, withdraw 30, print balance: Balance: $120.00",
            starter_code="""class BankAccount:
    def __init__(self, initial_balance=0.0):
        self.__balance = initial_balance

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        self.__balance += amount
        return self.__balance

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
        return self.__balance

acc = BankAccount(100.0)
acc.deposit(50.0)
acc.withdraw(30.0)
print(f"Balance: ${acc.balance:.2f}")
""",
            hints=[
                "Store balance in self.__balance",
                "Define @property def balance(self): return self.__balance"
            ],
            test_cases=[
                {"input": "", "expected_output": "Balance: $120.00", "description": "100 + 50 - 30 = 120"}
            ],
            expected_substrings=["__balance", "@property", "deposit", "withdraw"],
            solution="""class BankAccount:
    def __init__(self, initial_balance=0.0):
        self.__balance = initial_balance

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        self.__balance += amount
        return self.__balance

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
        return self.__balance

acc = BankAccount(100.0)
acc.deposit(50.0)
acc.withdraw(30.0)
print(f"Balance: ${acc.balance:.2f}")
"""
        ),
        PracticeExercise(
            id="m5-ex2",
            title="Inheritance and Method Overriding",
            difficulty="Intermediate",
            problem_statement="Create a base class `Employee(name, base_salary)` with method `calculate_pay()`. Subclass `Manager(Employee, bonus)` which overrides `calculate_pay()` to return base_salary + bonus.",
            input_output_expectations="Manager 'Aarav' with base 50000 and bonus 12000 must print 'Manager Aarav Pay: $62,000.00'",
            starter_code="""class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def calculate_pay(self):
        return self.base_salary

class Manager(Employee):
    def __init__(self, name, base_salary, bonus):
        super().__init__(name, base_salary)
        self.bonus = bonus

    def calculate_pay(self):
        return self.base_salary + self.bonus

m = Manager("Aarav", 50000.0, 12000.0)
print(f"Manager {m.name} Pay: ${m.calculate_pay():,.2f}")
""",
            hints=[
                "Call super().__init__(name, base_salary)",
                "Override calculate_pay() to return self.base_salary + self.bonus"
            ],
            test_cases=[
                {"input": "", "expected_output": "Manager Aarav Pay: $62,000.00", "description": "Verify pay calculation"}
            ],
            expected_substrings=["super().__init__", "calculate_pay"],
            solution="""class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def calculate_pay(self):
        return self.base_salary

class Manager(Employee):
    def __init__(self, name, base_salary, bonus):
        super().__init__(name, base_salary)
        self.bonus = bonus

    def calculate_pay(self):
        return self.base_salary + self.bonus

m = Manager("Aarav", 50000.0, 12000.0)
print(f"Manager {m.name} Pay: ${m.calculate_pay():,.2f}")
"""
        )
    ],
    quiz_questions=[
        QuizQuestion(
            id="m5-q1",
            question="What is the purpose of the `__init__` method in Python?",
            options=[
                "To allocate raw RAM bytes for the operating system",
                "To initialize the newly created object's attributes upon instantiation",
                "To destroy an object when garbage collected",
                "To import a module into the class namespace"
            ],
            correct_index=1,
            explanation="`__init__` serves as the constructor initializer, setting up instance attributes when an object is created."
        ),
        QuizQuestion(
            id="m5-q2",
            question="What function is used to invoke a method from a parent superclass inside a child class?",
            options=[
                "parent()",
                "super()",
                "base()",
                "inherit()"
            ],
            correct_index=1,
            explanation="`super()` returns a proxy object that delegates method calls to a parent or sibling class in the MRO."
        ),
        QuizQuestion(
            id="m5-q3",
            question="Which decorator allows a method to be accessed like an attribute without parentheses?",
            options=[
                "@classmethod",
                "@staticmethod",
                "@property",
                "@attribute"
            ],
            correct_index=2,
            explanation="The `@property` decorator enables Pythonic getters, allowing `obj.prop` syntax instead of `obj.get_prop()`."
        ),
        QuizQuestion(
            id="m5-q4",
            question="What error is raised if you try to instantiate a class that inherits from `abc.ABC` but has not implemented all `@abstractmethod` decorators?",
            options=[
                "AttributeError",
                "TypeError",
                "NotImplementedError",
                "AbstractClassError"
            ],
            correct_index=1,
            explanation="Python raises `TypeError: Can't instantiate abstract class ... with abstract methods`."
        ),
        QuizQuestion(
            id="m5-q5",
            question="Which dunder method must be implemented to allow two custom objects to be compared using `==`?",
            options=[
                "__compare__",
                "__match__",
                "__eq__",
                "__is__"
            ],
            correct_index=2,
            explanation="The `__eq__(self, other)` method overloads the equality operator `==`."
        )
    ]
)

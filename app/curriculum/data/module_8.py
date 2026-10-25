"""
Module 8: Data Analytics and Visualization
Marwadi University 01AP0303 - Unit 8 (6 Contact Hours, Syllabus Unit 8 Capstone)
Mini-Project: Sales Analytics Dashboard
"""
from app.curriculum.models import Module, Lesson, PracticeExercise, QuizQuestion, ProjectInfo, CommonMistake, MiniCheckpoint

MODULE_8 = Module(
    id=8,
    code="MOD-08",
    title="Data Analytics & Visualization",
    syllabus_unit="Unit 8: Numerical Arrays, Pandas DataFrames & Matplotlib Analytics",
    contact_hours=6,
    assessment_marks=10,  # Capstone analytics module
    description="Analyze quantitative datasets with NumPy vectorized arrays, clean tabular records using Pandas DataFrames, aggregate business metrics with groupby, and synthesize visual charts with Matplotlib.",
    learning_objectives=[
        "Perform vectorized numerical operations and multi-dimensional slicing using NumPy ndarrays",
        "Load, inspect, clean, and manipulate tabular datasets with Pandas Series and DataFrames",
        "Handle missing data, drop duplicates, and perform conditional row filtering",
        "Calculate split-apply-combine aggregations using DataFrame groupby()",
        "Generate publication-quality bar charts, line plots, and pie charts with Matplotlib"
    ],
    topics_covered=[
        "NumPy: Multi-dimensional ndarrays, Vectorization & Broadcasting",
        "Pandas Fundamentals: Series & DataFrame Data Structures",
        "Data Ingestion: Reading & Writing CSV Datasets",
        "Data Hygiene: Missing Values (isna, dropna, fillna) & Filtering",
        "Group Aggregations: groupby(), sum(), mean() & pivot tables",
        "Matplotlib: Line Plots, Bar Charts, Histograms & Pie Charts",
        "Executive Analytics & Dashboard Report Synthesis"
    ],
    artwork_id="ART-12",
    project=ProjectInfo(
        id="proj-sales-analytics",
        title="Sales Analytics Dashboard",
        subtitle="Multi-Channel Revenue Ingestion, Group Aggregation & Chart Generator",
        objective="Construct an end-to-end data analytics workflow that ingests transactional sales data, cleans dirty entries, calculates revenue by product category and region using Pandas, and generates Matplotlib bar and line visualizations.",
        requirements=[
            "Construct a multi-column dataset with Date, Category, Region, Units Sold, and Unit Price",
            "Perform vectorized revenue calculations (Units Sold * Unit Price)",
            "Aggregate total sales and units sold grouped by Category and Region",
            "Generate Matplotlib charts (Category Revenue Bar Chart and Regional Distribution)",
            "Export an executive summary report with actionable commercial insights"
        ],
        starter_snippet="""# Module 8 Project: Sales Analytics Engine
import pandas as pd
import numpy as np

def analyze_sales_data(transactions_list):
    df = pd.DataFrame(transactions_list)
    df["Revenue"] = df["Units"] * df["Price"]
    summary = df.groupby("Category")["Revenue"].agg(["sum", "mean", "count"])
    return summary
""",
        module_id=8
    ),
    lessons=[
        Lesson(
            id="m8-l1",
            title="NumPy: Vectorized Arrays & Broadcasting",
            subtitle="High-performance numerical computing without explicit Python loops.",
            reading_time_min=7,
            concept_markdown="""### The Power of NumPy ndarrays

Python's built-in lists are flexible, but slow for numerical math because each element is a separate pointer to an object.

**NumPy (Numerical Python)** provides the `ndarray` (N-dimensional array):
1. **Contiguous Memory**: Numbers are packed tightly in contiguous memory buffers (C-level arrays).
2. **Homogeneous Typing**: All elements share the exact same data type (e.g. `np.float64`).
3. **Vectorization**: Mathematical operations apply across the entire array in parallel without writing Python `for` loops!

```python
import numpy as np

# Standard Python loop (slow)
data = [1, 2, 3, 4, 5]
squared = [x ** 2 for x in data]

# NumPy Vectorized (up to 50x faster)
arr = np.array([1, 2, 3, 4, 5])
squared_fast = arr ** 2
```

#### Broadcasting
NumPy enables arithmetic between arrays of different shapes if their dimensions are compatible (e.g. adding a scalar to a matrix).
""",
            syntax_example="""# Array creation and basic statistics
import numpy as np

grades = np.array([88, 92, 79, 95, 84, 91])
print("Mean:", np.mean(grades))
print("Standard Deviation:", np.std(grades))
print("Curved (+5%):", grades * 1.05)
""",
            executable_code="""# Executable NumPy demonstration
import numpy as np

# Create 2D matrix (3 students x 4 exams)
scores = np.array([
    [85, 90, 88, 92],
    [78, 82, 80, 85],
    [92, 95, 96, 98]
])

print("Array Shape (rows, cols):", scores.shape)
print("Student 3 Scores:", scores[2, :])
print("Exam 1 Class Average:", np.mean(scores[:, 0]))
print("Overall Highest Mark:", np.max(scores))
""",
            expected_output="""Array Shape (rows, cols): (3, 4)
Student 3 Scores: [92 95 96 98]
Exam 1 Class Average: 85.0
Overall Highest Mark: 98""",
            output_explanation="NumPy slices 2D arrays efficiently: scores[2, :] selects row index 2 across all columns, while scores[:, 0] isolates column 0.",
            common_mistakes=[
                CommonMistake(
                    mistake="Writing explicit Python for loops over NumPy arrays",
                    explanation="Looping in Python defeats the performance advantage of NumPy's compiled C backend.",
                    correction="Use vectorized operations (e.g. arr1 + arr2, np.sum(arr)) instead of for loops."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="Why is a NumPy ndarray significantly faster than a standard Python list for math?",
                options=[
                    "It uses cloud computing",
                    "It stores data in contiguous memory blocks with homogeneous types and vectorized C operations",
                    "It converts numbers to strings",
                    "It disables garbage collection"
                ],
                correct_index=1,
                explanation="NumPy achieves exceptional speed through contiguous memory layouts, fixed data types, and vectorized C SIMD execution."
            )
        ),
        Lesson(
            id="m8-l2",
            title="Pandas: Series & DataFrames",
            subtitle="The tabular data foundation for data science and analytics.",
            reading_time_min=7,
            concept_markdown="""### The Pandas Data Model

**Pandas** is Python's primary library for tabular data manipulation, built on top of NumPy.

#### Core Data Structures:
1. **`Series`**: A 1D labeled array capable of holding any data type.
2. **`DataFrame`**: A 2D labeled tabular structure with rows and columns (like a SQL table or Excel sheet).

```python
import pandas as pd

# Creating a DataFrame from a dictionary
data = {
    "Student": ["Aarav", "Priya", "Rohan"],
    "Department": ["CSE", "CSE", "IT"],
    "GPA": [3.85, 3.92, 3.60]
}
df = pd.DataFrame(data)
```

#### Key DataFrame Attributes & Methods:
- `df.head(n)`: View first n rows.
- `df.info()`: Inspect data types, memory usage, and non-null counts.
- `df.describe()`: Summary statistics (mean, std, min, max, quartiles).
- `df.shape`: Tuple of (row_count, column_count).
""",
            syntax_example="""# Reading a CSV file and column selection
import pandas as pd

# df = pd.read_csv('students.csv')
# print(df['GPA'].mean())
""",
            executable_code="""# Executable Pandas DataFrame demonstration
import pandas as pd

data = {
    "Course": ["01AP0303", "01AP0304", "01AP0305"],
    "Title": ["Python", "DBMS", "Algorithms"],
    "Enrollment": [120, 115, 98],
    "AvgMarks": [86.5, 82.0, 79.2]
}
df = pd.DataFrame(data)

print("DataFrame Head:")
print(df)
print("\nMean Enrollment:", df["Enrollment"].mean())
print("Courses with > 100 students:")
print(df[df["Enrollment"] > 100][["Course", "Title"]])
""",
            expected_output="""DataFrame Head:
     Course       Title  Enrollment  AvgMarks
0  01AP0303      Python         120      86.5
1  01AP0304        DBMS         115      82.0
2  01AP0305  Algorithms          98      79.2

Mean Enrollment: 111.0
Courses with > 100 students:
     Course   Title
0  01AP0303  Python
1  01AP0304    DBMS""",
            output_explanation="Pandas enables intuitive column selection and boolean masking (df[df['Enrollment'] > 100]) for tabular analysis.",
            common_mistakes=[
                CommonMistake(
                    mistake="Using single brackets for multiple columns: `df['Course', 'Title']`",
                    explanation="Passing multiple column names requires a list of strings inside brackets: `df[['Course', 'Title']]`.",
                    correction="Use double brackets when selecting multiple columns."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What method gives immediate descriptive statistical summaries (count, mean, std, min, quartiles) for numeric columns in a DataFrame?",
                options=["df.info()", "df.describe()", "df.summary()", "df.stats()"],
                correct_index=1,
                explanation="`df.describe()` generates quick statistical metrics across all numeric columns."
            )
        ),
        Lesson(
            id="m8-l3",
            title="Data Hygiene: Cleaning, Nulls & Filtering",
            subtitle="Handling missing data, deduplication, and conditional row subsets.",
            reading_time_min=7,
            concept_markdown="""### Cleaning Real-World Data

Real datasets are messy: records have missing values (`NaN`), duplicate rows, and invalid types.

#### Handling Missing Values (`NaN`):
- `df.isna().sum()`: Count null values per column.
- `df.dropna()`: Remove rows containing any null values.
- `df.fillna(value)`: Impute missing values with a fallback (e.g. column mean or `"Unknown"`).

#### Filtering with Boolean Indexing:
```python
# Multiple conditions with bitwise operators (& for AND, | for OR)
# Note: Each condition MUST be enclosed in parentheses!
high_performing = df[(df["GPA"] >= 3.8) & (df["Department"] == "CSE")]
```
""",
            syntax_example="""# Imputing missing values
df['Salary'] = df['Salary'].fillna(df['Salary'].median())
df = df.drop_duplicates()
""",
            executable_code="""# Executable data cleaning demonstration
import pandas as pd
import numpy as np

dirty_data = {
    "Name": ["Aarav", "Priya", "Rohan", "Sneha", "Aarav"],
    "Score": [88.0, np.nan, 72.0, 95.0, 88.0],
    "Dept": ["CSE", "CSE", np.nan, "IT", "CSE"]
}
df = pd.DataFrame(dirty_data)

print("Original Dirty Data:")
print(df)

# Drop duplicates
df = df.drop_duplicates()

# Impute missing score with column mean
mean_score = df["Score"].mean()
df["Score"] = df["Score"].fillna(mean_score)

# Fill missing department
df["Dept"] = df["Dept"].fillna("General")

print("\nCleaned Data:")
print(df)
""",
            expected_output="""Original Dirty Data:
    Name  Score Dept
0  Aarav   88.0  CSE
1  Priya    NaN  CSE
2  Rohan   72.0  NaN
3  Sneha   95.0   IT
4  Aarav   88.0  CSE

Cleaned Data:
    Name  Score     Dept
0  Aarav   88.0      CSE
1  Priya   85.0      CSE
2  Rohan   72.0  General
3  Sneha   95.0       IT""",
            output_explanation="Duplicates are dropped, missing scores are imputed with the mean (88+72+95)/3 = 85.0, and missing departments are filled with 'General'.",
            common_mistakes=[
                CommonMistake(
                    mistake="Using standard `and` / `or` in Pandas filters instead of `&` / `|`",
                    explanation="`and` evaluates truthiness of the entire Series, raising ValueError. Pandas requires element-wise bitwise `&` and `|`.",
                    correction="Use `(cond1) & (cond2)` with parentheses around each condition."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="How do you replace missing NaN values in a column with the number 0 in Pandas?",
                options=["df['col'].replace_null(0)", "df['col'].fillna(0)", "df['col'].clean(0)", "df['col'].drop(0)"],
                correct_index=1,
                explanation="`fillna(value)` replaces missing `NaN` values with the specified replacement."
            )
        ),
        Lesson(
            id="m8-l4",
            title="Split-Apply-Combine with groupby()",
            subtitle="Aggregating metrics across categories, sums, means, and counts.",
            reading_time_min=6,
            concept_markdown="""### The Split-Apply-Combine Strategy

Business intelligence queries frequently aggregate data by dimensions (e.g. total revenue by product category, average test score by university department):

1. **Split**: Break DataFrame into groups based on key columns.
2. **Apply**: Compute an aggregation function (`sum()`, `mean()`, `count()`, `min()`, `max()`) on each group.
3. **Combine**: Assemble results into a structured summary DataFrame.

```python
# Group by Category and compute multiple aggregations
summary = df.groupby("Category")["Revenue"].agg(["sum", "mean", "count"])
```
""",
            syntax_example="""# Grouping by multiple columns
regional_sales = df.groupby(["Region", "Category"])["Amount"].sum().reset_index()
print(regional_sales)
""",
            executable_code="""# Executable groupby demonstration
import pandas as pd

sales_data = {
    "Category": ["Electronics", "Electronics", "Furniture", "Electronics", "Furniture"],
    "Product": ["Laptop", "Mouse", "Desk", "Monitor", "Chair"],
    "Revenue": [1200, 25, 350, 300, 150]
}
df = pd.DataFrame(sales_data)

summary = df.groupby("Category")["Revenue"].agg(
    Total_Revenue="sum",
    Average_Revenue="mean",
    Item_Count="count"
).reset_index()

print("Groupby Summary Table:")
print(summary)
""",
            expected_output="""Groupby Summary Table:
      Category  Total_Revenue  Average_Revenue  Item_Count
0  Electronics           1525       508.333333           3
1    Furniture            500       250.000000           2""",
            output_explanation="df.groupby('Category') splits records by Category, computing sum, mean, and count for each group.",
            common_mistakes=[
                CommonMistake(
                    mistake="Forgetting `.reset_index()` after groupby()",
                    explanation="Groupby makes the grouping column the DataFrame index, which can make subsequent filtering or plotting less intuitive.",
                    correction="Append `.reset_index()` to convert grouping keys back into standard columns."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What method splits a DataFrame into subsets based on category keys for aggregation?",
                options=["df.split()", "df.groupby()", "df.partition()", "df.aggregate_by()"],
                correct_index=1,
                explanation="`df.groupby()` implements the split-apply-combine workflow."
            )
        ),
        Lesson(
            id="m8-l5",
            title="Matplotlib: Charts & Data Visualization",
            subtitle="Creating publication-grade bar charts, line plots, and exportable figures.",
            reading_time_min=7,
            concept_markdown="""### The Matplotlib Architecture

**Matplotlib** is the foundational plotting library in Python.

#### Core Concepts:
- **`Figure`**: The overall canvas or page holding all plot elements.
- **`Axes`**: An individual coordinate space with x and y axes where plots (bars, lines, scatters) are drawn.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(["Module 1", "Module 2", "Module 3"], [85, 92, 88], color="#23342B")
ax.set_title("Module Assessment Averages")
ax.set_ylabel("Average Score (%)")
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
# fig.savefig("chart.png", dpi=150)
```

#### Common Chart Types:
- `ax.plot()`: Continuous trends and time-series line charts.
- `ax.bar()`: Categorical discrete comparisons.
- `ax.pie()`: Proportion of a whole.
- `ax.scatter()`: Correlation and relationships between two continuous variables.
""",
            syntax_example="""# Formatting and styling plots
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [10, 20, 25], marker='o', color='#23342B')
""",
            executable_code="""# Executable Matplotlib plot generation and base64 inspection
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

categories = ["Fundamentals", "Control Flow", "Structures", "Exceptions", "OOP"]
scores = [92.5, 88.0, 94.2, 86.8, 91.0]

fig, ax = plt.subplots(figsize=(7, 3.5))
bars = ax.bar(categories, scores, color="#23342B", edgecolor="#161616", width=0.55)
ax.set_title("Course 01AP0303 - Module Performance Summary", fontsize=11, fontweight="bold", pad=12)
ax.set_ylabel("Score (%)", fontsize=10)
ax.set_ylim(0, 105)
ax.grid(axis="y", linestyle="--", alpha=0.4)

# Render to memory buffer
buf = io.BytesIO()
plt.tight_layout()
fig.savefig(buf, format="png", dpi=100)
plt.close(fig)

img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
print(f"Chart successfully rendered into PNG buffer ({len(img_b64)} bytes base64)")
print("Image header preview:", img_b64[:32] + "...")
""",
            expected_output="""Chart successfully rendered into PNG buffer ([Size] bytes base64)
Image header preview: iVBORw0KGgoAAAANSUhEUgAAArwAAAF...""",
            output_explanation="Using matplotlib.use('Agg') allows charts to render into memory buffers headlessly without requiring a desktop window manager.",
            common_mistakes=[
                CommonMistake(
                    mistake="Forgetting to call `plt.close(fig)` after saving figures in web loops",
                    explanation="Unclosed figures stay in memory, causing cumulative memory leaks that degrade server stability.",
                    correction="Always call `plt.close(fig)` after generating or saving plots."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="Why is `matplotlib.use('Agg')` recommended when running data analysis in web applications?",
                options=[
                    "It makes lines thicker",
                    "It enables headless raster rendering without needing a graphical display window",
                    "It automatically shares charts to social media",
                    "It translates charts into HTML5"
                ],
                correct_index=1,
                explanation="The 'Agg' backend renders charts directly into raster image memory headlessly without requiring a desktop GUI window."
            )
        )
    ],
    practice_exercises=[
        PracticeExercise(
            id="m8-ex1",
            title="Vectorized Revenue Calculation",
            difficulty="Beginner",
            problem_statement="Given two NumPy arrays `units = np.array([10, 25, 40])` and `prices = np.array([15.0, 20.0, 12.5])`, compute the total revenue array using vectorization and calculate total revenue sum.",
            input_output_expectations="Total revenue must print: Total: $1150.00",
            starter_code="""import numpy as np

units = np.array([10, 25, 40])
prices = np.array([15.0, 20.0, 12.5])

# Vectorized multiplication
revenue_per_item = units * prices
total_revenue = np.sum(revenue_per_item)

print(f"Total: ${total_revenue:.2f}")
""",
            hints=[
                "Use units * prices for element-wise multiplication",
                "np.sum(revenue_per_item) computes the sum"
            ],
            test_cases=[
                {"input": "", "expected_output": "Total: $1150.00", "description": "10*15 + 25*20 + 40*12.5 = 150 + 500 + 500 = 1150"}
            ],
            expected_substrings=["np.array", "units * prices"],
            solution="""import numpy as np
units = np.array([10, 25, 40])
prices = np.array([15.0, 20.0, 12.5])
total_revenue = np.sum(units * prices)
print(f"Total: ${total_revenue:.2f}")
"""
        ),
        PracticeExercise(
            id="m8-ex2",
            title="Pandas Category Aggregation",
            difficulty="Intermediate",
            problem_statement="Create a DataFrame with columns 'Dept' and 'Salary'. Compute and print the average salary for each department using groupby.",
            input_output_expectations="Output must show CSE average: 60000.0 and IT average: 50000.0",
            starter_code="""import pandas as pd

data = {
    "Dept": ["CSE", "CSE", "IT", "IT"],
    "Salary": [55000, 65000, 48000, 52000]
}
df = pd.DataFrame(data)

avg_salaries = df.groupby("Dept")["Salary"].mean()
print("Average Salaries:")
print(avg_salaries)
""",
            hints=[
                "df.groupby('Dept')['Salary'].mean()"
            ],
            test_cases=[
                {"input": "", "expected_output": "CSE    60000.0", "description": "Verify CSE mean salary"},
                {"input": "", "expected_output": "IT     50000.0", "description": "Verify IT mean salary"}
            ],
            expected_substrings=["groupby", "mean"],
            solution="""import pandas as pd
data = {"Dept": ["CSE", "CSE", "IT", "IT"], "Salary": [55000, 65000, 48000, 52000]}
df = pd.DataFrame(data)
avg_salaries = df.groupby("Dept")["Salary"].mean()
print("Average Salaries:")
print(avg_salaries)
"""
        )
    ],
    quiz_questions=[
        QuizQuestion(
            id="m8-q1",
            question="What is the primary benefit of vectorized operations in NumPy?",
            options=[
                "They require fewer lines of comments",
                "They execute in compiled C code at hardware speeds without Python loop overhead",
                "They run inside web browsers",
                "They save memory on disk"
            ],
            correct_index=1,
            explanation="Vectorization pushes iteration down into compiled C loops, avoiding Python bytecode interpretation overhead."
        ),
        QuizQuestion(
            id="m8-q2",
            question="Which method checks for missing or NaN values across DataFrame columns?",
            options=[
                "df.is_missing()",
                "df.isna() or df.isnull()",
                "df.empty()",
                "df.has_null()"
            ],
            correct_index=1,
            explanation="`df.isna()` or `df.isnull()` returns a boolean mask indicating missing values."
        ),
        QuizQuestion(
            id="m8-q3",
            question="What Matplotlib function saves a rendered plot directly to an image file or byte stream?",
            options=[
                "plt.render()",
                "plt.savefig() or fig.savefig()",
                "plt.export()",
                "plt.write_image()"
            ],
            correct_index=1,
            explanation="`fig.savefig()` saves figures to disk files or in-memory byte buffers."
        ),
        QuizQuestion(
            id="m8-q4",
            question="In Pandas, what operator is required for combining multiple boolean conditions: `(df['A'] > 5) ... (df['B'] < 10)`?",
            options=[
                "and",
                "&",
                "&&",
                "plus"
            ],
            correct_index=1,
            explanation="Pandas requires bitwise `&` (and) and `|` (or) for element-wise Series comparisons."
        ),
        QuizQuestion(
            id="m8-q5",
            question="What does `df.shape` return for a DataFrame with 100 rows and 5 columns?",
            options=[
                "500",
                "(100, 5)",
                "[rows: 100, cols: 5]",
                "'100x5'"
            ],
            correct_index=1,
            explanation="`df.shape` returns a tuple representing dimensionality: `(row_count, column_count)`."
        )
    ]
)

"""
Pip Learn 2.0 - Lesson Reading Sections Helper
Provides single canonical extraction of reading sections for lessons.
"""
from typing import List, Tuple


def get_lesson_reading_sections(module, lesson) -> List[Tuple[str, str, str]]:
    """
    Organize curriculum depth into five pedagogical sections:
    1. Prerequisites & Objectives
    2. Understand the Concept
    3. See It in Python (Syntax & Output)
    4. Common Pitfalls & CPython Architecture
    5. Recap & Key Takeaways
    """
    if not lesson:
        return []

    # Curriculum 2026.1 supplies authored, topic-specific pages.
    if hasattr(lesson, "content_sections") and lesson.content_sections:
        return [(section.title, section.eyebrow, section.markdown) for section in lesson.content_sections]

    # Legacy fallback
    module_id = getattr(module, "id", 1) if module else 1
    module_code = getattr(module, "code", "MOD-01") if module else "MOD-01"
    syllabus_unit = getattr(module, "syllabus_unit", "Unit 1") if module else "Unit 1"

    s1_title = "Prerequisites & Objectives"
    s1_eyebrow = f"MODULE {module_id} · {module_code} · SYLLABUS UNIT {str(syllabus_unit).upper()}"
    s1_body = f"""## Before You Begin: {lesson.title}

**What you will master:** {lesson.subtitle}

### Required Prerequisites
To get the most from this lesson, you should be comfortable with:
- Running Python code and observing the standard output (`stdout`).
- Basic terminal or editor interactions.
- Predicting what happens before a statement executes.

### Why This Concept Matters in Python
In real software engineering, this concept appears constantly. Every production Python program relies on a strong understanding of how CPython processes instructions, binds references in memory, and handles data structures.
"""

    s2_title = "Understand the Concept"
    s2_eyebrow = "CORE MENTAL MODEL & FOUNDATION"
    s2_body = f"""## Understand the Concept

{getattr(lesson, 'concept_markdown', '').strip()}
"""

    s3_title = "Syntax Blueprint & Output"
    s3_eyebrow = "CPYTHON SYNTAX & EXECUTION TRACE"
    s3_body = f"""## See It in Python

Study the verified syntax example below:

```python
{getattr(lesson, 'syntax_example', '').strip()}
```

### Expected Standard Output

```text
{getattr(lesson, 'expected_output', '').strip()}
```

### Step-by-Step Execution Mechanics

{getattr(lesson, 'output_explanation', '').strip()}
"""

    s4_title = "Pitfalls & CPython Architecture"
    s4_eyebrow = "DIAGNOSTICS & DEEPER ENGINEERING"
    mistakes = getattr(lesson, "common_mistakes", []) or []
    if mistakes:
        mistakes_md = "\n\n".join(
            f"### Common Mistake: Problem Pattern\n\n```python\n# Risky or incorrect code:\n{m.mistake}\n```\n\n**Why it fails:** {m.explanation}\n\n**The Correction:**\n```python\n{m.correction}\n```"
            for m in mistakes
        )
    else:
        mistakes_md = "### Common Mistake: Mechanical Copying\n\nAvoid typing code without understanding. Test edge cases, change values, and verify how CPython responds."

    s4_body = f"""## Common Pitfalls & Architectural Depth

{mistakes_md}
"""

    s5_title = "Summary & Takeaways"
    s5_eyebrow = "RECAP & INTELLECTUAL MILESTONES"
    takeaways = getattr(lesson, "takeaways", []) or []
    if takeaways:
        items_md = "\n".join(f"- **Key Point:** {t}" for t in takeaways)
    else:
        items_md = "- **Verified Foundation:** Concept internalised through systematic trace."

    s5_body = f"""## Recap & Key Takeaways

Review the core conclusions of this lesson:

{items_md}
"""

    return [
        (s1_title, s1_eyebrow, s1_body),
        (s2_title, s2_eyebrow, s2_body),
        (s3_title, s3_eyebrow, s3_body),
        (s4_title, s4_eyebrow, s4_body),
        (s5_title, s5_eyebrow, s5_body),
    ]

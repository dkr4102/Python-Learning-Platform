"""
Unit tests for curriculum loading and validation.
Verifies all 8 modules, lessons, exercises, quizzes, and project schemas.
"""
import pytest
from app.curriculum.loader import get_all_modules, get_module, get_lesson, get_practice_exercise, get_total_lessons_count

def test_all_eight_modules_exist():
    modules = get_all_modules()
    assert len(modules) == 8
    expected_titles = [
        "Python Fundamentals",
        "Control Flow and Functions",
        "Data Structures",
        "File Handling and Exception Handling",
        "Object-Oriented Programming",
        "Database Connectivity",
        "API Integration, Automation & Reporting",
        "Data Analytics & Visualization"
    ]
    for idx, expected in enumerate(expected_titles, 1):
        m = get_module(idx)
        assert m is not None
        assert m.title == expected
        assert m.id == idx
        assert m.code == f"MOD-0{idx}"
        assert len(m.lessons) >= 4
        assert len(m.practice_exercises) >= 2
        assert len(m.quiz_questions) >= 5
        assert m.project is not None

def test_lesson_retrieval_and_content_quality():
    m1_l1 = get_lesson(1, "py-v2-u1-l01")
    assert m1_l1 is not None
    assert m1_l1.title == "Welcome to Programming and Python"
    assert "Programming means" in m1_l1.concept_markdown
    assert "CPython" not in m1_l1.concept_markdown
    assert m1_l1.syntax_example != ""
    assert m1_l1.executable_code != ""
    assert m1_l1.expected_output != ""
    assert len(m1_l1.common_mistakes) > 0
    assert m1_l1.mini_checkpoint is not None
    assert len(m1_l1.content_sections) == 5
    assert len(m1_l1.practice_tasks) == 3
    assert m1_l1.experiment is not None

def test_practice_exercise_structure():
    ex = get_practice_exercise(1, "py-v2-u1-l01-practice-1")
    assert ex is not None
    assert "print" in ex.starter_code
    assert len(ex.test_cases) > 0
    assert ex.solution != ""

def test_total_lessons_count():
    total = get_total_lessons_count()
    assert total == 50

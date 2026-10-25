from app.curriculum.loader import get_all_modules
from app.curriculum.validate import TOPIC_MAP, validate


def test_beginner_first_opening_sequence():
    titles = [lesson.title for lesson in get_all_modules()[0].lessons]
    assert titles == [
        "Welcome to Programming and Python",
        "Install Python and Set Up Your Environment",
        "Your First Program: Hello, World!",
        "Understanding print(), Strings and Output",
        "Variables and Assignment",
        "Numbers and Basic Arithmetic",
        "Data Types and Type Conversion",
        "User Input and Interactive Programs",
        "Operators and Expressions",
        "Formatting Output and Building Small Programs",
    ]


def test_every_lesson_has_complete_learning_journey():
    for module in get_all_modules():
        for lesson in module.lessons:
            assert lesson.id.startswith("py-v2-")
            assert len(lesson.content_sections) >= 5
            assert lesson.experiment is not None
            assert [task.difficulty for task in lesson.practice_tasks] == ["Introductory", "Guided", "Independent"]
            assert len(lesson.checkpoint_questions) >= 2
            assert lesson.completion_criteria


def test_all_syllabus_topics_and_examples_validate():
    assert sum(len(topics) for topics in TOPIC_MAP.values()) == 148
    report = validate()
    assert report["errors"] == []
    assert report["runnable_examples"]["passed"] == 50
    assert report["projects"] == 10


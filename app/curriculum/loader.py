"""
Curriculum loader and registry.
Provides centralized access to all 8 syllabus modules, lessons, exercises, quizzes, and projects.
"""
from typing import Dict, List, Optional
from app.curriculum.models import Module, Lesson, PracticeExercise, QuizQuestion, ProjectInfo
from app.curriculum.catalog_v2 import CURRICULUM_REGISTRY, CURRICULUM_VERSION

_CURRICULUM_REGISTRY: Dict[int, Module] = CURRICULUM_REGISTRY

def get_all_modules() -> List[Module]:
    """Return all 8 modules in syllabus order."""
    return [_CURRICULUM_REGISTRY[i] for i in range(1, 9)]

def get_module(module_id: int) -> Optional[Module]:
    """Retrieve module by ID (1-8)."""
    return _CURRICULUM_REGISTRY.get(module_id)

def get_lesson(module_id: int, lesson_id: str) -> Optional[Lesson]:
    """Retrieve a specific lesson inside a module."""
    module = get_module(module_id)
    if not module:
        return None
    for lesson in module.lessons:
        if lesson.id == lesson_id:
            return lesson
    # Historical URLs remain navigable but resolve to the new lesson object;
    # persistence always uses lesson.id (the 2026.1 stable identifier), never
    # the legacy route token.
    if lesson_id.startswith(f"m{module_id}-l"):
        try:
            legacy_position = int(lesson_id.rsplit("l", 1)[1])
            if 1 <= legacy_position <= len(module.lessons):
                return module.lessons[legacy_position - 1]
        except ValueError:
            pass
    return None

def get_practice_exercise(module_id: int, exercise_id: str) -> Optional[PracticeExercise]:
    """Retrieve an exercise inside a module."""
    module = get_module(module_id)
    if not module:
        return None
    for ex in module.practice_exercises:
        if ex.id == exercise_id:
            return ex
    return None

def get_total_lessons_count() -> int:
    """Return total number of lessons across all 8 modules."""
    return sum(len(m.lessons) for m in _CURRICULUM_REGISTRY.values())

"""
Pydantic schemas for structured curriculum content.
Ensures typing, validation and data integrity across all 8 modules.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class CommonMistake(BaseModel):
    mistake: str
    explanation: str
    correction: str

class MiniCheckpoint(BaseModel):
    question: str
    options: List[str]
    correct_index: int
    explanation: str

class ContentSection(BaseModel):
    """One digestible page in the paginated Read stage."""
    id: str
    title: str
    eyebrow: str
    markdown: str

class Experiment(BaseModel):
    id: str
    title: str
    prediction_prompt: str
    instructions: List[str]
    starter_code: str
    expected_output: str
    observation_prompt: str
    modification_prompt: str
    execution_mode: str = "python"  # python, guided, or external-safe

class Lesson(BaseModel):
    id: str
    title: str
    subtitle: str
    reading_time_min: int = 5
    concept_markdown: str
    syntax_example: str
    executable_code: str
    expected_output: str
    output_explanation: str
    common_mistakes: List[CommonMistake] = Field(default_factory=list)
    mini_checkpoint: Optional[MiniCheckpoint] = None
    module_id: Optional[int] = None
    position: Optional[int] = None
    description: str = ""
    prerequisites: List[str] = Field(default_factory=list)
    learning_objectives: List[str] = Field(default_factory=list)
    content_sections: List[ContentSection] = Field(default_factory=list)
    experiment: Optional[Experiment] = None
    practice_tasks: List["PracticeExercise"] = Field(default_factory=list)
    checkpoint_questions: List[MiniCheckpoint] = Field(default_factory=list)
    completion_criteria: List[str] = Field(default_factory=list)
    optional_deeper_learning: str = ""

class PracticeExercise(BaseModel):
    id: str
    title: str
    difficulty: str = "Beginner"
    problem_statement: str
    input_output_expectations: str
    starter_code: str
    hints: List[str] = Field(default_factory=list)
    test_cases: List[Dict[str, Any]] = Field(default_factory=list)
    expected_substrings: List[str] = Field(default_factory=list)
    solution: str

class QuizQuestion(BaseModel):
    id: str
    question: str
    options: List[str]
    correct_index: int
    explanation: str

class ProjectInfo(BaseModel):
    id: str
    title: str
    subtitle: str
    objective: str
    requirements: List[str]
    starter_snippet: str
    module_id: int
    prerequisites: List[str] = Field(default_factory=list)
    milestones: List[str] = Field(default_factory=list)
    testing_criteria: List[str] = Field(default_factory=list)
    expected_behavior: str = ""
    error_handling: List[str] = Field(default_factory=list)
    evidence: str = ""

class Module(BaseModel):
    id: int
    code: str
    title: str
    syllabus_unit: str
    contact_hours: int = 6
    assessment_marks: int = 10  # 10 marks for mod 1, 12 marks for mod 2-7
    description: str
    learning_objectives: List[str]
    topics_covered: List[str]
    artwork_id: str
    project: ProjectInfo
    lessons: List[Lesson]
    practice_exercises: List[PracticeExercise]
    quiz_questions: List[QuizQuestion]
    projects: List[ProjectInfo] = Field(default_factory=list)
    curriculum_version: str = "2026.1"

# PracticeExercise is declared after Lesson to preserve the public model order
# used by the existing modules. Resolve the forward reference once all schemas
# are available (Pydantic v1 and v2 compatible).
if hasattr(Lesson, "model_rebuild"):
    Lesson.model_rebuild()
else:  # pragma: no cover - Pydantic v1 compatibility
    Lesson.update_forward_refs(PracticeExercise=PracticeExercise)

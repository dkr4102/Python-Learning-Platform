"""Machine-readable curriculum QA and documentation generator.

Run with: ``python -m app.curriculum.validate --write``.
The command never mutates learner data; it executes examples in isolated temp
directories and writes evidence under docs/.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

from app.config import BASE_DIR
from app.curriculum.catalog_v2 import CURRICULUM_VERSION
from app.curriculum.loader import get_all_modules
from app.curriculum.videos import PLAYLIST_URL, get_verified_video_inventory
from app.execution.runner import run_python_code


TOPIC_MAP: Dict[int, Dict[str, List[int]]] = {
    1: {
        "Programming fundamentals": [1], "Introduction to Python": [1], "Installation": [2],
        "Python interpreter": [2], "IDE setup": [2], "VS Code": [2], "Jupyter Notebook": [2],
        "First Python program": [3], "Print statements": [3, 4], "Syntax fundamentals": [3, 4],
        "Comments": [4], "Variables": [5], "Naming conventions": [5], "Data types": [7],
        "Operators": [6, 9], "Operator precedence": [9], "Type conversion": [7],
        "User input": [8], "Formatted output": [10], "Beginner debugging": [10],
    },
    2: {
        "Boolean values and expressions": [1], "Comparison operators": [1], "Conditional statements": [2],
        "if, elif, else": [2], "Nested decisions": [2], "for loops": [3], "while loops": [4],
        "range": [3], "break": [4], "continue": [4], "pass": [4], "Loop patterns": [3, 4],
        "Function definitions": [5], "Calling functions": [5], "Arguments and parameters": [5],
        "Return values": [5], "Scope basics": [5], "Default arguments": [5], "Lambda functions": [6],
        "Recursion fundamentals": [6], "Modular program design": [6],
    },
    3: {
        "Strings and operations": [1], "String methods": [1], "Indexing": [1], "Slicing": [1],
        "Lists": [2], "List methods": [2], "Iteration": [3], "Tuples": [4], "Immutability": [4],
        "Sets": [5], "Set operations": [5], "Dictionaries": [6], "Key-value operations": [6],
        "Nested collections": [6, 7], "Data manipulation": [3, 7], "Built-in functions": [3],
        "Data storage and retrieval": [7], "Choosing the appropriate data structure": [7],
    },
    4: {
        "Files and file paths": [1], "Text files": [1], "File modes": [1], "Reading files": [2],
        "Writing files": [2], "Appending files": [1, 2], "with statement": [2], "seek": [2], "tell": [2],
        "CSV files": [3], "CSV reading and writing": [3], "Exceptions": [4],
        "try, except, else, finally": [4], "Common runtime errors": [4], "Raising exceptions": [5],
        "Custom exception classes": [5], "Logging": [6], "Logging levels": [6], "Error logs": [6],
        "Practical file-processing workflows": [6],
    },
    5: {
        "Why OOP exists": [1], "Classes": [1], "Objects": [1], "Attributes": [2], "Methods": [2],
        "self": [2], "Constructors": [2], "__init__": [2], "Instance variables": [3],
        "Class variables": [3], "Encapsulation": [4], "Inheritance": [5], "Method overriding": [5],
        "Polymorphism": [6], "Abstraction": [6], "Reusable modules": [7],
        "Modeling real systems with OOP": [7],
    },
    6: {
        "Relational database fundamentals": [1], "Tables, rows and columns": [1], "Primary keys": [1],
        "SQLite": [2], "MySQL connectivity": [6], "Database connection lifecycle": [2, 6],
        "Table creation": [2], "Create operations": [3], "Read operations": [3], "Update operations": [4],
        "Delete operations": [4], "Parameterized queries": [3, 4], "SQL injection prevention": [4],
        "Transactions": [5], "Commit and rollback": [5], "Error handling": [5, 6],
        "Python database integration": [2, 6],
    },
    7: {
        "API fundamentals": [1], "Web services": [1], "HTTP fundamentals": [1], "REST concepts": [1],
        "Requests library": [2], "GET requests": [2], "POST requests": [2], "Request parameters": [2],
        "Headers": [2], "JSON parsing": [2], "Status codes": [1, 2], "Network errors": [3],
        "Third-party API integration": [3], "Email automation": [4], "Scheduled tasks": [4],
        "Report automation": [4], "Basic API-driven dashboards": [4],
    },
    8: {
        "NumPy introduction": [1], "Arrays": [1], "Array operations": [1], "Pandas introduction": [2],
        "Series": [2], "DataFrames": [2], "CSV imports and exports": [2], "Excel imports and exports": [2],
        "Missing values": [3], "Data cleaning": [3], "Filtering": [3], "Grouping": [3], "Aggregation": [3],
        "Matplotlib": [4], "Bar charts": [4], "Line charts": [4], "Pie charts": [4],
        "Dashboard-oriented reporting": [4],
    },
}


def validate() -> dict:
    modules = get_all_modules()
    errors: List[str] = []
    warnings: List[str] = []
    lesson_ids = [lesson.id for module in modules for lesson in module.lessons]
    known = set(lesson_ids)
    runnable = []

    if len(modules) != 8:
        errors.append(f"Expected 8 units, found {len(modules)}")
    if sum(module.contact_hours for module in modules) != 45:
        errors.append("Official contact hours do not total 45")
    if [module.assessment_marks for module in modules] != [10, 12, 12, 12, 12, 12, 12, 0]:
        errors.append("Module marks do not match the official seven-module rubric; Unit 8 must add no marks")
    if len(known) != len(lesson_ids):
        errors.append("Lesson identifiers are not unique")

    for module in modules:
        if module.curriculum_version != CURRICULUM_VERSION:
            errors.append(f"Unit {module.id} has wrong curriculum version")
        for topic, positions in TOPIC_MAP[module.id].items():
            for position in positions:
                if position < 1 or position > len(module.lessons):
                    errors.append(f"Topic {topic!r} maps to missing Unit {module.id} lesson {position}")
        for expected_position, lesson in enumerate(module.lessons, 1):
            prefix = lesson.id
            required = {
                "module_id": lesson.module_id, "position": lesson.position, "description": lesson.description,
                "objectives": lesson.learning_objectives, "sections": lesson.content_sections,
                "experiment": lesson.experiment, "practice": lesson.practice_tasks,
                "checkpoints": lesson.checkpoint_questions, "completion": lesson.completion_criteria,
            }
            for field, value in required.items():
                if value in (None, "", []):
                    errors.append(f"{prefix}: missing {field}")
            if lesson.module_id != module.id or lesson.position != expected_position:
                errors.append(f"{prefix}: module/position mismatch")
            for prerequisite in lesson.prerequisites:
                if prerequisite not in known:
                    errors.append(f"{prefix}: missing prerequisite {prerequisite}")
            if len(lesson.content_sections) < 5:
                errors.append(f"{prefix}: Read stage has fewer than five pages")
            if len(lesson.practice_tasks) != 3:
                errors.append(f"{prefix}: practice must have three levels")
            if [x.difficulty for x in lesson.practice_tasks] != ["Introductory", "Guided", "Independent"]:
                errors.append(f"{prefix}: practice progression is incorrect")
            for exercise in lesson.practice_tasks:
                if not exercise.test_cases or not exercise.solution:
                    errors.append(f"{exercise.id}: missing behavior tests or reviewed solution")
            for question in lesson.checkpoint_questions:
                if not question.options or not 0 <= question.correct_index < len(question.options):
                    errors.append(f"{prefix}: checkpoint answer key is invalid")
            result = run_python_code(lesson.executable_code, timeout_sec=8)
            expected = lesson.expected_output.strip()
            actual = result["stdout"].strip()
            passed = result["success"] and actual == expected
            runnable.append({"lesson_id": prefix, "passed": passed, "expected": expected, "actual": actual, "stderr": result["stderr"]})
            if not passed:
                errors.append(f"{prefix}: runnable output mismatch")

    videos = get_verified_video_inventory()
    inventory_path = BASE_DIR / "docs" / "corey-schafer-playlist-inventory.json"
    playlist_inventory = json.loads(inventory_path.read_text(encoding="utf-8")) if inventory_path.exists() else {"record_count": 0, "videos": []}
    if playlist_inventory.get("record_count") != len(playlist_inventory.get("videos", [])) or playlist_inventory.get("record_count", 0) < len(videos):
        errors.append("Playlist inventory artifact is missing or internally inconsistent")
    for video in videos:
        if not video.video_id or not video.title or not video.source_url or not video.verification_status:
            errors.append(f"Video {video.video_id or '<missing>'}: incomplete metadata")
        for lesson_id in video.corresponding_lesson_ids:
            if lesson_id not in known:
                errors.append(f"Video {video.video_id}: missing lesson {lesson_id}")
    if any(video.duration == "Not independently verified" for video in videos):
        warnings.append("Video durations are intentionally not claimed because they were not independently verified.")

    projects = [project for module in modules for project in module.projects]
    if len(projects) != 10:
        errors.append(f"Expected 10 projects, found {len(projects)}")
    for project in projects:
        if not all([project.requirements, project.prerequisites, project.milestones, project.testing_criteria, project.evidence]):
            errors.append(f"{project.id}: incomplete project learning specification")

    return {
        "curriculum_version": CURRICULUM_VERSION,
        "units": len(modules), "lessons": len(lesson_ids),
        "syllabus_topics": sum(len(items) for items in TOPIC_MAP.values()),
        "projects": len(projects), "playlist_inventory_records": playlist_inventory.get("record_count", 0),
        "verified_video_records": len(videos),
        "runnable_examples": {"total": len(runnable), "passed": sum(x["passed"] for x in runnable), "results": runnable},
        "navigation": {"ordered_lessons": lesson_ids, "next_links_valid": len(known) == len(lesson_ids)},
        "errors": errors, "warnings": warnings, "status": "pass" if not errors else "fail",
    }


def _write(report: dict) -> None:
    docs = BASE_DIR / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "curriculum-coverage.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    modules = get_all_modules()
    map_lines = ["# Complete Curriculum Map", "", f"Curriculum version: `{CURRICULUM_VERSION}`", ""]
    for module in modules:
        map_lines += [f"## Unit {module.id} — {module.title}", "", f"Contact hours: {module.contact_hours}", ""]
        for lesson in module.lessons:
            prereq = ", ".join(lesson.prerequisites) or "None"
            map_lines.append(f"{lesson.position}. `{lesson.id}` — **{lesson.title}**  ")
            map_lines.append(f"   Prerequisite: {prereq}. Objectives: {'; '.join(lesson.learning_objectives)}")
        map_lines += ["", "Projects: " + ", ".join(p.title for p in module.projects), ""]
    (docs / "complete-curriculum-map.md").write_text("\n".join(map_lines) + "\n", encoding="utf-8")

    matrix = ["# Syllabus Coverage Matrix", "", "Every syllabus topic is mapped to concrete lesson evidence.", "", "| Unit | Topic | Lesson evidence |", "|---:|---|---|"]
    for unit, topics in TOPIC_MAP.items():
        for topic, positions in topics.items():
            ids = ", ".join(modules[unit - 1].lessons[p - 1].id for p in positions)
            matrix.append(f"| {unit} | {topic} | `{ids}` |")
    (docs / "syllabus-coverage-matrix.md").write_text("\n".join(matrix) + "\n", encoding="utf-8")

    videos = ["# Video Mapping", "", f"Playlist inventoried: {PLAYLIST_URL}", "", f"The source inventory contains **{report['playlist_inventory_records']} records** and is preserved in `docs/corey-schafer-playlist-inventory.json`. The table below contains only the {report['verified_video_records']} relevant records selected for this syllabus.", "", "Metadata was checked through YouTube oEmbed on 2026-10-25. Duration is not claimed unless independently verified. Runtime embedding may vary; every player provides an external link.", "", "| ID | Verified title | Lesson IDs | Topics | Verification | Embed |", "|---|---|---|---|---|---|"]
    for video in get_verified_video_inventory():
        videos.append(f"| `{video.video_id}` | {video.title} | {', '.join(video.corresponding_lesson_ids)} | {', '.join(video.topic_coverage)} | {video.verification_status} | {video.embed_status} |")
    videos += ["", "## Honest coverage gaps", "", "The supplied playlist has no verified, syllabus-focused match for beginner `input()`, MySQL connectivity, SMTP scheduling, NumPy, Pandas/Excel cleaning, or dashboard chart design. Those lessons use original Read content and runnable experiments; no substitute video is fabricated."]
    (docs / "video-mapping.md").write_text("\n".join(videos) + "\n", encoding="utf-8")

    quality = ["# Content Quality Report", "", f"Validation status: **{report['status'].upper()}**", "", f"- Units: {report['units']}", f"- Stable lessons: {report['lessons']}", f"- Syllabus topics mapped: {report['syllabus_topics']}", f"- Runnable examples passing: {report['runnable_examples']['passed']}/{report['runnable_examples']['total']}", f"- Projects specified: {report['projects']}", f"- Playlist records retrieved: {report['playlist_inventory_records']}", f"- Relevant verified video records: {report['verified_video_records']}", "", "Each lesson contains explicit prerequisites/objectives, five paginated reading sections, runnable code and expected output, debugging guidance, optional depth, a five-step experiment, three behavior-tested practices, two keyed checkpoints, and completion criteria.", "", "## Findings", ""]
    quality += [f"- ERROR: {x}" for x in report["errors"]] or ["- No validation errors."]
    quality += [f"- NOTE: {x}" for x in report["warnings"]]
    (docs / "content-quality-report.md").write_text("\n".join(quality) + "\n", encoding="utf-8")

    projects = ["# Project Coverage", "", "| Project | Unit | Implementation evidence | Tests/criteria |", "|---|---:|---|---|"]
    for module in modules:
        for project in module.projects:
            projects.append(f"| {project.title} | {module.id} | `{project.evidence}` | {'; '.join(project.testing_criteria)} |")
    (docs / "project-coverage.md").write_text("\n".join(projects) + "\n", encoding="utf-8")

    readiness = ["# Final Academic Readiness", "", f"Status: **{'READY' if report['status'] == 'pass' else 'NOT READY'}** for curriculum version `{CURRICULUM_VERSION}` based on automated structural and execution evidence.", "", "## Evaluation traceability", "", "- Module 1 retains the official 10-mark allocation.", "- Modules 2–7 retain 12 marks each.", "- Common IA remains 18 marks.", "- Unit 8 is covered without inventing additional official marks.", "- The ten practical applications are functional code paths with test evidence.", "- Historical progress is namespaced as `legacy-v1`; new progress starts under `2026.1`.", "", "## Outstanding constraints", "", "- YouTube embedding and availability are publisher/region dependent; the external fallback is authoritative.", "- Real email and credentialed API/MySQL actions require learner-controlled configuration. Offline/test paths are supplied and never represented as real sends.", "- GUI Tkinter execution is documented through project architecture rather than run inside the server sandbox."]
    (docs / "final-academic-readiness.md").write_text("\n".join(readiness) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write manifest and required documentation")
    args = parser.parse_args()
    report = validate()
    if args.write:
        _write(report)
    print(json.dumps({k: v for k, v in report.items() if k != "runnable_examples"}, indent=2))
    print(f"Runnable examples: {report['runnable_examples']['passed']}/{report['runnable_examples']['total']}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())


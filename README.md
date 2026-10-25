<div align="center">

# π Pip Learn

### Python, one concept at a time.

**A calm, beginner-first Python learning studio.**

[![Python](https://img.shields.io/badge/Python-Learning%20%26%20Execution-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![NiceGUI](https://img.shields.io/badge/UI-NiceGUI-5B84B1?style=for-the-badge)](https://nicegui.io/)
[![SQLite](https://img.shields.io/badge/Data-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)
[![Status](https://img.shields.io/badge/Source-Pending%20Local%20Upload-777777?style=for-the-badge)](#repository-status)

**Marwadi University · Programming with Python · 01AP0303**

*Read → Watch → Experiment → Practice → Check*

</div>

---

## The idea

Learning Python should feel like understanding a new language—not memorizing disconnected snippets or clicking through slides.

**Pip Learn** is an educational application designed around one small concept at a time. Students read an approachable explanation, watch a matching tutorial when available, predict and run real code, solve increasingly independent exercises, and verify understanding before moving forward.

The design takes inspiration from an editorial reading experience: spacious typography, calm colors, and a deliberate focus on the learning task.

> **Learn the idea. Predict what happens. Run the code. Explain why.**

## The learning journey

| Stage | What the learner does | Why it matters |
| --- | --- | --- |
| **01 · Read** | Work through prerequisites, examples, syntax, and mental models. | Build understanding before imitation. |
| **02 · Watch** | Watch a relevant, short video and take notes. | See the idea demonstrated. |
| **03 · Experiment** | Predict output, edit Python, execute it, and compare results. | Connect theory with observable behavior. |
| **04 · Practice** | Complete guided and independent tasks with test feedback. | Develop the ability to write code without copying. |
| **05 · Check** | Answer conceptual questions and review mistakes. | Demonstrate readiness for the next lesson. |

Progress is intended to continue from the student's **last saved learning location**, not a hard-coded default stage. The application also includes curriculum navigation and a study-space dashboard.

## Built with Python, to teach Python

Pip Learn has an especially fitting architecture: **Python is both the subject being taught and a central implementation language of the product.** The development history identifies the following components; exact code paths and versions will be documented against the source when the full local project is uploaded.

### 1. Python powers the application

The application uses **NiceGUI**, a Python UI framework, to define screens, navigation, and user interactions. Rather than using Python only for exercises, the product uses it to build the learning experience itself.

The development history references `app/main.py` as an application entry point and NiceGUI screen components for the homepage, dashboard, module views, and settings.

### 2. Python connects lessons with persistent learning data

The application uses **SQLite** for structured persistence. The local development history references `data/pip_learn.db`, `models.py`, and `crud.py` and includes tables named:

- `module_progress`
- `lesson_completions`
- `quiz_attempts`
- `practice_attempts`
- `project_submissions`
- `achievements`
- `lesson_activities`

These records support the intended learning experience: remember where a student stopped, track attempts, and distinguish completed lessons from in-progress work. The persisted state—not the button the student happened to click—should determine the next unfinished step.

### 3. Python supports the code laboratory

The learning workspace presents editable Python examples and a terminal-style output panel. Development screenshots and logs describe an isolated subprocess execution approach for running learners' code.

**Important security note:** executing untrusted Python requires real containment, explicit resource limits, and production-grade isolation. A subprocess by itself is **not** a secure sandbox. Deployment should validate those safeguards before accepting untrusted code from the public.

### 4. Python handles learning logic

The platform's learning workflow ties together lesson sections, code experiments, practice results, checkpoints, and advancement. Its goal is to advance only when the relevant learning requirements are met, while making earlier steps available to revisit.

The codebase also references **Argon2 password hashing** in the authentication work. Authentication behavior and session handling should be verified against the final source before production release.

### 5. Python is used to test Python teaching

The development history includes **pytest** execution, with references to authentication/navigation tests, end-to-end lesson journey tests, and acceptance tests. These checks are important because an educational product must get both the **code result** and the **learning progression** right.

No test pass rate is claimed here without checking the final uploaded source and running its tests.

## Course scope

The course is organized into eight syllabus units:

| Unit | Topic | Applied direction |
| --- | --- | --- |
| **01** | Python Fundamentals | First programs and foundational syntax |
| **02** | Control Flow and Functions | Decisions, repetition, and reusable logic |
| **03** | Data Structures | Collections and data handling |
| **04** | File Handling and Exception Handling | Persistent files and robust programs |
| **05** | Object-Oriented Programming | Classes and domain modeling |
| **06** | Database Connectivity | Python with relational data |
| **07** | API Integration, Automation & Reporting | Working with services and automated tasks |
| **08** | Data Analytics & Visualization | Processing and communicating data |

The curriculum is designed to begin with **Hello, world!**, then grow gradually toward real applications. The syllabus describes **45 contact hours**; contact hours should not be mistaken for a verified total video duration.

## Product philosophy

**Minimal, not empty.** Every screen should make the next useful action obvious.

**Teaching, not clicking.** The written explanations, experiments, and questions must encourage actual understanding.

**One source of progress truth.** Start Learning and Continue Learning must resolve to the correct learner state.

**Real feedback.** Running code and completing a quiz should produce grounded, helpful results, not simulated success.

**Accessible media.** Video should use a familiar embedded player, with a direct YouTube fallback when embedding fails.

## Running locally

The project was developed locally using a Python virtual environment. Its development history shows a command of the form:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app/main.py
```

Once the complete application is uploaded, install from its actual dependency manifest and follow any additional environment or database initialization instructions. **The source is not yet present in this repository**, so the commands above cannot currently launch the project from a fresh clone.

## Repository status

**Documentation initialized; complete local source upload pending.**

The running application seen at `localhost:8080` exists in a separate local development environment. This GitHub repository was empty when this README was created, and no claim is made that application code, media assets, database migrations, or tests have already been pushed.

The next publication step is to transfer the complete local source, exclude secrets and generated local state, then verify the documented setup and tests.

## Before publishing

- Do not commit `.env`, access tokens, user passwords, or private student records.
- Do not commit the local virtual environment, caches, or runtime-generated databases.
- Include a dependency lockfile or pinned requirements and a safe database initialization path.
- Confirm embedded video IDs and playback behavior.
- Run the project's tests and verify that onboarding, resume logic, exercises, and quizzes all work.

---

<div align="center">

**Made for learning. Built with Python. Designed for clarity.**

*Pip Learn · Marwadi University · 2026*

</div>

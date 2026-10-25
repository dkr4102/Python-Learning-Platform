# Pip Learn — Full Codebase, Authentication & Navigation Audit

**Date:** 2026-10-25  
**Author:** Principal Software Architect & Senior NiceGUI Engineer  
**Scope:** Local Authoritative Implementation (`http://127.0.0.1:8080`)  

---

## 1. Executive Summary & Root Causes

A comprehensive audit of the local Python/NiceGUI application reveals the architectural root causes behind broken navigation and missing learner identity:

1. **Complete Absence of an Authentication & Session System:**
   - The application does not implement user registration, login, session tokens, password hashing, or authentication guards.
   - Every single screen directly invokes `get_default_learner(db)` (`app/database/crud.py:89`), which executes `db.query(Learner).first()`.
   - If a record exists (currently `id=1, name="Dr. Priya Patel"`), **every visitor in every browser tab is treated as this identical user**, reading and mutating the same learner progress, practice runs, and quiz attempts.
   - There is no server-side session identification, no signed session cookie, and no user authorization layer.

2. **Scattered, Uncoordinated Navigation & Hardcoded Routes:**
   - Navigation targets are hardcoded directly inside inline lambda callbacks across screens (e.g. `on_click=lambda: ui.navigate.to("/setup")`).
   - "Continue Learning" on the Study Space Dashboard (`s03_dashboard.py:36`) is hardcoded to `/module/1/lesson/m1-l1`, completely ignoring the learner's actual module progress, completed lessons, and active stage.
   - "Start Learning" on the Homepage (`s01_home.py:40`) routes to `/setup`, confusing first-time profile creation with account registration.
   - Header navigation displays the exact same static links regardless of whether a user is logged in or unauthenticated. There are no Login, Register, or Logout controls.

3. **Unprotected Learning Content & Leakage of Private Records:**
   - All 12 application routes (`/dashboard`, `/curriculum`, `/module/{id}`, `/module/{id}/lesson/{id}`, `/practice`, `/module/{id}/quiz`, `/projects`, `/achievements`, `/report`, `/settings`) are publicly exposed without route guards.
   - Academic dossiers and grades at `/report` can be viewed and downloaded without identity verification.
   - Anonymous visitors can execute quiz attempts and project submissions that permanently mutate the database.

---

## 2. Inventory of Actionable UI Elements & Routes

| Source Page | UI Element Name | Current Action | Current Destination | Auth Required? | Intended Destination | Correct? | Required Correction |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Header** | Monogram `π Pip Learn` | `ui.link(target="/")` | `/` | No | Public Home `/` | Yes | Keep link to `/`. |
| **Header** | Desktop Nav: Curriculum | `ui.link(..., "/curriculum")` | `/curriculum` | Yes | `/curriculum` | **No** | Guard route; redirect to `/login?redirect=/curriculum` if unauthenticated. |
| **Header** | Desktop Nav: Dashboard | `ui.link(..., "/dashboard")` | `/dashboard` | Yes | `/dashboard` | **No** | Guard route; redirect to `/login?redirect=/dashboard` if unauthenticated. |
| **Header** | Desktop Nav: Practice Lab | `ui.link(..., "/practice")` | `/practice` | Yes | `/practice` | **No** | Guard route; redirect to `/login?redirect=/practice` if unauthenticated. |
| **Header** | Desktop Nav: Projects | `ui.link(..., "/projects")` | `/projects` | Yes | `/projects` | **No** | Guard route; redirect to `/login?redirect=/projects` if unauthenticated. |
| **Header** | Desktop Nav: Achievements | `ui.link(..., "/achievements")` | `/achievements` | Yes | `/achievements` | **No** | Guard route; redirect to `/login?redirect=/achievements` if unauthenticated. |
| **Header** | Desktop Nav: Report | `ui.link(..., "/report")` | `/report` | Yes | `/report` | **No** | Guard route; redirect to `/login?redirect=/report` if unauthenticated. |
| **Header** | Setup Button | `ui.navigate.to("/setup")` | `/setup` | Yes | Onboarding (new) or Settings | **No** | Hide from unauthenticated; replace with Login/Register when logged out. |
| **Header** | Settings Gear | `ui.navigate.to("/settings")` | `/settings` | Yes | `/settings` | **No** | Guard route; hide or redirect to login. |
| **Header** | Study Space CTA | `ui.navigate.to("/dashboard")` | `/dashboard` | Yes | `/dashboard` | **No** | Show Login/Register when unauthenticated; show user dropdown & Logout when authenticated. |
| **Home (`/`)** | Start Learning CTA | `ui.navigate.to("/setup")` | `/setup` | Yes | `/login` (if unauth) or canonical resume (if auth) | **No** | Centralize: If unauthenticated -> `/register` or `/login`. If authenticated -> canonical resume. |
| **Home (`/`)** | Explore Curriculum CTA | `ui.navigate.to("/curriculum")` | `/curriculum` | Yes | `/login` (if unauth) or `/curriculum` (if auth) | **No** | Require authentication before accessing curriculum. |
| **Home (`/`)** | Open Study Space Link | `target="/dashboard"` | `/dashboard` | Yes | `/login` (if unauth) or `/dashboard` (if auth) | **No** | Route through auth check. |
| **Home (`/`)** | Syllabus Unit Cards (8) | `ui.navigate.to(f"/module/{m_id}")` | `/module/{id}` | Yes | `/module/{id}` | **No** | Require authentication before viewing module syllabus details. |
| **Home (`/`)** | Enter Study Space CTA | `ui.navigate.to("/dashboard")` | `/dashboard` | Yes | `/dashboard` | **No** | Require authentication before dashboard access. |
| **Home (`/`)** | Configure Profile CTA | `ui.navigate.to("/setup")` | `/setup` | Yes | `/settings` or `/setup` | **No** | If unauthenticated -> `/login`. If authenticated -> `/settings`. |
| **Setup (`/setup`)** | Cancel Button | `ui.navigate.to("/")` | `/` | No | `/` | Yes | Return to `/`. |
| **Setup (`/setup`)** | Save & Enter Study Space | `update_learner_profile(...)` | `/dashboard` | Yes | `/dashboard` | **No** | Currently updates hardcoded Learner ID 1. Must associate with authenticated session. |
| **Dashboard (`/dashboard`)** | Curriculum Explorer Button | `ui.navigate.to("/curriculum")` | `/curriculum` | Yes | `/curriculum` | Yes | Maintain, but ensure authenticated session is active. |
| **Dashboard (`/dashboard`)** | Continue Learning Button | `ui.navigate.to("/module/1/lesson/m1-l1")` | `/module/1/lesson/m1-l1` | Yes | Canonical Resume Position | **CRITICAL BUG** | Hardcoded to M1-L1. Must calculate deterministic resume position from learner activity. |
| **Dashboard (`/dashboard`)** | Active Module Cards (8) | `ui.navigate.to(f"/module/{m_id}")` | `/module/{id}` | Yes | `/module/{id}` | Yes | Target is correct, but progress calculation must use authenticated user ID. |
| **Curriculum (`/curriculum`)** | Start Module 1 Button | `ui.navigate.to("/module/1")` | `/module/1` | Yes | `/module/1` | Yes | Correct destination. |
| **Curriculum (`/curriculum`)** | Study Dashboard Button | `ui.navigate.to("/dashboard")` | `/dashboard` | Yes | `/dashboard` | Yes | Correct destination. |
| **Curriculum (`/curriculum`)** | Module Cards Header | `ui.navigate.to(f"/module/{m_id}")` | `/module/{id}` | Yes | `/module/{id}` | Yes | Correct destination. |
| **Curriculum (`/curriculum`)** | Module Card CTA | `ui.navigate.to(f"/module/{m_id}/lesson/{first_id}")` | `/module/{id}/lesson/{first_id}` | Yes | First lesson or next incomplete lesson | Partial | Better: resume active lesson in that module if started. |
| **Module (`/module/{id}`)** | Begin Lesson Sequence Button | `ui.navigate.to(f"/module/{id}/lesson/{first_id}")` | `/module/{id}/lesson/{first_id}` | Yes | Active or first lesson in module | Yes | Resolves correctly. |
| **Module (`/module/{id}`)** | Lesson List Cards (5) | `ui.navigate.to(f"/module/{id}/lesson/{l_id}")` | `/module/{id}/lesson/{l_id}` | Yes | Specific lesson workspace | Yes | Resolves correctly. |
| **Module (`/module/{id}`)** | Open Practice Lab Button | `ui.navigate.to(f"/practice?module={id}")` | `/practice?module={id}` | Yes | `/practice?module={id}` | Yes | Resolves correctly. |
| **Module (`/module/{id}`)** | Take Assessment Button | `ui.navigate.to(f"/module/{id}/quiz")` | `/module/{id}/quiz` | Yes | `/module/{id}/quiz` | Yes | Resolves correctly. |
| **Module (`/module/{id}`)** | Project Workshop Button | `ui.navigate.to(f"/projects?module={id}")` | `/projects?module={id}` | Yes | `/projects?module={id}` | Yes | Resolves correctly. |
| **Lesson (`/module/{id}/lesson/{id}`)** | Return to Curriculum Button | `ui.navigate.to("/curriculum")` | `/curriculum` | Yes | `/curriculum` | Yes | Correct. |
| **Lesson (`/module/{id}/lesson/{id}`)** | Next Lesson Button (Check) | `ui.navigate.to(f"/module/{id}/lesson/{next_id}")` | Next lesson | Yes | Next sequential lesson | Yes | Correct. |
| **Lesson (`/module/{id}/lesson/{id}`)** | Module Assessment Button | `ui.navigate.to(f"/module/{id}/quiz")` | `/module/{id}/quiz` | Yes | `/module/{id}/quiz` | Yes | Correct. |
| **Lesson (`/module/{id}/lesson/{id}`)** | Previous Lesson Link | `ui.navigate.to(f"/module/{id}/lesson/{prev_id}")` | Prev lesson or module | Yes | Previous lesson / module | Yes | Correct. |
| **Practice (`/practice`)** | Module Selector Dropdown | `ui.navigate.to(f"/practice?module={val}")` | `/practice?module={val}` | Yes | Selected module practice | Yes | Correct. |
| **Quiz (`/module/{id}/quiz`)** | Return to Module Button | `ui.navigate.to(f"/module/{id}")` | `/module/{id}` | Yes | `/module/{id}` | Yes | Correct. |
| **Quiz (`/module/{id}/quiz`)** | Proceed to Project Workshop | `ui.navigate.to(f"/projects?module={id}")` | `/projects?module={id}` | Yes | `/projects?module={id}` | Yes | Correct. |
| **Settings (`/settings`)** | Save Profile Changes Button | `update_learner_profile(...)` | Stays on `/settings` | Yes | Stays on `/settings` | **No** | Currently modifies hardcoded Learner ID 1. Must mutate authenticated learner record. |
| **Footer** | All Links (Curriculum, Practice, Projects, Achievements, Report, Settings) | Direct hyperlinks | Respective routes | Yes | Respective routes | **No** | Must enforce authentication guards so unauthenticated clicks redirect to Login. |

---

## 3. Current Learner Progress & Identity Architecture Defects

1. **Hardcoded Demonstation Identity:**
   `get_default_learner(db)` returns the first row in `learners`. If no row exists, it seeds "Aarav Sharma". In `data/pip_learn.db`, ID 1 was customized to "Dr. Priya Patel". When any new visitor opens the site, they are immediately greeted as "Dr. Priya Patel" with all her past quiz attempts and completed lessons.
2. **Continue Learning Disconnected from Progress Model:**
   In `s03_dashboard.py:36`, "Continue Learning" does not query `LessonActivity` or `LessonCompletion`. It literally calls `ui.navigate.to("/module/1/lesson/m1-l1")`.
3. **No Session Boundary or Rate Limiting:**
   FastAPI/NiceGUI server has no session middleware or authentication dependencies configured on `@ui.page` routes. Anyone can write directly to SQLite via HTTP.
4. **No Logout Capability:**
   Because there is no session token or cookie, there is no way for a user to log out or switch accounts.
5. **Missing Confirmation on Destructive Operations:**
   Settings lacks a reset mechanism, or if reset were added, there was no confirmation dialog protecting against accidental progress deletion.

---

## 4. Planned Corrections Matrix

1. **Authentication Infrastructure:**
   - Create `User` model with `id`, `username`, `email`, `password_hash` (Argon2id), `created_at`.
   - Link `Learner` to `User` via `user_id` foreign key.
   - Implement server-side session management using encrypted session cookies with expiration and rate limiting on `/login`.
2. **Authentication Route Guards:**
   - Centralize route protection with a clean decorator or middleware:
     - Public: `/`, `/login`, `/register`.
     - Protected: `/setup`, `/dashboard`, `/curriculum`, `/module/*`, `/practice`, `/projects`, `/achievements`, `/report`, `/settings`.
   - Preserve internal redirect query parameter `?redirect=...` to seamlessly return the user to their requested page after login.
3. **Centralized Navigation Service (`app/navigation/nav.py`):**
   - Provide standard functions: `start_learning()`, `continue_learning()`, `go_to_dashboard()`, `go_to_curriculum()`, `open_module(id)`, `open_lesson(mod_id, lesson_id)`, `logout()`.
   - Calculate deterministic resume position from the learner's persisted `LessonActivity`, `LessonCompletion`, and `ModuleProgress`.
4. **Header Auth Awareness:**
   - When unauthenticated: Show "Login" and "Register" buttons; hide "Setup", "Settings", and personalized controls.
   - When authenticated: Show user name/avatar, "Study Space", "Settings", and "Logout" button.
5. **Settings Reset Protection:**
   - Implement an explicit confirmation dialog before any progress reset, explaining that saved exercises, quiz scores, and achievements will be reset.

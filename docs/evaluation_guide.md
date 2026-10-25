# Pip Learn 2.0 — University Evaluation & Demonstration Guide
## Marwadi University Course 01AP0303 Viva Presentation Guide

This guide outlines the recommended live demonstration workflow for university evaluators and faculty assessing Pip Learn 2.0 for Course 01AP0303 (Programming with Python).

---

## 1. Quick Start & Local Run Instructions

Ensure Python 3.12+ (or virtual environment) is active:

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Run automated test suite (all 22 tests should pass)
pytest -v

# 3. Launch Pip Learn local server
python app/main.py
```

The platform will start immediately at:
**`http://localhost:8080`**

---

## 2. Recommended 7-Step Demonstration Walkthrough

### Step 1: Homepage & Editorial Brand Identity (Screen 01)
- Navigate to `http://localhost:8080/`.
- Show the editorial aesthetic: Instrument Serif typography, warm ivory surfaces (`#F5F2EC`, `#FBF8F3`), and masterwork **`ART-01 (The Beginning)`**.
- Point out the 5-stage pedagogical framework: *Understand → Experiment → Practice → Prove → Progress*.
- Click **"Explore Curriculum"** or **"Start Learning"**.

### Step 2: Learner Setup & Personalization (Screen 02)
- Navigate to `http://localhost:8080/setup`.
- Show personalized onboarding: configure your name (e.g. "Aarav Sharma"), select your skill level (Beginner/Intermediate), and note the dynamic course recommendation.
- Click **"Save & Enter Study Space"** to commit the record to SQLite and transition directly to the Dashboard.

### Step 3: Learner Dashboard (Screen 03)
- Navigate to `http://localhost:8080/dashboard`.
- Point out **`ART-03 (The Study)`** dashboard artwork.
- Highlight the real-time metric cards reading directly from SQLite (overall progress, lessons completed, practice runs, earned achievements).
- Demonstrate the active module cards with dynamic progress bars.

### Step 4: Curriculum Explorer & Module Overview (Screens 04 & 05)
- Navigate to `http://localhost:8080/curriculum`.
- Show the 8 syllabus units with actual contact hours (total 45 hours) and assessment marks.
- Click into **Module 1 (Python Fundamentals)** at `http://localhost:8080/module/1` to demonstrate the single reusable template populated with actual module learning objectives, topics, and lesson sequences.

### Step 5: Interactive Lesson Workspace & Sandbox (Screen 06)
- Navigate to `http://localhost:8080/module/1/lesson/m1-l1`.
- Demonstrate the distraction-free reading layout with conceptual markdown.
- Show the interactive educational diagrams (e.g. Memory Reference Binding model on Lesson 2, or Sequence Slicing model on Module 3).
- Test the **Live Code Workbench**: edit the Python code and click **"Run Code ▶"**. Show stdout printing in real time and execution time in milliseconds.
- Test the interactive **Concept Checkpoint**: select an option and click "Verify Understanding" for instant feedback.
- Click **"Complete & Next Lesson →"** to prove that lesson completion persists into SQLite.

### Step 6: Practice Laboratory & Automated Assertions (Screen 07)
- Navigate to `http://localhost:8080/practice`.
- Filter exercises by module (e.g. Module 1: Temperature Conversion Utility, or Module 3: Student Grade Analyzer).
- Demonstrate the step-by-step expandable hints.
- Click **"Validate Solution ▶"** to run the learner code against automated test cases in an isolated subprocess.
- Show test case badges turning green (`✓ Passed`) and the "Code Crafter" achievement unlocking.

### Step 7: Practical Project Workshop (Screen 09)
- Navigate to `http://localhost:8080/projects`.
- Demonstrate the working functional implementations:
  1. **Smart Calculator**: Enter numbers, select operations (+, -, *, /, sqrt, discount), and test zero-division prevention.
  2. **Payroll Processing**: Enter employee hours and rate, calculate overtime (1.5x) and progressive taxes, and view itemized payslips.
  3. **Inventory Tracker**: Add a new SKU, track stock levels, and review reorder alerts and category valuation.
  4. **Log File Analyzer**: Parse sample log entries, classify event levels, and observe calculated error rates.
  5. **Banking Management System**: Execute an inter-account funds transfer and verify updated balances in the transaction ledger.
  6. **Customer CRM (SQLite)**: Create, search, update, and delete customer records with parameterized SQL injection defense.
  7. **Weather API Dashboard**: Query meteorological REST data for Rajkot/Ahmedabad with offline fallback.
  8. **Sales Analytics Dashboard**: Run Pandas aggregations and view the generated Matplotlib dual-chart figure.

### Step 8: Academic Evaluation Report & JSON Export (Screen 11)
- Navigate to `http://localhost:8080/report`.
- Show the comprehensive 100-mark Internal Assessment matrix mapping each module to implemented evidence.
- Click **"Download Dossier (JSON)"** to download the student evaluation file.

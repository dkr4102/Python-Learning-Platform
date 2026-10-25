"""
Activity: Student Grade Analyzer (Module 3 Companion)
Analyzes student grade cohorts, calculates letter grades, averages, and statistical distributions.
"""
from typing import Dict, Any, List

def analyze_student_grades(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Input: list of {"name": str, "score": float}
    Output: summary statistics, highest, lowest, and letter grade classifications.
    """
    if not records:
        return {"success": False, "error": "No student records provided."}

    scored_list = []
    grade_distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

    for r in records:
        name = r.get("name", "Unknown")
        try:
            score = float(r.get("score", 0.0))
        except (ValueError, TypeError):
            continue

        if score >= 90.0:
            letter = "A"
            points = 4.0
        elif score >= 80.0:
            letter = "B"
            points = 3.0
        elif score >= 70.0:
            letter = "C"
            points = 2.0
        elif score >= 60.0:
            letter = "D"
            points = 1.0
        else:
            letter = "F"
            points = 0.0

        grade_distribution[letter] += 1
        scored_list.append({
            "name": name,
            "score": score,
            "letter": letter,
            "grade_points": points
        })

    if not scored_list:
        return {"success": False, "error": "No valid numerical scores found."}

    scores = [s["score"] for s in scored_list]
    avg_score = sum(scores) / len(scores)
    gpa = sum(s["grade_points"] for s in scored_list) / len(scored_list)
    top_student = max(scored_list, key=lambda s: s["score"])
    lowest_student = min(scored_list, key=lambda s: s["score"])

    return {
        "success": True,
        "total_students": len(scored_list),
        "class_average": round(avg_score, 2),
        "cohort_gpa": round(gpa, 2),
        "highest": {"name": top_student["name"], "score": top_student["score"]},
        "lowest": {"name": lowest_student["name"], "score": lowest_student["score"]},
        "grade_distribution": grade_distribution,
        "students": scored_list
    }

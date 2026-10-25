"""
Activity: Email Automation Tool (Module 7 Companion)
MIME template compilation, validation, and safe interactive dispatch previews.
"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Any

TEMPLATES = {
    "PROGRESS_ALERT": {
        "title": "Academic Progress Milestone",
        "subject": "Progress Report: {course_code} - Module {module_id} Completed",
        "body": """Dear {learner_name},

Congratulations on completing Module {module_id}: {module_title} in course {course_code}.

Summary of Achievements:
- Module Completion: {completion_pct}%
- Assessment Score: {score}/100.0
- Practical Project: {project_title} Verified

Keep building your Python mastery. Your next recommended session is available on your Pip Learn dashboard.

Warm regards,
Pip Learn Academic Operations
Marwadi University Faculty of Engineering"""
    },
    "ASSESSMENT_REMINDER": {
        "title": "Internal Assessment Notification",
        "subject": "Notice: 01AP0303 Continuous Internal Assessment Window Open",
        "body": """Attention {learner_name},

The internal assessment for Marwadi University course {course_code} is currently active.
Ensure you have completed all laboratory assignments and module quizzes before the evaluation deadline.

Current standing: {completion_pct}% of contact hours fulfilled.

Academic Advisory Office
Marwadi University"""
    }
}

def render_email_template(
    template_key: str,
    learner_name: str,
    recipient_email: str,
    course_code: str = "01AP0303",
    module_id: int = 7,
    module_title: str = "API Integration & Automation",
    completion_pct: float = 87.5,
    score: float = 95.0,
    project_title: str = "Weather API Dashboard"
) -> Dict[str, Any]:
    tpl = TEMPLATES.get(template_key, TEMPLATES["PROGRESS_ALERT"])
    subs = {
        "learner_name": learner_name or "Learner",
        "course_code": course_code,
        "module_id": module_id,
        "module_title": module_title,
        "completion_pct": f"{completion_pct:.1f}",
        "score": f"{score:.1f}",
        "project_title": project_title
    }

    subject = tpl["subject"].format(**subs)
    body = tpl["body"].format(**subs)

    msg = MIMEMultipart()
    msg["From"] = "academic-dispatch@piplearn.edu"
    msg["To"] = recipient_email or "student@marwadi.edu"
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    raw_rfc_str = msg.as_string()

    return {
        "success": True,
        "from": "academic-dispatch@piplearn.edu",
        "to": recipient_email or "student@marwadi.edu",
        "subject": subject,
        "body": body,
        "raw_mime": raw_rfc_str,
        "safe_mode": "SIMULATION_MODE (Requires explicit user confirmation to dispatch)"
    }

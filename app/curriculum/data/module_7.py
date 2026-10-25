"""
Module 7: API Integration, Automation and Reporting
Marwadi University 01AP0303 - Unit 7 (6 Contact Hours, 12 Marks Assessment)
Mini-Project: Weather API Dashboard & Email Automation Tool
"""
from app.curriculum.models import Module, Lesson, PracticeExercise, QuizQuestion, ProjectInfo, CommonMistake, MiniCheckpoint

MODULE_7 = Module(
    id=7,
    code="MOD-07",
    title="API Integration, Automation & Reporting",
    syllabus_unit="Unit 7: REST APIs, HTTP Requests, Task Automation & Telemetry",
    contact_hours=6,
    assessment_marks=12,
    description="Consume RESTful web services using requests, parse JSON payloads, handle transient network timeouts, construct MIME email templates with security safeguards, and automate reporting pipelines.",
    learning_objectives=[
        "Understand HTTP protocol verbs (GET, POST), headers, query parameters, and status codes",
        "Consume public REST APIs securely using the Python requests library with timeout guardrails",
        "Parse, validate, and extract nested JSON telemetry payloads",
        "Construct an automated email generation tool using email.mime with safe preview safeguards",
        "Build resilient automated data ingestion scripts that recover from service outages"
    ],
    topics_covered=[
        "REST Architecture & HTTP Fundamentals (GET, POST, Status Codes)",
        "The requests Library: Headers, Params & JSON Parsing",
        "Resilient Network Error Handling (Timeouts, HTTPError, ConnectionError)",
        "Public API Consumption & Rate Limiting",
        "Task Automation & Scheduled Workflows",
        "Email Automation: MIME Construction & smtplib Safety Safeguards",
        "Automated System & Performance Report Generation"
    ],
    artwork_id="ART-11",
    project=ProjectInfo(
        id="proj-weather-dashboard",
        title="Weather API Dashboard",
        subtitle="Live Meteorological REST Ingestion & Telemetry Visualizer",
        objective="Develop a production-grade weather station application consuming live public meteorological REST services (such as Open-Meteo or wttr.in), parsing temperature, wind velocity, humidity, and atmospheric conditions, with automatic fallback handling when offline.",
        requirements=[
            "Execute HTTP GET queries with timeout parameters to public REST endpoints",
            "Parse JSON responses containing temperature, humidity, and condition forecasts",
            "Implement robust error recovery for connection failures or unavailable endpoints",
            "Provide search functionality for major world cities and campuses (including Rajkot / Marwadi University)",
            "Complement with the Email Automation Tool for scheduled report delivery"
        ],
        starter_snippet="""# Module 7 Project: Weather API Ingestion
import requests

def fetch_weather(city="Rajkot"):
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url, timeout=4.0)
        response.raise_for_status()
        data = response.json()
        current = data["current_condition"][0]
        return {
            "city": city,
            "temp_C": current["temp_C"],
            "humidity": current["humidity"],
            "desc": current["weatherDesc"][0]["value"]
        }
    except Exception as err:
        return {"error": f"Service unavailable: {err}"}
""",
        module_id=7
    ),
    lessons=[
        Lesson(
            id="m7-l1",
            title="REST Web Services & HTTP Fundamentals",
            subtitle="Client-server architecture, HTTP methods, headers, and status code families.",
            reading_time_min=6,
            concept_markdown="""### The Anatomy of a Web API

A **REST (Representational State Transfer)** API enables software systems to communicate over HTTP using standardized conventions:

- **Client**: Initiates an HTTP request to an endpoint URL.
- **Server**: Processes the request and returns an HTTP response containing headers, a status code, and a data payload (typically JSON).

#### Core HTTP Verbs:
- `GET`: Retrieve data without modifying server state (idempotent & safe).
- `POST`: Submit new data or trigger an action on the server.
- `PUT` / `PATCH`: Update an existing resource.
- `DELETE`: Remove a resource.

#### Standard HTTP Status Code Families:
- `2xx Success`: `200 OK`, `201 Created`
- `3xx Redirection`: `301 Moved Permanently`
- `4xx Client Error`: `400 Bad Request`, `401 Unauthorized`, `404 Not Found`
- `5xx Server Error`: `500 Internal Server Error`, `503 Service Unavailable`
""",
            syntax_example="""# Basic requests GET invocation
import requests

response = requests.get("https://api.github.com", timeout=5.0)
print(f"Status Code: {response.status_code}")
print(f"Content Type: {response.headers.get('Content-Type')}")
""",
            executable_code="""# Executable mock HTTP request demonstration
import json

# Simulating an API response structure
mock_api_payload = '''{
    "status": 200,
    "course": "01AP0303",
    "institution": "Marwadi University",
    "metrics": {
        "active_students": 128,
        "completion_rate": 0.88
    }
}'''

data = json.loads(mock_api_payload)
print("API Response Parsed:")
print(f"Course: {data['course']} ({data['institution']})")
print(f"Active Learners: {data['metrics']['active_students']}")
print(f"Completion Rate: {data['metrics']['completion_rate']:.1%}")
""",
            expected_output="""API Response Parsed:
Course: 01AP0303 (Marwadi University)
Active Learners: 128
Completion Rate: 88.0%""",
            output_explanation="The json standard library decodes the serialized text stream into native Python dictionaries and lists.",
            common_mistakes=[
                CommonMistake(
                    mistake="Omitting the `timeout` parameter in `requests.get()`",
                    explanation="Without a timeout, your Python application can hang indefinitely if the remote server drops the socket connection.",
                    correction="Always specify an explicit timeout: `requests.get(url, timeout=5.0)`."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="Which HTTP status code signifies that a resource was successfully found and returned?",
                options=["200 OK", "404 Not Found", "500 Server Error", "301 Redirect"],
                correct_index=0,
                explanation="200 OK is the standard HTTP status code for a successful request."
            )
        ),
        Lesson(
            id="m7-l2",
            title="Consuming APIs with `requests` & JSON Parsing",
            subtitle="Query parameters, headers, response.json(), and raise_for_status().",
            reading_time_min=7,
            concept_markdown="""### The Python `requests` Library

The third-party `requests` library is the de facto standard for HTTP in Python, offering an intuitive, human-friendly API.

#### Best Practices:
1. **Query Parameters**: Pass parameters as a dictionary via `params=...` rather than manually formatting URL strings.
2. **Raise for Status**: Call `response.raise_for_status()` to automatically raise an `HTTPError` if the response was a 4xx or 5xx error.
3. **Native JSON Deserialization**: Use `response.json()` to convert the JSON response body directly into a Python dictionary.

```python
import requests

params = {"latitude": 22.3039, "longitude": 70.8022, "current_weather": True}
response = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params=params,
    timeout=5.0
)
response.raise_for_status()
data = response.json()
print("Temperature:", data["current_weather"]["temperature"])
```
""",
            syntax_example="""# Passing custom headers and query params
headers = {"User-Agent": "PipLearn-Client/2.0"}
params = {"format": "j1"}
res = requests.get("https://wttr.in/Rajkot", headers=headers, params=params, timeout=4.0)
""",
            executable_code="""# Executable JSON transformation demo
import json

sample_json = '''[
    {"id": 1, "station": "Rajkot Main", "temp_c": 28.5, "status": "Clear"},
    {"id": 2, "station": "MU Campus", "temp_c": 27.8, "status": "Partly Cloudy"}
]'''

stations = json.loads(sample_json)
print(f"Received data from {len(stations)} meteorological stations:")
for s in stations:
    print(f" -> {s['station']:<12}: {s['temp_c']}°C ({s['status']})")
""",
            expected_output="""Received data from 2 meteorological stations:
 -> Rajkot Main : 28.5°C (Clear)
 -> MU Campus   : 27.8°C (Partly Cloudy)""",
            output_explanation="JSON arrays deserialize into Python lists of dictionaries, which can be directly traversed and displayed.",
            common_mistakes=[
                CommonMistake(
                    mistake="Manually calling `json.loads(response.text)` instead of `response.json()`",
                    explanation="Calling `response.json()` is cleaner and respects the HTTP charset encoding negotiated with the server.",
                    correction="Use `data = response.json()`."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What method on a `requests.Response` object throws an exception if the HTTP status was 404 or 500?",
                options=["response.validate()", "response.raise_for_status()", "response.check_error()", "response.assert_ok()"],
                correct_index=1,
                explanation="`response.raise_for_status()` checks if the status code indicates an HTTP error (>= 400) and raises HTTPError."
            )
        ),
        Lesson(
            id="m7-l3",
            title="Network Resilience & Error Recovery",
            subtitle="Handling ConnectionError, Timeout, and HTTPError gracefully.",
            reading_time_min=6,
            concept_markdown="""### Designing Fault-Tolerant Network Integrations

Network calls in distributed systems are inherently unreliable: servers reboot, routers drop packets, DNS lookups fail, and APIs rate-limit requests.

A robust software architecture **never assumes network calls succeed**.

#### The `requests` Exception Hierarchy:
- `requests.exceptions.Timeout`: Request exceeded the configured time limit.
- `requests.exceptions.ConnectionError`: DNS resolution failure or refused socket connection.
- `requests.exceptions.HTTPError`: Server returned an error status (e.g. 404 or 500).
- `requests.exceptions.RequestException`: Base class catching all requests-related exceptions.

```python
try:
    response = requests.get("https://api.example.com/data", timeout=3.0)
    response.raise_for_status()
    payload = response.json()
except requests.exceptions.Timeout:
    # Use cached data or fallback mode
    payload = get_cached_backup()
except requests.exceptions.RequestException as err:
    logger.error(f"API unreachable: {err}")
    payload = None
```
""",
            syntax_example="""# Safe fallback pattern
def fetch_telemetry_safe(url):
    try:
        r = requests.get(url, timeout=2.5)
        r.raise_for_status()
        return r.json(), None
    except requests.RequestException as err:
        return None, str(err)
""",
            executable_code="""# Executable network error interception demonstration
import requests

# Testing with an invalid domain to verify exception handling
invalid_url = "https://this-domain-does-not-exist-12345.org/api"

try:
    res = requests.get(invalid_url, timeout=1.0)
    res.raise_for_status()
except requests.exceptions.ConnectionError:
    print("Caught ConnectionError: Remote host could not be resolved. Activating offline fallback mode.")
except requests.exceptions.Timeout:
    print("Caught Timeout: Remote server took too long to respond.")
except requests.exceptions.RequestException as err:
    print(f"Handled generic request failure: {err}")
""",
            expected_output="Caught ConnectionError: Remote host could not be resolved. Activating offline fallback mode.",
            output_explanation="The script intercepts the connection failure cleanly, allowing the application to switch to offline fallback without crashing.",
            common_mistakes=[
                CommonMistake(
                    mistake="Allowing network exceptions to propagate unhandled to the user interface",
                    explanation="An unhandled ConnectionError halts the entire application and displays raw stack traces to users.",
                    correction="Catch requests.RequestException and return clear fallback messages or cached data."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What is the root exception class for all errors generated by the Python `requests` library?",
                options=["requests.exceptions.RequestException", "IOError", "NetworkError", "requests.Fail"],
                correct_index=0,
                explanation="All `requests` exceptions inherit from `requests.exceptions.RequestException`."
            )
        ),
        Lesson(
            id="m7-l4",
            title="Email Automation & Security Safeguards",
            subtitle="MIME message creation, templating, and dispatch rules.",
            reading_time_min=6,
            concept_markdown="""### Programmatic Email Dispatch with Python

Python provides standard modules for constructing and dispatching emails:
- `email.mime.text.MIMEText`: Builds plain-text or HTML email bodies.
- `email.mime.multipart.MIMEMultipart`: Allows combining text with file attachments.
- `smtplib`: Handles the SMTP (Simple Mail Transfer Protocol) client connection.

#### Safe Email Engineering Safeguards:
1. **Never send automated emails without explicit user trigger**: Automated tests and interactive tutorials must never dispatch emails to real inboxes without confirmation.
2. **Never commit SMTP passwords or API tokens**: Load credentials from environment variables.
3. **Use STARTTLS**: Always encrypt the SMTP communication channel using TLS encryption over port 587.
""",
            syntax_example="""# Constructing a MIME message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

msg = MIMEMultipart()
msg['From'] = 'system@marwadi.edu'
msg['To'] = 'aarav@marwadi.edu'
msg['Subject'] = 'Pip Learn Progress Summary'
msg.attach(MIMEText('Your Module 7 assessment is complete!', 'plain'))
""",
            executable_code="""# Executable MIME message generation and string inspection
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

msg = MIMEMultipart()
msg["From"] = "notifications@piplearn.edu"
msg["To"] = "student@marwadi.edu"
msg["Subject"] = "Course 01AP0303 - Weekly Academic Telemetry"

body = \"\"\"Dear Student,

Your Python laboratory exercises have been synchronized.
Current Progress: 87.5%
Status: Excellent Standing

Regards,
Pip Learn Automated Academic Dispatch
\"\"\"

msg.attach(MIMEText(body, "plain"))

print("Constructed RFC-compliant MIME Email Headers & Body:")
print("-" * 50)
print(msg.as_string())
""",
            expected_output="""Constructed RFC-compliant MIME Email Headers & Body:
--------------------------------------------------
Content-Type: multipart/mixed; boundary="==============="
MIME-Version: 1.0
From: notifications@piplearn.edu
To: student@marwadi.edu
Subject: Course 01AP0303 - Weekly Academic Telemetry

--===============
Content-Type: text/plain; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit

Dear Student,

Your Python laboratory exercises have been synchronized.
Current Progress: 87.5%
Status: Excellent Standing

Regards,
Pip Learn Automated Academic Dispatch

--===============--""",
            output_explanation="The email module formats the message according to RFC 5322 specifications, ready for dispatch across SMTP relays.",
            common_mistakes=[
                CommonMistake(
                    mistake="Triggering real SMTP sending inside automated unit tests",
                    explanation="Can spam real email inboxes, hit provider quotas, or fail due to network firewalls.",
                    correction="Mock the smtplib connection in tests and provide an interactive simulation preview for learners."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="What protocol does Python's built-in `smtplib` module implement?",
                options=["Simple Mail Transfer Protocol (SMTP)", "Post Office Protocol (POP3)", "Internet Message Access Protocol (IMAP)", "HTTP"],
                correct_index=0,
                explanation="smtplib implements the client side of the Simple Mail Transfer Protocol (SMTP)."
            )
        ),
        Lesson(
            id="m7-l5",
            title="Scheduled Tasks & Automated Report Generation",
            subtitle="Cron concepts, report pipelines, and markdown/HTML synthesis.",
            reading_time_min=6,
            concept_markdown="""### Automated Pipelines and Reporting

In modern engineering, Python scripts run on schedules (e.g. daily cron jobs, GitHub Actions, cloud functions) to generate reports and send alerts:

1. **Ingest**: Query databases and REST APIs for the latest metrics.
2. **Process**: Aggregate statistics, compute ratios, and flag anomalies.
3. **Format**: Synthesize data into structured Markdown, HTML, or CSV documents.
4. **Distribute**: Persist reports to disk, upload to cloud storage, or dispatch alerts.

```python
# Report Generator Pipeline
def generate_daily_audit(metrics):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    report = f'''# System Health Report
Generated: {timestamp}
- Total Queries: {metrics['queries']:,}
- Error Rate: {metrics['error_rate']:.2%}
- Service Status: {metrics['status']}
'''
    return report
```
""",
            syntax_example="""# Report generation template
report_template = "# Weekly Summary\\nLearner: {name}\\nCompleted: {pct:.1f}%"
rendered = report_template.format(name="Priya Patel", pct=94.2)
""",
            executable_code="""# Executable automated report synthesis
from datetime import datetime

audit_data = {
    "module": "01AP0303 Unit 7",
    "students_evaluated": 64,
    "pass_rate": 0.9375,
    "top_score": 100.0,
    "average_score": 88.4
}

timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

report = f\"\"\"# ACADEMIC EVALUATION TELEMETRY REPORT
Generated: {timestamp} UTC
Institution: Marwadi University

## Performance Metrics:
- Module Evaluated: {audit_data['module']}
- Total Students: {audit_data['students_evaluated']}
- Pass Percentage: {audit_data['pass_rate']:.1%}
- Class Average: {audit_data['average_score']:.1f} / 100.0
- Top Score: {audit_data['top_score']:.1f}
\"\"\"

print(report)
""",
            expected_output="""# ACADEMIC EVALUATION TELEMETRY REPORT
Generated: [Current Timestamp] UTC
Institution: Marwadi University

## Performance Metrics:
- Module Evaluated: 01AP0303 Unit 7
- Total Students: 64
- Pass Percentage: 93.8%
- Class Average: 88.4 / 100.0
- Top Score: 100.0""",
            output_explanation="The script structures real metrics into an editorial Markdown report format suitable for archival and distribution.",
            common_mistakes=[
                CommonMistake(
                    mistake="Generating reports without timestamps or audit metadata",
                    explanation="Without timestamps, operators cannot determine whether report data is fresh or stale.",
                    correction="Always include UTC generation timestamps in automated reports."
                )
            ],
            mini_checkpoint=MiniCheckpoint(
                question="Why is UTC time preferred over local time when generating automated system reports?",
                options=[
                    "UTC is faster to compute",
                    "UTC provides an unambiguous global baseline that avoids Daylight Saving Time confusion",
                    "Python cannot calculate local time",
                    "UTC is required by Markdown"
                ],
                correct_index=1,
                explanation="Coordinated Universal Time (UTC) avoids daylight saving shifts and timezone ambiguities in multi-region reporting."
            )
        )
    ],
    practice_exercises=[
        PracticeExercise(
            id="m7-ex1",
            title="Safe API JSON Extraction",
            difficulty="Beginner",
            problem_statement="Write a function `parse_weather_json(json_str)` that safely parses a JSON string containing `{'temp': 28.5, 'city': 'Rajkot', 'unit': 'C'}` and returns a formatted string: 'Rajkot: 28.5°C'.",
            input_output_expectations="Output must be 'Rajkot: 28.5°C'",
            starter_code="""import json

def parse_weather_json(json_str):
    data = json.loads(json_str)
    city = data.get("city", "Unknown")
    temp = data.get("temp", 0.0)
    unit = data.get("unit", "C")
    return f"{city}: {temp}°{unit}"

sample = '{"city": "Rajkot", "temp": 28.5, "unit": "C"}'
print(parse_weather_json(sample))
""",
            hints=[
                "Use json.loads(json_str) to convert text to dict",
                "Format as f'{city}: {temp}°{unit}'"
            ],
            test_cases=[
                {"input": "", "expected_output": "Rajkot: 28.5°C", "description": "Verify formatted weather output"}
            ],
            expected_substrings=["json.loads", "parse_weather_json"],
            solution="""import json

def parse_weather_json(json_str):
    data = json.loads(json_str)
    return f"{data['city']}: {data['temp']}°{data['unit']}"

sample = '{"city": "Rajkot", "temp": 28.5, "unit": "C"}'
print(parse_weather_json(sample))
"""
        ),
        PracticeExercise(
            id="m7-ex2",
            title="MIME Email Template Generator",
            difficulty="Intermediate",
            problem_statement="Create a function `build_email_notice(student_name, course_code, score)` that returns a dictionary with keys 'subject' and 'body'. The subject must be 'Score Update: {course_code}' and body must contain '{student_name} achieved {score}%'.",
            input_output_expectations="Calling build_email_notice('Aarav', '01AP0303', 92) must generate expected subject and body",
            starter_code="""def build_email_notice(student_name, course_code, score):
    subject = f"Score Update: {course_code}"
    body = f"Hello {student_name},\\n\\nYou achieved {score}% in course {course_code}."
    return {"subject": subject, "body": body}

notice = build_email_notice("Aarav", "01AP0303", 92)
print("Subject:", notice["subject"])
print("Body:", notice["body"])
""",
            hints=[
                "Return a dict with 'subject' and 'body' strings",
                "Use f-strings for dynamic formatting"
            ],
            test_cases=[
                {"input": "", "expected_output": "Subject: Score Update: 01AP0303", "description": "Check subject formatting"},
                {"input": "", "expected_output": "Aarav achieved 92%", "description": "Check body content"}
            ],
            expected_substrings=["build_email_notice", "Score Update"],
            solution="""def build_email_notice(student_name, course_code, score):
    return {
        "subject": f"Score Update: {course_code}",
        "body": f"Hello {student_name}, you achieved {score}% in course {course_code}."
    }

notice = build_email_notice("Aarav", "01AP0303", 92)
print("Subject:", notice["subject"])
print(notice["body"])
"""
        )
    ],
    quiz_questions=[
        QuizQuestion(
            id="m7-q1",
            question="Which HTTP method is specifically intended for retrieving data from a server without side effects?",
            options=[
                "POST",
                "GET",
                "DELETE",
                "PUT"
            ],
            correct_index=1,
            explanation="GET requests are designed to be safe and idempotent for retrieving representations of resources."
        ),
        QuizQuestion(
            id="m7-q2",
            question="What is the purpose of passing `timeout=5.0` to `requests.get()`?",
            options=[
                "To speed up the network connection",
                "To prevent the program from blocking indefinitely if the remote server fails to respond",
                "To wait at least 5 seconds before making the call",
                "To automatically retry 5 times"
            ],
            correct_index=1,
            explanation="The timeout parameter ensures the socket raises a Timeout exception if the server doesn't respond in time."
        ),
        QuizQuestion(
            id="m7-q3",
            question="What format does `response.json()` convert JSON data into in Python?",
            options=[
                "Native Python dictionaries and lists",
                "An XML Document Object Model",
                "A raw binary byte array",
                "An SQL database table"
            ],
            correct_index=0,
            explanation="`response.json()` decodes JSON strings into native Python objects (dicts, lists, ints, floats, booleans, None)."
        ),
        QuizQuestion(
            id="m7-q4",
            question="Why should automated unit test suites avoid sending real live emails via SMTP?",
            options=[
                "Python does not support SMTP in test mode",
                "Sending live emails can spam real recipients, incur API costs, and fail due to firewalls",
                "Emails can only be sent manually from a browser",
                "It violates PEP 8"
            ],
            correct_index=1,
            explanation="Tests must avoid external side effects like sending live emails; mocking or previewing ensures safe test execution."
        ),
        QuizQuestion(
            id="m7-q5",
            question="What HTTP status code range represents client errors (such as 404 Not Found)?",
            options=[
                "200-299",
                "300-399",
                "400-499",
                "500-599"
            ],
            correct_index=2,
            explanation="4xx codes indicate client-side errors (e.g. 400 Bad Request, 401 Unauthorized, 404 Not Found)."
        )
    ]
)

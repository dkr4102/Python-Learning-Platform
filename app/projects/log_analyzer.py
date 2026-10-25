"""
Project 4: Log File Analyzer
Parses system and server logs, classifies events by severity, and generates diagnostic summaries.
"""
import re
from typing import Dict, Any, List

DEFAULT_SAMPLE_LOG = """2026-10-24 10:14:02 [INFO] Auth: Learner 240101 authenticated via SSO.
2026-10-24 10:14:15 [INFO] Database: Read 12 course records in 2.4ms.
2026-10-24 10:14:48 [WARNING] Memory: Heap allocation reached 78% of container limit.
2026-10-24 10:15:10 [ERROR] Sandbox: Subprocess timeout expired after 3.5s for exercise m1-ex2.
2026-10-24 10:15:22 [INFO] Exercise: Learner Aarav submitted solution for Temperature Converter.
2026-10-24 10:16:05 [WARNING] Network: Transient socket timeout while querying wttr.in weather API.
2026-10-24 10:16:40 [CRITICAL] Storage: Database journal lock collision detected on disk volume.
2026-10-24 10:17:00 [INFO] Recovery: Journal lock cleared after automated retry."""

LOG_REGEX = re.compile(r"^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s\[(INFO|WARNING|ERROR|CRITICAL)\]\s([^:]+):\s(.+)$")

def parse_log_text(log_content: str) -> Dict[str, Any]:
    lines = log_content.strip().split("\n")
    parsed_entries: List[Dict[str, Any]] = []
    malformed_lines: List[str] = []
    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}
    critical_alerts: List[Dict[str, Any]] = []

    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue
        match = LOG_REGEX.match(cleaned)
        if match:
            timestamp, level, component, message = match.groups()
            counts[level] = counts.get(level, 0) + 1
            entry = {
                "timestamp": timestamp,
                "level": level,
                "component": component.strip(),
                "message": message.strip()
            }
            parsed_entries.append(entry)
            if level in ("ERROR", "CRITICAL"):
                critical_alerts.append(entry)
        else:
            malformed_lines.append(cleaned)

    total_valid = len(parsed_entries)
    error_count = counts["ERROR"] + counts["CRITICAL"]
    error_rate = (error_count / total_valid * 100.0) if total_valid > 0 else 0.0

    return {
        "success": True,
        "total_lines_read": len(lines),
        "valid_events_count": total_valid,
        "malformed_lines_count": len(malformed_lines),
        "counts": counts,
        "error_rate_percentage": round(error_rate, 2),
        "critical_alerts": critical_alerts,
        "recent_entries": parsed_entries[-10:] if parsed_entries else []
    }

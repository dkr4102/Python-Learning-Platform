"""Verified video metadata, deliberately separate from teaching content.

Titles, authors, and IDs were checked with YouTube's public oEmbed endpoint on
2026-10-25. A mapping is omitted when the supplied playlist has no honest topic
match. Embed availability can change, so the player keeps an external link.
"""
from dataclasses import dataclass
from typing import List, Optional, Tuple

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU"


@dataclass(frozen=True)
class LessonVideo:
    video_id: str
    title: str
    duration: str
    relevance: str
    instructor: str = "Corey Schafer"
    channel: str = "Corey Schafer"
    source_url: str = ""
    topic_coverage: Tuple[str, ...] = ()
    corresponding_lesson_ids: Tuple[str, ...] = ()
    verification_status: str = "oEmbed verified 2026-10-25"
    embed_status: str = "standard YouTube iframe; external fallback provided"


def _video(
    video_id: str,
    title: str,
    relevance: str,
    lessons: Tuple[str, ...],
    topics: Tuple[str, ...],
    instructor: str = "Corey Schafer",
    channel: str = "Corey Schafer",
    duration: str = "Not independently verified",
) -> LessonVideo:
    return LessonVideo(
        video_id=video_id,
        title=title,
        duration=duration,
        relevance=relevance,
        instructor=instructor,
        channel=channel,
        source_url=f"https://www.youtube.com/watch?v={video_id}",
        topic_coverage=topics,
        corresponding_lesson_ids=lessons,
    )


_INVENTORY = [
    _video("Sg4GMVMdOPo", "Start coding with PYTHON in 5 minutes!", "Fast-paced beginner introduction to writing and executing Python.", ("py-v2-u1-l01",), ("introduction", "basics", "first program"), instructor="Bro Code", channel="Bro Code", duration="5:15"),
    _video("YYXdXT2l-Gg", "Python Tutorial for Beginners 1: Install and Setup for Mac and Windows", "Direct environment setup support.", ("py-v2-u1-l02",), ("installation", "interpreter", "editor")),
    _video("k9TUPpGqYTo", "Python Tutorial for Beginners 2: Strings - Working with Textual Data", "Direct strings and output support.", ("py-v2-u1-l04", "py-v2-u3-l01"), ("strings", "methods", "formatting")),
    _video("khKv-8q7YmY", "Python Tutorial for Beginners 3: Integers and Floats - Working with Numeric Data", "Direct numeric and arithmetic support.", ("py-v2-u1-l06", "py-v2-u1-l07", "py-v2-u1-l09"), ("integers", "floats", "arithmetic")),
    _video("W8KRzm-HUcc", "Python Tutorial for Beginners 4: Lists, Tuples, and Sets", "Direct collection coverage.", ("py-v2-u3-l02", "py-v2-u3-l04", "py-v2-u3-l05"), ("lists", "tuples", "sets")),
    _video("daefaLgNkw0", "Python Tutorial for Beginners 5: Dictionaries - Working with Key-Value Pairs", "Direct dictionary coverage.", ("py-v2-u3-l06",), ("dictionaries", "key-value data")),
    _video("DZwmZ8Usvnk", "Python Tutorial for Beginners 6: Conditionals and Booleans - If, Else, and Elif Statements", "Direct Boolean and branching coverage.", ("py-v2-u2-l01", "py-v2-u2-l02"), ("booleans", "if", "elif", "else")),
    _video("6iF8Xb7Z3wQ", "Python Tutorial for Beginners 7: Loops and Iterations - For/While Loops", "Direct loop coverage.", ("py-v2-u2-l03", "py-v2-u2-l04"), ("for", "while", "range")),
    _video("9Os0o3wzS_I", "Python Tutorial for Beginners 8: Functions", "Direct function coverage.", ("py-v2-u2-l05",), ("functions", "parameters", "return")),
    _video("CqvZ3vGoGs0", "Python Tutorial for Beginners 9: Import Modules and Exploring The Standard Library", "Direct module coverage.", ("py-v2-u2-l06",), ("modules", "imports")),
    _video("HW29067qVWk", "Jupyter Notebook Tutorial: Introduction, Setup, and Walkthrough", "Direct Jupyter setup support.", ("py-v2-u1-l02",), ("Jupyter Notebook", "setup")),
    _video("QVdf0LgmICw", "Python Tutorial: Variable Scope - Understanding the LEGB rule and global/nonlocal statements", "Optional depth after function basics.", ("py-v2-u2-l05",), ("scope", "LEGB")),
    _video("ajrtAuDg3yw", "Python Tutorial: Slicing Lists and Strings", "Direct slicing coverage.", ("py-v2-u3-l01", "py-v2-u3-l02"), ("indexing", "slicing")),
    _video("q5uM4VKywbA", "Python Tutorial: CSV Module - How to Read, Parse, and Write CSV Files", "Direct CSV coverage.", ("py-v2-u4-l03",), ("CSV", "reading", "writing")),
    _video("Uh2ebFW8OYM", "Python Tutorial: File Objects - Reading and Writing to Files", "Direct file and context-manager coverage.", ("py-v2-u4-l01", "py-v2-u4-l02"), ("files", "read", "write")),
    _video("NIWwJbo-9_8", "Python Tutorial: Using Try/Except Blocks for Error Handling", "Direct exception coverage.", ("py-v2-u4-l04", "py-v2-u4-l05"), ("try", "except", "errors")),
    _video("-ARI4Cz-awo", "Python Tutorial: Logging Basics - Logging to Files, Setting Levels, and Formatting", "Direct logging coverage.", ("py-v2-u4-l06",), ("logging", "levels")),
    _video("ZDa-Z5JzLYM", "Python OOP Tutorial 1: Classes and Instances", "Direct introductory OOP coverage.", ("py-v2-u5-l01", "py-v2-u5-l02"), ("classes", "instances")),
    _video("BJ-VvGyQxho", "Python OOP Tutorial 2: Class Variables", "Direct class-variable coverage.", ("py-v2-u5-l03",), ("class variables", "instance variables")),
    _video("RSl87lqOXDE", "Python OOP Tutorial 4: Inheritance - Creating Subclasses", "Direct inheritance coverage.", ("py-v2-u5-l05", "py-v2-u5-l06"), ("inheritance", "overriding")),
    _video("pd-0G0MigUA", "Python SQLite Tutorial: Complete Overview - Creating a Database, Table, and Running Queries", "Direct SQLite and CRUD coverage.", ("py-v2-u6-l02", "py-v2-u6-l03", "py-v2-u6-l04", "py-v2-u6-l05"), ("SQLite", "tables", "CRUD")),
    _video("9N6a-VLBa2I", "Python Tutorial: Working with JSON Data using the json Module", "Direct JSON coverage.", ("py-v2-u7-l02",), ("JSON", "parsing")),
    _video("tb8gHvYlCFs", "Python Requests Tutorial: Request Web Pages, Download Images, POST Data, Read JSON, and More", "Direct requests and HTTP coverage.", ("py-v2-u7-l01", "py-v2-u7-l02", "py-v2-u7-l03"), ("HTTP", "requests", "GET", "POST", "JSON")),
]

VIDEOS = {}
for _video_item in _INVENTORY:
    for _lesson_id in _video_item.corresponding_lesson_ids:
        VIDEOS.setdefault(_lesson_id, _video_item)  # first, most foundational match wins
VIDEOS.update({  # archived deep-link compatibility; active progress never uses these IDs
    "m1-l1": _INVENTORY[0], "m1-l2": _INVENTORY[1], "m1-l3": _INVENTORY[2],
    "m2-l1": _INVENTORY[5], "m2-l2": _INVENTORY[6], "m2-l4": _INVENTORY[7],
    "m3-l1": _INVENTORY[3], "m3-l4": _INVENTORY[4], "m4-l1": _INVENTORY[13],
    "m4-l3": _INVENTORY[14], "m5-l1": _INVENTORY[16], "m5-l3": _INVENTORY[18],
    "m6-l1": _INVENTORY[19], "m7-l2": _INVENTORY[21],
})


def get_lesson_video(lesson_id: str) -> Optional[LessonVideo]:
    return VIDEOS.get(lesson_id)


def get_verified_video_inventory() -> List[LessonVideo]:
    return list(_INVENTORY)


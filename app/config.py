"""
Pip Learn 2.0 - Configuration and Global Settings
Marwadi University - Programming with Python (Course: 01AP0303)
"""
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
ARTWORKS_DIR = BASE_DIR / "pip-learn-artworks" / "optimized"
MASTER_ARTWORKS_DIR = BASE_DIR / "pip-learn-artworks" / "artworks"
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "pip_learn.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Course Metadata
COURSE_CODE = "01AP0303"
COURSE_NAME = "Programming with Python"
UNIVERSITY = "Marwadi University"
SYLLABUS_CONTACT_HOURS = 45
TOTAL_EVALUATION_MARKS = 100

PALETTE = {
    # Blue Interaction Color System (User Preferred)
    "primary_blue": "#4F83BC",
    "hover_blue": "#396DAB",
    "soft_blue": "#E9F1F9",
    "focus_blue": "#4F83BC",

    # Neutral Editorial Palette
    "canvas": "#F5F2EC",
    "primary_surface": "#FBF8F3",
    "secondary_surface": "#EFEAE2",
    "border": "#E2DCD2",
    "border_subtle": "#ECE7DF",
    "primary_text": "#161616",
    "secondary_text": "#5E5A55",
    "muted_text": "#8C857D",
    "forest": "#4F83BC", # Remapped for system-wide blue primary buttons
    "forest_dark": "#23342B",
    "dusty_blue": "#6E8098",
    "muted_peach": "#D8B6A3",
    "warm_sand": "#DCC9A3",
    "soft_olive": "#8B9B82",
    "success": "#2D6A4F",
    "warning": "#B4692C",
    "error": "#9D3A3A",
    "info": "#4F83BC",
    "code_bg": "#17212B",
    "code_text": "#F8FAFC"
}

# Artwork Manifest ID to Filename mapping
ARTWORK_MAPPING = {
    "ART-01": {"filename": "01-the-beginning.webp", "title": "The Beginning", "role": "Homepage Hero"},
    "ART-02": {"filename": "02-the-journey.webp", "title": "The Journey", "role": "Philosophy & Pedagogy"},
    "ART-03": {"filename": "03-the-study.webp", "title": "The Study", "role": "Learner Dashboard"},
    "ART-04": {"filename": "04-the-path.webp", "title": "The Path", "role": "Curriculum Explorer"},
    "ART-05": {"filename": "05-the-first-light.webp", "title": "The First Light", "role": "Module 1: Fundamentals"},
    "ART-06": {"filename": "06-the-crossroads.webp", "title": "The Crossroads", "role": "Module 2: Control Flow & Functions"},
    "ART-07": {"filename": "07-the-collection.webp", "title": "The Collection", "role": "Module 3: Data Structures"},
    "ART-08": {"filename": "08-the-archive.webp", "title": "The Archive", "role": "Module 4: Files & Exceptions"},
    "ART-09": {"filename": "09-the-structure.webp", "title": "The Structure", "role": "Module 5: Object-Oriented Programming"},
    "ART-10": {"filename": "10-the-connections.webp", "title": "The Connections", "role": "Module 6: Database Connectivity"},
    "ART-11": {"filename": "11-the-horizon.webp", "title": "The Horizon", "role": "Module 7: APIs & Automation"},
    "ART-12": {"filename": "12-the-observatory.webp", "title": "The Observatory", "role": "Module 8 & Analytics"}
}

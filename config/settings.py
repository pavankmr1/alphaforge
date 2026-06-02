from pathlib import Path

# ==========================================
# PROJECT ROOT
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# DATA DIRECTORIES
# ==========================================
RAW_PDF_DIR = BASE_DIR / "data/raw_pdfs"

EXTRACTED_TEXT_DIR = (
    BASE_DIR / "data/extracted_text"
)

PARSED_STRATEGY_DIR = (
    BASE_DIR / "data/parsed_strategies"
)

COMPILED_STRATEGY_DIR = (
    BASE_DIR / "data/compiled_strategies"
)

GENERATED_PINE_DIR = (
    BASE_DIR / "data/generated_pines"
)

# ==========================================
# LOGGING
# ==========================================
LOG_DIR = BASE_DIR / "logs"

LOG_FILE = LOG_DIR / "alphaforge.log"

# ==========================================
# AI SETTINGS
# ==========================================
OPENAI_MODEL = "gpt-4.1-mini"

# ==========================================
# STRATEGY SETTINGS
# ==========================================
DEFAULT_RISK_REWARD = 2.0

# ==========================================
# CREATE DIRECTORIES
# ==========================================
DIRECTORIES = [
    RAW_PDF_DIR,
    EXTRACTED_TEXT_DIR,
    PARSED_STRATEGY_DIR,
    COMPILED_STRATEGY_DIR,
    GENERATED_PINE_DIR,
    LOG_DIR
]

for directory in DIRECTORIES:

    directory.mkdir(
        parents=True,
        exist_ok=True
    )
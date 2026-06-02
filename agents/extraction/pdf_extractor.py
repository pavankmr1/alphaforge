from pathlib import Path
from loguru import logger

import fitz

# ==========================================
# PATHS
# ==========================================
PDF_DIR = Path("data/raw_pdfs")
TEXT_DIR = Path("data/extracted_text")

TEXT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================
# LOGGING
# ==========================================
logger.add(
    "logs/alphaforge.log",
    rotation="10 MB"
)

# ==========================================
# EXTRACT TEXT
# ==========================================
def extract_text_from_pdf(pdf_path: Path):

    logger.info(
        f"Extracting text from: {pdf_path.name}"
    )

    doc = fitz.open(pdf_path)

    extracted_text = ""

    for page in doc:

        page_text = page.get_text()

        extracted_text += page_text + "\n"

    return extracted_text

# ==========================================
# PROCESS ALL PDFs
# ==========================================
def process_pdfs():

    pdf_files = PDF_DIR.glob("*.pdf")

    for pdf_file in pdf_files:

        try:

            text = extract_text_from_pdf(
                pdf_file
            )

            output_file = (
                TEXT_DIR /
                f"{pdf_file.stem}.txt"
            )

            output_file.write_text(
                text,
                encoding="utf-8"
            )

            logger.success(
                f"Saved text: {output_file.name}"
            )

        except Exception as e:

            logger.error(
                f"Failed processing "
                f"{pdf_file.name}: {e}"
            )

# ==========================================
# RUN
# ==========================================
if __name__ == "__main__":

    process_pdfs()
from telethon import TelegramClient
from dotenv import load_dotenv
from loguru import logger

from pathlib import Path
import os

# ==========================================
# LOAD ENV
# ==========================================
load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

# ==========================================
# CHANNEL
# ==========================================
CHANNEL_NAME = "tradingmoods"
# ==========================================
# STORAGE
# ==========================================
PDF_DIR = Path("data/raw_pdfs")
PDF_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# LOGGING
# ==========================================
logger.add(
    "logs/alphaforge.log",
    rotation="10 MB"
)

# ==========================================
# TELEGRAM CLIENT
# ==========================================
client = TelegramClient(
    "alphaforge_session",
    API_ID,
    API_HASH
)

# ==========================================
# DOWNLOAD OLD PDFs
# ==========================================
async def download_old_pdfs():

    logger.info(
        "Starting historical PDF backfill..."
    )

    async for message in client.iter_messages(
        CHANNEL_NAME,
        limit=None
    ):

        if message.file and message.file.name:

            filename = message.file.name

            if filename.endswith(".pdf"):

                file_path = PDF_DIR / filename

                # ---------------------------------
                # SKIP DUPLICATES
                # ---------------------------------
                if file_path.exists():

                    logger.info(
                        f"Skipping existing file: {filename}"
                    )

                    continue

                logger.info(
                    f"Downloading: {filename}"
                )

                await message.download_media(
                    file=file_path
                )

                logger.success(
                    f"Downloaded: {filename}"
                )

# ==========================================
# MAIN
# ==========================================
async def main():

    await download_old_pdfs()

# ==========================================
# RUN
# ==========================================
with client:
    client.loop.run_until_complete(main())
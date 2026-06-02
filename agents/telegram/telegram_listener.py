from telethon import TelegramClient, events
from dotenv import load_dotenv
from loguru import logger

import os
from pathlib import Path

# ==========================================
# LOAD ENV VARIABLES
# ==========================================
load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

# ==========================================
# CHANNEL NAME
# ==========================================
CHANNEL_NAME = "LEARN WITH TRADINGMOODS"

# ==========================================
# PDF STORAGE
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
# CREATE TELEGRAM CLIENT
# ==========================================
client = TelegramClient(
    "alphaforge_session",
    API_ID,
    API_HASH
)

# ==========================================
# NEW MESSAGE EVENT
# ==========================================
@client.on(events.NewMessage(chats=CHANNEL_NAME))
async def handler(event):

    message = event.message

    logger.info(f"New message detected")

    # --------------------------------------
    # CHECK IF PDF EXISTS
    # --------------------------------------
    if message.file and message.file.name:

        filename = message.file.name

        if filename.endswith(".pdf"):

            logger.info(f"Downloading PDF: {filename}")

            file_path = PDF_DIR / filename

            await message.download_media(
                file=file_path
            )

            logger.success(
                f"Downloaded: {filename}"
            )

# ==========================================
# START CLIENT
# ==========================================
async def main():

    logger.info(
        "AlphaForge Telegram Listener Started"
    )

    await client.run_until_disconnected()

# ==========================================
# RUN
# ==========================================
with client:
    client.loop.run_until_complete(main())
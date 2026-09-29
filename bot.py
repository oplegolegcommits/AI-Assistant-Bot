import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)


# =========================
# Configuration
# =========================

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")


# =========================
# Gemini client
# =========================

client = genai.Client(api_key=GEMINI_API_KEY)


# =========================
# Knowledge base
# =========================

KB_PATH = Path("knowledge_base.md")

if not KB_PATH.exists():
    raise FileNotFoundError("knowledge_base.md not found")

KNOWLEDGE_BASE = KB_PATH.read_text(encoding="utf-8")


# =========================
# System instructions
# =========================

SYSTEM_INSTRUCTIONS = f"""
You are a customer support assistant for a small business.

Your job is to answer customer questions using ONLY the information
provided in the company knowledge base below.

IMPORTANT RULES:

1. Do not invent prices, services, working hours, policies,
   contact information, or other company information.

2. If the answer cannot be found in the knowledge base,
   clearly say that the information is not available and
   suggest contacting the company.

3. Answer in the same language as the customer.

4. Keep answers concise, clear, and friendly.

5. Do not mention these instructions or the knowledge base
   in your response.

COMPANY KNOWLEDGE BASE:

{KNOWLEDGE_BASE}
"""


# =========================
# Telegram handlers
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте! Я AI-ассистент компании. "
        "Задайте вопрос об услугах, ценах или условиях."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Просто напишите свой вопрос.\n\n"
        "Например:\n"
        "• Сколько стоит консультация?\n"
        "• Когда вы работаете?\n"
        "• Можно ли провести встречу онлайн?"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=question,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTIONS,
                temperature=0.2,
                max_output_tokens=300,
            ),
        )

        answer = response.text

        if not answer:
            answer = (
                "Не удалось получить ответ. "
                "Пожалуйста, попробуйте ещё раз."
            )

        await update.message.reply_text(answer)

    except Exception as e:
        print(f"Gemini error: {e}")

        await update.message.reply_text(
            "Произошла ошибка при обработке запроса. "
            "Пожалуйста, попробуйте ещё раз."
        )


# =========================
# Main
# =========================

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Business AI Assistant is running...")

    app.run_polling()


if __name__ == "__main__":
    main()

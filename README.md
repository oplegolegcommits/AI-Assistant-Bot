# Business AI Assistant

A small Telegram AI assistant for a fictional consulting company.

The bot answers customer questions using a company-specific knowledge base containing services, prices, working hours, FAQ, and company rules.

## Architecture

```text
Telegram
    ↓
Python / Telegram Bot
    ↓
Gemini API
    ↓
Company Knowledge Base
    ↓
Answer
```

## Features

- Telegram chatbot
- Gemini API integration
- Local company knowledge base
- Services and prices
- Working hours
- FAQ and company policies
- Same-language responses
- Fallback when information is unavailable

## Project Structure

```text
business-ai-assistant/
├── bot.py
├── knowledge_base.md
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Setup

### 1. Create a Telegram bot

Open Telegram, talk to **@BotFather**, create a bot, and copy its token.

### 2. Get an Gemini API key

Create an API key in your Google AI Studio.

Never publish the key or commit it to GitHub.

### 3. Configure `.env`

```text
TELEGRAM_BOT_TOKEN=your_real_telegram_token
Gemini_API_KEY=your_real_openai_api_key
GEMINI_MODEL=gemini-3.8-flash
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run

```bash
python bot.py
```

Then open your Telegram bot and send `/start`.

## Example

```text
User:
How much does a business consultation cost?

Bot:
A business consultation costs €50 and lasts 60 minutes.
```

```text
User:
Do you work on Sunday?

Bot:
No. SmartConsult is closed on Sundays.
```

```text
User:
How much is a legal consultation?

Bot:
I don't have information about legal consultations.
Please contact SmartConsult directly.
```

The last example demonstrates that the assistant does not invent information that is absent from the knowledge base.

## Customizing for a Client

For a real business, replace the contents of `knowledge_base.md` with the client's:

- company information
- services
- prices
- opening hours
- contacts
- delivery rules
- refund policy
- appointment rules
- FAQ

Basic knowledge-base changes require no Python code changes.

## Technologies

- Python
- Telegram Bot API
- Gemini API
- python-telegram-bot
- python-dotenv

## Security

Never commit `.env` to GitHub. It is already excluded by `.gitignore`.
Store API keys in environment variables rather than hard-coding them.

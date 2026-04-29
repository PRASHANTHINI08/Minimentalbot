# 🧠 Mini Mental Health Tool

A Telegram chatbot designed for college students to share feelings, rant, and receive gentle emotional support. Built with Python, Google Gemini AI, and python-telegram-bot.

> ⚠️ **Disclaimer**: This is NOT a substitute for professional mental health support. This tool is a supportive companion, not a therapist. If you're in crisis, please contact a helpline immediately.

---

## ✨ Features

- 💬 **Emotional Support** — Gentle, warm responses that make you feel heard
- 🧠 **Chat Memory** — Remembers your conversation context for natural follow-ups
- 🌐 **Bilingual** — Responds in English or Tanglish, matching your style
- ⚠️ **Crisis Detection** — Detects distress signals and provides helpline numbers
- 🎭 **Mood Adaptation** — Adjusts tone based on your emotional state
- 🔄 **Fresh Start** — Use `/reset` to clear conversation anytime

---

## 🚀 Setup Instructions

### 1. Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow the prompts to name your bot
4. Save the **API Token** you receive

### 2. Get a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click **"Get API Key"** → **"Create API key"**
4. Copy the key

### 3. Install Dependencies

```bash
# Navigate to the project folder
cd "mini mental health tool"

# (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux

# Install packages
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example file
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux

# Edit .env and add your keys:
# TELEGRAM_BOT_TOKEN=your_token_here
# GEMINI_API_KEY=your_key_here
```

### 5. Run the Bot

```bash
python bot.py
```

You should see:
```
🧠 Mini Mental Health Tool is running!
   Send /start to your bot on Telegram.
   Press Ctrl+C to stop.
```

---

## 💬 Usage

| Command  | Description                          |
|----------|--------------------------------------|
| `/start` | Begin conversation with welcome msg  |
| `/help`  | See available commands               |
| `/reset` | Clear conversation history           |

Just type anything to start talking! The bot will listen and respond with care.

---

## 📁 Project Structure

```
mini mental health tool/
├── bot.py              # Main entry point
├── config.py           # Configuration & settings
├── handlers.py         # Telegram command & message handlers
├── gemini_client.py    # Google Gemini AI integration
├── system_prompt.py    # AI personality & behavior rules
├── safety.py           # Crisis detection & helpline resources
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .env                # Your actual keys (DO NOT share!)
└── README.md           # This file
```

---

## 🆘 Crisis Helplines (India)

If you or someone you know needs help:

- **iCall** — 9152987821
- **Vandrevala Foundation** — 1860 2662 345 (24/7)
- **AASRA** — 9820466726
- **Snehi** — 044-24640050

---

## 📝 License

This project is for educational purposes only.

import os
import random
import openai
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Токены ---
TOKEN = "7756837917:AAFxCYDI7wnGGtd7MH5ifwh9jYn03pSN2UU"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # ключ OpenAI добавишь в Render

openai.api_key = OPENAI_API_KEY

# --- Данные ---
tips = [
    "Practice English at least 15 minutes every day.",
    "Think in English instead of translating.",
    "Learn phrases, not just single words.",
    "Don’t be afraid of mistakes!",
    "Listen to English podcasts or songs daily."
]

speaking_topics = [
    "Describe your favorite holiday.",
    "Talk about your best friend.",
    "What is your dream job and why?",
    "Do you prefer big cities or small towns?",
    "If you could travel anywhere, where would you go?"
]

words_of_day = [
    ("resilient", "able to recover quickly from difficulties"),
    ("serendipity", "the occurrence of events by chance in a happy way"),
    ("meticulous", "showing great attention to detail"),
    ("versatile", "able to adapt to many functions or activities"),
    ("eloquent", "fluent and persuasive in speaking")
]

# --- Команды ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["💬 Chat", "📚 Tip"], ["🗣️ Speaking", "📖 Word of the Day"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Hi! I'm @saeyle_bot, your English tutor. Choose an option:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📚 Tip":
        await update.message.reply_text(random.choice(tips))

    elif text == "🗣️ Speaking":
        await update.message.reply_text("Here’s a topic for you:\n\n" + random.choice(speaking_topics))

    elif text == "📖 Word of the Day":
        word, definition = random.choice(words_of_day)
        await update.message.reply_text(f"📖 Word: *{word}*\nMeaning: {definition}", parse_mode="Markdown")

    else:
        # Чат через OpenAI
        if OPENAI_API_KEY is None:
            await update.message.reply_text("⚠️ OpenAI API key is not set. Please add it in Render.")
            return

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an English tutor. Always reply in English."},
                {"role": "user", "content": text}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)

# --- Запуск ---
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()

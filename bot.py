import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Configuration
SOCIAL_LINKS = {
    "twitter": "https://twitter.com/gideon",
    "facebook": "https://facebook.com/gideon",
    "channel": "https://t.me/gideon",
    "group": "https://t.me/gideon1"  # Fixed from t.megideon1
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_msg = f"""
    🚀 Welcome {user.first_name} to the Megan Airdrop Call!

    To qualify for 100 SOL:
    1️⃣ Join our [Channel]({SOCIAL_LINKS['channel']})
    2️⃣ Join our [Group]({SOCIAL_LINKS['group']})
    3️⃣ Follow our [Twitter]({SOCIAL_LINKS['twitter']})
    4️⃣ Like our [Facebook]({SOCIAL_LINKS['facebook']})

    Click VERIFY after completing all steps.
    """
    
    keyboard = [[InlineKeyboardButton("✅ VERIFY", callback_data="verify")]]
    
    await update.message.reply_text(
        text=welcome_msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    social_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🐦 Twitter", url=SOCIAL_LINKS['twitter'])],
        [InlineKeyboardButton("📘 Facebook", url=SOCIAL_LINKS['facebook'])],
        [InlineKeyboardButton("✅ CONFIRM SOCIAL", callback_data="confirm_social")]
    ])
    
    await query.edit_message_text(
        text="✅ Telegram groups joined! (We trust you)\n\nNow follow our socials:",
        reply_markup=social_keyboard
    )

async def confirm_social(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("📝 Please send your SOL wallet address now:")

async def handle_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallet = update.message.text.strip()
    user = update.effective_user
    
    # Fun response message
    response = (
        "🎉 Congragtulations! You passed Megan Airdrop Call!\n\n"
        "100 SOLANA will be snet to your wallet.\n\n"
        f"🔑 Wallet: `{wallet}`\n"
        "⏳ Expected arrival: 24-48 hours\n\n"
        "Well done! Hope you really cheat the system 😉"
    )
    
    await update.message.reply_text(
        text=response,
        parse_mode="Markdown"
    )
    
    # Logging for testing purposes
    logging.info(f"User {user.id} (@{user.username}) submitted wallet: {wallet}")

if __name__ == "__main__":
    # Use your testing token directly
    TOKEN = "8187305665:AAGgRJQzwB2h2wJy2dFN9YHENf4xZIG0KD0"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify, pattern="^verify$"))
    app.add_handler(CallbackQueryHandler(confirm_social, pattern="^confirm_social$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet))
    
    app.run_polling()

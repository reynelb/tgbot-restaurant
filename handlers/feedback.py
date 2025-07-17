from telegram import Update, ReplyKeyboardRemove
from telegram.ext import MessageHandler, ConversationHandler, ContextTypes, filters

FEEDBACK = range(1)
ADMIN_CHAT_ID = 123456789  # ← Replace with your admin or channel ID

async def ask_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🗣️ Ваше мнение очень важно!\n\nПожалуйста, напишите отзыв о нашем сервисе или еде:",
        reply_markup=ReplyKeyboardRemove()
    )
    return FEEDBACK

async def save_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user = update.effective_user
    name = user.full_name

    # Send feedback to admin or channel
    text = f"📢 *Новый отзыв получен:*\n\n👤 {name}\n💬 {message}"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text, parse_mode="Markdown")

    await update.message.reply_text("✅ Спасибо за ваш отзыв! Это помогает нам становиться лучше 🙏")
    return ConversationHandler.END

# Feedback conversation handler
handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^💬 Оставить отзыв$"), ask_feedback)],
    states={
        FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_feedback)],
    },
    fallbacks=[]
)

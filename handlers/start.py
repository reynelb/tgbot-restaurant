from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from keyboards.main_menu import main_menu_keyboard

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    welcome_text = (
        f"👋 Привет, {user_first_name}!\n\n"
        "Добро пожаловать в бот ресторана 🍽.\n"
        "Что бы вы хотели сделать сегодня?"
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=ReplyKeyboardMarkup(main_menu_keyboard(), resize_keyboard=True)
    )

# Export the handler
handler = CommandHandler("start", start_command)

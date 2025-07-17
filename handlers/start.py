from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from keyboards.main_menu import main_menu_keyboard


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    welcome_text = (
        f"👋 ¡Hola, {user_first_name}!\n\n"
        "Bienvenido al bot del restaurante 🍽.\n"
        "¿Qué deseas hacer hoy?"
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=ReplyKeyboardMarkup(main_menu_keyboard(), resize_keyboard=True)
    )


# Exportamos el handler
handler = CommandHandler("start", start_command)


print(update.effective_chat.id)

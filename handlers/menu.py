from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, ContextTypes, filters, CallbackQueryHandler

# Simulated menu
MENU = {
    "Закуски": [("Брускетта", "Хлеб с помидорами и базиликом — 5$"),
                ("Эмпанадас", "С мясной начинкой — 6$")],
    "Основные блюда": [("Ломо Сальтадо", "С картофелем и рисом — 12$"),
                       ("Паэлья", "С морепродуктами — 15$")],
    "Напитки": [("Свежевыжатый сок", "Апельсиновый или ананасовый — 3$"),
                ("Красное вино", "Бокал домашнего — 6$")]
}


def build_category_keyboard():
    keyboard = [
        [InlineKeyboardButton(category, callback_data=f"menu_{category}")]
        for category in MENU.keys()
    ]
    return InlineKeyboardMarkup(keyboard)


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "📋 Вот категории меню:",
            reply_markup=build_category_keyboard()
        )


async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category = query.data.replace("menu_", "")
    items = MENU.get(category, [])
    if not items:
        await query.edit_message_text("❌ Элементы не найдены.")
        return

    text = f"📂 *{category}*\n\n"
    for name, description in items:
        text += f"• *{name}*: {description}\n"
    await query.edit_message_text(text, parse_mode="Markdown")


# Handlers
handler = MessageHandler(filters.Regex("^🍽 Посмотреть меню$"), show_menu)
callback_handler = CallbackQueryHandler(handle_menu_selection, pattern="^menu_")

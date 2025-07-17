from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, MessageHandler, ContextTypes, filters

# Simulated menu
MENU = {
    "Закуски": [("Брускетта", "5$"), ("Эмпанадас", "6$")],
    "Основные блюда": [("Ломо Сальтадо", "12$"), ("Паэлья", "15$")],
    "Напитки": [("Сок", "3$"), ("Вино", "6$")]
}

# Build category buttons
def build_category_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(cat, callback_data=f"preorder_{cat}")]
        for cat in MENU
    ] + [[InlineKeyboardButton("✅ Подтвердить заказ", callback_data="preorder_confirm")]])

# Start preorder flow
async def start_preorder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["preorder"] = []
    await update.message.reply_text(
        "📝 Выберите блюда, которые вы хотите получить по прибытии:",
        reply_markup=build_category_keyboard()
    )

# Show dishes for selected category
async def select_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category = query.data.replace("preorder_", "")
    if category == "confirm":
        return await confirm_preorder(update, context)

    items = MENU.get(category, [])
    keyboard = [
        [InlineKeyboardButton(f"{name} – {price}", callback_data=f"add_{name}")]
        for name, price in items
    ]
    keyboard.append([InlineKeyboardButton("⬅ Назад", callback_data="preorder_back")])

    await query.edit_message_text(
        f"🍽 *{category}* — выберите одно или несколько блюд:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# Add item to preorder
async def add_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    item = query.data.replace("add_", "")
    context.user_data.setdefault("preorder", []).append(item)
    await query.edit_message_text(f"✅ Добавлено: *{item}*", parse_mode="Markdown")
    await query.message.reply_text(
        "👉 Вы можете выбрать другие блюда:",
        reply_markup=build_category_keyboard()
    )

# Confirm the preorder
async def confirm_preorder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    items = context.user_data.get("preorder", [])
    if not items:
        await query.edit_message_text("⚠ Вы ещё ничего не выбрали.")
        return

    summary = "\n".join(f"• {i}" for i in items)
    await query.edit_message_text(
        f"📦 *Заказ подтверждён:*\n\n{summary}\n\nМы подготовим всё к вашему приходу!",
        parse_mode="Markdown"
    )


# Handlers
handler = MessageHandler(filters.Regex("^⏱ Заказать еду заранее$"), start_preorder)
callback_category = CallbackQueryHandler(select_category, pattern="^preorder_")
callback_add = CallbackQueryHandler(add_item, pattern="^add_")

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, MessageHandler, ContextTypes, filters

# Conversation states
PREFERENCE, ALLERGY = range(2)

# Simulated menu database with tags
MENU_TAGS = {
    "Ломо Сальтадо": ["мясо"],
    "Паэлья": ["морепродукты"],
    "Салат Цезарь": ["лёгкое", "вегетарианское"],
    "Веганский карри": ["вегетарианское", "острое"],
    "Брускетта": ["лёгкое", "вегетарианское"]
}

async def start_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_kb = [["Мясо", "Вегетарианское"], ["Лёгкое", "Острое"], ["Неважно"]]
    await update.message.reply_text(
        "🍴 Какую еду вы предпочитаете сегодня?",
        reply_markup=ReplyKeyboardMarkup(reply_kb, resize_keyboard=True)
    )
    return PREFERENCE

async def get_preference(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pref = update.message.text.lower()
    context.user_data["preference"] = pref
    await update.message.reply_text(
        "⚠ Есть ли у вас аллергии или ингредиенты, которых следует избегать?",
        reply_markup=ReplyKeyboardRemove()
    )
    return ALLERGY

async def get_allergy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    allergy = update.message.text.lower()
    pref = context.user_data["preference"]

    # Filter menu based on preference
    suggestions = []
    for dish, tags in MENU_TAGS.items():
        if pref == "неважно" or pref in tags:
            if allergy not in dish.lower():
                suggestions.append(dish)

    if suggestions:
        text = "👨‍🍳 Согласно вашим предпочтениям, мы рекомендуем:\n\n"
        text += "\n".join(f"• {s}" for s in suggestions[:3])
    else:
        text = "😕 Мы не нашли точных совпадений, но вы можете ознакомиться с полным меню."

    await update.message.reply_text(text)
    return ConversationHandler.END

# Cancel command
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Помощник отменён.")
    return ConversationHandler.END

# Conversation handler
handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^🧭 Помощь с выбором$"), start_help)],
    states={
        PREFERENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_preference)],
        ALLERGY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_allergy)],
    },
    fallbacks=[],
)

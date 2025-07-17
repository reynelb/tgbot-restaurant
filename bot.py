from telegram.ext import ApplicationBuilder
from handlers import start, menu, reservation, preorder, help_choice, feedback, contact_admin
from config import TELEGRAM_TOKEN
import logging

from handlers import menu
app.add_handler(menu.handler)
app.add_handler(menu.callback_handler)

from handlers import reservation
app.add_handler(reservation.handler)

from handlers import preorder
app.add_handler(preorder.handler)
app.add_handler(preorder.callback_category)
app.add_handler(preorder.callback_add)

from handlers import help_choice
app.add_handler(help_choice.handler)

from handlers import feedback
app.add_handler(feedback.handler)

from handlers import contact_admin
app.add_handler(contact_admin.handler)


logging.basicConfig(level=logging.INFO)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Agregar manejadores
app.add_handler(start.handler)
app.add_handler(menu.handler)
app.add_handler(reservation.handler)
app.add_handler(preorder.handler)
app.add_handler(help_choice.handler)
app.add_handler(feedback.handler)
app.add_handler(contact_admin.handler)

app.run_polling()

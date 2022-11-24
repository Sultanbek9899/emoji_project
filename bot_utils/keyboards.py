from aiogram import types
from database.manager import CategoryManager

def get_category_btns():
    categories = CategoryManager().get_all_categories()
    markup = types.InlineKeyboardMarkup(width=1)
    for c in categories:
        markup.add(
            types.InlineKeyboardButton(c.name, callback_data=f"category_{c.id}")
        )
    markup.add(
        types.InlineKeyboardButton("Смешанный", callback_data=f"category_all")
    )
    return markup
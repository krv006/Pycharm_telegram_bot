# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.types import CallbackQuery
#
#
# @dp.callback_query(lambda c: c.data and c.data.startswith("change"))
# async def savatcha(callback: CallbackQuery):
#     ikb = InlineKeyboardMarkup(row_width=3)
#     products = []
#     for product in products:
#         ikb.insert(
#             InlineKeyboardButton(
#                 text=f"{product['name']} - ${product['price']} - {product['quantity']}",
#                 callback_data=f"product_{product['name'].replace(' ', '_')}"
#             )
#         )
#     ikb.add(
#         InlineKeyboardButton(text="🛒 Savatcha", callback_data="savat"),
#         InlineKeyboardButton(text="◀️ Orqaga", callback_data="ortga")
#     )
#     await callback.message.edit_text('Savatcha narxlar va nechatliklarni belgilash uchun:',
#                                      reply_markup=ikb.as_markup())

# redict dictni  ichini tozalash uchun clear degan function qoyamiz
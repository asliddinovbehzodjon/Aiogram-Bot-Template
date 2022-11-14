from aiogram import types

from loader import dp


# Wiki bot
@dp.message_handler()
async def default(message: types.Message):
    await message.answer(message.text)


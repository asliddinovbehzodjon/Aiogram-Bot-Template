from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

# Xabar shaxsiy chatdan kelganini tekshirish
class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE

import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from data.config import CHANNELS
from utils.misc import subscription
from loader import bot


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):        
        if update.message:
            user = update.message.from_user.id
            if update.message.text in ['/start', '/help']:
                return
        elif update.callback_query:
            user = update.callback_query.from_user.id
            if update.callback_query.data == "check_subs":
                return
        else:
            return

        result = "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:\n"
        final_status = True
        btn =InlineKeyboardMarkup(row_width=1)
        for channel in CHANNELS:
            status = await subscription.check(user_id=user,
                                              channel=channel)
            final_status *= status
            channel = await bot.get_chat(channel)
            if status:
                invite_link = await channel.export_invite_link()
                btn.add(InlineKeyboardButton(text=f"✅ {channel.title}", url=invite_link))
            if not status:
                invite_link = await channel.export_invite_link()
                btn.add(InlineKeyboardButton(text=f"❌ {channel.title}",url=invite_link))
        btn.add(InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subs"))
        if not final_status:
            await update.message.answer(result, disable_web_page_preview=True,reply_markup=btn)
            raise CancelHandler()

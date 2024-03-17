import asyncio

from disnake.ext import commands

from utils.telegram_handler import TelegramClientHandler


class JustBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        self.tg_handler = TelegramClientHandler()
        super().__init__(*args, **kwargs)

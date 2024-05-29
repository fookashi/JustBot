import asyncio
import logging

import disnake

from bot import JustBot
from cogs.jokes import FunnyCogs
from cogs.music_player import MusicPlayer
from db.config import client
from db.repos.guild_info import GuildInfoRepo
from settings import get_settings

settings = get_settings()

bot = JustBot(command_prefix="!", help_command=None, intents=disnake.Intents.all())
bot.add_cog(FunnyCogs(bot))
bot.add_cog(MusicPlayer(bot))

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@bot.event
async def on_ready() -> None:
    logging.info("The bot is ready!")


@bot.event
async def on_guild_join(guild: disnake.Guild) -> None:
    async with GuildInfoRepo() as guild_repo:
        await guild_repo.add_one({"guild_id": guild.id})
        logging.info("Информация о сервере записана в БД")


@bot.event
async def on_guild_remove(guild: disnake.Guild) -> None:
    async with GuildInfoRepo() as guild_table:
        await guild_table.remove_one(guild.id, "guild_id")
        logging.info("Информация о сервере удалена из БД")


def main() -> None:
    bot.run(settings.BOT_TOKEN)


if __name__ == "__main__":
    main()

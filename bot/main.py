import logging

import disnake
from cogs.jokes import FunnyCogs
from cogs.music_player import MusicPlayer
from db.repos.guild_info import GuildInfoRepo
from just_bot import JustBot
from settings import get_settings

settings = get_settings()

bot = JustBot(command_prefix="!", help_command=None, intents=disnake.Intents.all())
funny_cogs = FunnyCogs(bot)
music_cogs = MusicPlayer(bot)
bot.add_cog(funny_cogs)
bot.add_cog(music_cogs)

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


@bot.event
async def on_message(message: disnake.Message) -> None:
    guild_info = await bot.get_guild_info(message.guild.id)
    msg_content = message.content
    logging.info(guild_info.model_dump())
    if msg_content.startswith(("!", "/")):
        command_key = msg_content.split()[0][1:]
        if (
            (channel := bot.get_channel(guild_info.spam_channel_id)) is not None
            and guild_info.spam_channel_id != message.channel.id
            and command_key in funny_cogs.command_names
        ) or (
            (channel := bot.get_channel(guild_info.music_channel_id)) is not None
            and guild_info.music_channel_id != message.channel.id
            and command_key in music_cogs.command_names
        ):
            await message.delete()
            await channel.send(
                f"{message.author.mention}, твое сообщение автоматически \
перенесено на этот канал:\n*{msg_content}*",
            )
    if guild_info.auto_demo:
        await funny_cogs.auto_demo(message)
    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(settings.BOT_TOKEN)

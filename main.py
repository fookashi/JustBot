import asyncio

import disnake

from settings import get_settings
from cogs.jokes import FunnyCogs
from cogs.music_player import MusicPlayer
from bot import JustBot
from db.tables import GuildInfoTable, GuildInfo

env_vars = get_settings().get_secrets()
TOKEN = env_vars.get('bot_token')

bot = JustBot(command_prefix="!", help_command=None, intents=disnake.Intents.all())
bot.add_cog(FunnyCogs(bot))
bot.add_cog(MusicPlayer(bot))


@bot.event
async def on_ready():
    print("The bot is ready!")

@bot.event
async def on_guild_join(guild: disnake.Guild):
    async with GuildInfoTable() as guild_table:
        info = GuildInfo(guild_id=guild.id)
        await guild_table.add_one(info)
        print('Информация о сервере записана в БД')

@bot.event
async def on_guild_remove(guild: disnake.Guild):
    async with GuildInfoTable() as guild_table:
        info = await guild_table.get_by_key(guild.id)
        if info is None:
            return
        await guild_table.remove_by_key(info.guild_id)
        print('Информация о сервере удалена из БД')

def start():
    bot.run(TOKEN)

if __name__ == '__main__':
    start()

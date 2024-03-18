import disnake

from settings import get_settings
from cogs.jokes import FunnyCogs
from bot import JustBot

env_vars = get_settings().get_secrets()
TOKEN = env_vars.get('bot_token')

bot = JustBot(command_prefix="!", help_command=None, intents=disnake.Intents.all())
bot.add_cog(FunnyCogs(bot))


@bot.event
async def on_ready():
    print("The bot is ready!")


if __name__ == '__main__':
    bot.run(TOKEN)

import asyncio
import uvloop

import disnake
from disnake.ext import commands
import yt_dlp as youtube_dl


from settings import get_settings
from web_scrapers.jokes_scraper import JokesScrapper
from web_scrapers.demotivator_creator import DemotivatorCreator
from web_scrapers.music_player import MusicPlayer
from models.images import ImageToDemotivator

env_vars = get_settings().get_secrets()
TOKEN = env_vars.get('bot_token')



class JustBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.jokes_scraper = JokesScrapper()
        self.demotivator_creator = DemotivatorCreator()
        super().__init__(*args, **kwargs)


bot = JustBot(command_prefix="!", help_command=None, intents=disnake.Intents.all(), test_guilds=[1218192939486941235,])
#bot.add_cog(MusicPlayer(bot))

@bot.event
async def on_ready():
    print("The bot is ready!")

@bot.event
async def on_message(message: disnake.Message):
    if message.author == bot.user:
        return await bot.process_commands(message)
    if not (hasattr(message, 'attachments') and len(message.attachments) == 1 and not message.content.startswith(('!', '/'))):
        return await bot.process_commands(message)
    attachment = message.attachments[0]
    try:
        image = ImageToDemotivator(name=attachment.filename, content_type=attachment.content_type, image=await attachment.read())
        demotivator = await bot.demotivator_creator.create_demotivator(text="do_random", image=image)
    except Exception:
        return await bot.process_commands(message)
    return await message.reply(file=disnake.File(demotivator.image, filename=demotivator.name))

@bot.command()
async def repeat(inter, s: str):
    await inter.send(s, )

@bot.command()
async def stupid_joke(inter):
    joke = await bot.jokes_scraper.do_stupid_joke()
    await inter.send(joke)

@bot.command()
async def joke(inter):
    joke = await bot.jokes_scraper.do_category_b_joke()
    await inter.send(joke)

@bot.command()
async def demo(ctx, *args):
    if not len(args):
        text = "do_random"
    else:
        text = " ".join(args)
    if not hasattr(ctx, 'message') or not ctx.message.attachments:
        return await ctx.send("Необходимо прикрепить изображение для создания демотиватора")

    image: disnake.Attachment = ctx.message.attachments[0]
    try:
        image = ImageToDemotivator(name=image.filename, content_type=image.content_type, image=await image.read())
    except Exception as e:
        return await ctx.send(f"Ошибка при преобразовании изображения: {e}")
    demotivator = await bot.demotivator_creator.create_demotivator(text=text, image=image)
    if demotivator is None:
        return await ctx.send("Ошибка при создании демотиватора. Попробуйте позже")
    await ctx.send(file=disnake.File(demotivator.image, filename=demotivator.name))

if __name__ == '__main__':
    bot.run(TOKEN)


# async def main():
#     cr = DemotivatorCreator()
#     data = await cr.create_demotivator("image.png")


# if __name__ == '__main__':
#     with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
#         runner.run(main())
from disnake.ext import commands
from disnake import File, Message

from bot import JustBot
from web_scrapers import JokesScrapper
from utils.demotivator_creator import DemotivatorCreator
from models.images import ImageToDemotivator


class FunnyCogs(commands.Cog):
    def __init__(self, bot: JustBot):
        self.bot = bot
        self.stupid_jokes_url = "https://www.anekdot.ru/release/anekdot/week/"
        self.jokes_scraper = JokesScrapper(bot.tg_handler)
        self.demo_creator = DemotivatorCreator()

    @commands.command()
    async def stupid_joke(self, ctx):
        joke = await self.jokes_scraper.do_stupid_joke()
        if joke == '':
            return await self.stupid_joke(ctx)
        await ctx.send(joke)

    @commands.command()
    async def joke(self, ctx):
        joke = await self.jokes_scraper.do_category_b_joke()
        if joke == '':
            return await self.joke(ctx)
        await ctx.send(joke)

    @commands.command()
    async def copypaste(self, ctx):
        copypaste = await self.jokes_scraper.do_copypaste()
        if copypaste.image is not None:
            return await ctx.send(copypaste.text, file=File(copypaste.image))
        await ctx.send(copypaste.text)

    @commands.command()
    async def demo(self, ctx, *args):
        if not len(args):
            text = None
        else:
            text = " ".join(args)
        if not hasattr(ctx, 'message') or not ctx.message.attachments:
            return await ctx.send("Необходимо прикрепить изображение для создания демотиватора")

        image = ctx.message.attachments[0]
        try:
            image = ImageToDemotivator(name=image.filename, content_type=image.content_type, image=await image.read())
        except Exception as e:
            return await ctx.send(f"Ошибка при преобразовании изображения: {e}")
        demotivator = await self.demo_creator.create_demotivator(text=text, image=image)
        if demotivator is None:
            return await ctx.send("Ошибка при создании демотиватора. Попробуйте позже")
        await ctx.send(file=File(demotivator.image, filename=demotivator.name))

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user:
            return print('Автор сообщения: JustBot')

        if not (hasattr(message, 'attachments')
                and len(message.attachments) == 1
                and not message.content.startswith(('!', '/'))):
            return print('Сообщение является командой или не содержит картинок')

        attachment = message.attachments[0]

        try:
            image = ImageToDemotivator(name=attachment.filename,
                                       content_type=attachment.content_type,
                                       image=await attachment.read())
            demotivator = await self.demo_creator.create_demotivator(image=image)

        except Exception as e:
            return print(e)

        return await message.reply(file=File(demotivator.image, filename=demotivator.name))

    @commands.command()
    async def frog(self, ctx):
        frog_data = await self.jokes_scraper.get_frog()
        if frog_data.image is None:
            return await ctx.send(frog_data.text)
        else:
            await ctx.send(frog_data.text, file=File(frog_data.image, filename='frog.jpg'))

from disnake.ext import commands
from disnake import File, Message

from bot import JustBot
from web_scrapers import JokesScrapper
from utils.demotivator_creator import DemotivatorCreator
from models.images import ImageToDemotivator
from db.tables import GuildInfoTable


class FunnyCogs(commands.Cog):
    def __init__(self, bot: JustBot):
        self.bot = bot
        self.stupid_jokes_url = "https://www.anekdot.ru/release/anekdot/week/"
        self.jokes_scraper = JokesScrapper(bot.tg_handler)
        self.demo_creator = DemotivatorCreator()

    @commands.command()
    async def stupid_joke(self, ctx: commands.Context):
        joke = await self.jokes_scraper.do_stupid_joke()
        if joke == '':
            return await self.stupid_joke(ctx)
        guild_info = await self.bot.get_guild_info(ctx.guild.id)
        if guild_info.spam_channel_id is not None:
            channel = self.bot.get_channel(guild_info.spam_channel_id)
            return await channel.send(joke)
        return await ctx.send(joke)

    @commands.command()
    async def joke(self, ctx: commands.Context):
        joke = await self.jokes_scraper.do_category_b_joke()
        if joke == '':
            return await self.joke(ctx)
        guild_info = await self.bot.get_guild_info(ctx.guild.id)
        if guild_info.spam_channel_id is not None:
            channel = self.bot.get_channel(guild_info.spam_channel_id)
            return await channel.send(joke)
        return await ctx.send(joke)

    @commands.command()
    async def copypaste(self, ctx: commands.Context):
        copypaste = await self.jokes_scraper.do_copypaste()
        if copypaste.image is not None:
            return await ctx.send(copypaste.text, file=File(copypaste.image))
        guild_info = await self.bot.get_guild_info(ctx.guild.id)
        if guild_info.spam_channel_id is not None:
            channel = self.bot.get_channel(guild_info.spam_channel_id)
            return await channel.send(copypaste.text)
        return await ctx.send(copypaste.text)

    @commands.command()
    async def demo(self, ctx: commands.Context, *args):
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

        guild_info = await self.bot.get_guild_info(ctx.guild.id)
        if guild_info.spam_channel_id is not None:
            channel = self.bot.get_channel(guild_info.spam_channel_id)
            return await channel.send(file=File(demotivator.image, filename=demotivator.name))

        return await ctx.send(file=File(demotivator.image, filename=demotivator.name))

    async def auto_demo(self, message: Message):
        if not (hasattr(message, 'attachments') and len(message.attachments) == 1):
            raise Exception('Not valid message for auto-demotivator')

        attachment = message.attachments[0]
        image = ImageToDemotivator(name=attachment.filename,
                                   content_type=attachment.content_type,
                                   image=await attachment.read())
        demotivator = await self.demo_creator.create_demotivator(image=image)

        return await message.reply(file=File(demotivator.image, filename=demotivator.name))
    
    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        guild_info = await self.bot.get_guild_info(message.guild.id)

        channel = self.bot.get_channel(guild_info.spam_channel_id)

        if channel is not None and message.content.startswith(('!', '/')):
            msg_content = message.content
            if msg_content.split()[0][1:] in self.get_commands():
                await message.delete()
                return await channel.send(f"{message.author.mention}, ваше сообщение автоматически перенесено на этот канал:\n*{msg_content}*")

        if guild_info.auto_demo:
            try:
                return await self.auto_demo(message)
            except Exception as e:
                print(e)


    @commands.command()
    async def frog(self, ctx: commands.Context):
        frog_data = await self.jokes_scraper.get_frog()
        data = {}
        data['content'] = frog_data.text
        if frog_data.image is not None:
            data['file'] = File(frog_data.image, filename='frog.jpg')
        guild_info = await self.bot.get_guild_info(ctx.guild.id)

        channel = self.bot.get_channel(guild_info.spam_channel_id)
        if guild_info.spam_channel_id is not None:
            channel = self.bot.get_channel(guild_info.spam_channel_id)
            return await channel.send(**data)

        return await ctx.send(**data)


    @commands.command()
    async def set_sc(self, ctx: commands.Context):
        if ctx.message.author.id != ctx.guild.owner_id:
            return await ctx.send("У вас не хватает прав")

        async with GuildInfoTable() as guild_table:
            await guild_table.update_by_key(ctx.guild.id, 'spam_channel_id', ctx.channel.id)
            if self.bot.guild_infos.get(ctx.guild.id) is None:
                return
            self.bot.guild_infos[ctx.guild.id]['spam_channel_id'] = ctx.channel.id

        await ctx.send("Канал для спама канал установлен")

    @commands.command()
    async def unset_sc(self, ctx: commands.Context):
        if ctx.message.author.id != ctx.guild.owner_id:
            return await ctx.send("У вас не хватает прав")

        async with GuildInfoTable() as guild_table:
            await guild_table.update_by_key(ctx.guild.id, 'spam_channel_id', None)
            if self.bot.guild_infos.get(ctx.guild.id) is None:
                return
            self.bot.guild_infos[ctx.guild.id]['spam_channel_id'] = None

        await ctx.send("Канал для спама откреплен")
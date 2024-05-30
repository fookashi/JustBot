import logging
import os

from db.repos.guild_info import GuildInfoRepo
from disnake import File, Message
from disnake.ext import commands
from models.images import ImageToDemotivator
from pydantic import ValidationError
from utils.demotivator_creator import DemotivatorCreator, DemotivatorCreatorError
from utils.web_scrapers import JokesScrapper


class FunnyCogs(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.stupid_jokes_url = "https://www.anekdot.ru/release/anekdot/week/"
        self.jokes_scraper = JokesScrapper(bot.tg_handler)
        self.demo_creator = DemotivatorCreator()

    @commands.command()
    async def stupid_joke(self, ctx: commands.Context) -> Message:
        joke = await self.jokes_scraper.do_stupid_joke()
        if joke == "":
            return await self.stupid_joke(ctx)
        guild_info = await self.bot.get_guild_info(ctx.guild.id)
        if guild_info.spam_channel_id is not None:
            channel = self.bot.get_channel(guild_info.spam_channel_id)
            return await channel.send(joke)
        return await ctx.send(joke)

    @commands.command()
    async def joke(self, ctx: commands.Context) -> Message:
        joke = await self.jokes_scraper.do_category_b_joke()
        if joke == "":
            return await self.joke(ctx)
        guild_info = await self.bot.get_guild_info(ctx.guild.id)
        if guild_info.spam_channel_id is not None:
            channel = self.bot.get_channel(guild_info.spam_channel_id)
            return await channel.send(joke)
        return await ctx.send(joke)

    @commands.command()
    async def copypaste(self, ctx: commands.Context) -> Message:
        copypaste = await self.jokes_scraper.do_copypaste()
        if copypaste.image is not None:
            await ctx.send(copypaste.text, file=File(fp=copypaste.image, filename="copypaste.jpg"))
            os.remove(copypaste.image)  # noqa: PTH107
            return None
        guild_info = await self.bot.get_guild_info(ctx.guild.id)
        if guild_info.spam_channel_id is not None:
            channel = self.bot.get_channel(guild_info.spam_channel_id)
            return await channel.send(copypaste.text)
        return await ctx.send(copypaste.text)

    @commands.command()
    async def demo(self, ctx: commands.Context, *args: int) -> Message:
        text = None if not len(args) else " ".join(args)
        if not hasattr(ctx, "message") or not ctx.message.attachments:
            return await ctx.send("Необходимо прикрепить изображение для создания демотиватора")

        image = ctx.message.attachments[0]
        try:
            image = ImageToDemotivator(name=image.filename, content_type=image.content_type, image=await image.read())
        except ValidationError as e:
            return await ctx.send(f"Ошибка при преобразовании изображения: {e}")

        demotivator = await self.demo_creator.create_demotivator(text=text, image=image)
        if demotivator is None:
            return await ctx.send("Ошибка при создании демотиватора. Попробуйте позже")

        guild_info = await self.bot.get_guild_info(ctx.guild.id)
        if guild_info.spam_channel_id is not None:
            channel = self.bot.get_channel(guild_info.spam_channel_id)
            return await channel.send(file=File(demotivator.image, filename=demotivator.name))

        return await ctx.send(file=File(demotivator.image, filename=demotivator.name))

    async def auto_demo(self, message: Message) -> Message:
        if not (hasattr(message, "attachments") and len(message.attachments) == 1):
            return None

        attachment = message.attachments[0]
        image = ImageToDemotivator(
            name=attachment.filename,
            content_type=attachment.content_type,
            image=await attachment.read(),
        )
        demotivator = await self.demo_creator.create_demotivator(image=image)

        return await message.reply(file=File(demotivator.image, filename=demotivator.name))

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.author.bot:
            return None
        guild_info = await self.bot.get_guild_info(message.guild.id)

        channel = self.bot.get_channel(guild_info.spam_channel_id)

        if channel is not None and message.content.startswith(("!", "/")):
            msg_content = message.content
            if msg_content.split()[0][1:] in self.get_commands():
                await message.delete()
                return await channel.send(
                    f"{message.author.mention}, ваше сообщение автоматически \
                        перенесено на этот канал:\n*{msg_content}*",
                )

        if guild_info.auto_demo:
            try:
                return await self.auto_demo(message)
            except DemotivatorCreatorError:
                logging.exception("Error whle trying creating autodemotivator")
        return None

    @commands.command()
    async def frog(self, ctx: commands.Context) -> Message:
        frog_data = await self.jokes_scraper.get_frog()
        data = {}
        data["content"] = frog_data.text
        if frog_data.image is not None:
            data["file"] = File(frog_data.image, filename="frog.jpg")
        guild_info = await self.bot.get_guild_info(ctx.guild.id)

        channel = self.bot.get_channel(guild_info.spam_channel_id)
        if guild_info.spam_channel_id is not None:
            channel = self.bot.get_channel(guild_info.spam_channel_id)
            return await channel.send(**data)

        return await ctx.send(**data)

    @commands.command()
    async def set_sc(self, ctx: commands.Context) -> Message:
        if ctx.message.author.id != ctx.guild.owner_id:
            return await ctx.send("У вас не хватает прав")

        async with GuildInfoRepo() as guild_repo:
            await guild_repo.update_one(ctx.guild.id, "guild_id", {"spam_channel_id": ctx.channel.id})

        return await ctx.send("Канал для спама канал установлен")

    @commands.command()
    async def unset_sc(self, ctx: commands.Context) -> Message:
        if ctx.message.author.id != ctx.guild.owner_id:
            return await ctx.send("У вас не хватает прав")

        async with GuildInfoRepo() as guild_repo:
            await guild_repo.update_one(ctx.guild.id, "guild_id", {"spam_channel_id": None})

        return await ctx.send("Канал для спама откреплен")

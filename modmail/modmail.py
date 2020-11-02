from redbot.core import commands, Config
import discord


class ModMail(commands.Cog):
    """This cog allows you to see any dms your bot receives"""

    default_global = {
        "Channel": None
    }

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, 12386760762, force_registration=True)
        self.config.register_global(**self.default_global)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not isinstance(message.channel, discord.DMChannel):
            return
        if message.author.bot:
            return
        app = await self.bot.application_info()
        if message.author.id == app.owner.id:
            return
        channel = self.bot.get_channel(await self.config.get_raw("Channel"))
        if not message.content[0] in await self.bot.get_prefix(message) and channel is not None:
            emb = discord.Embed(
                title="Mod Mail", description="From {}\n\n{}".format(
                    message.author.name, message.content), color=discord.Color.dark_magenta()
            )
            await channel.send(embed=emb)

    @commands.command()
    @commands.is_owner()
    async def modmail(self, ctx, toggle: discord.TextChannel = None):
        """Enable/disable the Mod mail"""

        if toggle is None:
            toggle = ctx.channel
        await self.config.set_raw("Channel", value=toggle.id)
        await ctx.send("Channel changed to {}".format(toggle.mention))

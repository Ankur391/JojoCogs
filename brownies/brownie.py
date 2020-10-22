# Standard Library
import asyncio
import os
import random
import time
from operator import itemgetter

# # Discord and Red
# import discord
# from .utils import checks
# from __main__ import send_cmd_help
# from .utils.dataIO import dataIO
# from discord.ext import commands
from redbot.core import commands, Config, checks
import discord


class PluralDict(dict):
    """This class is used to plural strings
    You can plural strings based on the value input when using this class as a dictionary.
    """

    def __missing__(self, key):
        if '(' in key and key.endswith(')'):
            key, rest = key.split('(', 1)
            value = super().__getitem__(key)
            suffix = rest.rstrip(')').split(',')
            if len(suffix) == 1:
                suffix.insert(0, '')
            return suffix[0] if value <= 1 else suffix[1]
        raise KeyError(key)


class Brownie(commands.Cog):
    """Collector loves brownies, and will steal from others for you!"""

    default_guild_settings = {
        "Players": {},
        "Config": {
            "Steal CD": 5,
            "brownie CD": 5
        }
    }

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 1224421848909)
        self.config.register_guild(**self.default_guild_settings)
        # self.file_path = "data/brownie/brownie.json"
        # self.system = dataIO.load_json(self.file_path)

    @commands.group()
    @commands.guild_only()
    async def setbrownie(self, ctx):
        """brownie settings group command"""

    @setbrownie.command(name="stealcd")
    @checks.admin()
    async def _stealcd_heist(self, ctx, cooldown: int):
        """Set the cooldown for stealing brownies"""
        if cooldown >= 0:
            await self.config.guild(ctx.guild).Config.set_raw("Steal CD", value=cooldown)
            msg = "Cooldown for steal set to {0}".format(cooldown)
        else:
            msg = "Cooldown needs to be higher than 0."
        await ctx.send(msg)
        # server = ctx.message.server
        # settings = self.check_server_settings(server)
        # if cooldown >= 0:
        #     pass
        #     # settings["Config"]["Steal CD"] = cooldown
        #     # dataIO.save_json(self.file_path, self.system)
        #     # msg = "Cooldown for steal set to {}".format(cooldown)
        # else:
        #     msg = "Cooldown needs to be higher than 0."
        # await ctx.send(msg)

    @setbrownie.command(name="browniecd")
    @checks.admin()
    async def _browniecd_heist(self, ctx, cooldown: int):
        """Set the cooldown for brownie command"""
        if cooldown >= 0:
            await self.config.guild(ctx.guild).Config.set_raw("brownie CD", value=cooldown)
            msg = "Cooldown for brownie set to {0}".format(cooldown)
        else:
            msg = "Cooldown needs to be higher than 0."
        await ctx.send(msg)
        # server = ctx.message.server
        # settings = self.check_server_settings(server)
        # if cooldown >= 0:
        #     settings["Config"]["brownie CD"] = cooldown
        #     dataIO.save_json(self.file_path, self.system)
        #     msg = "Cooldown for brownie set to {}".format(cooldown)
        # else:
        #     msg = "Cooldown needs to be higher than 0."
        # await ctx.send(msg)

    @commands.command()
    async def brownie(self, ctx):
        """Obtain a random number of brownies. 12h cooldown"""
        author = ctx.author
        server = ctx.guild
        action = "brownie CD"
        # settings = await self.check_server_settings(server)
        # await self.account_check(author)
        if await self.check_cooldowns(ctx, author, action):
            weighted_sample = [1] * 152 + [x for x in range(49) if x > 1]
            brownies = random.choice(weighted_sample)
            author_brownies = await self.config.guild(server).Players.author.get_raw("brownies")
            await self.config.guild(server).Players.author.set_raw("brownies", value=author_brownies+brownies)
            if brownies > 1:
                await ctx.send("{} found {} brownies!".format(author.name, brownies))
            else:
                await ctx.send('{} found 1 brownie!'.format(author.name))
            # settings["Players"][author.id]["brownies"] += brownies
            # dataIO.save_json(self.file_path, self.system)

        # if await
#     @commands.command()
#     @commands.guild_only()
#     async def brownie(self, ctx):
#         """Obtain a random number of brownies. 12h cooldown"""
#         author = ctx.message.author
#         server = ctx.message.server
#         action = "brownie CD"
#         settings = self.check_server_settings(server)
#         self.account_check(settings, author)
#         if await self.check_cooldowns(author.id, action, settings):

    @commands.command(aliases=['giveb', ])
    @commands.guild_only()
    async def givebrownie(self, ctx, user: discord.Member, brownies: int):
        """Gives another user your brownies"""
        author = ctx.author
        # settings = self.check_server_settings(ctx.guild())
        if ctx.author.id == user.id:
            return await ctx.send("You can't give yourself brownie points.")
        # await self.account_check(author)
        # await self.account_check(user)
        sender_brownies = await self.config.guild(ctx.guild).Players.author.get_raw("brownies")
        user_brownies = await self.config.guild(ctx.guild).Players.user.get_raw("brownies")
        if 0 < brownies <= sender_brownies:
            await self.config.guild(ctx.guild).Players.author.set_raw("brownies", value=sender_brownies - brownies)
            await self.config.guild(ctx.guild).Players.user.set_raw("brownies", value=user_brownies + brownies)
            msg = "{0} gave {1} brownies to {2}".format(
                ctx.author.display_name, brownies, user.display_name)
        else:
            msg = "You don't have enough brownies points"
        await ctx.send(msg)
        # if user.bot:
        #     return await ctx.send("I do not accept brownies from strangers.")
        # sender_brownies = settings["Players"][author.id]["brownies"]
        # if 0 < brownies <= sender_brownies:
        #     settings["Players"][author.id]["brownies"] -= brownies
        #     settings["Players"][user.id]["brownies"] += brownies
        #     dataIO.save_json(self.file_path, self.system)

#     @commands.command()
#     @commands.guild_only()
#     async def nom(self, ctx):
#         '''Eat a brownie'''
#         author = ctx.message.author
#         settings = self.check_server_settings(author.server)
#         self.account_check(settings, author)
#         brownies = settings['Players'][author.id]['brownies']
#         if brownies == 0:
#             await ctx.send('There are no brownies to eat.')
#         elif brownies >= 0:
#             brownies = brownies - 1
#             settings['Players'][author.id]['brownies'] = brownies
#             dataIO.save_json(self.file_path, self.system)
#             if brownies > 1:
#                 await ctx.send('Nom nom nom.\n{} has {} brownie points remaining.'.format(author.name, brownies))
#             elif brownies == 1:
#                 await ctx.send('Nom nom nom.\n{} has 1 brownie point remaining'.format(author.name))
#             else:
#                 await ctx.send('Nom nom nom.\n{} has no more brownie points'.format(author.name))

#     @commands.command(no_pm=False, ignore_extra=False)
#     async def brownies(self, ctx):
#         """See how many brownie points you have."""
#         author = ctx.message.author
#         server = ctx.message.server
#         settings = self.check_server_settings(server)
#         self.account_check(settings, author)
#         brownies = settings["Players"][author.id]["brownies"]
#         await ctx.send('{} has **{}** brownie points.'.format(author.name, brownies))

#     @commands.command()
#     @commands.guild_only()
#     async def steal(self, ctx, user: discord.Member = None):
#         """Steal brownies from another user. 2h cooldown."""
#         author = ctx.message.author
#         server = author.server
#         action = "Steal CD"
#         settings = self.check_server_settings(author.server)
#         self.account_check(settings, author)

#         if user is None:
#             user = self.random_user(settings, author, server)

#         if user == "Fail":
#             pass
#         elif user.bot:
#             return await ctx.send("Stealing failed because the picked target is a bot.\nYou "
#                                   "can retry stealing again, your cooldown is not consumed.")

#         if await self.check_cooldowns(author.id, action, settings):
#             msg = self.steal_logic(settings, user, author)
#             await ctx.send("{} is on the prowl to steal brownies.".format(author.name))
#             await asyncio.sleep(4)
#             await ctx.send(msg)

    async def check_cooldowns(self, ctx: commands.Context, user, action) -> bool:
        path = await self.config.Config.get_raw(action)
        if abs(await self.config.guild(user.guild).Players.user.get_raw(action) - int(time.perf_counter())) >= path:
            await self.config.guild(user.guild)
            return True
        elif await self.config.guild(user.guild).Players.user.get_raw(action) == 0:
            await self.config.guild(user.guild).Players.user.set_raw(action, value=int(time.perf_counter()))
            return True
        else:
            s = abs(await self.config.Players.user.action - int(time.perf_counter()))
            seconds = abs(s - path)
            remaining = self.time_formatting(seconds)
            await ctx.send("This action has a cooldown. You still have:\n{}".format(remaining))
            return False
        # path = settings["Config"][action]
        # if abs(settings["Players"][userid][action] - int(time.perf_counter())) >= path:
        #     settings["Players"][userid][action] = int(time.perf_counter())
        #     dataIO.save_json(self.file_path, self.system)
        #     return True
        # elif settings["Players"][userid][action] == 0:
        #     settings["Players"][userid][action] = int(time.perf_counter())
        #     dataIO.save_json(self.file_path, self.system)
        #     return True
        # else:
        #     s = abs(settings["Players"][userid]
        #             [action] - int(time.perf_counter()))
        #     seconds = abs(s - path)
        #     remaining = self.time_formatting(seconds)
        #     # await ctx.send("This action has a cooldown. You still have:\n{}".format(remaining))
        #     return False

    async def steal_logic(self, settings, user, author):
        success_chance = random.randint(1, 100)
        if user == "Fail":
            msg = "I couldn't find anyone with brownie points"
            return msg

        if user not in await self.config.guild(user.guild).Players:
            return "I could not find that user"
            # await self.account_check(user)

        brownies = await self.config.guild(author.guild).Players.user.get_raw("brownies")
        author_brownies = await self.config.guild(author.guild).Players.author.get_raw("brownies")

        if brownies == 0:
            msg = ('{} has no brownie points.'.format(user.name))
        else:
            if success_chance <= 90:
                brownie_jar = await self.config.guild(author.guild).Players.user.get_raw("brownies")
                brownies_stolen = int(brownie_jar * 0.75)

                if brownies_stolen == 0:
                    brownies_stolen = 1

                stolen = random.randint(1, brownies_stolen)
                await self.config.guild(author.guild).Players.user.set_raw("brownies", value=brownies - brownies_stolen)
                await self.config.guild(author.guild).Players.user.set_raw("brownies", value=author_brownies + brownies_stolen)
                msg = ("{} stole {} brownie points from {}!".format(
                    author.name, stolen, user.name))
            else:
                msg = "I could not find their brownie points"

        return msg

        # if user == "Fail":
        #     msg = "I couldn't find anyone with brownie points."
        #     return msg

        # if user.id not in settings["Players"]:
        #     self.account_check(settings, user)

        # if settings["Players"][user.id]["brownies"] == 0:
        #     msg = ('{} has no brownie points.'.format(user.name))
        # else:
        #     if success_chance <= 90:
        #         brownie_jar = settings["Players"][user.id]["brownies"]
        #         brownies_stolen = int(brownie_jar * 0.75)

        #         if brownies_stolen == 0:
        #             brownies_stolen = 1

        #         stolen = random.randint(1, brownies_stolen)
        #         # settings["Players"][user.id]["brownies"] -= stolen
        #         # settings["Players"][author.id]["brownies"] += stolen
        #         # dataIO.save_json(self.file_path, self.system)
        #         msg = ("{} stole {} brownie points from {}!".format(
        #             author.name, stolen, user.name))
        #     else:
        #         msg = "I could not find their brownie points."
        # return msg

    async def random_user(self, settings, author, server):
        filter_users = [server.get_member(x) for x in await self.config.guild(server).Players  # settings["Players"]
                        if hasattr(server.get_member(x), "name")]
        legit_users = [x for x in filter_users if x.id !=
                       author.id and x is not x.bot]

        # settings["Players"]
        users = [x for x in legit_users if await self.config.guild(server).Players.x.get_raw("brownies") > 0]
        #  [x.id]["brownies"] > 0]

        if not users:
            user = "Fail"
        else:
            user = random.choice(users)
            if user == user.bot:
                users.remove(user.bot)
                # settings["Players"].pop(user.bot)
                # dataIO.save_json(self.file_path, self.system)
                await self.config.Players.clear_raw(user.bot)
                user = random.choice(users)
            # await self.account_check(user)
        return user

    # async def account_check(self, userobj: discord.Member):
    #     player_list = await self.config.guild(userobj.guild).get_raw("Players")
    #     if userobj.id not in player_list:  # settings["Players"]:
    #         await self.config.guild(userobj.guild).Players.userobj.(
    #             "brownies",
    #             value=0
    #         )
    #         await self.config.guild(userobj.guild).Players.userobj.set_raw(
    #             "Steal CD",
    #             value=0
    #         )
    #         await self.config.guild(userobj.guild).Players.userobj.set_raw(
    #             "brownie CD",
    #             value=0
    #         )
        # settings["Players"][userobj.id] = {"brownies": 0,
        #                                    "Steal CD": 0,
        #                                    "brownie CD": 0}
        # dataIO.save_json(self.file_path, self.system)

    def time_formatting(self, seconds):
        # Calculate the time and input into a dict to plural the strings later.
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        data = PluralDict({'hour': h, 'minute': m, 'second': s})
        if h > 0:
            fmt = "{hour} hour{hour(s)}"
            if data["minute"] > 0 and data["second"] > 0:
                fmt += ", {minute} minute{minute(s)}, and {second} second{second(s)}"
            if data["second"] > 0 == data["minute"]:
                fmt += ", and {second} second{second(s)}"
            msg = fmt.format_map(data)
        elif h == 0 and m > 0:
            if data["second"] == 0:
                fmt = "{minute} minute{minute(s)}"
            else:
                fmt = "{minute} minute{minute(s)}, and {second} second{second(s)}"
            msg = fmt.format_map(data)
        elif m == 0 and h == 0 and s > 0:
            fmt = "{second} second{second(s)}"
            msg = fmt.format_map(data)
        elif m == 0 and h == 0 and s == 0:
            msg = "None"
        return msg

    # async def check_server_settings(self, server):
    #     if server.id not in self.config.:
    #         await self.config.guild(server.id).set_raw("Config", value={"Steal CD": 0, "brownie CD": 0})
    #         await self.config.guild(server.id).set_raw("Players", value={})
    #     else:
    #         return await self.config.guild(server.id)

        # ["Servers"][server.id] = {"Players": {},
        #  "Config": {"Steal CD": 5,
        #             "brownie CD": 5}
        #  }

        # dataIO.save_json(self.file_path, self.system)
        # print("Creating default heist settings for Server: {}".format(server.name))
        # path = self.system["Servers"][server.id]
        # return path
        # path = self.system["Servers"][server.id]
        # return path


# def check_folders():
#     if not os.path.exists("data/brownie"):
#         print("Creating data/brownie folder...")
#         os.makedirs("data/brownie")


# def check_files():
#     default = {"Servers": {}}

#     f = "data/brownie/brownie.json"
#     if not dataIO.is_valid_json(f):
#         print("Creating default brownie.json...")
#         dataIO.save_json(f, default)


# def setup(bot):
#     check_folders()
#     check_files()
#     bot.add_cog(Brownie(bot))

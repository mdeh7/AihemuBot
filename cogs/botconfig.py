#
# ************************************************************************
# This Cog is responsible for modifying the bots configuration
# ************************************************************************
#
# ************************************************************************
# Commands:
# changeprefix
# enableprefixmessage
# disableprefixmessage
# botprefix
# ************************************************************************

from discord.ext import commands
from typing import Union
import asyncio

class BotConfig(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def changeprefix(self, ctx, arg: Union[str, None]):
        if arg is None: # If the user does not input a character or series of characters after the command
            await ctx.send(f"Are you trying to break this command? <:neutralexpr:1233524707110948884>\n"
                           f"This is the correct usage: `{self.bot.command_prefix}changeprefix [prefix]`")
            return

        with open("prefix_message.txt", "r") as prefix_msg: # Reading prefix_message.txt to see if it contains "True" or "False"
            bot_prefix_msg = prefix_msg.readline()

        before = self.bot.command_prefix # Storing (remembering) the current prefix
        with open("bot_prefix.txt", "w") as prefix_obj: # Writing the new prefix to the prefix file -> bot_prefix.txt
            prefix_obj.write(arg)

        with open("bot_prefix.txt", "r") as read_prefix: # Setting the bot prefix to the new prefix
            self.bot.command_prefix = read_prefix.readline()

        await ctx.send(f"You successfully changed the prefix from `{before}` to `{self.bot.command_prefix}`")

        if len(arg) > 1 and bot_prefix_msg == "True": # If the inputted argument is greater than 1 character and bot_prefix_msg is set to "True", Aihemu sends a message
            await asyncio.sleep(0.75)
            await ctx.send(f"-# Yes! The prefix can be longer than 1 character! Why? Because I'm generous!")

    @commands.command()
    async def enableprefixmessage(self, ctx):
        with open("prefix_message.txt", "r") as enable_prefix_msg: # Reading the text of prefix_message.txt
            verify_enable = enable_prefix_msg.readline()
            if verify_enable == "True": # If prefix_message.txt has "True", Aihemu does not change the prefix
                await ctx.send(f"Prefix message is already enabled!")
                return

        with open("prefix_message.txt", "w") as enable_prefix_message:
            enable_prefix_message.write("True")
        await ctx.send("You enabled the prefix message!")

    @commands.command()
    async def disableprefixmessage(self, ctx):
        with open("prefix_message.txt", "r") as disable_prefix_msg:
            verify_disable = disable_prefix_msg.readline()
            if verify_disable == "False":
                await ctx.send(f"Prefix message is already disabled!")
                return

        with open("prefix_message.txt", "w") as disable_prefix_message:
            disable_prefix_message.write("False")
        await ctx.send("You disabled the prefix message!")

    @commands.command()
    async def botprefix(self, ctx):
        with open("bot_prefix.txt", "r") as bot_prefix:
            prefix = bot_prefix.readline()

        await ctx.send(f"The bot prefix is `{prefix}`")

async def setup(bot):
    await bot.add_cog(BotConfig(bot))
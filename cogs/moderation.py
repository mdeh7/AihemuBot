import discord
from discord.ext import commands
from cogs.userExistenceCheck import UserExistenceCheck


intents = discord.Intents.default() # All intents except presences, members & message_content are enabled
intents.message_content = True
intents.messages = True
intents.members = True
intents.moderation = True


class moderatorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, user: str = None, reason: str = "No reason provided"):

        userExistenceChecker = UserExistenceCheck(self.bot)
        userArgBool = await userExistenceChecker.isUserArgValid(ctx, user)

        if userArgBool is False: # If the user argument is None, not digits or between 15-19 numbers inclusive
            return

        elif not isinstance(userArgBool, discord.Member): # If the user is not a member of the server, they do not get banned
            await ctx.send(f"{userArgBool.mention} `{userArgBool.id}` is not a member of the server!")
            return

        else:
            await ctx.guild.ban(user=userArgBool, reason=reason)
            await ctx.send(f"{userArgBool.mention} `{userArgBool.id}` was banned by {ctx.author.name} for: {reason}!")
            return

    @commands.command()
    async def unban(self, ctx, user: str = None):

        userExistenceChecker = UserExistenceCheck(self.bot)
        userArgBool = await userExistenceChecker.isUserArgValid(ctx, user)

        if userArgBool is False: # If the user argument is None, not digits or between 15-19 numbers inclusive
            return

        else:
            try:
                await ctx.guild.unban(userArgBool)
                await ctx.send(f"{userArgBool.mention} `{userArgBool.id}` was unbanned by {ctx.author.name}!")
                return

            except discord.HTTPException:
                await ctx.send(f"Unban failed! {userArgBool.mention} `{userArgBool.id}` is not banned from the server!")
                return


async def setup(bot):
    await bot.add_cog(moderatorCommands(bot))
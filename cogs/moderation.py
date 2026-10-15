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
    async def ban(self, ctx, user: str = None, *, reason: str = "No reason provided"):

        userExistenceChecker = UserExistenceCheck(self.bot)
        isMember, userArgBool = await userExistenceChecker.isUserArgValid(ctx, user)

        if isMember is False:
            if isinstance(userArgBool, discord.User): # If the user is not a member of the server, they do not get banned
                await ctx.send(f"Ban failed! {userArgBool.mention} `{userArgBool.id}` is not a member of the server!")
                return
            else:
                return

        else:
            await userArgBool.send(f"You have been banned from {ctx.guild.name} for: {reason}")
            await ctx.guild.ban(user=userArgBool, reason=reason)
            await ctx.send(f"{userArgBool.mention} `{userArgBool.id}` was banned by {ctx.author.name} for: {reason}!")
            return

    @commands.command()
    async def unban(self, ctx, user: str = None):

        userExistenceChecker = UserExistenceCheck(self.bot)
        isMember, userArgBool = await userExistenceChecker.isUserArgValid(ctx, user)

        if isMember is False:
            if not isinstance(userArgBool, discord.User):
                return

        try:
            await ctx.guild.unban(userArgBool)
            await ctx.send(f"{userArgBool.mention} `{userArgBool.id}` was unbanned by {ctx.author.name}!")
            return

        except discord.HTTPException:
            await ctx.send(f"Unban failed! {userArgBool.mention} `{userArgBool.id}` is not banned from the server!")
            return

    @commands.command()
    async def kick(self, ctx, user: str = None, *, reason: str = "No reason provided"):

        userExistenceChecker = UserExistenceCheck(self.bot)
        isMember, userArgBool = await userExistenceChecker.isUserArgValid(ctx, user)

        if isMember is False:
            if isinstance(userArgBool, discord.User):
                await ctx.send(f"Kick failed! {userArgBool.mention} `{userArgBool.id}` is not on the server!")
                return
            else:
                return

        else:
            await userArgBool.send(f"You have been kicked from {ctx.guild.name} for: {reason}")
            await ctx.guild.kick(user=userArgBool, reason=reason)
            await ctx.send(f"{userArgBool.mention} `{userArgBool.id}` was kicked by {ctx.author.name}!")
            return

    @commands.command() # Forceban bans a user from a server, even if they are not a member
    async def forceban(self, ctx, user: str = None, reason: str = "No reason provided"):

        userExistenceChecker = UserExistenceCheck(self.bot)
        isMember, userArgBool = await userExistenceChecker.isUserArgValid(ctx, user)

        if isMember is False:
            if isinstance(userArgBool, discord.User): # If the user is not a member of the server, they do not get banned
                await ctx.guild.ban(user=userArgBool, reason=reason)
                await ctx.send(f"{userArgBool.mention} `{userArgBool.id}` was force-banned by {ctx.author.name} for: {reason}!")
                return
            else:
                return


async def setup(bot):
    await bot.add_cog(moderatorCommands(bot))
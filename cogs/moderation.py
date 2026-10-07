import discord
from discord.ext import commands
from discord.ext.commands import UserConverter, UserNotFound, MemberConverter, MemberNotFound
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
    async def ban(self, ctx, user: str = None):

        userExistenceChecker = UserExistenceCheck(self.bot)
        userArgBool = await userExistenceChecker.isUserArgValid(ctx, user)

        if userArgBool is False: # If the user argument is None, not digits or between 15-19 numbers inclusive
            return

        else:
            await ctx.guild.ban(userArgBool)
            await ctx.send(f"{userArgBool.mention} `{userArgBool.id}` was banned by {ctx.author.name}!")
            return

    @commands.command()
    async def unban(self, ctx, user: str = None):

        if user is None:
            await ctx.send(f"Incorrect usage!\n"
                           f"Correct usage: `{self.bot.command_prefix}unban [userID]`")
            return

        elif not user.isdigit():
            await ctx.send(f"Invalid ID! ID can only contain numbers!\n"
                           f"`Usage: {self.bot.command_prefix}unban [userID]`")
            return

        elif len(user) > 19 or len(user) < 15:
            await ctx.send(f"Invalid ID! ID must between 15 to 19 numbers long inclusive!\n"
                           f"`Usage: {self.bot.command_prefix}unban [userID]`")
            return

        try:
            unbannedUser = await UserConverter().convert(ctx, user)
            await ctx.guild.unban(unbannedUser)

        except discord.ext.commands.errors.UserNotFound:
            await ctx.send(f"Invalid ID! User with ID: `{user}` does not exist!\n"
                           f"`Usage: {self.bot.command_prefix}unban [userID]`")
            return

        except discord.HTTPException:  # If the user being unbanned is not banned
            await ctx.send(f"Unban failed! {unbannedUser.mention} `{unbannedUser.id}` is not banned from the server!")
            return

        await ctx.send(f"{unbannedUser.mention} `{unbannedUser.id}` was unbanned by {ctx.author.name}!")


async def setup(bot):
    await bot.add_cog(moderatorCommands(bot))
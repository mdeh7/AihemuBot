import discord
from discord.ext import commands
from discord.ext.commands import UserConverter, UserNotFound, MemberConverter, MemberNotFound

intents = discord.Intents.default() # All intents except presences are enabled
intents.message_content = True
intents.messages = True
intents.members = True
intents.moderation = True


class UserExistenceCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def convertUserToObject(self, ctx, user):

        try:  # Trying to convert the user into a Member object
            userObject = await MemberConverter().convert(ctx, user)
            return userObject

        except discord.ext.commands.errors.MemberNotFound:  # If the conversion fails i.e. the user being banned is not on the server
            try:  # Try to convert the user into a User object to see if the user exists in Discord
                userObject = await UserConverter().convert(ctx, user)
                return userObject

            except discord.ext.commands.errors.UserNotFound:
                await ctx.send(f"Invalid ID! User with ID: `{user}` does not exist!")
                return False

    async def isUserArgValid(self, ctx, user):
        if user is None:
            await ctx.send(f"Incorrect usage! userID is missing.")
            return False

        elif not user.isdigit():
            await ctx.send(f"Invalid ID! ID can only contain numbers!")
            return False

        elif len(user) > 19 or len(user) < 15:
            await ctx.send(f"Invalid ID! ID must between 15 to 19 numbers long inclusive!")
            return False
        else:
            return await self.convertUserToObject(ctx, user)


async def setup(bot):
    await bot.add_cog(UserExistenceCheck(bot))
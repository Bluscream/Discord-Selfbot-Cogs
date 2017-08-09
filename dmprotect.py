import discord, asyncio, datetime
from discord.ext import commands
from cogs.utils.checks import *

class DMProtect:
    """Protects you against DM invite spammers"""
    version = 1
    name = "DM Protection"
    author = "Bluscream#2597"
    authorid = 97138137679028224
    link = "https://raw.githubusercontent.com/Bluscream/Discord-Selfbot-Cogs/master/dmprotect.py"
    source = "https://github.com/Bluscream/Discord-Selfbot-Cogs/blob/master/dmprotect.py"
    support = "https://github.com/Bluscream/Discord-Selfbot-Cogs/issues/new"
    changelog = "https://github.com/Bluscream/Discord-Selfbot-Cogs/commits/master/dmprotect.py"

    def __init__(self, bot):
        self.active = True
        self.allowed = False
        self.invites = ['discord.gg', 'discord.io', 'discordapp.com/invite']
        self.bot = bot

    async def on_message(self, message):
        if not self.active: return
        if message.author.id == self.bot.user.id: return
        if not isinstance(message.channel, discord.abc.PrivateChannel): return
        if self.allowed:
            self.allowed = False
            return
        messages = await message.channel.history(limit=2).flatten()
        if not len(messages) == 1: return
        for invite in self.invites:
            if invite in message.content:
                await message.ack()
                await message.author.block()
                print('Automatically blocked user {} for sending an invite link ({}) in their first private message to you.'.format(message.author, invite))
                return

    @commands.command(aliases=['dmp'], pass_context=True)
    async def dmprotect(self, ctx):
        """Toggles DM Invite Protection."""
        await ctx.message.delete()
        self.active = not self.active
        self.allowed = True
        await ctx.send(self.bot.bot_prefix + 'DM Protection set to: `{}`'.format(self.active))

def setup(bot):
    bot.add_cog(DMProtect(bot))

import discord, asyncio
from discord.ext import commands
from cogs.utils.checks import *

class antimove:
    """Sticks you to the voice channel you're currently in"""
    version = 1
    name = "AntiMove"
    author = "Bluscream#2597"
    authorid = 97138137679028224
    link = "https://raw.githubusercontent.com/Bluscream/Discord-Selfbot-Cogs/master/antimove.py"
    source = "https://github.com/Bluscream/Discord-Selfbot-Cogs/blob/master/antimove.py"
    support = "https://github.com/Bluscream/Discord-Selfbot-Cogs/issues/new"
    changelog = "https://github.com/Bluscream/Discord-Selfbot-Cogs/commits/master/antimove.py"

    def __init__(self, bot):
        self.bot = bot
        self.active = False
        self.allowed = False

    async def on_voice_state_update(self, member, before, after):
        if not self.active: return
        if not member.id == self.bot.user.id: return
        if before.channel == after.channel: return
        if self.allowed: self.allowed = False; return
        try:
            self.allowed = True
            await member.move_to(before.channel)
            print("Someone tried to move me from \"{b}\" to \"{a}\" on guild \"{s}\"!".format(b=before.channel,a=after.channel,s=member.guild.name))
        except discord.Forbidden:
            print("Insufficient permissions to move yourself back to \"{n}\" on guild \"{s}\"".format(n=before.channel,s=member.guild.name))
            self.allowed = False

    @commands.command(aliases=['am'], pass_context=True)
    async def antimove(self, ctx):
        """Toggles Voice Antimove so you stay in the channel you choose."""
        await ctx.message.delete()
        self.active = not self.active
        await ctx.message.channel.send(self.bot.bot_prefix + 'Antimove set to: `%s`' % self.active)

def setup(bot):
    bot.add_cog(antimove(bot))

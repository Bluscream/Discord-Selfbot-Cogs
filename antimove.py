import discord, asyncio
from discord.ext import commands
from cogs.utils.checks import *

class AntiMove:
    """Sticks you to the voice channel you're currently in"""
    version = 1
    class author(discord.ClientUser):
        name = "Bluscream"
        discriminator = "2597"
        id = 97138137679028224
        email = "bluscreamlp@gmail.com"
    url = "https://raw.githubusercontent.com/LyricLy/ASCII/master/cogs/antimove.json"

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

    @commands.command(aliases=['am'])
    async def antimove(self, ctx):
        """Toggles Voice Antimove so you stay in the channel you choose."""
        await ctx.message.delete()
        self.active = not self.active
        await ctx.message.channel.send(self.bot.bot_prefix + 'Antimove set to: `%s`' % self.active)

def setup(bot):
    bot.add_cog(AntiMove(bot))

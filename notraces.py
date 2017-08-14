import discord, asyncio
from discord.ext import commands
from cogs.utils.checks import *

class NoTraces:
    """Auto delete your messages `n` seconds after you sent them."""
    version = 1
    class author(discord.ClientUser):
        name = "Bluscream"
        discriminator = "2597"
        id = 97138137679028224
        email = "admin@timo.de.vc"
    url = "https://raw.githubusercontent.com/LyricLy/ASCII/master/cogs/notraces.json"

    def __init__(self, bot):
        self.bot = bot
        self.active = False
        self.delete_after = 30

    @commands.command(aliases=['nt'], pass_context=True)
    async def notrace(self, ctx):
        """Toggles notraces mode which autodeletes **all** your messages after [seconds_tod_elete] have passed."""
        await ctx.message.delete()
        if not self.active:
        #if ' ' in ctx.message.content:
            params = ctx.message.content.split(' ', 1)
            if len(params) == 2: self.delete_after = int(params[1].strip())
            await ctx.message.channel.send("{p} No Traces mode activated, all following messages will auto-delete after {t} secs.".format(p=self.bot.bot_prefix,t=self.delete_after))
            self.active = True
        else:
            await ctx.message.channel.send("{p} No Traces mode deactivated.".format(p=self.bot.bot_prefix))
            self.active = False

    async def on_message(self, message):
        if self.active and message.author == self.bot.user:
            await asyncio.sleep(self.delete_after)
            await message.delete()

def setup(bot):
    bot.add_cog(NoTraces(bot))

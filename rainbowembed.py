import discord, asyncio
from random import randint
from discord.ext import commands


class RainbowEmbed:
    """Makes one of your embeds **very** colorful."""
    version = 1
    name = "RainbowEmbed"
    author = "Bluscream#2597"
    authorid = 97138137679028224
    link = "https://raw.githubusercontent.com/Bluscream/Discord-Selfbot-Cogs/master/rainbowembed.py"
    source = "https://github.com/Bluscream/Discord-Selfbot-Cogs/blob/master/rainbowembed.py"
    support = "https://github.com/Bluscream/Discord-Selfbot-Cogs/issues/new"
    changelog = "https://github.com/Bluscream/Discord-Selfbot-Cogs/commits/master/rainbowembed.py"

    message = None
    content = None
    def __init__(self, bot):
        self.bot = bot

    async def loop(self):
        while self.message is not None:
            await self.message.edit(content=None, embed=discord.Embed(description=self.content, color=discord.Colour.from_rgb(r=randint(0, 255), g=randint(0, 255), b=randint(0, 255))))
            await asyncio.sleep(1)

    @commands.command(aliases=['rbembed', 'rb'], pass_context=True)
    async def rainbowembed(self, ctx, msg_id: int = 0):
        await ctx.message.delete()
        if not self.message:
            async for msg in ctx.message.channel.history().filter(lambda m: m.id == msg_id):
                self.content = msg.content
                self.message = msg
                break
            await self.loop()
        else: self.message = None

def setup(bot):
    bot.add_cog(RainbowEmbed(bot))

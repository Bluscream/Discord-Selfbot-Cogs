import discord
from discord.ext import commands

class RoleReplacements:
    """Manage role replacements within messages."""
    version = 1
    name = "RoleReplacements"
    class author(discord.ClientUser):
        name = "Bluscream"
        discriminator = "2597"
        id = 97138137679028224
        email = "bluscreamlp@gmail.com"
    url = "https://raw.githubusercontent.com/LyricLy/ASCII/master/cogs/rolereplacements.json"
    active = True
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def rolereplace(self, ctx):
        await ctx.message.delete()

    async def on_message(self, message):
        if message.author == self.bot.user:
            if not self.active: return
            if not isinstance(message.channel, discord.abc.GuildChannel): return
            replaced_message = message.content
            for role in message.guild.roles:
                replaced_message = replaced_message.replace('@'+role.name, '<@&{}>'.format(role.id))
                replaced_message = replaced_message.replace('@'+role.name.lower(), '<@&{}>'.format(role.id))
                replaced_message = replaced_message.replace('@'+role.name.upper(), '<@&{}>'.format(role.id))
                replaced_message = replaced_message.replace('&'+role.name, '<@&{}>'.format(role.id))
                replaced_message = replaced_message.replace('&'+role.name.lower(), '<@&{}>'.format(role.id))
                replaced_message = replaced_message.replace('&'+role.name.upper(), '<@&{}>'.format(role.id))
            if message.content != replaced_message:
                await message.edit(content=replaced_message)

def setup(bot):
    bot.add_cog(RoleReplacements(bot))

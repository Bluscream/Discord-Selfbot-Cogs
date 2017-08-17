import discord, asyncio, datetime
from requests import post
from discord.ext import commands
from cogs.utils.checks import *

class DMProtect:
    """Protects you against DM invite spammers"""
    version = 1
    class author(discord.ClientUser):
        name = "Bluscream"
        discriminator = "2597"
        id = 97138137679028224
        email = "bluscreamlp@gmail.com"
    url = "https://raw.githubusercontent.com/LyricLy/ASCII/master/cogs/dmprotect.json"

    def __init__(self, bot):
        self.active = True
        self.block = True
        self.gban = True
        self.report = False
        self.invites = ['discord.gg', 'discord.io', 'discordapp.com/invite', 'paypal.me', 'patreon.com']
        self.bot = bot

    async def on_message(self, message):
        if not self.active: return
        if message.author.id == self.bot.user.id: return
        if not isinstance(message.channel, discord.abc.PrivateChannel): return
        if message.author.is_friend(): return
        messages = await message.channel.history(limit=2).flatten()
        if not len(messages) == 1: return
        for invite in self.invites:
            if invite in message.content:
                _msg = ""
                await message.ack()
                _msg += "acked"
                if self.block:
                    await message.author.block()
                    _msg += "/blocked"
                if not message.author.bot:
                    if self.gban:
                        for guild in self.bot.guilds:
                            if guild.me.guild_permissions.ban_members:
                                await guild.ban(message.author, reason="Server invite in first private message. ({})".format(invite), delete_message_days=0)
                        _msg += "/banned"
                    if self.report:
                        _banned = post('https://bans.discordlist.net/api', data=[('token', 'rnRKaAhkVX'), ('userid', str(message.author.id))]).text
                        if _banned == "False":
                            channel = self.bot.get_guild(269262004852621312).get_channel(269274277059100672)
                            await channel.send('=submit {}#{}|{}|Server invite in first private message. ({})|http://imgur.com/'.format(message.author.name,message.author.discriminator,message.author.id, invite))
                            await self.bot.wait_for('message', check=lambda m: m.author.id == 222853335877812224 and ' is this correct?(answer yes or no)' in m.content)
                            await channel.send('yes')
                            _msg += "/reported"
                return print('Automatically {} user {} for sending an invite link ({}) in their first private message to you.'.format(_msg, message.author, invite))

    @commands.command(aliases=['dmp'])
    async def dmprotect(self, ctx):
        """Toggles DM Invite Protection."""
        await ctx.message.delete()
        self.active = not self.active
        await ctx.send(self.bot.bot_prefix + 'DM Protection set to: `{}`'.format(self.active))

def setup(bot):
    bot.add_cog(DMProtect(bot))

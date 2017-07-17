import discord, asyncio
from discord.ext import commands
from cogs.utils.checks import *
import json

def save_json(self, filename, data):
    """Atomically saves json file"""
    rnd = randint(1000, 9999)
    path, ext = splitext(filename)
    tmp_file = "{}-{}.tmp".format(path, rnd)
    with open(filename, encoding='utf-8', mode="w") as f:
        json.dump(data, f, indent=4,sort_keys=True,
            separators=(',',' : '))
    try:
        read_json(tmp_file)
    except json.decoder.JSONDecodeError:
        self.logger.exception("Attempted to write file {} but JSON "
                              "integrity check on tmp file has failed. "
                              "The original file is unaltered."
                              "".format(filename))
        return False
    replace(tmp_file, filename)
    return True
        
def read_json(self, filename):
    with open(filename, encoding='utf-8', mode="r") as f:
        data = json.load(f)
    return data


class nickprotect:

    def __init__(self, bot):
        self.bot = bot
        self.active = read_json('settings/nickprotect/settings.json')
        self.allowed = False
        config = load_config()
        self.bot_prefix = config["bot_identifier"]
    
    async def on_member_update(self, before, after):
        if after.id == self.bot.user.id: return
        if not self.active: return
        if not before == self.bot.user: return
        if before.nick == after.nick: return
        if self.allowed: self.allowed = False; return
        if before.server.id in self.active or after.server.id in self.active:
            try:
                self.allowed = True
                await self.bot.change_nickname(before, before.nick)
                print("Someone tried to change my nickname from \"{b}\" to \"{a}\" on server \"{s}\"!".format(b=before.nick,a=after.nick,s=before.server.name))
            except discord.Forbidden: print("Insufficient to protect own nickname \"{n}\" on server \"{s}\"".format(n=before.nick,s=before.server.name))

    @commands.command(aliases=['np'], pass_context=True)
    async def nickprotect(self, ctx):
        """Toggles nickprotect mode so you keep your nick when you have enough permissions."""
        if ctx.message.server.id in self.active:
            self.active.remove(ctx.message.server.id)
            await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + 'Nickprotect disabled on this Server')
        else:
            self.active.append(ctx.message.server.id)
            await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + 'Nickprotect enabled on this Server')
        save_json('settings/nickprotect/settings.json', self.active)

def check_folder():
    if not exists("settings/nickprotect"):
        print("[NickProtect]Creating settings/terminal folder...")
        makedirs("settings/nickprotect")


def check_file():
    jdict = []

    if not dataIO.is_valid_json("settings/nickprotect/settings.json"):
        print("[NickProtect]Creating default settings.json...")
        dataIO.save_json("settings/nickprotect/settings.json", jdict)
        
def setup(bot):
    bot.add_cog(nickprotect(bot))

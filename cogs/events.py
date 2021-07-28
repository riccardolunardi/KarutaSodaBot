import discord, random, time
from discord.ext import commands, tasks


class EventsCog(commands.Cog, name="Events"):
    def __init__(self, bot):
        self.bot = bot

    async def add_reaction_event(self, drop):
        if self.bot.user.id != int(INSERT_MASTER_OF_MASTERS_ID):
            self.bot.logger.debug("Non grabbing the egg because I'm not the master")
            return None
        for reaction in drop.reactions:
            if reaction.emoji not in ["1️⃣", "2️⃣", "3️⃣"]:
                print("Adding:", reaction)
                self.bot.logger.debug("Adding: {}".format(reaction))
                await drop.add_reaction(reaction.emoji)


def setup(bot):
    bot.add_cog(EventsCog(bot))

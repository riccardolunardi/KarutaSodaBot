import asyncio, random
from discord.ext import commands
import utils.trading_utilities as trading_utilities


class TradeMasterCog(commands.Cog, name="TradeMaster"):
    def __init__(self, bot):
        self.bot = bot
        self.ktrade_channel = None

    @commands.command()
    async def mastertrade(self, ctx, new_slave, real_master):
        if str(self.bot.user.id) in new_slave:
            await trading_utilities.trading_slave(self, real_master, "real")

    # If triggered, it shows the user's card collection, in descending order of wishlist
    @commands.command()
    async def masterevent(self, ctx):
        await asyncio.sleep(random.randint(1, 4))  # If they send it all together it could be detected
        await ctx.channel.send(random.choice(["k!event", "kevent"]))
        self.bot.logger.debug('k!event')

    async def start_trade(self, message):
        await trading_utilities.trading_master(self, message)


def setup(bot):
    bot.add_cog(TradeMasterCog(bot))

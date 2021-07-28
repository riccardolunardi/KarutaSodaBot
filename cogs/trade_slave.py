import asyncio, random
from discord.ext import commands, tasks
import utils.trading_utilities as trading_utilities


class TradeSlaveCog(commands.Cog, name="TradeSlave"):
    def __init__(self, bot):
        self.bot = bot
        self.ktrade_channel = None
        self.trading_loop.start()

    @commands.command()
    async def trade(self, ctx):
        self.bot.logger.debug(f'{self.bot.user}, I have received the trade request')
        if self.bot.user in ctx.message.mentions:
            await self.trading_loop()

    @tasks.loop(minutes=random.randint(6 * 60, 8 * 60))
    async def trading_loop(self):
        await trading_utilities.trading_slave(self, self.bot.master, "real")

    @trading_loop.before_loop
    async def before_trading_loop(self):
        await self.bot.wait_until_ready()
        if self.bot.first_cycle:
            print(f'I\'m {self.bot.user}, waiting {self.bot.turn} to trade')
            self.bot.logger.debug(f'I\'m {self.bot.user}, waiting {self.bot.turn} to trade')
            await asyncio.sleep(self.bot.turn + random.randint(1 * 60, 8 * 60))
            self.bot.first_cycle = False


def setup(bot):
    bot.add_cog(TradeSlaveCog(bot))

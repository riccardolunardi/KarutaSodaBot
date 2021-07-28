import asyncio, discord, random, time
from discord.ext import commands, tasks

from utils.general_utilites import get_response_from_message


class BurnCog(commands.Cog, name="Burn"):
    def __init__(self, bot):
        self.bot = bot
        self.burn.start()

    @tasks.loop(minutes=random.randint(12 * 60, 13 * 60))
    async def burn(self):
        await self.bot.wait_until_ready()
        await self.burn_manager("w<=3 n>500")

    @commands.command()
    async def burncards(self, ctx, args):
        if self.bot.user in ctx.message.mentions:
            self.bot.logger.debug(f'{self.bot.user}, I have received the burning request')
            await self.burn_manager(args)


    async def burn_manager(self, conditions):
        await self.bot.wait_until_ready()
        self.bot.logger.debug("{} has started the burning procedure".format(self.bot.user))
        print("{} has started the burning procedure".format(self.bot.user))
        
        karuta = self.bot.get_channel(self.bot.ktrade_channel)
        await asyncio.sleep(random.randint(1, 60))

        conditions = " " + conditions
        burn_choices = ["k!multiburn", "k!mb", "kmb", "kmultiburn"]

        kmultiburn = await get_response_from_message(karuta, random.choice(burn_choices) + conditions, random.randint(2, 4))

        await kmultiburn.add_reaction("✅")
        await asyncio.sleep(random.randint(2, 7))
        await kmultiburn.add_reaction("🔥")
        print("Multiburn completed")
        self.bot.logger.debug(f'Multiburn completed')

    @burn.before_loop
    async def before_burn(self):
        await self.bot.wait_until_ready()
        if self.bot.first_cycle:
            print(f'I\'m {self.bot.user}, waiting {self.bot.turn} for the burn')
            self.bot.logger.debug(f'I\'m {self.bot.user}, waiting {self.bot.turn} for the burn')
            await asyncio.sleep(self.bot.turn)
            self.bot.first_cycle = False

    @burn.error
    async def send_kd_exception(self, exception):
        await self.bot.loop_unhandled_exception(exception, "k!multiburn")
        self.burn.restart()


def setup(bot):
    bot.add_cog(BurnCog(bot))

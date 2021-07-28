import asyncio
import random
import json

from discord.ext import commands, tasks

import utils.trading_utilities as trading_utilities


class TradeRandomCog(commands.Cog, name="TradeRandom"):
    def __init__(self, bot):
        self.bot = bot
        self.ktrade_channel = None
        self.random_trading_loop.start()

    async def random_trading(self):
        if random.choice([True, False]):
            await self.bot.wait_until_ready()

            dipendenti = await self.get_dipendenti_list()
            if dipendenti:
                await trading_utilities.trading_slave(self, random.choice(dipendenti), "antisgamo")

    @tasks.loop(minutes=random.randint(6 * 60, 9 * 60))
    async def random_trading_loop(self):
        await self.random_trading()

    @random_trading_loop.before_loop
    async def before_random_trading_loop(self):
        await self.bot.wait_until_ready()
        if self.bot.first_cycle:
            print(f'I\'m {self.bot.user}, waiting {self.bot.turn} for the random trade')
            self.bot.logger.debug(f'I\'m {self.bot.user}, waiting {self.bot.turn} for the random trade')
            await asyncio.sleep(self.bot.turn + random.randint(1 * 60, 8 * 60))
            self.bot.first_cycle = False

    async def get_dipendenti_list(self):
        await self.set_trading_channel()
        await asyncio.sleep(1, 50)
        server = self.ktrade_channel.guild

        for role in server.roles:
            if "Dipendenti" == role.name: #TO DO
                role_id = role
                break
        else:
            return

        dipendenti = []
        for member in server.members:
            if role_id in member.roles and member.name != self.bot.user.name:
                dipendenti.append(member)

        if not dipendenti:
            with open("options.json","r") as options:
                user_data = json.load(options)
            
            user_list = []
            for users_set in user_data["guilds"]["premium"]:
                user_list += users_set["users"]
            
            user_list = [user["name"] for user in user_list if user["name"] not in self.bot.user.name]
            dipendenti = user_list

        return dipendenti

    async def set_trading_channel(self):
        if self.ktrade_channel is None:
            self.ktrade_channel = self.bot.get_channel(self.bot.ktrade_channel)


def setup(bot):
    bot.add_cog(TradeRandomCog(bot))

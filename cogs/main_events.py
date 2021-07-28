import asyncio, discord, random, sys, time, traceback
import utils.trading_utilities as trading_utilities
from discord.ext import commands, tasks
import pprint

class MainCog(commands.Cog, name = "Main"):
    def __init__(self, bot):
        self.bot = bot
        self.daily.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print('KarutaSoda started for {}'.format(self.bot.user))
        self.bot.logger.debug('KarutaSoda started for {}'.format(self.bot.user))
        

    @commands.Cog.listener()
    async def on_message(self, message):
        # To grab more cards
        #print(message.author.id, message.content, message.mentions, message.attachments)
        if (message.author.id == self.bot.id_karuta and message.channel.id == self.bot.kdrop_channel and self.bot.user not in message.mentions and message.attachments) or "before dropping more card" in message.content:
            grab = self.bot.get_cog("Grab")
            await grab.additional_grab(message)

        if message.author.id == self.bot.id_karuta and message.channel.id == self.bot.ktrade_channel and self.bot.user in message.mentions and "would you like to trade with" in message.content:
            master = self.bot.get_cog("TradeMaster")

            if (self.bot.user == message.mentions[0] or master) and self.bot.user != message.mentions[1]:
                self.bot.logger.debug('Trading with slave')
                try:
                    await master.start_trade(message)
                except AttributeError as e:
                    print(e, "I'm not a master, trading just to not been detected")
                    antisgamo_trade = self.bot.get_cog("TradeRandom")
                    await trading_utilities.trading_master(self, message)

    # K!daily ez
    @tasks.loop(minutes=24*60+1)
    async def daily(self):
        await self.bot.wait_until_ready()
        kdrop_channel_instance = self.bot.get_channel(self.bot.kdrop_channel)
        await kdrop_channel_instance.send(random.choice(["k!daily","kdaily"]))
        self.bot.logger.debug('k!daily')

    @daily.before_loop
    async def before_daily(self):
        await self.bot.wait_until_ready()
        if self.bot.first_cycle:
            print(f'I\'m {self.bot.user}, waiting for {self.bot.turn} k!daily')
            await asyncio.sleep(self.bot.turn)
            self.bot.first_cycle = False

    @daily.error
    async def daily_exceptions(self, exception):
        await self.bot.loop_unhandled_exception(exception, "k!daily")
        self.daily.restart()
    
    # If triggered, it shows the user's card collection, in descending order of wishlist
    @commands.command()
    async def info(self, ctx):
        await asyncio.sleep(random.randint(1,50)) # Randomizing
        await ctx.channel.send(random.choice(["k!collection o:w","k!c o:w","kc o:w","kcollection o:w"]))
        self.bot.logger.debug('k!collection')

    # If triggered it shows the user's inventory
    @commands.command()
    async def inve(self, ctx):
        await asyncio.sleep(random.randint(1,40)) # Randomizing
        await ctx.channel.send(random.choice(["k!i","ki"]))
        self.bot.logger.debug('k!invent')

    # If triggered it shows the user's inventory
    @commands.command()
    async def lice(self, ctx):
        await asyncio.sleep(random.randint(1,3)) # Randomizing
        if self.bot.user in ctx.message.mentions:
            await ctx.channel.send("k!buy trade license")
            await asyncio.sleep(4)

            buying_message = (await ctx.history(limit=1).flatten())[0]

            await buying_message.add_reaction("✅")
            await asyncio.sleep(2)

            await ctx.channel.send("k!use trade license")

            await asyncio.sleep(2)

            buying_message = (await ctx.history(limit=1).flatten())[0]

            await buying_message.add_reaction("✅")

def setup(bot):
    bot.add_cog(MainCog(bot))

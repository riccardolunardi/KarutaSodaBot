import asyncio, discord, random, time, traceback
from Drop import Drop
from discord.ext import commands, tasks


class DropCog(commands.Cog, name="Drop"):
    def __init__(self, bot):
        self.bot = bot
        self.send_kd.start()

    @tasks.loop(seconds=random.randint(30 * 60 + 10, 31 * 60 + 20))
    async def send_kd(self):
        await self.bot.wait_until_ready()

        await asyncio.sleep(random.randint(2, 3))

        self.bot.logger.debug("k!drop")
        kdrop_channel_instance = self.bot.get_channel(self.bot.kdrop_channel)

        kd_message = await kdrop_channel_instance.send(random.choice(["k!d", "k!drop", "kd", "kdrop"]))

        await asyncio.sleep(random.randint(2, 3))

        karuta_mex = await kdrop_channel_instance.history(limit=1, after=kd_message).flatten()

        try:
            await asyncio.sleep(random.randint(2, 5))
            await self.grab(karuta_mex)

            # Managing events
            await asyncio.sleep(3)  # TEST
            karuta_mex = await kdrop_channel_instance.history(limit=1, around=karuta_mex[0]).flatten()

            # Logic event disabled
            if len(karuta_mex[0].reactions) > 3 and self.bot.master == 1:
                event = self.bot.get_cog("Events")
                await event.add_reaction_event(karuta_mex[0])


        except IndexError as e:
            try:
                print(e, ":", karuta_mex[0].content)
            except Exception as e:
                self.bot.logger.debug(str(e))
                self.bot.logger.debug(traceback.format_exc())
        except Exception as e:
            print(e)

    @send_kd.before_loop
    async def before_send_kd(self):
        await self.bot.wait_until_ready()
        if self.bot.first_cycle:
            print(f'I\'m {self.bot.user}, waiting {self.bot.turn} for a drop')
            await asyncio.sleep(self.bot.turn)
            self.bot.first_cycle = False

    @send_kd.error
    async def send_kd_exception(self, exception):
        await self.bot.loop_unhandled_exception(exception, "k!drop")
        self.send_kd.restart()

    async def grab(self, cards):
        drop_image = cards[0].attachments[0].url
        drop_content = Drop(drop_image)

        print(drop_content)
        choice = drop_content.get_choice()
        choice = DropCog.choice_to_emoji(choice)
        self.bot.logger.debug(str(drop_content) + " - Choice: " + choice)

        await cards[0].add_reaction(choice)

    @staticmethod
    def choice_to_emoji(choice):
        if choice == 1:
            return "1️⃣"
        elif choice == 2:
            return "2️⃣"
        return "3️⃣"


def setup(bot):
    bot.add_cog(DropCog(bot))

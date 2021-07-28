import asyncio, discord, time, random, re
from discord.ext import commands, tasks
from operator import attrgetter

from utils.general_utilites import get_response_from_message


class GrabCog(commands.Cog, name="Grab"):
    def __init__(self, bot):
        self.bot = bot

    async def additional_grab(self, message):
        # dm = await message.author.create_dm()
        await asyncio.sleep(random.randint(1, 20))
        dm = self.bot.get_channel(self.bot.spam_channel)

        k_cooldown = await get_response_from_message(dm, "k!cd", random.randint(0, 4))

        cooldowns = []

        try:
            for line in re.findall("(?<=\*\*).+?(?=\n)", k_cooldown.embeds[0].description + "\n"):
                time_to_wait = re.findall("(?<=`).+?(?=`)", line)
                if time_to_wait:
                    cooldowns.append(GrabCog.cd_to_seconds(time_to_wait[0]))
                else:
                    cooldowns.append(0)
        except IndexError as ie:
            print("Additional grab:", ie)
            return

        print(cooldowns)
        if len(message.reactions) > 3 and self.bot.master == 1:
            event = self.bot.get_cog("Events")
            await event.add_reaction_event(message)

        # The rule is that if the drop is available after the grab, then grabb
        if cooldowns[0] == 0 and cooldowns[1] > 10 * 60:
            try:
                print("Grabbing extra cards")
                await self.grab_extra(message)
            except Exception as e:
                print(e)

    async def grab_extra(self, cards):
        card_not_ever_chosen = min(cards.reactions, key=attrgetter('count'))
        await cards.add_reaction(card_not_ever_chosen)
        self.bot.logger.debug('Grabbing')

    @staticmethod
    def cd_to_seconds(string):
        if "minute" in string:
            return int(string.split(" ")[0]) * 60
        elif "second" in string:
            return int(string.split(" ")[0])


def setup(bot):
    bot.add_cog(GrabCog(bot))

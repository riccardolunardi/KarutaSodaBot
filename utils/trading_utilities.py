import discord, asyncio, random, re, traceback, sys
from utils.general_utilites import get_last_message_from

sys.path.insert(1, '/home/ubuntu/KarutaSoda/cogs/src')

from Items import Items

async def trading_slave(cog_trade, trader, antisgamo):
    cog_trade.bot.logger.debug("Trading master-master started")

    if cog_trade.ktrade_channel is None:
        cog_trade.ktrade_channel = cog_trade.bot.get_channel(cog_trade.bot.ktrade_channel)

    cards_to_trade = await get_cards_to_trade(cog_trade)
    inventory_to_trade = await get_items_to_trade(cog_trade)

    if cards_to_trade and inventory_to_trade:

        inve = Items(inventory_to_trade)

        if antisgamo == "antisgamo":
            cog_trade.bot.logger.debug("Trading antisgamo")
            cards_to_trade = cards_to_trade[0]
            #inventory_to_trade = inventory_to_trade[-1] # TO DO
            inventory_to_trade = inve.get_little()
        else:
            cog_trade.bot.logger.debug("Trading fr")
            cards_to_trade = ",".join(cards_to_trade[:int(len(inventory_to_trade)/3)])
            #inventory_to_trade = ",".join(inventory_to_trade[:-int(len(inventory_to_trade)*2/3)])
            inventory_to_trade = inve.get_percent()

        if not isinstance(trader, str):
            try:
                trader = trader.mentions
            except:
                trader = str(trader)

        await cog_trade.ktrade_channel.send(random.choice(["k!mt", "k!multitrade", "kmt", "kmultitrade"]) + " " + trader)
        await asyncio.sleep(random.randint(1, 2))
        init_trade = await get_last_message_from(cog_trade.ktrade_channel)

        def acceptance_check(reaction, user):
            print("slave:", user, reaction.emoji, trader)
            try:
                return init_trade == reaction.message and reaction.emoji == "☑️" and (str(user.id) in trader or trader in user.name.lower())
            except Exception as e:
                print(e)
                traceback.print_exc()
                return False

        try:
            reaction, user = await cog_trade.bot.wait_for('reaction_add', timeout=20.0, check=acceptance_check)
        except asyncio.TimeoutError:
            print("slave:", "Exchange procedure not started correctly")
        else:
            # print("slave:","Trading started")
            cog_trade.bot.logger.debug("slave: Trading started")
            # Synchronization point
            # await asyncio.sleep(random.randint(4,5))
            pending_emoji = "🔒"

            def check(reaction, user):
                print("slave:", user, reaction.emoji)
                return init_trade == reaction.message and reaction.emoji == pending_emoji and init_trade.author == user

            try:
                reaction, user = await cog_trade.bot.wait_for('reaction_add', timeout=25.0, check=check)
            except asyncio.TimeoutError:
                print("slave:", "Locking error")
            else:
                # print("slave","Lockable exchange from Karuta")
                cog_trade.bot.logger.debug("slave: Lockable exchange from Karuta")
                await asyncio.sleep(random.randint(3, 4))
                try:
                    await cog_trade.ktrade_channel.send(cards_to_trade)
                except discord.errors.HTTPException:
                    pass
                else:
                    await asyncio.sleep(random.randint(3, 4))

                try:
                    await cog_trade.ktrade_channel.send(inventory_to_trade)
                except discord.errors.HTTPException:
                    pass
                else:
                    await asyncio.sleep(random.randint(3, 4))

                await init_trade.add_reaction("🔒")
                pending_emoji = "✅"

                try:
                    reaction, user = await cog_trade.bot.wait_for('reaction_add', timeout=20.0, check=check)
                except asyncio.TimeoutError:
                    print("slave:", "Confirmation error")
                    cog_trade.bot.logger.debug("slave: Confirmation error")
                else:
                    await asyncio.sleep(random.randint(2, 4))
                    await init_trade.add_reaction("✅")
                    await asyncio.sleep(random.randint(2, 4))

                    print("slave:", "Exchange confirmed")
                    cog_trade.bot.logger.debug("slave: Exchange confirmed")

async def trading_master(trading_bot, message):
        await trading_bot.bot.wait_until_ready()

        ktrade_channel = trading_bot.bot.get_channel(trading_bot.bot.ktrade_channel)

        await asyncio.sleep(random.randint(2, 3))
        await message.add_reaction("☑️")

        # Synchronization point
        pending_emoji = "🔒"

        def check(reaction, user):
            return message == reaction.message and reaction.emoji == pending_emoji and message.author == user

        try:
            reaction, user = await trading_bot.bot.wait_for('reaction_add', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            print("master:", "Error during the lock")
            trading_bot.bot.logger.debug("master: Error during the lock")
        else:
            # print("master:","Lockable exchange from Karuta")
            trading_bot.bot.logger.debug("master: Lockable exchange from Karuta")

            #dummy_payment = "{} gold".format(random.randint(200, 400)) # TO CHANGE
            
            await asyncio.sleep(random.randint(13, 16))
            inventory_to_trade = await get_items_to_trade(trading_bot)
            inve = Items(inventory_to_trade)
            dummy_payment = inve.get_little()

            await ktrade_channel.send(dummy_payment)
            await asyncio.sleep(random.randint(2, 4))

            await message.add_reaction("🔒")
            pending_emoji = "✅"

            try:
                reaction, user = await trading_bot.bot.wait_for('reaction_add', timeout=20.0, check=check)
            except asyncio.TimeoutError:
                print("master:", "Error during confirmation")
                trading_bot.bot.logger.debug("master: Error during confirmation")
            else:
                print("master:", "Exchange confirmed by Karuta")
                trading_bot.bot.logger.debug("master: Exchange confirmed by Karuta")
                await asyncio.sleep(random.randint(2, 5))
                await message.add_reaction("✅")


async def get_cards_to_trade(cog_trade):
    await cog_trade.ktrade_channel.send(random.choice(["k!collection o:w", "k!c o:w", "kc o:w", "kcollection o:w"]))
    await asyncio.sleep(random.randint(4, 6))

    kc1 = await get_last_message_from(cog_trade.ktrade_channel)
    kc = kc1.embeds[0].description
    await asyncio.sleep(random.randint(1, 2))

    return kc_to_cards_code(kc)


async def get_items_to_trade(cog_trade):
    try:
        await cog_trade.ktrade_channel.send(random.choice(["kinventory", "k!inventory", "ki", "k!i"]))
    except:
        cog_trade.ktrade_channel = cog_trade.bot.get_channel(cog_trade.bot.ktrade_channel)
        await cog_trade.ktrade_channel.send(random.choice(["kinventory", "k!inventory", "ki", "k!i"]))

    await asyncio.sleep(random.randint(2, 4))
    
    # Retry
    for _ in range (0, 3):
        try:
            ki_embed = await get_last_message_from(cog_trade.ktrade_channel)
            ki = ki_embed.embeds[0].description
            break
        except Exception as e:
            print(e)
    else:
        raise IndexError
        

    quantity = re.findall("(?<=\*\*)([0-9,]+)(?=\*\*)", ki)  # <-- inventory quantity
    inv_codes = re.findall("(?<=`)[a-z ]+(?=`)", ki)  # <-- id inventory

    inventory = []

    for i in range(0, len(inv_codes)):
        inventory.append("{} {}".format(quantity[i].replace(",", ""), inv_codes[i]))

    return inventory


def kc_to_cards_code(kc_cards):
    card_codes = re.findall("(?<=\*\*`).+?(?=`\*\*)", kc_cards)
    if card_codes:
        card_codes = list(dict.fromkeys(card_codes))
        return card_codes
    return None

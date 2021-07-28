import asyncio


async def get_last_message_from(channel):
    return (await channel.history(limit=1).flatten())[0]


async def get_response_from_message(channel, message, time_to_sleep):
    await channel.send(message)
    await asyncio.sleep(time_to_sleep)
    return (await channel.history(limit=1).flatten())[0]

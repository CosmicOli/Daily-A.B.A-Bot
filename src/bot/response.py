import asyncio
import discord

import bot.globals as bg
import bot.utils as bu
import scraper.download as sd


async def sendMessageToChannel(channel, content, image):
    if (image is None):
        message = await channel.send(content=content)
    else:
        message = await channel.send(content=content, file=image)
        await message.edit(suppress=True)


async def sendPostToChannels(ordinal):
    content, image = bu.generateMessageContentAndImage(ordinal)

    for channel in bg.channels:
        await sendMessageToChannel(channel, content, image)
    return 0


async def respondWithPost(interaction: discord.Interaction, content: str, image: discord.File):
    if (image is None):
        await interaction.response.send_message(content=content)
    else:
        await interaction.response.send_message(content=content, file=image, suppress_embeds = True)
    

async def mainLoop():
    while True:
        await asyncio.sleep(1800) # 30 minutes timer
        flag = sd.downloadMostRecentPost()

        if (flag == 0):
            bu.updateCurrentDay()

            await sendPostToChannels(bg.day)



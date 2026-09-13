import asyncio
import discord

import bot.globals as bg
import bot.utils as bu
import scraper.download as sd


async def sendMessageToChannel(channel, content, image):
    removeEmbed = True
    if (image is None):
        removeEmbed = False

    message = await channel.send(content=content, file=image)
    await message.edit(suppress=removeEmbed)


async def sendPostToChannels(ordinal):
    content, image = bu.generateMessageContent(ordinal)

    for channel in bg.channels:
        await sendMessageToChannel(channel, content, image)
    return 0


async def respondWithPost(interaction: discord.Interaction, content: str, image: discord.File):
    removeEmbed = True
    if (image is None):
        removeEmbed = False
    
    await interaction.response.send_message(content=content, file=image, suppress_embeds = removeEmbed)


async def mainLoop():
    while True:
        await asyncio.sleep(1800) # 30 minutes timer
        flag = sd.downloadMostRecentPost()

        if (flag == 0):
            bu.updateCurrentDay()

            await sendPostToChannels(bg.day)



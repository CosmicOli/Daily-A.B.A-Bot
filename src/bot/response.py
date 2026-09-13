import asyncio
import discord

import bot.globals as bg
import bot.utils as bu
import scraper.download as sd
import scraper.tracker as st


async def sendMessageToChannel(channel, content, image):
    if (image is None):
        message = await channel.send(content=content)
    else:
        message = await channel.send(content=content, file=image)
        await message.edit(suppress=True)


async def sendPostToChannels(ordinal):
    entry = st.getPostTrackingEntry(ordinal)
    if (entry is None):
        raise Exception(f"No entry associated with '{ordinal}'")

    content = bu.generateMessageContent(ordinal, entry[2])

    for channel in bg.channels:
        image = bu.generateMessageImage(ordinal, entry[1])
        await sendMessageToChannel(channel, content, image)


async def respondWithPost(interaction: discord.Interaction, content: str, image: discord.File):
    if (image is None):
        await interaction.response.send_message(content=content)
    else:
        await interaction.response.send_message(content=content, file=image, suppress_embeds = True)
    

async def mainLoop():
    while True:
        await asyncio.sleep(1800) # 30 minutes timer
        try:
            flag = sd.downloadMostRecentPost()
        except:
            print("A DOWNLOAD ERROR HAS OCCURED IN MAIN LOOP")
        else:
            if (flag == 0):
                try:
                    bu.updateCurrentDay()
                except:
                    print("UNABLE TO UPDATE CURRENT DAY IN MAIN LOOP")

                try:
                    await sendPostToChannels(bg.day)
                except Exception:
                    print("UNABLE TO SEND POST TO AT LEAST ONE CHANNEL IN MAIN LOOP")



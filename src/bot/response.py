import asyncio
import discord

import bot.globals as bg
import bot.utils as bu
import scraper.download as sd
import scraper.globals as sg
import scraper.tracker as st
import scraper.utils as su

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
        await asyncio.sleep(10) # 30 minutes timer
        try:
            profileHTML = su.getHTMLFromLink(sg.profileLink)
        except Exception as e:
            print("A PROFILEHTML REQUEST ERROR HAS OCCURED IN MAIN LOOP: " + str(e))
        else:
            try:
                flag = sd.downloadMostRecentPostFromProfileHTML(profileHTML)
            except Exception as e:
                print("A DOWNLOAD ERROR HAS OCCURED IN MAIN LOOP: " + str(e))
            else:
                if (flag == 0):
                    try:
                        bu.updateCurrentDayFromProfileHTML(profileHTML)
                    except Exception as e:
                        print("UNABLE TO UPDATE CURRENT DAY IN MAIN LOOP: " + str(e))

                    try:
                        await sendPostToChannels(bg.day)
                    except Exception as e:
                        print("UNABLE TO SEND POST TO AT LEAST ONE CHANNEL IN MAIN LOOP: " + str(e))



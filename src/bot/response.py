import asyncio
import datetime
import discord
import re

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


# NOTE: When this function fails to send a post to a channel, the channel is removed from the bound list
# This ensures it cannot get cluttered with non existent channels, and also that all channels are attempted to be sent to without erroring out on a failed send attempt
# I also don't make it error out to the main loop as that would lead to channels receiving repeat posts; I could make a system that tracks which channels have been sent what posts and only send posts to channels that haven't recieved today's post, but I don't really want to tbh
async def sendPostToChannels(ordinal):
    entry = st.getPostTrackingEntry(ordinal)
    if (entry is None):
        raise Exception(f"No entry associated with '{ordinal}'")

    content = bu.generateMessageContent(ordinal, entry[2])

    removalQueue = []

    for channel in bg.channels:
        try:
            image = bu.generateMessageImage(ordinal, entry[1])
            await sendMessageToChannel(channel, content, image)
        except Exception as e:
            print(f"WARNING: failed to send post to channel '{channel.name}' (ID: {channel.id}) in server '{channel.guild.name}' (ID: {channel.guild.id})")
            print(f"Exception Text={e}")

            removalQueue.append(channel)

            try:
                await sendMessageToChannel(channel, "Failed to send daily post to this channel, please do /bind again to reenable daily posting", None)
            except Exception as e:
                print(f"WARNING: failed to send notification of unbinding to channel '{channel.name}' (ID: {channel.id}) in server '{channel.guild.name}' (ID: {channel.guild.id})")
                print(f"Exception Text={e}")

    # Removing the channel inside the other loop creates issues of not posting to channels after a failed channel in the list so I queue the removals instead
    for channel in removalQueue:
        try:
            await bu.unbindToChannel(channel)
        except Exception as e:
            print(f"WARNING: unbinding failure after failing to send post to channel '{channel.name}' (ID: {channel.id}) in server '{channel.guild.name}' (ID: {channel.guild.id})")
            print(f"Exception Text={e}")


async def respondWithPost(interaction: discord.Interaction, content: str, image: discord.File):
    if (image is None):
        await interaction.response.send_message(content=content)
    else:
        await interaction.response.send_message(content=content, file=image, suppress_embeds = True)
    

async def mainLoop():
    # Waits to do the check on every half hour of the clock, instead of being every half hour from running
    # Okay technically it is still every half hour but it will always happen during the minute of every 30 mins, offset by how long through the minute you were when you ran the code
    def getSleepTime():
        sleepTime = ((30 - datetime.datetime.now().minute) % 30) * 60
        if (sleepTime == 0):
            sleepTime = 1800 # 30 mins
        print(f"Waiting {sleepTime} seconds before update")
        return sleepTime
    await asyncio.sleep(getSleepTime())
    
    while True:
        print("") # Makes it easier to read
        currentDay = bg.day

        # I catch exceptions only to raise them again to make it explicitly clear and obvious which component of this function has failed
        try:
            try:
                profileHTML = su.getHTMLFromLink(sg.profileLink)
            except Exception as e:
                raise Exception("AN EXCEPTION IN THE PROFILEHTML REQUEST HAS OCCURED IN MAIN LOOP: " + str(e))
            else:
                try:
                    flag = sd.downloadMostRecentPostFromProfileHTML(profileHTML)
                except Exception as e:
                    raise Exception("AN EXCEPTION IN THE DOWNLOAD HAS OCCURED IN MAIN LOOP: " + str(e))
                else:
                    if (flag == 0):
                        try:
                            bu.updateCurrentDayFromProfileHTML(profileHTML)
                        except Exception as e:
                            raise Exception("UNABLE TO UPDATE CURRENT DAY IN MAIN LOOP: " + str(e))

                        try:
                            await sendPostToChannels(bg.day)
                        except Exception as e:
                            raise Exception("UNABLE TO SEND POST TO AT LEAST ONE CHANNEL IN MAIN LOOP: " + str(e))
        except Exception as e:
            print(e)

            # Resets the current day back to the previous day and untracks the new day
            # If the post was never tracked, this throws an exception; this is fine, hence why the exception is marked as a warning
            # The reason the post is removed from tracking is to allow for a clean attempt at downloading and sending today's post when the next timer ticks over
            try:
                ordinal = re.search(sg.ordinalMatch, profileHTML).group(1)
                st.untrackPost(ordinal)
                print(f"Successfully untracked post '{ordinal}'")
            except Exception as e:
                print("WARNING: failed to remove the presumably newly tracked post")
                print("WARNING NOTE: This may be a runon effect from the post never being tracked to begin with")
                print(f"Exception Text={e}")
            bg.day = currentDay

        # As the above code takes some amount of time to run, eventually the time would drift if a fixed 30 minute timer was used as the processing time would be added to the 30 minutes
        # Hence, I am making sure to always set the timer based on how many minutes it is until the next half hour on the clock  
        await asyncio.sleep(getSleepTime()) 



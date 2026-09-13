import re
import discord

import bot.globals as bg
import scraper.globals as sg
import scraper.tracker as st
import scraper.utils as su


def updateCurrentDay():
    profileHTML = su.getHTMLFromLink(sg.profileLink)
    bg.day = re.search(sg.ordinalMatch, profileHTML).group(1)


def generateMessageContent(ordinal):
    entry = st.getPostTrackingEntry(ordinal)
    if (not entry):
        return -1

    if (entry[1]):
        image = discord.File(f"Posts/{ordinal}.jpg")
    else:
        image = None

    bodyFile = open(f"Posts/{ordinal}.txt")
    body = bodyFile.read()
    bodyFile.close()

    return (body + "\n" + entry[2]), image


async def bindToChannel(channel: discord.channel):
    if (not channel in bg.channels):
        bg.channels.append(channel)
        return 0
    else:
        return 1
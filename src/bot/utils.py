import re
import discord

import bot.globals as bg
import scraper.globals as sg
import scraper.tracker as st
import scraper.utils as su


def updateCurrentDay():
    profileHTML = su.getHTMLFromLink(sg.profileLink)
    bg.day = re.search(sg.ordinalMatch, profileHTML).group(1)


def generateMessageContentAndImage(ordinal):
    entry = st.getPostTrackingEntry(ordinal)
    if (not entry):
        return -1

    if (entry[1]):
        try:
            image = discord.File(f"{sg.postsDirectory}{ordinal}.jpg")
        except FileNotFoundError:
            image = None
            print(f"WARNING: image for {ordinal} missing when marked as found")
    else:
        image = None

    try:
        bodyFile = open(f"{sg.postsDirectory}{ordinal}.txt")
        body = bodyFile.read()
        bodyFile.close()
    except FileNotFoundError:
        body = ""
        print(f"WARNING: body for {ordinal} missing while still tracked")
        
    return (body + "\n" + entry[2]), image


async def bindToChannel(channel: discord.channel):
    if (not channel in bg.channels):
        bg.channels.append(channel)
        return 0
    else:
        return 1
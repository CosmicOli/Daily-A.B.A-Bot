import re
import discord

import bot.globals as bg
import scraper.globals as sg
import scraper.tracker as st
import scraper.utils as su


def updateCurrentDay():
    profileHTML = su.getHTMLFromLink(sg.profileLink)
    try:
        bg.day = re.search(sg.ordinalMatch, profileHTML).group(1)
    except:
        raise Exception("Cannot find post to pull current day from")


def generateMessageContent(ordinal, link):
    try:
        bodyFile = open(f"{sg.postsDirectory}{ordinal}.txt")
        body = bodyFile.read()
        bodyFile.close()
    except FileNotFoundError:
        body = ""
        print(f"WARNING: body for {ordinal} missing while still tracked")

    return f"{body}\n{link}"


def generateMessageImage(ordinal, expectingImage):
    if (expectingImage == "True"):
        try:
            image = discord.File(f"{sg.postsDirectory}{ordinal}.jpg")
        except FileNotFoundError:
            image = None
            print(f"WARNING: image for {ordinal} missing when marked as found")
    else:
        image = None

    return image


def generateMessageContentAndImage(ordinal):
    entry = st.getPostTrackingEntry(ordinal)
    if (entry is None):
        raise Exception(f"No entry associated with '{ordinal}'")

    image = generateMessageImage(ordinal, entry[1])

    content = generateMessageContent(ordinal, entry[2])

    # As discord omits leading new line characters, no changes to this have to be made when body is an empty string
    return content, image


async def bindToChannel(channel: discord.channel):
    if (not channel in bg.channels):
        bg.channels.append(channel)
    else:
        raise Exception(f"Already bound to channel '{channel.name}' (ID: {channel.id})")
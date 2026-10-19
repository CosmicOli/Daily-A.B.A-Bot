import re
import discord

import bot.globals as bg
import scraper.globals as sg
import scraper.tracker as st
import scraper.utils as su


def updateCurrentDayFromProfileHTML(profileHTML):
    ordinal = su.getFirstOrdinalFromText(profileHTML)
    if (ordinal == None):
        raise Exception("Cannot find current day in profile HTML")
    else:
        bg.day = ordinal


def generateMessageContent(ordinal, link):
    try:
        bodyFile = open(f"{sg.postsDirectory}{ordinal}.txt", encoding="utf-8")
        body = bodyFile.read()
        bodyFile.close()
    except FileNotFoundError:
        body = ""
        print(f"WARNING: body for '{ordinal}' missing while still tracked")

    # As discord omits leading new line characters, no changes to this have to be made when body is an empty string
    return f"{body}\n{link}"


def generateMessageImage(ordinal, expectingImage):
    if (expectingImage == "True"):
        try:
            image = discord.File(f"{sg.postsDirectory}{ordinal}.jpg")
        except FileNotFoundError:
            image = None
            print(f"WARNING: image for '{ordinal}' missing when marked as found")
    else:
        image = None

    return image


def generateMessageContentAndImage(ordinal):
    entry = st.getPostTrackingEntry(ordinal)
    if (entry is None):
        raise Exception(f"No entry associated with '{ordinal}'")

    image = generateMessageImage(ordinal, entry[1])

    content = generateMessageContent(ordinal, entry[2])

    return content, image


async def bindToChannel(channel: discord.channel):
    if (not channel in bg.channels):
        bg.channels.append(channel)
    else:
        raise Exception(f"Already bound to channel '{channel.name}' (ID: {channel.id}) in server '{channel.guild.name}' (ID: {channel.guild.id})")


async def unbindToChannel(channel: discord.channel):
    if (channel in bg.channels):
        bg.channels.remove(channel)
    else:
        raise Exception(f"Already unbound channel '{channel.name}' (ID: {channel.id}) in server '{channel.guild.name}' (ID: {channel.guild.id})")